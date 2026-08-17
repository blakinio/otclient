#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SECRET_REQUIRE = '[[ -n "${TIBIA_TEST_EMAIL:-}" && -n "${TIBIA_TEST_PASSWORD:-}" ]] || fail protected_login_secrets_missing\n'
SECRET_ABSENT = '[[ -z "${TIBIA_TEST_EMAIL:-}" && -z "${TIBIA_TEST_PASSWORD:-}" ]] || fail prelogin_focus_scan_secret_env_present\n'
TOOLING_MARKER = "echo 'WORLDMAP_BASELINE_LOGIN_UI_TOOLING=RAW_XWD_AGGREGATE_BEHAVIOR_PASS'\n"

SCAN_TAIL = r'''
echo 'WORLDMAP_PRELOGIN_FOCUS_SCAN_SECRET_ENV=ABSENT'
echo 'WORLDMAP_PRELOGIN_FOCUS_SCAN_MODE=TAB_REVERSIBLE_DUMMY_TEXT_AMBIENT_CONTROLLED'

CANDIDATES=0
ACTION_DELTA_MIN=80
scan_focus_round() {
  local round="$1" idx idle0 idle1 typed cleared postidle probe rc bbox typed_changed cleared_changed overlap
  local pre_idle_out post_idle_out pre_idle_changed post_idle_changed ambient typed_delta cleared_delta
  xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
  xdo windowfocus --sync "$UI_WIN"

  for idx in $(seq 0 15); do
    idle0="$ROOT/focus-$round-$idx-idle0.xwd"
    idle1="$ROOT/focus-$round-$idx-idle1.xwd"
    typed="$ROOT/focus-$round-$idx-typed.xwd"
    cleared="$ROOT/focus-$round-$idx-cleared.xwd"
    postidle="$ROOT/focus-$round-$idx-postidle.xwd"

    capture_xwd "$idle0"
    sleep .20
    capture_xwd "$idle1"
    pre_idle_out="$(python3 "$COMPARE" change "$idle0" "$idle1" --min-changed 0)"
    pre_idle_changed="$(awk -F= '/^WORLDMAP_XWD_CHANGED_PIXELS=/{print $2}' <<<"$pre_idle_out" | tail -1)"
    [[ "$pre_idle_changed" =~ ^[0-9]+$ ]] || fail focus_scan_pre_idle_changed_invalid

    xdo type --window "$UI_WIN" --delay 10 -- 'wmprobe7'
    sleep .20
    capture_xwd "$typed"
    xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
    sleep .20
    capture_xwd "$cleared"
    sleep .20
    capture_xwd "$postidle"
    post_idle_out="$(python3 "$COMPARE" change "$cleared" "$postidle" --min-changed 0)"
    post_idle_changed="$(awk -F= '/^WORLDMAP_XWD_CHANGED_PIXELS=/{print $2}' <<<"$post_idle_out" | tail -1)"
    [[ "$post_idle_changed" =~ ^[0-9]+$ ]] || fail focus_scan_post_idle_changed_invalid

    set +e
    probe="$(python3 "$COMPARE" roi-cycle "$idle1" "$typed" "$cleared" 0 0 1020 650 --min-changed 60 2>&1)"
    rc=$?
    set -e

    typed_changed="$(awk -F= '/^WORLDMAP_XWD_EDITABLE_TYPED_CHANGED=/{print $2}' <<<"$probe" | tail -1)"
    cleared_changed="$(awk -F= '/^WORLDMAP_XWD_EDITABLE_CLEARED_CHANGED=/{print $2}' <<<"$probe" | tail -1)"
    overlap="$(awk -F= '/^WORLDMAP_XWD_EDITABLE_MASK_OVERLAP_RATIO=/{print $2}' <<<"$probe" | tail -1)"
    bbox="$(awk -F= '/^WORLDMAP_XWD_EDITABLE_TYPED_BBOX=/{print $2}' <<<"$probe" | tail -1)"
    [[ "$typed_changed" =~ ^[0-9]+$ ]] || fail focus_scan_typed_changed_invalid
    [[ "$cleared_changed" =~ ^[0-9]+$ ]] || fail focus_scan_cleared_changed_invalid
    [[ "$overlap" =~ ^0\.[0-9]+$|^1\.000000$ ]] || fail focus_scan_overlap_invalid

    if (( pre_idle_changed > post_idle_changed )); then ambient="$pre_idle_changed"; else ambient="$post_idle_changed"; fi
    if (( typed_changed > ambient )); then typed_delta=$((typed_changed-ambient)); else typed_delta=0; fi
    if (( cleared_changed > ambient )); then cleared_delta=$((cleared_changed-ambient)); else cleared_delta=0; fi

    echo "WORLDMAP_PRELOGIN_FOCUS_METRIC=round:$round;tab:$idx;pre_idle:$pre_idle_changed;post_idle:$post_idle_changed;ambient:$ambient;typed:$typed_changed;cleared:$cleared_changed;typed_delta:$typed_delta;cleared_delta:$cleared_delta;overlap:$overlap;bbox:$bbox"

    if [[ "$rc" -eq 0 && "$typed_delta" -ge "$ACTION_DELTA_MIN" && "$cleared_delta" -ge "$ACTION_DELTA_MIN" ]]; then
      [[ "$bbox" =~ ^[0-9]+,[0-9]+,[0-9]+,[0-9]+$ ]] || fail focus_scan_candidate_bbox_invalid
      CANDIDATES=$((CANDIDATES+1))
      echo "WORLDMAP_PRELOGIN_EDITABLE_CANDIDATE=round:$round;tab:$idx;bbox:$bbox;ambient:$ambient;typed_delta:$typed_delta;cleared_delta:$cleared_delta;overlap:$overlap"
    fi

    rm -f "$idle0" "$idle1" "$typed" "$cleared" "$postidle"
    xdo key --window "$UI_WIN" --clearmodifiers Tab
    sleep .12
  done
}

scan_focus_round 1
if [[ "$CANDIDATES" -eq 0 ]]; then
  echo 'WORLDMAP_PRELOGIN_FOCUS_SCAN_FIRST_ROUND=no_ambient_controlled_candidate'
  sleep 20
  scan_focus_round 2
fi

echo "WORLDMAP_PRELOGIN_EDITABLE_CANDIDATE_COUNT=$CANDIDATES"
[[ "$CANDIDATES" -gt 0 ]] || fail no_ambient_controlled_editable_focus_state_detected
echo 'WORLDMAP_PRELOGIN_FOCUS_SCAN=COMPLETE_NO_SECRET_AMBIENT_CONTROLLED'
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
        'WORLDMAP_PRELOGIN_FOCUS_SCAN_MODE=TAB_REVERSIBLE_DUMMY_TEXT_AMBIENT_CONTROLLED',
        'WORLDMAP_PRELOGIN_FOCUS_METRIC=',
        'WORLDMAP_PRELOGIN_EDITABLE_CANDIDATE=',
        'WORLDMAP_PRELOGIN_EDITABLE_CANDIDATE_COUNT=',
        'WORLDMAP_PRELOGIN_FOCUS_SCAN=COMPLETE_NO_SECRET_AMBIENT_CONTROLLED',
        'ACTION_DELTA_MIN=80',
        "'wmprobe7'",
        'change "$idle0" "$idle1" --min-changed 0',
        'change "$cleared" "$postidle" --min-changed 0',
        'roi-cycle "$idle1" "$typed" "$cleared" 0 0 1020 650 --min-changed 60',
        'typed_delta=$((typed_changed-ambient))',
        'cleared_delta=$((cleared_changed-ambient))',
        'xdo key --window "$UI_WIN" --clearmodifiers Tab',
        'rm -f "$idle0" "$idle1" "$typed" "$cleared" "$postidle"',
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
