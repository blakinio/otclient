#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

GDB_V7 = (
    "M(0xcec8d0,'FullMap');M(0xcecc70,'CreateOnMap');M(0xcecf40,'ChangeOnMap');M(0xcd4e20,'DeleteOnMap')"
    ";M(0xcfb374,'ShowCharacterSelection');M(0xd47300,'RequestCharacterLogin')"
    ";M(0xcfb2e7,'RequestCharacterGameserverLogin');M(0xcfb122,'StartGameServerLogin')"
)
GDB_V9 = (
    "M(0xcec8d0,'FullMap');M(0xcecc70,'CreateOnMap');M(0xcecf40,'ChangeOnMap');M(0xcd4e20,'DeleteOnMap')"
    ";M(0xcfadd4,'LoginStateMachineStarted');M(0xcfb2ff,'LoginWaitingDialogEntered')"
    ";M(0xcfb7c0,'AccountLoginUploaderSuccess');M(0xcfb790,'AccountLoginUploaderFailed')"
    ";M(0xcfaeb4,'LoginFinishedSuccessfully');M(0xcfb404,'LoginFailedStateEntered')"
    ";M(0xcfb374,'ShowCharacterSelection');M(0xd47130,'CharacterSelectionConfirmed')"
    ";M(0xd47300,'RequestCharacterLogin');M(0xcfb2e7,'RequestCharacterGameserverLogin')"
    ";M(0xcfb122,'StartGameServerLogin');M(0xcfa0e0,'GameserverTcpConnected')"
    ";M(0xd06810,'ClientConnectGameserver');M(0xd067b0,'ClientAbortGameserverConnect')"
    ";M(0xd066e0,'GameSessionConnected')"
)

PRELOGIN_OLD = r'''PRELOGIN_REFERENCE="$ROOT/prelogin-reference.xwd"
sleep .20
capture_xwd "$PRELOGIN_REFERENCE"

# Secrets enter this helper only through the already-created mode-0600 FIFO,
'''

