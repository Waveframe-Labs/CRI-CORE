import copy
import json
import time

from compiler.compile_policy import compile_policy
from cricore.enforcement.execution import run_execution_pipeline
from cricore.enforcement.execution import run_enforcement_pipeline
from cricore.integrity.payload import build_payload_archive_bytes
from cricore.interface.evaluate_core import evaluate_core
from cricore.interface.evaluate_proposal import evaluate_proposal
from cricore.proposal.validator import validate_proposal
from proposal_normalizer.build_proposal import build_proposal


def _compiled_contract():
    return compile_policy(
        {
            "contract_id": "boundary-contract",
            "contract_version": "1.0.0",
            "authority": {
                "required_roles": ["manager"],
            },
        }
    )


def _run_context(mode="local"):
    return {
        "mode": mode,
        "identities": {
            "actors": [
                {
                    "id": "user-1",
                    "type": "human",
                    "role": "manager",
                }
            ],
            "required_roles": ["manager"],
        },
        "integrity": {},
        "publication": {},
    }


def _proposal(compiled, contract_hash=None, run_context=None):
    return build_proposal(
        proposal_id="boundary-test",
        actor={
            "id": "user-1",
            "type": "human",
            "role": "manager",
        },
        artifact_paths=[],
        mutation={
            "domain": "test",
            "resource": "file",
            "action": "write",
        },
        contract={
            "id": compiled["contract_id"],
            "version": compiled["contract_version"],
            "hash": contract_hash or compiled["contract_hash"],
        },
        run_context=run_context,
    )


def test_evaluate_core_hash_mismatch_blocks_without_mutation():
    compiled = _compiled_contract()
    proposal = _proposal(
        compiled,
        contract_hash="BAD_HASH",
        run_context=_run_context(),
    )
    original = copy.deepcopy(proposal)

    result = evaluate_core(
        proposal=proposal,
        compiled_contract=compiled,
        run_context=_run_context(),
    )

    assert result.commit_allowed is False
    assert "structure-contract-hash-gate" in result.failed_stages
    assert proposal == original


def test_evaluate_proposal_hash_mismatch_blocks_without_mutation():
    compiled = _compiled_contract()
    proposal = _proposal(
        compiled,
        contract_hash="BAD_HASH",
        run_context=_run_context(),
    )
    original = copy.deepcopy(proposal)

    result = evaluate_proposal(
        proposal=proposal,
        compiled_contract=compiled,
        run_id="boundary-test",
    )

    assert result.commit_allowed is False
    assert "structure-contract-hash-gate" in result.failed_stages
    assert proposal == original


def test_run_context_mode_is_preserved_when_mode_argument_omitted():
    compiled = _compiled_contract()
    strict_context = {
        "mode": "strict",
        "identities": _run_context()["identities"],
    }
    proposal = _proposal(
        compiled,
        run_context=strict_context,
    )

    result = run_execution_pipeline(
        proposal=proposal,
        compiled_contract=compiled,
        run_context=strict_context,
    )

    assert result.commit_allowed is False
    assert "integrity" in result.failed_stages
    assert "publication" in result.failed_stages


def test_expected_contract_version_mismatch_blocks_structured_pipeline():
    compiled = _compiled_contract()
    proposal = _proposal(
        compiled,
        run_context=_run_context(),
    )

    result = run_execution_pipeline(
        proposal=proposal,
        compiled_contract=compiled,
        run_context=_run_context(),
        expected_contract_version="9.9.9",
    )

    assert result.commit_allowed is False
    assert "run-structure" in result.failed_stages
    assert "structure-contract-version-gate" in result.failed_stages


def test_expected_contract_version_mismatch_blocks_run_path_pipeline(tmp_path):
    compiled = _compiled_contract()
    proposal = _proposal(
        compiled,
        run_context=_run_context(),
    )

    (tmp_path / "proposal.json").write_text(
        json.dumps(proposal),
        encoding="utf-8",
    )
    (tmp_path / "compiled_contract.json").write_text(
        json.dumps(compiled),
        encoding="utf-8",
    )
    (tmp_path / "run_context.json").write_text(
        json.dumps(_run_context()),
        encoding="utf-8",
    )

    stages, commit_allowed = run_enforcement_pipeline(
        str(tmp_path),
        expected_contract_version="9.9.9",
    )

    failed_stages = [stage.stage_id for stage in stages if not stage.passed]
    assert commit_allowed is False
    assert "run-structure" in failed_stages
    assert "structure-contract-version-gate" in failed_stages


def test_proposal_validator_loads_packaged_schema():
    compiled = _compiled_contract()
    proposal = {
        "proposal_id": "schema-test",
        "timestamp": "2026-01-01T00:00:00Z",
        "actor": {
            "id": "user-1",
            "type": "human",
            "declared_role": "manager",
        },
        "contract": {
            "id": compiled["contract_id"],
            "version": compiled["contract_version"],
            "hash": compiled["contract_hash"],
        },
        "requested_mutation": {
            "domain": "test",
            "resource": "file",
            "action": "write",
        },
        "artifacts": [
            {
                "path": "proposal.json",
                "sha256": "0" * 64,
            }
        ],
    }

    validate_proposal(proposal)


def test_payload_archive_bytes_are_deterministic(tmp_path):
    (tmp_path / "proposal.json").write_text('{"ok": true}\n', encoding="utf-8")

    first = build_payload_archive_bytes(tmp_path)
    time.sleep(1.1)
    second = build_payload_archive_bytes(tmp_path)

    assert first == second
