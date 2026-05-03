"""
---
title: "Independence Stage Multi-Role Enforcement Tests"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.2.0"
doi: "TBD-0.2.0"
status: "Active"
created: "2026-02-10"
updated: "2026-02-26"

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
ai_assistance_details: "AI-assisted drafting of updated independence stage tests aligned with ADR-001 multi-role structural model."

dependencies:
  - "../../src/cricore/enforcement/independence.py"

anchors:
  - "CRI-CORE-IndependenceTests-v0.2.0"
---
"""

from cricore.enforcement.independence import run_independence_stage


def test_missing_identities_fails():
    result = run_independence_stage("dummy", run_context={})
    assert result.passed is False


def test_no_required_roles_passes_structural_minimum():
    ctx = {
        "identities": {
            "actors": [
                {"id": "alice", "type": "human", "role": "initiator"}
            ]
        }
    }
    result = run_independence_stage("dummy", run_context=ctx)
    assert result.passed is True


def test_missing_required_role_fails():
    ctx = {
        "identities": {
            "actors": [
                {"id": "alice", "type": "human", "role": "initiator"}
            ],
            "required_roles": ["controller"]
        }
    }
    result = run_independence_stage("dummy", run_context=ctx)
    assert result.passed is False


def test_multiple_candidates_for_required_role_fails():
    ctx = {
        "identities": {
            "actors": [
                {"id": "alice", "type": "human", "role": "controller"},
                {"id": "bob", "type": "human", "role": "controller"}
            ],
            "required_roles": ["controller"]
        }
    }
    result = run_independence_stage("dummy", run_context=ctx)
    assert result.passed is False


def test_duplicate_identity_across_required_roles_fails():
    ctx = {
        "identities": {
            "actors": [
                {"id": "alice", "type": "human", "role": "controller"},
                {"id": "alice", "type": "human", "role": "cfo"}
            ],
            "required_roles": ["controller", "cfo"]
        }
    }
    result = run_independence_stage("dummy", run_context=ctx)
    assert result.passed is False


def test_conflict_flag_blocks_required_role():
    ctx = {
        "identities": {
            "actors": [
                {"id": "alice", "type": "human", "role": "controller"},
                {"id": "bob", "type": "human", "role": "cfo"}
            ],
            "required_roles": ["controller", "cfo"],
            "conflict_flags": {
                "bob": True
            }
        }
    }
    result = run_independence_stage("dummy", run_context=ctx)
    assert result.passed is False


def test_valid_multi_role_configuration_passes():
    ctx = {
        "identities": {
            "actors": [
                {"id": "alice", "type": "human", "role": "initiator"},
                {"id": "bob", "type": "human", "role": "controller"},
                {"id": "carol", "type": "human", "role": "cfo"}
            ],
            "required_roles": ["controller", "cfo"],
            "conflict_flags": {
                "bob": False,
                "carol": False
            }
        }
    }
    result = run_independence_stage("dummy", run_context=ctx)
    assert result.passed is True


def test_identity_with_multiple_roles_including_required_fails():
    ctx = {
        "identities": {
            "actors": [
                {"id": "alice", "type": "human", "role": "initiator"},
                {"id": "alice", "type": "human", "role": "controller"},
                {"id": "bob", "type": "human", "role": "cfo"}
            ],
            "required_roles": ["controller", "cfo"]
        }
    }
    result = run_independence_stage("dummy", run_context=ctx)
    assert result.passed is False