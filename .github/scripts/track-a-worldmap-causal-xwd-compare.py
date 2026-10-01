#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import struct


STATIC_EXPECTED = {
    "file_version": 7,
    "pixmap_format": 2,
    "pixmap_depth": 24,
    "byte_order": 0,
    "bits_per_pixel": 32,
    "red_mask": 0xFF0000,
    "green_mask": 0x00FF00,
    "blue_mask": 0x0000FF,
}
MAX_DIMENSION = 8192
MAX_COLORS = 65536


class XwdError(RuntimeError):
    pass


def load(path: Path) -> tuple[dict[str, int], bytes, int]:
    raw = path.read_bytes()
    if len(raw) < 100:
        raise XwdError("xwd_too_small")
    h = struct.unpack(">25I", raw[:100])
    fields = {
        "header_size": h[0],
        "file_version": h[1],
        "pixmap_format": h[2],
        "pixmap_depth": h[3],
        "width": h[4],
        "height": h[5],
        "xoffset": h[6],
        "byte_order": h[7],
        "bitmap_unit": h[8],
        "bitmap_bit_order": h[9],
        "bitmap_pad": h[10],
        "bits_per_pixel": h[11],
        "bytes_per_line": h[12],
        "visual_class": h[13],
        "red_mask": h[14],
        "green_mask": h[15],
        "blue_mask": h[16],
        "bits_per_rgb": h[17],
        "colormap_entries": h[18],
        "ncolors": h[19],
        "window_width": h[20],
        "window_height": h[21],
        "window_x": h[22],
        "window_y": h[23],
        "window_bdrwidth": h[24],
    }
    for key, expected in STATIC_EXPECTED.items():
        if fields[key] != expected:
            raise XwdError(f"shape_{key}:{fields[key]}!={expected}")
    if fields["header_size"] < 100 or fields["header_size"] > len(raw):
        raise XwdError("header_size_out_of_bounds")
    if not (1 <= fields["width"] <= MAX_DIMENSION and 1 <= fields["height"] <= MAX_DIMENSION):
        raise XwdError("pixmap_geometry_out_of_bounds")
    if not (1 <= fields["window_width"] <= MAX_DIMENSION and 1 <= fields["window_height"] <= MAX_DIMENSION):
        raise XwdError("window_geometry_out_of_bounds")
    if fields["ncolors"] > MAX_COLORS:
        raise XwdError("color_table_too_large")
    minimum_stride = fields["width"] * 4
    if fields["bytes_per_line"] < minimum_stride or fields["bytes_per_line"] % 4:
        raise XwdError("bytes_per_line_invalid")
    if fields["bytes_per_line"] > minimum_stride + 4096:
        raise XwdError("bytes_per_line_excessive_padding")
    pixel_offset = fields["header_size"] + fields["ncolors"] * 12
    if pixel_offset > len(raw):
        raise XwdError("pixel_offset_out_of_bounds")
    expected_len = pixel_offset + fields["bytes_per_line"] * fields["height"]
    if len(raw) < expected_len:
        raise XwdError("pixel_payload_truncated")
    return fields, raw, pixel_offset


def _shape(path: Path) -> dict[str, int]:
    fields, _raw, _offset = load(path)
    return fields


def changed_mask(
    a: Path,
    b: Path,
    roi: tuple[int, int, int, int] | None = None,
) -> set[int]:
    fa, ra, oa = load(a)
    fb, rb, ob = load(b)
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
            aa = rowa + x * 4
            bb = rowb + x * 4
            if ra[aa : aa + 3] != rb[bb : bb + 3]:
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


def parse_bbox(raw: str, width: int, height: int) -> tuple[int, int, int, int]:
    if raw == "NONE":
        raise XwdError("bbox_none")
    try:
        x0, y0, x1, y1 = (int(v) for v in raw.split(","))
    except Exception as exc:
        raise XwdError("bbox_invalid") from exc
    if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height):
        raise XwdError("bbox_out_of_bounds")
    return x0, y0, x1, y1


