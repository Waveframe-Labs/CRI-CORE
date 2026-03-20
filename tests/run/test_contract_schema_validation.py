"""
---
title: "CRI-CORE Contract Schema Validation Test"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.2.0"
doi: "TBD-0.2.0"
status: "Active"
created: "2026-03-09"
updated: "2026-03-19"

author:
  name: "Shawn C. Wright"
  email: "swright@waveframelabs.org"
  orcid: "https://orcid.org/0009-0006-6043-9295"

maintainer:
  name: "Waveframe Labs"
  url: "https://waveframelabs.org"

license: "Apache-2.0"

ai_assisted: "partial"

dependencies:
  - "../../src/cricore/schema/contract.schema.json"

anchors:
  - "CRI-CORE-CONTRACT-SCHEMA-VALIDATION-v0.2.0"
---
"""

import json
from importlib.resources import files

import pytest
from jsonschema import Draft202012Validator


SCHEMA_PATH = files("cricore").joinpath("schema/contract.schema.json")


@pytest.fixture(scope="module")
def validator():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def test_valid_contracts_pass_schema(validator):
    base = files("tests").joinpath("fixtures/contracts/valid")

    for path in base.iterdir():
        obj = json.loads(path.read_text(encoding="utf-8"))
        validator.validate(obj)


def test_invalid_contracts_fail_schema(validator):
    base = files("tests").joinpath("fixtures/contracts/invalid")

    for path in base.iterdir():
        obj = json.loads(path.read_text(encoding="utf-8"))
        with pytest.raises(Exception):
            validator.validate(obj)