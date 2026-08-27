#!/usr/bin/env python3
import argparse
import collections
import json
import re
import subprocess
from pathlib import Path

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

# Exact 15.32.75d4a0 QString storage identities independently derived from the
# first hosted literal/init artifact. They are version-fenced and re-scanned
# only to follow references into the actual request builder; they are never
# promoted to another client build.
STORAGE_TARGETS = {
    'type': 0x31BA520,
    'email': 0x31BA700,
    'password': 0x31BA6E0,
    'stayloggedin': 0x31BA5E0,
    'devicecookie': 0x31BA5C0,
    'clienttype': 0x31BA5A0,
    'clientversion': 0x31BA580,
    'assetversion': 0x31BA560,
    'isreturner': 0x31BA160,
    'showrewardnews': 0x31BA140,
}

# Every QString storage referenced by the exact current request builder
# 0xe1e780..0xe1eb21. Names are deliberately not assigned until the bounded
# static initializer below proves the literal behind each storage.
BUILDER_STORAGE_ADDRESSES = (
    0x31BA740,
    0x31BA720,
    0x31BA700,
    0x31BA6E0,
    0x31BA6C0,
    0x31BA6A0,
    0x31BA680,
    0x31BA660,
    0x31BA640,
    0x31BA620,
    0x31BA600,
    0x31BA5E0,
    0x31BA5C0,
    0x31BA5A0,
    0x31BA580,
    0x31BA560,
)
INITIALIZER_FDE = (0x6130C0, 0x613B27)
QSTRING_FROM_UTF8_CTOR = 0x6A7200


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
    pattern = re.compile(r'\bFDE\b.*?pc=([0-9a-fA-F]+)\.\.([0-9a-fA-F]+)')
    fdes = []
    for line in proc.stdout.splitlines():
        match = pattern.search(line)
        if not match:
            continue
        start, end = int(match.group(1), 16), int(match.group(2), 16)
        if start < end:
            fdes.append((start, end))
    return sorted(set(fdes))


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
            return start, end
    return None


def file_offset_to_va(sections, offset):
    for section in sections:
        start = section['offset']
        end = start + section['size']
        if start <= offset < end:
            return section['addr'] + (offset - start)
    return None


def va_to_file_offset(sections, address):
    for section in sections:
        start = section['addr']
        end = start + section['size']
        if start <= address < end:
            return section['offset'] + (address - start)
    return None


def read_cstring_at_va(blob, sections, address, max_len=160):
    offset = va_to_file_offset(sections, address)
    if offset is None or offset >= len(blob):
        return None
    end = blob.find(b'\0', offset, min(len(blob), offset + max_len))
    if end < 0 or end == offset:
        return None
    raw = blob[offset:end]
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        return None
    if any(ord(ch) < 0x20 and ch not in '\t\r\n' for ch in text):
        return None
    return text


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


def parse_instruction_line(line):
    match = re.match(r'^\s*([0-9a-fA-F]+):\s+(.+?)\s*$', line)
    if not match:
        return None
    body = match.group(2)
    if body.endswith('>:'):
        return None
    parts = body.split(None, 1)
    if not parts or not parts[0] or not parts[0][0].isalpha():
        return None
    address = int(match.group(1), 16)
    return {
        'address': address,
        'at': hx(address),
        'mnemonic': parts[0],
        'operand': parts[1] if len(parts) > 1 else '',
    }


