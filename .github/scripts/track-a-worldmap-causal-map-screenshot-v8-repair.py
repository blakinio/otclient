#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

MARKER = "echo 'WORLDMAP_BASELINE_STRUCTURAL_IN_GAME=PASS'\n"

REPLACEMENT = r'''echo 'WORLDMAP_BASELINE_STRUCTURAL_IN_GAME=PASS'

# Owner-authorized corroborating visual evidence. Structural FullMap + strip
# proof above is authoritative; the screenshot is never used to establish
# IN_GAME by itself. Capture the exact manifest-owned UI XID only.
SCREENSHOT_EXPORTER="${GITHUB_WORKSPACE:-$PWD}/.github/scripts/track-a-worldmap-causal-xwd-to-png.py"
SCREENSHOT_XWD="$ROOT/world-entry-map.xwd"
SCREENSHOT_PNG="$EVIDENCE/map-world-entry.png"
[[ -f "$SCREENSHOT_EXPORTER" ]] || fail map_screenshot_exporter_missing
capture_xwd "$SCREENSHOT_XWD"

CROP_W=1280
CROP_H=720
(( CROP_W > ACTUAL_WIDTH )) && CROP_W=$ACTUAL_WIDTH
(( CROP_H > ACTUAL_HEIGHT )) && CROP_H=$ACTUAL_HEIGHT
CROP_X0=$(((ACTUAL_WIDTH-CROP_W)/2))
CROP_Y0=$(((ACTUAL_HEIGHT-CROP_H)/2))
CROP_X1=$((CROP_X0+CROP_W))
CROP_Y1=$((CROP_Y0+CROP_H))
python3 "$SCREENSHOT_EXPORTER" "$SCREENSHOT_XWD" "$SCREENSHOT_PNG" \
  --crop "$CROP_X0" "$CROP_Y0" "$CROP_X1" "$CROP_Y1"
rm -f "$SCREENSHOT_XWD"
[[ -s "$SCREENSHOT_PNG" ]] || fail map_screenshot_png_missing
chmod 600 "$SCREENSHOT_PNG"
SCREENSHOT_SHA="$(sha256sum "$SCREENSHOT_PNG" | awk '{print $1}')"
[[ "$SCREENSHOT_SHA" =~ ^[0-9a-f]{64}$ ]] || fail map_screenshot_sha_invalid
echo "WORLDMAP_BASELINE_MAP_SCREENSHOT_SHA256=$SCREENSHOT_SHA"
echo 'WORLDMAP_BASELINE_MAP_SCREENSHOT=PASS'
'''


class TransformRefused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(MARKER) != 1:
        raise TransformRefused(f"STRUCTURAL_MARKER_COUNT:{text.count(MARKER)}")
    output = text.replace(MARKER, REPLACEMENT, 1)
    required = (
        "WORLDMAP_BASELINE_STRUCTURAL_IN_GAME=PASS",
        "WORLDMAP_BASELINE_MAP_SCREENSHOT=PASS",
        "WORLDMAP_BASELINE_MAP_SCREENSHOT_SHA256=",
        'capture_xwd "$SCREENSHOT_XWD"',
        "track-a-worldmap-causal-xwd-to-png.py",
        'rm -f "$SCREENSHOT_XWD"',
        'UI_WIN="$WIN"',
    )
    missing = [token for token in required if token not in output]
    if missing:
        raise TransformRefused("REQUIRED_MISSING:" + ",".join(missing))
    lower = output.lower()
    forbidden_lower = (
        '"$xwd" -root',
        "xwd -root",
        "xrandr --output",
        "wmctrl -r",
        "tesseract",
        "ocrmypdf",
    )
    survivors = [token for token in forbidden_lower if token in lower]
    if survivors:
        raise TransformRefused("FORBIDDEN_SURVIVORS:" + ",".join(survivors))
    if output.count('UI_WIN="$WIN"') != 1:
        raise TransformRefused("MANIFEST_WINDOW_IDENTITY_NOT_UNIQUE")
    marker_at = output.index("WORLDMAP_BASELINE_STRUCTURAL_IN_GAME=PASS")
    capture_at = output.index('SCREENSHOT_XWD="$ROOT/world-entry-map.xwd"')
    if capture_at <= marker_at:
        raise TransformRefused("SCREENSHOT_NOT_POST_STRUCTURAL")
    return output


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    args = p.parse_args()
    try:
        result = transform(args.source.read_text(encoding="utf-8"))
    except TransformRefused as exc:
        print(f"WORLDMAP_MAP_SCREENSHOT_V8_REPAIR_REFUSED={exc}")
        return 44
    args.output.write_text(result, encoding="utf-8")
    args.output.chmod(0o700)
    print("WORLDMAP_MAP_SCREENSHOT_V8_REPAIR=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
