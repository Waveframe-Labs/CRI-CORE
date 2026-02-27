"""
---
title: "CRI-CORE Run Integrity Finalization Writer"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.2.0"
doi: "TBD-0.2.0"
status: "Active"
created: "2026-02-11"
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
  - "./payload.py"
  - "./seal.py"

anchors:
  - "CRI-CORE-IntegrityFinalizationWriter-v0.2.0"
---
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

from .manifest import build_integrity_manifest
from .payload import build_payload_archive_bytes
from .seal import build_run_seal


def _format_sha256sums(manifest: dict[str, str]) -> str:
    """
    Deterministic formatting:
      <sha256><two spaces><posix relative path>\n
    """
    lines = []
    for rel_path in sorted(manifest.keys()):
        lines.append(f"{manifest[rel_path]}  {rel_path}")
    return "\n".join(lines) + "\n"


def finalize_run_integrity(run_root: Path) -> Tuple[Path, Path, Path]:
    """
    Materialize run integrity artifacts inside run_root:

      1) payload.tar.gz
      2) SHA256SUMS.txt
      3) SEAL.json   (must be written last)

    Returns:
      (sha256sums_path, payload_path, seal_path)
    """

    run_root = run_root.resolve()

    sha_path = run_root / "SHA256SUMS.txt"
    payload_path = run_root / "payload.tar.gz"

    # -----------------------------------------------------------------
    # 1) Build payload archive
    # -----------------------------------------------------------------

    payload_bytes = build_payload_archive_bytes(run_root)
    payload_path.write_bytes(payload_bytes)

    # -----------------------------------------------------------------
    # 2) Build SHA256SUMS.txt (excludes payload + SHA by design)
    # -----------------------------------------------------------------

    manifest = build_integrity_manifest(run_root)
    sha_path.write_text(_format_sha256sums(manifest), encoding="utf-8")

    # -----------------------------------------------------------------
    # 3) Build SEAL.json (must be last)
    # -----------------------------------------------------------------

    seal_path = build_run_seal(run_root)

    return sha_path, payload_path, seal_path