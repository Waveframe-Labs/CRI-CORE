"""
---
title: "CRI-CORE Run Seal Builder"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.3.0"
doi: "TBD-0.3.0"
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
  - "./manifest.py"

anchors:
  - "CRI-CORE-RunSealBuilder-v0.3.0"
---
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Optional

from .manifest import build_integrity_manifest


EXCLUDED_FROM_SEAL = {
    "SEAL.json",
    "payload.tar.gz",
    "SHA256SUMS.txt",
}


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def compute_seal_obj(run_root: Path) -> Dict[str, Any]:
    """
    Compute the deterministic seal object for a run directory.

    IMPORTANT:
      - This function is PURE (no file writes).
      - This is tamper-evidence (NOT a signature).

    Seal model:
      - Hash ALL files under run_root (recursive) in deterministic order,
        excluding: SEAL.json, payload.tar.gz, SHA256SUMS.txt
      - Also include component hashes of SHA256SUMS.txt and payload.tar.gz
        when present (explicit top-level components).

    Returns:
      A JSON-serializable dict containing:
        - contract_version
        - sha256sums_hash (optional)
        - payload_hash (optional)
        - sealed_files (mapping relpath -> sha256)
        - seal_hash (sha256 of concatenated component hashes in deterministic order)
    """

    run_root = run_root.resolve()

    contract_path = run_root / "contract.json"
    if not contract_path.exists():
        raise FileNotFoundError("contract.json missing (seal requires run root)")

    contract_obj = _load_json(contract_path)
    cv = contract_obj.get("contract_version")
    if not isinstance(cv, str) or not cv.strip():
        raise ValueError("contract.json missing valid contract_version")

    # Deterministic manifest of run files (excludes payload + SHA by design).
    manifest = build_integrity_manifest(run_root)

    sealed_files: Dict[str, str] = {}
    for rel, digest in manifest.items():
        name = Path(rel).name
        if name in EXCLUDED_FROM_SEAL:
            continue
        sealed_files[rel] = digest

    # Explicit components excluded from sealed_files
    sha_path = run_root / "SHA256SUMS.txt"
    sha256sums_hash: Optional[str] = _sha256_file(sha_path) if sha_path.exists() else None

    payload_path = run_root / "payload.tar.gz"
    payload_hash: Optional[str] = _sha256_file(payload_path) if payload_path.exists() else None

    # Deterministic seal hash:
    #  1) sealed file hashes ordered by path
    #  2) sha256sums_hash (if present)
    #  3) payload_hash (if present)
    components = []
    for rel in sorted(sealed_files.keys()):
        components.append(sealed_files[rel])

    if sha256sums_hash is not None:
        components.append(sha256sums_hash)
    if payload_hash is not None:
        components.append(payload_hash)

    seal_hash = hashlib.sha256("".join(components).encode("utf-8")).hexdigest()

    return {
        "contract_version": cv,
        "sha256sums_hash": sha256sums_hash,
        "payload_hash": payload_hash,
        "sealed_files": {k: sealed_files[k] for k in sorted(sealed_files.keys())},
        "seal_hash": seal_hash,
    }


def write_seal(run_root: Path, seal_obj: Mapping[str, Any]) -> Path:
    """
    Write SEAL.json deterministically.

    This function performs I/O and is intended for finalize-time artifact
    materialization, not verification.
    """
    run_root = run_root.resolve()
    seal_path = run_root / "SEAL.json"
    seal_path.write_text(json.dumps(dict(seal_obj), indent=2), encoding="utf-8")
    return seal_path


def build_run_seal(run_root: Path) -> Path:
    """
    Backward-compatible wrapper: compute + write SEAL.json.
    """
    seal_obj = compute_seal_obj(run_root)
    return write_seal(run_root, seal_obj)