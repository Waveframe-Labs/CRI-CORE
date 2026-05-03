"""
---
title: "CRI-CORE Structure Contract Test (v0.1.0 minimal run)"
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

anchors:
  - "CRI-CORE-STRUCTURE-TEST-v0.1.0"
---
"""

from pathlib import Path

from cricore.run.structure import run_structure_stage


FIXTURE_ROOT = Path(__file__).parent.parent / "fixtures" / "minimal_run_v0_1_0"
RUN_PATH = FIXTURE_ROOT / "runs" / "TEST-RUN-001"


def test_minimal_run_fixture_satisfies_structure_contract():
    """
    This test verifies that the minimal run fixture satisfies the
    CRI run artifact structure contract (Section 3 of the enforcement contract).

    This test validates only structural presence and layout.
    It does not validate independence, integrity, or publication semantics.
    """

    result = run_structure_stage(
        run_path=str(RUN_PATH)
    )

    assert result.stage_id == "run-structure"
    assert result.passed is True

    # No structural failures should be reported
    assert result.failure_classes == []

    # No diagnostic messages should be present on a clean fixture
    assert result.messages == []