def inspect_xwd(args: argparse.Namespace) -> int:
    fields = _shape(args.xwd)
    print(f"WORLDMAP_XWD_PIXMAP_GEOMETRY={fields['width']}x{fields['height']}")
    print(f"WORLDMAP_XWD_WINDOW_GEOMETRY={fields['window_width']}x{fields['window_height']}")
    print(f"WORLDMAP_XWD_WINDOW_POSITION={fields['window_x']},{fields['window_y']}")
    print(f"WORLDMAP_XWD_WINDOW_BORDER_WIDTH={fields['window_bdrwidth']}")
    print(f"WORLDMAP_XWD_BYTES_PER_LINE={fields['bytes_per_line']}")
    if args.expected_width is not None:
        if fields["width"] != args.expected_width or fields["height"] != args.expected_height:
            raise XwdError(
                f"pixmap_geometry:{fields['width']}x{fields['height']}!="
                f"{args.expected_width}x{args.expected_height}"
            )
        if fields["window_width"] != args.expected_width or fields["window_height"] != args.expected_height:
            raise XwdError(
                f"window_geometry:{fields['window_width']}x{fields['window_height']}!="
                f"{args.expected_width}x{args.expected_height}"
            )
        print("WORLDMAP_XWD_GEOMETRY_MATCH=PASS")
    return 0


def roi_cycle(args: argparse.Namespace) -> int:
    fields = _shape(args.before)
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
    print(f"WORLDMAP_XWD_EDITABLE_TYPED_BBOX={mask_bbox(typed_mask, fields['width'])}")
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
    fields = _shape(args.idle0)
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
    bw, bh, area = bbox_metrics(signal, fields["width"])

    print(f"WORLDMAP_XWD_CONTROLLED_NOISE_PIXELS={len(noise)}")
    print(f"WORLDMAP_XWD_CONTROLLED_TYPED_RAW_CHANGED={len(typed_raw)}")
    print(f"WORLDMAP_XWD_CONTROLLED_CLEARED_RAW_CHANGED={len(cleared_raw)}")
    print(f"WORLDMAP_XWD_CONTROLLED_CAUSAL_TYPED_CHANGED={typed_n}")
    print(f"WORLDMAP_XWD_CONTROLLED_CAUSAL_CLEARED_CHANGED={cleared_n}")
    print(f"WORLDMAP_XWD_CONTROLLED_SIGNAL_CHANGED={signal_n}")
    print(f"WORLDMAP_XWD_CONTROLLED_RESIDUAL_CHANGED={residual_n}")
    print(f"WORLDMAP_XWD_CONTROLLED_OVERLAP_RATIO={overlap_ratio:.6f}")
    print(f"WORLDMAP_XWD_CONTROLLED_SIGNAL_BBOX={mask_bbox(signal, fields['width'])}")
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


