#!/usr/bin/env python3
"""
CRI-CORE root CLI (validate → run → commit)

- validate <workflow.json>: basic structure check
- run <workflow.json>: writes runs/<id>/run_manifest.json + SHA256SUMS.txt
- commit <run_id>: stages gate checklists under runs/<id>/gates/
"""

import argparse
import json
import sys
import hashlib
import zlib
import time
import pathlib

# Try to import version from root __init__.py if you’ve set it; fall back quietly.
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

def cmd_validate(workflow_path: str) -> int:
    p = _resolve_workflow_path(workflow_path)
    try:
        wf = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"✗ Invalid JSON: {e}")
        return 1
    required = ["id", "name", "steps"]
    missing = [k for k in required if k not in wf]
    if missing:
        print(f"✗ Missing keys: {missing}")
        return 2
    print("✓ Workflow validated")
    return 0

def cmd_run(workflow_path: str) -> int:
    RUNS.mkdir(exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    stem = pathlib.Path(workflow_path).stem
    run_id = f"{ts}-{stem}"
    rdir = RUNS / run_id
    rdir.mkdir(parents=True, exist_ok=True)

    raw = _resolve_workflow_path(workflow_path).read_bytes()
    steps = json.loads(raw).get("steps", [])
    manifest = {
        "run_id": run_id,
        "workflow_sha256": _sha256_bytes(raw),
        "info_density": round(1.0 - _compress_ratio(raw), 4),  # harmless proxy
        "started_at": ts,
        "steps": steps,
    }
    (rdir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (rdir / "SHA256SUMS.txt").write_text(f"{manifest['workflow_sha256']}  {pathlib.Path(workflow_path)}\n", encoding="utf-8")
    print(f"✓ Run created: runs/{run_id}")
    return 0

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
