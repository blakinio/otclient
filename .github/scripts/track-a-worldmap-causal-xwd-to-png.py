#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import struct
import zlib

EXPECTED = {
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


class ExportError(RuntimeError):
    pass


def load_xwd(path: Path) -> tuple[dict[str, int], bytes, int]:
    raw = path.read_bytes()
    if len(raw) < 100:
        raise ExportError("xwd_too_small")
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
        "window_width": h[20],
        "window_height": h[21],
        "window_x": h[22],
        "window_y": h[23],
        "window_bdrwidth": h[24],
    }
    for key, expected in EXPECTED.items():
        if fields[key] != expected:
            raise ExportError(f"{key}:{fields[key]}!={expected}")
    if not (1 <= fields["width"] <= MAX_DIMENSION and 1 <= fields["height"] <= MAX_DIMENSION):
        raise ExportError("geometry_out_of_bounds")
    if fields["window_width"] != fields["width"] or fields["window_height"] != fields["height"]:
        raise ExportError("window_pixmap_geometry_mismatch")
    if fields["bytes_per_line"] < fields["width"] * 4:
        raise ExportError("stride_too_small")
    pixel_offset = fields["header_size"] + fields["ncolors"] * 12
    needed = pixel_offset + fields["bytes_per_line"] * fields["height"]
    if pixel_offset < 100 or needed > len(raw):
        raise ExportError("pixel_payload_invalid")
    return fields, raw, pixel_offset


def chunk(kind: bytes, payload: bytes) -> bytes:
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)


def write_png(path: Path, width: int, height: int, rgb_rows: list[bytes]) -> None:
    if len(rgb_rows) != height or any(len(row) != width * 3 for row in rgb_rows):
        raise ExportError("rgb_shape_invalid")
    scanlines = b"".join(b"\x00" + row for row in rgb_rows)
    png = bytearray(b"\x89PNG\r\n\x1a\n")
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(scanlines, level=9))
    png += chunk(b"IEND", b"")
    path.write_bytes(bytes(png))


def export(xwd: Path, out: Path, crop: tuple[int, int, int, int] | None) -> None:
    fields, raw, offset = load_xwd(xwd)
    width = fields["width"]
    height = fields["height"]
    if crop is None:
        x0, y0, x1, y1 = 0, 0, width, height
    else:
        x0, y0, x1, y1 = crop
        if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height):
            raise ExportError("crop_out_of_bounds")
    stride = fields["bytes_per_line"]
    rows: list[bytes] = []
    for y in range(y0, y1):
        src = offset + y * stride + x0 * 4
        row = bytearray()
        for _x in range(x0, x1):
            b, g, r, _pad = raw[src : src + 4]
            row.extend((r, g, b))
            src += 4
        rows.append(bytes(row))
    write_png(out, x1 - x0, y1 - y0, rows)
    print(f"WORLDMAP_SCREENSHOT_SOURCE_GEOMETRY={width}x{height}")
    print(f"WORLDMAP_SCREENSHOT_CROP={x0},{y0},{x1},{y1}")
    print(f"WORLDMAP_SCREENSHOT_PNG_GEOMETRY={x1-x0}x{y1-y0}")
    print("WORLDMAP_SCREENSHOT_EXPORT=PASS")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("xwd", type=Path)
    p.add_argument("out", type=Path)
    p.add_argument("--crop", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"))
    args = p.parse_args()
    try:
        export(args.xwd, args.out, tuple(args.crop) if args.crop else None)
    except ExportError as exc:
        print(f"WORLDMAP_SCREENSHOT_EXPORT_ERROR={exc}")
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
