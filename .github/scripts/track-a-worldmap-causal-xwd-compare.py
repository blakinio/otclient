#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import struct


EXPECTED = {
    "file_version": 7,
    "pixmap_format": 2,
    "pixmap_depth": 24,
    "width": 1020,
    "height": 650,
    "byte_order": 0,
    "bits_per_pixel": 32,
    "bytes_per_line": 4080,
    "red_mask": 0xFF0000,
    "green_mask": 0x00FF00,
    "blue_mask": 0x0000FF,
}


class XwdError(RuntimeError):
    pass


def load(path: Path) -> tuple[dict[str, int], bytes, int]:
    raw = path.read_bytes()
    if len(raw) < 100:
        raise XwdError("xwd_too_small")
    h = struct.unpack(">25I", raw[:100])
    fields = {
        "header_size": h[0], "file_version": h[1], "pixmap_format": h[2],
        "pixmap_depth": h[3], "width": h[4], "height": h[5],
        "byte_order": h[7], "bits_per_pixel": h[11], "bytes_per_line": h[12],
        "red_mask": h[14], "green_mask": h[15], "blue_mask": h[16],
        "ncolors": h[19],
    }
    for key, expected in EXPECTED.items():
        if fields[key] != expected:
            raise XwdError(f"shape_{key}:{fields[key]}!={expected}")
    pixel_offset = fields["header_size"] + fields["ncolors"] * 12
    expected_len = pixel_offset + fields["bytes_per_line"] * fields["height"]
    if len(raw) < expected_len:
        raise XwdError("pixel_payload_truncated")
    return fields, raw, pixel_offset


def changed_mask(
    a: Path,
    b: Path,
    roi: tuple[int, int, int, int] | None = None,
) -> set[int]:
    fa, ra, oa = load(a); fb, rb, ob = load(b)
    if fa != fb:
        raise XwdError("shape_mismatch")
    if roi is None:
        x0, y0, x1, y1 = 0, 0, fa["width"], fa["height"]
    else:
        x0, y0, x1, y1 = roi
        if not (0 <= x0 < x1 <= fa["width"] and 0 <= y0 < y1 <= fa["height"]):
            raise XwdError("roi_out_of_bounds")
    changed: set[int] = set()
    stride = fa["bytes_per_line"]
    width = fa["width"]
    for y in range(y0, y1):
        rowa = oa + y * stride
        rowb = ob + y * stride
        for x in range(x0, x1):
            aa = rowa + x * 4; bb = rowb + x * 4
            if ra[aa:aa+3] != rb[bb:bb+3]:
                changed.add(y * width + x)
    return changed


def changed_count(a: Path, b: Path, roi: tuple[int, int, int, int] | None = None) -> int:
    return len(changed_mask(a, b, roi))


