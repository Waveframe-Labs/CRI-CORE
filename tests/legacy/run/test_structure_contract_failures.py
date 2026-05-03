"""
---
title: "CRI-CORE Structure Contract Failure Test (missing report.md)"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-02-10"
updated: "2026-02-10"

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
ai_assistance_details: "AI-assisted test scaffolding aligned strictly to the CRI-CORE Enforcement & Run Artifact Contract and existing structure stage behavior."

dependencies:
  - "../../src/cricore/run/structure.py"
  - "../../src/cricore/results/model.py"
  - "../../src/cricore/errors.py"

anchors:
  - "CRI-CORE-STRUCTURE-FAILURE-TEST-v0.1.0"
---
"""

from pathlib import Path

from cricore.run.structure import run_structure_stage
from cricore.errors import FailureClass


FIXTURE_ROOT = Path(__file__).parent.parent / "fixtures" / "minimal_run_missing_report"
RUN_PATH = FIXTURE_ROOT / "runs" / "TEST-RUN-002"


def test_structure_contract_fails_when_report_is_missing():
    """
    Verifies that the structure contract fails when report.md is missing
    and that the failure is classified as a missing required artifact.
    """

    result = run_structure_stage(
        run_path=str(RUN_PATH)
    )

    assert result.stage_id == "run-structure"
    assert result.passed is False

    # Must contain a missing required artifact failure
    assert FailureClass.MISSING_REQUIRED_ARTIFACT in result.failure_classes

    # The missing report file should be mentioned in messages
    joined_messages = " ".join(result.messages).lower()
    assert "report.md" in joined_messages
