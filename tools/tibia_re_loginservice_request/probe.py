#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP
from elftools.elf.elffile import ELFFile

KEYS = (
    'email',
    'password',
    'stayloggedin',
    'type',
    'clientversion',
    'clienttype',
    'assetversion',
    'devicecookie',
    'fromtimestamp',
    'isreturner',
    'showrewardnews',
    'viewedid',
)
ENDPOINT_TERMS = (
    'loginservice.php',
    'clientservices/loginservice.php',
)


def hx(value):
    return f'0x{value:x}' if value is not None else None


def parse_fdes(client):
    proc = subprocess.run(
        ['readelf', '--debug-dump=frames', str(client)],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    fdes = []
    pattern = re.compile(r'\bFDE\b.*?pc=([0-9a-fA-F]+)\.\.([0-9a-fA-F]+)')
    for line in proc.stdout.splitlines():
        match = pattern.search(line)
        if not match:
            continue
        start, end = (int(match.group(1), 16), int(match.group(2), 16))
        if start < end:
            fdes.append((start, end))
    fdes = sorted(set(fdes))
    return fdes


def fde_for(fdes, address):
    lo, hi = 0, len(fdes)
    while lo < hi:
        mid = (lo + hi) // 2
        if fdes[mid][0] <= address:
            lo = mid + 1
        else:
            hi = mid
    for index in range(max(0, lo - 3), min(len(fdes), lo + 1)):
        start, end = fdes[index]
        if start <= address < end:
            return (start, end)
    return None


def file_offset_to_va(sections, offset):
    for section in sections:
        start = section['offset']
        end = start + section['size']
        if start <= offset < end:
            return section['addr'] + (offset - start)
    return None


def find_literal_occurrences(blob, sections, literal):
    variants = {
        'ascii': literal.encode('utf-8') + b'\0',
        'utf16le': literal.encode('utf-16le') + b'\0\0',
    }
    found = []
    for encoding, needle in variants.items():
        start = 0
        while True:
            index = blob.find(needle, start)
            if index < 0:
                break
            va = file_offset_to_va(sections, index)
            if va is not None:
                found.append({'encoding': encoding, 'file_offset': hx(index), 'va': va})
            start = index + 1
    return found


def disasm_text(elf, blob):
    text = elf.get_section_by_name('.text')
    if text is None:
        raise SystemExit('TEXT_SECTION_MISSING')
    start = text['sh_offset']
    data = blob[start:start + text['sh_size']]
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    return list(md.disasm(data, text['sh_addr']))


def rip_targets(instruction):
    targets = []
    for operand in instruction.operands:
        if operand.type == X86_OP_MEM and operand.mem.base == X86_REG_RIP:
            targets.append(instruction.address + instruction.size + operand.mem.disp)
    return targets


def row(instruction):
    return {
        'at': hx(instruction.address),
        'mnemonic': instruction.mnemonic,
        'operand': instruction.op_str,
    }


def instruction_context(instructions, index, radius=10):
    start = max(0, index - radius)
    end = min(len(instructions), index + radius + 1)
    return [row(item) for item in instructions[start:end]]


def snapshot_fde(instructions, fde, limit=320):
    if not fde:
        return []
    start, end = fde
    rows = [row(item) for item in instructions if start <= item.address < end]
    if len(rows) <= limit:
        return rows
    head = rows[:limit // 2]
    tail = rows[-(limit // 2):]
    return head + [{'at': 'TRUNCATED', 'mnemonic': '...', 'operand': f'{len(rows)-len(head)-len(tail)} instructions'}] + tail


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    client = Path(args.client)
    output = Path(args.output)
    blob = client.read_bytes()

    with client.open('rb') as handle:
        elf = ELFFile(handle)
        sections = [
            {
                'name': sec.name,
                'offset': int(sec['sh_offset']),
                'size': int(sec['sh_size']),
                'addr': int(sec['sh_addr']),
            }
            for sec in elf.iter_sections()
            if int(sec['sh_size']) > 0
        ]
        instructions = disasm_text(elf, blob)

    fdes = parse_fdes(client)
    literals = {}
    target_to_terms = {}
    for term in (*KEYS, *ENDPOINT_TERMS):
        occurrences = find_literal_occurrences(blob, sections, term)
        literals[term] = [
            {'encoding': item['encoding'], 'file_offset': item['file_offset'], 'va': hx(item['va'])}
            for item in occurrences
        ]
        for item in occurrences:
            target_to_terms.setdefault(item['va'], set()).add(term)

    refs = {term: [] for term in (*KEYS, *ENDPOINT_TERMS)}
    grouped = {}
    for index, instruction in enumerate(instructions):
        matched_terms = set()
        for target in rip_targets(instruction):
            matched_terms.update(target_to_terms.get(target, ()))
        if not matched_terms:
            continue
        fde = fde_for(fdes, instruction.address)
        fde_key = f'{hx(fde[0])}..{hx(fde[1])}' if fde else 'UNKNOWN'
        for term in sorted(matched_terms):
            refs[term].append({
                'site': hx(instruction.address),
                'fde': fde_key,
                'context': instruction_context(instructions, index),
            })
            grouped.setdefault(fde_key, set()).add(term)

    candidate_rows = []
    for fde_key, terms in grouped.items():
        key_terms = sorted(set(terms) & set(KEYS))
        endpoint_terms = sorted(set(terms) & set(ENDPOINT_TERMS))
        candidate_rows.append({
            'fde': fde_key,
            'distinct_request_keys': key_terms,
            'request_key_count': len(key_terms),
            'endpoint_terms': endpoint_terms,
        })
    candidate_rows.sort(key=lambda item: (item['request_key_count'], len(item['endpoint_terms'])), reverse=True)

    top_snapshots = []
    for candidate in candidate_rows[:12]:
        if candidate['fde'] == 'UNKNOWN':
            continue
        match = re.fullmatch(r'0x([0-9a-f]+)\.\.0x([0-9a-f]+)', candidate['fde'])
        if not match:
            continue
        fde = (int(match.group(1), 16), int(match.group(2), 16))
        top_snapshots.append({
            'fde': candidate['fde'],
            'distinct_request_keys': candidate['distinct_request_keys'],
            'endpoint_terms': candidate['endpoint_terms'],
            'snapshot': snapshot_fde(instructions, fde),
        })

    result = {
        'schema': 'otclient.track-a.current-loginservice-request.discovery.v1',
        'exact_client': {
            'version': '15.32.75d4a0',
            'packed_sha256': '075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f',
            'unpacked_sha256': 'd1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a',
            'unpacked_size': 52105824,
        },
        'runtime_access': 'none',
        'login_performed': False,
        'secret_access': False,
        'raw_client_uploaded': False,
        'request_keys': list(KEYS),
        'literal_occurrences': literals,
        'references': refs,
        'candidate_fdes': candidate_rows[:40],
        'candidate_snapshots': top_snapshots,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding='utf-8')
    print('CURRENT_LOGINSERVICE_REQUEST_STATIC_PROBE=PASS')
    print('CURRENT_LOGINSERVICE_REQUEST_KEYS_PRESENT=' + str(sum(bool(literals[key]) for key in KEYS)))
    if candidate_rows:
        print('CURRENT_LOGINSERVICE_TOP_FDE=' + candidate_rows[0]['fde'])
        print('CURRENT_LOGINSERVICE_TOP_KEY_COUNT=' + str(candidate_rows[0]['request_key_count']))


if __name__ == '__main__':
    main()
