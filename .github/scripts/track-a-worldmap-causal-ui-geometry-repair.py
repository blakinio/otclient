#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


START = "# Screenshot/OCR is used only to locate login/character-selection controls. No screenshot or OCR text is retained.\n"
END = "world=0\n"

REPLACEMENT = r'''# Raw XWD is used only as a transient, aggregate interaction discriminator.
# The task-owned desktop has already been normalized to 1020x650 before launch.
XWD="$(command -v xwd 2>/dev/null || true)"
[[ -n "$XWD" ]] || XWD="$(find "$TOOL" -xdev -type f -name xwd -perm -111 -print -quit 2>/dev/null || true)"
COMPARE="${GITHUB_WORKSPACE:-$PWD}/.github/scripts/track-a-worldmap-causal-xwd-compare.py"
[[ -x "$XWD" ]] || fail xwd_missing_before_secret_use
[[ -f "$COMPARE" ]] || fail xwd_compare_missing

# WIN came from the worker manifest only after raw-XRes LocalClientPid matched the
# exact task-owned client PID under the task-local 1020x650 owner helper.
UI_WIN="$WIN"
[[ "$UI_WIN" =~ ^[1-9][0-9]*$ ]] || fail manifest_ui_window_invalid
echo "WORLDMAP_BASELINE_UI_WINDOW_IDENTITY=x11-window:$UI_WIN"
echo 'WORLDMAP_BASELINE_UI_WINDOW_XRES_OWNER=MANIFEST_PROVEN'
echo 'WORLDMAP_BASELINE_UI_WINDOW_GEOMETRY_EXPECTED=1020x650'
echo 'WORLDMAP_BASELINE_UI_WINDOW_EQUALS_RUNTIME_IDENTITY=true'

XWD_TOOLROOT_LIBS="$TOOL/usr/lib/x86_64-linux-gnu:$TOOL/lib/x86_64-linux-gnu"
XDO_TOOLROOT_LIBS="$XWD_TOOLROOT_LIBS"
capture_xwd() {
  local outfile="$1"
  if [[ "$XWD" == "$TOOL/"* ]]; then
    DISPLAY="$DISPLAY" LD_LIBRARY_PATH="$XWD_TOOLROOT_LIBS" "$XWD" -silent -id "$UI_WIN" -out "$outfile"
  else
    DISPLAY="$DISPLAY" "$XWD" -silent -id "$UI_WIN" -out "$outfile"
  fi
}
xdo() {
  DISPLAY="$DISPLAY" LD_LIBRARY_PATH="$XDO_TOOLROOT_LIBS" "$XDOTOOL" "$@"
}

# Historical exact-client 1020x650 coordinates are taken from the effective
# software-world login/character-entry workflow, not inferred from text/OCR.
EMAIL_X=535
EMAIL_Y=275
PASS_X=535
PASS_Y=304
LOGIN_X=590
LOGIN_Y=388
ROW_X=285
ROW_Y=193

xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
xdo windowfocus --sync "$UI_WIN"

echo 'WORLDMAP_BASELINE_LOGIN_UI_TOOLING=RAW_XWD_AGGREGATE_BEHAVIOR_PASS'

# Prove both expected login fields are editable using harmless dummy text before
# any credential is exposed. Raw XWDs never leave the task namespace and are
# deleted immediately after aggregate changed-pixel classification.
probe_editable_field() {
  local name="$1"
  local x="$2"
  local y="$3"
  local dummy="$4"
  local x0="$5"
  local y0="$6"
  local x1="$7"
  local y1="$8"
  local before="$ROOT/$name-before.xwd"
  local typed="$ROOT/$name-typed.xwd"
  local cleared="$ROOT/$name-cleared.xwd"

  xdo mousemove --window "$UI_WIN" "$x" "$y" click 1
  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
  sleep .20
  capture_xwd "$before"
  xdo type --window "$UI_WIN" --delay 10 -- "$dummy"
  sleep .25
  capture_xwd "$typed"
  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
  sleep .25
  capture_xwd "$cleared"
  if ! python3 "$COMPARE" roi-cycle "$before" "$typed" "$cleared" \
      "$x0" "$y0" "$x1" "$y1" --min-changed 60; then
    rm -f "$before" "$typed" "$cleared"
    fail "${name}_editable_probe_failed"
  fi
  rm -f "$before" "$typed" "$cleared"
}

probe_editable_field email "$EMAIL_X" "$EMAIL_Y" 'wm-probe@example.invalid' 330 255 720 293
echo 'WORLDMAP_BASELINE_EMAIL_FIELD_EDITABLE=PASS'
probe_editable_field password "$PASS_X" "$PASS_Y" 'wm-probe-7' 330 289 720 325
echo 'WORLDMAP_BASELINE_PASSWORD_FIELD_EDITABLE=PASS'
echo 'WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_EDITABLE_FIELDS'

# Capture a blank, no-secret reference after both dummy probes have been cleared.
PRELOGIN_REFERENCE="$ROOT/prelogin-reference.xwd"
xdo mousemove --window "$UI_WIN" "$EMAIL_X" "$EMAIL_Y" click 1
xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
xdo mousemove --window "$UI_WIN" "$PASS_X" "$PASS_Y" click 1
xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
sleep .25
capture_xwd "$PRELOGIN_REFERENCE"

# Only now may the bounded baseline credential submission occur.
xdo mousemove --window "$UI_WIN" "$EMAIL_X" "$EMAIL_Y" click 1
xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
printf '%s' "$TIBIA_TEST_EMAIL" | xdo type --window "$UI_WIN" --delay 10 --file -
xdo mousemove --window "$UI_WIN" "$PASS_X" "$PASS_Y" click 1
xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
printf '%s' "$TIBIA_TEST_PASSWORD" | xdo type --window "$UI_WIN" --delay 10 --file -
xdo mousemove --window "$UI_WIN" "$LOGIN_X" "$LOGIN_Y" click 1
unset TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD
echo 'WORLDMAP_BASELINE_LOGIN_SUBMITTED=true'

# Require a large aggregate visual transition from the blank login reference.
# This is only a UI transition gate; authoritative IN_GAME proof remains FullMap
# plus map-description records from the already-armed pre-Storage observer.
POST_LOGIN_XWD=''
for i in $(seq 1 40); do
  sleep 1
  candidate="$ROOT/post-login-$i.xwd"
  capture_xwd "$candidate"
  if python3 "$COMPARE" change "$PRELOGIN_REFERENCE" "$candidate" --min-changed 5000; then
    POST_LOGIN_XWD="$candidate"
    break
  fi
  rm -f "$candidate"
done
rm -f "$PRELOGIN_REFERENCE"
[[ -n "$POST_LOGIN_XWD" ]] || fail post_login_visual_transition_not_observed
echo 'WORLDMAP_BASELINE_POST_LOGIN_VISUAL_TRANSITION=PROVEN_AGGREGATE'

# Give the transitioned UI a bounded settle interval, then prove the historical
# first-character row is interactive by a localized aggregate pixel change from
# a single selection click before Return is sent.
sleep 3
SELECT_BEFORE="$ROOT/select-before.xwd"
SELECT_AFTER="$ROOT/select-after.xwd"
capture_xwd "$SELECT_BEFORE"
xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
xdo windowfocus --sync "$UI_WIN"
xdo mousemove --window "$UI_WIN" "$ROW_X" "$ROW_Y" click 1
sleep .35
capture_xwd "$SELECT_AFTER"
if ! python3 "$COMPARE" change "$SELECT_BEFORE" "$SELECT_AFTER" --min-changed 80 \
    --x0 100 --y0 165 --x1 900 --y1 230; then
  rm -f "$POST_LOGIN_XWD" "$SELECT_BEFORE" "$SELECT_AFTER"
  fail character_row_interaction_not_observed
fi
rm -f "$POST_LOGIN_XWD" "$SELECT_BEFORE" "$SELECT_AFTER"
echo 'WORLDMAP_BASELINE_CHARACTER_ROW_SELECTION=PROVEN_AGGREGATE'
xdo key --window "$UI_WIN" Return
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

    # The base helper still owns three post-login/movement xdotool call sites
    # after world=0. Route exactly those through the same loader-safe wrapper;
    # fail closed if upstream changes their count rather than silently missing one.
    direct_xdo = 'DISPLAY="$DISPLAY" "$XDOTOOL"'
    direct_count = output.count(direct_xdo)
    if direct_count != 3:
        raise TransformRefused(f"POST_BLOCK_DIRECT_XDOTOOL_COUNT:{direct_count}")
    output = output.replace(direct_xdo, "xdo")

    forbidden = (
        "tesseract",
        "capture_ocr",
        "LOGIN_OCR_ANCHORS",
        "SELECT_TSV",
        "PRE_TSV",
        "track-a-worldmap-causal-ui-window.py",
        "login_form_geometry_not_revalidated",
        "WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_RAW_XWD_GEOMETRY",
        "WORLDMAP_BASELINE_CHARACTER_SELECTION=PROVEN_RAW_XWD_GEOMETRY",
        direct_xdo,
    )
    survivors = [token for token in forbidden if token in output]
    if survivors:
        raise TransformRefused("FORBIDDEN_SURVIVORS:" + ",".join(survivors))
    required = (
        "WORLDMAP_BASELINE_UI_WINDOW_XRES_OWNER=MANIFEST_PROVEN",
        "WORLDMAP_BASELINE_UI_WINDOW_GEOMETRY_EXPECTED=1020x650",
        "WORLDMAP_BASELINE_UI_WINDOW_EQUALS_RUNTIME_IDENTITY=true",
        "WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_EDITABLE_FIELDS",
        "WORLDMAP_BASELINE_EMAIL_FIELD_EDITABLE=PASS",
        "WORLDMAP_BASELINE_PASSWORD_FIELD_EDITABLE=PASS",
        "WORLDMAP_BASELINE_POST_LOGIN_VISUAL_TRANSITION=PROVEN_AGGREGATE",
        "WORLDMAP_BASELINE_CHARACTER_ROW_SELECTION=PROVEN_AGGREGATE",
        "track-a-worldmap-causal-xwd-compare.py",
        'UI_WIN="$WIN"',
        "EMAIL_X=535",
        "EMAIL_Y=275",
        "PASS_X=535",
        "PASS_Y=304",
        "LOGIN_X=590",
        "LOGIN_Y=388",
        "ROW_X=285",
        "ROW_Y=193",
        'LD_LIBRARY_PATH="$XWD_TOOLROOT_LIBS" "$XWD"',
        'LD_LIBRARY_PATH="$XDO_TOOLROOT_LIBS" "$XDOTOOL"',
        "xdo windowfocus --sync",
        'xdo mousemove --window "$WIN" "$ROW_X" "$ROW_Y" click --repeat 2 --delay 120 1 key Return',
        'xdo windowactivate --sync "$WIN" key --clearmodifiers Right',
        'xdo key --clearmodifiers Left',
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
