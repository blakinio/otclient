#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

GDB_OLD = "M(0xcec8d0,'FullMap');M(0xcecc70,'CreateOnMap');M(0xcecf40,'ChangeOnMap');M(0xcd4e20,'DeleteOnMap')"
GDB_NEW = (
    GDB_OLD
    + ";M(0xcfb374,'ShowCharacterSelection')"
    + ";M(0xd47300,'RequestCharacterLogin')"
    + ";M(0xcfb2e7,'RequestCharacterGameserverLogin')"
    + ";M(0xcfb122,'StartGameServerLogin')"
)

START = "POST_LOGIN_XWD=''\n"
END = "[[ \"$world\" == 1 ]] || fail structural_world_entry_not_observed\n"

REPLACEMENT = r'''# V7: native state/event proof replaces the failed translated historical row target.
# Wait for the exact native authentication state-machine entry into character selection.
CHAR_STATE=0
for _ in $(seq 1 60); do
  sleep .5
  if grep -Fq $'\tShowCharacterSelection' "$EVENTS" 2>/dev/null; then
    CHAR_STATE=1
    break
  fi
done
[[ "$CHAR_STATE" == 1 ]] || fail native_character_selection_state_not_observed
echo 'WORLDMAP_BASELINE_NATIVE_CHARACTER_SELECTION_STATE=PASS'

# The pre-login XWD is no longer required once the native state is proven.
# Keep a best-effort aggregate visual transition marker only as corroboration;
# native GDB state is the authority.
CHARSEL_XWD="$ROOT/character-selection.xwd"
sleep .20
capture_xwd "$CHARSEL_XWD"
set +e
VIS_OUT="$(python3 "$COMPARE" change "$PRELOGIN_REFERENCE" "$CHARSEL_XWD" --min-changed 5000 2>&1)"
VIS_RC=$?
set -e
if [[ "$VIS_RC" -eq 0 ]]; then
  echo 'WORLDMAP_BASELINE_CHARACTER_SELECTION_VISUAL_TRANSITION=CORROBORATED'
else
  echo 'WORLDMAP_BASELINE_CHARACTER_SELECTION_VISUAL_TRANSITION=NOT_REQUIRED'
fi
rm -f "$PRELOGIN_REFERENCE" "$CHARSEL_XWD"

character_request_seen() {
  grep -Fq $'\tRequestCharacterLogin' "$EVENTS" 2>/dev/null
}
wait_character_request() {
  local _i
  for _i in $(seq 1 12); do
    character_request_seen && return 0
    sleep .25
  done
  return 1
}

xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
xdo windowfocus --sync "$UI_WIN"

# If the native state machine has already auto-requested a character, do not
# send a second activation. Otherwise use only bounded keyboard/list semantics.
if character_request_seen; then
  echo 'WORLDMAP_BASELINE_CHARACTER_ACTIVATION_METHOD=AUTO_NATIVE_REQUEST'
else
  # Attempt 1: Return on the native character-selection state. Acceptance is
  # exclusively the requestCharacterLogin(TCharacter) breakpoint.
  xdo key --window "$UI_WIN" --clearmodifiers Return
  if wait_character_request; then
    echo 'WORLDMAP_BASELINE_CHARACTER_ACTIVATION_METHOD=RETURN_ON_NATIVE_CHARACTER_SELECTION'
  else
    # Attempt 2: use list navigation. Prove Down changes a localized region
    # after temporal XWD-noise subtraction before Return is sent.
    K0="$ROOT/char-key-idle0.xwd"; K1="$ROOT/char-key-idle1.xwd"; KB="$ROOT/char-key-before.xwd"; KA="$ROOT/char-key-after.xwd"
    capture_xwd "$K0"; sleep .20; capture_xwd "$K1"; sleep .20; capture_xwd "$KB"
    xdo key --window "$UI_WIN" --clearmodifiers Down
    sleep .30
    capture_xwd "$KA"
    set +e
    KEY_OUT="$(python3 - "$COMPARE" "$K0" "$K1" "$KB" "$KA" <<'PY'
import importlib.util,sys
from pathlib import Path
compare,i0,i1,before,after=sys.argv[1:]
spec=importlib.util.spec_from_file_location('wm_v7_compare',compare)
if spec is None or spec.loader is None: raise SystemExit(3)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
i0=Path(i0);i1=Path(i1);before=Path(before);after=Path(after)
noise=m.changed_mask(i0,i1)
signal=m.changed_mask(before,after)-noise
fields,_,_=m.load(before);bw,bh,area=m.bbox_metrics(signal,fields['width'])
print('WORLDMAP_V7_KEYBOARD_SELECTION_NOISE_PIXELS='+str(len(noise)))
print('WORLDMAP_V7_KEYBOARD_SELECTION_SIGNAL_PIXELS='+str(len(signal)))
print('WORLDMAP_V7_KEYBOARD_SELECTION_BBOX='+m.mask_bbox(signal,fields['width']))
print(f'WORLDMAP_V7_KEYBOARD_SELECTION_EXTENT={bw}x{bh};area={area}')
passed=len(signal)>=25 and bw>0 and bh>0 and bw<=1200 and bh<=260 and area<=160000
print('WORLDMAP_V7_KEYBOARD_SELECTION_CHANGE='+('PASS' if passed else 'FAIL'))
raise SystemExit(0 if passed else 3)
PY
)"
    KEY_RC=$?
    set -e
    rm -f "$K0" "$K1" "$KB" "$KA"
    printf '%s\n' "$KEY_OUT"
    if [[ "$KEY_RC" -eq 0 ]]; then
      xdo key --window "$UI_WIN" --clearmodifiers Return
      if wait_character_request; then
        echo 'WORLDMAP_BASELINE_CHARACTER_ACTIVATION_METHOD=DOWN_LOCAL_CHANGE_THEN_RETURN'
      fi
    fi
  fi
fi

if ! character_request_seen; then
  # Attempt 3: reverse list navigation only. No Tab/button traversal and no
  # coordinate click. The native request breakpoint remains the acceptance gate.
  xdo key --window "$UI_WIN" --clearmodifiers Up
  sleep .25
  xdo key --window "$UI_WIN" --clearmodifiers Return
  wait_character_request || true
  if character_request_seen; then
    echo 'WORLDMAP_BASELINE_CHARACTER_ACTIVATION_METHOD=UP_THEN_RETURN'
  fi
fi

[[ $(grep -Fc $'\tRequestCharacterLogin' "$EVENTS" 2>/dev/null || true) -ge 1 ]] || fail native_character_request_not_observed
echo 'WORLDMAP_BASELINE_NATIVE_CHARACTER_REQUEST=PASS'

GAME_REQ=0
for _ in $(seq 1 40); do
  sleep .25
  if grep -Fq $'\tRequestCharacterGameserverLogin' "$EVENTS" 2>/dev/null && \
     grep -Fq $'\tStartGameServerLogin' "$EVENTS" 2>/dev/null; then
    GAME_REQ=1
    break
  fi
done
[[ "$GAME_REQ" == 1 ]] || fail native_game_login_state_not_observed
echo 'WORLDMAP_BASELINE_NATIVE_GAME_LOGIN_STATE=PASS'

world=0
for _ in $(seq 1 60); do
  sleep 1
  if grep -Fq $'\tFullMap' "$EVENTS" 2>/dev/null && [[ "$(wc -l <"$STRIPS")" -ge 10 ]]; then
    world=1
    break
  fi
done
[[ "$world" == 1 ]] || fail structural_world_entry_not_observed
'''


