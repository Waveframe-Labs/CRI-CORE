"""
---
title: "CRI-CORE Enforcement Pipeline Execution Test"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.3.0"
doi: "TBD-0.3.0"
status: "Active"
created: "2026-02-11"
updated: "2026-02-19"

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
ai_assistance_details: "AI-assisted update to reflect canonical 8-stage enforcement pipeline including lifecycle-contract-conformity stage."

dependencies:
  - "../../src/cricore/enforcement/execution.py"
  - "../../src/cricore/results/stage.py"

anchors:
  - "CRI-CORE-PIPELINE-EXECUTION-TEST-v0.3.0"
---
"""

from pathlib import Path
import shutil
import hashlib
import json

from cricore.enforcement.execution import run_enforcement_pipeline


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def test_enforcement_pipeline_executes_all_stages_in_order(tmp_path: Path):
    """
    Verifies that the enforcement pipeline executes all mandatory stages
    in the defined canonical order (8 stages).

    IMPORTANT:
      - The pipeline includes mutating stages (e.g., integrity-finalization).
      - Therefore we MUST copy fixtures to tmp_path before execution to keep
        repository fixtures immutable.
    """

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

    # Minimal valid lifecycle contract
    lifecycle_contract = {
        "contract_id": "lifecycle-contract-001",
        "version": "0.1.0",
        "allowed_transitions": [
            {"from": "proposed", "to": "supported"}
        ],
    }

    lifecycle_contract_hash = _sha256_text(
        json.dumps(lifecycle_contract, sort_keys=True)
    )

    run_context = {
        "proposal": {
            "proposal_id": "p-001",
            "type": "claim_transition",
            "claim_id": "claim-001",
            "from": "proposed",
            "to": "supported",
        },
        "lifecycle_contract": lifecycle_contract,
        "lifecycle_contract_hash": lifecycle_contract_hash,
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

    assert len(results) == 8

    assert [r.stage_id for r in results] == [
        "run-structure",
        "structure-contract-version-gate",
        "lifecycle-contract-conformity",
        "independence",
        "integrity",
        "integrity-finalization",
        "publication",
        "publication-commit",
    ]
