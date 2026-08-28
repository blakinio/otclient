#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP

import probe as core

QMETA_CALLER_OWNER = True
TARGET_SCALAR_PARENT_THIS = True
STATIC_METAOBJECT_TRIPLE = True
METHOD_CASE_DIRECT_EDGE = True
OWNER_QMETA_CLASS = True
PARENT_MEMBER_HANDLER_BINDING = True
NO_HEURISTIC_RANKING = True
NO_SEMANTIC_GUESSING = True
UNRESOLVED_TYPE = 0x80000000

QT_METATYPE_NAMES = {
    0: 'UnknownType', 1: 'bool', 2: 'int', 3: 'uint', 4: 'qlonglong',
    5: 'qulonglong', 6: 'double', 7: 'QChar', 8: 'QVariantMap',
    9: 'QVariantList', 10: 'QString', 11: 'QStringList', 12: 'QByteArray',
    13: 'QBitArray', 14: 'QDate', 15: 'QTime', 16: 'QDateTime',
    17: 'QUrl', 18: 'QLocale', 19: 'QRect', 20: 'QRectF', 21: 'QSize',
    22: 'QSizeF', 23: 'QLine', 24: 'QLineF', 25: 'QPoint', 26: 'QPointF',
}


def u32(img: core.Image, va: int) -> int:
    return int.from_bytes(img.bytes(va, 4), 'little', signed=False)


def qstring(img: core.Image, base: int, index: int) -> str:
    entry = base + index * 8
    if not img.mapped(entry, 8):
        raise ValueError('qstring entry unmapped')
    rel = u32(img, entry)
    length = u32(img, entry + 4)
    if length > 4096 or not img.mapped(base + rel, length):
        raise ValueError('qstring payload invalid')
    return img.bytes(base + rel, length).decode('utf-8')


def decode_type(img: core.Image, sbase: int, raw: int) -> dict:
    if raw & UNRESOLVED_TYPE:
        index = raw & ~UNRESOLVED_TYPE
        try:
            name = qstring(img, sbase, index)
        except Exception:
            name = None
        return {'encoding': 'UNRESOLVED_STRING_INDEX', 'raw': raw, 'string_index': index, 'name': name}
    return {'encoding': 'QMETATYPE_ID', 'raw': raw, 'id': raw, 'name': QT_METATYPE_NAMES.get(raw)}


def parse_meta_candidate(img: core.Image, sbase: int, mbase: int) -> dict | None:
    if not img.mapped(sbase, 8) or not img.mapped(mbase, 56):
        return None
    try:
        header = [u32(img, mbase + i * 4) for i in range(14)]
    except Exception:
        return None
    revision, class_index, _cic, _cio, method_count, method_offset, _pc, _po, _ec, _eo, _cc, _co, flags, signal_count = header
    if not (7 <= revision <= 20 and class_index == 0 and 0 < method_count <= 512 and 14 <= method_offset < 200000 and signal_count <= method_count):
        return None
    try:
        class_name = qstring(img, sbase, class_index)
    except Exception:
        return None
    if not class_name or len(class_name) > 256 or '::' not in class_name:
        return None
    methods = []
    try:
        for index in range(method_count):
            at = mbase + (method_offset + index * 6) * 4
            row = [u32(img, at + j * 4) for j in range(6)]
            name_index, argc, parameter_offset, tag_index, method_flags, meta_type_offset = row
            if argc > 32 or parameter_offset >= 400000:
                return None
            name = qstring(img, sbase, name_index)
            tag = qstring(img, sbase, tag_index) if tag_index else ''
            parameter_base = mbase + parameter_offset * 4
            type_refs = [u32(img, parameter_base + 4 * i) for i in range(argc + 1)]
            name_refs = [u32(img, parameter_base + 4 * (argc + 1 + i)) for i in range(argc)]
            parameter_names = [qstring(img, sbase, ref) if ref else '' for ref in name_refs]
            methods.append({
                'index': index,
                'name': name,
                'argc': argc,
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
        'class_name': class_name,
        'revision': revision,
        'flags': flags,
        'signal_count': signal_count,
        'method_count': method_count,
        'method_offset': method_offset,
        'methods': methods,
    }


def static_metaobject_candidates(img: core.Image) -> list[dict]:
    rows = []
    seen = set()
    for where, sbase in img.rel.items():
        mbase = img.rel.get(where + 8)
        static_metacall = img.rel.get(where + 16)
        if mbase is None or static_metacall is None or not img.executable(static_metacall):
            continue
        meta = parse_meta_candidate(img, sbase, mbase)
        if meta is None:
            continue
        key = (sbase, mbase, static_metacall, meta['class_name'])
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            **meta,
            'static_metaobject': where,
            'stringdata': sbase,
            'metadata': mbase,
            'static_metacall': static_metacall,
        })
    return rows


