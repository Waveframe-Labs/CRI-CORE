"""
---
title: "CRI-CORE Compiled Contract Schema Validation Test"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-03-09"
updated: "2026-03-09"

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
  - "../../schema/contract.schema.json"

anchors:
  - "CRI-CORE-CONTRACT-SCHEMA-VALIDATION-TEST-v0.1.0"
---
"""

import json
from pathlib import Path

import pytest
import jsonschema
from jsonschema import Draft202012Validator


SCHEMA_PATH = Path("schema/contract.schema.json")

VALID_FIXTURES = Path("tests/fixtures/contracts/valid")
INVALID_FIXTURES = Path("tests/fixtures/contracts/invalid")


@pytest.fixture(scope="module")
def validator():
    with SCHEMA_PATH.open() as f:
        schema = json.load(f)

    return Draft202012Validator(schema)


def load_json(path: Path):
    with path.open() as f:
        return json.load(f)


def test_valid_contracts_pass_schema(validator):
    valid_files = sorted(VALID_FIXTURES.glob("*.json"))

    assert valid_files, "No valid contract fixtures found."

    for file in valid_files:
        contract = load_json(file)

        try:
            validator.validate(contract)
        except jsonschema.ValidationError as e:
            pytest.fail(
                f"{file} should be valid but failed schema validation:\n{e}"
            )


def test_invalid_contracts_fail_schema(validator):
    invalid_files = sorted(INVALID_FIXTURES.glob("*.json"))

    assert invalid_files, "No invalid contract fixtures found."

    for file in invalid_files:
        contract = load_json(file)

        try:
            validator.validate(contract)
        except jsonschema.ValidationError:
            # Correct behavior — schema rejected the contract
            continue

        pytest.fail(
            f"{file} should have failed schema validation but passed."
        )
        