PRELOGIN_NEW = r'''PRELOGIN_REFERENCE="$ROOT/prelogin-reference.xwd"
sleep .20
capture_xwd "$PRELOGIN_REFERENCE"

# V9 pre-secret geometry parity: the historical proven 1020x650 surface is
# centered inside the current exact 1920x1080 X11 surface. The translation is
# accepted only when it agrees with the current dynamically discovered fields.
(( ACTUAL_WIDTH >= 1020 && ACTUAL_HEIGHT >= 650 )) || fail v9_surface_too_small
DELTA_W=$((ACTUAL_WIDTH-1020)); DELTA_H=$((ACTUAL_HEIGHT-650))
(( DELTA_W % 2 == 0 && DELTA_H % 2 == 0 )) || fail v9_surface_center_translation_fractional
SURFACE_DX=$((DELTA_W/2)); SURFACE_DY=$((DELTA_H/2))
HIST_EMAIL_X=$((535+SURFACE_DX)); HIST_EMAIL_Y=$((275+SURFACE_DY))
HIST_PASS_X=$((535+SURFACE_DX)); HIST_PASS_Y=$((304+SURFACE_DY))
LOGIN_X=$((590+SURFACE_DX)); LOGIN_Y=$((388+SURFACE_DY))
ROW_X=$((285+SURFACE_DX)); ROW_Y=$((193+SURFACE_DY))
ROW_X0=$((100+SURFACE_DX)); ROW_Y0=$((165+SURFACE_DY)); ROW_X1=$((900+SURFACE_DX)); ROW_Y1=$((230+SURFACE_DY))

IFS=, read -r EX0 EY0 EX1 EY1 <<<"$EMAIL_BBOX"
IFS=, read -r PX0 PY0 PX1 PY1 <<<"$PASS_BBOX"
for v in "$EX0" "$EY0" "$EX1" "$EY1" "$PX0" "$PY0" "$PX1" "$PY1"; do [[ "$v" =~ ^[0-9]+$ ]] || fail v9_dynamic_field_bbox_invalid; done
(( HIST_EMAIL_X >= EX0-180 && HIST_EMAIL_X <= EX1+180 && HIST_EMAIL_Y >= EY0-20 && HIST_EMAIL_Y <= EY1+20 )) || fail v9_email_translation_not_correlated
(( HIST_PASS_X >= PX0-180 && HIST_PASS_X <= PX1+180 && HIST_PASS_Y >= PY0-20 && HIST_PASS_Y <= PY1+20 )) || fail v9_password_translation_not_correlated
(( LOGIN_X >= 20 && LOGIN_X < ACTUAL_WIDTH-20 && LOGIN_Y >= 20 && LOGIN_Y < ACTUAL_HEIGHT-20 )) || fail v9_login_target_out_of_bounds
(( ROW_X >= 20 && ROW_X < ACTUAL_WIDTH-20 && ROW_Y >= 20 && ROW_Y < ACTUAL_HEIGHT-20 )) || fail v9_row_target_out_of_bounds
echo "WORLDMAP_V9_SURFACE_TRANSLATION=$SURFACE_DX,$SURFACE_DY"
echo "WORLDMAP_V9_LOGIN_BUTTON_TARGET=$LOGIN_X,$LOGIN_Y"
echo "WORLDMAP_V9_CHARACTER_ROW_TARGET=$ROW_X,$ROW_Y"
echo 'WORLDMAP_V9_SURFACE_TRANSLATION=PROVEN_BY_DYNAMIC_FIELDS'

# Prove the translated login-button target without clicking or using secrets.
# A reversible local hover response must exist around the candidate target.
H0="$ROOT/v9-login-hover-idle0.xwd"; H1="$ROOT/v9-login-hover-idle1.xwd"
HH="$ROOT/v9-login-hover.xwd"; H2="$ROOT/v9-login-hover-idle2.xwd"
HX0=$((LOGIN_X>180 ? LOGIN_X-180 : 0)); HY0=$((LOGIN_Y>70 ? LOGIN_Y-70 : 0))
HX1=$((LOGIN_X+180<ACTUAL_WIDTH ? LOGIN_X+180 : ACTUAL_WIDTH)); HY1=$((LOGIN_Y+70<ACTUAL_HEIGHT ? LOGIN_Y+70 : ACTUAL_HEIGHT))
xdo mousemove --window "$UI_WIN" 20 20
sleep .25; capture_xwd "$H0"; sleep .25; capture_xwd "$H1"
xdo mousemove --window "$UI_WIN" "$LOGIN_X" "$LOGIN_Y"
sleep .30; capture_xwd "$HH"
xdo mousemove --window "$UI_WIN" 20 20
sleep .30; capture_xwd "$H2"
set +e
HOVER_OUT="$(python3 - "$COMPARE" "$H0" "$H1" "$HH" "$H2" "$HX0" "$HY0" "$HX1" "$HY1" <<'PY'
import importlib.util,sys
from pathlib import Path
compare,i0,i1,hover,i2,*box=sys.argv[1:]
roi=tuple(map(int,box))
spec=importlib.util.spec_from_file_location('wm_v9_hover',compare)
if spec is None or spec.loader is None: raise SystemExit(3)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
i0=Path(i0);i1=Path(i1);hover=Path(hover);i2=Path(i2)
noise=m.changed_mask(i0,i1,roi)
enter=m.changed_mask(i1,hover,roi)-noise
leave=m.changed_mask(hover,i2,roi)-noise
signal=enter&leave
den=min(len(enter),len(leave)); overlap=len(signal)/den if den else 0.0
fields,_,_=m.load(i0);bw,bh,area=m.bbox_metrics(signal,fields['width'])
print('WORLDMAP_V9_LOGIN_HOVER_NOISE_PIXELS='+str(len(noise)))
print('WORLDMAP_V9_LOGIN_HOVER_ENTER_PIXELS='+str(len(enter)))
print('WORLDMAP_V9_LOGIN_HOVER_LEAVE_PIXELS='+str(len(leave)))
print('WORLDMAP_V9_LOGIN_HOVER_SIGNAL_PIXELS='+str(len(signal)))
print(f'WORLDMAP_V9_LOGIN_HOVER_OVERLAP={overlap:.6f}')
print('WORLDMAP_V9_LOGIN_HOVER_BBOX='+m.mask_bbox(signal,fields['width']))
print(f'WORLDMAP_V9_LOGIN_HOVER_EXTENT={bw}x{bh};area={area}')
passed=len(signal)>=10 and overlap>=0.35 and bw>0 and bh>0 and area<=50000
print('WORLDMAP_V9_LOGIN_BUTTON_HOVER=' + ('PASS' if passed else 'FAIL'))
raise SystemExit(0 if passed else 3)
PY
)"
HOVER_RC=$?
set -e
rm -f "$H0" "$H1" "$HH" "$H2"
printf '%s\n' "$HOVER_OUT"
[[ "$HOVER_RC" -eq 0 ]] || fail v9_login_button_hover_unproven
echo 'WORLDMAP_V9_PRESECRET_LOGIN_BUTTON=PROVEN'

# Secrets enter this helper only through the already-created mode-0600 FIFO,
'''

