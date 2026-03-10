"""
---
title: "CRI-CORE Compiled Contract Loader"
filetype: "source"
type: "implementation"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-03-10"
updated: "2026-03-10"

author:
  name: "Shawn C. Wright"
  email: "swright@waveframelabs.org"
  orcid: "https://orcid.org/0009-0006-6043-9295"

maintainer:
  name: "Waveframe Labs"
  url: "https://waveframelabs.org"

license: "Apache-2.0"

copyright:
  holder: "Waveframe Labs"
  year: "2026"

ai_assisted: "partial"

dependencies:
  - "../../../schema/contract.schema.json"
  - "./errors.py"
  - "./model.py"

anchors:
  - "CRI-CORE-COMPILED-CONTRACT-LOADER-v0.1.0"
---
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator

from .errors import CompiledContractLoadError, CompiledContractValidationError
from .model import CompiledContract


SCHEMA_PATH = Path(__file__).resolve().parents[3] / "schema" / "contract.schema.json"


def _load_schema() -> Mapping[str, Any]:
    try:
        raw = SCHEMA_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        raise CompiledContractLoadError(
            f"failed to read compiled contract schema: {exc}"
        ) from exc

    try:
        schema = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CompiledContractLoadError(
            f"invalid JSON in compiled contract schema: {exc}"
        ) from exc

    if not isinstance(schema, Mapping):
        raise CompiledContractLoadError(
            "compiled contract schema must contain a JSON object"
        )

    return schema


_SCHEMA = _load_schema()
_VALIDATOR = Draft202012Validator(_SCHEMA)


def load_compiled_contract(path: Path) -> CompiledContract:
    """
    Load and validate a compiled contract artifact.

    This function performs:
      - file presence checks
      - JSON parsing
      - schema validation
      - normalization into a stable kernel-facing model

    It does not interpret governance semantics.
    """

    if not path.exists():
        raise CompiledContractLoadError(f"compiled contract file is missing: {path}")

    if not path.is_file():
        raise CompiledContractLoadError(f"compiled contract path is not a file: {path}")

    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CompiledContractLoadError(
            f"failed to read compiled contract file: {exc}"
        ) from exc

    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CompiledContractLoadError(
            f"invalid JSON in compiled contract file: {exc}"
        ) from exc

    if not isinstance(obj, Mapping):
        raise CompiledContractLoadError(
            "compiled contract file must contain a JSON object"
        )

    errors = sorted(_VALIDATOR.iter_errors(obj), key=lambda e: list(e.path))
    if errors:
        messages = []
        for err in errors:
            location = ".".join(str(part) for part in err.path)
            if location:
                messages.append(f"{location}: {err.message}")
            else:
                messages.append(err.message)

        raise CompiledContractValidationError(
            "compiled contract schema validation failed:\n- "
            + "\n- ".join(messages)
        )

    return CompiledContract.from_mapping(obj)