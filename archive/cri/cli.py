import importlib.util, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
ROOT_CLI = ROOT / "cli.py"
def main():
    spec = importlib.util.spec_from_file_location("cri_root_cli", ROOT_CLI)
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    if hasattr(mod, "main"):
        return mod.main()
    return 0
if __name__ == "__main__":
    sys.exit(main())