def text_semantics(args: argparse.Namespace) -> int:
    fields = _shape(args.idle0)
    noise = (
        changed_mask(args.idle0, args.idle1)
        | changed_mask(args.idle1, args.idle2)
        | changed_mask(args.clear_long, args.idle3)
    )
    short_type = changed_mask(args.idle2, args.short) - noise
    short_clear = changed_mask(args.short, args.clear_short) - noise
    long_type = changed_mask(args.clear_short, args.long) - noise
    long_clear = changed_mask(args.long, args.clear_long) - noise
    short_signal = short_type & short_clear
    long_signal = long_type & long_clear
    short_den = min(len(short_type), len(short_clear))
    long_den = min(len(long_type), len(long_clear))
    short_overlap = len(short_signal) / short_den if short_den else 0.0
    long_overlap = len(long_signal) / long_den if long_den else 0.0
    sw, sh, sa = bbox_metrics(short_signal, fields["width"])
    lw, lh, la = bbox_metrics(long_signal, fields["width"])
    short_n = len(short_signal)
    long_n = len(long_signal)
    growth_pixels = max(0, long_n - short_n)
    growth_ratio = (long_n / short_n) if short_n else 0.0
    growth_width = max(0, lw - sw)
    residual_short = len(changed_mask(args.idle2, args.clear_short) - noise)
    residual_long = len(changed_mask(args.clear_short, args.clear_long) - noise)

    print(f"WORLDMAP_TEXT_SEMANTICS_NOISE_PIXELS={len(noise)}")
    print(f"WORLDMAP_TEXT_SEMANTICS_SHORT_SIGNAL={short_n}")
    print(f"WORLDMAP_TEXT_SEMANTICS_LONG_SIGNAL={long_n}")
    print(f"WORLDMAP_TEXT_SEMANTICS_SHORT_OVERLAP={short_overlap:.6f}")
    print(f"WORLDMAP_TEXT_SEMANTICS_LONG_OVERLAP={long_overlap:.6f}")
    print(f"WORLDMAP_TEXT_SEMANTICS_SHORT_BBOX={mask_bbox(short_signal, fields['width'])}")
    print(f"WORLDMAP_TEXT_SEMANTICS_LONG_BBOX={mask_bbox(long_signal, fields['width'])}")
    print(f"WORLDMAP_TEXT_SEMANTICS_GROWTH_PIXELS={growth_pixels}")
    print(f"WORLDMAP_TEXT_SEMANTICS_GROWTH_RATIO={growth_ratio:.6f}")
    print(f"WORLDMAP_TEXT_SEMANTICS_GROWTH_WIDTH={growth_width}")
    print(f"WORLDMAP_TEXT_SEMANTICS_RESIDUAL_SHORT={residual_short}")
    print(f"WORLDMAP_TEXT_SEMANTICS_RESIDUAL_LONG={residual_long}")

    local = (
        sw > 0
        and sh > 0
        and lw > 0
        and lh > 0
        and sw <= args.max_width
        and sh <= args.max_height
        and sa <= args.max_area
        and lw <= args.max_width
        and lh <= args.max_height
        and la <= args.max_area
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
        and residual_short <= args.max_residual
        and residual_long <= args.max_residual
        and local
        and growth
    )
    print("WORLDMAP_TEXT_SEMANTICS_FIELD=" + ("PASS" if passed else "FAIL"))
    return 0 if passed else 3


def variant_classify(args: argparse.Namespace) -> int:
    if args.i_signal < 25 or args.w_signal < 25:
        cls = "AMBIGUOUS"
        iw = ww = 0
        ratio = 0.0
    else:
        ib = parse_bbox(args.i_bbox, args.width, args.height)
        wb = parse_bbox(args.w_bbox, args.width, args.height)
        iw, ih = ib[2] - ib[0], ib[3] - ib[1]
        ww, wh = wb[2] - wb[0], wb[3] - wb[1]
        if max(iw, ww) > args.max_width or max(ih, wh) > args.max_height:
            cls = "AMBIGUOUS"
            ratio = 0.0
        else:
            ratio = max(iw, ww) / min(iw, ww)
            center_delta = abs((ib[0] + ib[2]) - (wb[0] + wb[2])) / 2.0
            if ratio <= 1.12 and center_delta <= 12:
                cls = "MASKED_LIKE"
            elif ratio >= 1.35:
                cls = "UNMASKED_LIKE"
            else:
                cls = "AMBIGUOUS"
    print(f"WORLDMAP_TEXT_VARIANT_I_WIDTH={iw}")
    print(f"WORLDMAP_TEXT_VARIANT_W_WIDTH={ww}")
    print(f"WORLDMAP_TEXT_VARIANT_WIDTH_RATIO={ratio:.6f}")
    print(f"WORLDMAP_TEXT_VARIANT_CLASS={cls}")
    return 0


def simple_change(args: argparse.Namespace) -> int:
    fields = _shape(args.before)
    roi = None if args.x0 is None else (args.x0, args.y0, args.x1, args.y1)
    mask = changed_mask(args.before, args.after, roi)
    changed = len(mask)
    print(f"WORLDMAP_XWD_CHANGED_PIXELS={changed}")
    print(f"WORLDMAP_XWD_CHANGED_BBOX={mask_bbox(mask, fields['width'])}")
    if changed < args.min_changed:
        print("WORLDMAP_XWD_CHANGE=FAIL")
        return 3
    print("WORLDMAP_XWD_CHANGE=PASS")
    return 0


