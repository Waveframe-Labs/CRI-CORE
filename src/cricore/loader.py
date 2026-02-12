"""
---
title: "CRI-CORE Run Contract Loader"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-02-11"
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
ai_assistance_details: "AI-assisted implementation of a minimal, policy-free contract.json loader used to enforce the CRI run artifact contract version declaration (CRI-CORE contract §3.3)."

dependencies:
  - "./version.py"
  - "../errors.py"

anchors:
  - "CRI-CORE-ContractLoader-v0.1.0"
---
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Optional, Tuple


def _read_json_file(path: Path) -> Tuple[Optional[Mapping[str, Any]], Optional[str]]:
    """
    Load a JSON object from disk.

    Returns: (obj, error_message)
    - obj is a Mapping when successful, otherwise None
    - error_message is None on success, otherwise a human-readable string
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None, f"missing required file: {path.name}"
    except OSError as e:
        return None, f"failed to read {path.name}: {e}"

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as e:
        return None, f"invalid JSON in {path.name}: {e}"

    if not isinstance(parsed, Mapping):
        return None, f"{path.name} must contain a JSON object"

    return parsed, None


def load_run_contract(run_path: str) -> Tuple[Optional[Mapping[str, Any]], Optional[str]]:
    """
    Load and minimally validate the CRI run contract declaration.

    Contract surface:
      - runs/<RUN_ID>/contract.json

    This loader performs only structural validation:
      - contract.json exists
      - JSON is valid
      - root is a JSON object
      - contains a string field 'version'

    Returns: (contract_obj, error_message)
    """
    p = Path(run_path) / "contract.json"
    contract, err = _read_json_file(p)
    if err is not None:
        return None, err

    version = contract.get("version")
    if not isinstance(version, str) or not version.strip():
        return None, "contract.json must declare a non-empty string field: version"

    return contract, None
