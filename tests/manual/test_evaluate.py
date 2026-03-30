from cricore import evaluate_run


# --- POINT THIS TO YOUR DEMO RUN ---
run_path = "C:/GitHub/governed-finance-mutation-demo/runs/allowed-run"


# --- RUN EVALUATION ---
allowed = evaluate_run(run_path)


# --- OUTPUT ---
print("\n=== EVALUATE_RUN RESULT ===\n")
print("Commit allowed:", allowed)
print("\n===========================\n")
