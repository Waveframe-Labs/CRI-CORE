"""
---
title: "CRI-CORE Integrity Stage Finalization Hook Test"
filetype: "documentation"
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
ai_assistance_details: "AI-assisted test scaffolding for the integrity stage finalization hook."

dependencies:
  - "../../src/cricore/enforcement/integrity.py"

anchors:
  - "CRI-CORE-IntegrityStageFinalizeTest-v0.1.0"
---
"""

import shutil
from pathlib import Path

from cricore.enforcement.integrity import run_integrity_stage


def test_integrity_stage_writes_finalization_artifacts_when_enabled(tmp_path: Path):
    fixture = (
        Path(__file__).parent
        / ".."
        / "fixtures"
        / "minimal_run_v0_1_0"
        / "runs"
        / "TEST-RUN-001"
    ).resolve()

    run_root = tmp_path / "TEST-RUN-001"
    shutil.copytree(fixture, run_root)

    run_context = {
        "integrity": {
            "workflow_execution_ref": "workflow-001",
            "run_payload_ref": "payload-001",
            "attestation_ref": "attestation-001",
        }
    }

    result = run_integrity_stage(
        str(run_root),
        run_context=run_context,
        finalize=True,
    )

    assert result.passed is True
    assert (run_root / "SHA256SUMS.txt").exists()
    assert (run_root / "payload.tar.gz").exists()