def mask_bbox(mask: set[int], width: int) -> str:
    if not mask:
        return "NONE"
    xs = [idx % width for idx in mask]
    ys = [idx // width for idx in mask]
    return f"{min(xs)},{min(ys)},{max(xs)+1},{max(ys)+1}"


def bbox_metrics(mask: set[int], width: int) -> tuple[int, int, int]:
    if not mask:
        return 0, 0, 0
    xs = [idx % width for idx in mask]
    ys = [idx // width for idx in mask]
    w = max(xs) - min(xs) + 1
    h = max(ys) - min(ys) + 1
    return w, h, w * h


def roi_cycle(args: argparse.Namespace) -> int:
    roi = (args.x0, args.y0, args.x1, args.y1)
    typed_mask = changed_mask(args.before, args.typed, roi)
    cleared_mask = changed_mask(args.typed, args.cleared, roi)
    residual_mask = changed_mask(args.before, args.cleared, roi)
    typed = len(typed_mask)
    cleared = len(cleared_mask)
    residual = len(residual_mask)
    overlap = len(typed_mask & cleared_mask)
    overlap_den = min(typed, cleared)
    overlap_ratio = (overlap / overlap_den) if overlap_den else 0.0
    print(f"WORLDMAP_XWD_EDITABLE_TYPED_CHANGED={typed}")
    print(f"WORLDMAP_XWD_EDITABLE_CLEARED_CHANGED={cleared}")
    print(f"WORLDMAP_XWD_EDITABLE_RESIDUAL_CHANGED={residual}")
    print(f"WORLDMAP_XWD_EDITABLE_MASK_OVERLAP={overlap}")
    print(f"WORLDMAP_XWD_EDITABLE_MASK_OVERLAP_RATIO={overlap_ratio:.6f}")
    print(f"WORLDMAP_XWD_EDITABLE_TYPED_BBOX={mask_bbox(typed_mask, EXPECTED['width'])}")
    max_residual = max(80, int(typed * 0.55))
    if (
        typed < args.min_changed
        or cleared < args.min_changed
        or residual > max_residual
        or overlap_ratio < args.min_overlap_ratio
    ):
        print("WORLDMAP_XWD_EDITABLE_PROBE=FAIL")
        return 3
    print("WORLDMAP_XWD_EDITABLE_PROBE=PASS")
    return 0


def controlled_cycle(args: argparse.Namespace) -> int:
    """Reject animation-driven false positives using measured temporal noise.

    idle0->idle1 and idle1->idle2 measure pre-input noise. cleared->idle3
    measures post-input noise. Pixels seen in any of those controls are removed
    from both the type and clear masks. A causal editable-field signal must then
    survive in both directions and stay spatially local.
    """
    noise = (
        changed_mask(args.idle0, args.idle1)
        | changed_mask(args.idle1, args.idle2)
        | changed_mask(args.cleared, args.idle3)
    )
    typed_raw = changed_mask(args.idle2, args.typed)
    cleared_raw = changed_mask(args.typed, args.cleared)
    residual_raw = changed_mask(args.idle2, args.cleared)

    typed = typed_raw - noise
    cleared = cleared_raw - noise
    residual = residual_raw - noise
    signal = typed & cleared

    typed_n = len(typed)
    cleared_n = len(cleared)
    signal_n = len(signal)
    residual_n = len(residual)
    den = min(typed_n, cleared_n)
    overlap_ratio = (signal_n / den) if den else 0.0
    bw, bh, area = bbox_metrics(signal, EXPECTED["width"])

    print(f"WORLDMAP_XWD_CONTROLLED_NOISE_PIXELS={len(noise)}")
    print(f"WORLDMAP_XWD_CONTROLLED_TYPED_RAW_CHANGED={len(typed_raw)}")
    print(f"WORLDMAP_XWD_CONTROLLED_CLEARED_RAW_CHANGED={len(cleared_raw)}")
    print(f"WORLDMAP_XWD_CONTROLLED_CAUSAL_TYPED_CHANGED={typed_n}")
    print(f"WORLDMAP_XWD_CONTROLLED_CAUSAL_CLEARED_CHANGED={cleared_n}")
    print(f"WORLDMAP_XWD_CONTROLLED_SIGNAL_CHANGED={signal_n}")
    print(f"WORLDMAP_XWD_CONTROLLED_RESIDUAL_CHANGED={residual_n}")
    print(f"WORLDMAP_XWD_CONTROLLED_OVERLAP_RATIO={overlap_ratio:.6f}")
    print(f"WORLDMAP_XWD_CONTROLLED_SIGNAL_BBOX={mask_bbox(signal, EXPECTED['width'])}")
    print(f"WORLDMAP_XWD_CONTROLLED_SIGNAL_WIDTH={bw}")
    print(f"WORLDMAP_XWD_CONTROLLED_SIGNAL_HEIGHT={bh}")
    print(f"WORLDMAP_XWD_CONTROLLED_SIGNAL_AREA={area}")

    if (
        signal_n < args.min_signal
        or overlap_ratio < args.min_overlap_ratio
        or bw == 0
        or bh == 0
        or bw > args.max_width
        or bh > args.max_height
        or area > args.max_area
    ):
        print("WORLDMAP_XWD_CONTROLLED_EDITABLE_PROBE=FAIL")
        return 3
    print("WORLDMAP_XWD_CONTROLLED_EDITABLE_PROBE=PASS")
    return 0


def simple_change(args: argparse.Namespace) -> int:
    roi = None if args.x0 is None else (args.x0, args.y0, args.x1, args.y1)
    mask = changed_mask(args.before, args.after, roi)
    changed = len(mask)
    print(f"WORLDMAP_XWD_CHANGED_PIXELS={changed}")
    print(f"WORLDMAP_XWD_CHANGED_BBOX={mask_bbox(mask, EXPECTED['width'])}")
    if changed < args.min_changed:
        print("WORLDMAP_XWD_CHANGE=FAIL")
        return 3
    print("WORLDMAP_XWD_CHANGE=PASS")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("roi-cycle")
    c.add_argument("before", type=Path); c.add_argument("typed", type=Path); c.add_argument("cleared", type=Path)
    c.add_argument("x0", type=int); c.add_argument("y0", type=int); c.add_argument("x1", type=int); c.add_argument("y1", type=int)
    c.add_argument("--min-changed", type=int, default=60)
    c.add_argument("--min-overlap-ratio", type=float, default=0.80)

    n = sub.add_parser("controlled-cycle")
    n.add_argument("idle0", type=Path); n.add_argument("idle1", type=Path); n.add_argument("idle2", type=Path)
    n.add_argument("typed", type=Path); n.add_argument("cleared", type=Path); n.add_argument("idle3", type=Path)
    n.add_argument("--min-signal", type=int, default=25)
    n.add_argument("--min-overlap-ratio", type=float, default=0.55)
    n.add_argument("--max-width", type=int, default=500)
    n.add_argument("--max-height", type=int, default=120)
    n.add_argument("--max-area", type=int, default=30000)

    s = sub.add_parser("change")
    s.add_argument("before", type=Path); s.add_argument("after", type=Path); s.add_argument("--min-changed", type=int, required=True)
    s.add_argument("--x0", type=int); s.add_argument("--y0", type=int); s.add_argument("--x1", type=int); s.add_argument("--y1", type=int)

    args = p.parse_args()
    try:
        if args.cmd == "roi-cycle":
            if not (0.0 <= args.min_overlap_ratio <= 1.0):
                raise XwdError("overlap_ratio_out_of_bounds")
            return roi_cycle(args)
        if args.cmd == "controlled-cycle":
            if not (0.0 <= args.min_overlap_ratio <= 1.0):
                raise XwdError("overlap_ratio_out_of_bounds")
            if min(args.min_signal, args.max_width, args.max_height, args.max_area) <= 0:
                raise XwdError("controlled_limit_out_of_bounds")
            return controlled_cycle(args)
        if (args.x0 is None) != (args.y0 is None) or (args.x0 is None) != (args.x1 is None) or (args.x0 is None) != (args.y1 is None):
            raise XwdError("partial_roi")
        return simple_change(args)
    except (XwdError, OSError, struct.error) as exc:
        print(f"WORLDMAP_XWD_COMPARE_ERROR={type(exc).__name__}:{exc}")
        return 44


if __name__ == "__main__":
    raise SystemExit(main())
