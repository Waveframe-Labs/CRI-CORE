"""
---
title: "CRI-CORE Run Structure Stage Version Gate Test"
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
ai_assistance_details: "AI-assisted test scaffolding that locks contract.json version gating behavior for the run structure stage."

dependencies:
  - "../../src/cricore/run/structure.py"
  - "../../src/cricore/errors.py"

anchors:
  - "CRI-CORE-STRUCTURE-VERSION-GATE-TEST-v0.1.0"
---
"""

from pathlib import Path

from cricore.errors import FailureClass
from cricore.run.structure import run_structure_stage


def test_structure_stage_fails_on_contract_version_mismatch():
    run_root = (
        Path(__file__).parent
        / ".."
        / "fixtures"
        / "minimal_run_v0_1_0"
        / "runs"
        / "TEST-RUN-001"
    ).resolve()

    # Assuming fixture declares 0.1.0. We intentionally require a different one.
    result = run_structure_stage(
        str(run_root),
        expected_contract_version="9.9.9",
    )

    assert result.stage_id == "run-structure"
    assert result.passed is False
    assert FailureClass.INVARIANT_VIOLATION in result.failure_classes
