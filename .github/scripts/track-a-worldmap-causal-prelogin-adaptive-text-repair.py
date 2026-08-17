#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

SECRET_REQUIRE = '[[ -n "${TIBIA_TEST_EMAIL:-}" && -n "${TIBIA_TEST_PASSWORD:-}" ]] || fail protected_login_secrets_missing\n'
SECRET_ABSENT = '[[ -z "${TIBIA_TEST_EMAIL:-}" && -z "${TIBIA_TEST_PASSWORD:-}" ]] || fail prelogin_adaptive_text_secret_env_present\n'
TOOLING_MARKER = "echo 'WORLDMAP_BASELINE_LOGIN_UI_TOOLING=RAW_XWD_AGGREGATE_BEHAVIOR_PASS'\n"

TAIL = r'''
echo 'WORLDMAP_PRELOGIN_ADAPTIVE_TEXT_SECRET_ENV=ABSENT'
echo 'WORLDMAP_PRELOGIN_ADAPTIVE_TEXT_MODE=SAME_LAUNCH_DISCOVER_THEN_CLASSIFY'
SEMANTICS="${GITHUB_WORKSPACE:-$PWD}/.github/scripts/track-a-worldmap-causal-xwd-text-semantics.py"
[[ -f "$SEMANTICS" ]] || fail adaptive_text_semantics_helper_missing

LOCAL_CANDIDATES=0
TEXT_FIELDS=0
scan_round() {
  local round="$1" idx d0 d1 d2 dtyped dclear d3 discover discover_rc dbbox dsignal doverlap dnoise dresidual
  local s0 s1 s2 short sclear long lclear s3 semantic semantic_rc short_n long_n growth ratio sbbox lbbox

  xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
  xdo windowfocus --sync "$UI_WIN"

  for idx in $(seq 0 15); do
    d0="$ROOT/adaptive-$round-$idx-d0.xwd"; d1="$ROOT/adaptive-$round-$idx-d1.xwd"; d2="$ROOT/adaptive-$round-$idx-d2.xwd"
    dtyped="$ROOT/adaptive-$round-$idx-dtyped.xwd"; dclear="$ROOT/adaptive-$round-$idx-dclear.xwd"; d3="$ROOT/adaptive-$round-$idx-d3.xwd"

    capture_xwd "$d0"; sleep .18; capture_xwd "$d1"; sleep .18; capture_xwd "$d2"
    xdo type --window "$UI_WIN" --delay 10 -- 'wmprobe7'
    sleep .20; capture_xwd "$dtyped"
    xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
    sleep .20; capture_xwd "$dclear"; sleep .20; capture_xwd "$d3"

    set +e
    discover="$(python3 "$COMPARE" controlled-cycle \
      "$d0" "$d1" "$d2" "$dtyped" "$dclear" "$d3" \
      --min-signal 25 --min-overlap-ratio 0.55 \
      --max-width 500 --max-height 120 --max-area 30000 2>&1)"
    discover_rc=$?
    set -e
    dnoise="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_NOISE_PIXELS=/{print $2}' <<<"$discover" | tail -1)"
    dsignal="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_SIGNAL_CHANGED=/{print $2}' <<<"$discover" | tail -1)"
    doverlap="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_OVERLAP_RATIO=/{print $2}' <<<"$discover" | tail -1)"
    dbbox="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_SIGNAL_BBOX=/{print $2}' <<<"$discover" | tail -1)"
    dresidual="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_RESIDUAL_CHANGED=/{print $2}' <<<"$discover" | tail -1)"
    [[ "$dnoise" =~ ^[0-9]+$ && "$dsignal" =~ ^[0-9]+$ && "$dresidual" =~ ^[0-9]+$ ]] || fail adaptive_discovery_count_invalid
    [[ "$doverlap" =~ ^0\.[0-9]+$|^1\.000000$ ]] || fail adaptive_discovery_overlap_invalid
    echo "WORLDMAP_PRELOGIN_ADAPTIVE_DISCOVERY=round:$round;tab:$idx;noise:$dnoise;signal:$dsignal;overlap:$doverlap;bbox:$dbbox;residual:$dresidual;pass:$([[ $discover_rc -eq 0 ]] && echo true || echo false)"

    rm -f "$d0" "$d1" "$d2" "$dtyped" "$dclear" "$d3"

    if [[ $discover_rc -eq 0 ]]; then
      LOCAL_CANDIDATES=$((LOCAL_CANDIDATES+1))
      # Same launch and same focus state: classify text semantics immediately,
      # before the Tab key advances to any other control.
      s0="$ROOT/adaptive-$round-$idx-s0.xwd"; s1="$ROOT/adaptive-$round-$idx-s1.xwd"; s2="$ROOT/adaptive-$round-$idx-s2.xwd"
      short="$ROOT/adaptive-$round-$idx-short.xwd"; sclear="$ROOT/adaptive-$round-$idx-sclear.xwd"
      long="$ROOT/adaptive-$round-$idx-long.xwd"; lclear="$ROOT/adaptive-$round-$idx-lclear.xwd"; s3="$ROOT/adaptive-$round-$idx-s3.xwd"

      xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
      sleep .18; capture_xwd "$s0"; sleep .18; capture_xwd "$s1"; sleep .18; capture_xwd "$s2"
      xdo type --window "$UI_WIN" --delay 10 -- 'abc'
      sleep .20; capture_xwd "$short"
      xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
      sleep .20; capture_xwd "$sclear"
      xdo type --window "$UI_WIN" --delay 10 -- 'abcdefghijklm'
      sleep .20; capture_xwd "$long"
      xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
      sleep .20; capture_xwd "$lclear"; sleep .20; capture_xwd "$s3"

      set +e
      semantic="$(python3 "$SEMANTICS" "$COMPARE" \
        "$s0" "$s1" "$s2" "$short" "$sclear" "$long" "$lclear" "$s3" 2>&1)"
      semantic_rc=$?
      set -e
      short_n="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_SHORT_SIGNAL=/{print $2}' <<<"$semantic" | tail -1)"
      long_n="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_LONG_SIGNAL=/{print $2}' <<<"$semantic" | tail -1)"
      growth="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_GROWTH_PIXELS=/{print $2}' <<<"$semantic" | tail -1)"
      ratio="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_GROWTH_RATIO=/{print $2}' <<<"$semantic" | tail -1)"
      sbbox="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_SHORT_BBOX=/{print $2}' <<<"$semantic" | tail -1)"
      lbbox="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_LONG_BBOX=/{print $2}' <<<"$semantic" | tail -1)"
      [[ "$short_n" =~ ^[0-9]+$ && "$long_n" =~ ^[0-9]+$ && "$growth" =~ ^[0-9]+$ ]] || fail adaptive_semantic_count_invalid
      echo "WORLDMAP_PRELOGIN_ADAPTIVE_SEMANTICS=round:$round;tab:$idx;short:$short_n;long:$long_n;growth:$growth;ratio:$ratio;short_bbox:$sbbox;long_bbox:$lbbox;pass:$([[ $semantic_rc -eq 0 ]] && echo true || echo false)"
      if [[ $semantic_rc -eq 0 ]]; then
        TEXT_FIELDS=$((TEXT_FIELDS+1))
        echo "WORLDMAP_PRELOGIN_ADAPTIVE_TEXT_FIELD=round:$round;tab:$idx;short:$short_n;long:$long_n;growth:$growth;ratio:$ratio;short_bbox:$sbbox;long_bbox:$lbbox"
      fi
      rm -f "$s0" "$s1" "$s2" "$short" "$sclear" "$long" "$lclear" "$s3"
    fi

    xdo key --window "$UI_WIN" --clearmodifiers Tab
    sleep .12
  done
}

scan_round 1
if [[ "$TEXT_FIELDS" -eq 0 ]]; then
  echo 'WORLDMAP_PRELOGIN_ADAPTIVE_FIRST_ROUND=no_text_field'
  sleep 20
  scan_round 2
fi

echo "WORLDMAP_PRELOGIN_ADAPTIVE_LOCAL_CANDIDATE_COUNT=$LOCAL_CANDIDATES"
echo "WORLDMAP_PRELOGIN_ADAPTIVE_TEXT_FIELD_COUNT=$TEXT_FIELDS"
echo 'WORLDMAP_PRELOGIN_ADAPTIVE_TEXT=COMPLETE_NO_SECRET'
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
    output = text[:cut] + TAIL

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
        'WORLDMAP_PRELOGIN_ADAPTIVE_TEXT_SECRET_ENV=ABSENT',
        'WORLDMAP_PRELOGIN_ADAPTIVE_TEXT_MODE=SAME_LAUNCH_DISCOVER_THEN_CLASSIFY',
        'WORLDMAP_PRELOGIN_ADAPTIVE_DISCOVERY=',
        'WORLDMAP_PRELOGIN_ADAPTIVE_SEMANTICS=',
        'WORLDMAP_PRELOGIN_ADAPTIVE_TEXT_FIELD=',
        'WORLDMAP_PRELOGIN_ADAPTIVE_TEXT_FIELD_COUNT=',
        'WORLDMAP_PRELOGIN_ADAPTIVE_TEXT=COMPLETE_NO_SECRET',
        'controlled-cycle',
        'track-a-worldmap-causal-xwd-text-semantics.py',
        "'wmprobe7'",
        "'abc'",
        "'abcdefghijklm'",
        'if [[ $discover_rc -eq 0 ]]; then',
        'xdo key --window "$UI_WIN" --clearmodifiers Tab',
        'if [[ "$TEXT_FIELDS" -eq 0 ]]; then',
        'sleep 20',
        'exit 0',
    )
    missing = [token for token in required if token not in output]
    if missing:
        raise TransformRefused("REQUIRED_MISSING:" + ",".join(missing))
    return output


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    a = p.parse_args()
    try:
        out = transform(a.source.read_text(encoding="utf-8"))
    except TransformRefused as exc:
        print(f"WORLDMAP_PRELOGIN_ADAPTIVE_TEXT_REPAIR_REFUSED={exc}")
        return 44
    a.output.write_text(out, encoding="utf-8")
    a.output.chmod(0o700)
    print("WORLDMAP_PRELOGIN_ADAPTIVE_TEXT_REPAIR=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
