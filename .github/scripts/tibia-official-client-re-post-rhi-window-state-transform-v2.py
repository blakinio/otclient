#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

BASE = Path(__file__).with_name('tibia-official-client-re-post-rhi-window-state-transform.py')


def patched_namespace() -> dict[str, object]:
    text = BASE.read_text(encoding='utf-8')
    replacements = (
        (
            "    process_anchor = '    descendant_pids | sort -nu >\"$pids\"\\n    while read -r pid; do'",
            "    process_anchor = '  descendant_pids | sort -nu >\"$pids\"\\n  while read -r pid; do'",
            'THREAD_ANCHOR_INDENT',
        ),
        (
            "    allx_anchor = '    done <\"$pids\"\\n    : >\"$out\"'",
            "    allx_anchor = '  done <\"$pids\"\\n  : >\"$out\"'",
            'ALL_X11_ANCHOR_INDENT',
        ),
    )
    for old, new, label in replacements:
        count = text.count(old)
        if count != 1:
            raise SystemExit(f'POST_RHI_V2_REFUSED={label}_COUNT:{count}')
        text = text.replace(old, new, 1)
    namespace: dict[str, object] = {
        '__name__': 'post_rhi_transform_base',
        '__file__': str(BASE),
    }
    exec(compile(text, str(BASE), 'exec'), namespace)
    return namespace


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit('usage: transform-v2.py SOURCE OUTPUT')
    ns = patched_namespace()
    transform = ns.get('transform')
    source_blob = ns.get('SOURCE_BLOB')
    if not callable(transform) or not isinstance(source_blob, str):
        raise SystemExit('POST_RHI_V2_REFUSED=BASE_API')
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    script = transform(source.read_bytes())
    if not isinstance(script, str):
        raise SystemExit('POST_RHI_V2_REFUSED=TRANSFORM_RESULT')
    output.write_text(script, encoding='utf-8')
    print(f'POST_RHI_SOURCE_BLOB=PASS:{source_blob}')
    print('POST_RHI_TRANSFORM_V2=PASS')
    print('POST_RHI_CANONICAL_STATE_ACCESS=NONE')
    print('POST_RHI_RUNTIME_ACCESS=EPHEMERAL_ISOLATED')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