LOGIN_SUBMIT_OLD = r'''# Password is the second physically proven local text field. Move exactly one
# focus step forward and activate the next control; success is never inferred
# from this keypress and requires the independent transition/structural gates.
xdo key --window "$UI_WIN" --clearmodifiers Tab
sleep .20
xdo key --window "$UI_WIN" --clearmodifiers Return
echo 'WORLDMAP_BASELINE_LOGIN_SUBMISSION_METHOD=PASSWORD_TAB_RETURN'
echo 'WORLDMAP_BASELINE_LOGIN_SUBMITTED=true'
'''

LOGIN_SUBMIT_NEW = r'''# V9: submit through the translated button proven pre-secret by reversible hover.
AUTH_SUCCESS_BEFORE="$(grep -Fc $'\tAccountLoginUploaderSuccess' "$EVENTS" 2>/dev/null || true)"
AUTH_FAIL_BEFORE="$(grep -Fc $'\tAccountLoginUploaderFailed' "$EVENTS" 2>/dev/null || true)"
LOGIN_OK_BEFORE="$(grep -Fc $'\tLoginFinishedSuccessfully' "$EVENTS" 2>/dev/null || true)"
LOGIN_FAIL_BEFORE="$(grep -Fc $'\tLoginFailedStateEntered' "$EVENTS" 2>/dev/null || true)"
CHAR_STATE_BEFORE="$(grep -Fc $'\tShowCharacterSelection' "$EVENTS" 2>/dev/null || true)"
xdo mousemove --window "$UI_WIN" "$LOGIN_X" "$LOGIN_Y" click 1
echo 'WORLDMAP_BASELINE_LOGIN_SUBMISSION_METHOD=CENTER_TRANSLATED_BUTTON_CLICK'
echo 'WORLDMAP_BASELINE_LOGIN_SUBMITTED=true'

AUTH_UPLOADER_OK=0
for _ in $(seq 1 180); do
  sleep .5
  suc="$(grep -Fc $'\tAccountLoginUploaderSuccess' "$EVENTS" 2>/dev/null || true)"
  bad="$(grep -Fc $'\tAccountLoginUploaderFailed' "$EVENTS" 2>/dev/null || true)"
  lbad="$(grep -Fc $'\tLoginFailedStateEntered' "$EVENTS" 2>/dev/null || true)"
  if (( bad > AUTH_FAIL_BEFORE || lbad > LOGIN_FAIL_BEFORE )); then fail native_account_login_failed; fi
  if (( suc > AUTH_SUCCESS_BEFORE )); then AUTH_UPLOADER_OK=1; break; fi
done
[[ "$AUTH_UPLOADER_OK" == 1 ]] || fail native_account_login_uploader_success_not_observed
echo 'WORLDMAP_BASELINE_ACCOUNT_LOGIN_UPLOADER_SUCCESS=PASS'

LOGIN_FINISHED_OK=0
for _ in $(seq 1 120); do
  sleep .5
  ok="$(grep -Fc $'\tLoginFinishedSuccessfully' "$EVENTS" 2>/dev/null || true)"
  bad="$(grep -Fc $'\tLoginFailedStateEntered' "$EVENTS" 2>/dev/null || true)"
  (( bad > LOGIN_FAIL_BEFORE )) && fail native_login_failed_state_observed
  if (( ok > LOGIN_OK_BEFORE )); then LOGIN_FINISHED_OK=1; break; fi
done
[[ "$LOGIN_FINISHED_OK" == 1 ]] || fail native_login_finished_successfully_not_observed
echo 'WORLDMAP_BASELINE_LOGIN_FINISHED_SUCCESSFULLY=PASS'
'''

