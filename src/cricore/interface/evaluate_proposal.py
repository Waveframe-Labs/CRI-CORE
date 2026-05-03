"""
---
title: "CRI-CORE Proposal Evaluation Interface"
filetype: "source"
type: "execution-interface"
domain: "integration"
version: "0.1.3"
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
  - "CRI-CORE-Interface-evaluate_proposal-v0.1.3"
---
"""

from datetime import datetime, timezone
from pathlib import Path
import json
import tempfile
from typing import Dict, Any, Optional

from cricore import evaluate
from cricore.integrity.finalize import finalize_run_integrity


# -----------------------------
# Utilities
# -----------------------------

def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _utc_now_safe() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


# -----------------------------
# Core Interface
# -----------------------------

def evaluate_proposal(
    proposal: Dict[str, Any],
    compiled_contract: Dict[str, Any],
    *,
    run_id: Optional[str] = None,
) -> Any:

    if run_id is None:
        run_id = f"run-{_utc_now_safe()}"

    temp_root = Path(tempfile.mkdtemp(prefix="cricore_interface_"))
    run_path = temp_root / run_id
    run_path.mkdir(parents=True)

    (run_path / "validation").mkdir(exist_ok=True)

    # -----------------------------
    # Use precompiled contract
    # -----------------------------

    if "contract" not in proposal:
        raise ValueError("proposal must include 'contract' field")

    # -----------------------------
    # Claim artifact (minimal stub)
    # -----------------------------

    claim_id = f"claim-{run_id}"
    claims_dir = run_path / "claims"
    claims_dir.mkdir(exist_ok=True)

    claim_path = claims_dir / f"{claim_id}.json"

    _write_json(
        claim_path,
        {
            "claim_id": claim_id,
            "created_utc": _utc_now_safe(),
            "description": "Stub claim for interface evaluation",
        },
    )

    claim_ref = f"claims/{claim_id}.json"

    # -----------------------------
    # Write run artifacts
    # -----------------------------

    _write_json(
        run_path / "contract.json",
        {
            "run_id": run_id,
            "contract_id": compiled_contract.get("contract_id"),
            "contract_version": compiled_contract.get("contract_version"),
            "contract_hash": compiled_contract.get("contract_hash", "MISSING_HASH"),
            "claim_ref": claim_ref,
            "created_utc": _utc_now_safe(),
        },
    )

    _write_json(run_path / "compiled_contract.json", compiled_contract)
    _write_json(run_path / "proposal.json", proposal)
    _write_json(
        run_path / "run_context.json",
        proposal.get("run_context", {})
    )

    (run_path / "report.md").write_text("# CRI-CORE Evaluation Run\n", encoding="utf-8")

    _write_json(
        run_path / "approval.json",
        {
            "approved_by": "system",
            "timestamp": _utc_now_safe(),
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
