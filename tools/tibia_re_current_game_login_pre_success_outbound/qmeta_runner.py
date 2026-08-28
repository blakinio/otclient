#!/usr/bin/env python3
from __future__ import annotations

import probe as core


def exact_qmeta_class(img: core.Image, class_name: str, required: tuple[str, ...]) -> dict:
    candidates = []
    for sbase in core.stringdata_bases_for_literal(img, class_name):
        for mbase in range(max(0, sbase - 0x20000) & ~3, sbase + 0x20000, 4):
            meta = core.parse_meta(img, sbase, mbase)
            if not meta or meta['class_name'] != class_name:
                continue
            names = {row['name'] for row in meta['rows']}
            if not set(required).issubset(names):
                continue
            static = []
            for where, value in img.rel.items():
                if value != sbase or img.rel.get(where + 8) != mbase:
                    continue
                target = img.rel.get(where + 16)
                if target is not None and img.executable(target):
                    static.append(target)
            if len(static) != 1:
                continue
            table, targets = core.recover_qmeta_jump_table(img, static[0], meta['method_count'])
            methods = {}
            for row in meta['rows']:
                if row['name'] not in required:
                    continue
                target = targets[row['index']]
                methods[row['name']] = {
                    'index': row['index'],
                    'target': target,
                    'fde': img.fde(target),
                }
            candidates.append({
                'metadata': mbase,
                'stringdata': sbase,
                'static_metacall': static[0],
                'jump_table': table,
                'methods': methods,
            })
    unique = {(row['metadata'], row['stringdata']): row for row in candidates}
    if len(unique) != 1:
        raise RuntimeError(f'QMETA_CLASS_AMBIGUOUS:{class_name}:{len(unique)}')
    return next(iter(unique.values()))


core.exact_qmeta_class = exact_qmeta_class

if __name__ == '__main__':
    core.main()
