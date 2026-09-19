#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

CENTER_ANCHOR = '''[[ "$LOGIN_BUTTON_PROVEN" == 1 ]] || fail v10_login_button_press_cancel_unproven\n\n# Secrets enter this helper only through the already-created mode-0600 FIFO,\n'''
CENTER_REPLACEMENT = r'''[[ "$LOGIN_BUTTON_PROVEN" == 1 ]] || fail v10_login_button_press_cancel_unproven

# V11: use the center of the physically observed pressed-state bbox rather than
# the scan stimulus point itself. This remains pre-secret and non-activating.
PRESS_BBOX="$(awk -F= '/^WORLDMAP_V10_PRESS_BBOX=/{print $2}' <<<"$PRESS_OUT" | tail -1)"
IFS=, read -r LBX0 LBY0 LBX1 LBY1 <<<"$PRESS_BBOX"
for v in "$LBX0" "$LBY0" "$LBX1" "$LBY1"; do [[ "$v" =~ ^[0-9]+$ ]] || fail v11_login_button_bbox_invalid; done
(( LBX0 < LBX1 && LBY0 < LBY1 )) || fail v11_login_button_bbox_empty
LOGIN_X=$(((LBX0+LBX1)/2)); LOGIN_Y=$(((LBY0+LBY1)/2))
echo "WORLDMAP_V11_LOGIN_BUTTON_CENTER=$LOGIN_X,$LOGIN_Y"
echo 'WORLDMAP_V11_LOGIN_BUTTON_CENTER=PROVEN_FROM_PRESS_BBOX'

# Secrets enter this helper only through the already-created mode-0600 FIFO,
'''

AUTH_START = '''AUTH_SUCCESS_BEFORE="$(grep -Fc $'\\tAccountLoginUploaderSuccess' "$EVENTS" 2>/dev/null || true)"\n'''
AUTH_END = "echo 'WORLDMAP_BASELINE_LOGIN_FINISHED_SUCCESSFULLY=PASS'\n"

