#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


START = "# Screenshot/OCR is used only to locate login/character-selection controls. No screenshot or OCR text is retained.\n"
END = "world=0\n"

REPLACEMENT = r'''# Raw XWD bootstrap geometry is used only to locate login/character-selection controls.
# It is calibrated from retained exact-client artifacts and is never world-state evidence.
XWD="$(command -v xwd 2>/dev/null || true)"
[[ -n "$XWD" ]] || XWD="$(find "$TOOL" -xdev -type f -name xwd -perm -111 -print -quit 2>/dev/null || true)"
CLASSIFIER="${GITHUB_WORKSPACE:-$PWD}/.github/scripts/track-a-worldmap-causal-xwd-classify.py"
UI_WINDOW_RESOLVER="${GITHUB_WORKSPACE:-$PWD}/.github/scripts/track-a-worldmap-causal-ui-window.py"
UI_OWNER_HELPER="${GITHUB_WORKSPACE:-$PWD}/.github/scripts/tibia-official-client-re-xres-window-owner.py"
UI_WIRE_HELPER="${GITHUB_WORKSPACE:-$PWD}/.github/scripts/tibia-official-client-re-xres-wire.py"
[[ -x "$XWD" ]] || fail xwd_missing_before_secret_use
[[ -f "$CLASSIFIER" ]] || fail xwd_classifier_missing
[[ -f "$UI_WINDOW_RESOLVER" && -f "$UI_OWNER_HELPER" && -f "$UI_WIRE_HELPER" ]] || fail xres_ui_window_helper_missing
python3 "$CLASSIFIER" self-test

# Runtime identity remains the already-proven XRes-owned 1920x1080 WIN. Resolve a
# separate 1020x650 UI-control XID and independently require XRes LocalClientPid
# to equal the same exact task-owned client PID. No legacy _NET_WM_PID result is
# promoted as ownership evidence.
UI_WIN="$(python3 "$UI_WINDOW_RESOLVER" \
  --display "$DISPLAY" --pid "$PID" --toolroot "$TOOL" \
  --owner-helper "$UI_OWNER_HELPER" --wire-helper "$UI_WIRE_HELPER")" || fail xres_ui_window_unresolved
[[ "$UI_WIN" =~ ^[1-9][0-9]*$ ]] || fail xres_ui_window_invalid
[[ "$UI_WIN" != "$WIN" ]] || fail ui_window_must_be_distinct_from_identity_window
echo "WORLDMAP_BASELINE_UI_WINDOW_IDENTITY=x11-window:$UI_WIN"
echo 'WORLDMAP_BASELINE_UI_WINDOW_XRES_OWNER=PROVEN'
echo 'WORLDMAP_BASELINE_UI_WINDOW_GEOMETRY=1020x650'

XWD_TOOLROOT_LIBS="$TOOL/usr/lib/x86_64-linux-gnu:$TOOL/lib/x86_64-linux-gnu"
capture_xwd() {
  local outfile="$1"
  if [[ "$XWD" == "$TOOL/"* ]]; then
    DISPLAY="$DISPLAY" LD_LIBRARY_PATH="$XWD_TOOLROOT_LIBS" "$XWD" -silent -id "$UI_WIN" -out "$outfile"
  else
    DISPLAY="$DISPLAY" "$XWD" -silent -id "$UI_WIN" -out "$outfile"
  fi
}

echo 'WORLDMAP_BASELINE_LOGIN_UI_TOOLING=RAW_XWD_GEOMETRY_PASS'

SCREEN_CLASS=''
SCREEN_RESULT=''
classify_screen() {
  local stem="$1"
  local xwdfile="$ROOT/$stem.xwd"
  capture_xwd "$xwdfile"
  if ! SCREEN_RESULT="$(python3 "$CLASSIFIER" classify "$xwdfile")"; then
    rm -f "$xwdfile"
    printf '%s\n' "$SCREEN_RESULT"
    fail xwd_classifier_failed
  fi
  rm -f "$xwdfile"
  printf '%s\n' "$SCREEN_RESULT"
  SCREEN_CLASS="$(printf '%s\n' "$SCREEN_RESULT" | sed -n 's/^WORLDMAP_XWD_CLASS=//p')"
  [[ -n "$SCREEN_CLASS" ]] || fail xwd_classifier_no_class
}

login_ready=0
for i in $(seq 1 30); do
  classify_screen "login-geometry-$i"
  if [[ "$SCREEN_CLASS" == LOGIN_FORM ]]; then login_ready=1; break; fi
  sleep 1
done
[[ "$login_ready" == 1 ]] || fail login_form_geometry_not_revalidated
echo 'WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_RAW_XWD_GEOMETRY'

# Safe interior points from retained exact-client empty-login artifact 9221131366.
EMAIL_X=520
EMAIL_Y=275
PASS_X=520
PASS_Y=305
LOGIN_X=590
LOGIN_Y=389
DISPLAY="$DISPLAY" "$XDOTOOL" windowactivate --sync "$UI_WIN"
DISPLAY="$DISPLAY" "$XDOTOOL" mousemove --window "$UI_WIN" "$EMAIL_X" "$EMAIL_Y" click 1 key --clearmodifiers ctrl+a
printf '%s' "$TIBIA_TEST_EMAIL" | DISPLAY="$DISPLAY" "$XDOTOOL" type --window "$UI_WIN" --clearmodifiers --file -
DISPLAY="$DISPLAY" "$XDOTOOL" mousemove --window "$UI_WIN" "$PASS_X" "$PASS_Y" click 1 key --clearmodifiers ctrl+a
printf '%s' "$TIBIA_TEST_PASSWORD" | DISPLAY="$DISPLAY" "$XDOTOOL" type --window "$UI_WIN" --clearmodifiers --file -
DISPLAY="$DISPLAY" "$XDOTOOL" mousemove --window "$UI_WIN" "$LOGIN_X" "$LOGIN_Y" click 1
unset TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD
echo 'WORLDMAP_BASELINE_LOGIN_SUBMITTED=true'

select_ready=0
for i in $(seq 1 40); do
  sleep 2
  classify_screen "selection-geometry-$i"
  if [[ "$SCREEN_CLASS" == SELECT_CHARACTER ]]; then select_ready=1; break; fi
done
[[ "$select_ready" == 1 ]] || fail character_selection_geometry_not_observed
echo 'WORLDMAP_BASELINE_CHARACTER_SELECTION=PROVEN_RAW_XWD_GEOMETRY'

# Safe interior point of the first full character row from retained exact-client artifact 9221234379.
ROW_X=300
ROW_Y=195
DISPLAY="$DISPLAY" "$XDOTOOL" mousemove --window "$UI_WIN" "$ROW_X" "$ROW_Y" click 1 key Return
echo 'WORLDMAP_BASELINE_CHARACTER_ACTIVATION_SENT=true'

'''


