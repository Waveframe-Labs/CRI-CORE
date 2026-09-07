"""Public mode contract, including the issue #2 omitted-mode reproduction."""

from copy import deepcopy
from dataclasses import asdict
import importlib
import json
from pathlib import Path
from types import MappingProxyType
from unittest.mock import Mock

import pytest

import cricore
from cricore.api import evaluate, evaluate_structured
from cricore.enforcement import execution
from cricore.enforcement.integrity import (
    run_integrity_stage, run_integrity_finalization_stage,
)
from cricore.enforcement.publication import (
    run_publication_stage, run_publication_commit_stage,
)
from cricore.interface.evaluate_core import evaluate_core
from cricore.interface.evaluate_proposal import evaluate_proposal
from cricore.interface.governed_execute import governed_execute


@pytest.fixture
def inputs():
    evidence = Path(__file__).parent / "fixtures" / "issue2_baseline.json"
    return json.loads(evidence.read_text(encoding="utf-8"))["inputs"]


@pytest.fixture(params=[
    "structured", "root-structured", "execution", "core", "proposal",
    "evaluate", "root-evaluate", "enforcement", "root-enforcement", "disk-context",
])
def call(request, tmp_path, monkeypatch):
    # Keep the historical proposal wrapper's scratch artifacts within pytest's tree.
    proposal_module = importlib.import_module("cricore.interface.evaluate_proposal")
    mkdtemp = proposal_module.tempfile.mkdtemp
    monkeypatch.setattr(proposal_module.tempfile, "mkdtemp",
                        lambda **kwargs: mkdtemp(dir=tmp_path, **kwargs))

    def invoke(data, **kwargs):
        proposal, contract, context = (
            data["proposal"], data["compiled_contract"], data["run_context"]
        )
        structured = {
            "structured": evaluate_structured,
            "root-structured": cricore.evaluate_structured,
            "execution": execution.run_execution_pipeline,
            "core": evaluate_core,
        }
        if request.param in structured:
            return structured[request.param](**data, **kwargs)
        if request.param == "proposal":
            # The wrapper's supported context source is embedded in the proposal.
            embedded = dict(proposal, run_context=context)
            before = deepcopy(embedded)
            try:
                return evaluate_proposal(embedded, contract, run_id="mode-test", **kwargs)
            finally:
                assert embedded == before
        disk_context = dict(context) if request.param == "disk-context" else {}
        if isinstance(disk_context.get("mode"), bytes):
            pytest.skip("bytes cannot occur in a JSON run_context; covered via function arguments")
        for name, obj in (("proposal", proposal), ("compiled_contract", contract),
                          ("run_context", disk_context)):
            (tmp_path / f"{name}.json").write_text(json.dumps(obj), encoding="utf-8")
        before = {p.name: p.read_bytes() for p in tmp_path.glob("*.json")}
        filesystem = {
            "evaluate": evaluate,
            "root-evaluate": cricore.evaluate,
            "enforcement": execution.run_enforcement_pipeline,
            "root-enforcement": cricore.run_enforcement_pipeline,
            "disk-context": execution.run_enforcement_pipeline,
        }
        context_arg = {} if request.param == "disk-context" else {"run_context": context}
        try:
            result = filesystem[request.param](str(tmp_path), **context_arg, **kwargs)
        finally:
            assert before == {p.name: p.read_bytes() for p in tmp_path.glob("*.json")}
        if isinstance(result, tuple):
            stages, allowed = result
            return execution.EvaluationResult(
                allowed, [s.stage_id for s in stages if not s.passed], "", stages
            )
        return result

    return invoke


def trace(result):
    # Wall-clock observation metadata is not part of the policy decision trace.
    return [{k: v for k, v in asdict(s).items() if k != "checked_at_utc"}
            for s in result.stage_results]


@pytest.mark.parametrize("kwargs,allowed", [({}, False), ({"mode": "strict"}, False),
                                           ({"mode": "local"}, True)])
def test_mode_selection_and_missing_evidence(call, inputs, kwargs, allowed):
    original = deepcopy(inputs)
    result = call(inputs, **kwargs)
    assert result.commit_allowed is allowed
    if not allowed:
        assert {"integrity", "publication", "publication-commit"} <= set(result.failed_stages)
    else:
        assert any("missing" in message for s in result.stage_results for message in s.messages)
    assert inputs == original


@pytest.mark.parametrize("missing", ["integrity", "publication"])
def test_each_missing_evidence_section_blocks_default(call, inputs, missing):
    # These are the existing structural stage requirements, not invented evidence rules.
    inputs["run_context"].update(integrity={}, publication={})
    del inputs["run_context"][missing]
    result = call(inputs)
    assert result.commit_allowed is False
    assert missing in result.failed_stages
    other = "publication" if missing == "integrity" else "integrity"
    assert other not in result.failed_stages


@pytest.mark.parametrize("mode", ["strict", "local"])
def test_matching_explicit_declarations(call, inputs, mode):
    inputs["run_context"]["mode"] = mode
    assert call(inputs, mode=mode).commit_allowed is (mode == "local")


def test_existing_strict_success_conditions_are_unchanged(call, inputs):
    inputs["run_context"].update(mode="strict", integrity={}, publication={})
    assert call(inputs).commit_allowed is True


def test_explicit_local_retains_soft_failures(call, inputs):
    inputs["run_context"].update(
        integrity={"attestation_ref": 123}, publication={"commit_ref": 123}
    )
    assert call(inputs).commit_allowed is False
    result = call(inputs, mode="local")
    assert result.commit_allowed is True
    assert {"integrity", "publication"} <= set(result.failed_stages)


