"""
---
title: "CRI-CORE Enforcement Pipeline Execution Test"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.3.2"
doi: "TBD-0.3.2"
status: "Active"
created: "2026-02-11"
updated: "2026-03-09"

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
  - "../../src/cricore/enforcement/execution.py"
  - "../../src/cricore/results/stage.py"

anchors:
  - "CRI-CORE-PIPELINE-EXECUTION-TEST-v0.3.2"
---
"""

from pathlib import Path
import shutil

from cricore.enforcement.execution import run_enforcement_pipeline


def test_enforcement_pipeline_executes_all_stages_in_order(tmp_path: Path):

    fixture_root = (
        Path(__file__).parent
        / ".."
        / "fixtures"
        / "minimal_run_v0_1_0"
        / "runs"
        / "TEST-RUN-001"
    ).resolve()

    run_root = tmp_path / "TEST-RUN-001"
    shutil.copytree(fixture_root, run_root)

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

    results, commit_allowed = run_enforcement_pipeline(
        str(run_root),
        run_context=run_context,
    )

    assert len(results) == 7

    assert [r.stage_id for r in results] == [
        "run-structure",
        "structure-contract-version-gate",
        "independence",
        "integrity",
        "integrity-finalization",
        "publication",
        "publication-commit",
    ]

    # commit_allowed should match publication-commit stage
    assert commit_allowed == results[-1].passed
    