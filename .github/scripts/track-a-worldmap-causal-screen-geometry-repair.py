#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


ADAPTER_BLOCK = r'''PY
python3 .github/scripts/tibia-official-client-re-canonical-xres-worker-adapter.py \
  "$STAGE_WORKER" "$WORKER" \
  --owner-helper .github/scripts/tibia-official-client-re-xres-window-owner.py \
  --wire-helper .github/scripts/tibia-official-client-re-xres-wire.py
'''

REPLACEMENT = r'''PY
# Normalize this task-owned ephemeral desktop to the exact 1020x650 geometry of
# the retained successful login flow. Baseline and patched comparison must use
# the identical transform. The canonical source/helper files are not modified.
OWNER_1020_DIR="$RUNNER_TEMP/worldmap-xres-owner-1020"
OWNER_1020="$OWNER_1020_DIR/tibia-official-client-re-xres-window-owner.py"
mkdir -p "$OWNER_1020_DIR"
chmod 700 "$OWNER_1020_DIR"
python3 - "$STAGE_WORKER" "$OWNER_1020" <<'PY_1020'
from pathlib import Path
import sys
stage_path=Path(sys.argv[1]); owner_out=Path(sys.argv[2])
stage=stage_path.read_text()
old_screen='-screen 0 1920x1080x24'
new_screen='-screen 0 1020x650x24'
if stage.count(old_screen)!=1:
    raise SystemExit(f'WORLDMAP_SCREEN_NORMALIZE_ERROR=screen_anchor_count:{stage.count(old_screen)}')
stage=stage.replace(old_screen,new_screen,1)
stage_path.write_text(stage)
stage_path.chmod(0o700)
owner=Path('.github/scripts/tibia-official-client-re-xres-window-owner.py').read_text()
replacements=(('TARGET_WIDTH = 1920','TARGET_WIDTH = 1020'),('TARGET_HEIGHT = 1080','TARGET_HEIGHT = 650'))
for old,new in replacements:
    if owner.count(old)!=1:
        raise SystemExit(f'WORLDMAP_SCREEN_NORMALIZE_ERROR=owner_anchor_count:{old}:{owner.count(old)}')
    owner=owner.replace(old,new,1)
owner_out.write_text(owner)
owner_out.chmod(0o600)
print('WORLDMAP_SCREEN_NORMALIZE_STAGE=PASS')
print('WORLDMAP_SCREEN_NORMALIZE_OWNER=PASS')
PY_1020
python3 .github/scripts/tibia-official-client-re-canonical-xres-worker-adapter.py \
  "$STAGE_WORKER" "$WORKER" \
  --owner-helper "$OWNER_1020" \
  --wire-helper .github/scripts/tibia-official-client-re-xres-wire.py
grep -F -- '-screen 0 1020x650x24' "$WORKER" >/dev/null || fail normalized_screen_missing
! grep -F -- '-screen 0 1920x1080x24' "$WORKER" >/dev/null || fail old_screen_survived
echo 'WORLDMAP_BASELINE_DESKTOP_GEOMETRY=1020x650'
'''

CLEANUP_OLD = '  rm -f "$STAGE_WORKER" "$WORKER" "$GCMD" 2>/dev/null || true\n'
CLEANUP_NEW = CLEANUP_OLD + '  rm -rf "$RUNNER_TEMP/worldmap-xres-owner-1020" 2>/dev/null || true\n'


class TransformRefused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(ADAPTER_BLOCK) != 1:
        raise TransformRefused(f"ADAPTER_BLOCK_COUNT:{text.count(ADAPTER_BLOCK)}")
    if text.count(CLEANUP_OLD) != 1:
        raise TransformRefused(f"CLEANUP_ANCHOR_COUNT:{text.count(CLEANUP_OLD)}")
    output = text.replace(ADAPTER_BLOCK, REPLACEMENT, 1)
    output = output.replace(CLEANUP_OLD, CLEANUP_NEW, 1)
    required = (
        "WORLDMAP_BASELINE_DESKTOP_GEOMETRY=1020x650",
        "WORLDMAP_SCREEN_NORMALIZE_STAGE=PASS",
        "WORLDMAP_SCREEN_NORMALIZE_OWNER=PASS",
        'TARGET_WIDTH = 1020',
        'TARGET_HEIGHT = 650',
        '--owner-helper "$OWNER_1020"',
        'rm -rf "$RUNNER_TEMP/worldmap-xres-owner-1020"',
    )
    missing = [token for token in required if token not in output]
    if missing:
        raise TransformRefused("REQUIRED_MISSING:" + ",".join(missing))
    return output


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    args = p.parse_args()
    try:
        repaired = transform(args.source.read_text(encoding="utf-8"))
    except TransformRefused as exc:
        print(f"WORLDMAP_SCREEN_GEOMETRY_REPAIR_REFUSED={exc}")
        return 44
    args.output.write_text(repaired, encoding="utf-8")
    args.output.chmod(0o700)
    print("WORLDMAP_SCREEN_GEOMETRY_REPAIR=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
