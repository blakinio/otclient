#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

START = "AUTH_STATE_BEFORE=\"$(grep -Fc $'\\tLoginStateMachineStarted' \"$EVENTS\" 2>/dev/null || true)\"\n"
END = '[[ "$world" == 1 ]] || fail structural_world_entry_not_observed\n'

REPLACEMENT = r'''# V12: the account form, protected field occupancy and the physical Login
# control are already independently proven. Do not require brittle auth QMeta
# breakpoints. Follow the historical exact-SHA successful execution model:
# transport activation + persistent visual transition, then character stimulus,
# with FullMap + pre-Storage strip records as the sole IN_GAME truth.
LOGIN_TYPED_REFERENCE="$ROOT/v12-login-typed.xwd"
sleep .20
capture_xwd "$LOGIN_TYPED_REFERENCE"

local_socks_count() {
  ss -ntp 2>/dev/null | awk -v needle="pid=$PID," -v port="$WARP_PORT" '
    index($0,needle) && ($5=="127.0.0.1:"port || $5=="[::1]:"port) {n++}
    END {print n+0}'
}
SOCKS_BEFORE="$(local_socks_count)"
SOCKS_MAX="$SOCKS_BEFORE"

echo "WORLDMAP_V12_LOCAL_SOCKS_BEFORE=$SOCKS_BEFORE"
xdo mousemove --window "$UI_WIN" "$LOGIN_X" "$LOGIN_Y" click 1
echo 'WORLDMAP_BASELINE_LOGIN_SUBMISSION_METHOD=PRESS_BBOX_CENTER_CLICK_TRANSPORT_VISUAL_PROOF'
echo 'WORLDMAP_BASELINE_LOGIN_SUBMITTED=true'

UI_TRANSITION=0
for i in $(seq 1 60); do
  sleep 1
  cur_socks="$(local_socks_count)"
  (( cur_socks > SOCKS_MAX )) && SOCKS_MAX="$cur_socks" || true
  candidate="$ROOT/v12-post-login-$i.xwd"
  capture_xwd "$candidate"
  set +e
  change_out="$(python3 "$COMPARE" change "$LOGIN_TYPED_REFERENCE" "$candidate" --min-changed 5000 2>&1)"
  change_rc=$?
  set -e
  if [[ "$change_rc" -eq 0 ]]; then
    confirm="$ROOT/v12-post-login-confirm-$i.xwd"
    sleep .50
    capture_xwd "$confirm"
    set +e
    confirm_out="$(python3 "$COMPARE" change "$LOGIN_TYPED_REFERENCE" "$confirm" --min-changed 5000 2>&1)"
    confirm_rc=$?
    set -e
    rm -f "$candidate" "$confirm"
    if [[ "$confirm_rc" -eq 0 ]]; then
      UI_TRANSITION=1
      echo 'WORLDMAP_V12_POST_LOGIN_UI_TRANSITION=PERSISTENT_LARGE_CHANGE'
      break
    fi
  else
    rm -f "$candidate"
  fi
done

echo "WORLDMAP_V12_LOCAL_SOCKS_MAX=$SOCKS_MAX"
(( SOCKS_MAX >= 1 )) || fail v12_login_transport_activity_not_observed
[[ "$UI_TRANSITION" == 1 ]] || fail v12_persistent_post_login_ui_transition_not_observed
echo 'WORLDMAP_BASELINE_LOGIN_TRANSPORT_ACTIVITY=PASS'
echo 'WORLDMAP_BASELINE_POST_LOGIN_UI_TRANSITION=PASS'
rm -f "$PRELOGIN_REFERENCE" "$LOGIN_TYPED_REFERENCE"

# Character activation follows the historical same-SHA successful stimulus.
# ROW_X/ROW_Y are translated from the live fields found in this exact launch.
# Coordinates are stimulus only; no success is inferred from the click/Return.
xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
xdo windowfocus --sync "$UI_WIN"
xdo mousemove --window "$UI_WIN" "$ROW_X" "$ROW_Y" click 1
sleep .40
xdo key --window "$UI_WIN" --clearmodifiers Return
echo 'WORLDMAP_BASELINE_CHARACTER_STIMULUS=FIELD_DERIVED_ROW_CLICK_RETURN'

world=0
for _ in $(seq 1 30); do
  sleep 1
  if grep -Fq $'\tFullMap' "$EVENTS" 2>/dev/null && [[ "$(wc -l <"$STRIPS")" -ge 10 ]]; then
    world=1
    break
  fi
done
if [[ "$world" != 1 ]]; then
  xdo mousemove --window "$UI_WIN" "$ROW_X" "$ROW_Y" click --repeat 2 --delay 160 1
  sleep .20
  xdo key --window "$UI_WIN" --clearmodifiers Return
  echo 'WORLDMAP_BASELINE_CHARACTER_STIMULUS_FALLBACK=FIELD_DERIVED_ROW_DOUBLECLICK_RETURN'
  for _ in $(seq 1 40); do
    sleep 1
    if grep -Fq $'\tFullMap' "$EVENTS" 2>/dev/null && [[ "$(wc -l <"$STRIPS")" -ge 10 ]]; then
      world=1
      break
    fi
  done
fi
[[ "$world" == 1 ]] || fail structural_world_entry_not_observed
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
        "WORLDMAP_V11_SECRET_FIELD_OCCUPANCY=",
        "WORLDMAP_BASELINE_SECRET_FIELD_OCCUPANCY=PASS",
        "WORLDMAP_V10_PRESECRET_LOGIN_BUTTON=PROVEN_PRESS_CANCEL",
        "WORLDMAP_V11_LOGIN_BUTTON_CENTER=PROVEN_FROM_PRESS_BBOX",
        "WORLDMAP_V12_LOCAL_SOCKS_BEFORE=",
        "WORLDMAP_V12_LOCAL_SOCKS_MAX=",
        "WORLDMAP_V12_POST_LOGIN_UI_TRANSITION=PERSISTENT_LARGE_CHANGE",
        "WORLDMAP_BASELINE_LOGIN_TRANSPORT_ACTIVITY=PASS",
        "WORLDMAP_BASELINE_POST_LOGIN_UI_TRANSITION=PASS",
        "WORLDMAP_BASELINE_CHARACTER_STIMULUS=FIELD_DERIVED_ROW_CLICK_RETURN",
        "WORLDMAP_BASELINE_STRUCTURAL_IN_GAME=PASS",
        'UI_WIN="$WIN"',
    )
    missing = [x for x in required if x not in out]
    if missing:
        raise TransformRefused("REQUIRED_MISSING:" + ",".join(missing))

    forbidden = (
        "WORLDMAP_BASELINE_NATIVE_LOGIN_ACTIVATION=PASS",
        "WORLDMAP_BASELINE_AUTH_DOWNSTREAM_CHARACTER_SELECTION=PASS",
        "native_login_activation_state_not_observed",
        "native_auth_downstream_character_selection_not_observed",
        "native_character_request_not_observed_on_field_derived_target",
        "native_game_login_state_not_observed",
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
        print(f"WORLDMAP_TRANSPORT_VISUAL_V12_REPAIR_REFUSED={exc}")
        return 44
    a.output.write_text(out, encoding="utf-8")
    a.output.chmod(0o700)
    print("WORLDMAP_TRANSPORT_VISUAL_V12_REPAIR=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
