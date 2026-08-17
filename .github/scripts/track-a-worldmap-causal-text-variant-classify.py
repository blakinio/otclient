#!/usr/bin/env python3
"""Classify equal-length text rendering as masked-like, unmasked-like or ambiguous.

Inputs are noise-controlled causal signal bboxes and signal counts produced by
track-a-worldmap-causal-xwd-text-semantics.py for two equal-length strings with
very different glyph widths (`iiiiii` and `WWWWWW`). This is a rendering
classification only; it never claims semantic password/account identity.
"""
from __future__ import annotations

import argparse


class VariantError(RuntimeError):
    pass


def parse_bbox(raw: str) -> tuple[int, int, int, int]:
    if raw == "NONE":
        raise VariantError("bbox_none")
    try:
        x0, y0, x1, y1 = (int(v) for v in raw.split(","))
    except Exception as exc:
        raise VariantError("bbox_invalid") from exc
    if not (0 <= x0 < x1 <= 1020 and 0 <= y0 < y1 <= 650):
        raise VariantError("bbox_out_of_bounds")
    return x0, y0, x1, y1


def classify(i_bbox: str, w_bbox: str, i_signal: int, w_signal: int) -> tuple[str, int, int, float]:
    if i_signal < 25 or w_signal < 25:
        return "AMBIGUOUS", 0, 0, 0.0
    ib = parse_bbox(i_bbox); wb = parse_bbox(w_bbox)
    iw, ih = ib[2] - ib[0], ib[3] - ib[1]
    ww, wh = wb[2] - wb[0], wb[3] - wb[1]
    if max(iw, ww) > 500 or max(ih, wh) > 120:
        return "AMBIGUOUS", iw, ww, 0.0
    ratio = max(iw, ww) / min(iw, ww)
    center_delta = abs((ib[0] + ib[2]) - (wb[0] + wb[2])) / 2.0
    # Equal-length masked text should occupy nearly the same horizontal span.
    if ratio <= 1.12 and center_delta <= 12:
        return "MASKED_LIKE", iw, ww, ratio
    # Proportional unmasked glyphs `i` and `W` should diverge strongly in width.
    if ratio >= 1.35:
        return "UNMASKED_LIKE", iw, ww, ratio
    return "AMBIGUOUS", iw, ww, ratio


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("i_bbox")
    p.add_argument("w_bbox")
    p.add_argument("i_signal", type=int)
    p.add_argument("w_signal", type=int)
    args = p.parse_args()
    try:
        cls, iw, ww, ratio = classify(args.i_bbox, args.w_bbox, args.i_signal, args.w_signal)
    except VariantError as exc:
        print(f"WORLDMAP_TEXT_VARIANT_ERROR={exc}")
        return 44
    print(f"WORLDMAP_TEXT_VARIANT_I_WIDTH={iw}")
    print(f"WORLDMAP_TEXT_VARIANT_W_WIDTH={ww}")
    print(f"WORLDMAP_TEXT_VARIANT_WIDTH_RATIO={ratio:.6f}")
    print(f"WORLDMAP_TEXT_VARIANT_CLASS={cls}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
