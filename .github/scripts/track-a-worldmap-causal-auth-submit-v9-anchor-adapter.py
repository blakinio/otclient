#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


class AdapterError(RuntimeError):
    pass


def load_v9(path: Path):
    spec = importlib.util.spec_from_file_location("worldmap_v9_impl", path)
    if spec is None or spec.loader is None:
        raise AdapterError("v9_import_spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("v9_impl", type=Path)
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    args = p.parse_args()
    try:
        v9 = load_v9(args.v9_impl)
        text = args.source.read_text(encoding="utf-8")
        count = text.count(v9.WORLD_FALLBACK)
        if count > 1:
            raise AdapterError(f"LEGACY_FALLBACK_COUNT:{count}")
        if count == 0:
            anchor = '[[ "$world" == 1 ]] || fail structural_world_entry_not_observed\n'
            if text.count(anchor) != 1:
                raise AdapterError(f"WORLD_ASSERT_COUNT:{text.count(anchor)}")
            text = text.replace(anchor, v9.WORLD_FALLBACK + anchor, 1)
            print("WORLDMAP_V9_ANCHOR_ADAPTER=INSERT_THEN_REMOVE")
        else:
            print("WORLDMAP_V9_ANCHOR_ADAPTER=LEGACY_PRESENT")
        result = v9.transform(text)
        if "SELECT_X=" in result or "SELECT_Y=" in result:
            raise AdapterError("LEGACY_COORDINATE_SURVIVED")
        if "PASSWORD_TAB_RETURN" in result:
            raise AdapterError("OLD_LOGIN_SUBMIT_SURVIVED")
        if v9.WORLD_FALLBACK in result:
            raise AdapterError("SYNTHETIC_FALLBACK_SURVIVED")
    except (AdapterError, Exception) as exc:
        # Keep the error type but never print source text or environment values.
        print(f"WORLDMAP_V9_ANCHOR_ADAPTER_REFUSED={type(exc).__name__}:{exc}")
        return 44
    args.output.write_text(result, encoding="utf-8")
    args.output.chmod(0o700)
    print("WORLDMAP_V9_ANCHOR_ADAPTER=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
