"""Validate execution configuration before evaluating policy stages."""

from typing import Any, Mapping, Optional


def resolve_mode(
    mode: str = "strict", run_context: Optional[Mapping[str, Any]] = None
) -> str:
    """Require an explicit local argument; context is a consistency check only."""
    if type(mode) is not str or mode not in ("strict", "local"):
        raise ValueError(
            'CRI_MODE_INVALID: mode must be exactly "strict" or "local"; '
            'omit mode for enforcement or pass mode="local" for advisory evaluation.'
        )
    if run_context is not None and not isinstance(run_context, Mapping):
        raise ValueError("CRI_RUN_CONTEXT_INVALID: run_context must be a mapping.")
    if run_context is not None and "mode" in run_context:
        context_mode = run_context["mode"]
        if type(context_mode) is not str or context_mode not in ("strict", "local"):
            raise ValueError(
                'CRI_MODE_INVALID: run_context["mode"] must be exactly "strict" '
                'or "local"; remove it or match the function mode.'
            )
        if context_mode != mode:
            raise ValueError(
                'CRI_MODE_CONFLICT: run_context["mode"] must match the function '
                'mode (default "strict"); remove the context mode or make both '
                'declarations identical. Advisory evaluation requires mode="local".'
            )
    return mode