class TransformRefused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(GDB_OLD) != 1:
        raise TransformRefused(f"GDB_ANCHOR_COUNT:{text.count(GDB_OLD)}")
    text = text.replace(GDB_OLD, GDB_NEW)
    if text.count(START) != 1:
        raise TransformRefused(f"START_COUNT:{text.count(START)}")
    start = text.index(START)
    end = text.find(END, start)
    if end < 0:
        raise TransformRefused("END_MISSING")
    end += len(END)
    output = text[:start] + REPLACEMENT + text[end:]

    required = (
        "M(0xcfb374,'ShowCharacterSelection')",
        "M(0xd47300,'RequestCharacterLogin')",
        "M(0xcfb2e7,'RequestCharacterGameserverLogin')",
        "M(0xcfb122,'StartGameServerLogin')",
        "WORLDMAP_BASELINE_NATIVE_CHARACTER_SELECTION_STATE=PASS",
        "WORLDMAP_BASELINE_NATIVE_CHARACTER_REQUEST=PASS",
        "WORLDMAP_BASELINE_NATIVE_GAME_LOGIN_STATE=PASS",
        "WORLDMAP_V7_KEYBOARD_SELECTION_CHANGE=",
        "WORLDMAP_BASELINE_STRUCTURAL_IN_GAME=PASS",
        "WORLDMAP_BASELINE_PRESECRET_READY=true",
        "WORLDMAP_BASELINE_LOGIN_SUBMITTED=true",
        'UI_WIN="$WIN"',
    )
    missing = [token for token in required if token not in output]
    if missing:
        raise TransformRefused("REQUIRED_MISSING:" + ",".join(missing))

    forbidden = (
        "WORLDMAP_BASELINE_CHARACTER_ROW_TARGET=",
        "WORLDMAP_BASELINE_CHARACTER_ROW_ROI=",
        "translated_character_row",
        "character_row_interaction_not_observed",
        "WORLDMAP_BASELINE_CHARACTER_DOUBLECLICK_FALLBACK_SENT=true",
        "SELECT_X",
        "SELECT_Y",
        "LOGIN_X=590",
        '"$XWD" -root',
        "xwd -root",
        "xrandr --output",
        "wmctrl -r",
    )
    survivors = [token for token in forbidden if token in output]
    if survivors:
        raise TransformRefused("FORBIDDEN_SURVIVORS:" + ",".join(survivors))
    if output.count('UI_WIN="$WIN"') != 1:
        raise TransformRefused("MANIFEST_WINDOW_IDENTITY_NOT_UNIQUE")
    return output


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    args = p.parse_args()
    try:
        out = transform(args.source.read_text(encoding="utf-8"))
    except TransformRefused as exc:
        print(f"WORLDMAP_CHARACTER_SELECTION_V7_REPAIR_REFUSED={exc}")
        return 44
    args.output.write_text(out, encoding="utf-8")
    args.output.chmod(0o700)
    print("WORLDMAP_CHARACTER_SELECTION_V7_REPAIR=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
