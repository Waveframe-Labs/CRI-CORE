from typing import Any, Dict

from cricore.api import evaluate_structured


def evaluate_core(
    proposal: Dict[str, Any],
    compiled_contract: Dict[str, Any],
    run_context: Dict[str, Any],
    mode: str = "local",
) -> Any:
    """
    Pure CRI-CORE evaluation interface.

    This function performs deterministic enforcement evaluation
    without filesystem or simulation scaffolding.
    """

    # Ensure contract hash is bound
    if "contract" not in proposal:
        raise ValueError("proposal must include 'contract' field")

    # Call structured kernel entrypoint
    result = evaluate_structured(
        proposal=proposal,
        compiled_contract=compiled_contract,
        run_context=run_context,
        mode=mode,
    )

    return result
