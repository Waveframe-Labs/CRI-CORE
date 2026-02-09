"""
---
title: "CRI-CORE Enforcement Contract Declaration Loader"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-02-09"
updated: "2026-02-09"

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
ai_assistance_details: "AI-assisted design of a minimal contract declaration load/extract surface aligned to the CRI-CORE enforcement contract."

dependencies:
  - "../run/structure.py"

anchors:
  - "CRI-CORE-ContractLoader-v0.1.0"
---
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


class ContractDeclarationError(Exception):
    """Raised when the contract declaration file is missing or unreadable."""


def load_contract_declaration(run_root: Path) -> Dict[str, Any]:
    """
    Load and parse runs/<RUN_ID>/contract.json.

    Structural parsing only. No interpretation of contract semantics.
    """
    contract_path = run_root / "contract.json"
    if not contract_path.exists():
        raise ContractDeclarationError("Missing contract.json")

    try:
        with contract_path.open("r", encoding="utf-8") as f:
            obj = json.load(f)
    except Exception as exc:
        raise ContractDeclarationError(f"Failed to parse contract.json: {exc}") from exc

    if not isinstance(obj, dict):
        raise ContractDeclarationError("contract.json must be a JSON object")

    return obj


def extract_contract_version(contract_obj: Dict[str, Any]) -> Optional[str]:
    """
    Extract contract_version from contract.json.

    Expected minimal shape:
      - contract_version: "X.Y.Z"
    """
    v = contract_obj.get("contract_version")
    return v if isinstance(v, str) else None


def extract_run_id(contract_obj: Dict[str, Any]) -> Optional[str]:
    """
    Extract run_id from contract.json.

    Expected minimal shape:
      - run_id: "<RUN_ID>"
    """
    rid = contract_obj.get("run_id")
    return rid if isinstance(rid, str) else None


def extract_created_utc(contract_obj: Dict[str, Any]) -> Optional[str]:
    """
    Extract created_utc from contract.json.

    Expected minimal shape:
      - created_utc: RFC3339 UTC string (e.g. 2026-02-09T16:12:34Z)
    """
    ts = contract_obj.get("created_utc")
    return ts if isinstance(ts, str) else None
