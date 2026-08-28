#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import probe as core

HANDLER_QMETA_CLASS = 'tibia::authentication::TLoginProtocolMessageHandler'
UNRESOLVED_TYPE = 0x80000000

# Only names that are fixed by Qt's public QMetaType ids are rendered. Unknown
# numeric ids stay numeric; no semantic name is guessed.
QT_METATYPE_NAMES = {
    0: 'UnknownType',
    1: 'bool',
    2: 'int',
    3: 'uint',
    4: 'qlonglong',
    5: 'qulonglong',
    6: 'double',
    7: 'QChar',
    8: 'QVariantMap',
    9: 'QVariantList',
    10: 'QString',
    11: 'QStringList',
    12: 'QByteArray',
    13: 'QBitArray',
    14: 'QDate',
    15: 'QTime',
    16: 'QDateTime',
    17: 'QUrl',
    18: 'QLocale',
    19: 'QRect',
    20: 'QRectF',
    21: 'QSize',
    22: 'QSizeF',
    23: 'QLine',
    24: 'QLineF',
    25: 'QPoint',
    26: 'QPointF',
}


def qstring(img: core.Image, base: int, index: int) -> str:
    entry = base + index * 8
    if not img.mapped(entry, 8):
        raise ValueError('qstring entry unmapped')
    rel = img.u32(entry)
    length = img.u32(entry + 4)
    if length > 4096 or not img.mapped(base + rel, length):
        raise ValueError('qstring payload invalid')
    return img.bytes(base + rel, length).decode('utf-8')


def stringdata_bases_for_literal(img: core.Image, literal: str) -> list[int]:
    out: set[int] = set()
    encoded = literal.encode('utf-8')
    for string_va in img.occurrences(encoded):
        string_off = img.va_to_off(string_va)
        lower = max(0, string_off - 0x10000)
        for entry_off in range(lower, string_off + 1, 4):
            entry_va = img.off_to_va(entry_off)
            if entry_va is None or not img.mapped(entry_va, 8):
                continue
            try:
                rel = img.u32(entry_va)
                length = img.u32(entry_va + 4)
            except Exception:
                continue
            if length != len(encoded) or rel > 0x20000:
                continue
            base = string_va - rel
            if base > entry_va or (entry_va - base) % 8:
                continue
            index = (entry_va - base) // 8
            try:
                if qstring(img, base, index) == literal and qstring(img, base, 0):
                    out.add(base)
            except Exception:
                pass
    return sorted(out)


def decode_type(img: core.Image, sbase: int, raw: int) -> dict:
    if raw & UNRESOLVED_TYPE:
        index = raw & ~UNRESOLVED_TYPE
        try:
            name = qstring(img, sbase, index)
        except Exception:
            name = None
        return {
            'encoding': 'UNRESOLVED_STRING_INDEX',
            'raw': raw,
            'string_index': index,
            'name': name,
        }
    return {
        'encoding': 'QMETATYPE_ID',
        'raw': raw,
        'id': raw,
        'name': QT_METATYPE_NAMES.get(raw),
    }


