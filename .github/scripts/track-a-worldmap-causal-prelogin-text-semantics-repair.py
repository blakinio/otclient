#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

SECRET_REQUIRE = '[[ -n "${TIBIA_TEST_EMAIL:-}" && -n "${TIBIA_TEST_PASSWORD:-}" ]] || fail protected_login_secrets_missing\n'
SECRET_ABSENT = '[[ -z "${TIBIA_TEST_EMAIL:-}" && -z "${TIBIA_TEST_PASSWORD:-}" ]] || fail prelogin_text_semantics_secret_env_present\n'
TOOLING_MARKER = "echo 'WORLDMAP_BASELINE_LOGIN_UI_TOOLING=RAW_XWD_AGGREGATE_BEHAVIOR_PASS'\n"

TAIL = r'''
echo 'WORLDMAP_PRELOGIN_TEXT_SEMANTICS_SECRET_ENV=ABSENT'
echo 'WORLDMAP_PRELOGIN_TEXT_SEMANTICS_TARGETS=tab2,tab3,tab5'
SEMANTICS="${GITHUB_WORKSPACE:-$PWD}/.github/scripts/track-a-worldmap-causal-xwd-text-semantics.py"
[[ -f "$SEMANTICS" ]] || fail text_semantics_helper_missing
TEXT_FIELDS=0
xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
xdo windowfocus --sync "$UI_WIN"

for idx in $(seq 0 5); do
  if [[ "$idx" == 2 || "$idx" == 3 || "$idx" == 5 ]]; then
    prefix="$ROOT/text-$idx"
    idle0="$prefix-idle0.xwd"; idle1="$prefix-idle1.xwd"; idle2="$prefix-idle2.xwd"
    short="$prefix-short.xwd"; clear_short="$prefix-clear-short.xwd"
    long="$prefix-long.xwd"; clear_long="$prefix-clear-long.xwd"; idle3="$prefix-idle3.xwd"

    xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
    sleep .18; capture_xwd "$idle0"
    sleep .18; capture_xwd "$idle1"
    sleep .18; capture_xwd "$idle2"
    xdo type --window "$UI_WIN" --delay 10 -- 'abc'
    sleep .20; capture_xwd "$short"
    xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
    sleep .20; capture_xwd "$clear_short"
    xdo type --window "$UI_WIN" --delay 10 -- 'abcdefghijklm'
    sleep .20; capture_xwd "$long"
    xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
    sleep .20; capture_xwd "$clear_long"
    sleep .20; capture_xwd "$idle3"

    set +e
    probe="$(python3 "$SEMANTICS" "$COMPARE" "$idle0" "$idle1" "$idle2" "$short" "$clear_short" "$long" "$clear_long" "$idle3" 2>&1)"
    rc=$?
    set -e
    short_n="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_SHORT_SIGNAL=/{print $2}' <<<"$probe" | tail -1)"
    long_n="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_LONG_SIGNAL=/{print $2}' <<<"$probe" | tail -1)"
    growth="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_GROWTH_PIXELS=/{print $2}' <<<"$probe" | tail -1)"
    ratio="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_GROWTH_RATIO=/{print $2}' <<<"$probe" | tail -1)"
    sbbox="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_SHORT_BBOX=/{print $2}' <<<"$probe" | tail -1)"
    lbbox="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_LONG_BBOX=/{print $2}' <<<"$probe" | tail -1)"
    echo "WORLDMAP_PRELOGIN_TEXT_SEMANTICS_METRIC=tab:$idx;short:$short_n;long:$long_n;growth:$growth;ratio:$ratio;short_bbox:$sbbox;long_bbox:$lbbox;pass:$([[ $rc -eq 0 ]] && echo true || echo false)"
    if [[ $rc -eq 0 ]]; then
      TEXT_FIELDS=$((TEXT_FIELDS+1))
      echo "WORLDMAP_PRELOGIN_TEXT_FIELD_CANDIDATE=tab:$idx;short:$short_n;long:$long_n;growth:$growth;ratio:$ratio;short_bbox:$sbbox;long_bbox:$lbbox"
    fi
    rm -f "$idle0" "$idle1" "$idle2" "$short" "$clear_short" "$long" "$clear_long" "$idle3"
  fi
  xdo key --window "$UI_WIN" --clearmodifiers Tab
  sleep .12
done

echo "WORLDMAP_PRELOGIN_TEXT_FIELD_CANDIDATE_COUNT=$TEXT_FIELDS"
echo 'WORLDMAP_PRELOGIN_TEXT_SEMANTICS=COMPLETE_NO_SECRET'
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
        'printf \'%s\' "$TIBIA_TEST_EMAIL"', 'printf \'%s\' "$TIBIA_TEST_PASSWORD"',
        'WORLDMAP_BASELINE_LOGIN_SUBMITTED=true', 'WORLDMAP_BASELINE_CHARACTER_ACTIVATION_SENT=true',
        'WORLDMAP_BASELINE_RIGHT_SENT=true', 'WORLDMAP_BASELINE_LEFT_SENT=true',
    )
    survivors=[x for x in forbidden if x in output]
    if survivors:
        raise TransformRefused('SECRET_OR_GAMEPLAY_SURVIVORS:'+','.join(survivors))
    required=(
        'WORLDMAP_PRELOGIN_TEXT_SEMANTICS_SECRET_ENV=ABSENT',
        'WORLDMAP_PRELOGIN_TEXT_SEMANTICS_TARGETS=tab2,tab3,tab5',
        'track-a-worldmap-causal-xwd-text-semantics.py', "'abc'", "'abcdefghijklm'",
        'WORLDMAP_PRELOGIN_TEXT_FIELD_CANDIDATE=', 'WORLDMAP_PRELOGIN_TEXT_FIELD_CANDIDATE_COUNT=',
        'WORLDMAP_PRELOGIN_TEXT_SEMANTICS=COMPLETE_NO_SECRET', 'exit 0',
    )
    missing=[x for x in required if x not in output]
    if missing:
        raise TransformRefused('REQUIRED_MISSING:'+','.join(missing))
    return output

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('source',type=Path); p.add_argument('output',type=Path); a=p.parse_args()
    try: out=transform(a.source.read_text())
    except TransformRefused as e:
        print(f'WORLDMAP_PRELOGIN_TEXT_SEMANTICS_REPAIR_REFUSED={e}'); return 44
    a.output.write_text(out); a.output.chmod(0o700)
    print('WORLDMAP_PRELOGIN_TEXT_SEMANTICS_REPAIR=PASS'); return 0

if __name__=='__main__': raise SystemExit(main())
