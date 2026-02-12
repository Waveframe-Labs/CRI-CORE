"""
---
title: "CRI-CORE Run Contract Declaration Loader"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-02-09"
updated: "2026-02-11"

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
ai_assistance_details: "AI-assisted implementation of a minimal structural loader for CRI run contract declarations, enforcing only presence and structural fields required by the CRI-CORE enforcement contract."

dependencies:
  - "../errors.py"

anchors:
  - "CRI-CORE-ContractDeclarationLoader-v0.1.0"
---
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Optional


class ContractDeclarationError(Exception):
    """
    Raised when a run contract declaration cannot be loaded or parsed.
    """
    pass


def load_contract_declaration(run_root: Path) -> Mapping[str, Any]:
    """
    Load and minimally parse runs/<RUN_ID>/contract.json.

    Structural enforcement only:
      - file exists
      - valid JSON
      - root is an object
    """

    contract_path = run_root / "contract.json"

    if not contract_path.exists():
        raise ContractDeclarationError("contract.json is missing")

    if not contract_path.is_file():
        raise ContractDeclarationError("contract.json is not a file")

    try:
        raw = contract_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ContractDeclarationError(
            f"failed to read contract.json: {exc}"
        ) from exc

    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ContractDeclarationError(
            f"invalid JSON in contract.json: {exc}"
        ) from exc

    if not isinstance(obj, Mapping):
        raise ContractDeclarationError("contract.json must contain a JSON object")

    return obj


def extract_contract_version(contract_obj: Mapping[str, Any]) -> Optional[str]:
    value = contract_obj.get("version")
    if isinstance(value, str):
        return value
    return None


def extract_run_id(contract_obj: Mapping[str, Any]) -> Optional[str]:
    value = contract_obj.get("run_id")
    if isinstance(value, str):
        return value
    return None


def extract_created_utc(contract_obj: Mapping[str, Any]) -> Optional[str]:
    value = contract_obj.get("created_utc")
    if isinstance(value, str):
        return value
    return None