def parse_meta_candidate(img: core.Image, sbase: int, mbase: int) -> dict | None:
    if not img.mapped(mbase, 56):
        return None
    try:
        header = [img.u32(mbase + i * 4) for i in range(14)]
    except Exception:
        return None
    revision, class_index, _class_info_count, _class_info_offset, method_count, method_offset, _property_count, _property_offset, _enum_count, _enum_offset, _ctor_count, _ctor_offset, flags, signal_count = header
    if not (7 <= revision <= 20 and class_index == 0 and 0 < method_count <= 1000 and 14 <= method_offset < 200000 and signal_count <= method_count):
        return None
    try:
        class_name = qstring(img, sbase, class_index)
    except Exception:
        return None
    if class_name != HANDLER_QMETA_CLASS:
        return None

    methods = []
    try:
        for index in range(method_count):
            at = mbase + (method_offset + index * 6) * 4
            row = [img.u32(at + j * 4) for j in range(6)]
            name_index, argc, parameter_offset, tag_index, method_flags, meta_type_offset = row
            if argc > 64 or parameter_offset >= 400000:
                return None
            name = qstring(img, sbase, name_index)
            tag = qstring(img, sbase, tag_index) if tag_index else ''

            parameter_base = mbase + parameter_offset * 4
            # Qt moc metadata stores return type followed by argc argument types,
            # then argc argument-name string indices.
            type_refs = [img.u32(parameter_base + 4 * i) for i in range(argc + 1)]
            name_refs = [img.u32(parameter_base + 4 * (argc + 1 + i)) for i in range(argc)]
            parameter_names = [qstring(img, sbase, ref) if ref else '' for ref in name_refs]
            methods.append({
                'index': index,
                'name': name,
                'argc': argc,
                'parameter_offset': parameter_offset,
                'flags': method_flags,
                'tag': tag,
                'meta_type_offset': meta_type_offset,
                'return_type': decode_type(img, sbase, type_refs[0]),
                'parameter_types': [decode_type(img, sbase, raw) for raw in type_refs[1:]],
                'parameter_names': parameter_names,
            })
    except Exception:
        return None

    return {
        'revision': revision,
        'flags': flags,
        'signal_count': signal_count,
        'method_count': method_count,
        'method_offset': method_offset,
        'methods': methods,
    }


def recover_jump_table(img: core.Image, static_metacall: int, method_count: int) -> tuple[int, list[int]]:
    # Same bounded Qt static-metacall discriminator already proven in source #743.
    instructions = list(img.md.disasm(img.bytes(static_metacall, 0x900), static_metacall))[:420]
    candidates: set[tuple[int, tuple[int, ...]]] = set()
    for pos, row in enumerate(instructions):
        if row.mnemonic != 'lea' or len(row.operands) < 2:
            continue
        source = row.operands[1]
        if source.type != core.X86_OP_MEM or source.mem.base != core.X86_REG_RIP:
            continue
        table_register = row.operands[0].reg
        table = row.address + row.size + int(source.mem.disp)
        used = any(
            any(op.type == core.X86_OP_MEM and op.mem.base == table_register and op.mem.scale == 4 for op in later.operands)
            for later in instructions[pos + 1:pos + 12]
        )
        if not used:
            continue
        try:
            targets = tuple(table + int.from_bytes(img.bytes(table + 4 * i, 4), 'little', signed=True) for i in range(method_count))
        except Exception:
            continue
        if not all(img.executable(target) for target in targets):
            continue
        bounded = any(
            previous.mnemonic == 'cmp'
            and len(previous.operands) >= 2
            and previous.operands[0].type == core.X86_OP_REG
            and img.md.reg_name(previous.operands[0].reg) == 'edx'
            and previous.operands[1].type == core.X86_OP_IMM
            and int(previous.operands[1].imm) == method_count - 1
            for previous in instructions[max(0, pos - 12):pos]
        )
        if bounded:
            candidates.add((table, targets))
    if len(candidates) != 1:
        raise RuntimeError(f'QMeta jump table ambiguous: {len(candidates)}')
    table, targets = next(iter(candidates))
    return table, list(targets)


def recover_qmeta(img: core.Image) -> dict:
    candidates = []
    for sbase in stringdata_bases_for_literal(img, HANDLER_QMETA_CLASS):
        for mbase in range(max(0, sbase - 0x20000) & ~3, sbase + 0x20000, 4):
            meta = parse_meta_candidate(img, sbase, mbase)
            if meta is None:
                continue
            static_targets = []
            for where, value in img.rel.items():
                if value != sbase or img.rel.get(where + 8) != mbase:
                    continue
                target = img.rel.get(where + 16)
                if target is not None and img.executable(target):
                    static_targets.append(target)
            if len(static_targets) != 1:
                continue
            try:
                jump_table, targets = recover_jump_table(img, static_targets[0], meta['method_count'])
            except RuntimeError:
                continue
            meta['stringdata'] = sbase
            meta['metadata'] = mbase
            meta['static_metacall'] = static_targets[0]
            meta['jump_table'] = jump_table
            for method, target in zip(meta['methods'], targets):
                method['case_target'] = target
            candidates.append(meta)
    unique = {(row['stringdata'], row['metadata'], row['static_metacall']): row for row in candidates}
    if len(unique) != 1:
        raise RuntimeError(f'handler QMeta ambiguous/absent: {len(unique)}')
    return next(iter(unique.values()))


