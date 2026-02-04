#!/usr/bin/env python3
"""
CRI-CORE root CLI (validate → run → commit)

- validate <workflow.json>: AWO-aligned structure checks (claims/falsification)
- run <workflow.json>: creates runs/<id>/ with manifest, workflow copy, hashes, lock
- commit <run_id>: stages gate checklists under runs/<id>/gates/
"""

import argparse
import json
import sys
import hashlib
import zlib
import time
import pathlib
import subprocess  # for Git provenance

# Try to import version from root __init__.py; fall back quietly.
try:
    from __init__ import __version__  # type: ignore
except Exception:
    __version__ = "0.1.0"

ROOT = pathlib.Path(__file__).resolve().parent
RUNS = ROOT / "runs"

# ---------- path resolver (works locally and in CI) ----------
def _resolve_workflow_path(workflow_path: str) -> pathlib.Path:
    """
    Resolve a workflow path safely:
    - If absolute, return as-is.
    - If relative, prefer path relative to this file's directory (repo root).
    - Fallback to current working directory if needed.
    """
    p = pathlib.Path(workflow_path)
    if p.is_absolute():
        return p
    candidate = (ROOT / p).resolve()
    if candidate.exists():
        return candidate
    return (pathlib.Path.cwd() / p).resolve()
# -------------------------------------------------------------

def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def _compress_ratio(b: bytes) -> float:
    if not b:
        return 1.0
    return len(zlib.compress(b)) / len(b)

def _get_git_info(repo_root: pathlib.Path) -> dict:
    """Collect Git provenance; return empty fields if Git unavailable."""
    def _run(args):
        try:
            out = subprocess.check_output(args, cwd=repo_root, stderr=subprocess.DEVNULL)
            return out.decode("utf-8").strip()
        except Exception:
            return ""
    # `dirty` returns True if there is any uncommitted change
    dirty_out = _run(["git", "status", "--porcelain"])
    return {
        "head":   _run(["git", "rev-parse", "HEAD"]),
        "branch": _run(["git", "rev-parse", "--abbrev-ref", "HEAD"]),
        "remote": _run(["git", "config", "--get", "remote.origin.url"]),
        "dirty":  bool(dirty_out)
    }

# -------------------------- VALIDATE --------------------------
def cmd_validate(workflow_path: str) -> int:
    p = _resolve_workflow_path(workflow_path)
    try:
        wf = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"✗ Invalid JSON: {e}")
        return 1

    # AWO minimal contract for a runnable workflow
    must_have = ["id", "name", "steps", "claims"]
    missing = [k for k in must_have if k not in wf]
    if missing:
        print(f"✗ Missing keys: {missing}")
        return 2

    # steps: array of objects with id + type
    if not isinstance(wf["steps"], list) or any(not isinstance(s, dict) for s in wf["steps"]):
        print("✗ 'steps' must be an array of objects")
        return 2
    for i, s in enumerate(wf["steps"], 1):
        for k in ["id", "type"]:
            if k not in s:
                print(f"✗ step[{i}] missing '{k}'")
                return 2

    # claims: each must include falsification tuple per AWO (dataset, procedure, metric)
    claim_errors = []
    for i, c in enumerate(wf.get("claims", []), 1):
        if not isinstance(c, dict):
            claim_errors.append(f"claim[{i}] not an object"); continue
        for k in ["id", "statement", "falsification"]:
            if k not in c:
                claim_errors.append(f"claim[{i}] missing '{k}'"); continue
        fals = c.get("falsification", {})
        for k in ["dataset", "procedure", "metric"]:
            if k not in fals:
                claim_errors.append(f"claim[{i}].falsification missing '{k}'")
        metric = fals.get("metric", {})
        for k in ["name", "target", "tolerance", "units"]:
            if k not in metric:
                claim_errors.append(f"claim[{i}].falsification.metric missing '{k}'")

    if claim_errors:
        print("✗ Claim validation errors:")
        for e in claim_errors:
            print("  -", e)
        return 2

    print("✓ Workflow validated (AWO-aligned)")
    return 0