def objdump_rows(client, start=None, end=None):
    command = ['objdump', '-d', '-Mintel', '--no-show-raw-insn']
    if start is not None:
        command.append(f'--start-address={start}')
    if end is not None:
        command.append(f'--stop-address={end}')
    command.append(str(client))
    proc = subprocess.run(
        command,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [
        parsed for line in proc.stdout.splitlines()
        if (parsed := parse_instruction_line(line)) is not None
    ]


def comment_target(operand):
    match = re.search(r'#\s*([0-9a-fA-F]+)\b', operand)
    return int(match.group(1), 16) if match else None


def decode_builder_storage_literals(client, blob, sections):
    rows = objdump_rows(client, *INITIALIZER_FDE)
    storage_set = set(BUILDER_STORAGE_ADDRESSES)
    register_targets = {}
    decoded = []

    register_name = re.compile(r'^[a-z][a-z0-9]*$')
    for row in rows:
        mnemonic = row['mnemonic']
        operands = [part.strip() for part in row['operand'].split(',', 1)]
        if mnemonic == 'lea' and len(operands) == 2:
            dest = operands[0]
            target = comment_target(row['operand'])
            if register_name.fullmatch(dest) and target is not None:
                register_targets[dest] = target
        elif mnemonic == 'mov' and len(operands) == 2:
            dest, src = operands
            if register_name.fullmatch(dest) and register_name.fullmatch(src):
                if src in register_targets:
                    register_targets[dest] = register_targets[src]
                else:
                    register_targets.pop(dest, None)
        elif mnemonic == 'call':
            call_match = re.match(r'^([0-9a-fA-F]+)\b', row['operand'])
            call_target = int(call_match.group(1), 16) if call_match else None
            if call_target == QSTRING_FROM_UTF8_CTOR:
                storage = register_targets.get('rdi')
                literal_va = register_targets.get('rsi')
                if storage in storage_set and literal_va is not None:
                    decoded.append({
                        'storage': hx(storage),
                        'literal_va': hx(literal_va),
                        'literal': read_cstring_at_va(blob, sections, literal_va),
                        'constructor_site': row['at'],
                    })
            # SysV caller-clobbered registers must not leak across a call.
            for register in ('rax', 'rcx', 'rdx', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'r11'):
                register_targets.pop(register, None)

    by_storage = {}
    for item in decoded:
        by_storage.setdefault(item['storage'], []).append(item)
    return {
        'initializer_fde': f'{hx(INITIALIZER_FDE[0])}..{hx(INITIALIZER_FDE[1])}',
        'requested_storages': [hx(value) for value in BUILDER_STORAGE_ADDRESSES],
        'decoded': decoded,
        'unique_by_storage': {
            storage: rows[0] if len(rows) == 1 else rows
            for storage, rows in sorted(by_storage.items())
        },
        'missing_storages': [
            hx(value) for value in BUILDER_STORAGE_ADDRESSES
            if hx(value) not in by_storage
        ],
    }


def stream_xrefs(client, target_to_terms, term_names, fdes):
    proc = subprocess.Popen(
        ['objdump', '-d', '-Mintel', '--no-show-raw-insn', str(client)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.stdout is None:
        raise SystemExit('OBJDUMP_STDOUT_MISSING')

    refs = {term: [] for term in term_names}
    grouped = {}
    previous = collections.deque(maxlen=8)
    target_pattern = re.compile(r'#\s*([0-9a-fA-F]+)\b')

    for line in proc.stdout:
        parsed = parse_instruction_line(line)
        if not parsed:
            continue
        matched_terms = set()
        match = target_pattern.search(parsed['operand'])
        if match:
            matched_terms.update(target_to_terms.get(int(match.group(1), 16), ()))
        if matched_terms:
            fde = fde_for(fdes, parsed['address'])
            fde_key = f'{hx(fde[0])}..{hx(fde[1])}' if fde else 'UNKNOWN'
            context = [
                {'at': item['at'], 'mnemonic': item['mnemonic'], 'operand': item['operand']}
                for item in list(previous)
            ] + [{'at': parsed['at'], 'mnemonic': parsed['mnemonic'], 'operand': parsed['operand']}]
            for term in sorted(matched_terms):
                refs[term].append({'site': parsed['at'], 'fde': fde_key, 'context_before': context})
                grouped.setdefault(fde_key, set()).add(term)
        previous.append(parsed)

    stderr = proc.stderr.read() if proc.stderr else ''
    code = proc.wait()
    if code != 0:
        raise SystemExit(f'OBJDUMP_FAILED={code}:{stderr[-500:]}')
    return refs, grouped


def bounded_snapshot(client, start, end, limit=420):
    rows = objdump_rows(client, start, end)
    output = [
        {'at': row['at'], 'mnemonic': row['mnemonic'], 'operand': row['operand']}
        for row in rows
    ]
    if len(output) <= limit:
        return output
    half = limit // 2
    return output[:half] + [
        {'at': 'TRUNCATED', 'mnemonic': '...', 'operand': f'{len(output)-2*half} instructions'}
    ] + output[-half:]


def candidate_rows(grouped, allowed_terms):
    rows = []
    allowed = set(allowed_terms)
    for fde_key, terms in grouped.items():
        matched = sorted(set(terms) & allowed)
        rows.append({'fde': fde_key, 'terms': matched, 'term_count': len(matched)})
    rows.sort(key=lambda item: item['term_count'], reverse=True)
    return rows


def snapshot_candidates(client, candidates, key_name='terms'):
    snapshots = []
    for candidate in candidates[:12]:
        match = re.fullmatch(r'0x([0-9a-f]+)\.\.0x([0-9a-f]+)', candidate['fde'])
        if not match:
            continue
        start, end = int(match.group(1), 16), int(match.group(2), 16)
        snapshots.append({
            'fde': candidate['fde'],
            key_name: candidate.get(key_name, candidate.get('terms', [])),
            'snapshot': bounded_snapshot(client, start, end),
        })
    return snapshots


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
            {'offset': int(sec['sh_offset']), 'size': int(sec['sh_size']), 'addr': int(sec['sh_addr'])}
            for sec in elf.iter_sections() if int(sec['sh_size']) > 0
        ]

    fdes = parse_fdes(client)
    literals = {}
    literal_target_to_terms = {}
    literal_terms = (*KEYS, *ENDPOINT_TERMS)
    for term in literal_terms:
        occurrences = find_literal_occurrences(blob, sections, term)
        literals[term] = [
            {'encoding': item['encoding'], 'file_offset': item['file_offset'], 'va': hx(item['va'])}
            for item in occurrences
        ]
        for item in occurrences:
            literal_target_to_terms.setdefault(item['va'], set()).add(term)

    refs, grouped = stream_xrefs(client, literal_target_to_terms, literal_terms, fdes)
    literal_candidates = candidate_rows(grouped, KEYS)

    storage_target_to_terms = {}
    for term, target in STORAGE_TARGETS.items():
        storage_target_to_terms.setdefault(target, set()).add(term)
    storage_refs, storage_grouped = stream_xrefs(
        client, storage_target_to_terms, tuple(STORAGE_TARGETS), fdes)
    storage_candidates = candidate_rows(storage_grouped, tuple(STORAGE_TARGETS))
    initializer_literals = decode_builder_storage_literals(client, blob, sections)

    result = {
        'schema': 'otclient.track-a.current-loginservice-request.discovery.v4',
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
        'candidate_fdes': literal_candidates[:40],
        'candidate_snapshots': snapshot_candidates(client, literal_candidates),
        'storage_targets_exact_build': {key: hx(value) for key, value in STORAGE_TARGETS.items()},
        'storage_references': storage_refs,
        'storage_candidate_fdes': storage_candidates[:40],
        'storage_candidate_snapshots': snapshot_candidates(client, storage_candidates),
        'request_builder_storage_literals': initializer_literals,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding='utf-8')
    print('CURRENT_LOGINSERVICE_REQUEST_STATIC_PROBE=PASS')
    print('CURRENT_LOGINSERVICE_REQUEST_KEYS_PRESENT=' + str(sum(bool(literals[key]) for key in KEYS)))
    print('CURRENT_LOGINSERVICE_BUILDER_STORAGE_LITERALS=' + str(len(initializer_literals['decoded'])))
    print('CURRENT_LOGINSERVICE_BUILDER_STORAGE_MISSING=' + str(len(initializer_literals['missing_storages'])))
    if literal_candidates:
        print('CURRENT_LOGINSERVICE_LITERAL_TOP_FDE=' + literal_candidates[0]['fde'])
        print('CURRENT_LOGINSERVICE_LITERAL_TOP_KEY_COUNT=' + str(literal_candidates[0]['term_count']))
    if storage_candidates:
        print('CURRENT_LOGINSERVICE_STORAGE_TOP_FDE=' + storage_candidates[0]['fde'])
        print('CURRENT_LOGINSERVICE_STORAGE_TOP_KEY_COUNT=' + str(storage_candidates[0]['term_count']))


if __name__ == '__main__':
    main()
