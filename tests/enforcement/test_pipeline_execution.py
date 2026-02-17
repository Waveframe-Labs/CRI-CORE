"""
---
title: "CRI-CORE Enforcement Pipeline Execution Test"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.2.0"
doi: "TBD-0.2.0"
status: "Active"
created: "2026-02-11"
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
ai_assistance_details: "AI-assisted test scaffolding aligned to CRI-CORE enforcement pipeline stage ordering as of v0.2.0."

dependencies:
  - "../../src/cricore/enforcement/execution.py"
  - "../../src/cricore/results/stage.py"

anchors:
  - "CRI-CORE-PIPELINE-EXECUTION-TEST-v0.2.0"
---
"""

from pathlib import Path

from cricore.enforcement.execution import run_enforcement_pipeline


def test_enforcement_pipeline_executes_all_stages_in_order():
    """
    Verifies that the enforcement pipeline executes all mandatory stages
    in the defined order and returns a StageResult for each stage.
    """

    run_root = (
        Path(__file__).parent
        / ".."
        / "fixtures"
        / "minimal_run_v0_1_0"
        / "runs"
        / "TEST-RUN-001"
    ).resolve()

    run_context = {
        "identities": {
            "orchestrator": {"id": "alice", "type": "human"},
            "reviewer": {"id": "bob", "type": "human"},
        },
        "integrity": {
            "workflow_execution_ref": "workflow-001",
            "run_payload_ref": "payload-001",
            "attestation_ref": "attestation-001",
        },
        "publication": {
            "repository_ref": "repo-001",
            "commit_ref": "abc123",
        },
    }

    results = run_enforcement_pipeline(
        str(run_root),
        run_context=run_context,
    )

    # Canonical pipeline stage count
    assert len(results) == 7

    # Canonical pipeline stage order (v0.2.0)
    assert [r.stage_id for r in results] == [
        "run-structure",
        "structure-contract-version-gate",
        "independence",
        "integrity",
        "integrity-finalization",
        "publication",
        "publication-commit",
    ]
