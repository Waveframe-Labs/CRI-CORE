from cricore.interface.governed_execute import governed_execute


def execute_fn(proposal: dict) -> dict:
    return {
        "status": "executed",
        "mutation": proposal.get("requested_mutation"),
    }


policy = {
    "contract_id": "finance-raci",
    "contract_version": "0.3.0",
    "required_roles": ["responsible", "accountable"],
}

allowed_proposal = {
    "contract": {
        "id": "finance-raci",
        "version": "0.3.0",
        "hash": "",
    },
    "requested_mutation": {
        "type": "budget_reallocation",
        "from": "Marketing",
        "to": "Operations",
        "amount": 2000000,
    },
    "run_context": {
        "identities": {
            "required_roles": ["responsible", "accountable"],
            "actors": [
                {
                    "id": "finance_manager",
                    "type": "human",
                    "role": "responsible",
                },
                {
                    "id": "cfo",
                    "type": "human",
                    "role": "accountable",
                },
            ],
        },
        "integrity": {
            "workflow_execution_ref": "local",
            "run_payload_ref": "local",
            "attestation_ref": "local",
        },
        "publication": {
            "repository_ref": "local",
            "commit_ref": "local",
        },
    },
}

blocked_proposal = {
    "contract": {
        "id": "finance-raci",
        "version": "0.3.0",
        "hash": "",
    },
    "requested_mutation": {
        "type": "budget_reallocation",
        "from": "Marketing",
        "to": "Operations",
        "amount": 2000000,
    },
    "run_context": {
        "identities": {
            "required_roles": ["responsible", "accountable"],
            "actors": [
                {
                    "id": "finance_manager",
                    "type": "human",
                    "role": "responsible",
                },
                {
                    "id": "finance_manager",
                    "type": "human",
                    "role": "accountable",
                },
            ],
        },
        "integrity": {
            "workflow_execution_ref": "local",
            "run_payload_ref": "local",
            "attestation_ref": "local",
        },
        "publication": {
            "repository_ref": "local",
            "commit_ref": "local",
        },
    },
}

print("\n=== GOVERNED EXECUTE TEST ===\n")

allowed_result = governed_execute(
    proposal=allowed_proposal,
    policy=policy,
    execute_fn=execute_fn,
)

print("ALLOWED CASE")
print("commit_allowed:", allowed_result["commit_allowed"])
print("blocked:", allowed_result["blocked"])
print("summary:", allowed_result["result"].summary)
print("execution_result:", allowed_result["execution_result"])
print()

blocked_result = governed_execute(
    proposal=blocked_proposal,
    policy=policy,
    execute_fn=execute_fn,
)

print("BLOCKED CASE")
print("commit_allowed:", blocked_result["commit_allowed"])
print("blocked:", blocked_result["blocked"])
print("summary:", blocked_result["result"].summary)
print("execution_result:", blocked_result["execution_result"])
print()

print("=============================\n")