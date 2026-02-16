"""
---
title: "CRI-CORE Repository Integrity Manifest and Verification"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.2.0"
doi: "TBD-0.2.0"
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
ai_assistance_details: "AI-assisted implementation of deterministic repository-level integrity manifest generation and verification without auto-healing behavior."

dependencies:
  - "../results/stage.py"
  - "../errors.py"

anchors:
  - "CRI-CORE-RepositoryIntegrity-v0.2.0"
---
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

from ..results.stage import StageResult
from ..errors import FailureClass


# Directories and files excluded from repository hashing
_EXCLUDED_PREFIXES = (
    ".git/",
    "__pycache__/",
    ".pytest_cache/",
    "archive/",
)

_EXCLUDED_FILES = (
    "SHA256SUMS.txt",
)


def _compute_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _should_exclude(rel_posix_path: str) -> bool:
    if rel_posix_path in _EXCLUDED_FILES:
        return True

    for prefix in _EXCLUDED_PREFIXES:
        if rel_posix_path.startswith(prefix):
            return True

    return False


def build_repository_manifest(repo_root: Path) -> Dict[str, str]:
    """
    Deterministically build a repository SHA256 manifest.

    - Recursively walks repo_root
    - Uses POSIX-style relative paths
    - Excludes defined prefixes and manifest file itself
    - Returns sorted dictionary (path -> sha256)
    """
    repo_root = repo_root.resolve()

    manifest: Dict[str, str] = {}

    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue

        rel_path = path.relative_to(repo_root).as_posix()

        if _should_exclude(rel_path):
            continue

        manifest[rel_path] = _compute_sha256(path)

    # Return manifest sorted by key deterministically
    return dict(sorted(manifest.items()))


def verify_repository_manifest(repo_root: Path) -> StageResult:
    """
    Verify repository integrity if SHA256SUMS.txt exists.

    Behavior:
      - If SHA256SUMS.txt does not exist → pass (non-strict mode)
      - If it exists → strict verification
    """
    repo_root = repo_root.resolve()
    sha_path = repo_root / "SHA256SUMS.txt"

    messages = []
    failure_classes = []

    # Non-strict mode if manifest missing
    if not sha_path.exists():
        return StageResult(
            stage_id="repository-integrity",
            passed=True,
            failure_classes=[],
            messages=["SHA256SUMS.txt not present — repository integrity not enforced"],
            checked_at_utc=datetime.now(timezone.utc).isoformat(),
            engine_version=None,
        )

    # Load declared manifest
    declared_manifest: Dict[str, str] = {}

    for line in sha_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        digest, rel_path = parts[0], parts[-1]
        declared_manifest[rel_path] = digest

    # Build current manifest
    current_manifest = build_repository_manifest(repo_root)

    # Compare declared vs current
    for rel_path, expected_digest in declared_manifest.items():
        if rel_path not in current_manifest:
            messages.append(f"declared file missing: {rel_path}")
            failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
            continue

        if current_manifest[rel_path] != expected_digest:
            messages.append(f"hash mismatch: {rel_path}")
            failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)

    # Detect undeclared files
    for rel_path in current_manifest.keys():
        if rel_path not in declared_manifest:
            messages.append(f"undeclared file detected: {rel_path}")
            failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)

    passed = not failure_classes

    return StageResult(
        stage_id="repository-integrity",
        passed=passed,
        failure_classes=failure_classes,
        messages=messages,
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        engine_version=None,
    )
