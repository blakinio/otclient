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
# Normalize only the task-owned Xvfb desktop to the retained successful-flow
# geometry. Do not bind XRes ownership to an assumed window size: the task-local
# census owner keeps exact-PID ownership as the authority, reports every owned
# VIEWABLE geometry, and selects only a unique largest owned window.
OWNER_CENSUS_DIR="$RUNNER_TEMP/worldmap-xres-owner-census"
OWNER_CENSUS="$OWNER_CENSUS_DIR/tibia-official-client-re-xres-window-owner.py"
mkdir -p "$OWNER_CENSUS_DIR"
chmod 700 "$OWNER_CENSUS_DIR"
python3 - "$STAGE_WORKER" <<'PY_1020'
from pathlib import Path
import sys
stage_path=Path(sys.argv[1])
stage=stage_path.read_text()
old_screen='-screen 0 1920x1080x24'
new_screen='-screen 0 1020x650x24'
if stage.count(old_screen)!=1:
    raise SystemExit(f'WORLDMAP_SCREEN_NORMALIZE_ERROR=screen_anchor_count:{stage.count(old_screen)}')
stage=stage.replace(old_screen,new_screen,1)
stage_path.write_text(stage)
stage_path.chmod(0o700)
print('WORLDMAP_SCREEN_NORMALIZE_STAGE=PASS')
PY_1020
python3 .github/scripts/track-a-worldmap-causal-xres-geometry-census-repair.py \
  .github/scripts/tibia-official-client-re-xres-window-owner.py "$OWNER_CENSUS"
python3 -m py_compile "$OWNER_CENSUS"
grep -F 'WORLDMAP_XRES_OWNED_VIEWABLE_COUNT=' "$OWNER_CENSUS" >/dev/null || fail xres_census_owner_marker_missing
grep -F 'WORLDMAP_XRES_SELECTED_GEOMETRY=' "$OWNER_CENSUS" >/dev/null || fail xres_census_selected_marker_missing
! grep -F 'and int(attr.width) == TARGET_WIDTH' "$OWNER_CENSUS" >/dev/null || fail xres_census_width_filter_survived
! grep -F 'and int(attr.height) == TARGET_HEIGHT' "$OWNER_CENSUS" >/dev/null || fail xres_census_height_filter_survived
echo 'WORLDMAP_SCREEN_XRES_GEOMETRY_CENSUS_OWNER=PASS'
python3 .github/scripts/tibia-official-client-re-canonical-xres-worker-adapter.py \
  "$STAGE_WORKER" "$WORKER" \
  --owner-helper "$OWNER_CENSUS" \
  --wire-helper .github/scripts/tibia-official-client-re-xres-wire.py
grep -F -- '-screen 0 1020x650x24' "$WORKER" >/dev/null || fail normalized_screen_missing
! grep -F -- '-screen 0 1920x1080x24' "$WORKER" >/dev/null || fail old_screen_survived
grep -F -- "$(readlink -f "$OWNER_CENSUS")" "$WORKER" >/dev/null || fail xres_census_owner_binding_missing
echo 'WORLDMAP_BASELINE_DESKTOP_GEOMETRY=1020x650'
echo 'WORLDMAP_BASELINE_XRES_SELECTOR=EXACT_PID_UNIQUE_LARGEST_VIEWABLE'
'''

CLEANUP_OLD = '  rm -f "$STAGE_WORKER" "$WORKER" "$GCMD" 2>/dev/null || true\n'
CLEANUP_NEW = CLEANUP_OLD + '  rm -rf "$RUNNER_TEMP/worldmap-xres-owner-census" 2>/dev/null || true\n'


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
        "WORLDMAP_SCREEN_XRES_GEOMETRY_CENSUS_OWNER=PASS",
        "WORLDMAP_BASELINE_XRES_SELECTOR=EXACT_PID_UNIQUE_LARGEST_VIEWABLE",
        "track-a-worldmap-causal-xres-geometry-census-repair.py",
        '--owner-helper "$OWNER_CENSUS"',
        'xres_census_owner_binding_missing',
        'rm -rf "$RUNNER_TEMP/worldmap-xres-owner-census"',
    )
    missing = [token for token in required if token not in output]
    if missing:
        raise TransformRefused("REQUIRED_MISSING:" + ",".join(missing))
    forbidden = (
        'worldmap-xres-owner-1020',
        'TARGET_WIDTH = 1020',
        'TARGET_HEIGHT = 650',
        '--owner-helper "$OWNER_1020"',
    )
    survivors = [token for token in forbidden if token in output]
    if survivors:
        raise TransformRefused("LEGACY_GEOMETRY_OWNER_SURVIVORS:" + ",".join(survivors))
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
