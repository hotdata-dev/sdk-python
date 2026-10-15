"""Unit tests for hotdata.loads: 409 RESOURCE_LOCKED retry of table loads.

The generated load methods are stubbed at the class level so no server is
needed, and time.sleep / random.random are patched so retry timing is
deterministic and instant. Covered:

* retry-then-succeed on 409 RESOURCE_LOCKED, honouring Retry-After;
* exponential backoff when no Retry-After is sent;
* exhaustion by max_retries and by the deadline budget -> TableLockedError;
* 409 CONFLICT / IDEMPOTENCY_KEY_CONFLICT and non-409 errors are never retried;
* the code is matched from exc.data or the raw JSON body, never the message;
* the enhanced classes are the default `hotdata.DatabasesApi` / `ConnectionsApi`.
"""

from __future__ import annotations

from typing import Any, Optional
from unittest.mock import patch

import pytest

from hotdata.api.connections_api import ConnectionsApi as _GeneratedConnectionsApi
from hotdata.api.databases_api import DatabasesApi as _GeneratedDatabasesApi
from hotdata.exceptions import ApiException, ConflictException
from hotdata.loads import (
    ConnectionsApi,
    DatabasesApi,
    LoadRetryPolicy,
    TableLockedError,
    error_code,
    is_resource_locked,
)
from hotdata.models.api_error_detail import ApiErrorDetail
from hotdata.models.api_error_response import ApiErrorResponse
from hotdata.models.load_managed_table_request import LoadManagedTableRequest
from hotdata.models.load_managed_table_response import LoadManagedTableResponse

REQ = LoadManagedTableRequest(data="x\n1\n", mode="replace")
ARGS = ("db1", "public", "t", REQ)


def _api(**kwargs: Any) -> DatabasesApi:
    return DatabasesApi(api_client=object(), **kwargs)


def _ok() -> LoadManagedTableResponse:
    return LoadManagedTableResponse(
        arrow_schema_json="{}",
        connection_id="conn1",
        row_count=1,
        schema_name="public",
        table_name="t",
    )


def _conflict(
    code: str = "RESOURCE_LOCKED",
    *,
    retry_after: Optional[str] = None,
    via: str = "data",
    message: str = "another operation is already running for t; retry shortly",
) -> ApiException:
    """A 409 as the generated client raises it (ConflictException)."""
    exc = ConflictException(status=409, reason="Conflict")
    exc.headers = {"Retry-After": retry_after} if retry_after is not None else {}
    body = '{"error":{"code":"%s","message":"%s"}}' % (code, message)
    if via == "data":
        exc.data = ApiErrorResponse(error=ApiErrorDetail(code=code, message=message))
        exc.body = body
    elif via == "body":
        exc.data = None
        exc.body = body
    else:
        raise AssertionError(via)
    return exc


# --- classification -----------------------------------------------------------


def test_error_code_from_data_and_from_body() -> None:
    assert error_code(_conflict(via="data")) == "RESOURCE_LOCKED"
    assert error_code(_conflict(via="body")) == "RESOURCE_LOCKED"
    bare = ApiException(status=409, reason="Conflict")
    assert error_code(bare) is None
    bare.body = "not json"
    assert error_code(bare) is None
    bare.body = '{"error": "string, not an object"}'
    assert error_code(bare) is None


def test_is_resource_locked_matches_code_not_message() -> None:
    assert is_resource_locked(_conflict("RESOURCE_LOCKED"))
    # Same wording, different code: must not be retried.
    assert not is_resource_locked(_conflict("CONFLICT"))
    assert not is_resource_locked(_conflict("IDEMPOTENCY_KEY_CONFLICT"))
    # Right code on a non-409 status is not a lock either.
    other = _conflict("RESOURCE_LOCKED")
    other.status = 423
    assert not is_resource_locked(other)
    assert not is_resource_locked(ValueError("x"))


# --- retry ----------------------------------------------------------------------


def test_success_passthrough_makes_one_call() -> None:
    resp = _ok()
    with patch.object(_GeneratedDatabasesApi, "load_database_table", return_value=resp) as m, \
            patch("hotdata.loads.time.sleep") as sleep:
        out = _api().load_database_table(*ARGS)
    assert out is resp
    assert m.call_count == 1
    sleep.assert_not_called()


def test_locked_then_succeed_honours_retry_after() -> None:
    resp = _ok()
    side = [_conflict(retry_after="5"), _conflict(retry_after="2"), resp]
    with patch.object(_GeneratedDatabasesApi, "load_database_table", side_effect=side) as m, \
            patch("hotdata.loads.time.sleep") as sleep, \
            patch("hotdata.loads.random.random", return_value=0.0):
        out = _api().load_database_table(*ARGS)
    assert out is resp
    assert m.call_count == 3
    assert [c.args[0] for c in sleep.call_args_list] == [5.0, 2.0]


def test_retry_after_gets_jitter_on_top_and_is_not_capped() -> None:
    side = [_conflict(retry_after="40"), _ok()]
    policy = LoadRetryPolicy(max_backoff_s=1.0, deadline_s=120.0, jitter=0.5)
    with patch.object(_GeneratedDatabasesApi, "load_database_table", side_effect=side), \
            patch("hotdata.loads.time.sleep") as sleep, \
            patch("hotdata.loads.random.random", return_value=1.0):
        _api(load_retry=policy).load_database_table(*ARGS)
    # 40s hint + 50% jitter; the per-delay cap does not dishonour the hint.
    assert sleep.call_args_list[0].args[0] == pytest.approx(60.0)


