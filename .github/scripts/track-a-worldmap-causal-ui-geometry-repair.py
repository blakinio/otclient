#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


START = "# Native pre-secret UI gate: no OCR and no credential-bearing environment.\n"

PRESECRET_TAIL = r'''# Native pre-secret UI gate v2: inspect/capture the exact manifest-owned XID.
# Do not resize, reparent, recreate, replace, or globally rediscover the client window.
echo 'WORLDMAP_BASELINE_NATIVE_PRESECRET_GATE_VERSION=2'
XWD="$(command -v xwd 2>/dev/null || true)"
[[ -n "$XWD" ]] || XWD="$(find "$TOOL" -xdev -type f -name xwd -perm -111 -print -quit 2>/dev/null || true)"
COMPARE="${GITHUB_WORKSPACE:-$PWD}/.github/scripts/track-a-worldmap-causal-xwd-compare.py"
TOPOLOGY="${GITHUB_WORKSPACE:-$PWD}/.github/scripts/track-a-worldmap-causal-ui-window.py"
OWNER="${GITHUB_WORKSPACE:-$PWD}/.github/scripts/tibia-official-client-re-xres-window-owner.py"
WIRE="${GITHUB_WORKSPACE:-$PWD}/.github/scripts/tibia-official-client-re-xres-wire.py"
[[ -x "$XWD" ]] || fail xwd_missing_before_secret_use
[[ -f "$COMPARE" && -f "$TOPOLOGY" && -f "$OWNER" && -f "$WIRE" ]] || fail presecret_geometry_helper_missing
[[ ${TIBIA_TEST_EMAIL+x} != x && ${TIBIA_TEST_PASSWORD+x} != x ]] || fail secret_env_present_before_editability_gates

UI_WIN="$WIN"
[[ "$UI_WIN" =~ ^[1-9][0-9]*$ ]] || fail manifest_ui_window_invalid
echo "WORLDMAP_BASELINE_UI_WINDOW_IDENTITY=x11-window:$UI_WIN"
echo 'WORLDMAP_BASELINE_UI_WINDOW_XRES_OWNER=MANIFEST_PROVEN'
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

TOPOLOGY_OUT="$(python3 "$TOPOLOGY" \
  --display "$DISPLAY" --pid "$PID" --xid "$UI_WIN" --toolroot "$TOOL" \
  --owner-helper "$OWNER" --wire-helper "$WIRE" 2>&1)" || {
    printf '%s\n' "$TOPOLOGY_OUT"
    fail exact_manifest_window_topology_unproven
  }
printf '%s\n' "$TOPOLOGY_OUT"
ACTUAL_GEOMETRY="$(awk -F= '/^WORLDMAP_UI_EXACT_GEOMETRY=/{print $2}' <<<"$TOPOLOGY_OUT" | tail -1)"
ROOT_GEOMETRY="$(awk -F= '/^WORLDMAP_UI_ROOT_GEOMETRY=/{print $2}' <<<"$TOPOLOGY_OUT" | tail -1)"
PARENT_RELATION="$(awk -F= '/^WORLDMAP_UI_PARENT_RELATION=/{print $2}' <<<"$TOPOLOGY_OUT" | tail -1)"
[[ "$ACTUAL_GEOMETRY" =~ ^([1-9][0-9]*)x([1-9][0-9]*)$ ]] || fail exact_manifest_window_geometry_invalid
ACTUAL_WIDTH="${BASH_REMATCH[1]}"
ACTUAL_HEIGHT="${BASH_REMATCH[2]}"
[[ "$ROOT_GEOMETRY" =~ ^[1-9][0-9]*x[1-9][0-9]*$ ]] || fail root_geometry_invalid
[[ "$PARENT_RELATION" == DIRECT_ROOT_CHILD || "$PARENT_RELATION" == REPARENTED_OR_NESTED ]] || fail parent_relation_invalid
echo "WORLDMAP_BASELINE_UI_WINDOW_GEOMETRY_ACTUAL=$ACTUAL_GEOMETRY"
echo "WORLDMAP_BASELINE_ROOT_DISPLAY_GEOMETRY=$ROOT_GEOMETRY"
echo "WORLDMAP_BASELINE_UI_PARENT_RELATION=$PARENT_RELATION"

GEOMETRY_XWD="$ROOT/presecret-geometry-witness.xwd"
capture_xwd "$GEOMETRY_XWD"
XWD_INSPECT="$(python3 "$COMPARE" inspect "$GEOMETRY_XWD" \
  --expected-width "$ACTUAL_WIDTH" --expected-height "$ACTUAL_HEIGHT" 2>&1)" || {
    printf '%s\n' "$XWD_INSPECT"
    rm -f "$GEOMETRY_XWD"
    fail xwd_exact_window_geometry_mismatch
  }
printf '%s\n' "$XWD_INSPECT"
CAPTURE_GEOMETRY="$(awk -F= '/^WORLDMAP_XWD_PIXMAP_GEOMETRY=/{print $2}' <<<"$XWD_INSPECT" | tail -1)"
HEADER_WINDOW_GEOMETRY="$(awk -F= '/^WORLDMAP_XWD_WINDOW_GEOMETRY=/{print $2}' <<<"$XWD_INSPECT" | tail -1)"
rm -f "$GEOMETRY_XWD"
[[ "$CAPTURE_GEOMETRY" == "$ACTUAL_GEOMETRY" && "$HEADER_WINDOW_GEOMETRY" == "$ACTUAL_GEOMETRY" ]] || fail xwd_header_geometry_not_exact_manifest_window
echo "WORLDMAP_BASELINE_XWD_CAPTURED_GEOMETRY=$CAPTURE_GEOMETRY"
echo "WORLDMAP_BASELINE_XWD_HEADER_WINDOW_GEOMETRY=$HEADER_WINDOW_GEOMETRY"
echo 'WORLDMAP_BASELINE_XWD_CAPTURE_TARGET_EQUALS_RUNTIME_IDENTITY=true'
echo 'WORLDMAP_BASELINE_XWD_GEOMETRY_PROOF=PASS'
echo 'WORLDMAP_BASELINE_VNC_MAPPING_PRESERVED=MANIFEST_RUNTIME_UNCHANGED'

echo 'WORLDMAP_BASELINE_LOGIN_UI_TOOLING=RAW_XWD_DYNAMIC_EXACT_WINDOW_BEHAVIOR_PASS'
echo 'WORLDMAP_PRELOGIN_ADAPTIVE_FIELD_SCAN_SECRET_ENV=ABSENT'
echo 'WORLDMAP_PRELOGIN_ADAPTIVE_FIELD_SCAN_MODE=TAB_TEXT_GROWTH_AND_MASK_VARIANT_NO_COORDINATES'

META="$ROOT/presecret-field-candidates.tsv"
: >"$META"
chmod 600 "$META"

capture_semantics() {
  local prefix="$1" short_text="$2" long_text="$3"
  local idle0="$ROOT/$prefix-idle0.xwd" idle1="$ROOT/$prefix-idle1.xwd" idle2="$ROOT/$prefix-idle2.xwd"
  local short="$ROOT/$prefix-short.xwd" clear_short="$ROOT/$prefix-clear-short.xwd"
  local long="$ROOT/$prefix-long.xwd" clear_long="$ROOT/$prefix-clear-long.xwd" idle3="$ROOT/$prefix-idle3.xwd"

  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
  sleep .18
  capture_xwd "$idle0"; sleep .18; capture_xwd "$idle1"; sleep .18; capture_xwd "$idle2"
  xdo type --window "$UI_WIN" --delay 10 -- "$short_text"; sleep .20; capture_xwd "$short"
  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace; sleep .20; capture_xwd "$clear_short"
  xdo type --window "$UI_WIN" --delay 10 -- "$long_text"; sleep .20; capture_xwd "$long"
  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace; sleep .20; capture_xwd "$clear_long"
  sleep .20; capture_xwd "$idle3"

  set +e
  SEM_OUT="$(python3 "$COMPARE" text-semantics \
    "$idle0" "$idle1" "$idle2" "$short" "$clear_short" "$long" "$clear_long" "$idle3" 2>&1)"
  SEM_RC=$?
  set -e
  rm -f "$idle0" "$idle1" "$idle2" "$short" "$clear_short" "$long" "$clear_long" "$idle3"
}

xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
xdo windowfocus --sync "$UI_WIN"

for idx in $(seq 0 15); do
  capture_semantics "presecret-$idx-text" 'abc' 'abcdefghijklm'
  if [[ "$SEM_RC" -eq 0 ]]; then
    text_bbox="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_LONG_BBOX=/{print $2}' <<<"$SEM_OUT" | tail -1)"
    text_signal="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_LONG_SIGNAL=/{print $2}' <<<"$SEM_OUT" | tail -1)"
    [[ "$text_bbox" =~ ^[0-9]+,[0-9]+,[0-9]+,[0-9]+$ && "$text_signal" =~ ^[0-9]+$ ]] || fail adaptive_text_metric_invalid

    capture_semantics "presecret-$idx-variant" 'iiiiii' 'WWWWWW'
    i_bbox="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_SHORT_BBOX=/{print $2}' <<<"$SEM_OUT" | tail -1)"
    w_bbox="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_LONG_BBOX=/{print $2}' <<<"$SEM_OUT" | tail -1)"
    i_signal="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_SHORT_SIGNAL=/{print $2}' <<<"$SEM_OUT" | tail -1)"
    w_signal="$(awk -F= '/^WORLDMAP_TEXT_SEMANTICS_LONG_SIGNAL=/{print $2}' <<<"$SEM_OUT" | tail -1)"
    [[ "$i_bbox" =~ ^[0-9]+,[0-9]+,[0-9]+,[0-9]+$ && "$w_bbox" =~ ^[0-9]+,[0-9]+,[0-9]+,[0-9]+$ ]] || fail adaptive_variant_bbox_invalid
    [[ "$i_signal" =~ ^[0-9]+$ && "$w_signal" =~ ^[0-9]+$ ]] || fail adaptive_variant_signal_invalid
    VARIANT_OUT="$(python3 "$COMPARE" variant "$i_bbox" "$w_bbox" "$i_signal" "$w_signal" \
      --width "$ACTUAL_WIDTH" --height "$ACTUAL_HEIGHT" 2>&1)" || fail adaptive_variant_classifier_failed
    variant_class="$(awk -F= '/^WORLDMAP_TEXT_VARIANT_CLASS=/{print $2}' <<<"$VARIANT_OUT" | tail -1)"
    ratio="$(awk -F= '/^WORLDMAP_TEXT_VARIANT_WIDTH_RATIO=/{print $2}' <<<"$VARIANT_OUT" | tail -1)"
    case "$variant_class" in
      MASKED_LIKE|UNMASKED_LIKE)
        printf '%s\t%s\t%s\t%s\t%s\n' "$idx" "$variant_class" "$text_bbox" "$text_signal" "$ratio" >>"$META"
        echo "WORLDMAP_PRELOGIN_ADAPTIVE_TEXT_FIELD=tab:$idx;bbox:$text_bbox;signal:$text_signal;variant:$variant_class;width_ratio:$ratio"
        ;;
      AMBIGUOUS) ;;
      *) fail adaptive_variant_class_invalid ;;
    esac
  fi
  xdo key --window "$UI_WIN" --clearmodifiers Tab
  sleep .12
done

FIELD_JSON="$(python3 - "$META" "$ACTUAL_WIDTH" "$ACTUAL_HEIGHT" <<'PY'
import json, sys
from pathlib import Path

path=Path(sys.argv[1]); width=int(sys.argv[2]); height=int(sys.argv[3])
rows=[]
for line in path.read_text().splitlines():
    if not line.strip():
        continue
    tab_s,variant,bbox_s,signal_s,ratio_s=line.split('\t')
    x0,y0,x1,y1=(int(v) for v in bbox_s.split(','))
    if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height):
        raise SystemExit('candidate_bbox_out_of_bounds')
    rows.append({'tab':int(tab_s),'variant':variant,'bbox':[x0,y0,x1,y1],'signal':int(signal_s),'ratio':float(ratio_s)})

def same(a,b):
    ax0,ay0,ax1,ay1=a['bbox']; bx0,by0,bx1,by1=b['bbox']
    ix=max(0,min(ax1,bx1)-max(ax0,bx0)); iy=max(0,min(ay1,by1)-max(ay0,by0))
    inter=ix*iy; aa=(ax1-ax0)*(ay1-ay0); ba=(bx1-bx0)*(by1-by0)
    if min(aa,ba) and inter/min(aa,ba) >= 0.55:
        return True
    acx=(ax0+ax1)/2; acy=(ay0+ay1)/2; bcx=(bx0+bx1)/2; bcy=(by0+by1)/2
    return abs(acx-bcx) <= max(30,width*0.025) and abs(acy-bcy) <= max(20,height*0.025)

def clusters(kind):
    groups=[]
    for row in [r for r in rows if r['variant']==kind]:
        for group in groups:
            if any(same(row,old) for old in group):
                group.append(row); break
        else:
            groups.append([row])
    return groups

def representative(group):
    return max(group,key=lambda r:(r['signal'],-r['tab']))

unmasked=clusters('UNMASKED_LIKE'); masked=clusters('MASKED_LIKE')
if len(unmasked) != 1 or len(masked) != 1:
    raise SystemExit(f'unique_field_classes_required:unmasked={len(unmasked)};masked={len(masked)}')
email=representative(unmasked[0]); password=representative(masked[0])
def center(row):
    x0,y0,x1,y1=row['bbox']; return ((x0+x1)//2,(y0+y1)//2)
ex,ey=center(email); px,py=center(password)
if not ey < py:
    raise SystemExit('field_vertical_order_invalid')
if abs(ex-px) > max(250,width//4):
    raise SystemExit('field_horizontal_alignment_invalid')
if py-ey > max(220,height//3):
    raise SystemExit('field_vertical_spacing_invalid')
print(json.dumps({
    'candidate_rows':len(rows),
    'unmasked_clusters':len(unmasked),
    'masked_clusters':len(masked),
    'email_tab':email['tab'],'password_tab':password['tab'],
    'email_bbox':','.join(str(v) for v in email['bbox']),
    'password_bbox':','.join(str(v) for v in password['bbox']),
    'email_x':ex,'email_y':ey,'password_x':px,'password_y':py,
},sort_keys=True,separators=(',',':')))
PY
)" || fail adaptive_unique_email_password_discriminator_failed
rm -f "$META"

EMAIL_X="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["email_x"])' "$FIELD_JSON")"
EMAIL_Y="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["email_y"])' "$FIELD_JSON")"
PASS_X="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["password_x"])' "$FIELD_JSON")"
PASS_Y="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["password_y"])' "$FIELD_JSON")"
EMAIL_TAB="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["email_tab"])' "$FIELD_JSON")"
PASS_TAB="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["password_tab"])' "$FIELD_JSON")"
EMAIL_BBOX="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["email_bbox"])' "$FIELD_JSON")"
PASS_BBOX="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["password_bbox"])' "$FIELD_JSON")"
echo "WORLDMAP_BASELINE_EMAIL_FIELD_DISCOVERY=tab:$EMAIL_TAB;bbox:$EMAIL_BBOX;variant:UNMASKED_LIKE"
echo "WORLDMAP_BASELINE_PASSWORD_FIELD_DISCOVERY=tab:$PASS_TAB;bbox:$PASS_BBOX;variant:MASKED_LIKE"

probe_discovered_field() {
  local name="$1" x="$2" y="$3" dummy="$4"
  local idle0="$ROOT/$name-final-idle0.xwd" idle1="$ROOT/$name-final-idle1.xwd" idle2="$ROOT/$name-final-idle2.xwd"
  local typed="$ROOT/$name-final-typed.xwd" cleared="$ROOT/$name-final-cleared.xwd" idle3="$ROOT/$name-final-idle3.xwd"
  xdo mousemove --window "$UI_WIN" "$x" "$y" click 1
  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
  capture_xwd "$idle0"; sleep .18; capture_xwd "$idle1"; sleep .18; capture_xwd "$idle2"
  xdo type --window "$UI_WIN" --delay 10 -- "$dummy"; sleep .20; capture_xwd "$typed"
  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace; sleep .20; capture_xwd "$cleared"; sleep .20; capture_xwd "$idle3"
  set +e
  out="$(python3 "$COMPARE" controlled-cycle "$idle0" "$idle1" "$idle2" "$typed" "$cleared" "$idle3" \
    --min-signal 25 --min-overlap-ratio 0.55 --max-width 700 --max-height 160 --max-area 60000 2>&1)"
  rc=$?
  set -e
  rm -f "$idle0" "$idle1" "$idle2" "$typed" "$cleared" "$idle3"
  [[ "$rc" -eq 0 ]] || { printf '%s\n' "$out"; fail "${name}_editable_probe_failed"; }
}

probe_discovered_field email "$EMAIL_X" "$EMAIL_Y" 'wm-probe@example.invalid'
echo 'WORLDMAP_BASELINE_EMAIL_FIELD_EDITABLE=PASS'
probe_discovered_field password "$PASS_X" "$PASS_Y" 'wm-probe-7'
echo 'WORLDMAP_BASELINE_PASSWORD_FIELD_EDITABLE=PASS'
echo 'WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_EDITABLE_FIELDS'

xdo mousemove --window "$UI_WIN" "$EMAIL_X" "$EMAIL_Y" click 1
xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
xdo mousemove --window "$UI_WIN" "$PASS_X" "$PASS_Y" click 1
xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
[[ ${TIBIA_TEST_EMAIL+x} != x && ${TIBIA_TEST_PASSWORD+x} != x ]] || fail secret_env_present_before_handoff_gate
rm -f "$CRED_FIFO" "$READY" "$CONTROL/presecret.stop"
mkfifo -m 600 "$CRED_FIFO"
printf '%s\n' 'WORLDMAP_BASELINE_PRESECRET_READY=true' >"$READY.tmp"
chmod 600 "$READY.tmp"
mv -f "$READY.tmp" "$READY"
echo 'WORLDMAP_BASELINE_PRESECRET_READY=true'
echo 'WORLDMAP_BASELINE_PRESECRET_ONLY_COMPLETE=true'

for _ in $(seq 1 600); do
  [[ -f "$CONTROL/presecret.stop" ]] && exit 0
  sleep .5
done
fail presecret_only_stop_timeout
'''


