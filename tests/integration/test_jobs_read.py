"""Scenario: jobs_read.

Read-only: list_jobs returns the workspace job history, and get_job fetches a
single job by id (the first from the list, when any exist). Never starts a job;
tolerates an empty history.
"""

from __future__ import annotations

from hotdata.api.jobs_api import JobsApi


def test_jobs_read(jobs_api: JobsApi) -> None:
    listing = jobs_api.list_jobs()
    assert isinstance(listing.jobs, list)

    if not listing.jobs:
        # A fresh workspace may have no job history — that's a valid state.
        return

    first = listing.jobs[0]
    assert first.id
    assert first.status

    fetched = jobs_api.get_job(first.id)
    assert fetched.id == first.id
    assert fetched.status
