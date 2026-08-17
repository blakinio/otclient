#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

BASE = Path(__file__).with_name('tibia-official-client-re-xres-raw-pid-identity-patch.py')
TASK_ID = 'OTC-20260817-track-a-xres-raw-pid-identity'
INHERITED_TASK_ID = 'OTC-20260816-track-a-canonical-runtime-e2e'


def patched_namespace() -> dict[str, object]:
    text = BASE.read_text(encoding='utf-8')
    old = "    snapshot_anchor = 'PYALLX\\n  : >\"$out\"'"
    new = "    snapshot_anchor = 'PYALLX\\n    : >\"$out\"'"
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'XRES_RAW_PATCH_V2_REFUSED=SNAPSHOT_ANCHOR_LITERAL_COUNT:{count}')
    text = text.replace(old, new, 1)
    ns: dict[str, object] = {'__name__': 'xres_raw_patch_base', '__file__': str(BASE)}
    exec(compile(text, str(BASE), 'exec'), ns)
    return ns


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit('usage: xres-raw-pid-patch-v2.py INPUT OUTPUT')
    ns = patched_namespace()
    patch = ns.get('patch')
    if not callable(patch):
        raise SystemExit('XRES_RAW_PATCH_V2_REFUSED=BASE_API')
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    result = patch(src.read_text(encoding='utf-8'))
    if not isinstance(result, str):
        raise SystemExit('XRES_RAW_PATCH_V2_REFUSED=PATCH_RESULT')
    inherited = f"task='{INHERITED_TASK_ID}'"
    replacement = f"task='{TASK_ID}'"
    count = result.count(inherited)
    if count != 1:
        raise SystemExit(f'XRES_RAW_PATCH_V2_REFUSED=TASK_OWNER_COUNT:{count}')
    result = result.replace(inherited, replacement, 1)
    if INHERITED_TASK_ID in result:
        raise SystemExit('XRES_RAW_PATCH_V2_REFUSED=INHERITED_TASK_REMAINS')
    dst.write_text(result, encoding='utf-8')
    print(f'XRES_RAW_TASK_OWNER={TASK_ID}')
    print('XRES_RAW_PATCH_V2=PASS')
    print('XRES_OBSERVATION_ONLY=true')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