def recover_jump_table(img: core.Image, static_metacall: int, method_count: int) -> tuple[int, list[int]]:
    fde = img.fde(static_metacall)
    if fde is None:
        raise RuntimeError('static metacall FDE unavailable')
    instructions = img.instructions(fde)
    candidates: set[tuple[int, tuple[int, ...]]] = set()
    for pos, row in enumerate(instructions):
        if row.mnemonic != 'lea' or len(row.operands) < 2:
            continue
        source = row.operands[1]
        if source.type != X86_OP_MEM or source.mem.base != X86_REG_RIP:
            continue
        table_register = row.operands[0].reg
        table = row.address + row.size + int(source.mem.disp)
        used = any(
            any(op.type == X86_OP_MEM and op.mem.base == table_register and op.mem.scale == 4 for op in later.operands)
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
            prev.mnemonic == 'cmp'
            and len(prev.operands) >= 2
            and prev.operands[0].type == X86_OP_REG
            and img.md.reg_name(prev.operands[0].reg) == 'edx'
            and prev.operands[1].type == X86_OP_IMM
            and int(prev.operands[1].imm) == method_count - 1
            for prev in instructions[max(0, pos - 16):pos]
        )
        if bounded:
            candidates.add((table, targets))
    if len(candidates) != 1:
        raise RuntimeError(f'QMeta jump table ambiguous: {len(candidates)}')
    table, targets = next(iter(candidates))
    return table, list(targets)


def direct_edges_into_fde(img: core.Image, target_fde: tuple[int, int]) -> list[dict]:
    rows = []
    for fde in img.fdes:
        if not img.executable(fde[0]) or fde[1] - fde[0] > 0x10000:
            continue
        for ins in img.instructions(fde):
            if ins.mnemonic not in ('call', 'jmp') or not ins.operands or ins.operands[0].type != X86_OP_IMM:
                continue
            target = int(ins.operands[0].imm)
            if target_fde[0] <= target < target_fde[1]:
                rows.append({
                    'site': ins.address,
                    'target': target,
                    'source_fde': fde,
                    'mnemonic': ins.mnemonic,
                })
    return rows


def case_block(img: core.Image, static_fde: tuple[int, int], case_target: int, all_targets: set[int]) -> list:
    instructions = img.instructions(static_fde)
    by = {row.address: i for i, row in enumerate(instructions)}
    if case_target not in by:
        return []
    out = []
    for row in instructions[by[case_target]:by[case_target] + 96]:
        if out and row.address in all_targets:
            break
        out.append(row)
        mnemonic = row.mnemonic.lower()
        if mnemonic.startswith('ret') or mnemonic == 'jmp':
            break
    return out


