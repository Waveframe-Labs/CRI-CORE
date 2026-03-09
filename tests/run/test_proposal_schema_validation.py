"""
---
title: "CRI-CORE Canonical Proposal Schema Validation Test"
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
  - "../../schema/proposal.schema.json"

anchors:
  - "CRI-CORE-PROPOSAL-SCHEMA-VALIDATION-TEST-v0.1.0"
---
"""

import json
from pathlib import Path

import pytest
import jsonschema


SCHEMA_PATH = Path("schema/proposal.schema.json")
VALID_FIXTURES = Path("tests/fixtures/proposals/valid")
INVALID_FIXTURES = Path("tests/fixtures/proposals/invalid")


@pytest.fixture(scope="module")
def validator():
    with SCHEMA_PATH.open(encoding="utf-8") as f:
        schema = json.load(f)

    Validator = jsonschema.validators.validator_for(schema)
    Validator.check_schema(schema)

    return Validator(
        schema,
        format_checker=jsonschema.FormatChecker()
    )


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def test_valid_proposals_pass_schema(validator):
    valid_files = sorted(VALID_FIXTURES.glob("*.json"))

    assert valid_files, "No valid proposal fixtures found."

    for file in valid_files:
        proposal = load_json(file)

        try:
            validator.validate(proposal)
        except jsonschema.ValidationError as e:
            pytest.fail(
                f"{file} should be valid but failed schema validation:\n{e}"
            )


def test_invalid_proposals_fail_schema(validator):
    invalid_files = sorted(INVALID_FIXTURES.glob("*.json"))

    assert invalid_files, "No invalid proposal fixtures found."

    for file in invalid_files:
        proposal = load_json(file)

        try:
            validator.validate(proposal)
        except jsonschema.ValidationError:
            # Correct behavior — schema rejected the proposal
            continue

        pytest.fail(
            f"{file} should have failed schema validation but passed."
        )