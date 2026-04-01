"""
---
title: "CRI-CORE Proposal Evaluation Interface"
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
  - "CRI-CORE-Interface-evaluate_proposal-v0.1.0"
---
"""

from datetime import datetime, timezone
from pathlib import Path
import json
import tempfile
from typing import Dict, Any, Optional

from compiler.compile_policy import compile_policy
from cricore import evaluate
from cricore.integrity.finalize import finalize_run_integrity


# -----------------------------
# Utilities
# -----------------------------

def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# -----------------------------
# Core Interface
# -----------------------------

def evaluate_proposal(
    proposal: Dict[str, Any],
    policy: Dict[str, Any],
    *,
    run_id: Optional[str] = None,
) -> Any:
    """
    Evaluate a mutation proposal against a compiled governance contract.

    This function provides a minimal integration surface for CRI-CORE by:
    - compiling a policy into a contract
    - constructing a deterministic run artifact
    - finalizing integrity (binding + seal)
    - invoking the CRI-CORE enforcement kernel

    Parameters
    ----------
    proposal : dict
        Canonical mutation proposal object.
    policy : dict
        Governance policy definition (input to contract compiler).
    run_id : str, optional
        Optional override for run identifier.

    Returns
    -------
    EvaluationResult
        Result object returned by `cricore.evaluate`.
    """

    # -----------------------------
    # Prepare run context
    # -----------------------------

    if run_id is None:
        run_id = f"run-{_utc_now()}"

    temp_root = Path(tempfile.mkdtemp(prefix="cricore_interface_"))
    run_path = temp_root / run_id
    run_path.mkdir(parents=True)

    (run_path / "validation").mkdir(exist_ok=True)

    # -----------------------------
    # Compile contract
    # -----------------------------

    compiled_contract = compile_policy(policy)
    contract_hash = compiled_contract.get("contract_hash", "MISSING_HASH")

    # bind contract hash to proposal
    if "contract" not in proposal:
        raise ValueError("proposal must include 'contract' field")

    proposal["contract"]["hash"] = contract_hash

    # -----------------------------
    # Write run artifacts
    # -----------------------------

    _write_json(
        run_path / "contract.json",
        {
            "run_id": run_id,
            "contract_id": policy.get("contract_id"),
            "contract_version": policy.get("contract_version"),
            "contract_hash": contract_hash,
            "created_utc": _utc_now(),
        },
    )

    _write_json(run_path / "compiled_contract.json", compiled_contract)
    _write_json(run_path / "proposal.json", proposal)

    (run_path / "report.md").write_text("# CRI-CORE Evaluation Run\n", encoding="utf-8")

    _write_json(
        run_path / "approval.json",
        {
            "approved_by": "system",
            "timestamp": _utc_now(),
        },
    )

    _write_json(
        run_path / "randomness.json",
        {
            "seed": 42,
        },
    )

    # -----------------------------
    # Finalize integrity
    # -----------------------------

    finalize_run_integrity(run_path)

    # -----------------------------
    # Invoke kernel
    # -----------------------------

    result = evaluate(
        run_path=str(run_path),
        run_context=proposal.get("run_context", {}),
    )

    return result