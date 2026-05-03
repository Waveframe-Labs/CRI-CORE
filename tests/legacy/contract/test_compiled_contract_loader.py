"""
---
title: "CRI-CORE Compiled Contract Loader Test"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-03-10"
updated: "2026-03-10"

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
  - "../../src/cricore/contract/compiled_loader.py"
  - "../../schema/contract.schema.json"

anchors:
  - "CRI-CORE-COMPILED-CONTRACT-LOADER-TEST-v0.1.0"
---
"""

from pathlib import Path

import pytest

from cricore.contract.compiled_loader import load_compiled_contract
from cricore.contract.errors import (
    CompiledContractLoadError,
    CompiledContractValidationError,
)


VALID_FIXTURES = Path("tests/fixtures/contracts/valid")
INVALID_FIXTURES = Path("tests/fixtures/contracts/invalid")


def test_valid_compiled_contracts_load_successfully():
    valid_files = sorted(VALID_FIXTURES.glob("*.json"))

    assert valid_files, "No valid compiled contract fixtures found."

    for file in valid_files:
        contract = load_compiled_contract(file)

        assert contract.contract_id
        assert contract.contract_version


def test_invalid_compiled_contracts_fail_validation():
    invalid_files = sorted(INVALID_FIXTURES.glob("*.json"))

    assert invalid_files, "No invalid compiled contract fixtures found."

    for file in invalid_files:
        with pytest.raises((CompiledContractValidationError, CompiledContractLoadError)):
            load_compiled_contract(file)