AUTH_REPLACEMENT = r'''# V11 secret-safe occupancy proof: prove only that both protected fields are
# visibly non-empty. No pixels are persisted and no text/secret value is read.
OCC0="$ROOT/v11-occupied0.xwd"; OCC1="$ROOT/v11-occupied1.xwd"
sleep .20; capture_xwd "$OCC0"; sleep .20; capture_xwd "$OCC1"
OCC_OUT="$(python3 - "$COMPARE" "$PRELOGIN_REFERENCE" "$OCC0" "$OCC1" "$EMAIL_BBOX" "$PASS_BBOX" <<'PY'
import importlib.util,sys
from pathlib import Path
compare,blank,occ0,occ1,email_box,pass_box=sys.argv[1:]
spec=importlib.util.spec_from_file_location('wm_v11_occ',compare)
if spec is None or spec.loader is None: raise SystemExit(3)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
blank=Path(blank);occ0=Path(occ0);occ1=Path(occ1)
fields,_,_=m.load(blank);w=fields['width'];h=fields['height']
def roi(raw):
    x0,y0,x1,y1=map(int,raw.split(','))
    return (max(0,x0-20),max(0,y0-12),min(w,x1+120),min(h,y1+12))
def count(r):
    noise=m.changed_mask(occ0,occ1,r)
    return len(m.changed_mask(blank,occ0,r)-noise),len(noise)
e,n1=count(roi(email_box));p,n2=count(roi(pass_box))
print('WORLDMAP_V11_EMAIL_OCCUPANCY_CHANGED='+str(e))
print('WORLDMAP_V11_PASSWORD_OCCUPANCY_CHANGED='+str(p))
print('WORLDMAP_V11_EMAIL_OCCUPANCY_NOISE='+str(n1))
print('WORLDMAP_V11_PASSWORD_OCCUPANCY_NOISE='+str(n2))
passed=e>=20 and p>=20
print('WORLDMAP_V11_SECRET_FIELD_OCCUPANCY='+('PASS' if passed else 'FAIL'))
raise SystemExit(0 if passed else 3)
PY
)" || fail v11_secret_field_occupancy_unproven
rm -f "$OCC0" "$OCC1"
printf '%s\n' "$OCC_OUT"
echo 'WORLDMAP_BASELINE_SECRET_FIELD_OCCUPANCY=PASS'

AUTH_STATE_BEFORE="$(grep -Fc $'\tLoginStateMachineStarted' "$EVENTS" 2>/dev/null || true)"
AUTH_WAIT_BEFORE="$(grep -Fc $'\tLoginWaitingDialogEntered' "$EVENTS" 2>/dev/null || true)"
AUTH_SUCCESS_BEFORE="$(grep -Fc $'\tAccountLoginUploaderSuccess' "$EVENTS" 2>/dev/null || true)"
AUTH_FAIL_BEFORE="$(grep -Fc $'\tAccountLoginUploaderFailed' "$EVENTS" 2>/dev/null || true)"
LOGIN_OK_BEFORE="$(grep -Fc $'\tLoginFinishedSuccessfully' "$EVENTS" 2>/dev/null || true)"
LOGIN_FAIL_BEFORE="$(grep -Fc $'\tLoginFailedStateEntered' "$EVENTS" 2>/dev/null || true)"
CHAR_STATE_BEFORE="$(grep -Fc $'\tShowCharacterSelection' "$EVENTS" 2>/dev/null || true)"

xdo mousemove --window "$UI_WIN" "$LOGIN_X" "$LOGIN_Y" click 1
echo 'WORLDMAP_BASELINE_LOGIN_SUBMISSION_METHOD=PRESS_BBOX_CENTER_CLICK'
echo 'WORLDMAP_BASELINE_LOGIN_SUBMITTED=true'

# A click may focus rather than activate on some Qt paths. Only when no native
# auth/downstream event is observed do one Return fallback on that now-focused
# control; this remains the same bounded login attempt.
AUTH_ACTIVATED=0
for _ in $(seq 1 16); do
  sleep .25
  state="$(grep -Fc $'\tLoginStateMachineStarted' "$EVENTS" 2>/dev/null || true)"
  suc="$(grep -Fc $'\tAccountLoginUploaderSuccess' "$EVENTS" 2>/dev/null || true)"
  fin="$(grep -Fc $'\tLoginFinishedSuccessfully' "$EVENTS" 2>/dev/null || true)"
  chr="$(grep -Fc $'\tShowCharacterSelection' "$EVENTS" 2>/dev/null || true)"
  bad="$(grep -Fc $'\tAccountLoginUploaderFailed' "$EVENTS" 2>/dev/null || true)"
  lbad="$(grep -Fc $'\tLoginFailedStateEntered' "$EVENTS" 2>/dev/null || true)"
  (( bad > AUTH_FAIL_BEFORE || lbad > LOGIN_FAIL_BEFORE )) && fail native_account_login_failed
  if (( state > AUTH_STATE_BEFORE || suc > AUTH_SUCCESS_BEFORE || fin > LOGIN_OK_BEFORE || chr > CHAR_STATE_BEFORE )); then AUTH_ACTIVATED=1; break; fi
done
if [[ "$AUTH_ACTIVATED" != 1 ]]; then
  xdo key --window "$UI_WIN" --clearmodifiers Return
  echo 'WORLDMAP_BASELINE_LOGIN_ACTIVATION_FALLBACK=RETURN_ON_PRESS_PROVEN_BUTTON'
  for _ in $(seq 1 16); do
    sleep .25
    state="$(grep -Fc $'\tLoginStateMachineStarted' "$EVENTS" 2>/dev/null || true)"
    suc="$(grep -Fc $'\tAccountLoginUploaderSuccess' "$EVENTS" 2>/dev/null || true)"
    fin="$(grep -Fc $'\tLoginFinishedSuccessfully' "$EVENTS" 2>/dev/null || true)"
    chr="$(grep -Fc $'\tShowCharacterSelection' "$EVENTS" 2>/dev/null || true)"
    bad="$(grep -Fc $'\tAccountLoginUploaderFailed' "$EVENTS" 2>/dev/null || true)"
    lbad="$(grep -Fc $'\tLoginFailedStateEntered' "$EVENTS" 2>/dev/null || true)"
    (( bad > AUTH_FAIL_BEFORE || lbad > LOGIN_FAIL_BEFORE )) && fail native_account_login_failed
    if (( state > AUTH_STATE_BEFORE || suc > AUTH_SUCCESS_BEFORE || fin > LOGIN_OK_BEFORE || chr > CHAR_STATE_BEFORE )); then AUTH_ACTIVATED=1; break; fi
  done
fi
[[ "$AUTH_ACTIVATED" == 1 ]] || fail native_login_activation_state_not_observed
echo 'WORLDMAP_BASELINE_NATIVE_LOGIN_ACTIVATION=PASS'

# Strong auth completion is downstream character-selection state. Uploader and
# LoginFinished are recorded when seen but are not mandatory if the stronger
# ShowCharacterSelection state is reached through another legitimate path.
AUTH_DOWNSTREAM=0
for _ in $(seq 1 360); do
  sleep .5
  bad="$(grep -Fc $'\tAccountLoginUploaderFailed' "$EVENTS" 2>/dev/null || true)"
  lbad="$(grep -Fc $'\tLoginFailedStateEntered' "$EVENTS" 2>/dev/null || true)"
  (( bad > AUTH_FAIL_BEFORE || lbad > LOGIN_FAIL_BEFORE )) && fail native_account_login_failed
  chr="$(grep -Fc $'\tShowCharacterSelection' "$EVENTS" 2>/dev/null || true)"
  if (( chr > CHAR_STATE_BEFORE )); then AUTH_DOWNSTREAM=1; break; fi
done

state="$(grep -Fc $'\tLoginStateMachineStarted' "$EVENTS" 2>/dev/null || true)"
waitc="$(grep -Fc $'\tLoginWaitingDialogEntered' "$EVENTS" 2>/dev/null || true)"
suc="$(grep -Fc $'\tAccountLoginUploaderSuccess' "$EVENTS" 2>/dev/null || true)"
fin="$(grep -Fc $'\tLoginFinishedSuccessfully' "$EVENTS" 2>/dev/null || true)"
chr="$(grep -Fc $'\tShowCharacterSelection' "$EVENTS" 2>/dev/null || true)"
echo "WORLDMAP_V11_AUTH_EVENT_COUNTS=state:$((state-AUTH_STATE_BEFORE));waiting:$((waitc-AUTH_WAIT_BEFORE));uploader_success:$((suc-AUTH_SUCCESS_BEFORE));login_finished:$((fin-LOGIN_OK_BEFORE));character_selection:$((chr-CHAR_STATE_BEFORE))"
[[ "$AUTH_DOWNSTREAM" == 1 ]] || fail native_auth_downstream_character_selection_not_observed
if (( suc > AUTH_SUCCESS_BEFORE )); then
  echo 'WORLDMAP_BASELINE_ACCOUNT_LOGIN_UPLOADER_SUCCESS=PASS'
else
  echo 'WORLDMAP_BASELINE_ACCOUNT_LOGIN_UPLOADER_SUCCESS=NOT_OBSERVED_DOWNSTREAM_SUCCESS_PROVEN'
fi
if (( fin > LOGIN_OK_BEFORE )); then
  echo 'WORLDMAP_BASELINE_LOGIN_FINISHED_SUCCESSFULLY=PASS'
else
  echo 'WORLDMAP_BASELINE_LOGIN_FINISHED_SUCCESSFULLY=NOT_OBSERVED_DOWNSTREAM_SUCCESS_PROVEN'
fi
echo 'WORLDMAP_BASELINE_AUTH_DOWNSTREAM_CHARACTER_SELECTION=PASS'
'''


