#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

START = "echo 'WORLDMAP_PRELOGIN_ADAPTIVE_FIELD_SCAN_MODE=TAB_TEXT_GROWTH_AND_MASK_VARIANT_NO_COORDINATES'\n"
END = "probe_discovered_field() {\n"

REPLACEMENT = r'''echo 'WORLDMAP_PRELOGIN_ADAPTIVE_FIELD_SCAN_MODE=TAB_CONTROLLED_CYCLE_THEN_MASK_VARIANT_V3'

META="$ROOT/presecret-field-candidates.tsv"
: >"$META"
chmod 600 "$META"

capture_controlled() {
  local prefix="$1" text="$2"
  local idle0="$ROOT/$prefix-idle0.xwd" idle1="$ROOT/$prefix-idle1.xwd" idle2="$ROOT/$prefix-idle2.xwd"
  local typed="$ROOT/$prefix-typed.xwd" cleared="$ROOT/$prefix-cleared.xwd" idle3="$ROOT/$prefix-idle3.xwd"

  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
  sleep .18
  capture_xwd "$idle0"; sleep .18; capture_xwd "$idle1"; sleep .18; capture_xwd "$idle2"
  xdo type --window "$UI_WIN" --delay 10 -- "$text"; sleep .20; capture_xwd "$typed"
  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace; sleep .20; capture_xwd "$cleared"
  sleep .20; capture_xwd "$idle3"

  set +e
  CONTROLLED_OUT="$(python3 "$COMPARE" controlled-cycle \
    "$idle0" "$idle1" "$idle2" "$typed" "$cleared" "$idle3" \
    --min-signal 25 --min-overlap-ratio 0.55 \
    --max-width 700 --max-height 160 --max-area 60000 2>&1)"
  CONTROLLED_RC=$?
  set -e
  rm -f "$idle0" "$idle1" "$idle2" "$typed" "$cleared" "$idle3"
}

scan_round() {
  local round="$1" idx base_bbox base_signal base_overlap base_noise
  local i_bbox i_signal w_bbox w_signal variant_class ratio

  xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
  xdo windowfocus --sync "$UI_WIN"

  for idx in $(seq 0 15); do
    capture_controlled "v3-$round-$idx-base" 'wmprobe7'
    base_bbox="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_SIGNAL_BBOX=/{print $2}' <<<"$CONTROLLED_OUT" | tail -1)"
    base_signal="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_SIGNAL_CHANGED=/{print $2}' <<<"$CONTROLLED_OUT" | tail -1)"
    base_overlap="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_OVERLAP_RATIO=/{print $2}' <<<"$CONTROLLED_OUT" | tail -1)"
    base_noise="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_NOISE_PIXELS=/{print $2}' <<<"$CONTROLLED_OUT" | tail -1)"
    echo "WORLDMAP_PRELOGIN_V3_EDITABLE_METRIC=round:$round;tab:$idx;noise:${base_noise:-UNKNOWN};signal:${base_signal:-UNKNOWN};overlap:${base_overlap:-UNKNOWN};bbox:${base_bbox:-NONE};pass:$([[ "$CONTROLLED_RC" -eq 0 ]] && echo true || echo false)"

    if [[ "$CONTROLLED_RC" -eq 0 ]]; then
      [[ "$base_bbox" =~ ^[0-9]+,[0-9]+,[0-9]+,[0-9]+$ && "$base_signal" =~ ^[0-9]+$ ]] || fail v3_base_metric_invalid

      capture_controlled "v3-$round-$idx-i" 'iiiiii'
      if [[ "$CONTROLLED_RC" -eq 0 ]]; then
        i_bbox="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_SIGNAL_BBOX=/{print $2}' <<<"$CONTROLLED_OUT" | tail -1)"
        i_signal="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_SIGNAL_CHANGED=/{print $2}' <<<"$CONTROLLED_OUT" | tail -1)"
        capture_controlled "v3-$round-$idx-w" 'WWWWWW'
        if [[ "$CONTROLLED_RC" -eq 0 ]]; then
          w_bbox="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_SIGNAL_BBOX=/{print $2}' <<<"$CONTROLLED_OUT" | tail -1)"
          w_signal="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_SIGNAL_CHANGED=/{print $2}' <<<"$CONTROLLED_OUT" | tail -1)"
          [[ "$i_bbox" =~ ^[0-9]+,[0-9]+,[0-9]+,[0-9]+$ && "$w_bbox" =~ ^[0-9]+,[0-9]+,[0-9]+,[0-9]+$ ]] || fail v3_variant_bbox_invalid
          [[ "$i_signal" =~ ^[0-9]+$ && "$w_signal" =~ ^[0-9]+$ ]] || fail v3_variant_signal_invalid
          VARIANT_OUT="$(python3 "$COMPARE" variant "$i_bbox" "$w_bbox" "$i_signal" "$w_signal" \
            --width "$ACTUAL_WIDTH" --height "$ACTUAL_HEIGHT" 2>&1)" || fail v3_variant_classifier_failed
          variant_class="$(awk -F= '/^WORLDMAP_TEXT_VARIANT_CLASS=/{print $2}' <<<"$VARIANT_OUT" | tail -1)"
          ratio="$(awk -F= '/^WORLDMAP_TEXT_VARIANT_WIDTH_RATIO=/{print $2}' <<<"$VARIANT_OUT" | tail -1)"
          echo "WORLDMAP_PRELOGIN_V3_VARIANT_METRIC=round:$round;tab:$idx;base_bbox:$base_bbox;i_bbox:$i_bbox;w_bbox:$w_bbox;i_signal:$i_signal;w_signal:$w_signal;class:$variant_class;width_ratio:$ratio"
          case "$variant_class" in
            MASKED_LIKE|UNMASKED_LIKE)
              printf '%s\t%s\t%s\t%s\t%s\n' "$idx" "$variant_class" "$base_bbox" "$base_signal" "$ratio" >>"$META"
              ;;
            AMBIGUOUS) ;;
            *) fail v3_variant_class_invalid ;;
          esac
        fi
      fi
    fi

    xdo key --window "$UI_WIN" --clearmodifiers Tab
    sleep .12
  done
}

# Materially changed hypothesis versus the failed v2 run: allow the startup
# surface to settle, prove generic local editability first, and only then run
# the equal-length masked/unmasked classifier on the same focus state.
sleep 15
scan_round 1
if [[ ! -s "$META" ]]; then
  echo 'WORLDMAP_PRELOGIN_V3_FIRST_ROUND=no_classified_candidate'
  sleep 15
  scan_round 2
fi

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

def center(row):
    x0,y0,x1,y1=row['bbox']; return ((x0+x1)//2,(y0+y1)//2)

unmasked=clusters('UNMASKED_LIKE'); masked=clusters('MASKED_LIKE')
if len(unmasked) != 1 or len(masked) != 1:
    raise SystemExit(f'unique_field_classes_required:unmasked={len(unmasked)};masked={len(masked)};rows={len(rows)}')
email=representative(unmasked[0]); password=representative(masked[0])
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
)" || fail v3_unique_email_password_discriminator_failed
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
'''