POST_START = "# V7: native state/event proof replaces the failed translated historical row target.\n"
POST_END = "world=0\n"

POST_NEW = r'''# V9: account auth is already proven by uploader-success and login-finished events.
# Now require the native character-selection state before any character input.
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
xdo key --window "$UI_WIN" --clearmodifiers Return
echo 'WORLDMAP_BASELINE_CHARACTER_ACTIVATION_METHOD=CENTER_TRANSLATED_ROW_CLICK_RETURN'

CHAR_REQUEST=0
for _ in $(seq 1 24); do
  sleep .25
  req="$(grep -Fc $'\tRequestCharacterLogin' "$EVENTS" 2>/dev/null || true)"
  if (( req > REQUEST_BEFORE )); then CHAR_REQUEST=1; break; fi
done
if [[ "$CHAR_REQUEST" != 1 ]]; then
  # Historical successful flow used one double-click fallback on this same row.
  # V9 permits exactly one such fallback only on the center-translated target.
  xdo mousemove --window "$UI_WIN" "$ROW_X" "$ROW_Y" click --repeat 2 --delay 160 1
  xdo key --window "$UI_WIN" --clearmodifiers Return
  echo 'WORLDMAP_BASELINE_CHARACTER_ACTIVATION_FALLBACK=CENTER_TRANSLATED_ROW_DOUBLECLICK_RETURN'
  for _ in $(seq 1 40); do
    sleep .25
    req="$(grep -Fc $'\tRequestCharacterLogin' "$EVENTS" 2>/dev/null || true)"
    if (( req > REQUEST_BEFORE )); then CHAR_REQUEST=1; break; fi
  done
fi
[[ "$CHAR_REQUEST" == 1 ]] || fail native_character_request_not_observed_on_corrected_target
confirm="$(grep -Fc $'\tCharacterSelectionConfirmed' "$EVENTS" 2>/dev/null || true)"
if (( confirm > CONFIRM_BEFORE )); then echo 'WORLDMAP_BASELINE_NATIVE_CHARACTER_SELECTION_CONFIRMED=PASS'; else echo 'WORLDMAP_BASELINE_NATIVE_CHARACTER_SELECTION_CONFIRMED=NOT_REQUIRED_REQUEST_PROVEN'; fi
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

WORLD_FALLBACK = r'''if [[ "$world" != 1 ]]; then
  xdo mousemove --window "$UI_WIN" "$SELECT_X" "$SELECT_Y" click --repeat 2 --delay 120 1
  xdo key --window "$UI_WIN" --clearmodifiers Return
  echo 'WORLDMAP_BASELINE_CHARACTER_DOUBLECLICK_FALLBACK_SENT=true'
  for _ in $(seq 1 30); do
    sleep 1
    if grep -Fq $'\tFullMap' "$EVENTS" 2>/dev/null && [[ "$(wc -l <"$STRIPS")" -ge 10 ]]; then
      world=1
      break
    fi
  done
