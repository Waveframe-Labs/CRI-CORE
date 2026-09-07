"""Compare source and distribution inventories and smoke-test a clean wheel.

Run with the same Python used to build dist; no source checkout is importable
inside the isolated smoke process. Temporary environments are removed on exit.
"""

import argparse
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import venv
import zipfile


SMOKE = '''
from pathlib import Path
import importlib
import importlib.metadata
import cricore
from cricore.api import evaluate_structured
api = importlib.import_module("cricore.api")
module = importlib.import_module("cricore.api.evaluate")
assert Path(api.__file__).parts[-2:] == ("api", "__init__.py")
assert api.evaluate_structured is module.evaluate_structured is cricore.evaluate_structured
assert api.evaluate is cricore.evaluate
assert not (Path(cricore.__file__).parent / "api.py").exists()
assert "site-packages" in Path(api.__file__).parts
proposal = {"proposal_id": "wheel-smoke", "contract": {"id": "t", "version": "1", "hash": "h"}}
contract = {"contract_id": "t", "contract_version": "1", "contract_hash": "h"}
context = {"identities": {"actors": [{"id": "u", "type": "human", "role": "manager"}],
                          "required_roles": ["manager"]}}
data = dict(proposal=proposal, compiled_contract=contract, run_context=context)
default = evaluate_structured(**data)
assert not default.commit_allowed
assert {"integrity", "publication"} <= set(default.failed_stages)
assert not evaluate_structured(**data, mode="strict").commit_allowed
assert evaluate_structured(**data, mode="local").commit_allowed
for invalid in (None, "", "STRICT", "local ", False, 0, [], {}):
    try:
        evaluate_structured(**data, mode=invalid)
    except ValueError as exc:
        assert str(exc).startswith("CRI_MODE_INVALID:")
    else:
        raise AssertionError("invalid mode accepted")
context["mode"] = "local"
try:
    evaluate_structured(**data)
except ValueError as exc:
    assert str(exc).startswith("CRI_MODE_CONFLICT:")
else:
    raise AssertionError("context silently downgraded strict enforcement")
assert evaluate_structured(**data, mode="local").commit_allowed
print("Clean wheel strict/default/local and canonical import passed:", api.__file__)
print("Installed version:", importlib.metadata.version("cricore"))
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist-dir", type=Path, default=Path("dist"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    wheels = list(args.dist_dir.glob("*.whl"))
    sdists = list(args.dist_dir.glob("*.tar.gz"))
    assert len(wheels) == len(sdists) == 1, "expected one fresh wheel and sdist"
    expected = {p.relative_to(root / "src").as_posix()
                for p in (root / "src" / "cricore").rglob("*")
                if p.suffix in (".py", ".json")}
    with zipfile.ZipFile(wheels[0]) as wheel:
        names = set(wheel.namelist())
        actual = {n for n in names if n.startswith("cricore/")}
        assert actual == expected, (actual - expected, expected - actual)
        assert "cricore/api.py" not in names
        assert not any(n.endswith((".pyc", ".pyo")) for n in names)
    with tarfile.open(sdists[0]) as sdist:
        names = {n.split("/", 1)[-1] for n in sdist.getnames()}
        actual = {n.removeprefix("src/") for n in names
                  if n.startswith("src/cricore/") and n.endswith((".py", ".json"))}
        assert actual == expected, (actual - expected, expected - actual)
        assert "src/cricore/api.py" not in names
    print(f"Source/wheel/sdist inventories match: {len(expected)} Python/schema files")
    with tempfile.TemporaryDirectory(prefix="cricore-wheel-") as scratch:
        env_dir = Path(scratch) / "venv"
        venv.EnvBuilder(with_pip=True).create(env_dir)
        python = env_dir / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        for command in (
            [str(python), "-m", "pip", "install", "--no-deps", str(wheels[0].resolve())],
            [str(python), "-m", "pip", "check"],
            [str(python), "-I", "-c", SMOKE],
        ):
            subprocess.run(command, cwd=scratch, check=True)


if __name__ == "__main__":
    main()
