"""
---
title: "CRI-CORE Run Integrity Finalization Writer"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.3.0"
doi: "TBD-0.3.0"
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
  - "./binding.py"

anchors:
  - "CRI-CORE-IntegrityFinalizationWriter-v0.3.0"
---
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

from .binding import build_binding_artifact
from .manifest import build_integrity_manifest
from .payload import build_payload_archive_bytes
from .seal import build_run_seal


def _format_sha256sums(manifest: dict[str, str]) -> str:
    """
    Format SHA256SUMS.txt deterministically:
      <sha256><two spaces><posix relative path>\n
    """
    lines = []
    for rel_path in sorted(manifest.keys()):
        lines.append(f"{manifest[rel_path]}  {rel_path}")
    return "\n".join(lines) + "\n"


def finalize_run_integrity(run_root: Path) -> Tuple[Path, Path, Path, Path]:
    """
    Materialize run integrity artifacts inside run_root:

      - payload.tar.gz
      - SHA256SUMS.txt
      - binding.json
      - SEAL.json

    Order matters:
      1) payload.tar.gz (excluded from SHA manifest by design)
      2) SHA256SUMS.txt (hashes run files excluding payload + SHA)
      3) binding.json (explicit bindings of contract/claim/logs)
      4) SEAL.json (top-level seal over the full run state, including binding)

    Returns: (sha256sums_path, payload_path, binding_path, seal_path)
    """
    run_root = run_root.resolve()

    sha_path = run_root / "SHA256SUMS.txt"
    payload_path = run_root / "payload.tar.gz"

    # 1) Build and write payload archive
    payload_bytes = build_payload_archive_bytes(run_root)
    payload_path.write_bytes(payload_bytes)

    # 2) Build and write hash manifest (excluding payload + SHA file by design)
    manifest = build_integrity_manifest(run_root)
    sha_path.write_text(_format_sha256sums(manifest), encoding="utf-8")

    # 3) Build and write binding.json (explicit per-artifact binding)
    binding_path = build_binding_artifact(run_root)

    # 4) Build and write SEAL.json LAST (seals everything, including binding)
    seal_path = build_run_seal(run_root)

    return sha_path, payload_path, binding_path, seal_path