def add_text_semantics_args(t: argparse.ArgumentParser) -> None:
    for name in ("idle0", "idle1", "idle2", "short", "clear_short", "long", "clear_long", "idle3"):
        t.add_argument(name, type=Path)
    t.add_argument("--min-short", type=int, default=25)
    t.add_argument("--min-long", type=int, default=40)
    t.add_argument("--min-overlap", type=float, default=0.55)
    t.add_argument("--min-growth-pixels", type=int, default=20)
    t.add_argument("--min-growth-ratio", type=float, default=1.30)
    t.add_argument("--min-growth-width", type=int, default=8)
    t.add_argument("--max-width", type=int, default=500)
    t.add_argument("--max-height", type=int, default=120)
    t.add_argument("--max-area", type=int, default=30000)
    t.add_argument("--max-residual", type=int, default=1000)


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    i = sub.add_parser("inspect")
    i.add_argument("xwd", type=Path)
    i.add_argument("--expected-width", type=int)
    i.add_argument("--expected-height", type=int)

    c = sub.add_parser("roi-cycle")
    c.add_argument("before", type=Path)
    c.add_argument("typed", type=Path)
    c.add_argument("cleared", type=Path)
    c.add_argument("x0", type=int)
    c.add_argument("y0", type=int)
    c.add_argument("x1", type=int)
    c.add_argument("y1", type=int)
    c.add_argument("--min-changed", type=int, default=60)
    c.add_argument("--min-overlap-ratio", type=float, default=0.80)

    n = sub.add_parser("controlled-cycle")
    n.add_argument("idle0", type=Path)
    n.add_argument("idle1", type=Path)
    n.add_argument("idle2", type=Path)
    n.add_argument("typed", type=Path)
    n.add_argument("cleared", type=Path)
    n.add_argument("idle3", type=Path)
    n.add_argument("--min-signal", type=int, default=25)
    n.add_argument("--min-overlap-ratio", type=float, default=0.55)
    n.add_argument("--max-width", type=int, default=500)
    n.add_argument("--max-height", type=int, default=120)
    n.add_argument("--max-area", type=int, default=30000)

    t = sub.add_parser("text-semantics")
    add_text_semantics_args(t)

    v = sub.add_parser("variant")
    v.add_argument("i_bbox")
    v.add_argument("w_bbox")
    v.add_argument("i_signal", type=int)
    v.add_argument("w_signal", type=int)
    v.add_argument("--width", type=int, required=True)
    v.add_argument("--height", type=int, required=True)
    v.add_argument("--max-width", type=int, default=500)
    v.add_argument("--max-height", type=int, default=120)

    s = sub.add_parser("change")
    s.add_argument("before", type=Path)
    s.add_argument("after", type=Path)
    s.add_argument("--min-changed", type=int, required=True)
    s.add_argument("--x0", type=int)
    s.add_argument("--y0", type=int)
    s.add_argument("--x1", type=int)
    s.add_argument("--y1", type=int)

    args = p.parse_args()
    try:
        if args.cmd == "inspect":
            if (args.expected_width is None) != (args.expected_height is None):
                raise XwdError("partial_expected_geometry")
            if args.expected_width is not None and min(args.expected_width, args.expected_height) <= 0:
                raise XwdError("expected_geometry_out_of_bounds")
            return inspect_xwd(args)
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
        if args.cmd == "text-semantics":
            if not (0.0 <= args.min_overlap <= 1.0):
                raise XwdError("text_overlap_out_of_bounds")
            if min(
                args.min_short,
                args.min_long,
                args.min_growth_pixels,
                args.min_growth_width,
                args.max_width,
                args.max_height,
                args.max_area,
                args.max_residual,
            ) <= 0:
                raise XwdError("text_limit_out_of_bounds")
            return text_semantics(args)
        if args.cmd == "variant":
            if min(args.width, args.height, args.max_width, args.max_height) <= 0:
                raise XwdError("variant_limit_out_of_bounds")
            return variant_classify(args)
        if (args.x0 is None) != (args.y0 is None) or (args.x0 is None) != (args.x1 is None) or (args.x0 is None) != (args.y1 is None):
            raise XwdError("partial_roi")
        return simple_change(args)
    except (XwdError, OSError, struct.error) as exc:
        print(f"WORLDMAP_XWD_COMPARE_ERROR={type(exc).__name__}:{exc}")
        return 44


if __name__ == "__main__":
    raise SystemExit(main())