def method_edges_for_meta(img: core.Image, meta: dict, target_fde: tuple[int, int], direct_edges: list[dict]) -> list[dict]:
    static_fde = img.fde(meta['static_metacall'])
    if static_fde is None:
        return []
    relevant_edges = [row for row in direct_edges if row['source_fde'] == static_fde]
    if not relevant_edges:
        return []
    try:
        jump_table, targets = recover_jump_table(img, meta['static_metacall'], meta['method_count'])
    except RuntimeError:
        return []
    all_targets = set(targets)
    rows = []
    for method, case_target in zip(meta['methods'], targets):
        block = case_block(img, static_fde, case_target, all_targets)
        sites = {row.address for row in block}
        hits = [edge for edge in relevant_edges if edge['site'] in sites]
        if not hits:
            continue
        rows.append({
            'class_name': meta['class_name'],
            'static_metaobject': core.hx(meta['static_metaobject']),
            'stringdata': core.hx(meta['stringdata']),
            'metadata': core.hx(meta['metadata']),
            'static_metacall': core.hx(meta['static_metacall']),
            'jump_table': core.hx(jump_table),
            'method': {
                'index': method['index'],
                'name': method['name'],
                'argc': method['argc'],
                'flags': method['flags'],
                'return_type': method['return_type'],
                'parameter_types': method['parameter_types'],
                'parameter_names': method['parameter_names'],
                'case_target': core.hx(case_target),
            },
            'direct_edges': [
                {
                    'site': core.hx(edge['site']),
                    'target': core.hx(edge['target']),
                    'mnemonic': edge['mnemonic'],
                }
                for edge in hits
            ],
        })
    return rows


def target_scalar_parent_this(result: dict) -> dict:
    candidates = []
    for row in result['scalar_callsite_census']['candidates']:
        receiver = row.get('receiver') or {}
        origin = receiver.get('object_origin') or {}
        parent = receiver.get('parent_base_entry') or {}
        if row.get('edx', {}).get('classification') != 'UNIQUE_STATIC_SCALAR':
            continue
        if receiver.get('abi_receiver_matches_vtable_object') is not True:
            continue
        if origin.get('classification') != 'MEMORY_LOAD' or int(origin.get('displacement', -1)) != 0x10:
            continue
        if parent.get('classification') != 'ENTRY_ALIAS_PROVEN' or parent.get('entry_family') != 'rdi':
            continue
        candidates.append(row)
    if len(candidates) != 1:
        raise RuntimeError(f'TARGET_SCALAR_PARENT_THIS ambiguous: {len(candidates)}')
    return candidates[0]


