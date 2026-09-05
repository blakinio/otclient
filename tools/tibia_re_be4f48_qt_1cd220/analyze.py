"""Strict two-file qualification of one selected receiver-storage callee."""
import argparse
import json
from pathlib import Path
from package import (select_package, verify_member, qualify_dependency_fence,
                     qualify_core_identity, unique_definition, SYMBOL)
from static_flow import Image, verify_fence, EXPECTED_VERSION, EXPECTED_SIZE, EXPECTED_SHA256
from callee import qualify_call, exact_owner
from storage import storage_region, receiver_storage


def analyze(selected, client, core):
    verify_fence(client.read_bytes(), selected['version'])
    primary = Image(client)
    try:
        if primary.elf.elfclass != 64 or primary.elf['e_machine'] != 'EM_X86_64':
            raise ValueError('PRIMARY_ELF_IDENTITY_CHANGED')
        needed = [t.needed for t in primary.elf.get_section_by_name('.dynamic').iter_tags()
                  if t.entry.d_tag == 'DT_NEEDED' and t.needed == 'libQt6Core.so.6']
        imports = [s for s in primary.elf.get_section_by_name('.dynsym').iter_symbols() if s.name == SYMBOL]
        if len(needed) != 1 or len(imports) != 1 or imports[0]['st_shndx'] != 'SHN_UNDEF':
            raise ValueError('PRIMARY_IMPORT_IDENTITY_CHANGED')
    finally:
        primary.close()
    if not selected['qtcore']:
        raise ValueError('NO_UNIQUE_EXACT_QTCORE')
    qualify_dependency_fence(selected['qtcore'])
    verify_member(core.read_bytes(), selected['qtcore'])
    img = Image(core)
    try:
        syms = [s for s in img.elf.get_section_by_name('.dynsym').iter_symbols() if s.name == SYMBOL]
        address, size = unique_definition([(s['st_shndx'], int(s['st_value']), int(s['st_size'])) for s in syms])
        sonames = [t.soname for t in img.elf.get_section_by_name('.dynamic').iter_tags() if t.entry.d_tag == 'DT_SONAME']
        qualify_core_identity(img.elf.elfclass, img.elf['e_machine'], sonames, syms[0]['st_info']['type'])
        if (address, size, img.containing_fde(address)) != (0x1d3570, 506, (0x1d3570, 0x1d376a)):
            raise ValueError('PROMOTED_CONNECTIMPL_IDENTITY_CHANGED')
        qualify_call(img.read(0x1d36e8, 5), 0x1d36e8, 0x1cd220)
        lo, hi = storage_region(img.fdes, 0x1cd220)
        if not any(slo <= lo and hi <= shi and flags & 4 for slo, shi, off, flags in img.sections):
            raise ValueError('STORAGE_FDE_NOT_EXECUTABLE')
        rows = [{'name': s.name, 'address': int(s['st_value']), 'size': int(s['st_size']),
                 'type': s['st_info']['type'], 'section': s['st_shndx']}
                for s in img.elf.get_section_by_name('.dynsym').iter_symbols()
                if int(s['st_value']) == lo]
        owner = exact_owner(rows, lo, (lo, hi))
        flow = receiver_storage(img.read(lo, hi - lo), lo)
        writes = [s for s in flow['receiver_stores'] if s['destination_provenance'] == 'SYMBOLIC_VALUE_RELATIVE']
        if flow['resource_limit_hit']:
            terminal, boundary = 'ANALYSIS_INCOMPLETE', 'RECEIVER_STORAGE_RESOURCE_FRONTIER'
        elif writes:
            terminal, boundary = 'POSITIVE_EXACT_CONDITIONAL_RECEIVER_STORAGE', 'STORED_RECEIVER_DESTINATION_OWNER_AND_DELIVERY_NOT_PROVEN'
        else:
            terminal, boundary = 'SOURCE_BLOCKER', 'NO_SYMBOLIC_DESTINATION_RECEIVER_STORE_PROVEN_IN_BOUNDED_MUST_MODEL'
        return {
            'schema': 'otclient.track-a.be4f48-qt-1cd220.v1',
            'exact_client': {'version': EXPECTED_VERSION, 'size': EXPECTED_SIZE, 'sha256': EXPECTED_SHA256},
            'packaged_qtcore': selected['qtcore'],
            'packaged_identity_is_runtime_loaded_identity': False,
            'FACT': {'caller_site': '0x1d36e8', 'callee_entry': hex(lo),
                     'receiver_input': 'entry:rcx, conditional promoted #912 carrier',
                     'containing_fde': [hex(lo), hex(hi)], 'unique_exact_dynsym_owner': owner,
                     'conditional_storage_model': flow},
            'INFERENCE': [],
            'UNKNOWN': ['runtime_loaded_qtcore', 'actual_sendlogin_receiver_identity',
                        'destination_dynamic_owner_type', 'successful_registration_and_delivery',
                        'complete_sendlogin_causal_binding', 'final_queue_writer', 'final_tcp_writer',
                        'final_writer_contract', 'field6_value', 'pre_success_send_sequence'],
            'terminal_result': terminal, 'FIRST_MISSING_BOUNDARY': boundary,
            'absence_of_real_receiver_stores_proven': False,
            'full_receiver_registration_delivery_contract_proven': False,
            'runtime_access': 'none', 'official_client_executed': False,
            'login_performed': False, 'credentials_used': False, 'process_memory_access': False,
            'packet_capture': False, 'ocr_vision_used': False, 'official_service_e2e_count': 0,
            'track_b_pr_284_modified': False, 'track_b_current_wire_delta': 'NOT_PROVEN',
            'field6_value': 'UNKNOWN', 'final_writer_contract': 'UNKNOWN',
            'pre_success_send_sequence': 'UNKNOWN'}
    finally:
        img.close()


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--manifest', type=Path)
    p.add_argument('--selection', type=Path, required=True)
    p.add_argument('--client', type=Path)
    p.add_argument('--qtcore', type=Path)
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    if a.manifest:
        a.selection.write_text(json.dumps(select_package(json.loads(a.manifest.read_text())), sort_keys=True) + '\n')
    else:
        result = analyze(json.loads(a.selection.read_text()), a.client, a.qtcore)
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
