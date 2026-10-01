#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

START = "# Character activation follows the historical same-SHA successful stimulus.\n"
END = '[[ "$world" == 1 ]] || fail structural_world_entry_not_observed\n'

REPLACEMENT = r'''# V14: account Login is already proven by local SOCKS activity plus a persistent
# post-login UI transition. Resolve character activation causally: bounded UI
# stimuli are allowed, but only native RequestCharacterLogin or direct FullMap
# may select the winning candidate.
REQUEST_BEFORE="$(grep -Fc $'\tRequestCharacterLogin' "$EVENTS" 2>/dev/null || true)"
CHARACTER_REQUEST=0
world=0
ACTIVATION_METHOD='NONE'

fullmap_ready() {
  grep -Fq $'\tFullMap' "$EVENTS" 2>/dev/null && [[ "$(wc -l <"$STRIPS")" -ge 10 ]]
}

request_count() {
  grep -Fc $'\tRequestCharacterLogin' "$EVENTS" 2>/dev/null || true
}

check_activation() {
  local label="$1"
  for _ in $(seq 1 12); do
    sleep .25
    if fullmap_ready; then
      world=1
      ACTIVATION_METHOD="FULLMAP_DIRECT_AFTER_${label}"
      echo "WORLDMAP_V14_CHARACTER_ACTIVATION=${ACTIVATION_METHOD}"
      return 0
    fi
    local cur
    cur="$(request_count)"
    if (( cur > REQUEST_BEFORE )); then
      CHARACTER_REQUEST=1
      ACTIVATION_METHOD="$label"
      echo "WORLDMAP_V14_CHARACTER_REQUEST_COUNT_DELTA=$((cur-REQUEST_BEFORE))"
      echo "WORLDMAP_V14_CHARACTER_ACTIVATION=${ACTIVATION_METHOD}"
      echo 'WORLDMAP_BASELINE_NATIVE_CHARACTER_REQUEST=PASS'
      return 0
    fi
  done
  return 1
}

xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
xdo windowfocus --sync "$UI_WIN"

echo 'WORLDMAP_V14_CHARACTER_ATTEMPT=RETURN_ONLY'
xdo key --window "$UI_WIN" --clearmodifiers Return
check_activation RETURN_ONLY || true

if [[ "$CHARACTER_REQUEST" != 1 && "$world" != 1 ]]; then
  for spec in \
    'CENTER_735_408:735:408' \
    'UP_735_384:735:384' \
    'DOWN_735_432:735:432' \
    'RIGHT_785_408:785:408' \
    'LEGACY_TRANSLATED_685_408:685:408'; do
    IFS=: read -r label tx ty <<<"$spec"
    (( tx >= 20 && tx < ACTUAL_WIDTH-20 && ty >= 20 && ty < ACTUAL_HEIGHT-20 )) || fail v14_character_candidate_oob
    echo "WORLDMAP_V14_CHARACTER_ATTEMPT=$label@$tx,$ty"
    xdo mousemove --window "$UI_WIN" "$tx" "$ty" click 1
    sleep .20
    xdo key --window "$UI_WIN" --clearmodifiers Return
    check_activation "$label" && break || true
  done
fi

if [[ "$CHARACTER_REQUEST" != 1 && "$world" != 1 ]]; then
  echo 'WORLDMAP_V14_CHARACTER_ATTEMPT=DOUBLECLICK_CENTER_735_408'
  xdo mousemove --window "$UI_WIN" 735 408 click --repeat 2 --delay 160 1
  sleep .20
  xdo key --window "$UI_WIN" --clearmodifiers Return
  check_activation DOUBLECLICK_CENTER_735_408 || true
fi

[[ "$CHARACTER_REQUEST" == 1 || "$world" == 1 ]] || fail native_character_request_not_observed_after_bounded_v14_candidates

if [[ "$world" != 1 ]]; then
  # Once the native request is observed, stop stimulating the UI and allow the
  # normal client state machine to connect to the game server and deliver map.
  for _ in $(seq 1 120); do
    sleep .5
    if fullmap_ready; then world=1; break; fi
  done
fi
[[ "$world" == 1 ]] || fail structural_world_entry_not_observed_after_native_character_request
'''


class TransformRefused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(START) != 1:
        raise TransformRefused(f"START_COUNT:{text.count(START)}")
    start = text.index(START)
    end = text.find(END, start)
    if end < 0:
        raise TransformRefused("END_MISSING")
    end += len(END)
    out = text[:start] + REPLACEMENT + text[end:]

    required = (
        "WORLDMAP_BASELINE_LOGIN_TRANSPORT_ACTIVITY=PASS",
        "WORLDMAP_BASELINE_POST_LOGIN_UI_TRANSITION=PASS",
        "WORLDMAP_V14_CHARACTER_ATTEMPT=RETURN_ONLY",
        "WORLDMAP_V14_CHARACTER_ATTEMPT=$label@$tx,$ty",
        "WORLDMAP_BASELINE_NATIVE_CHARACTER_REQUEST=PASS",
        "WORLDMAP_V14_CHARACTER_ACTIVATION=",
        "native_character_request_not_observed_after_bounded_v14_candidates",
        "structural_world_entry_not_observed_after_native_character_request",
        "WORLDMAP_BASELINE_STRUCTURAL_IN_GAME=PASS",
        'UI_WIN="$WIN"',
    )
    missing = [x for x in required if x not in out]
    if missing:
        raise TransformRefused("REQUIRED_MISSING:" + ",".join(missing))

    forbidden = (
        "WORLDMAP_BASELINE_CHARACTER_STIMULUS=FIELD_DERIVED_ROW_CLICK_RETURN",
        "WORLDMAP_BASELINE_CHARACTER_STIMULUS_FALLBACK=FIELD_DERIVED_ROW_DOUBLECLICK_RETURN",
        "structural_world_entry_not_observed\n",
        '"$XWD" -root',
        "xwd -root",
        "xrandr --output",
        "wmctrl -r",
    )
    survivors = [x for x in forbidden if x in out]
    if survivors:
        raise TransformRefused("FORBIDDEN_SURVIVORS:" + ",".join(survivors))
    if out.count('UI_WIN="$WIN"') != 1:
        raise TransformRefused("MANIFEST_WINDOW_IDENTITY_NOT_UNIQUE")
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    a = p.parse_args()
    try:
        out = transform(a.source.read_text(encoding="utf-8"))
    except TransformRefused as exc:
        print(f"WORLDMAP_CHARACTER_ACTIVATION_V14_REPAIR_REFUSED={exc}")
        return 44
    a.output.write_text(out, encoding="utf-8")
    a.output.chmod(0o700)
    print("WORLDMAP_CHARACTER_ACTIVATION_V14_REPAIR=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
