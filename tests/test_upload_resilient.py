"""Tests for the whole-upload re-sweep driver (Item 1) and the per-part work
unit (Items 4, 6, 7, 8).

The driver `_upload_parts_resilient` re-runs only the parts still failing after
each round, at halving concurrency, with completed parts keeping their ETags;
exactly-once for healthy parts; terminal (non-retryable) errors fail fast.

Most driver tests use a transport-free fake per-part callable (`_FakeUploader`)
— no HTTP. The eager/streaming/mint behaviors use the real `_upload_multipart`
with the storage pool + mint handler stubbed.
"""

from __future__ import annotations

import threading
from typing import Callable, Dict, List, Optional, Tuple

import pytest

from hotdata.models.finalize_upload_part import FinalizeUploadPart
from hotdata.uploads import (
    MalformedSessionError,
    StorageError,
    StorageTransportError,
    UploadError,
    _PartPlan,
    _round_in_flight,
    _round_delay,
    _upload_parts_resilient,
)


# --- pure helpers: concurrency halving + round backoff --------------------


def test_round_in_flight_halves_each_round_min_one() -> None:
    assert _round_in_flight(8, 0) == 8
    assert _round_in_flight(8, 1) == 4
    assert _round_in_flight(8, 2) == 2
    assert _round_in_flight(8, 3) == 1
    assert _round_in_flight(8, 4) == 1  # floored at 1
    assert _round_in_flight(1, 0) == 1
    assert _round_in_flight(8, 99) == 1  # large round → 1, no overflow


def test_round_delay_grows_exponentially() -> None:
    # base 2s → 2, 4, 8 before rounds 1, 2, 3; clamped so it can't overflow.
    assert _round_delay(1, base_delay=2.0) == pytest.approx(2.0)
    assert _round_delay(2, base_delay=2.0) == pytest.approx(4.0)
    assert _round_delay(3, base_delay=2.0) == pytest.approx(8.0)
    assert _round_delay(99, base_delay=2.0) < float("inf")


# --- transport-free fake per-part uploader --------------------------------


class _FakeUploader:
    """Records attempts per part number; can force the first K attempts of named
    parts to fail with a configurable exception; tracks peak concurrency.
    """

    def __init__(
        self,
        *,
        fail_counts: Optional[Dict[int, int]] = None,
        failure_factory: Optional[Callable[[int], BaseException]] = None,
        etag_for: Optional[Callable[[int], str]] = None,
    ) -> None:
        self._fail_counts = dict(fail_counts or {})
        self._failure_factory = failure_factory or (
            lambda pn: StorageTransportError(url=f"u{pn}", part_number=pn)
        )
        self._etag_for = etag_for or (lambda pn: f'"etag-{pn}"')
        self.attempts: Dict[int, int] = {}
        self._active = 0
        self.peak = 0
        self._lock = threading.Lock()

    def __call__(self, plan: "_PartPlan") -> FinalizeUploadPart:
        pn = plan.part_number
        with self._lock:
            self.attempts[pn] = self.attempts.get(pn, 0) + 1
            self._active += 1
            self.peak = max(self.peak, self._active)
            attempt_no = self.attempts[pn]
        try:
            remaining_failures = self._fail_counts.get(pn, 0)
            if attempt_no <= remaining_failures:
                raise self._failure_factory(pn)
            return FinalizeUploadPart(e_tag=self._etag_for(pn), part_number=pn)
        finally:
            with self._lock:
                self._active -= 1


def _plans(n: int, part_size: int = 1024) -> List[_PartPlan]:
    return [
        _PartPlan(index=i, part_number=i + 1, offset=i * part_size, length=part_size)
        for i in range(n)
    ]


def _run(uploader, n, *, base_in_flight=4, max_extra_rounds=3):
    return _upload_parts_resilient(
        _plans(n),
        uploader,
        base_in_flight=base_in_flight,
        max_extra_rounds=max_extra_rounds,
        round_base_delay=0.0,  # no real sleeps in tests
    )


# --- the bug + the fix ----------------------------------------------------


def test_repro_single_part_blip_sinks_without_rounds() -> None:
    # max_extra_rounds=0 reproduces the legacy "one failure sinks everything".
    up = _FakeUploader(fail_counts={3: 1})
    with pytest.raises(StorageTransportError):
        _run(up, 5, max_extra_rounds=0)