fi
'''


class TransformRefused(RuntimeError):
    pass


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise TransformRefused(f"{label}_COUNT:{count}")
    return text.replace(old, new, 1)


def transform(text: str) -> str:
    text = replace_once(text, GDB_V7, GDB_V9, "GDB_V7")
    text = replace_once(text, PRELOGIN_OLD, PRELOGIN_NEW, "PRELOGIN")
    text = replace_once(text, LOGIN_SUBMIT_OLD, LOGIN_SUBMIT_NEW, "LOGIN_SUBMIT")

    if text.count(POST_START) != 1:
        raise TransformRefused(f"POST_START_COUNT:{text.count(POST_START)}")
    start = text.index(POST_START)
    end = text.find(POST_END, start)
    if end < 0:
        raise TransformRefused("POST_END_MISSING")
    end += len(POST_END)
    text = text[:start] + POST_NEW + text[end:]

    text = replace_once(text, WORLD_FALLBACK, "", "WORLD_COORDINATE_FALLBACK")

    required = (
        "M(0xcfb7c0,'AccountLoginUploaderSuccess')",
        "M(0xcfb790,'AccountLoginUploaderFailed')",
        "M(0xcfaeb4,'LoginFinishedSuccessfully')",
        "M(0xcfb404,'LoginFailedStateEntered')",
        "M(0xd47130,'CharacterSelectionConfirmed')",
        "WORLDMAP_V9_SURFACE_TRANSLATION=PROVEN_BY_DYNAMIC_FIELDS",
        "WORLDMAP_V9_LOGIN_BUTTON_HOVER=",
        "WORLDMAP_V9_PRESECRET_LOGIN_BUTTON=PROVEN",
        "WORLDMAP_BASELINE_LOGIN_SUBMISSION_METHOD=CENTER_TRANSLATED_BUTTON_CLICK",
        "WORLDMAP_BASELINE_ACCOUNT_LOGIN_UPLOADER_SUCCESS=PASS",
        "WORLDMAP_BASELINE_LOGIN_FINISHED_SUCCESSFULLY=PASS",
        "WORLDMAP_BASELINE_NATIVE_CHARACTER_SELECTION_STATE=PASS",
        "WORLDMAP_BASELINE_NATIVE_CHARACTER_REQUEST=PASS",
        "WORLDMAP_BASELINE_NATIVE_GAME_LOGIN_STATE=PASS",
        "WORLDMAP_BASELINE_STRUCTURAL_IN_GAME=PASS",
        'UI_WIN="$WIN"',
    )
    missing = [token for token in required if token not in text]
    if missing:
        raise TransformRefused("REQUIRED_MISSING:" + ",".join(missing))

    forbidden = (
        "PASSWORD_TAB_RETURN",
        "WORLDMAP_BASELINE_CHARACTER_ROW_TARGET=",
        "WORLDMAP_BASELINE_CHARACTER_ROW_ROI=",
        "translated_character_row",
        "character_row_interaction_not_observed",
        "SELECT_X=",
        "SELECT_Y=",
        '"$XWD" -root',
        "xwd -root",
        "xrandr --output",
        "wmctrl -r",
    )
    survivors = [token for token in forbidden if token in text]
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
        result = transform(args.source.read_text(encoding="utf-8"))
    except TransformRefused as exc:
        print(f"WORLDMAP_AUTH_SUBMIT_V9_REPAIR_REFUSED={exc}")
        return 44
    args.output.write_text(result, encoding="utf-8")
    args.output.chmod(0o700)
    print("WORLDMAP_AUTH_SUBMIT_V9_REPAIR=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
