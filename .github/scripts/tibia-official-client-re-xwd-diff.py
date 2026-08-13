#!/usr/bin/env python3
"""Return the changed-pixel count for two same-sized XWD captures."""

from __future__ import annotations

import pathlib
import struct
import sys


def _header(blob: bytes) -> tuple[str, tuple[int, ...]]:
    if len(blob) < 100:
        raise ValueError("truncated XWD header")
    for endian in (">", "<"):
        fields = struct.unpack(f"{endian}25I", blob[:100])
        header_size, version, image_format, _, width, height, *_ = fields
        if 100 <= header_size <= len(blob) and version == 7 and image_format <= 2 and width and height:
            return endian, fields
    raise ValueError("unsupported XWD header")


def _pixels(blob: bytes) -> tuple[int, int, int, int, bytes]:
    _, fields = _header(blob)
    header_size, _, _, _, width, height, _, _, _, _, _, bits_per_pixel, bytes_per_line, *rest = fields
    ncolors = rest[6]
    pixel_bytes = (bits_per_pixel + 7) // 8
    offset = header_size + ncolors * 12
    expected = offset + height * bytes_per_line
    if not pixel_bytes or bytes_per_line < width * pixel_bytes or expected > len(blob):
        raise ValueError("truncated or unsupported XWD pixel data")
    return width, height, pixel_bytes, bytes_per_line, blob[offset:expected]


def changed_pixels(before: bytes, after: bytes) -> int:
    width, height, pixel_bytes, stride, before_pixels = _pixels(before)
    after_width, after_height, after_pixel_bytes, after_stride, after_pixels = _pixels(after)
    if (width, height, pixel_bytes, stride) != (after_width, after_height, after_pixel_bytes, after_stride):
        raise ValueError("XWD captures have different geometry or pixel format")
    changed = 0
    row_bytes = width * pixel_bytes
    for row in range(height):
        start = row * stride
        for column in range(0, row_bytes, pixel_bytes):
            if before_pixels[start + column : start + column + pixel_bytes] != after_pixels[start + column : start + column + pixel_bytes]:
                changed += 1
    return changed


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(f"usage: {pathlib.Path(sys.argv[0]).name} BEFORE.xwd AFTER.xwd")
    print(changed_pixels(pathlib.Path(sys.argv[1]).read_bytes(), pathlib.Path(sys.argv[2]).read_bytes()))
