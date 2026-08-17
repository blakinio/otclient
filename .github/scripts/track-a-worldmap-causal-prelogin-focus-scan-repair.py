#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


SECRET_REQUIRE = '[[ -n "${TIBIA_TEST_EMAIL:-}" && -n "${TIBIA_TEST_PASSWORD:-}" ]] || fail protected_login_secrets_missing\n'
SECRET_ABSENT = '[[ -z "${TIBIA_TEST_EMAIL:-}" && -z "${TIBIA_TEST_PASSWORD:-}" ]] || fail prelogin_focus_scan_secret_env_present\n'
TOOLING_MARKER = "echo 'WORLDMAP_BASELINE_LOGIN_UI_TOOLING=RAW_XWD_AGGREGATE_BEHAVIOR_PASS'\n"

SCAN_TAIL = r'''
echo 'WORLDMAP_PRELOGIN_FOCUS_SCAN_SECRET_ENV=ABSENT'
echo 'WORLDMAP_PRELOGIN_FOCUS_SCAN_MODE=TAB_REVERSIBLE_DUMMY_TEXT'

CANDIDATES=0
scan_focus_round() {
  local round="$1" idx before typed cleared probe rc bbox typed_changed overlap variant_a variant_b variant_out variant_changed
  xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
  xdo windowfocus --sync "$UI_WIN"

  for idx in $(seq 0 15); do
    before="$ROOT/focus-$round-$idx-before.xwd"
    typed="$ROOT/focus-$round-$idx-typed.xwd"
    cleared="$ROOT/focus-$round-$idx-cleared.xwd"
    variant_a="$ROOT/focus-$round-$idx-variant-a.xwd"
    variant_b="$ROOT/focus-$round-$idx-variant-b.xwd"

    capture_xwd "$before"
    xdo type --window "$UI_WIN" --delay 10 -- 'wmprobe7'
    sleep .20
    capture_xwd "$typed"
    xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
    sleep .20
    capture_xwd "$cleared"

    set +e
    probe="$(python3 "$COMPARE" roi-cycle "$before" "$typed" "$cleared" 0 0 1020 650 --min-changed 60 2>&1)"
    rc=$?
    set -e

    if [[ "$rc" -eq 0 ]]; then
      bbox="$(awk -F= '/^WORLDMAP_XWD_EDITABLE_TYPED_BBOX=/{print $2}' <<<"$probe" | tail -1)"
      typed_changed="$(awk -F= '/^WORLDMAP_XWD_EDITABLE_TYPED_CHANGED=/{print $2}' <<<"$probe" | tail -1)"
      overlap="$(awk -F= '/^WORLDMAP_XWD_EDITABLE_MASK_OVERLAP_RATIO=/{print $2}' <<<"$probe" | tail -1)"
      [[ "$bbox" =~ ^[0-9]+,[0-9]+,[0-9]+,[0-9]+$ ]] || fail focus_scan_candidate_bbox_invalid
      [[ "$typed_changed" =~ ^[0-9]+$ ]] || fail focus_scan_candidate_changed_invalid
      [[ "$overlap" =~ ^0\.[0-9]+$|^1\.000000$ ]] || fail focus_scan_candidate_overlap_invalid

      # Equal-length visual discriminator. A masked field should render these two
      # strings almost identically; an unmasked text field should not. This step
      # only records aggregate changed-pixel evidence and does not classify the
      # field semantically by itself.
      xdo type --window "$UI_WIN" --delay 10 -- 'iiiiii'
      sleep .20
      capture_xwd "$variant_a"
      xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
      xdo type --window "$UI_WIN" --delay 10 -- 'WWWWWW'
      sleep .20
      capture_xwd "$variant_b"
      xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
      sleep .15
      variant_out="$(python3 "$COMPARE" change "$variant_a" "$variant_b" --min-changed 0)"
      variant_changed="$(awk -F= '/^WORLDMAP_XWD_CHANGED_PIXELS=/{print $2}' <<<"$variant_out" | tail -1)"
      [[ "$variant_changed" =~ ^[0-9]+$ ]] || fail focus_scan_variant_changed_invalid

      CANDIDATES=$((CANDIDATES+1))
      echo "WORLDMAP_PRELOGIN_EDITABLE_CANDIDATE=round:$round;tab:$idx;bbox:$bbox;typed_changed:$typed_changed;overlap:$overlap;equal_length_variant_changed:$variant_changed"
    fi

    rm -f "$before" "$typed" "$cleared" "$variant_a" "$variant_b"
    xdo key --window "$UI_WIN" --clearmodifiers Tab
    sleep .12
  done
}

scan_focus_round 1
if [[ "$CANDIDATES" -eq 0 ]]; then
  echo 'WORLDMAP_PRELOGIN_FOCUS_SCAN_FIRST_ROUND=no_editable_candidate'
  sleep 20
  scan_focus_round 2
fi

echo "WORLDMAP_PRELOGIN_EDITABLE_CANDIDATE_COUNT=$CANDIDATES"
[[ "$CANDIDATES" -gt 0 ]] || fail no_editable_focus_state_detected
echo 'WORLDMAP_PRELOGIN_FOCUS_SCAN=COMPLETE_NO_SECRET'
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
        'WORLDMAP_PRELOGIN_FOCUS_SCAN_MODE=TAB_REVERSIBLE_DUMMY_TEXT',
        'WORLDMAP_PRELOGIN_EDITABLE_CANDIDATE=',
        'WORLDMAP_PRELOGIN_EDITABLE_CANDIDATE_COUNT=',
        'WORLDMAP_PRELOGIN_FOCUS_SCAN=COMPLETE_NO_SECRET',
        "'wmprobe7'",
        "'iiiiii'",
        "'WWWWWW'",
        'roi-cycle "$before" "$typed" "$cleared" 0 0 1020 650 --min-changed 60',
        'xdo key --window "$UI_WIN" --clearmodifiers Tab',
        'rm -f "$before" "$typed" "$cleared" "$variant_a" "$variant_b"',
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
