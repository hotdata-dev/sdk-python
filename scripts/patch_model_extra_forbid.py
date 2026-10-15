#!/usr/bin/env python3
"""Make request models reject unknown fields after OpenAPI regeneration.

The generated pydantic models use ``ConfigDict(populate_by_name=True,
validate_assignment=True, protected_namespaces=())``, which leaves pydantic's
default ``extra="ignore"`` in place: ``QueryRequest(sql=..., tiemout=5)`` or a
field this SDK release does not know yet is silently dropped and never sent.

This patch adds ``extra="forbid"`` to every **request** model so an unknown
keyword raises ``pydantic.ValidationError`` at construction. Request models
are found from the generated API classes — every model type used as a request
body — plus, transitively, every model those reference through their fields.
Response models are left alone on purpose: the server may add fields, and
their ``from_dict`` deserialisation must keep ignoring what this release does
not know. (A model shared by a request and a response gets ``forbid``; that is
safe because ``from_dict`` only ever passes known properties to pydantic.)

Idempotent: a model that already carries ``extra="forbid"`` is skipped. The
oneOf/anyOf wrapper models use a different ``ConfigDict`` and have no plain
fields to forbid on, so they are passed through without change (their leaf
alternatives are patched like any other model in the closure).
"""

from __future__ import annotations

import pathlib
import re
import sys
from typing import Dict, List, Set

ROOT = pathlib.Path(__file__).resolve().parents[1]
API_DIR = ROOT / "hotdata" / "api"
MODELS_DIR = ROOT / "hotdata" / "models"

CONFIG_OLD = (
    "    model_config = ConfigDict(\n"
    "        populate_by_name=True,\n"
    "        validate_assignment=True,\n"
    "        protected_namespaces=(),\n"
    "    )\n"
)
CONFIG_NEW = (
    "    model_config = ConfigDict(\n"
    "        populate_by_name=True,\n"
    "        validate_assignment=True,\n"
    "        protected_namespaces=(),\n"
    "        # Hand-applied (scripts/patch_model_extra_forbid.py): this is a\n"
    "        # request model, so an unknown keyword is a caller mistake (or a field\n"
    "        # this SDK release does not know) and must not be dropped silently.\n"
    "        extra=\"forbid\",\n"
    "    )\n"
)

_BODY_RE = re.compile(r"^\s+_body_params = (\w+)\s*$", re.M)
_MODEL_IMPORT_RE = re.compile(r"^from hotdata\.models\.(\w+) import (\w+)\s*$", re.M)


def _param_types(api_src: str, names: Set[str]) -> Set[str]:
    """Map body parameter names to the model class names in their annotations."""
    found: Set[str] = set()
    for name in names:
        # e.g. `    query_request: QueryRequest,` or
        # `    x: Annotated[Optional[FooRequest], Field(...)] = None,`
        pat = re.compile(
            r"^\s+" + re.escape(name) + r": (?:Annotated\[)?(?:Optional\[)?([A-Z]\w+)",
            re.M,
        )
        m = pat.search(api_src)
        if not m:
            sys.exit(f"Could not resolve the model type of body parameter {name!r}")
        found.add(m.group(1))
    return found


def request_body_models() -> Set[str]:
    """Class names of every model used as a request body by the generated APIs."""
    models: Set[str] = set()
    for api_file in sorted(API_DIR.glob("*_api.py")):
        src = api_file.read_text()
        names = set(_BODY_RE.findall(src))
        if names:
            models |= _param_types(src, names)
    return models


def model_index() -> Dict[str, pathlib.Path]:
    """Class name -> file for every generated model (from hotdata/models/__init__.py)."""
    init = (MODELS_DIR / "__init__.py").read_text()
    index: Dict[str, pathlib.Path] = {}
    for module, cls in _MODEL_IMPORT_RE.findall(init):
        index[cls] = MODELS_DIR / f"{module}.py"
    return index


def request_model_closure(index: Dict[str, pathlib.Path]) -> List[str]:
    """Request body models plus every model they reference, transitively."""
    seen: Set[str] = set()
    todo = sorted(request_body_models())
    while todo:
        cls = todo.pop()
        if cls in seen:
            continue
        seen.add(cls)
        path = index.get(cls)
        if path is None:
            sys.exit(f"Request model {cls} is not listed in hotdata/models/__init__.py")
        for _module, ref in _MODEL_IMPORT_RE.findall(path.read_text()):
            if ref not in seen:
                todo.append(ref)
    return sorted(seen)


def patch_models() -> None:
    index = model_index()
    patched: List[str] = []
    skipped: List[str] = []
    for cls in request_model_closure(index):
        path = index[cls]
        src = path.read_text()
        if 'extra="forbid"' in src:
            continue
        if CONFIG_OLD not in src:
            # oneOf/anyOf wrapper (ConfigDict without populate_by_name) or an
            # enum: nothing to forbid on.
            skipped.append(cls)
            continue
        path.write_text(src.replace(CONFIG_OLD, CONFIG_NEW, 1))
        patched.append(cls)
    print(f"extra='forbid' applied to {len(patched)} request models"
          + (f" (skipped {len(skipped)} wrapper/enum models: {', '.join(skipped)})" if skipped else ""))


def main() -> None:
    patch_models()


if __name__ == "__main__":
    main()
