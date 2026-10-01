#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

PRE_START = "# V9 pre-secret geometry parity:"
PRE_END = "echo 'WORLDMAP_V9_PRESECRET_LOGIN_BUTTON=PROVEN'\n"
POST_START = "# V9: account auth is already proven by uploader-success and login-finished events.\n"
POST_END = "world=0\n"

PRE_REPLACEMENT = r'''# V10 pre-secret locator: derive the historical-target translation from the
# two fields physically rediscovered in this exact launch, then prove the Login
# control with a reversible mouse press cancelled outside the candidate control.
# No protected credential is present and no click/release occurs inside it.
DX_EMAIL=$((EMAIL_X-535)); DY_EMAIL=$((EMAIL_Y-275))
DX_PASS=$((PASS_X-535)); DY_PASS=$((PASS_Y-304))
abs() { local v="$1"; (( v < 0 )) && echo $((-v)) || echo "$v"; }
(( $(abs $((DX_EMAIL-DX_PASS))) <= 60 )) || fail v10_field_translation_x_inconsistent
(( $(abs $((DY_EMAIL-DY_PASS))) <= 20 )) || fail v10_field_translation_y_inconsistent
SURFACE_DX=$(((DX_EMAIL+DX_PASS)/2)); SURFACE_DY=$(((DY_EMAIL+DY_PASS)/2))
PRED_LOGIN_X=$((590+SURFACE_DX)); PRED_LOGIN_Y=$((388+SURFACE_DY))
ROW_X=$((285+SURFACE_DX)); ROW_Y=$((193+SURFACE_DY))
(( PRED_LOGIN_X >= 40 && PRED_LOGIN_X < ACTUAL_WIDTH-40 && PRED_LOGIN_Y >= 40 && PRED_LOGIN_Y < ACTUAL_HEIGHT-40 )) || fail v10_predicted_login_target_oob
(( ROW_X >= 20 && ROW_X < ACTUAL_WIDTH-20 && ROW_Y >= 20 && ROW_Y < ACTUAL_HEIGHT-20 )) || fail v10_predicted_character_target_oob
echo "WORLDMAP_V10_FIELD_DERIVED_TRANSLATION=$SURFACE_DX,$SURFACE_DY"
echo "WORLDMAP_V10_PREDICTED_LOGIN_TARGET=$PRED_LOGIN_X,$PRED_LOGIN_Y"
echo "WORLDMAP_V10_PREDICTED_CHARACTER_TARGET=$ROW_X,$ROW_Y"
echo 'WORLDMAP_V10_FIELD_DERIVED_TRANSLATION=PASS'

SCAN_AUTH_BEFORE="$(grep -Fc $'\tLoginStateMachineStarted' "$EVENTS" 2>/dev/null || true)"
LOGIN_BUTTON_PROVEN=0
attempt=0
for yoff in 0 -20 20; do
  for xoff in 0 -40 40 -80 80 -120 120; do
    attempt=$((attempt+1)); tx=$((PRED_LOGIN_X+xoff)); ty=$((PRED_LOGIN_Y+yoff))
    (( tx >= 30 && tx < ACTUAL_WIDTH-30 && ty >= 30 && ty < ACTUAL_HEIGHT-30 )) || continue
    RX0=$((tx>140 ? tx-140 : 0)); RY0=$((ty>65 ? ty-65 : 0))
    RX1=$((tx+140<ACTUAL_WIDTH ? tx+140 : ACTUAL_WIDTH)); RY1=$((ty+65<ACTUAL_HEIGHT ? ty+65 : ACTUAL_HEIGHT))
    I0="$ROOT/v10-$attempt-idle0.xwd"; I1="$ROOT/v10-$attempt-idle1.xwd"
    PR="$ROOT/v10-$attempt-pressed.xwd"; RL="$ROOT/v10-$attempt-released.xwd"
    xdo mousemove --window "$UI_WIN" 20 20
    sleep .16; capture_xwd "$I0"; sleep .16; capture_xwd "$I1"
    xdo mousemove --window "$UI_WIN" "$tx" "$ty"
    sleep .08
    xdo mousedown --window "$UI_WIN" 1
    sleep .20; capture_xwd "$PR"
    xdo mousemove --window "$UI_WIN" 20 20
    sleep .08
    xdo mouseup --window "$UI_WIN" 1
    sleep .22; capture_xwd "$RL"
    set +e
    PRESS_OUT="$(python3 - "$COMPARE" "$I0" "$I1" "$PR" "$RL" "$RX0" "$RY0" "$RX1" "$RY1" <<'PY'
import importlib.util,sys
from pathlib import Path
compare,i0,i1,pressed,released,*box=sys.argv[1:]
roi=tuple(map(int,box))
spec=importlib.util.spec_from_file_location('wm_v10_press',compare)
if spec is None or spec.loader is None: raise SystemExit(3)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
i0=Path(i0);i1=Path(i1);pressed=Path(pressed);released=Path(released)
noise=m.changed_mask(i0,i1,roi)
down=m.changed_mask(i1,pressed,roi)-noise
up=m.changed_mask(pressed,released,roi)-noise
residual=m.changed_mask(i1,released,roi)-noise
signal=down&up
den=min(len(down),len(up)); overlap=len(signal)/den if den else 0.0
fields,_,_=m.load(i0);bw,bh,area=m.bbox_metrics(signal,fields['width'])
print('WORLDMAP_V10_PRESS_NOISE='+str(len(noise)))
print('WORLDMAP_V10_PRESS_DOWN='+str(len(down)))
print('WORLDMAP_V10_PRESS_UP='+str(len(up)))
print('WORLDMAP_V10_PRESS_SIGNAL='+str(len(signal)))
print('WORLDMAP_V10_PRESS_RESIDUAL='+str(len(residual)))
print(f'WORLDMAP_V10_PRESS_OVERLAP={overlap:.6f}')
print('WORLDMAP_V10_PRESS_BBOX='+m.mask_bbox(signal,fields['width']))
print(f'WORLDMAP_V10_PRESS_EXTENT={bw}x{bh};area={area}')
passed=len(signal)>=8 and overlap>=0.40 and len(residual)<=max(60,int(len(signal)*0.55)) and bw>0 and bh>0 and area<=60000
print('WORLDMAP_V10_PRESS_CANCEL='+('PASS' if passed else 'FAIL'))
raise SystemExit(0 if passed else 3)
PY
)"
    PRESS_RC=$?
    set -e
    rm -f "$I0" "$I1" "$PR" "$RL"
    printf '%s\n' "$PRESS_OUT"
    scan_auth_now="$(grep -Fc $'\tLoginStateMachineStarted' "$EVENTS" 2>/dev/null || true)"
    (( scan_auth_now == SCAN_AUTH_BEFORE )) || fail v10_press_cancel_unexpected_login_activation
    if [[ "$PRESS_RC" -eq 0 ]]; then
      LOGIN_X="$tx"; LOGIN_Y="$ty"; LOGIN_BUTTON_PROVEN=1
      echo "WORLDMAP_V10_LOGIN_BUTTON_TARGET=$LOGIN_X,$LOGIN_Y"
      echo 'WORLDMAP_V10_PRESECRET_LOGIN_BUTTON=PROVEN_PRESS_CANCEL'
      break 2
    fi
  done
done
[[ "$LOGIN_BUTTON_PROVEN" == 1 ]] || fail v10_login_button_press_cancel_unproven

# Secrets enter this helper only through the already-created mode-0600 FIFO,
'''