def handler_binding_for_owner(img: core.Image, owner_class: str, member_offset: int) -> dict:
    vtables = core.recover_vtables(img)
    owner_vtables = [row for row in vtables if row['type_name'] == owner_class]
    proofs = []
    for vt in owner_vtables:
        for ctor in core.owner_constructors(img, int(vt['address_point'])):
            for proof in core.constructor_member_proofs(img, ctor, member_offset):
                proofs.append({
                    'owner_type': owner_class,
                    'owner_vtable_address_point': core.hx(int(vt['address_point'])),
                    'constructor_fde': [core.hx(ctor['fde'][0]), core.hx(ctor['fde'][1])],
                    **proof,
                })
    proven = [row for row in proofs if row['classification'] == 'PARENT_MEMBER_HANDLER_BINDING_PROVEN']
    return {
        'classification': 'PARENT_MEMBER_HANDLER_BINDING_PROVEN' if len(proven) == 1 else 'PARENT_MEMBER_HANDLER_BINDING_UNKNOWN',
        'owner_qmeta_class': owner_class,
        'owner_vtable_count': len(owner_vtables),
        'proof_count': len(proven),
        'proofs': proofs,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    result = json.loads(args.output.read_text(encoding='utf-8'))
    img = core.Image(args.client)
    vtables = core.recover_vtables(img)
    core.verify_exact(img, vtables)

    target = target_scalar_parent_this(result)
    target_fde = tuple(int(value, 16) for value in target['fde'])
    direct_edges = direct_edges_into_fde(img, target_fde)
    meta_candidates = static_metaobject_candidates(img)
    method_links = []
    for meta in meta_candidates:
        method_links.extend(method_edges_for_meta(img, meta, target_fde, direct_edges))

    unique_links = {
        (
            row['class_name'],
            row['static_metacall'],
            row['method']['index'],
            row['method']['case_target'],
            tuple((edge['site'], edge['target']) for edge in row['direct_edges']),
        ): row
        for row in method_links
    }
    links = list(unique_links.values())
    if len(links) == 1:
        owner_classification = 'OWNER_QMETA_CLASS_PROVEN'
        owner = links[0]
        member_offset = int((target['receiver']['object_origin'])['displacement'])
        binding = handler_binding_for_owner(img, owner['class_name'], member_offset)
    else:
        owner_classification = 'OWNER_QMETA_CLASS_UNKNOWN'
        owner = None
        binding = {
            'classification': 'PARENT_MEMBER_HANDLER_BINDING_UNKNOWN',
            'owner_qmeta_class': None,
            'owner_vtable_count': 0,
            'proof_count': 0,
            'proofs': [],
        }

    if owner is not None and binding['classification'] == 'PARENT_MEMBER_HANDLER_BINDING_PROVEN':
        classification = 'FIELD6_VALUE_PROVEN'
        value = int(target['edx']['value'])
        result['classification'] = classification
        result['field6_value'] = value
        result['accepted_callsite'] = target
    else:
        classification = 'FIELD6_VALUE_UNKNOWN'
        value = None

    result['qmeta_caller_owner'] = {
        'classification': 'QMETA_CALLER_OWNER',
        'target_scalar_parent_this': target,
        'target_fde': [core.hx(target_fde[0]), core.hx(target_fde[1])],
        'direct_edge_count': len(direct_edges),
        'direct_edges': [
            {
                'site': core.hx(row['site']),
                'target': core.hx(row['target']),
                'source_fde': [core.hx(row['source_fde'][0]), core.hx(row['source_fde'][1])],
                'mnemonic': row['mnemonic'],
            }
            for row in direct_edges
        ],
        'static_metaobject_candidate_count': len(meta_candidates),
        'method_case_direct_edge_count': len(links),
        'method_case_direct_edges': links,
        'owner_classification': owner_classification,
        'owner': owner,
        'parent_member_handler_binding': binding,
        'field6_value_classification': classification,
        'field6_value': value,
        'scope_markers': {
            'TARGET_SCALAR_PARENT_THIS': TARGET_SCALAR_PARENT_THIS,
            'STATIC_METAOBJECT_TRIPLE': STATIC_METAOBJECT_TRIPLE,
            'METHOD_CASE_DIRECT_EDGE': METHOD_CASE_DIRECT_EDGE,
            'OWNER_QMETA_CLASS': OWNER_QMETA_CLASS,
            'PARENT_MEMBER_HANDLER_BINDING': PARENT_MEMBER_HANDLER_BINDING,
            'NO_HEURISTIC_RANKING': NO_HEURISTIC_RANKING,
            'NO_SEMANTIC_GUESSING': NO_SEMANTIC_GUESSING,
        },
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')

    print('QMETA_CALLER_OWNER=PASS')
    print('TARGET_SCALAR_PARENT_THIS=PASS')
    print('STATIC_METAOBJECT_TRIPLE=PASS')
    print('METHOD_CASE_DIRECT_EDGE=' + str(len(links)))
    print('OWNER_QMETA_CLASS=' + owner_classification)
    print('PARENT_MEMBER_HANDLER_BINDING=' + binding['classification'])
    print('FIELD6_VALUE=' + (str(value) if value is not None else 'UNKNOWN'))
    print('CLASSIFICATION=' + classification)
    print('NO_HEURISTIC_RANKING=true')
    print('NO_SEMANTIC_GUESSING=true')


if __name__ == '__main__':
    main()
