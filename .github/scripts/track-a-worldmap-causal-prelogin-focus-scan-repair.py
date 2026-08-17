#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SECRET_REQUIRE = '[[ -n "${TIBIA_TEST_EMAIL:-}" && -n "${TIBIA_TEST_PASSWORD:-}" ]] || fail protected_login_secrets_missing\n'
SECRET_ABSENT = '[[ -z "${TIBIA_TEST_EMAIL:-}" && -z "${TIBIA_TEST_PASSWORD:-}" ]] || fail prelogin_focus_scan_secret_env_present\n'
TOOLING_MARKER = "echo 'WORLDMAP_BASELINE_LOGIN_UI_TOOLING=RAW_XWD_AGGREGATE_BEHAVIOR_PASS'\n"

SCAN_TAIL = r'''
echo 'WORLDMAP_PRELOGIN_FOCUS_SCAN_SECRET_ENV=ABSENT'
echo 'WORLDMAP_PRELOGIN_FOCUS_SCAN_MODE=TAB_NOISE_MASK_CONTROLLED_REVERSIBLE_DUMMY_TEXT'

CANDIDATES=0
scan_focus_round() {
  local round="$1" idx idle0 idle1 idle2 typed cleared idle3 probe rc bbox signal overlap noise residual
  xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
  xdo windowfocus --sync "$UI_WIN"

  for idx in $(seq 0 15); do
    idle0="$ROOT/focus-$round-$idx-idle0.xwd"
    idle1="$ROOT/focus-$round-$idx-idle1.xwd"
    idle2="$ROOT/focus-$round-$idx-idle2.xwd"
    typed="$ROOT/focus-$round-$idx-typed.xwd"
    cleared="$ROOT/focus-$round-$idx-cleared.xwd"
    idle3="$ROOT/focus-$round-$idx-idle3.xwd"

    capture_xwd "$idle0"
    sleep .18
    capture_xwd "$idle1"
    sleep .18
    capture_xwd "$idle2"

    xdo type --window "$UI_WIN" --delay 10 -- 'wmprobe7'
    sleep .20
    capture_xwd "$typed"
    xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
    sleep .20
    capture_xwd "$cleared"
    sleep .20
    capture_xwd "$idle3"

    set +e
    probe="$(python3 "$COMPARE" controlled-cycle \
      "$idle0" "$idle1" "$idle2" "$typed" "$cleared" "$idle3" \
      --min-signal 25 --min-overlap-ratio 0.55 \
      --max-width 500 --max-height 120 --max-area 30000 2>&1)"
    rc=$?
    set -e

    noise="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_NOISE_PIXELS=/{print $2}' <<<"$probe" | tail -1)"
    signal="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_SIGNAL_CHANGED=/{print $2}' <<<"$probe" | tail -1)"
    overlap="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_OVERLAP_RATIO=/{print $2}' <<<"$probe" | tail -1)"
    bbox="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_SIGNAL_BBOX=/{print $2}' <<<"$probe" | tail -1)"
    residual="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_RESIDUAL_CHANGED=/{print $2}' <<<"$probe" | tail -1)"
    [[ "$noise" =~ ^[0-9]+$ && "$signal" =~ ^[0-9]+$ && "$residual" =~ ^[0-9]+$ ]] || fail focus_scan_controlled_count_invalid
    [[ "$overlap" =~ ^0\.[0-9]+$|^1\.000000$ ]] || fail focus_scan_controlled_overlap_invalid

    echo "WORLDMAP_PRELOGIN_CONTROLLED_FOCUS_METRIC=round:$round;tab:$idx;noise_pixels:$noise;signal_changed:$signal;overlap:$overlap;bbox:$bbox;residual_changed:$residual;pass:$([[ "$rc" -eq 0 ]] && echo true || echo false)"

    if [[ "$rc" -eq 0 ]]; then
      [[ "$bbox" =~ ^[0-9]+,[0-9]+,[0-9]+,[0-9]+$ ]] || fail focus_scan_candidate_bbox_invalid
      CANDIDATES=$((CANDIDATES+1))
      echo "WORLDMAP_PRELOGIN_CONTROLLED_EDITABLE_CANDIDATE=round:$round;tab:$idx;bbox:$bbox;signal_changed:$signal;overlap:$overlap;noise_pixels:$noise;residual_changed:$residual"
    fi

    rm -f "$idle0" "$idle1" "$idle2" "$typed" "$cleared" "$idle3"
    xdo key --window "$UI_WIN" --clearmodifiers Tab
    sleep .12
  done
}

scan_focus_round 1
if [[ "$CANDIDATES" -eq 0 ]]; then
  echo 'WORLDMAP_PRELOGIN_CONTROLLED_FOCUS_SCAN_FIRST_ROUND=no_editable_candidate'
  sleep 20
  scan_focus_round 2
fi

echo "WORLDMAP_PRELOGIN_CONTROLLED_EDITABLE_CANDIDATE_COUNT=$CANDIDATES"
[[ "$CANDIDATES" -gt 0 ]] || fail no_noise_mask_controlled_editable_focus_state_detected
echo 'WORLDMAP_PRELOGIN_CONTROLLED_FOCUS_SCAN=COMPLETE_NO_SECRET'
exit 0
'''