POST_REPLACEMENT = r'''# V10: account auth is already proven by uploader-success and login-finished
# events. Require native character-selection state before using the field-derived
# historical target. The target is stimulus only; RequestCharacterLogin is proof.
CHAR_STATE=0
for _ in $(seq 1 120); do
  sleep .25
  cur="$(grep -Fc $'\tShowCharacterSelection' "$EVENTS" 2>/dev/null || true)"
  if (( cur > CHAR_STATE_BEFORE )); then CHAR_STATE=1; break; fi
done
[[ "$CHAR_STATE" == 1 ]] || fail native_character_selection_state_not_observed_after_auth_success
echo 'WORLDMAP_BASELINE_NATIVE_CHARACTER_SELECTION_STATE=PASS'
rm -f "$PRELOGIN_REFERENCE"

CONFIRM_BEFORE="$(grep -Fc $'\tCharacterSelectionConfirmed' "$EVENTS" 2>/dev/null || true)"
REQUEST_BEFORE="$(grep -Fc $'\tRequestCharacterLogin' "$EVENTS" 2>/dev/null || true)"
xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
xdo windowfocus --sync "$UI_WIN"
xdo mousemove --window "$UI_WIN" "$ROW_X" "$ROW_Y" click 1
sleep .25
req="$(grep -Fc $'\tRequestCharacterLogin' "$EVENTS" 2>/dev/null || true)"
if (( req <= REQUEST_BEFORE )); then
  xdo key --window "$UI_WIN" --clearmodifiers Return
fi
CHAR_REQUEST=0
for _ in $(seq 1 28); do
  sleep .25
  req="$(grep -Fc $'\tRequestCharacterLogin' "$EVENTS" 2>/dev/null || true)"
  if (( req > REQUEST_BEFORE )); then CHAR_REQUEST=1; break; fi
done
if [[ "$CHAR_REQUEST" != 1 ]]; then
  xdo mousemove --window "$UI_WIN" "$ROW_X" "$ROW_Y" click --repeat 2 --delay 160 1
  xdo key --window "$UI_WIN" --clearmodifiers Return
  echo 'WORLDMAP_BASELINE_CHARACTER_ACTIVATION_FALLBACK=FIELD_DERIVED_ROW_DOUBLECLICK_RETURN'
  for _ in $(seq 1 40); do
    sleep .25
    req="$(grep -Fc $'\tRequestCharacterLogin' "$EVENTS" 2>/dev/null || true)"
    if (( req > REQUEST_BEFORE )); then CHAR_REQUEST=1; break; fi
  done
fi
[[ "$CHAR_REQUEST" == 1 ]] || fail native_character_request_not_observed_on_field_derived_target
confirm="$(grep -Fc $'\tCharacterSelectionConfirmed' "$EVENTS" 2>/dev/null || true)"
if (( confirm > CONFIRM_BEFORE )); then
  echo 'WORLDMAP_BASELINE_NATIVE_CHARACTER_SELECTION_CONFIRMED=PASS'
else
  echo 'WORLDMAP_BASELINE_NATIVE_CHARACTER_SELECTION_CONFIRMED=NOT_REQUIRED_REQUEST_PROVEN'
fi
echo 'WORLDMAP_BASELINE_CHARACTER_ACTIVATION_METHOD=FIELD_DERIVED_ROW_TARGET'
echo 'WORLDMAP_BASELINE_NATIVE_CHARACTER_REQUEST=PASS'

GAME_REQ_BEFORE="$(grep -Fc $'\tRequestCharacterGameserverLogin' "$EVENTS" 2>/dev/null || true)"
GAME_START_BEFORE="$(grep -Fc $'\tStartGameServerLogin' "$EVENTS" 2>/dev/null || true)"
GAME_REQ=0
for _ in $(seq 1 80); do
  sleep .25
  req="$(grep -Fc $'\tRequestCharacterGameserverLogin' "$EVENTS" 2>/dev/null || true)"
  start="$(grep -Fc $'\tStartGameServerLogin' "$EVENTS" 2>/dev/null || true)"
  if (( req > GAME_REQ_BEFORE && start > GAME_START_BEFORE )); then GAME_REQ=1; break; fi
done
[[ "$GAME_REQ" == 1 ]] || fail native_game_login_state_not_observed
echo 'WORLDMAP_BASELINE_NATIVE_GAME_LOGIN_STATE=PASS'

world=0
'''


