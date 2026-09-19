#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

START = "probe_discovered_field() {\n"
END = "echo 'WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_EDITABLE_FIELDS'\n"

REPLACEMENT = r'''probe_discovered_field() {
  local name="$1" x="$2" y="$3" bbox="$4" dummy="$5"
  local bx0 by0 bx1 by1 x0 y0 x1 y1
  IFS=, read -r bx0 by0 bx1 by1 <<<"$bbox"
  [[ "$bx0" =~ ^[0-9]+$ && "$by0" =~ ^[0-9]+$ && "$bx1" =~ ^[0-9]+$ && "$by1" =~ ^[0-9]+$ ]] || fail "${name}_final_roi_bbox_invalid"
  x0=$((bx0>60 ? bx0-60 : 0)); y0=$((by0>25 ? by0-25 : 0))
  x1=$((bx1+90<ACTUAL_WIDTH ? bx1+90 : ACTUAL_WIDTH)); y1=$((by1+25<ACTUAL_HEIGHT ? by1+25 : ACTUAL_HEIGHT))

  local idle0="$ROOT/$name-final-idle0.xwd" idle1="$ROOT/$name-final-idle1.xwd" idle2="$ROOT/$name-final-idle2.xwd"
  local typed="$ROOT/$name-final-typed.xwd" cleared="$ROOT/$name-final-cleared.xwd" idle3="$ROOT/$name-final-idle3.xwd"
  xdo mousemove --window "$UI_WIN" "$x" "$y" click 1
  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace
  sleep .18; capture_xwd "$idle0"; sleep .18; capture_xwd "$idle1"; sleep .18; capture_xwd "$idle2"
  xdo type --window "$UI_WIN" --delay 10 -- "$dummy"; sleep .22; capture_xwd "$typed"
  xdo key --window "$UI_WIN" --clearmodifiers ctrl+a BackSpace; sleep .22; capture_xwd "$cleared"; sleep .18; capture_xwd "$idle3"

  set +e
  out="$(python3 - "$COMPARE" "$idle0" "$idle1" "$idle2" "$typed" "$cleared" "$idle3" "$x0" "$y0" "$x1" "$y1" <<'PY'
import importlib.util,sys
from pathlib import Path
compare,*rest=sys.argv[1:]
i0,i1,i2,typed,cleared,i3=map(Path,rest[:6]); roi=tuple(map(int,rest[6:10]))
spec=importlib.util.spec_from_file_location('wm_v5_compare',compare)
if spec is None or spec.loader is None: raise SystemExit('compare_import_failed')
m=importlib.util.module_from_spec(spec); sys.modules[spec.name]=m; spec.loader.exec_module(m)
noise=m.changed_mask(i0,i1,roi)|m.changed_mask(i1,i2,roi)|m.changed_mask(cleared,i3,roi)
typed_m=m.changed_mask(i2,typed,roi)-noise
cleared_m=m.changed_mask(typed,cleared,roi)-noise
residual=m.changed_mask(i2,cleared,roi)-noise
signal=typed_m&cleared_m
den=min(len(typed_m),len(cleared_m)); overlap=len(signal)/den if den else 0.0
fields,_,_=m.load(i0); bw,bh,area=m.bbox_metrics(signal,fields['width'])
print('WORLDMAP_V5_FINAL_ROI_NOISE_PIXELS='+str(len(noise)))
print('WORLDMAP_V5_FINAL_ROI_TYPED_CHANGED='+str(len(typed_m)))
print('WORLDMAP_V5_FINAL_ROI_CLEARED_CHANGED='+str(len(cleared_m)))
print('WORLDMAP_V5_FINAL_ROI_SIGNAL_CHANGED='+str(len(signal)))
print('WORLDMAP_V5_FINAL_ROI_RESIDUAL_CHANGED='+str(len(residual)))
print(f'WORLDMAP_V5_FINAL_ROI_OVERLAP_RATIO={overlap:.6f}')
print('WORLDMAP_V5_FINAL_ROI_SIGNAL_BBOX='+m.mask_bbox(signal,fields['width']))
print(f'WORLDMAP_V5_FINAL_ROI_SIGNAL_EXTENT={bw}x{bh};area={area}')
max_residual=max(80,int(len(signal)*0.55))
passed=len(signal)>=25 and overlap>=0.55 and len(residual)<=max_residual and bw>0 and bh>0 and area<=60000
print('WORLDMAP_V5_FINAL_ROI_EDITABLE_PROBE=' + ('PASS' if passed else 'FAIL'))
raise SystemExit(0 if passed else 3)
PY
)"
  rc=$?
  set -e
  rm -f "$idle0" "$idle1" "$idle2" "$typed" "$cleared" "$idle3"
  printf '%s\n' "$out"
  [[ "$rc" -eq 0 ]] || fail "${name}_editable_probe_failed"
}

probe_discovered_field email "$EMAIL_X" "$EMAIL_Y" "$EMAIL_BBOX" 'wm-probe@example.invalid'
echo 'WORLDMAP_BASELINE_EMAIL_FIELD_EDITABLE=PASS'
probe_discovered_field password "$PASS_X" "$PASS_Y" "$PASS_BBOX" 'wm-probe-7'
echo 'WORLDMAP_BASELINE_PASSWORD_FIELD_EDITABLE=PASS'
echo 'WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_EDITABLE_FIELDS'
'''

class TransformRefused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(START) != 1:
        raise TransformRefused(f"START_COUNT:{text.count(START)}")
    start=text.index(START)
    end=text.find(END,start)
    if end < 0:
        raise TransformRefused("END_MISSING")
    end += len(END)
    output=text[:start]+REPLACEMENT+text[end:]
    required=(
      'WORLDMAP_V5_FINAL_ROI_EDITABLE_PROBE=',
      'probe_discovered_field email "$EMAIL_X" "$EMAIL_Y" "$EMAIL_BBOX"',
      'probe_discovered_field password "$PASS_X" "$PASS_Y" "$PASS_BBOX"',
      'WORLDMAP_BASELINE_EMAIL_FIELD_EDITABLE=PASS',
      'WORLDMAP_BASELINE_PASSWORD_FIELD_EDITABLE=PASS',
      'WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_EDITABLE_FIELDS',
      'WORLDMAP_BASELINE_PRESECRET_READY=true',
    )
    missing=[x for x in required if x not in output]
    if missing: raise TransformRefused('REQUIRED_MISSING:'+','.join(missing))
    if output.count('UI_WIN="$WIN"') != 1: raise TransformRefused('MANIFEST_WINDOW_IDENTITY_NOT_UNIQUE')
    if '"$XWD" -root' in output or 'xwd -root' in output: raise TransformRefused('ROOT_CAPTURE_FORBIDDEN')
    if 'WORLDMAP_BASELINE_LOGIN_SUBMITTED=true' in output: raise TransformRefused('LOGIN_PATH_SURVIVED')
    return output


def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('source',type=Path); p.add_argument('output',type=Path); a=p.parse_args()
    try: out=transform(a.source.read_text(encoding='utf-8'))
    except TransformRefused as exc:
        print(f'WORLDMAP_UI_FIELD_V5_REPAIR_REFUSED={exc}'); return 44
    a.output.write_text(out,encoding='utf-8'); a.output.chmod(0o700)
    print('WORLDMAP_UI_FIELD_V5_REPAIR=PASS'); return 0

if __name__=='__main__':
    raise SystemExit(main())