class TransformRefused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(SECRET_REQUIRE) != 1:
        raise TransformRefused(f"SECRET_REQUIRE_COUNT:{text.count(SECRET_REQUIRE)}")
    text = text.replace(SECRET_REQUIRE, SECRET_ABSENT, 1)
    if text.count(TOOLING_MARKER) != 1:
        raise TransformRefused(f"TOOLING_MARKER_COUNT:{text.count(TOOLING_MARKER)}")
    cut = text.index(TOOLING_MARKER) + len(TOOLING_MARKER)
    output = text[:cut] + SCAN_TAIL

    forbidden = (
        'printf \'%s\' "$TIBIA_TEST_EMAIL"',
        'printf \'%s\' "$TIBIA_TEST_PASSWORD"',
        'WORLDMAP_BASELINE_LOGIN_SUBMITTED=true',
        'WORLDMAP_BASELINE_CHARACTER_ACTIVATION_SENT=true',
        'WORLDMAP_BASELINE_RIGHT_SENT=true',
        'WORLDMAP_BASELINE_LEFT_SENT=true',
    )
    survivors = [token for token in forbidden if token in output]
    if survivors:
        raise TransformRefused("SECRET_OR_GAMEPLAY_SURVIVORS:" + ",".join(survivors))

    required = (
        'prelogin_focus_scan_secret_env_present',
        'WORLDMAP_PRELOGIN_FOCUS_SCAN_SECRET_ENV=ABSENT',
        'WORLDMAP_PRELOGIN_FOCUS_SCAN_MODE=TAB_NOISE_MASK_CONTROLLED_REVERSIBLE_DUMMY_TEXT',
        'WORLDMAP_PRELOGIN_CONTROLLED_FOCUS_METRIC=',
        'WORLDMAP_PRELOGIN_CONTROLLED_EDITABLE_CANDIDATE=',
        'WORLDMAP_PRELOGIN_CONTROLLED_EDITABLE_CANDIDATE_COUNT=',
        'WORLDMAP_PRELOGIN_CONTROLLED_FOCUS_SCAN=COMPLETE_NO_SECRET',
        "'wmprobe7'",
        'controlled-cycle',
        '--min-signal 25 --min-overlap-ratio 0.55',
        '--max-width 500 --max-height 120 --max-area 30000',
        'xdo key --window "$UI_WIN" --clearmodifiers Tab',
        'rm -f "$idle0" "$idle1" "$idle2" "$typed" "$cleared" "$idle3"',
        'exit 0',
    )
    missing = [token for token in required if token not in output]
    if missing:
        raise TransformRefused("REQUIRED_MISSING:" + ",".join(missing))
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        repaired = transform(args.source.read_text(encoding="utf-8"))
    except TransformRefused as exc:
        print(f"WORLDMAP_PRELOGIN_FOCUS_SCAN_REPAIR_REFUSED={exc}")
        return 44
    args.output.write_text(repaired, encoding="utf-8")
    args.output.chmod(0o700)
    print("WORLDMAP_PRELOGIN_FOCUS_SCAN_REPAIR=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
