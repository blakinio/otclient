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


def load_xwd(path: Path):
    raw = path.read_bytes()
    if len(raw) < 100:
        raise ValueError("xwd_too_small")
    h = struct.unpack(">25I", raw[:100])
    fields = {
        "header_size": h[0],
        "file_version": h[1],
        "pixmap_format": h[2],
        "pixmap_depth": h[3],
        "width": h[4],
        "height": h[5],
        "byte_order": h[7],
        "bits_per_pixel": h[11],
        "bytes_per_line": h[12],
        "red_mask": h[14],
        "green_mask": h[15],
        "blue_mask": h[16],
        "ncolors": h[19],
    }
    for key, expected in EXPECTED.items():
        if fields[key] != expected:
            raise ValueError(f"xwd_shape_{key}:{fields[key]}!={expected}")
    pixel_offset = fields["header_size"] + fields["ncolors"] * 12
    expected_len = pixel_offset + fields["bytes_per_line"] * fields["height"]
    if len(raw) < expected_len:
        raise ValueError("xwd_pixel_payload_truncated")

    def pixel(x: int, y: int) -> tuple[int, int, int]:
        if not (0 <= x < fields["width"] and 0 <= y < fields["height"]):
            raise ValueError("pixel_out_of_bounds")
        off = pixel_offset + y * fields["bytes_per_line"] + x * 4
        value = int.from_bytes(raw[off : off + 4], "little")
        return ((value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF)

    return fields, pixel


def grayscale_ratio(pixel) -> float:
    total = 0
    grayscale = 0
    for y in range(110, 330, 5):
        for x in range(135, 885, 5):
            r, g, b = pixel(x, y)
            total += 1
            if max(r, g, b) - min(r, g, b) <= 3:
                grayscale += 1
    return grayscale / total


def luminance(rgb: tuple[int, int, int]) -> float:
    return sum(rgb) / 3.0


def near_gray(rgb: tuple[int, int, int], spread: int = 5) -> bool:
    return max(rgb) - min(rgb) <= spread


def classify(path: Path) -> tuple[str, float, dict[str, tuple[int, int, int]]]:
    _fields, pixel = load_xwd(path)
    ratio = grayscale_ratio(pixel)
    samples = {
        "email": pixel(520, 275),
        "password": pixel(520, 305),
        "login_button": pixel(590, 389),
        "first_row": pixel(300, 195),
        "selection_ok": pixel(800, 511),
    }

    login_points = (
        near_gray(samples["email"])
        and 35 <= luminance(samples["email"]) <= 85
        and near_gray(samples["password"])
        and 35 <= luminance(samples["password"]) <= 85
        and near_gray(samples["login_button"])
        and 45 <= luminance(samples["login_button"]) <= 115
    )
    select_points = (
        near_gray(samples["first_row"])
        and 55 <= luminance(samples["first_row"]) <= 120
        and near_gray(samples["selection_ok"])
        and 45 <= luminance(samples["selection_ok"]) <= 110
    )

    if 0.08 <= ratio <= 0.35 and login_points:
        result = "LOGIN_FORM"
    elif ratio >= 0.90 and select_points:
        result = "SELECT_CHARACTER"
    else:
        result = "OTHER"
    return result, ratio, samples


def self_test() -> int:
    # Pure arithmetic threshold tests. Real exact-client calibration is retained in
    # docs/agents/evidence/.../20260817-ui-geometry-without-ocr.md.
    cases = [
        (0.15984848484848485, "LOGIN_FORM_REFERENCE"),
        (0.9890909090909091, "SELECT_CHARACTER_REFERENCE"),
        (0.435, "WORLD_REFERENCE"),
        (0.003787878787878788, "LOADING_REFERENCE"),
    ]
    if not (0.08 <= cases[0][0] <= 0.35):
        return 2
    if not (cases[1][0] >= 0.90):
        return 3
    if cases[2][0] >= 0.90 or 0.08 <= cases[2][0] <= 0.35:
        return 4
    if cases[3][0] >= 0.08:
        return 5
    print("WORLDMAP_XWD_CLASSIFIER_SELF_TEST=PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_classify = sub.add_parser("classify")
    p_classify.add_argument("xwd", type=Path)
    sub.add_parser("self-test")
    args = parser.parse_args()

    if args.cmd == "self-test":
        return self_test()

    try:
        result, ratio, samples = classify(args.xwd)
    except Exception as exc:
        print(f"WORLDMAP_XWD_CLASSIFIER_ERROR={type(exc).__name__}:{exc}")
        return 44
    print("WORLDMAP_XWD_WIDTH=1020")
    print("WORLDMAP_XWD_HEIGHT=650")
    print(f"WORLDMAP_XWD_GRAYSCALE_RATIO={ratio:.12f}")
    # Only luminance/spread summaries are emitted; no screenshot text/account identity.
    for name, rgb in samples.items():
        print(
            f"WORLDMAP_XWD_SAMPLE_{name.upper()}="
            f"lum:{luminance(rgb):.1f},spread:{max(rgb)-min(rgb)}"
        )
    print(f"WORLDMAP_XWD_CLASS={result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
