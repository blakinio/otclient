#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys


def load_compare(path: Path):
    spec = importlib.util.spec_from_file_location("worldmap_xwd_compare_semantics", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("compare_import_spec_failed")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("compare", type=Path)
    for name in ("idle0", "idle1", "idle2", "short", "clear_short", "long", "clear_long", "idle3"):
        p.add_argument(name, type=Path)
    p.add_argument("--min-short", type=int, default=25)
    p.add_argument("--min-long", type=int, default=40)
    p.add_argument("--min-overlap", type=float, default=0.55)
    p.add_argument("--min-growth-pixels", type=int, default=20)
    p.add_argument("--min-growth-ratio", type=float, default=1.30)
    p.add_argument("--min-growth-width", type=int, default=8)
    p.add_argument("--max-width", type=int, default=500)
    p.add_argument("--max-height", type=int, default=120)
    p.add_argument("--max-area", type=int, default=30000)
    args = p.parse_args()

    m = load_compare(args.compare)
    noise = (
        m.changed_mask(args.idle0, args.idle1)
        | m.changed_mask(args.idle1, args.idle2)
        | m.changed_mask(args.clear_long, args.idle3)
    )
    short_type = m.changed_mask(args.idle2, args.short) - noise
    short_clear = m.changed_mask(args.short, args.clear_short) - noise
    long_type = m.changed_mask(args.clear_short, args.long) - noise
    long_clear = m.changed_mask(args.long, args.clear_long) - noise
    short_signal = short_type & short_clear
    long_signal = long_type & long_clear
    short_den = min(len(short_type), len(short_clear))
    long_den = min(len(long_type), len(long_clear))
    short_overlap = len(short_signal) / short_den if short_den else 0.0
    long_overlap = len(long_signal) / long_den if long_den else 0.0
    sw, sh, sa = m.bbox_metrics(short_signal, m.EXPECTED["width"])
    lw, lh, la = m.bbox_metrics(long_signal, m.EXPECTED["width"])
    short_n = len(short_signal)
    long_n = len(long_signal)
    growth_pixels = max(0, long_n - short_n)
    growth_ratio = (long_n / short_n) if short_n else 0.0
    growth_width = max(0, lw - sw)
    residual_short = len(m.changed_mask(args.idle2, args.clear_short) - noise)
    residual_long = len(m.changed_mask(args.clear_short, args.clear_long) - noise)

    print(f"WORLDMAP_TEXT_SEMANTICS_NOISE_PIXELS={len(noise)}")
    print(f"WORLDMAP_TEXT_SEMANTICS_SHORT_SIGNAL={short_n}")
    print(f"WORLDMAP_TEXT_SEMANTICS_LONG_SIGNAL={long_n}")
    print(f"WORLDMAP_TEXT_SEMANTICS_SHORT_OVERLAP={short_overlap:.6f}")
    print(f"WORLDMAP_TEXT_SEMANTICS_LONG_OVERLAP={long_overlap:.6f}")
    print(f"WORLDMAP_TEXT_SEMANTICS_SHORT_BBOX={m.mask_bbox(short_signal, m.EXPECTED['width'])}")
    print(f"WORLDMAP_TEXT_SEMANTICS_LONG_BBOX={m.mask_bbox(long_signal, m.EXPECTED['width'])}")
    print(f"WORLDMAP_TEXT_SEMANTICS_GROWTH_PIXELS={growth_pixels}")
    print(f"WORLDMAP_TEXT_SEMANTICS_GROWTH_RATIO={growth_ratio:.6f}")
    print(f"WORLDMAP_TEXT_SEMANTICS_GROWTH_WIDTH={growth_width}")
    print(f"WORLDMAP_TEXT_SEMANTICS_RESIDUAL_SHORT={residual_short}")
    print(f"WORLDMAP_TEXT_SEMANTICS_RESIDUAL_LONG={residual_long}")

    local = (
        sw > 0 and sh > 0 and lw > 0 and lh > 0
        and sw <= args.max_width and sh <= args.max_height and sa <= args.max_area
        and lw <= args.max_width and lh <= args.max_height and la <= args.max_area
    )
    growth = (
        growth_pixels >= args.min_growth_pixels
        and (growth_ratio >= args.min_growth_ratio or growth_width >= args.min_growth_width)
    )
    passed = (
        short_n >= args.min_short
        and long_n >= args.min_long
        and short_overlap >= args.min_overlap
        and long_overlap >= args.min_overlap
        and local
        and growth
    )
    print("WORLDMAP_TEXT_SEMANTICS_FIELD=" + ("PASS" if passed else "FAIL"))
    return 0 if passed else 3


if __name__ == "__main__":
    raise SystemExit(main())
