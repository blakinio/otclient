#!/usr/bin/env python3
from __future__ import annotations

import probe as core

FOCUSED_TIMEOUT_RECOVERY = True
RAW_REL32_TARGET_PREFILTER = True
RAW_RIP_VTABLE_PREFILTER = True


def fast_direct_edges_into_target(img: core.Image):
    raw_candidates: set[tuple[int, int, str]] = set()
    for section in img.sections:
        if not (section.flags & 4):
            continue
        blob = img.raw[section.offset:section.offset + section.size]
        for opcode, mnemonic in ((0xE8, 'call'), (0xE9, 'jmp')):
            needle = bytes((opcode,))
            pos = 0
            while True:
                pos = blob.find(needle, pos)
                if pos < 0:
                    break
                if pos + 5 <= len(blob):
                    site = section.va + pos
                    disp = int.from_bytes(blob[pos + 1:pos + 5], 'little', signed=True)
                    target = site + 5 + disp
                    if core.TARGET_FDE[0] <= target < core.TARGET_FDE[1]:
                        raw_candidates.add((site, target, mnemonic))
                pos += 1
    rows = []
    for site, target, mnemonic in sorted(raw_candidates):
        fde = img.fde(site)
        if fde is None or fde[1] - fde[0] > 0x10000:
            continue
        ins = next((row for row in img.instructions(fde) if row.address == site), None)
        if ins is None or ins.mnemonic != mnemonic or not ins.operands or ins.operands[0].type != core.X86_OP_IMM:
            continue
        if int(ins.operands[0].imm) != target:
            continue
        rows.append({'site': site, 'target': target, 'source_fde': fde})
    return rows


def fast_rip_refs_to(img: core.Image, target: int):
    sites: set[int] = set()
    for section in img.sections:
        if not (section.flags & 4):
            continue
        blob = img.raw[section.offset:section.offset + section.size]
        # REX + LEA/MOV reg,[RIP+disp32]
        for pos in range(0, max(0, len(blob) - 7)):
            if 0x40 <= blob[pos] <= 0x4F and blob[pos + 1] in (0x8D, 0x8B) and (blob[pos + 2] & 0xC7) == 0x05:
                disp = int.from_bytes(blob[pos + 3:pos + 7], 'little', signed=True)
                site = section.va + pos
                if site + 7 + disp == target:
                    sites.add(site)
            if blob[pos] in (0x8D, 0x8B) and (blob[pos + 1] & 0xC7) == 0x05:
                disp = int.from_bytes(blob[pos + 2:pos + 6], 'little', signed=True)
                site = section.va + pos
                if site + 6 + disp == target:
                    sites.add(site)
    rows = []
    for site in sorted(sites):
        fde = img.fde(site)
        if fde is None or fde[1] - fde[0] > 0x10000:
            continue
        ins = next((row for row in img.instructions(fde) if row.address == site), None)
        if ins is None:
            continue
        matched = False
        for op in ins.operands:
            if op.type == core.X86_OP_MEM and op.mem.base == core.X86_REG_RIP:
                if ins.address + ins.size + int(op.mem.disp) == target:
                    matched = True
                    break
        if matched:
            rows.append((fde, site))
    return rows


core.direct_edges_into_target = fast_direct_edges_into_target
core.rip_refs_to = fast_rip_refs_to

if __name__ == '__main__':
    core.main()
