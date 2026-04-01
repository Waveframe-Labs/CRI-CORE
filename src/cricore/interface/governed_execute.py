"""
---
title: "CRI-CORE Governed Execution Interface"
filetype: "source"
type: "execution-interface"
domain: "integration"
version: "0.1.0"
status: "Active"
created: "2026-04-01"
updated: "2026-04-01"

author:
  name: "Shawn C. Wright"

maintainer:
  name: "Waveframe Labs"

license: "Apache-2.0"

ai_assisted: "partial"

anchors:
  - "CRI-CORE-Interface-governed_execute-v0.1.0"
---
"""

from typing import Callable, Any, Dict

from .evaluate_proposal import evaluate_proposal


# -----------------------------
# Governed Execution
# -----------------------------

def governed_execute(
    proposal: Dict,
    policy: Dict,
    execute_fn: Callable[[Dict], Any],
) -> Dict[str, Any]:
    """
    Execute a mutation under CRI-CORE governance.

    This function enforces a hard execution boundary:
    - proposal is evaluated by CRI-CORE
    - execution only occurs if commit_allowed is True

    Parameters
    ----------
    proposal : dict
        Canonical mutation proposal
    policy : dict
        Governance policy definition
    execute_fn : callable
        Function that performs the actual mutation

    Returns
    -------
    dict
        {
            "commit_allowed": bool,
            "result": EvaluationResult,
            "execution_result": Any | None,
            "blocked": bool,
        }
    """

    # -----------------------------
    # Evaluate proposal
    # -----------------------------

    result = evaluate_proposal(proposal, policy)

    # -----------------------------
    # Enforce execution boundary
    # -----------------------------

    if not result.commit_allowed:
        return {
            "commit_allowed": False,
            "result": result,
            "execution_result": None,
            "blocked": True,
        }

    # -----------------------------
    # Execute mutation
    # -----------------------------

    execution_result = execute_fn(proposal)

    return {
        "commit_allowed": True,
        "result": result,
        "execution_result": execution_result,
        "blocked": False,
    }