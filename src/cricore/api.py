"""
---
title: "CRI-CORE Public API"
filetype: "operational"
type: "interface"
domain: "enforcement"
version: "0.2.1"
doi: "TBD-0.2.1"
status: "Active"
created: "2026-03-29"
updated: "2026-03-29"

author:
  name: "Shawn C. Wright"
  email: "swright@waveframelabs.org"

maintainer:
  name: "Waveframe Labs"
  url: "https://waveframelabs.org"

license: "Apache-2.0"

ai_assisted: "partial"

anchors:
  - "CRI-CORE-API-Evaluate-v0.2.1"
---
"""

import json
import tempfile
from pathlib import Path
from typing import Any, Dict, Tuple, List

from .enforcement.execution import run_enforcement_pipeline
from .results.stage import StageResult


def evaluate(
    proposal: Dict[str, Any],
    compiled_contract: Dict[str, Any],
) -> Tuple[List[StageResult], bool]:
    """
    Convenience evaluation interface (non-strict).

    For strict enforcement, use evaluate_run().
    """

    with tempfile.TemporaryDirectory() as tmpdir:
        run_path = Path(tmpdir)

        _write_json(run_path / "proposal.json", proposal)
        _write_json(
            run_path / "run_context.json",
            proposal.get("run_context", {})
        )
        _write_json(run_path / "compiled_contract.json", compiled_contract)

        contract_stub = {
            "contract_version": compiled_contract.get("contract_version", "unknown"),
            "run_id": "api-run",
            "created_utc": "2026-01-01T00:00:00Z",
        }
        _write_json(run_path / "contract.json", contract_stub)

        _write_json(run_path / "randomness.json", {"deterministic": True})
        (run_path / "report.md").write_text("# API Run\n", encoding="utf-8")
        (run_path / "SHA256SUMS.txt").write_text("", encoding="utf-8")

        validation_dir = run_path / "validation"
        validation_dir.mkdir(exist_ok=True)
        _write_json(validation_dir / "structure.json", {})

        _write_json(run_path / "approval.json", {"approved": True})

        results, commit_allowed = run_enforcement_pipeline(
            str(run_path),
            run_context=_minimal_run_context(),
        )

        return results, commit_allowed


def evaluate_structured(
    *,
    proposal: dict,
    compiled_contract: dict,
    run_context: dict,
):
    """
    New structured evaluation entrypoint.

    Bypasses filesystem-based run_path execution.
    """

    from cricore.enforcement.execution import run_execution_pipeline

    return run_execution_pipeline(
        proposal=proposal,
        compiled_contract=compiled_contract,
        run_context=run_context,
    )


def evaluate_run(run_path: str) -> bool:
    """
    Canonical enforcement entry point.
    """

    _, commit_allowed = run_enforcement_pipeline(
        run_path,
        run_context=_minimal_run_context(),
    )

    return commit_allowed


def _minimal_run_context() -> Dict[str, Any]:
    """
    Minimal valid run_context required for enforcement stages.
    """

    return {
        "independence": {},
        "integrity": {},
        "publication": {},
    }


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
