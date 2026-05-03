"""
---
title: "CRI-CORE Run Artifact Structural Validator"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.3.0"
doi: "TBD-0.3.0"
status: "Active"
created: "2026-02-09"
updated: "2026-03-17"

author:
  name: "Shawn C. Wright"
  email: "swright@waveframelabs.org"
  orcid: "https://orcid.org/0009-0006-6043-9295"

maintainer:
  name: "Waveframe Labs"
  url: "https://waveframelabs.org"

license: "Apache-2.0"

copyright:
  holder: "Waveframe Labs"
  year: "2026"

ai_assisted: "partial"

dependencies:
  - "../results/model.py"
  - "../results/stage.py"
  - "../errors.py"

anchors:
  - "CRI-CORE-RunStructureValidator-v0.3.0"
---
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping, Optional

from ..errors import FailureClass
from ..results.model import ValidationResult
from ..results.stage import StageResult


def validate_run_structure(
    *,
    proposal: Mapping[str, Any],
    compiled_contract: Mapping[str, Any],
    expected_contract_version: Optional[str] = None,
) -> ValidationResult:
    """
    Validate the structured CRI-CORE evaluation inputs.
    """

    missing_paths: list[str] = []
    invalid_paths: list[str] = []
    contract_errors: list[str] = []
    invariant_errors: list[str] = []
    warnings: list[str] = []

    declared_contract_version = compiled_contract.get("contract_version")
    run_id = proposal.get("proposal_id")

    if not isinstance(proposal, Mapping):
        invariant_errors.append("proposal must be a mapping")
    if not isinstance(compiled_contract, Mapping):
        invariant_errors.append("compiled_contract must be a mapping")

    proposal_contract = proposal.get("contract")
    if not isinstance(proposal_contract, Mapping):
        contract_errors.append("proposal.contract missing or not a mapping")
    else:
        proposal_contract_id = proposal_contract.get("id")
        proposal_contract_version = proposal_contract.get("version")
        proposal_contract_hash = proposal_contract.get("hash")

        if not isinstance(proposal_contract_id, str) or not proposal_contract_id.strip():
            contract_errors.append("proposal.contract.id missing or invalid")
        if not isinstance(proposal_contract_version, str) or not proposal_contract_version.strip():
            contract_errors.append("proposal.contract.version missing or invalid")
        if not isinstance(proposal_contract_hash, str) or not proposal_contract_hash.strip():
            contract_errors.append("proposal.contract.hash missing or invalid")

    compiled_contract_id = compiled_contract.get("contract_id")
    compiled_contract_version = compiled_contract.get("contract_version")
    compiled_contract_hash = compiled_contract.get("contract_hash")

    if not isinstance(compiled_contract_id, str) or not compiled_contract_id.strip():
        contract_errors.append("compiled_contract.contract_id missing or invalid")
    if not isinstance(compiled_contract_version, str) or not compiled_contract_version.strip():
        contract_errors.append("compiled_contract.contract_version missing or invalid")
    if not isinstance(compiled_contract_hash, str) or not compiled_contract_hash.strip():
        contract_errors.append("compiled_contract.contract_hash missing or invalid")

    if isinstance(proposal_contract, Mapping):
        if proposal_contract.get("id") != compiled_contract_id:
            contract_errors.append("proposal contract id does not match compiled contract")
        if proposal_contract.get("version") != compiled_contract_version:
            contract_errors.append("proposal contract version does not match compiled contract")

    if expected_contract_version is not None and compiled_contract_version != expected_contract_version:
        contract_errors.append("Declared contract version does not match expected version")

    passed = (
        not missing_paths
        and not invalid_paths
        and not contract_errors
        and not invariant_errors
    )

    return ValidationResult(
        contract_version=declared_contract_version if isinstance(declared_contract_version, str) else None,
        run_id=run_id if isinstance(run_id, str) else None,
        run_path="",
        passed=passed,
        missing_paths=missing_paths,
        invalid_paths=invalid_paths,
        contract_errors=contract_errors,
        invariant_errors=invariant_errors,
        warnings=warnings,
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        engine_version=None,
    )


def run_structure_stage(
    *,
    proposal: Mapping[str, Any],
    compiled_contract: Mapping[str, Any],
    expected_contract_version: Optional[str] = None,
) -> StageResult:
    """
    Structural enforcement stage adapter for structured CRI-CORE inputs.
    """

    result = validate_run_structure(
        proposal=proposal,
        compiled_contract=compiled_contract,
        expected_contract_version=expected_contract_version,
    )

    failure_classes = []

    if result.missing_paths:
        failure_classes.append(FailureClass.MISSING_REQUIRED_ARTIFACT)

    if result.invalid_paths:
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)

    if result.contract_errors:
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)

    if result.invariant_errors:
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)

    messages = []
    messages.extend(result.missing_paths)
    messages.extend(result.invalid_paths)
    messages.extend(result.contract_errors)
    messages.extend(result.invariant_errors)

    return StageResult(
        stage_id="run-structure",
        passed=result.passed,
        failure_classes=failure_classes,
        messages=messages,
        checked_at_utc=result.checked_at_utc,
        engine_version=result.engine_version,
    )