@pytest.mark.parametrize("kwargs,context_mode", [
    ({}, "local"), ({"mode": "strict"}, "local"), ({"mode": "local"}, "strict"),
])
def test_conflicts_precede_every_stage(call, inputs, monkeypatch, kwargs, context_mode):
    inputs["run_context"]["mode"] = context_mode
    original = deepcopy(inputs)
    stages = []
    for name in (
        "run_structure_stage", "_make_version_gate_stage", "_make_contract_hash_gate_stage",
        "run_independence_stage", "run_integrity_stage", "run_integrity_finalization_stage",
        "run_publication_stage", "run_publication_commit_stage",
    ):
        stage = Mock(side_effect=AssertionError("configuration must fail before policy"))
        monkeypatch.setattr(execution, name, stage)
        stages.append(stage)
    with pytest.raises(ValueError, match="^CRI_MODE_CONFLICT:.*match the function mode"):
        call(inputs, **kwargs)
    assert all(stage.call_count == 0 for stage in stages)
    assert inputs == original


INVALID_MODES = [None, "", "unknown", "STRICT", "Local", " strict", "local ", "strict\n",
                 0, 1, True, False, 1.0, b"strict", [], {}, ["local"]]


@pytest.mark.parametrize("value", INVALID_MODES)
@pytest.mark.parametrize("location", ["argument", "context", "both"])
def test_invalid_modes_fail_before_stages(call, inputs, monkeypatch, value, location):
    kwargs = {"mode": value} if location in ("argument", "both") else {}
    if location in ("context", "both"):
        inputs["run_context"]["mode"] = value
    original = deepcopy(inputs)
    stage = Mock(side_effect=AssertionError("invalid mode reached policy"))
    monkeypatch.setattr(execution, "run_structure_stage", stage)
    with pytest.raises(ValueError, match='^CRI_MODE_INVALID:.*must be exactly "strict" or "local"'):
        call(inputs, **kwargs)
    stage.assert_not_called()
    assert inputs == original


@pytest.mark.parametrize("mode", ["strict", "local"])
def test_decisions_and_policy_traces_are_deterministic_and_inputs_immutable(call, inputs, mode):
    original = deepcopy(inputs)
    first, second = call(inputs, mode=mode), call(inputs, mode=mode)
    assert (first.commit_allowed, first.failed_stages, first.summary) == (
        second.commit_allowed, second.failed_stages, second.summary
    )
    assert trace(first) == trace(second)
    assert inputs == original


def test_canonical_imports():
    api = importlib.import_module("cricore.api")
    module = importlib.import_module("cricore.api.evaluate")
    assert Path(api.__file__).parts[-2:] == ("api", "__init__.py")
    assert api.evaluate_structured is module.evaluate_structured is cricore.evaluate_structured
    assert api.evaluate is module.evaluate is cricore.evaluate
    assert not (Path(cricore.__file__).parent / "api.py").exists()


def test_read_only_mapping_context_cannot_downgrade(inputs):
    inputs["run_context"] = MappingProxyType(dict(inputs["run_context"], mode="local"))
    with pytest.raises(ValueError, match="CRI_MODE_CONFLICT"):
        evaluate_structured(**inputs)
    assert evaluate_structured(**inputs, mode="local").commit_allowed is True


@pytest.mark.parametrize("context_mode", [None, "local", "strict"])
def test_governed_execution_never_runs_advisory_callback(inputs, context_mode):
    context = inputs["run_context"]
    if context_mode is not None:
        context["mode"] = context_mode
    proposal = dict(inputs["proposal"], run_context=context)
    callback = Mock()
    if context_mode == "local":
        with pytest.raises(ValueError, match="CRI_MODE_CONFLICT"):
            governed_execute(proposal, inputs["compiled_contract"], callback)
    else:
        result = governed_execute(proposal, inputs["compiled_contract"], callback)
        assert result["blocked"] is True
    callback.assert_not_called()


@pytest.mark.parametrize("stage", [run_integrity_stage, run_integrity_finalization_stage,
                                   run_publication_stage, run_publication_commit_stage])
def test_direct_mode_sensitive_stages_share_contract(stage, inputs):
    kwargs = dict(inputs)
    if stage is run_integrity_finalization_stage:
        kwargs["prerequisite_passed"] = False
    if stage is run_publication_commit_stage:
        kwargs["prior_stage_results"] = [run_integrity_stage(**inputs)]
    assert stage(**kwargs).passed is False
    assert stage(**kwargs, mode="strict").passed is False
    assert stage(**kwargs, mode="local").passed is True
    for value in INVALID_MODES:
        with pytest.raises(ValueError, match="CRI_MODE_INVALID"):
            stage(**kwargs, mode=value)
    kwargs["run_context"]["mode"] = "local"
    with pytest.raises(ValueError, match="CRI_MODE_CONFLICT"):
        stage(**kwargs)
    assert stage(**kwargs, mode="local").passed is True


def test_issue2_reproduction_matches_preserved_baseline(inputs):
    evidence = json.loads((Path(__file__).parent / "fixtures" / "issue2_baseline.json").read_text())
    assert evidence["base"] == "28bc5636e4edadc6442cb003cb91df091286cb05"
    assert evidence["results"]["omitted"]["commit_allowed"] is True
    assert evaluate_structured(**inputs).commit_allowed is False
    assert evaluate_structured(**inputs, mode="local").commit_allowed is True
