"""
---
title: "CRI-CORE Structural Binding Artifact Builder"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.2.0"
doi: "TBD-0.2.0"
status: "Active"
created: "2026-02-27"
updated: "2026-02-27"

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
  - "../contract/loader.py"

anchors:
  - "CRI-CORE-BindingBuilder-v0.2.0"
---
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Optional


# These match the demo names you called out.
DECLARED_LOG_PATHS = [
    "transitions/transition-log.json",
    "transitions/rejection-log.json",
]


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _version_tuple(v: str) -> tuple[int, int, int]:
    parts = v.split(".")
    if len(parts) != 3:
        raise ValueError(f"invalid contract_version (expected X.Y.Z): {v}")
    return (int(parts[0]), int(parts[1]), int(parts[2]))


def _contract_at_least(contract_version: str, minimum: str) -> bool:
    return _version_tuple(contract_version) >= _version_tuple(minimum)


def compute_binding_obj(run_root: Path) -> Dict[str, Any]:
    """
    Compute a deterministic binding object for a run directory (PURE; no writes).

    Binding is structural-only and binds *specific* artifacts by hash:
      - contract.json (required)
      - claim artifact referenced by contract.json: claim_ref (required for contract_version >= 0.3.0)
      - approval.json (optional)
      - declared logs (optional when absent; hashed explicitly when present):
          transitions/transition-log.json
          transitions/rejection-log.json

    Output includes a binding_hash computed deterministically from component hashes.

    NOTE:
      - This is tamper-evidence (not signatures).
      - Claim/log semantics are not interpreted; only file bytes are hashed.
    """
    run_root = run_root.resolve()

    contract_path = run_root / "contract.json"
    if not contract_path.exists():
        raise FileNotFoundError("contract.json missing")

    contract_obj = _load_json(contract_path)

    contract_version = contract_obj.get("contract_version")
    if not isinstance(contract_version, str) or not contract_version.strip():
        raise ValueError("contract.json missing valid contract_version")

    contract_hash = _sha256_file(contract_path)

    # claim_ref is required starting at 0.3.0 (your chosen hardening seam)
    claim_ref = contract_obj.get("claim_ref")
    claim_hash: Optional[str] = None
    claim_rel: Optional[str] = None

    if _contract_at_least(contract_version, "0.3.0"):
        if not isinstance(claim_ref, str) or not claim_ref.strip():
            raise ValueError("contract.json missing valid claim_ref for contract_version >= 0.3.0")

        claim_rel = claim_ref.strip()
        claim_path = run_root / claim_rel
        if not claim_path.exists():
            raise FileNotFoundError(f"declared claim_ref not found: {claim_rel}")

        claim_hash = _sha256_file(claim_path)
    else:
        # legacy behavior: claim_ref may not exist; binding still records contract hash
        if isinstance(claim_ref, str) and claim_ref.strip():
            claim_rel = claim_ref.strip()
            claim_path = run_root / claim_rel
            if claim_path.exists():
                claim_hash = _sha256_file(claim_path)

    approval_path = run_root / "approval.json"
    approval_hash: Optional[str] = _sha256_file(approval_path) if approval_path.exists() else None

    # Declared logs: explicit per-file hashes when present
    logs: Dict[str, Optional[str]] = {}
    for rel in DECLARED_LOG_PATHS:
        p = run_root / rel
        logs[rel] = _sha256_file(p) if p.exists() else None

    # Deterministic binding hash construction:
    # Order is fixed:
    #   1) contract_hash
    #   2) claim_hash (if present)
    #   3) approval_hash (if present)
    #   4) declared logs in lexical order by rel path, but only those present
    components = [contract_hash]
    if claim_hash is not None:
        components.append(claim_hash)
    if approval_hash is not None:
        components.append(approval_hash)

    for rel in sorted(logs.keys()):
        h = logs[rel]
        if h is not None:
            components.append(h)

    binding_hash = hashlib.sha256("".join(components).encode("utf-8")).hexdigest()

    return {
        "contract_version": contract_version,
        "contract_hash": contract_hash,
        "claim_ref": claim_rel,
        "claim_hash": claim_hash,
        "approval_hash": approval_hash,
        "declared_logs": {k: logs[k] for k in sorted(logs.keys())},
        "binding_hash": binding_hash,
    }


def write_binding(run_root: Path, binding_obj: Mapping[str, Any]) -> Path:
    """
    Write binding.json deterministically (writer; performs I/O).
    """
    run_root = run_root.resolve()
    binding_path = run_root / "binding.json"
    binding_path.write_text(json.dumps(dict(binding_obj), indent=2), encoding="utf-8")
    return binding_path


def build_binding_artifact(run_root: Path) -> Path:
    """
    Backward-compatible wrapper: compute + write binding.json.
    """
    obj = compute_binding_obj(run_root)
    return write_binding(run_root, obj)