class TransformRefused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(START) != 1:
        raise TransformRefused(f"NATIVE_PRESECRET_START_COUNT:{text.count(START)}")
    start = text.index(START)
    output = text[:start] + PRESECRET_TAIL

    forbidden = (
        "WORLDMAP_BASELINE_LOGIN_SUBMITTED=true",
        "WORLDMAP_BASELINE_CHARACTER_ACTIVATION_SENT=true",
        "WORLDMAP_BASELINE_RIGHT_SENT=true",
        "WORLDMAP_BASELINE_LEFT_SENT=true",
        "credential_email_handoff_timeout",
        "credential_password_handoff_timeout",
        "EMAIL_SECRET",
        "PASSWORD_SECRET",
        "-screen 0 1020x650x24",
        'UI_WIN="$(python3',
        "track-a-worldmap-causal-screen-geometry-repair.py",
    )
    survivors = [token for token in forbidden if token in output]
    if survivors:
        raise TransformRefused("FORBIDDEN_SURVIVORS:" + ",".join(survivors))

    required = (
        'UI_WIN="$WIN"',
        '"$XWD" -silent -id "$UI_WIN"',
        "WORLDMAP_BASELINE_UI_WINDOW_EQUALS_RUNTIME_IDENTITY=true",
        "WORLDMAP_BASELINE_XWD_CAPTURE_TARGET_EQUALS_RUNTIME_IDENTITY=true",
        "WORLDMAP_BASELINE_XWD_GEOMETRY_PROOF=PASS",
        "WORLDMAP_BASELINE_VNC_MAPPING_PRESERVED=MANIFEST_RUNTIME_UNCHANGED",
        "track-a-worldmap-causal-ui-window.py",
        "track-a-worldmap-causal-xwd-compare.py",
        "text-semantics",
        "variant",
        "WORLDMAP_BASELINE_EMAIL_FIELD_EDITABLE=PASS",
        "WORLDMAP_BASELINE_PASSWORD_FIELD_EDITABLE=PASS",
        "WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_EDITABLE_FIELDS",
        "WORLDMAP_BASELINE_PRESECRET_READY=true",
        "WORLDMAP_BASELINE_PRESECRET_ONLY_COMPLETE=true",
        'mkfifo -m 600 "$CRED_FIFO"',
    )
    missing = [token for token in required if token not in output]
    if missing:
        raise TransformRefused("REQUIRED_MISSING:" + ",".join(missing))

    if output.count('UI_WIN="$WIN"') != 1:
        raise TransformRefused("MANIFEST_WINDOW_IDENTITY_NOT_UNIQUE")
    if "xwd -root" in output or '"$XWD" -root' in output:
        raise TransformRefused("ROOT_CAPTURE_FORBIDDEN")
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
