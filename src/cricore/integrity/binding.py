"""
---
title: "CRI-CORE Structural Binding Artifact Builder"
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
ai_assistance_details: "AI-assisted implementation of a deterministic structural binding artifact builder that binds contract.json, declared claim_ref artifact, and approval.json via SHA256 hashing without introducing semantic coupling."

dependencies:
  - "../contract/loader.py"

anchors:
  - "CRI-CORE-BindingBuilder-v0.1.0"
---
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, Optional


def _sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _load_contract(run_root: Path) -> Dict:
    contract_path = run_root / "contract.json"
    if not contract_path.exists():
        raise FileNotFoundError("contract.json missing")

    return json.loads(contract_path.read_text(encoding="utf-8"))


def build_binding_artifact(run_root: Path) -> Path:
    """
    Build binding.json inside run_root.

    Binding includes:
      - contract_hash
      - claim_hash (declared via contract.json claim_ref)
      - approval_hash (if approval.json present)
      - binding_hash (sha256 of concatenated component hashes)

    This function writes binding.json and returns its path.

    Structural only:
      - No semantic interpretation of claim content
      - No semantic interpretation of contract content
      - Only deterministic hashing
    """

    run_root = run_root.resolve()

    contract_path = run_root / "contract.json"
    if not contract_path.exists():
        raise FileNotFoundError("contract.json missing")

    contract_obj = _load_contract(run_root)

    claim_ref = contract_obj.get("claim_ref")
    if not isinstance(claim_ref, str) or not claim_ref.strip():
        raise ValueError("contract.json missing valid claim_ref")

    claim_path = run_root / claim_ref
    if not claim_path.exists():
        raise FileNotFoundError(f"declared claim_ref not found: {claim_ref}")

    approval_path = run_root / "approval.json"

    contract_hash = _sha256_file(contract_path)
    claim_hash = _sha256_file(claim_path)

    approval_hash: Optional[str] = None
    if approval_path.exists():
        approval_hash = _sha256_file(approval_path)

    # Deterministic binding hash construction
    components = [contract_hash, claim_hash]
    if approval_hash:
        components.append(approval_hash)

    binding_hash_input = "".join(components).encode("utf-8")
    binding_hash = hashlib.sha256(binding_hash_input).hexdigest()

    binding_obj = {
        "contract_hash": contract_hash,
        "claim_hash": claim_hash,
        "approval_hash": approval_hash,
        "binding_hash": binding_hash,
    }

    binding_path = run_root / "binding.json"
    binding_path.write_text(
        json.dumps(binding_obj, indent=2),
        encoding="utf-8",
    )

    return binding_path