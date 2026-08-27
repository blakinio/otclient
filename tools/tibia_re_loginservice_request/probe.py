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
    if not parts:
        return None
    mnemonic = parts[0]
    if not mnemonic or not mnemonic[0].isalpha():
        return None
    return {
        'address': int(match.group(1), 16),
        'at': hx(int(match.group(1), 16)),
        'mnemonic': mnemonic,
        'operand': parts[1] if len(parts) > 1 else '',
        'raw': line.strip(),
    }


def stream_xrefs(client, target_to_terms, fdes):
    command = ['objdump', '-d', '-Mintel', '--no-show-raw-insn', str(client)]
    proc = subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.stdout is None:
        raise SystemExit('OBJDUMP_STDOUT_MISSING')

    refs = {term: [] for term in (*KEYS, *ENDPOINT_TERMS)}
    grouped = {}
    previous = collections.deque(maxlen=8)
    comment_target = re.compile(r'#\s*([0-9a-fA-F]+)\b')

    for line in proc.stdout:
        parsed = parse_instruction_line(line)
        if not parsed:
            continue
        match = comment_target.search(parsed['operand'])
        matched_terms = set()
        if match:
            target = int(match.group(1), 16)
            matched_terms.update(target_to_terms.get(target, ()))
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


def bounded_snapshot(client, start, end, limit=320):
    proc = subprocess.run(
        [
            'objdump', '-d', '-Mintel', '--no-show-raw-insn',
            f'--start-address={start}', f'--stop-address={end}', str(client),
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    rows = []
    for line in proc.stdout.splitlines():
        parsed = parse_instruction_line(line)
        if parsed:
            rows.append({'at': parsed['at'], 'mnemonic': parsed['mnemonic'], 'operand': parsed['operand']})
    if len(rows) <= limit:
        return rows
    half = limit // 2
    return rows[:half] + [
        {'at': 'TRUNCATED', 'mnemonic': '...', 'operand': f'{len(rows)-2*half} instructions'}
    ] + rows[-half:]


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
                'offset': int(sec['sh_offset']),
                'size': int(sec['sh_size']),
                'addr': int(sec['sh_addr']),
            }
            for sec in elf.iter_sections()
            if int(sec['sh_size']) > 0
        ]

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

    refs, grouped = stream_xrefs(client, target_to_terms, fdes)

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

    snapshots = []
    for candidate in candidate_rows[:12]:
        match = re.fullmatch(r'0x([0-9a-f]+)\.\.0x([0-9a-f]+)', candidate['fde'])
        if not match:
            continue
        start, end = int(match.group(1), 16), int(match.group(2), 16)
        snapshots.append({
            'fde': candidate['fde'],
            'distinct_request_keys': candidate['distinct_request_keys'],
            'endpoint_terms': candidate['endpoint_terms'],
            'snapshot': bounded_snapshot(client, start, end),
        })

    result = {
        'schema': 'otclient.track-a.current-loginservice-request.discovery.v2',
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
        'candidate_snapshots': snapshots,
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