def test_single_part_blip_recovers_on_later_round() -> None:
    up = _FakeUploader(fail_counts={3: 1})
    parts = _run(up, 5)
    assert [p.part_number for p in parts] == [1, 2, 3, 4, 5]
    assert [p.e_tag for p in parts] == [f'"etag-{i}"' for i in range(1, 6)]
    assert up.attempts[3] == 2  # failed once, succeeded on the re-sweep
    for pn in (1, 2, 4, 5):
        assert up.attempts[pn] == 1  # healthy parts attempted exactly once


def test_multiple_flaky_parts_all_recover() -> None:
    up = _FakeUploader(fail_counts={1: 2, 3: 1, 5: 3})
    parts = _run(up, 6)
    assert [p.part_number for p in parts] == [1, 2, 3, 4, 5, 6]
    assert up.attempts[1] == 3
    assert up.attempts[3] == 2
    assert up.attempts[5] == 4
    assert up.attempts[2] == up.attempts[4] == up.attempts[6] == 1


def test_permanent_failure_surfaced_after_rounds() -> None:
    up = _FakeUploader(fail_counts={2: 99})
    with pytest.raises(StorageTransportError):
        _run(up, 4, max_extra_rounds=3)
    # 1 initial + 3 re-sweeps = 4 attempts for the doomed part.
    assert up.attempts[2] == 4
    # Healthy parts attempted exactly once.
    for pn in (1, 3, 4):
        assert up.attempts[pn] == 1


def test_happy_path_each_part_once() -> None:
    up = _FakeUploader()
    parts = _run(up, 10)
    assert len(parts) == 10
    assert all(v == 1 for v in up.attempts.values())


def test_concurrency_never_exceeds_base_cap() -> None:
    # 20 parts, base cap 3: many concurrent, but never more than 3 in flight.
    up = _FakeUploader()
    _run(up, 20, base_in_flight=3, max_extra_rounds=0)
    assert up.peak <= 3


# --- terminal errors fail fast (Item 2) -----------------------------------


def test_terminal_error_fails_fast_without_resweeping() -> None:
    up = _FakeUploader(
        fail_counts={2: 99},
        failure_factory=lambda pn: MalformedSessionError(f"contract violation part {pn}"),
    )
    with pytest.raises(MalformedSessionError):
        _run(up, 4)
    # Terminal: attempted exactly once, never re-swept.
    assert up.attempts[2] == 1


def test_generic_uploaderror_not_retried() -> None:
    # A deterministic local short-read (generic UploadError) is non-retryable.
    up = _FakeUploader(
        fail_counts={2: 99},
        failure_factory=lambda pn: UploadError("deterministic short read"),
    )
    with pytest.raises(UploadError):
        _run(up, 3)
    assert up.attempts[2] == 1


# --- result completeness --------------------------------------------------


def test_missing_slot_is_hard_error() -> None:
    # An uploader that returns None for a part (a bug) must not silently produce
    # a short finalize list.
    def bad(plan):
        if plan.part_number == 2:
            return None  # type: ignore[return-value]
        return FinalizeUploadPart(e_tag=f'"e{plan.part_number}"', part_number=plan.part_number)

    with pytest.raises(MalformedSessionError, match="never uploaded|part 2"):
        _upload_parts_resilient(
            _plans(3), bad, base_in_flight=2, max_extra_rounds=0, round_base_delay=0.0
        )


# --- progress exactly-once under retry (Item 8) ---------------------------


def test_progress_no_double_count_under_resweep() -> None:
    ticks: List[int] = []
    lock = threading.Lock()

    def on_progress(done: int) -> None:
        with lock:
            ticks.append(done)

    up = _FakeUploader(fail_counts={2: 1})
    parts = _upload_parts_resilient(
        _plans(3, part_size=100),
        up,
        base_in_flight=2,
        max_extra_rounds=3,
        round_base_delay=0.0,
        on_part_done=lambda plan: on_progress(plan.length),
    )
    assert len(parts) == 3
    # Part 2 failed round 0 then succeeded: counted exactly once. 3 parts × 100.
    assert sum(ticks) == 300
    assert len(ticks) == 3  # one tick per successful part, no double-count
