"""Exact selected QMeta callable activation arguments, no downstream traversal."""
import argparse
import json
from pathlib import Path
from elftools.elf.relocation import RelocationSection
from activation import project, qualify_tail, classify, import_binding
from package import select_package, qualify_dependency_fence, verify_member
from static_flow import Image, verify_fence, EXPECTED_VERSION, EXPECTED_SIZE, EXPECTED_SHA256


def analyze(selected, client, core):
    verify_fence(client.read_bytes(), selected['version'])
    qualify_dependency_fence(selected['qtcore'])
    verify_member(core.read_bytes(), selected['qtcore'])
    img = Image(client)
    try:
        if img.elf.elfclass != 64 or img.elf['e_machine'] != 'EM_X86_64':
            raise ValueError('PRIMARY_ELF_IDENTITY_CHANGED')
        qualify_tail(img.read(0xde823a, 5), 0xde823a, 0xdd8df0)
        fde = img.containing_fde(0xdd8df0)
        flow, symbol, owner = None, None, None
        if fde is None:
            terminal, missing = 'SOURCE_BLOCKER', 'NO_UNIQUE_SELECTED_CALLABLE_FDE'
        elif fde[1] - fde[0] > 4096:
            terminal, missing = 'ANALYSIS_INCOMPLETE', 'SELECTED_CALLABLE_FDE_SIZE_FRONTIER'
        else:
            lo, hi = fde
            if not any(a <= lo < hi <= b and flags & 4 for a, b, off, flags in img.sections):
                raise ValueError('SELECTED_FDE_NOT_EXECUTABLE')
            owners = [s for s in img.elf.get_section_by_name('.dynsym').iter_symbols()
                      if int(s['st_value']) == 0xdd8df0 and s['st_shndx'] != 'SHN_UNDEF' and s['st_info']['type'] == 'STT_FUNC']
            if len(owners) == 1 and fde == (0xdd8df0, 0xdd8df0 + int(owners[0]['st_size'])):
                owner = owners[0].name or None
            flow = project(img.read(lo, hi - lo), lo, 0xdd8df0)
            target = flow['boundary'].get('target')
            if target is not None:
                target = int(target, 16)
                sections = [s for s in img.elf.iter_sections() if s.name in ('.plt', '.plt.sec', '.plt.got')
                            and int(s['sh_addr']) <= target < int(s['sh_addr']) + int(s['sh_size'])]
                if len(sections) == 1:
                    sec = sections[0]
                    extent = min(16, int(sec['sh_addr']) + int(sec['sh_size']) - target)
                    rows = []
                    for relsec in img.elf.iter_sections():
                        if not isinstance(relsec, RelocationSection):
                            continue
                        symtab = img.elf.get_section(relsec['sh_link']) if relsec['sh_link'] else None
                        for rel in relsec.iter_relocations():
                            idx = int(rel['r_info_sym'])
                            s = symtab.get_symbol(idx) if symtab is not None and idx else None
                            rows.append({'offset': int(rel['r_offset']), 'type': int(rel['r_info_type']),
                                         'name': s.name if s is not None else '',
                                         'undefined': s is not None and s['st_shndx'] == 'SHN_UNDEF'})
                    symbol = import_binding(img.read(target, extent), target, rows)
            terminal, missing = classify(flow, symbol)
        return {
            'schema': 'otclient.track-a.be4f48-queue-dd8df0.v1',
            'exact_client': {'version': EXPECTED_VERSION, 'size': EXPECTED_SIZE, 'sha256': EXPECTED_SHA256},
            'packaged_qtcore': selected['qtcore'], 'packaged_identity_is_runtime_loaded_identity': False,
            'FACT': {'promoted_tail': {'site': '0xde823a', 'target': '0xdd8df0', 'kind': 'DIRECT_JMP'},
                     'selected_fde': [hex(x) for x in fde] if fde else None,
                     'selected_exact_dynsym_owner': owner, 'first_transfer_model': flow,
                     'first_target_unique_plt_import': symbol},
            'INFERENCE': [],
            'UNKNOWN': ['actual_sendlogin_receiver_identity', 'complete_sendlogin_causal_binding',
                        'qmeta_enum_and_method_index_equivalence', 'registered_downstream_receiver',
                        'successful_registration_and_delivery', 'final_queue_writer', 'final_tcp_writer',
                        'final_writer_contract', 'field6_value', 'pre_success_send_sequence'],
            'terminal_result': terminal, 'FIRST_MISSING_BOUNDARY': missing,
            'actual_absence_of_activation_proven': False,
            'runtime_access': 'none', 'official_client_executed': False,
            'login_performed': False, 'credentials_used': False, 'process_memory_access': False,
            'packet_capture': False, 'ocr_vision_used': False, 'official_service_e2e_count': 0,
            'track_b_pr_284_modified': False, 'track_b_current_wire_delta': 'NOT_PROVEN',
            'field6_value': 'UNKNOWN', 'final_writer_contract': 'UNKNOWN', 'pre_success_send_sequence': 'UNKNOWN'}
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