class TransformRefused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(START) != 1:
        raise TransformRefused(f"UI_START_MARKER_COUNT:{text.count(START)}")
    if text.count(END) != 1:
        raise TransformRefused(f"WORLD_MARKER_COUNT:{text.count(END)}")
    start = text.index(START)
    end = text.index(END, start)
    output = text[:start] + REPLACEMENT + text[end:]
    forbidden = ("tesseract", "capture_ocr", "LOGIN_OCR_ANCHORS", "SELECT_TSV", "PRE_TSV")
    survivors = [token for token in forbidden if token in output]
    if survivors:
        raise TransformRefused("OCR_SURVIVORS:" + ",".join(survivors))
    required = (
        "WORLDMAP_BASELINE_UI_WINDOW_XRES_OWNER=PROVEN",
        "WORLDMAP_BASELINE_UI_WINDOW_GEOMETRY=1020x650",
        "WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_RAW_XWD_GEOMETRY",
        "WORLDMAP_BASELINE_CHARACTER_SELECTION=PROVEN_RAW_XWD_GEOMETRY",
        "EMAIL_X=520",
        "ROW_X=300",
        'LD_LIBRARY_PATH="$XWD_TOOLROOT_LIBS" "$XWD"',
        '--owner-helper "$UI_OWNER_HELPER" --wire-helper "$UI_WIRE_HELPER"',
    )
    missing = [token for token in required if token not in output]
    if missing:
        raise TransformRefused("REQUIRED_MISSING:" + ",".join(missing))
    if 'search --onlyvisible --pid' in output:
        raise TransformRefused("LEGACY_PID_WINDOW_SELECTOR_SURVIVED")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        repaired = transform(args.source.read_text(encoding="utf-8"))
    except TransformRefused as exc:
        print(f"WORLDMAP_UI_GEOMETRY_REPAIR_REFUSED={exc}")
        return 44
    args.output.write_text(repaired, encoding="utf-8")
    args.output.chmod(0o700)
    print("WORLDMAP_UI_GEOMETRY_REPAIR=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
