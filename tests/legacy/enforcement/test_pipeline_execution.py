"""
---
title: "CRI-CORE Enforcement Pipeline Execution Test"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.4.1"
doi: "TBD-0.4.1"
status: "Active"
created: "2026-02-11"
updated: "2026-03-19"

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
  - "CRI-CORE-PIPELINE-EXECUTION-TEST-v0.4.1"
---
"""

from pathlib import Path
import shutil
import json

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

    # --- Inject compiled contract artifact ---
    compiled_contract = {
        "contract_id": "test-contract",
        "contract_version": "0.1.0",
        "contract_hash": "abc123",
    }

    (run_root / "compiled_contract.json").write_text(
        json.dumps(compiled_contract)
    )

    # --- Inject proposal aligned to contract hash ---
    proposal = {
        "proposal_id": "proposal-001",
        "timestamp": "2026-03-17T00:00:00Z",
        "actor": {
            "id": "tester",
            "type": "human",
            "declared_role": "proposer",
        },
        "contract": {
            "id": "test-contract",
            "version": "0.1.0",
            "hash": "abc123",
        },
        "requested_mutation": {
            "domain": "test",
            "resource": "test",
            "action": "test",
        },
        "artifacts": [],
    }

    (run_root / "proposal.json").write_text(json.dumps(proposal))

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

    # 8 stages
    assert len(results) == 8

    assert [r.stage_id for r in results] == [
        "run-structure",
        "structure-contract-version-gate",
        "structure-contract-hash-gate",
        "independence",
        "integrity",
        "integrity-finalization",
        "publication",
        "publication-commit",
    ]

    # commit_allowed should match final stage
    assert commit_allowed == results[-1].passed