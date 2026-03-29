import json
from pathlib import Path

from cricore import evaluate


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# --- POINT THIS TO YOUR DEMO RUN ---
BASE_PATH = Path(__file__).resolve().parents[2] / "governed-finance-mutation-demo" / "runs" / "allowed-run"

proposal_path = BASE_PATH / "proposal.json"
contract_path = BASE_PATH / "compiled_contract.json"

proposal = load_json(proposal_path)
compiled_contract = load_json(contract_path)


# --- RUN EVALUATION ---
results, allowed = evaluate(proposal, compiled_contract)


# --- OUTPUT ---
print("\n=== EVALUATE RESULT ===\n")

print("Commit allowed:", allowed)

print("\nStage Results:")
for r in results:
    print(f"{r.stage_id}: {'PASS' if r.passed else 'FAIL'}")

print("\n========================\n")
