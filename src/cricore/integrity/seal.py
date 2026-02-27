"""
---
title: "CRI-CORE Run Seal Builder"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
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
  - "./binding.py"

anchors:
  - "CRI-CORE-RunSealBuilder-v0.1.0"
---
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional


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
        raise ValueError(f"invalid semantic version: {v}")
    return (int(parts[0]), int(parts[1]), int(parts[2]))


def build_run_seal(
    run_root: Path,
    *,
    log_refs: Optional[List[str]] = None,
    include_payload: bool = True,
) -> Path:
    """
    Build SEAL.json inside run_root.

    The seal is a deterministic, tamper-evident artifact. It is NOT a signature.

    Seal inputs (hashed):
      - binding.json (required)
      - SHA256SUMS.txt (optional if present)
      - payload.tar.gz (optional if present and include_payload=True)
      - log_refs entries (explicit list; each path must exist)

    Output:
      - SEAL.json containing component hashes and a deterministic seal_hash.

    Determinism:
      - log refs are normalized to POSIX-style relative paths
      - log hashes are included in sorted path order
      - seal_hash is sha256 of concatenated component hashes + sorted log hashes
    """

    run_root = run_root.resolve()

    contract_path = run_root / "contract.json"
    if not contract_path.exists():
        raise FileNotFoundError("contract.json missing (seal requires run root)")

    contract_obj = _load_json(contract_path)
    cv = contract_obj.get("contract_version")
    if not isinstance(cv, str) or not cv.strip():
        raise ValueError("contract.json missing valid contract_version")

    # binding.json is the structural prerequisite for sealing
    binding_path = run_root / "binding.json"
    if not binding_path.exists():
        raise FileNotFoundError("binding.json missing (seal requires binding)")

    binding_hash = _sha256_file(binding_path)

    sha_path = run_root / "SHA256SUMS.txt"
    sha256sums_hash: Optional[str] = _sha256_file(sha_path) if sha_path.exists() else None

    payload_path = run_root / "payload.tar.gz"
    payload_hash: Optional[str] = None
    if include_payload and payload_path.exists():
        payload_hash = _sha256_file(payload_path)

    # logs are explicitly declared: no crawling, no inference
    logs: List[str] = []
    if log_refs:
        for p in log_refs:
            if not isinstance(p, str) or not p.strip():
                raise ValueError("log_refs must contain non-empty strings")
            logs.append(p.strip())

    log_hashes: Dict[str, str] = {}
    for rel in sorted(set(logs)):
        target = run_root / rel
        if not target.exists():
            raise FileNotFoundError(f"declared log missing: {rel}")
        # normalize key to POSIX relative path
        key = Path(rel).as_posix()
        log_hashes[key] = _sha256_file(target)

    # deterministic seal hash
    components: List[str] = [binding_hash]
    if sha256sums_hash is not None:
        components.append(sha256sums_hash)
    if payload_hash is not None:
        components.append(payload_hash)

    for k in sorted(log_hashes.keys()):
        components.append(log_hashes[k])

    seal_hash = hashlib.sha256("".join(components).encode("utf-8")).hexdigest()

    seal_obj: Dict[str, Any] = {
        "contract_version": cv,
        "binding_hash": binding_hash,
        "sha256sums_hash": sha256sums_hash,
        "payload_hash": payload_hash,
        "log_hashes": {k: log_hashes[k] for k in sorted(log_hashes.keys())},
        "seal_hash": seal_hash,
    }

    seal_path = run_root / "SEAL.json"
    seal_path.write_text(json.dumps(seal_obj, indent=2), encoding="utf-8")
    return seal_path
