"""
---
title: "CRI-CORE Integrity and Provenance Enforcement Stages"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.3.0"
doi: "TBD-0.3.0"
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
ai_assistance_details: "AI-assisted structural + cryptographic integrity enforcement stage expansion including canonical finalization stage."

dependencies:
  - "../results/stage.py"
  - "../errors.py"
  - "../integrity/finalize.py"

anchors:
  - "CRI-CORE-IntegrityStage-v0.3.0"
  - "CRI-CORE-IntegrityFinalizationStage-v0.3.0"
---
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Optional

from ..results.stage import StageResult
from ..errors import FailureClass
from ..integrity.finalize import finalize_run_integrity


# ---------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------

def _compute_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _load_manifest(sha_path: Path) -> dict[str, str]:
    manifest: dict[str, str] = {}

    if not sha_path.exists():
        raise FileNotFoundError("SHA256SUMS.txt missing")

    for line in sha_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        digest, rel_path = parts[0], parts[-1]
        manifest[rel_path] = digest

    return manifest


# ---------------------------------------------------------------------
# Stage 1: Integrity Verification
# ---------------------------------------------------------------------

def run_integrity_stage(
    run_path: str,
    *,
    run_context: Optional[Mapping[str, Any]] = None,
) -> StageResult:

    messages = []
    failure_classes = []

    run_root = Path(run_path).resolve()
    integrity = None

    if not run_context or not isinstance(run_context, Mapping):
        messages.append("run_context is missing or not a mapping")
    else:
        integrity = run_context.get("integrity")

    if not isinstance(integrity, Mapping):
        messages.append("integrity section missing from run_context")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
    else:
        for key in (
            "workflow_execution_ref",
            "run_payload_ref",
            "attestation_ref",
        ):
            value = integrity.get(key)
            if value is not None and not isinstance(value, str):
                messages.append(f"integrity.{key} must be a string when present")

        if messages:
            failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)

    sha_path = run_root / "SHA256SUMS.txt"

    try:
        manifest = _load_manifest(sha_path)
    except Exception as exc:
        messages.append(f"integrity manifest load failed: {exc}")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
        manifest = {}

    for rel_path, expected_digest in manifest.items():
        target = run_root / rel_path

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
        stage_id="integrity",
        passed=passed,
        failure_classes=failure_classes,
        messages=messages,
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        engine_version=None,
    )


# ---------------------------------------------------------------------
# Stage 2: Integrity Finalization
# ---------------------------------------------------------------------

def run_integrity_finalization_stage(
    run_path: str,
) -> StageResult:

    run_root = Path(run_path).resolve()

    try:
        finalize_run_integrity(run_root)
        passed = True
        failure_classes = []
        messages = []
    except Exception as exc:
        passed = False
        failure_classes = [FailureClass.INTEGRITY_CHECK_FAILED]
        messages = [f"finalization failed: {exc}"]

    return StageResult(
        stage_id="integrity-finalization",
        passed=passed,
        failure_classes=failure_classes,
        messages=messages,
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        engine_version=None,
    )
