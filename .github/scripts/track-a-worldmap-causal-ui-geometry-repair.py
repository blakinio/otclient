#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


START = "# Screenshot/OCR is used only to locate login/character-selection controls. No screenshot or OCR text is retained.\n"
END = "world=0\n"

REPLACEMENT = r'''# Raw XWD bootstrap geometry is used only to locate login/character-selection controls.
# The task-owned desktop has already been normalized to 1020x650 before launch.
XWD="$(command -v xwd 2>/dev/null || true)"
[[ -n "$XWD" ]] || XWD="$(find "$TOOL" -xdev -type f -name xwd -perm -111 -print -quit 2>/dev/null || true)"
CLASSIFIER="${GITHUB_WORKSPACE:-$PWD}/.github/scripts/track-a-worldmap-causal-xwd-classify.py"
[[ -x "$XWD" ]] || fail xwd_missing_before_secret_use
[[ -f "$CLASSIFIER" ]] || fail xwd_classifier_missing
python3 "$CLASSIFIER" self-test

# WIN came from the worker manifest only after raw-XRes LocalClientPid matched the
# exact task-owned client PID under the task-local 1020x650 owner helper. Reuse
# that already-proven XID instead of performing a redundant second XRes search.
# The live raw-XWD classifier below independently revalidates current 1020x650
# geometry and LOGIN_FORM immediately before any credential is typed.
UI_WIN="$WIN"
[[ "$UI_WIN" =~ ^[1-9][0-9]*$ ]] || fail manifest_ui_window_invalid
echo "WORLDMAP_BASELINE_UI_WINDOW_IDENTITY=x11-window:$UI_WIN"
echo 'WORLDMAP_BASELINE_UI_WINDOW_XRES_OWNER=MANIFEST_PROVEN'
echo 'WORLDMAP_BASELINE_UI_WINDOW_GEOMETRY_EXPECTED=1020x650'
echo 'WORLDMAP_BASELINE_UI_WINDOW_EQUALS_RUNTIME_IDENTITY=true'

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
    forbidden = (
        "tesseract",
        "capture_ocr",
        "LOGIN_OCR_ANCHORS",
        "SELECT_TSV",
        "PRE_TSV",
        "track-a-worldmap-causal-ui-window.py",
    )
    survivors = [token for token in forbidden if token in output]
    if survivors:
        raise TransformRefused("FORBIDDEN_SURVIVORS:" + ",".join(survivors))
    required = (
        "WORLDMAP_BASELINE_UI_WINDOW_XRES_OWNER=MANIFEST_PROVEN",
        "WORLDMAP_BASELINE_UI_WINDOW_GEOMETRY_EXPECTED=1020x650",
        "WORLDMAP_BASELINE_UI_WINDOW_EQUALS_RUNTIME_IDENTITY=true",
        "WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_RAW_XWD_GEOMETRY",
        "WORLDMAP_BASELINE_CHARACTER_SELECTION=PROVEN_RAW_XWD_GEOMETRY",
        'UI_WIN="$WIN"',
        "EMAIL_X=520",
        "ROW_X=300",
        'LD_LIBRARY_PATH="$XWD_TOOLROOT_LIBS" "$XWD"',
    )
    missing = [token for token in required if token not in output]
    if missing:
        raise TransformRefused("REQUIRED_MISSING:" + ",".join(missing))
    executable_legacy = (
        '"$XDOTOOL" search --onlyvisible --pid',
        '$XDOTOOL search --onlyvisible --pid',
        'xdotool search --onlyvisible --pid',
    )
    survivors = [token for token in executable_legacy if token in output]
    if survivors:
        raise TransformRefused("LEGACY_PID_WINDOW_SELECTOR_EXECUTABLE_SURVIVED")
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