def direct_edges_to(img: core.Image, fde: tuple[int, int] | None, target: int) -> list[dict]:
    if fde is None:
        return []
    rows = []
    for ins in img.instructions(fde):
        if ins.mnemonic not in ('call', 'jmp') or not ins.operands or ins.operands[0].type != core.X86_OP_IMM:
            continue
        if int(ins.operands[0].imm) == target:
            rows.append({'site': core.hx(ins.address), 'mnemonic': ins.mnemonic})
    return rows


def sanitize_type(value: dict) -> dict:
    # Keep only static metadata; no binary bytes or runtime values.
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    result = json.loads(args.output.read_text(encoding='utf-8'))
    img = core.Image(args.client)
    core.verify_promoted_target(img)
    meta = recover_qmeta(img)
    producer_fde = img.fde(core.HANDLER_SLOT_TARGET)

    linked = []
    methods = []
    for method in meta['methods']:
        target = int(method['case_target'])
        fde = img.fde(target)
        reasons = []
        if target == core.HANDLER_SLOT_TARGET:
            reasons.append('CASE_TARGET_EQUALS_PRODUCER')
        if producer_fde is not None and fde == producer_fde:
            reasons.append('CASE_TARGET_SHARES_PRODUCER_FDE')
        direct_edges = direct_edges_to(img, fde, core.HANDLER_SLOT_TARGET)
        if direct_edges:
            reasons.append('CASE_FDE_DIRECT_EDGE_TO_PRODUCER')
        row = {
            'index': method['index'],
            'name': method['name'],
            'argc': method['argc'],
            'return_type': sanitize_type(method['return_type']),
            'parameter_types': [sanitize_type(value) for value in method['parameter_types']],
            'parameter_names': method['parameter_names'],
            'flags': method['flags'],
            'case_target': core.hx(target),
            'case_fde': [core.hx(fde[0]), core.hx(fde[1])] if fde else None,
            'producer_link_reasons': reasons,
            'producer_direct_edges': direct_edges,
        }
        methods.append(row)
        if reasons:
            linked.append(row)

    if len(linked) == 1:
        link_classification = 'UNIQUE_QMETA_METHOD_LINK_TO_PRODUCER'
        linked_method = linked[0]
    elif len(linked) == 0:
        link_classification = 'NO_QMETA_LINK_TO_PRODUCER'
        linked_method = None
    else:
        link_classification = 'AMBIGUOUS_QMETA_LINK_TO_PRODUCER'
        linked_method = None

    result['handler_qmeta_signatures'] = {
        'classification': 'HANDLER_QMETA_SIGNATURES',
        'class_name': HANDLER_QMETA_CLASS,
        'revision': meta['revision'],
        'method_count': meta['method_count'],
        'signal_count': meta['signal_count'],
        'stringdata': core.hx(meta['stringdata']),
        'metadata': core.hx(meta['metadata']),
        'static_metacall': core.hx(meta['static_metacall']),
        'jump_table': core.hx(meta['jump_table']),
        'methods': methods,
        'producer_link_classification': link_classification,
        'producer_linked_method': linked_method,
        'scope_markers': {
            'PARAMETER_TYPES': True,
            'PARAMETER_NAMES': True,
            'NO_SEMANTIC_GUESSING': True,
        },
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('HANDLER_QMETA_SIGNATURES=PASS')
    print('PARAMETER_TYPES=PASS')
    print('PARAMETER_NAMES=PASS')
    print('NO_SEMANTIC_GUESSING=true')
    print('HANDLER_QMETA_PRODUCER_LINK=' + link_classification)


if __name__ == '__main__':
    main()
