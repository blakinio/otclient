#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

START = "echo 'WORLDMAP_PRELOGIN_ADAPTIVE_FIELD_SCAN_MODE=TAB_CONTROLLED_CYCLE_THEN_MASK_VARIANT_V3'\n"
END = "probe_discovered_field() {\n"

REPLACEMENT = r'''echo 'WORLDMAP_PRELOGIN_ADAPTIVE_FIELD_SCAN_MODE=TAB_CONTROLLED_EDITABILITY_PLUS_ROI_ECHO_V4'

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
    --min-signal 25 --min-overlap-ratio 0.55 --max-width 700 --max-height 160 --max-area 60000 2>&1)"
  CONTROLLED_RC=$?
  set -e
  rm -f "$idle0" "$idle1" "$idle2" "$typed" "$cleared" "$idle3"
}

capture_variant_roi() {
  local prefix="$1" bbox="$2"
  local x0 y0 x1 y1 rx0 ry0 rx1 ry1
  IFS=, read -r x0 y0 x1 y1 <<<"$bbox"
  [[ "$x0" =~ ^[0-9]+$ && "$y0" =~ ^[0-9]+$ && "$x1" =~ ^[0-9]+$ && "$y1" =~ ^[0-9]+$ ]] || fail v4_bbox_parse_failed
  rx0=$((x0>50 ? x0-50 : 0)); ry0=$((y0>20 ? y0-20 : 0))
  rx1=$((x1+80<ACTUAL_WIDTH ? x1+80 : ACTUAL_WIDTH)); ry1=$((y1+20<ACTUAL_HEIGHT ? y1+20 : ACTUAL_HEIGHT))
  local i0="$ROOT/$prefix-i0.xwd" i1="$ROOT/$prefix-i1.xwd" w0="$ROOT/$prefix-w0.xwd" w1="$ROOT/$prefix-w1.xwd"

  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
  xdo type --window "$UI_WIN" --delay 10 -- 'iiiiii'; sleep .22; capture_xwd "$i0"; sleep .18; capture_xwd "$i1"
  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
  xdo type --window "$UI_WIN" --delay 10 -- 'WWWWWW'; sleep .22; capture_xwd "$w0"; sleep .18; capture_xwd "$w1"
  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace

  VARIANT_ROI_OUT="$(python3 - "$COMPARE" "$i0" "$i1" "$w0" "$w1" "$rx0" "$ry0" "$rx1" "$ry1" <<'PY'
import importlib.util,sys
from pathlib import Path
compare,i0,i1,w0,w1,x0,y0,x1,y1=sys.argv[1:]
spec=importlib.util.spec_from_file_location('wm_v4_compare',compare)
if spec is None or spec.loader is None: raise SystemExit('compare_import_failed')
m=importlib.util.module_from_spec(spec); sys.modules[spec.name]=m; spec.loader.exec_module(m)
roi=tuple(map(int,(x0,y0,x1,y1)))
noise=m.changed_mask(Path(i0),Path(i1),roi) | m.changed_mask(Path(w0),Path(w1),roi)
delta=m.changed_mask(Path(i1),Path(w0),roi)-noise
fields,_,_=m.load(Path(i0))
print('WORLDMAP_V4_VARIANT_ROI_NOISE='+str(len(noise)))
print('WORLDMAP_V4_VARIANT_ROI_CHANGED='+str(len(delta)))
print('WORLDMAP_V4_VARIANT_ROI_BBOX='+m.mask_bbox(delta,fields['width']))
PY
)" || fail v4_variant_roi_compare_failed
  rm -f "$i0" "$i1" "$w0" "$w1"
}

xdo windowactivate --sync "$UI_WIN" 2>/dev/null || true
xdo windowfocus --sync "$UI_WIN"

# The v3 physical run proved startup timing mattered. Keep one bounded settle
# interval, then rediscover all local editable states from scratch on this launch.
sleep 15
for idx in $(seq 0 15); do
  capture_controlled "v4-$idx-base" 'wmprobe7'
  bbox="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_SIGNAL_BBOX=/{print $2}' <<<"$CONTROLLED_OUT" | tail -1)"
  signal="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_SIGNAL_CHANGED=/{print $2}' <<<"$CONTROLLED_OUT" | tail -1)"
  overlap="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_OVERLAP_RATIO=/{print $2}' <<<"$CONTROLLED_OUT" | tail -1)"
  noise="$(awk -F= '/^WORLDMAP_XWD_CONTROLLED_NOISE_PIXELS=/{print $2}' <<<"$CONTROLLED_OUT" | tail -1)"
  echo "WORLDMAP_PRELOGIN_V4_EDITABLE_METRIC=tab:$idx;noise:${noise:-UNKNOWN};signal:${signal:-UNKNOWN};overlap:${overlap:-UNKNOWN};bbox:${bbox:-NONE};pass:$([[ "$CONTROLLED_RC" -eq 0 ]] && echo true || echo false)"
  if [[ "$CONTROLLED_RC" -eq 0 ]]; then
    [[ "$bbox" =~ ^[0-9]+,[0-9]+,[0-9]+,[0-9]+$ && "$signal" =~ ^[0-9]+$ ]] || fail v4_editable_metric_invalid
    capture_variant_roi "v4-$idx-variant" "$bbox"
    variant_changed="$(awk -F= '/^WORLDMAP_V4_VARIANT_ROI_CHANGED=/{print $2}' <<<"$VARIANT_ROI_OUT" | tail -1)"
    variant_noise="$(awk -F= '/^WORLDMAP_V4_VARIANT_ROI_NOISE=/{print $2}' <<<"$VARIANT_ROI_OUT" | tail -1)"
    variant_bbox="$(awk -F= '/^WORLDMAP_V4_VARIANT_ROI_BBOX=/{print $2}' <<<"$VARIANT_ROI_OUT" | tail -1)"
    [[ "$variant_changed" =~ ^[0-9]+$ && "$variant_noise" =~ ^[0-9]+$ ]] || fail v4_variant_metric_invalid
    echo "WORLDMAP_PRELOGIN_V4_ECHO_METRIC=tab:$idx;base_bbox:$bbox;variant_changed:$variant_changed;variant_noise:$variant_noise;variant_bbox:$variant_bbox"
    printf '%s\t%s\t%s\t%s\n' "$idx" "$bbox" "$signal" "$variant_changed" >>"$META"
  fi
  xdo key --window "$UI_WIN" --clearmodifiers Tab
  sleep .12
done

FIELD_JSON="$(python3 - "$META" "$ACTUAL_WIDTH" "$ACTUAL_HEIGHT" <<'PY'
import json,statistics,sys
from pathlib import Path
path=Path(sys.argv[1]); width=int(sys.argv[2]); height=int(sys.argv[3])
rows=[]
for line in path.read_text().splitlines():
    if not line.strip(): continue
    tab_s,bbox_s,signal_s,delta_s=line.split('\t')
    box=tuple(int(v) for v in bbox_s.split(','))
    x0,y0,x1,y1=box
    if not (0<=x0<x1<=width and 0<=y0<y1<=height): raise SystemExit('candidate_bbox_out_of_bounds')
    rows.append({'tab':int(tab_s),'bbox':box,'signal':int(signal_s),'delta':int(delta_s)})

def same(a,b):
    ax0,ay0,ax1,ay1=a['bbox']; bx0,by0,bx1,by1=b['bbox']
    ix=max(0,min(ax1,bx1)-max(ax0,bx0)); iy=max(0,min(ay1,by1)-max(ay0,by0))
    inter=ix*iy; aa=(ax1-ax0)*(ay1-ay0); ba=(bx1-bx0)*(by1-by0)
    if min(aa,ba) and inter/min(aa,ba)>=0.55: return True
    acx=(ax0+ax1)/2; acy=(ay0+ay1)/2; bcx=(bx0+bx1)/2; bcy=(by0+by1)/2
    return abs(acx-bcx)<=max(30,width*0.025) and abs(acy-bcy)<=max(20,height*0.025)

groups=[]
for row in rows:
    for g in groups:
        if any(same(row,old) for old in g): g.append(row); break
    else: groups.append([row])

summ=[]
for g in groups:
    rep=max(g,key=lambda r:(r['signal'],-r['tab']))
    summ.append({'rep':rep,'delta':int(statistics.median(r['delta'] for r in g)),'n':len(g)})

def center(s):
    x0,y0,x1,y1=s['rep']['bbox']; return ((x0+x1)/2,(y0+y1)/2)

pairs=[]
for upper in summ:
    ux,uy=center(upper)
    if upper['delta'] < 50: continue
    for lower in summ:
        if lower is upper: continue
        lx,ly=center(lower)
        dy=ly-uy
        if not (10 <= dy <= max(140,height*0.15)): continue
        if abs(lx-ux) > max(180,width*0.12): continue
        if lower['delta'] > max(35,int(upper['delta']*0.25)): continue
        pairs.append((upper,lower))
if len(pairs)!=1:
    detail=';'.join(f"bbox={','.join(map(str,s['rep']['bbox']))},delta={s['delta']},n={s['n']}" for s in summ)
    raise SystemExit(f'unique_echo_pair_required:pairs={len(pairs)};clusters={len(summ)};{detail}')
email,password=pairs[0]
def out_center(s):
    x0,y0,x1,y1=s['rep']['bbox']; return ((x0+x1)//2,(y0+y1)//2)
ex,ey=out_center(email); px,py=out_center(password)
print(json.dumps({
 'clusters':len(summ),'rows':len(rows),
 'email_tab':email['rep']['tab'],'password_tab':password['rep']['tab'],
 'email_bbox':','.join(map(str,email['rep']['bbox'])),'password_bbox':','.join(map(str,password['rep']['bbox'])),
 'email_delta':email['delta'],'password_delta':password['delta'],
 'email_x':ex,'email_y':ey,'password_x':px,'password_y':py,
},sort_keys=True,separators=(',',':')))
PY
)" || fail v4_unique_email_password_discriminator_failed
rm -f "$META"

EMAIL_X="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["email_x"])' "$FIELD_JSON")"
EMAIL_Y="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["email_y"])' "$FIELD_JSON")"
PASS_X="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["password_x"])' "$FIELD_JSON")"
PASS_Y="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["password_y"])' "$FIELD_JSON")"
EMAIL_TAB="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["email_tab"])' "$FIELD_JSON")"
PASS_TAB="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["password_tab"])' "$FIELD_JSON")"
EMAIL_BBOX="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["email_bbox"])' "$FIELD_JSON")"
PASS_BBOX="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["password_bbox"])' "$FIELD_JSON")"
EMAIL_DELTA="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["email_delta"])' "$FIELD_JSON")"
PASS_DELTA="$(python3 -c 'import json,sys;print(json.loads(sys.argv[1])["password_delta"])' "$FIELD_JSON")"
echo "WORLDMAP_BASELINE_EMAIL_FIELD_DISCOVERY=tab:$EMAIL_TAB;bbox:$EMAIL_BBOX;echo_variant_delta:$EMAIL_DELTA;class:UNMASKED_RENDERING"
echo "WORLDMAP_BASELINE_PASSWORD_FIELD_DISCOVERY=tab:$PASS_TAB;bbox:$PASS_BBOX;echo_variant_delta:$PASS_DELTA;class:MASKED_RENDERING"

probe_discovered_field() {
'''

