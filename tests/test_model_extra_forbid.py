"""Request models reject unknown fields; response models keep ignoring them.

Applied by scripts/patch_model_extra_forbid.py (re-run by the regenerate
workflow): every model used as a request body, and every model nested in one,
carries `extra="forbid"`. A misspelled keyword or a field from a newer API that
this SDK release lacks fails loudly instead of vanishing from the request.
Response models stay forward-compatible so a newer server cannot break an
older SDK.
"""

from __future__ import annotations

import importlib
import re
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from hotdata.models.create_database_request import CreateDatabaseRequest
from hotdata.models.get_result_response import GetResultResponse
from hotdata.models.load_managed_table_request import LoadManagedTableRequest
from hotdata.models.query_request import QueryRequest
from hotdata.models.query_response import QueryResponse

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"


def _patch_module():
    sys.path.insert(0, str(SCRIPTS))
    try:
        return importlib.import_module("patch_model_extra_forbid")
    finally:
        sys.path.pop(0)


def test_unknown_kwarg_on_request_model_raises() -> None:
    with pytest.raises(ValidationError) as ei:
        QueryRequest(sql="SELECT 1", tiemout_ms=5)  # type: ignore[call-arg]  # typo
    assert "tiemout_ms" in str(ei.value)
    with pytest.raises(ValidationError):
        LoadManagedTableRequest(  # type: ignore[call-arg]
            data="x\n1\n", mode="replace", field_from_newer_api=True
        )
    with pytest.raises(ValidationError):
        CreateDatabaseRequest(name="db", unknown=1)  # type: ignore[call-arg]


def test_known_fields_and_aliases_still_work() -> None:
    req = LoadManagedTableRequest(data="x\n1\n", mode="replace")
    assert req.mode == "replace"
    # populate_by_name=True: both the field name and its wire alias are accepted.
    by_alias = LoadManagedTableRequest.from_dict({"data": "x\n1\n", "mode": "replace", "async": True})
    assert by_alias is not None and by_alias.var_async is True
    by_name = LoadManagedTableRequest.model_validate({"data": "x\n1\n", "mode": "replace", "var_async": True})
    assert by_name.var_async is True
    assert QueryRequest(sql="SELECT 1").to_dict()["sql"] == "SELECT 1"


def test_unknown_field_in_request_model_from_dict_is_dropped_not_rejected() -> None:
    # from_dict only ever passes known properties through, so a payload with an
    # extra key still deserialises (this mirrors how responses are parsed).
    req = QueryRequest.from_dict({"sql": "SELECT 1", "some_future_field": 1})
    assert req is not None and req.sql == "SELECT 1"
    assert not hasattr(req, "some_future_field")


def test_response_models_still_ignore_unknown_fields() -> None:
    resp = GetResultResponse.from_dict(
        {"result_id": "r1", "status": "ready", "rows": [[1]], "brand_new_field": 1}
    )
    assert resp is not None and resp.status == "ready"
    # A response model also accepts an unknown kwarg directly (extra is not
    # forbidden there), so a newer server can never break an older SDK.
    newer = GetResultResponse(result_id="r1", status="ready", brand_new_field=1)  # type: ignore[call-arg]
    assert newer.status == "ready"
    assert "extra" not in QueryResponse.model_config


def test_every_request_body_model_forbids_extras() -> None:
    mod = _patch_module()
    index = mod.model_index()
    closure = mod.request_model_closure(index)
    body_models = mod.request_body_models()
    assert {"QueryRequest", "LoadManagedTableRequest", "CreateDatabaseRequest"} <= body_models
    assert body_models <= set(closure)
    missing = []
    for cls in closure:
        src = index[cls].read_text()
        if 'extra="forbid"' in src:
            continue
        # The oneOf/anyOf wrappers carry a different ConfigDict and have no
        # plain fields to forbid on; anything else must have been patched.
        if re.search(r"^\s+(oneof|anyof)_schema_\d+_validator", src, re.M):
            continue
        missing.append(cls)
    assert missing == []


def test_patch_is_idempotent_and_wired_for_regeneration() -> None:
    mod = _patch_module()
    index = mod.model_index()
    before = {cls: index[cls].read_text() for cls in mod.request_model_closure(index)}
    mod.patch_models()
    after = {cls: index[cls].read_text() for cls in before}
    assert after == before
    workflow = (REPO_ROOT / ".github" / "workflows" / "regenerate.yml").read_text()
    assert "scripts/patch_model_extra_forbid.py" in workflow
