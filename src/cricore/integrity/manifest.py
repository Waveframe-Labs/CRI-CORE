"""
---
title: "CRI-CORE Integrity Manifest Builder"
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
ai_assistance_details: "AI-assisted implementation of a deterministic, side-effect-free integrity manifest builder for CRI run artifacts, derived from CRI-CORE enforcement contract §3.10 and §6.3."

dependencies:
  - "../errors.py"

anchors:
  - "CRI-CORE-IntegrityManifestBuilder-v0.1.0"
---
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict


EXCLUDED_FILENAMES = {
    "SHA256SUMS.txt",
    "payload.tar.gz",
}


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_integrity_manifest(run_root: Path) -> Dict[str, str]:
    """
    Build a deterministic SHA256 manifest for a CRI run directory.

    The manifest covers all files under run_root, excluding:
      - SHA256SUMS.txt
      - payload.tar.gz

    Returned mapping keys are POSIX-style relative paths
    rooted at run_root.

    This function has no side effects and performs no I/O writes.
    """

    run_root = run_root.resolve()

    entries: Dict[str, str] = {}

    if not run_root.exists() or not run_root.is_dir():
        return entries

    files = []

    for p in run_root.rglob("*"):
        if not p.is_file():
            continue

        if p.name in EXCLUDED_FILENAMES:
            continue

        files.append(p)

    # Deterministic ordering
    files.sort(key=lambda x: x.relative_to(run_root).as_posix())

    for p in files:
        rel = p.relative_to(run_root).as_posix()
        entries[rel] = _hash_file(p)

    return entries