class TransformRefused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(CENTER_ANCHOR) != 1:
        raise TransformRefused(f"CENTER_ANCHOR_COUNT:{text.count(CENTER_ANCHOR)}")
    text = text.replace(CENTER_ANCHOR, CENTER_REPLACEMENT, 1)

    if text.count(AUTH_START) != 1:
        raise TransformRefused(f"AUTH_START_COUNT:{text.count(AUTH_START)}")
    start = text.index(AUTH_START)
    end = text.find(AUTH_END, start)
    if end < 0:
        raise TransformRefused("AUTH_END_MISSING")
    end += len(AUTH_END)
    text = text[:start] + AUTH_REPLACEMENT + text[end:]

    required = (
        "WORLDMAP_V11_LOGIN_BUTTON_CENTER=PROVEN_FROM_PRESS_BBOX",
        "WORLDMAP_V11_SECRET_FIELD_OCCUPANCY=",
        "WORLDMAP_BASELINE_SECRET_FIELD_OCCUPANCY=PASS",
        "WORLDMAP_BASELINE_LOGIN_SUBMISSION_METHOD=PRESS_BBOX_CENTER_CLICK",
        "WORLDMAP_BASELINE_NATIVE_LOGIN_ACTIVATION=PASS",
        "WORLDMAP_V11_AUTH_EVENT_COUNTS=",
        "WORLDMAP_BASELINE_AUTH_DOWNSTREAM_CHARACTER_SELECTION=PASS",
        "WORLDMAP_BASELINE_NATIVE_CHARACTER_SELECTION_STATE=PASS",
        "WORLDMAP_BASELINE_NATIVE_CHARACTER_REQUEST=PASS",
        "WORLDMAP_BASELINE_STRUCTURAL_IN_GAME=PASS",
        'UI_WIN="$WIN"',
    )
    missing=[x for x in required if x not in text]
    if missing:
        raise TransformRefused("REQUIRED_MISSING:"+",".join(missing))
    forbidden=(
        "native_account_login_uploader_success_not_observed",
        "PRESS_CANCEL_PROVEN_BUTTON_CLICK",
        "CENTER_TRANSLATED_BUTTON_CLICK",
        "PASSWORD_TAB_RETURN",
        '"$XWD" -root',
        "xwd -root",
        "xrandr --output",
        "wmctrl -r",
    )
    survivors=[x for x in forbidden if x in text]
    if survivors:
        raise TransformRefused("FORBIDDEN_SURVIVORS:"+",".join(survivors))
    if text.count('UI_WIN="$WIN"') != 1:
        raise TransformRefused("MANIFEST_WINDOW_IDENTITY_NOT_UNIQUE")
    return text


def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("source",type=Path); p.add_argument("output",type=Path); a=p.parse_args()
    try: out=transform(a.source.read_text(encoding="utf-8"))
    except TransformRefused as exc:
        print(f"WORLDMAP_AUTH_STATE_V11_REPAIR_REFUSED={exc}"); return 44
    a.output.write_text(out,encoding="utf-8"); a.output.chmod(0o700)
    print("WORLDMAP_AUTH_STATE_V11_REPAIR=PASS"); return 0

if __name__=="__main__": raise SystemExit(main())
