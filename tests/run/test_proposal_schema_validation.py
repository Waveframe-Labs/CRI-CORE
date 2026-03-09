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
    with SCHEMA_PATH.open() as f:
        schema = json.load(f)

    Validator = jsonschema.validators.validator_for(schema)
    Validator.check_schema(schema)

    return Validator(schema, format_checker=jsonschema.FormatChecker())


def load_json(path: Path):
    with path.open() as f:
        return json.load(f)


def test_valid_proposals_pass_schema(validator):
    for file in sorted(VALID_FIXTURES.glob("*.json")):
        proposal = load_json(file)

        try:
            validator.validate(proposal)
        except jsonschema.ValidationError as e:
            pytest.fail(f"{file} should be valid but failed validation:\n{e}")


def test_invalid_proposals_fail_schema(validator):
    for file in sorted(INVALID_FIXTURES.glob("*.json")):
        proposal = load_json(file)

        with pytest.raises(jsonschema.ValidationError):
            validator.validate(proposal)
            