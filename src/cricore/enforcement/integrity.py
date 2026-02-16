"""
---
title: "CRI-CORE Integrity and Provenance Enforcement Stage"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.2.0"
doi: "TBD-0.2.0"
status: "Active"
created: "2026-02-10"
updated: "2026-02-16"

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
ai_assistance_details: "AI-assisted implementation of structural + cryptographic integrity verification for CRI-CORE run artifacts, including strict manifest enforcement when SHA256SUMS.txt is present."

dependencies:
  - "../results/stage.py"
  - "../errors.py"
  - "../integrity/finalize.py"

anchors:
  - "CRI-CORE-IntegrityStage-v0.2.0"
---
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Optional

from ..errors import FailureClass
from ..integrity.finalize import finalize_run_integrity
from ..results.stage import StageResult


# Files that may exist in a run directory but are excluded from strict-manifest
# "must be listed" enforcement.
#
# Rationale:
# - SHA256SUMS.txt: the manifest itself
# - payload.tar.gz: optional integrity payload archive produced by finalization
_EXCLUDED_TOP_LEVEL_FILES = {
    "SHA256SUMS.txt",
    "payload.tar.gz",
}


def _compute_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _as_posix_relpath(run_root: Path, path: Path) -> str:
    rel = path.relative_to(run_root)
    return rel.as_posix()


def _load_manifest(sha_path: Path) -> dict[str, str]:
    """
    Load SHA256SUMS.txt formatted as:
      <sha256><two spaces><relative_posix_path>

    Comments (# ...) and blank lines are ignored.
    """
    if not sha_path.exists():
        raise FileNotFoundError("SHA256SUMS.txt missing")

    manifest: dict[str, str] = {}
    for raw in sha_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        # Format: "<sha>  <path>"
        # Use split with maxsplit=1 so paths with spaces are still workable
        # (even though we strongly prefer no spaces in paths).
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue

        digest = parts[0].strip()
        rel_path = parts[1].strip()

        if digest and rel_path:
            manifest[rel_path] = digest

    return manifest


def _iter_run_files(run_root: Path) -> list[Path]:
    """
    Enumerate files under run_root, excluding directories.
    Returned paths are absolute (Path objects).
    """
    files: list[Path] = []
    for p in run_root.rglob("*"):
        if p.is_file():
            files.append(p)
    return files


def _is_excluded(rel_posix: str) -> bool:
    """
    Determine whether a relative posix path is excluded from strict manifest enforcement.
    """
    # Exclude known top-level files
    if "/" not in rel_posix and rel_posix in _EXCLUDED_TOP_LEVEL_FILES:
        return True
    return False


def run_integrity_stage(
    run_path: str,
    *,
    run_context: Optional[Mapping[str, Any]] = None,
    finalize: bool = False,
) -> StageResult:
    """
    Structural integrity and provenance enforcement.

    Behavior:
      - Always validates structural integrity context shape (run_context.integrity).
      - If SHA256SUMS.txt exists, integrity verification is STRICT:
          * All manifest entries must exist and match their SHA256
          * No unexpected (unlisted) files may exist in the run directory
            (excluding deterministic exclusions like SHA256SUMS.txt itself)
      - If SHA256SUMS.txt does not exist:
          * Cryptographic verification is skipped (structural-only mode)

    When finalize=True and the stage passes, integrity finalization artifacts are materialized.
    """

    messages: list[str] = []
    failure_classes: list[FailureClass] = []

    run_root = Path(run_path).resolve()

    # --- Structural validation (existing behavior) ---

    integrity = None
    if not run_context or not isinstance(run_context, Mapping):
        messages.append("run_context is missing or not a mapping")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
    else:
        integrity = run_context.get("integrity")

    if not isinstance(integrity, Mapping):
        messages.append("integrity section missing from run_context")
        if FailureClass.INTEGRITY_CHECK_FAILED not in failure_classes:
            failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
    else:
        for key in ("workflow_execution_ref", "run_payload_ref", "attestation_ref"):
            value = integrity.get(key)
            if value is not None and not isinstance(value, str):
                messages.append(f"integrity.{key} must be a string when present")

        if messages:
            if FailureClass.INTEGRITY_CHECK_FAILED not in failure_classes:
                failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
   
    # Optional finalization hook
    if finalize and not failure_classes:
        finalize_run_integrity(run_root)
   
    # --- Cryptographic verification (auto-strict when SHA256SUMS.txt exists) ---

    sha_path = run_root / "SHA256SUMS.txt"
    strict = sha_path.exists()

    if strict:
        try:
            manifest = _load_manifest(sha_path)
        except Exception as exc:
            messages.append(f"integrity manifest load failed: {exc}")
            failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
            manifest = {}

        # 1) Verify every manifest entry exists and matches hash
        for rel_path, expected_digest in manifest.items():
            if _is_excluded(rel_path):
                # We do not expect excluded files to be listed; if they are listed,
                # treat it as a policy violation because it breaks determinism.
                messages.append(f"manifest must not include excluded file: {rel_path}")
                failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
                continue

            target = run_root / Path(rel_path)
            if not target.exists():
                messages.append(f"manifest references missing file: {rel_path}")
                failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
                continue
            if not target.is_file():
                messages.append(f"manifest references non-file path: {rel_path}")
                failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
                continue

            actual_digest = _compute_sha256(target)
            if actual_digest != expected_digest:
                messages.append(f"hash mismatch: {rel_path}")
                failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)

        # 2) Detect unexpected/unlisted files (strict mode)
        #
        # Build the set of "allowed" file relpaths:
        # - everything in manifest
        # - deterministic exclusions
        allowed: set[str] = set(manifest.keys()) | {
            name for name in _EXCLUDED_TOP_LEVEL_FILES
        }

        unexpected: list[str] = []
        for f in _iter_run_files(run_root):
            rel_posix = _as_posix_relpath(run_root, f)
            if _is_excluded(rel_posix):
                continue
            if rel_posix not in allowed:
                unexpected.append(rel_posix)

        if unexpected:
            # Sort for deterministic error output
            unexpected_sorted = sorted(unexpected)
            messages.append("unexpected files present (not listed in SHA256SUMS.txt):")
            for p in unexpected_sorted:
                messages.append(f"  - {p}")
            failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED) 

    passed = not failure_classes

    return StageResult(
        stage_id="integrity",
        passed=passed,
        failure_classes=failure_classes,
        messages=messages,
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        engine_version=None,
    )
