"""
---
title: "CRI-CORE Seal Enforcement Test"
filetype: "documentation"
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
  - "../../src/cricore/enforcement/integrity.py"
  - "../../src/cricore/integrity/finalize.py"
  - "../../src/cricore/integrity/manifest.py"

anchors:
  - "CRI-CORE-SealEnforcementTest-v0.1.0"
---
"""

from __future__ import annotations

import shutil
from pathlib import Path

from cricore.enforcement.integrity import run_integrity_stage
from cricore.integrity.finalize import finalize_run_integrity
from cricore.integrity.manifest import build_integrity_manifest


def _format_sha256sums(manifest: dict[str, str]) -> str:
    lines = []
    for rel_path in sorted(manifest.keys()):
        lines.append(f"{manifest[rel_path]}  {rel_path}")
    return "\n".join(lines) + "\n"


def test_seal_blocks_tamper_even_if_sha_is_regenerated(tmp_path: Path):
    fixture = (
        Path(__file__).parent
        / ".."
        / "fixtures"
        / "minimal_run_v0_3_0"
        / "runs"
        / "TEST-RUN-003"
    ).resolve()

    run_root = tmp_path / "TEST-RUN-003"
    shutil.copytree(fixture, run_root)

    # Generate payload.tar.gz, SHA256SUMS.txt, SEAL.json
    finalize_run_integrity(run_root)

    run_context = {
        "integrity": {
            "workflow_execution_ref": "test://exec/TEST-RUN-003",
            "run_payload_ref": "test://payload/TEST-RUN-003",
            "attestation_ref": "test://attestation/TEST-RUN-003",
        }
    }

    # Baseline: should pass
    res_ok = run_integrity_stage(str(run_root), run_context=run_context)
    assert res_ok.passed is True

    # Tamper with a sealed file
    report_path = run_root / "report.md"
    report_path.write_text(report_path.read_text(encoding="utf-8") + "\nTAMPERED\n", encoding="utf-8")

    # Regenerate SHA256SUMS.txt to match the tampered state (so SHA check passes),
    # but DO NOT recompute SEAL.json. This isolates seal enforcement.
    sha_path = run_root / "SHA256SUMS.txt"
    manifest = build_integrity_manifest(run_root)
    sha_path.write_text(_format_sha256sums(manifest), encoding="utf-8")

    # Now integrity must fail due to seal mismatch
    res_bad = run_integrity_stage(str(run_root), run_context=run_context)
    assert res_bad.passed is False

    msgs = "\n".join(res_bad.messages)
    assert "seal mismatch" in msgs