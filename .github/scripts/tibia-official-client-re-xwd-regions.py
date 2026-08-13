#!/usr/bin/env python3
"""Report non-secret changed-pixel geometry between same-sized XWD captures."""

from __future__ import annotations

import pathlib
import struct
import sys


def _header(blob: bytes) -> tuple[tuple[int, ...], int]:
    if len(blob) < 100:
        raise ValueError("truncated XWD header")
    for endian in (">", "<"):
        fields = struct.unpack(f"{endian}25I", blob[:100])
        header_size, version, image_format, _, width, height, *_ = fields
        if 100 <= header_size <= len(blob) and version == 7 and image_format <= 2 and width and height:
            return fields, header_size
    raise ValueError("unsupported XWD header")


def _pixels(blob: bytes) -> tuple[int, int, int, int, bytes]:
    fields, header_size = _header(blob)
    width = fields[4]
    height = fields[5]
    bits_per_pixel = fields[11]
    bytes_per_line = fields[12]
    ncolors = fields[19]
    pixel_bytes = (bits_per_pixel + 7) // 8
    offset = header_size + ncolors * 12
    expected = offset + height * bytes_per_line
    if not pixel_bytes or bytes_per_line < width * pixel_bytes or expected > len(blob):
        raise ValueError("truncated or unsupported XWD pixel data")
    return width, height, pixel_bytes, bytes_per_line, blob[offset:expected]


def changed_region(before: bytes, after: bytes) -> dict[str, int]:
    width, height, pixel_bytes, stride, a = _pixels(before)
    width2, height2, pixel_bytes2, stride2, b = _pixels(after)
    if (width, height, pixel_bytes, stride) != (width2, height2, pixel_bytes2, stride2):
        raise ValueError("XWD captures differ in geometry or pixel format")

    min_x = width
    min_y = height
    max_x = -1
    max_y = -1
    count = 0
    row_counts = [0] * height
    col_counts = [0] * width

    row_bytes = width * pixel_bytes
    for y in range(height):
        row = y * stride
        for byte_x in range(0, row_bytes, pixel_bytes):
            if a[row + byte_x : row + byte_x + pixel_bytes] == b[row + byte_x : row + byte_x + pixel_bytes]:
                continue
            x = byte_x // pixel_bytes
            count += 1
            row_counts[y] += 1
            col_counts[x] += 1
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

    if count == 0:
        min_x = min_y = max_x = max_y = -1
        peak_row = peak_col = -1
        peak_row_count = peak_col_count = 0
    else:
        peak_row = max(range(height), key=row_counts.__getitem__)
        peak_col = max(range(width), key=col_counts.__getitem__)
        peak_row_count = row_counts[peak_row]
        peak_col_count = col_counts[peak_col]

    return {
        "count": count,
        "min_x": min_x,
        "min_y": min_y,
        "max_x": max_x,
        "max_y": max_y,
        "peak_row": peak_row,
        "peak_row_count": peak_row_count,
        "peak_col": peak_col,
        "peak_col_count": peak_col_count,
    }


def main() -> int:
    if len(sys.argv) != 4:
        raise SystemExit(f"usage: {pathlib.Path(sys.argv[0]).name} LABEL BEFORE.xwd AFTER.xwd")
    label = sys.argv[1].upper().replace("-", "_")
    result = changed_region(pathlib.Path(sys.argv[2]).read_bytes(), pathlib.Path(sys.argv[3]).read_bytes())
    for key, value in result.items():
        print(f"TRACK_A_{label}_{key.upper()}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