def test_exponential_backoff_without_retry_after() -> None:
    side = [_conflict(via="body"), _conflict(via="body"), _conflict(via="body"), _ok()]
    policy = LoadRetryPolicy(base_backoff_s=1.0, max_backoff_s=3.0, deadline_s=60.0)
    with patch.object(_GeneratedDatabasesApi, "load_database_table", side_effect=side), \
            patch("hotdata.loads.time.sleep") as sleep, \
            patch("hotdata.loads.random.random", return_value=0.0):
        _api(load_retry=policy).load_database_table(*ARGS)
    assert [c.args[0] for c in sleep.call_args_list] == [1.0, 2.0, 3.0]


def test_exhausts_max_retries() -> None:
    side = [_conflict(retry_after="1")] * 4
    policy = LoadRetryPolicy(max_retries=2, deadline_s=600.0)
    with patch.object(_GeneratedDatabasesApi, "load_database_table", side_effect=side) as m, \
            patch("hotdata.loads.time.sleep"), \
            patch("hotdata.loads.random.random", return_value=0.0):
        with pytest.raises(TableLockedError) as ei:
            _api(load_retry=policy).load_database_table(*ARGS)
    assert m.call_count == 3  # initial + 2 retries
    assert ei.value.attempts == 3
    assert ei.value.status == 409
    assert "RESOURCE_LOCKED" in str(ei.value)
    assert isinstance(ei.value.__cause__, ConflictException)
    # Last server response rides on the error for diagnostics.
    assert ei.value.headers == {"Retry-After": "1"}
    assert ei.value.data is not None


def test_exhausts_deadline_budget() -> None:
    # Retry-After of 30s against a 10s budget: give up before sleeping.
    side = [_conflict(retry_after="30"), _ok()]
    policy = LoadRetryPolicy(max_retries=10, deadline_s=10.0)
    with patch.object(_GeneratedDatabasesApi, "load_database_table", side_effect=side) as m, \
            patch("hotdata.loads.time.sleep") as sleep:
        with pytest.raises(TableLockedError) as ei:
            _api(load_retry=policy).load_database_table(*ARGS)
    assert m.call_count == 1
    sleep.assert_not_called()
    assert "budget" in ei.value.reason


@pytest.mark.parametrize("code", ["CONFLICT", "IDEMPOTENCY_KEY_CONFLICT"])
def test_other_409_codes_are_not_retried(code: str) -> None:
    boom = _conflict(code, retry_after="5")
    with patch.object(_GeneratedDatabasesApi, "load_database_table", side_effect=boom) as m, \
            patch("hotdata.loads.time.sleep") as sleep:
        with pytest.raises(ConflictException) as ei:
            _api().load_database_table(*ARGS)
    assert ei.value is boom
    assert not isinstance(ei.value, TableLockedError)
    assert m.call_count == 1
    sleep.assert_not_called()


def test_409_without_a_code_is_not_retried() -> None:
    boom = ConflictException(status=409, reason="Conflict")
    with patch.object(_GeneratedDatabasesApi, "load_database_table", side_effect=boom), \
            patch("hotdata.loads.time.sleep") as sleep:
        with pytest.raises(ConflictException):
            _api().load_database_table(*ARGS)
    sleep.assert_not_called()


def test_non_409_error_propagates_unchanged() -> None:
    boom = ApiException(status=413, reason="Payload Too Large")
    with patch.object(_GeneratedDatabasesApi, "load_database_table", side_effect=boom), \
            patch("hotdata.loads.time.sleep") as sleep:
        with pytest.raises(ApiException) as ei:
            _api().load_database_table(*ARGS)
    assert ei.value is boom
    sleep.assert_not_called()


def test_arguments_are_forwarded_verbatim() -> None:
    with patch.object(_GeneratedDatabasesApi, "load_database_table", return_value=_ok()) as m:
        _api().load_database_table(
            "db1", "public", "t", REQ, _request_timeout=5, _headers={"X-Test": "1"}
        )
    assert m.call_args.args == ("db1", "public", "t", REQ)
    assert m.call_args.kwargs == {"_request_timeout": 5, "_headers": {"X-Test": "1"}}


def test_connections_api_load_managed_table_retries_too() -> None:
    resp = _ok()
    side = [_conflict(retry_after="1"), resp]
    with patch.object(_GeneratedConnectionsApi, "load_managed_table", side_effect=side) as m, \
            patch("hotdata.loads.time.sleep") as sleep, \
            patch("hotdata.loads.random.random", return_value=0.0):
        out = ConnectionsApi(api_client=object()).load_managed_table("conn1", "public", "t", REQ)
    assert out is resp
    assert m.call_count == 2
    assert sleep.call_args_list[0].args[0] == 1.0


# --- wiring ---------------------------------------------------------------------


def test_enhanced_load_clients_are_the_default_export() -> None:
    import hotdata

    assert hotdata.DatabasesApi is DatabasesApi
    assert hotdata.ConnectionsApi is ConnectionsApi
    assert hotdata.LoadRetryPolicy is LoadRetryPolicy
    assert hotdata.TableLockedError is TableLockedError
    assert "LoadRetryPolicy" in hotdata.__all__
    assert "TableLockedError" in hotdata.__all__
    assert issubclass(DatabasesApi, _GeneratedDatabasesApi)
    assert issubclass(ConnectionsApi, _GeneratedConnectionsApi)


def test_loads_module_is_generator_ignored() -> None:
    from pathlib import Path

    ignore = (Path(__file__).resolve().parents[1] / ".openapi-generator-ignore").read_text()
    assert "hotdata/loads.py" in ignore.splitlines()
