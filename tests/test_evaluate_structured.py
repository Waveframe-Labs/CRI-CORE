from compiler.compile_policy import compile_policy
from proposal_normalizer.build_proposal import build_proposal
from cricore.api import evaluate_structured


def _build_base_contract():
    policy = {
        "contract_id": "test-contract",
        "contract_version": "1.0.0",
        "authority": {
            "required_roles": ["manager"]
        }
    }
    return compile_policy(policy)


def _build_proposal(actor, compiled):
    return build_proposal(
        proposal_id="test-1",
        actor=actor,
        artifact_paths=[],
        mutation={
            "domain": "test",
            "resource": "file",
            "action": "write"
        },
        contract={
            "id": compiled["contract_id"],
            "version": compiled["contract_version"],
            "hash": compiled["contract_hash"]
        }
    )


def _build_run_context(actors, required_roles):
    return {
        "mode": "local",
        "identities": {
            "actors": actors,
            "required_roles": required_roles
        },
        "integrity": {},
        "publication": {}
    }


# -------------------------
# ✅ Success Case
# -------------------------

def test_evaluate_structured_allows_valid_role():
    compiled = _build_base_contract()

    actor = {
        "id": "user-1",
        "type": "human",
        "role": "manager"
    }

    proposal = _build_proposal(actor, compiled)

    run_context = _build_run_context(
        actors=[actor],
        required_roles=["manager"]
    )

    result = evaluate_structured(
        proposal=proposal,
        compiled_contract=compiled,
        run_context=run_context
    )

    assert result.commit_allowed is True
    assert "Commit allowed" in result.summary


# -------------------------
# ❌ Failure Case (Wrong Role)
# -------------------------

def test_evaluate_structured_blocks_invalid_role():
    compiled = _build_base_contract()

    actor = {
        "id": "user-1",
        "type": "human",
        "role": "intern"
    }

    proposal = _build_proposal(actor, compiled)

    run_context = _build_run_context(
        actors=[actor],
        required_roles=["manager"]
    )

    result = evaluate_structured(
        proposal=proposal,
        compiled_contract=compiled,
        run_context=run_context
    )

    assert result.commit_allowed is False
    assert "independence" in result.summary


# -------------------------
# ❌ Failure Case (Duplicate Identity / Separation of Duties)
# -------------------------

def test_evaluate_structured_blocks_duplicate_identity():
    policy = {
        "contract_id": "approval-contract",
        "contract_version": "1.0.0",
        "authority": {
            "required_roles": ["proposer", "approver"]
        }
    }

    compiled = compile_policy(policy)

    actor_proposer = {
        "id": "user-1",
        "type": "human",
        "role": "proposer"
    }

    actor_approver = {
        "id": "user-1",  # same identity (violation)
        "type": "human",
        "role": "approver"
    }

    proposal = build_proposal(
        proposal_id="test-2",
        actor=actor_proposer,
        artifact_paths=[],
        mutation={
            "domain": "finance",
            "resource": "transaction",
            "action": "approve"
        },
        contract={
            "id": compiled["contract_id"],
            "version": compiled["contract_version"],
            "hash": compiled["contract_hash"]
        }
    )

    run_context = {
        "mode": "local",
        "identities": {
            "actors": [actor_proposer, actor_approver],
            "required_roles": ["proposer", "approver"]
        },
        "integrity": {},
        "publication": {}
    }

    result = evaluate_structured(
        proposal=proposal,
        compiled_contract=compiled,
        run_context=run_context
    )

    assert result.commit_allowed is False
    assert "independence" in result.summary