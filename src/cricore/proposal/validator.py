"""
---
title: "CRI-CORE Proposal Validator"
filetype: "source"
type: "implementation"
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
  - "../../../schema/proposal.schema.json"

anchors:
  - "CRI-CORE-PROPOSAL-VALIDATOR-v0.1.0"
---
"""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema


SCHEMA_PATH = Path(__file__).resolve().parents[3] / "schema" / "proposal.schema.json"


class ProposalValidationError(RuntimeError):
    """Raised when a proposal fails schema validation."""


def _load_schema():
    with SCHEMA_PATH.open(encoding="utf-8") as f:
        schema = json.load(f)

    Validator = jsonschema.validators.validator_for(schema)
    Validator.check_schema(schema)

    return Validator(schema)


VALIDATOR = _load_schema()


def validate_proposal(proposal: dict) -> None:
    """
    Validate a canonical proposal object.

    Raises
    ------
    ProposalValidationError
        If the proposal violates the canonical schema.
    """
    try:
        VALIDATOR.validate(proposal)
    except jsonschema.ValidationError as e:
        raise ProposalValidationError(str(e)) from e