import argparse, json, sys, hashlib, re, datetime, pathlib, subprocess

BASE = pathlib.Path(__file__).resolve().parents[1]

def _load(p): return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
def _dump(p, obj): p=pathlib.Path(p); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(obj, indent=2), encoding="utf-8")
def _sha(p): h=hashlib.sha256(); h.update(pathlib.Path(p).read_bytes()); return h.hexdigest()
def _ts(): return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H%M%SZ")
def _slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "run"

def _validate(obj, schema, path="$", errs=None):
    if errs is None: errs=[]
    t=schema.get("type")
    if t=="object" and not isinstance(obj,dict): errs.append(f"{path}: expected object")
    if t=="array" and not isinstance(obj,list): errs.append(f"{path}: expected array")
    if t=="string" and not isinstance(obj,str): errs.append(f"{path}: expected string")
    if t=="number" and not isinstance(obj,(int,float)): errs.append(f"{path}: expected number")
    if t=="boolean" and not isinstance(obj,bool): errs.append(f"{path}: expected boolean")
    if isinstance(obj,dict):
        for r in schema.get("required",[]): 
            if r not in obj: errs.append(f"{path}.{r}: missing required property")
        props=schema.get("properties",{})
        for k,v in obj.items():
            if k in props: _validate(v, props[k], f"{path}.{k}", errs)
            elif schema.get("additionalProperties") is False: errs.append(f"{path}.{k}: additionalProperties not allowed")
    if isinstance(obj,list) and "items" in schema:
        for i,it in enumerate(obj): _validate(it, schema["items"], f"{path}[{i}]", errs)
    if "enum" in schema and obj not in schema["enum"]: errs.append(f"{path}: value '{obj}' not in enum {schema['enum']}")
    if "pattern" in schema and isinstance(obj,str) and not re.match(schema["pattern"], obj): errs.append(f"{path}: string doesn't match pattern {schema['pattern']}")
    if "minLength" in schema and isinstance(obj,str) and len(obj)<schema["minLength"]: errs.append(f"{path}: string too short (minLength={schema['minLength']})")
    return errs

def cmd_validate(args):
    wf=(BASE/args.workflow).resolve()
    if not wf.exists(): print(f"ERROR: workflow not found: {wf}", file=sys.stderr); return 2
    schema=_load(BASE/"schemas/workflow.schema.json"); wf_obj=_load(wf)
    errs=_validate(wf_obj, schema, "$")
    missing=[i["path"] for i in wf_obj.get("inputs",[]) if not (BASE/i["path"]).exists()]
    if missing: errs.append(f"$: missing inputs -> {', '.join(missing)}")
    if errs: [print("SCHEMA:",e,file=sys.stderr) for e in errs]; return 1
    print("OK"); return 0

def cmd_run(args):
    wf_path=(BASE/args.workflow).resolve()
    if not wf_path.exists(): print(f"ERROR: workflow not found: {wf_path}", file=sys.stderr); return 2
    wf=_load(wf_path); slug=_slug(wf.get("name","run")); run_id=f"{_ts()}-{slug}"
    run_dir=BASE/"runs"/run_id
    (run_dir/"reports").mkdir(parents=True, exist_ok=True)
    (run_dir/"gates").mkdir(parents=True, exist_ok=True)
    # copy gate templates
    for g in ("scope_checklist.md","merge_checklist.md"):
        (run_dir/"gates"/g).write_text((BASE/"templates"/"gates"/g).read_text(encoding="utf-8"), encoding="utf-8")
    # validate and stamp
    schema=_load(BASE/"schemas/workflow.schema.json")
    errs=_validate(wf, schema, "$")
    missing=[i["path"] for i in wf.get("inputs",[]) if not (BASE/i["path"]).exists()]
    status="pass" if (not errs and not missing) else "fail"
    _dump(run_dir/"reports"/"validate.json", {"timestamp":_ts(),"status":status,"schema_errors":errs,"missing_inputs":missing})
    _dump(run_dir/"manifest.json", {
        "run_id":run_id,"started_at":_ts(),"finished_at":None,
        "workflow_path":str(pathlib.Path(args.workflow)),"workflow_sha256":_sha(wf_path),
        "repo":{"git_head":None,"dirty":False},
        "machine_validation":{"status":status,"errors":errs,"warnings":[]},
        "gates":{"scope":{"status":"pending","approver":None,"timestamp":None},
                 "merge":{"status":"pending","approver":None,"timestamp":None}},
        "artifacts":[]
    })
    print(str(run_dir)); return 0 if status=="pass" else 1

def cmd_commit(args):
    run_dir=(BASE/args.run).resolve(); man_path=run_dir/"manifest.json"
    if not man_path.exists(): print("ERROR: manifest.json not found", file=sys.stderr); return 2
    m=_load(man_path)
    def ok(txt): return "Reviewer:" in txt and "Date:" in txt and "<name>" not in txt
    scope=(run_dir/"gates"/"scope_checklist.md").read_text(encoding="utf-8")
    merge=(run_dir/"gates"/"merge_checklist.md").read_text(encoding="utf-8")
    missing=[]
    if not ok(scope): missing.append("scope_checklist.md (fill Reviewer/Date)")
    if not ok(merge): missing.append("merge_checklist.md (fill Reviewer/Date)")
    if missing: [print("GATE:",x,file=sys.stderr) for x in missing]; return 1
    for k in ("scope","merge"):
        m["gates"][k].update({"status":"passed","approver":"human@local","timestamp":_ts()})
    m["finished_at"]=_ts(); _dump(man_path,m); print("RUN COMMIT OK"); return 0

def main():
    ap=argparse.ArgumentParser(prog="cri"); sp=ap.add_subparsers(dest="cmd", required=True)
    p1=sp.add_parser("validate"); p1.add_argument("workflow"); p1.set_defaults(func=cmd_validate)
    p2=sp.add_parser("run"); p2.add_argument("--workflow", required=True); p2.set_defaults(func=cmd_run)
    p3=sp.add_parser("commit"); p3.add_argument("--run", required=True); p3.set_defaults(func=cmd_commit)
    args=ap.parse_args(); sys.exit(args.func(args))

if __name__=="__main__":
    main()
