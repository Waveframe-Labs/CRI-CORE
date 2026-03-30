from __future__ import annotations

"""
---
title: "CRI-CORE Public API"
filetype: "operational"
type: "interface"
domain: "enforcement"
version: "0.2.0"
doi: "TBD-0.2.0"
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
  - "CRI-CORE-API-Evaluate-v0.2.0"
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
    Convenience evaluation interface.

    NOTE:
    - proposal must already be normalized
    - compiled_contract must already be compiled

    This function materializes a minimal run structure and executes the pipeline.
    It is intended for experimentation and local evaluation.

    For strict, production-aligned enforcement, use evaluate_run().
    """

    with tempfile.TemporaryDirectory() as tmpdir:
        run_path = Path(tmpdir)

        # --- Core artifacts ---
        _write_json(run_path / "proposal.json", proposal)
        _write_json(run_path / "compiled_contract.json", compiled_contract)

        # Minimal contract.json (required for structure stage)
        contract_stub = {
            "contract_version": compiled_contract.get("contract_version", "unknown"),
            "run_id": "api-run",
            "created_utc": "2026-01-01T00:00:00Z",
        }
        _write_json(run_path / "contract.json", contract_stub)

        # --- Required supporting artifacts ---
        _write_json(run_path / "randomness.json", {"deterministic": True})

        (run_path / "report.md").write_text("# API Run\n", encoding="utf-8")

        (run_path / "SHA256SUMS.txt").write_text("", encoding="utf-8")

        validation_dir = run_path / "validation"
        validation_dir.mkdir(exist_ok=True)
        _write_json(validation_dir / "structure.json", {})

        # Minimal approval stub
        _write_json(run_path / "approval.json", {"approved": True})

        # --- Execute enforcement pipeline ---
        results, commit_allowed = run_enforcement_pipeline(str(run_path))

        return results, commit_allowed


def evaluate_run(run_path: str) -> bool:
    """
    Canonical CRI-CORE enforcement entry point.

    Evaluates a fully materialized run directory and returns whether the
    proposed action is allowed to commit.

    Args:
        run_path: Path to a structured run directory

    Returns:
        commit_allowed (bool)

    This function preserves full enforcement semantics and should be used
    in production or system integrations.
    """

    _, commit_allowed = run_enforcement_pipeline(run_path)

    return commit_allowed


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")