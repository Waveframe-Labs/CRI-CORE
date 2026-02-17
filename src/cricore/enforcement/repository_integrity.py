"""
---
title: "CRI-CORE Repository Integrity Enforcement Stage"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-02-16"
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
ai_assistance_details: "AI-assisted implementation of repository-level cryptographic integrity verification, enforcing strict mode automatically when SHA256SUMS.txt exists."

dependencies:
  - "../results/stage.py"
  - "../errors.py"

anchors:
  - "CRI-CORE-RepositoryIntegrityStage-v0.1.0"
---
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from ..results.stage import StageResult
from ..errors import FailureClass


def _compute_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _load_manifest(manifest_path: Path) -> dict[str, str]:
    manifest: dict[str, str] = {}

    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        digest, rel_path = parts[0], parts[-1]
        manifest[rel_path] = digest

    return manifest


def run_repository_integrity_stage(repo_root: str) -> StageResult:
    """
    Enforce repository-level cryptographic integrity.

    Behavior:
      - If SHA256SUMS.txt does not exist → pass (non-strict mode).
      - If it exists → strict verification of all referenced files.
    """

    messages: List[str] = []
    failure_classes: List[FailureClass] = []

    root = Path(repo_root).resolve()
    manifest_path = root / "SHA256SUMS.txt"

    # Non-strict mode if manifest absent
    if not manifest_path.exists():
        return StageResult(
            stage_id="repository_integrity",
            passed=True,
            failure_classes=[],
            messages=["SHA256SUMS.txt not present — non-strict mode"],
            checked_at_utc=datetime.now(timezone.utc).isoformat(),
            engine_version=None,
        )

    try:
        manifest = _load_manifest(manifest_path)
    except Exception as exc:
        return StageResult(
            stage_id="repository_integrity",
            passed=False,
            failure_classes=[FailureClass.INTEGRITY_CHECK_FAILED],
            messages=[f"repository manifest load failed: {exc}"],
            checked_at_utc=datetime.now(timezone.utc).isoformat(),
            engine_version=None,
        )

    for rel_path, expected_digest in manifest.items():
        target = root / rel_path

        if not target.exists():
            messages.append(f"manifest references missing file: {rel_path}")
            failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
            continue

        actual_digest = _compute_sha256(target)

        if actual_digest != expected_digest:
            messages.append(f"hash mismatch: {rel_path}")
            failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)

    passed = not failure_classes

    return StageResult(
        stage_id="repository_integrity",
        passed=passed,
        failure_classes=failure_classes,
        messages=messages,
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        engine_version=None,
    )