class TransformRefused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(START)!=1: raise TransformRefused(f'START_COUNT:{text.count(START)}')
    if text.count(END)!=1: raise TransformRefused(f'END_COUNT:{text.count(END)}')
    start=text.index(START); end=text.index(END,start)
    output=text[:start]+REPLACEMENT+text[end+len(END):]
    forbidden=('TAB_CONTROLLED_CYCLE_THEN_MASK_VARIANT_V3','WORLDMAP_PRELOGIN_V3_EDITABLE_METRIC=','WORLDMAP_PRELOGIN_V3_VARIANT_METRIC=')
    survivors=[x for x in forbidden if x in output]
    if survivors: raise TransformRefused('V3_SURVIVORS:'+','.join(survivors))
    required=(
      'TAB_CONTROLLED_EDITABILITY_PLUS_ROI_ECHO_V4','WORLDMAP_PRELOGIN_V4_EDITABLE_METRIC=',
      'WORLDMAP_PRELOGIN_V4_ECHO_METRIC=','WORLDMAP_V4_VARIANT_ROI_CHANGED=',
      'v4_unique_email_password_discriminator_failed','class:UNMASKED_RENDERING','class:MASKED_RENDERING',
      'probe_discovered_field() {','WORLDMAP_BASELINE_EMAIL_FIELD_EDITABLE=PASS',
      'WORLDMAP_BASELINE_PASSWORD_FIELD_EDITABLE=PASS','WORLDMAP_BASELINE_PRESECRET_READY=true')
    missing=[x for x in required if x not in output]
    if missing: raise TransformRefused('REQUIRED_MISSING:'+','.join(missing))
    if output.count('UI_WIN="$WIN"')!=1: raise TransformRefused('MANIFEST_WINDOW_IDENTITY_NOT_UNIQUE')
    if '"$XWD" -root' in output or 'xwd -root' in output: raise TransformRefused('ROOT_CAPTURE_FORBIDDEN')
    if 'WORLDMAP_BASELINE_LOGIN_SUBMITTED=true' in output: raise TransformRefused('LOGIN_PATH_SURVIVED')
    return output


def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('source',type=Path); p.add_argument('output',type=Path); a=p.parse_args()
    try: out=transform(a.source.read_text(encoding='utf-8'))
    except TransformRefused as exc:
        print(f'WORLDMAP_UI_FIELD_V4_REPAIR_REFUSED={exc}'); return 44
    a.output.write_text(out,encoding='utf-8'); a.output.chmod(0o700)
    print('WORLDMAP_UI_FIELD_V4_REPAIR=PASS'); return 0

if __name__=='__main__':
    raise SystemExit(main())
