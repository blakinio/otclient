#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

SECRET_REQUIRE = '[[ -n "${TIBIA_TEST_EMAIL:-}" && -n "${TIBIA_TEST_PASSWORD:-}" ]] || fail protected_login_secrets_missing\n'
SECRET_ABSENT = '[[ -z "${TIBIA_TEST_EMAIL:-}" && -z "${TIBIA_TEST_PASSWORD:-}" ]] || fail adaptive_field_scan_secret_env_present\n'
TOOLING_MARKER = "echo 'WORLDMAP_BASELINE_LOGIN_UI_TOOLING=RAW_XWD_AGGREGATE_BEHAVIOR_PASS'\n"

TAIL = r'''
echo 'WORLDMAP_ADAPTIVE_FIELD_SCAN_SECRET_ENV=ABSENT'
echo 'WORLDMAP_ADAPTIVE_FIELD_SCAN_MODE=SAME_LAUNCH_DISCOVER_TEXT_AND_VARIANT'
TEXT_SEM="${GITHUB_WORKSPACE:-$PWD}/.github/scripts/track-a-worldmap-causal-xwd-text-semantics.py"
VARIANT="${GITHUB_WORKSPACE:-$PWD}/.github/scripts/track-a-worldmap-causal-text-variant-classify.py"
[[ -f "$TEXT_SEM" && -f "$VARIANT" ]] || fail adaptive_field_semantics_helper_missing

FIELDS=0
MASKED=0
UNMASKED=0
AMBIGUOUS=0

capture_semantics() {
  local prefix="$1" short_text="$2" long_text="$3"
  local idle0="$ROOT/$prefix-idle0.xwd" idle1="$ROOT/$prefix-idle1.xwd" idle2="$ROOT/$prefix-idle2.xwd"
  local short="$ROOT/$prefix-short.xwd" clear_short="$ROOT/$prefix-clear-short.xwd"
  local long="$ROOT/$prefix-long.xwd" clear_long="$ROOT/$prefix-clear-long.xwd" idle3="$ROOT/$prefix-idle3.xwd"
  capture_xwd "$idle0"; sleep .18; capture_xwd "$idle1"; sleep .18; capture_xwd "$idle2"
  xdo type --window "$UI_WIN" --delay 10 -- "$short_text"; sleep .20; capture_xwd "$short"
  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace; sleep .20; capture_xwd "$clear_short"
  xdo type --window "$UI_WIN" --delay 10 -- "$long_text"; sleep .20; capture_xwd "$long"
  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace; sleep .20; capture_xwd "$clear_long"
  sleep .20; capture_xwd "$idle3"
  set +e
  SEM_OUT="$(python3 "$TEXT_SEM" "$COMPARE" "$idle0" "$idle1" "$idle2" "$short" "$clear_short" "$long" "$clear_long" "$idle3" 2>&1)"
  SEM_RC=$?
  set -e
  rm -f "$idle0" "$idle1" "$idle2" "$short" "$clear_short" "$long" "$clear_long" "$idle3"
}

xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
xdo windowfocus --sync "$UI_WIN"

for idx in $(seq 0 15); do
  # Stage 1: prove this exact focus state is a real local text field by requiring
  # causal rendering growth from a short to a much longer string.
  capture_semantics "adaptive-$idx-text" 'abc' 'abcdefghijklm'
  if [[ "$SEM_RC" -eq 0 ]]; then
    text_bbox="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_LONG_BBOX=/{print $2}' <<<"$SEM_OUT" | tail -1)"
    text_signal="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_LONG_SIGNAL=/{print $2}' <<<"$SEM_OUT" | tail -1)"
    [[ "$text_bbox" =~ ^[0-9]+,[0-9]+,[0-9]+,[0-9]+$ && "$text_signal" =~ ^[0-9]+$ ]] || fail adaptive_text_metric_invalid
    FIELDS=$((FIELDS+1))

    # Stage 2: without leaving the same focus state, compare two equal-length
    # strings whose proportional glyph widths should diverge only when text is
    # rendered unmasked. Both strings are immediately cleared.
    capture_semantics "adaptive-$idx-variant" 'iiiiii' 'WWWWWW'
    i_bbox="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_SHORT_BBOX=/{print $2}' <<<"$SEM_OUT" | tail -1)"
    w_bbox="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_LONG_BBOX=/{print $2}' <<<"$SEM_OUT" | tail -1)"
    i_signal="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_SHORT_SIGNAL=/{print $2}' <<<"$SEM_OUT" | tail -1)"
    w_signal="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_LONG_SIGNAL=/{print $2}' <<<"$SEM_OUT" | tail -1)"
    [[ "$i_signal" =~ ^[0-9]+$ && "$w_signal" =~ ^[0-9]+$ ]] || fail adaptive_variant_metric_invalid
    variant_out="$(python3 "$VARIANT" "$i_bbox" "$w_bbox" "$i_signal" "$w_signal")" || fail adaptive_variant_classifier_failed
    variant_class="$(awk -F= '/^WORLDMAP_TEXT_VARIANT_CLASS=/{print $2}' <<<"$variant_out" | tail -1)"
    ratio="$(awk -F= '/^WORLDMAP_TEXT_VARIANT_WIDTH_RATIO=/{print $2}' <<<"$variant_out" | tail -1)"
    case "$variant_class" in
      MASKED_LIKE) MASKED=$((MASKED+1)) ;;
      UNMASKED_LIKE) UNMASKED=$((UNMASKED+1)) ;;
      AMBIGUOUS) AMBIGUOUS=$((AMBIGUOUS+1)) ;;
      *) fail adaptive_variant_class_invalid ;;
    esac
    echo "WORLDMAP_ADAPTIVE_TEXT_FIELD=tab:$idx;bbox:$text_bbox;signal:$text_signal;variant:$variant_class;width_ratio:$ratio"
  fi
  xdo key --window "$UI_WIN" --clearmodifiers Tab
  sleep .12
done

echo "WORLDMAP_ADAPTIVE_TEXT_FIELD_COUNT=$FIELDS"
echo "WORLDMAP_ADAPTIVE_MASKED_LIKE_COUNT=$MASKED"
echo "WORLDMAP_ADAPTIVE_UNMASKED_LIKE_COUNT=$UNMASKED"
echo "WORLDMAP_ADAPTIVE_AMBIGUOUS_COUNT=$AMBIGUOUS"
echo 'WORLDMAP_ADAPTIVE_FIELD_SCAN=COMPLETE_NO_SECRET'
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
    survivors = [t for t in forbidden if t in output]
    if survivors:
        raise TransformRefused('SECRET_OR_GAMEPLAY_SURVIVORS:' + ','.join(survivors))
    required = (
        'adaptive_field_scan_secret_env_present', 'WORLDMAP_ADAPTIVE_FIELD_SCAN_SECRET_ENV=ABSENT',
        'WORLDMAP_ADAPTIVE_FIELD_SCAN_MODE=SAME_LAUNCH_DISCOVER_TEXT_AND_VARIANT',
        'track-a-worldmap-causal-xwd-text-semantics.py', 'track-a-worldmap-causal-text-variant-classify.py',
        "'abc'", "'abcdefghijklm'", "'iiiiii'", "'WWWWWW'",
        'WORLDMAP_ADAPTIVE_TEXT_FIELD=', 'WORLDMAP_ADAPTIVE_FIELD_SCAN=COMPLETE_NO_SECRET', 'exit 0',
    )
    missing = [t for t in required if t not in output]
    if missing:
        raise TransformRefused('REQUIRED_MISSING:' + ','.join(missing))
    return output

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('source',type=Path); p.add_argument('output',type=Path); a=p.parse_args()
    try: out=transform(a.source.read_text(encoding='utf-8'))
    except TransformRefused as exc:
        print(f'WORLDMAP_ADAPTIVE_FIELD_SCAN_REPAIR_REFUSED={exc}'); return 44
    a.output.write_text(out,encoding='utf-8'); a.output.chmod(0o700)
    print('WORLDMAP_ADAPTIVE_FIELD_SCAN_REPAIR=PASS'); return 0

if __name__ == '__main__':
    raise SystemExit(main())