class TransformRefused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(PRE_START) != 1:
        raise TransformRefused(f"PRE_START_COUNT:{text.count(PRE_START)}")
    ps = text.index(PRE_START)
    pe = text.find(PRE_END, ps)
    if pe < 0:
        raise TransformRefused("PRE_END_MISSING")
    pe += len(PRE_END)
    text = text[:ps] + PRE_REPLACEMENT + text[pe:]

    if text.count(POST_START) != 1:
        raise TransformRefused(f"POST_START_COUNT:{text.count(POST_START)}")
    ps = text.index(POST_START)
    pe = text.find(POST_END, ps)
    if pe < 0:
        raise TransformRefused("POST_END_MISSING")
    pe += len(POST_END)
    text = text[:ps] + POST_REPLACEMENT + text[pe:]

    text = text.replace(
        "WORLDMAP_BASELINE_LOGIN_SUBMISSION_METHOD=CENTER_TRANSLATED_BUTTON_CLICK",
        "WORLDMAP_BASELINE_LOGIN_SUBMISSION_METHOD=PRESS_CANCEL_PROVEN_BUTTON_CLICK",
    )

    required = (
        "WORLDMAP_V10_FIELD_DERIVED_TRANSLATION=PASS",
        "WORLDMAP_V10_PRESS_CANCEL=",
        "WORLDMAP_V10_PRESECRET_LOGIN_BUTTON=PROVEN_PRESS_CANCEL",
        "WORLDMAP_BASELINE_LOGIN_SUBMISSION_METHOD=PRESS_CANCEL_PROVEN_BUTTON_CLICK",
        "WORLDMAP_BASELINE_ACCOUNT_LOGIN_UPLOADER_SUCCESS=PASS",
        "WORLDMAP_BASELINE_LOGIN_FINISHED_SUCCESSFULLY=PASS",
        "WORLDMAP_BASELINE_NATIVE_CHARACTER_SELECTION_STATE=PASS",
        "WORLDMAP_BASELINE_NATIVE_CHARACTER_REQUEST=PASS",
        "WORLDMAP_BASELINE_NATIVE_GAME_LOGIN_STATE=PASS",
        "WORLDMAP_BASELINE_STRUCTURAL_IN_GAME=PASS",
        'UI_WIN="$WIN"',
    )
    missing = [x for x in required if x not in text]
    if missing:
        raise TransformRefused("REQUIRED_MISSING:" + ",".join(missing))

    forbidden = (
        "WORLDMAP_V9_LOGIN_BUTTON_HOVER=",
        "WORLDMAP_V9_PRESECRET_LOGIN_BUTTON=PROVEN",
        "CENTER_TRANSLATED_BUTTON_CLICK",
        "WORLDMAP_V9_CHARACTER_ROW_TARGET=",
        "PASSWORD_TAB_RETURN",
        "SELECT_X=",
        "SELECT_Y=",
        '"$XWD" -root',
        "xwd -root",
        "xrandr --output",
        "wmctrl -r",
    )
    survivors = [x for x in forbidden if x in text]
    if survivors:
        raise TransformRefused("FORBIDDEN_SURVIVORS:" + ",".join(survivors))
    if text.count('UI_WIN="$WIN"') != 1:
        raise TransformRefused("MANIFEST_WINDOW_IDENTITY_NOT_UNIQUE")
    return text


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    args = p.parse_args()
    try:
        out = transform(args.source.read_text(encoding="utf-8"))
    except TransformRefused as exc:
        print(f"WORLDMAP_PRESS_CANCEL_V10_REPAIR_REFUSED={exc}")
        return 44
    args.output.write_text(out, encoding="utf-8")
    args.output.chmod(0o700)
    print("WORLDMAP_PRESS_CANCEL_V10_REPAIR=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