# ----------------------------- RUN ----------------------------
def cmd_run(workflow_path: str) -> int:
    RUNS.mkdir(exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    stem = pathlib.Path(workflow_path).stem
    run_id = f"{ts}-{stem}"
    rdir = RUNS / run_id
    rdir.mkdir(parents=True, exist_ok=True)

    # Load workflow and compute its hash
    wf_path = _resolve_workflow_path(workflow_path)
    raw = wf_path.read_bytes()
    wf = json.loads(raw)

    # Copy exact workflow into the run (immutability & inspection)
    (rdir / "workflow.json").write_bytes(raw)

    # Gather context
    steps  = wf.get("steps", [])
    claims = wf.get("claims", [])
    git    = _get_git_info(ROOT)

    # Manifest with Git provenance + workflow provenance
    # Include workflow_path relative to repo root when possible
    try:
        rel_path = str(wf_path.relative_to(ROOT))
    except ValueError:
        rel_path = str(wf_path)

    manifest = {
        "run_id": run_id,
        "started_at": ts,

        # workflow provenance
        "workflow_id": wf.get("id"),
        "workflow_name": wf.get("name"),
        "workflow_path": rel_path,
        "workflow_sha256": _sha256_bytes(raw),

        # AWO alignment
        "claims": [c.get("id") for c in claims],

        # execution outline
        "steps": steps,

        # repo provenance (binds run to source state)
        "git": git,

        # lightweight analytics
        "info_density": round(1.0 - _compress_ratio(raw), 4)
    }

    # Write manifest
    (rdir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # Hash seal: proves key artifacts at creation time
    seal_lines = [
        f"{manifest['workflow_sha256']}  workflow.json",
        f"{_sha256_bytes((rdir / 'run_manifest.json').read_bytes())}  run_manifest.json",
    ]
    (rdir / "SHA256SUMS.txt").write_text("\n".join(seal_lines) + "\n", encoding="utf-8")

    # Lock sentinel (human-facing)
    (rdir / "RUN_LOCK.txt").write_text(
        "This directory is a sealed CRI run. Do not edit files in-place.\n"
        "Regenerate via CLI to change state. See run_manifest.json for provenance.\n",
        encoding="utf-8"
    )

    print(f"✓ Run created: runs/{run_id}")
    return 0

# --------------------------- COMMIT ---------------------------
def cmd_commit(run_id: str) -> int:
    rdir = RUNS / run_id
    if not rdir.exists():
        print("✗ Run folder not found")
        return 1
    gates = rdir / "gates"
    gates.mkdir(exist_ok=True)
    (gates / "scope_checklist.md").write_text(
        "# Scope Gate\n- [ ] Objectives clear\n- [ ] Data sources listed\n", encoding="utf-8"
    )
    (gates / "merge_checklist.md").write_text(
        "# Merge Gate\n- [ ] Repro steps pass\n- [ ] Hashes verified\n", encoding="utf-8"
    )
    print(f"✓ Gates staged in runs/{run_id}/gates")
    return 0

# ---------------------------- MAIN ---------------------------
def main() -> int:
    ap = argparse.ArgumentParser(prog="cri", description="CRI-CORE CLI")
    ap.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sp = ap.add_subparsers(dest="cmd", required=True)

    v = sp.add_parser("validate", help="validate a workflow JSON")
    v.add_argument("workflow")

    r = sp.add_parser("run", help="execute a workflow and emit a run artifact")
    r.add_argument("workflow")

    c = sp.add_parser("commit", help="stage audit gates for a run")
    c.add_argument("run_id")

    args = ap.parse_args()
    if args.cmd == "validate":
        return cmd_validate(args.workflow)
    if args.cmd == "run":
        return cmd_run(args.workflow)
    if args.cmd == "commit":
        return cmd_commit(args.run_id)
    return 2

if __name__ == "__main__":
    sys.exit(main())