class TransformRefused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(START) != 1:
        raise TransformRefused(f"START_COUNT:{text.count(START)}")
    if text.count(END) != 1:
        raise TransformRefused(f"END_COUNT:{text.count(END)}")
    start=text.index(START)
    end=text.index(END,start)
    output=text[:start] + REPLACEMENT + text[end+len(END):]
    forbidden=(
        'TAB_TEXT_GROWTH_AND_MASK_VARIANT_NO_COORDINATES',
        'capture_semantics()',
        ' text-semantics ',
    )
    survivors=[token for token in forbidden if token in output]
    if survivors:
        raise TransformRefused('OLD_DISCRIMINATOR_SURVIVED:'+','.join(survivors))
    required=(
        'TAB_CONTROLLED_CYCLE_THEN_MASK_VARIANT_V3',
        'capture_controlled()',
        'controlled-cycle',
        "'wmprobe7'",
        "'iiiiii'",
        "'WWWWWW'",
        'WORLDMAP_PRELOGIN_V3_EDITABLE_METRIC=',
        'WORLDMAP_PRELOGIN_V3_VARIANT_METRIC=',
        'v3_unique_email_password_discriminator_failed',
        'probe_discovered_field() {',
        'WORLDMAP_BASELINE_EMAIL_FIELD_EDITABLE=PASS',
        'WORLDMAP_BASELINE_PASSWORD_FIELD_EDITABLE=PASS',
        'WORLDMAP_BASELINE_PRESECRET_READY=true',
    )
    missing=[token for token in required if token not in output]
    if missing:
        raise TransformRefused('REQUIRED_MISSING:'+','.join(missing))
    if output.count('UI_WIN="$WIN"') != 1:
        raise TransformRefused('MANIFEST_WINDOW_IDENTITY_NOT_UNIQUE')
    if '"$XWD" -root' in output or 'xwd -root' in output:
        raise TransformRefused('ROOT_CAPTURE_FORBIDDEN')
    if 'WORLDMAP_BASELINE_LOGIN_SUBMITTED=true' in output:
        raise TransformRefused('LOGIN_PATH_SURVIVED')
    return output


def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument('source',type=Path)
    p.add_argument('output',type=Path)
    args=p.parse_args()
    try:
        out=transform(args.source.read_text(encoding='utf-8'))
    except TransformRefused as exc:
        print(f'WORLDMAP_UI_FIELD_V3_REPAIR_REFUSED={exc}')
        return 44
    args.output.write_text(out,encoding='utf-8')
    args.output.chmod(0o700)
    print('WORLDMAP_UI_FIELD_V3_REPAIR=PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
