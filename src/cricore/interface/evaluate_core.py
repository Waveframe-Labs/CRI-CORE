from typing import Any, Dict

from cricore.api import evaluate_structured
from cricore.enforcement.mode import resolve_mode


def evaluate_core(
    proposal: Dict[str, Any],
    compiled_contract: Dict[str, Any],
    run_context: Dict[str, Any],
    mode: str = "strict",
) -> Any:
    """
    Pure CRI-CORE evaluation interface.

    This function performs deterministic enforcement evaluation
    without filesystem or simulation scaffolding.
    """

    resolve_mode(mode, run_context)
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
