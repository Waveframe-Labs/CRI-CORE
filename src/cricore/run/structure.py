"""
---
title: "CRI-CORE Run Artifact Structural Validator"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.2.0"
doi: "TBD-0.2.0"
status: "Active"
created: "2026-02-09"
updated: "2026-02-16"

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
ai_assistance_details: "AI-assisted refactor separating structural validation from explicit contract version gate enforcement."

dependencies:
  - "./paths.py"
  - "../results/model.py"
  - "../results/stage.py"
  - "../errors.py"
  - "../contract/loader.py"

anchors:
  - "CRI-CORE-RunStructureValidator-v0.2.0"
---
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .paths import required_directory_paths, required_file_paths
from ..contract.loader import (
    ContractDeclarationError,
    extract_contract_version,
    extract_created_utc,
    extract_run_id,
    load_contract_declaration,
)
from ..results.model import ValidationResult
from ..results.stage import StageResult
from ..errors import FailureClass


# -------------------------------------------------------------------
# Core structural validation (no version gate here anymore)
# -------------------------------------------------------------------

def validate_run_structure(
    run_path: str,
) -> ValidationResult:

    run_root = Path(run_path)

    missing_paths = []
    invalid_paths = []
    contract_errors = []
    invariant_errors = []
    warnings = []

    run_id_from_path = run_root.name if run_root.exists() else None
    declared_contract_version: Optional[str] = None

    if not run_root.exists():
        missing_paths.append(str(run_root))
    elif not run_root.is_dir():
        invalid_paths.append(str(run_root))

    if run_root.exists() and run_root.is_dir():
        try:
            contract_obj = load_contract_declaration(run_root)

            declared_contract_version = extract_contract_version(contract_obj)
            declared_run_id = extract_run_id(contract_obj)
            declared_created_utc = extract_created_utc(contract_obj)

            if declared_contract_version is None:
                contract_errors.append("contract_version missing or not a string in contract.json")

            if declared_run_id is None:
                contract_errors.append("run_id missing or not a string in contract.json")
            elif run_id_from_path is not None and declared_run_id != run_id_from_path:
                contract_errors.append("run_id in contract.json does not match run directory name")

            if declared_created_utc is None:
                contract_errors.append("created_utc missing or not a string in contract.json")

        except ContractDeclarationError as exc:
            contract_errors.append(str(exc))

        for p in required_file_paths(run_root):
            if not p.exists():
                missing_paths.append(str(p))
            elif not p.is_file():
                invalid_paths.append(str(p))

        for p in required_directory_paths(run_root):
            if not p.exists():
                missing_paths.append(str(p))
            elif not p.is_dir():
                invalid_paths.append(str(p))

    passed = (
        not missing_paths
        and not invalid_paths
        and not contract_errors
        and not invariant_errors
    )

    return ValidationResult(
        contract_version=declared_contract_version,
        run_id=run_id_from_path,
        run_path=str(run_root),
        passed=passed,
        missing_paths=missing_paths,
        invalid_paths=invalid_paths,
        contract_errors=contract_errors,
        invariant_errors=invariant_errors,
        warnings=warnings,
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        engine_version=None,
    )


# -------------------------------------------------------------------
# Stage: run-structure
# -------------------------------------------------------------------

def run_structure_stage(
    run_path: str,
) -> StageResult:

    result = validate_run_structure(run_path)

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


# -------------------------------------------------------------------
# Stage: structure-contract-version-gate
# -------------------------------------------------------------------

def run_structure_contract_version_gate_stage(
    run_path: str,
    *,
    expected_contract_version: Optional[str],
) -> StageResult:

    result = validate_run_structure(run_path)

    failure_classes = []
    messages = []

    if expected_contract_version is not None:
        if result.contract_version != expected_contract_version:
            failure_classes.append(FailureClass.INVARIANT_VIOLATION)
            messages.append("Declared contract version does not match expected version")

    passed = not failure_classes

    return StageResult(
        stage_id="structure-contract-version-gate",
        passed=passed,
        failure_classes=failure_classes,
        messages=messages,
        checked_at_utc=result.checked_at_utc,
        engine_version=result.engine_version,
    )
