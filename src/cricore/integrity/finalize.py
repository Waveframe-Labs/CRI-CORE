"""
---
title: "CRI-CORE Run Integrity Finalization Writer"
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
ai_assistance_details: "AI-assisted implementation of a narrow integrity finalization writer that materializes SHA256SUMS.txt and payload.tar.gz for a run directory using deterministic builders (contract §3.10, §6.3)."

dependencies:
  - "./manifest.py"
  - "./payload.py"

anchors:
  - "CRI-CORE-IntegrityFinalizationWriter-v0.1.0"
---
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

from .manifest import build_integrity_manifest
from .payload import build_payload_archive_bytes


def _format_sha256sums(manifest: dict[str, str]) -> str:
    """
    Format SHA256SUMS.txt contents deterministically:
      <sha256><two spaces><posix relative path>\n
    """
    lines = []
    for rel_path in sorted(manifest.keys()):
        lines.append(f"{manifest[rel_path]}  {rel_path}")
    return "\n".join(lines) + "\n"


def finalize_run_integrity(run_root: Path) -> Tuple[Path, Path]:
    """
    Materialize run integrity artifacts inside run_root:

      - SHA256SUMS.txt
      - payload.tar.gz

    This function writes files to disk.

    Returns: (sha256sums_path, payload_path)
    """
    run_root = run_root.resolve()

    sha_path = run_root / "SHA256SUMS.txt"
    payload_path = run_root / "payload.tar.gz"

    # Build and write payload archive
    payload_bytes = build_payload_archive_bytes(run_root)
    payload_path.write_bytes(payload_bytes)

    # Build and write hash manifest (excluding payload + SHA file by design)
    manifest = build_integrity_manifest(run_root)
    sha_path.write_text(_format_sha256sums(manifest), encoding="utf-8")

    return sha_path, payload_path
