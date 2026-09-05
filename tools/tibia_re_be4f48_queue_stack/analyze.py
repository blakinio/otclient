"""Exact construction facts only; no activation/import/target body analysis."""
import argparse
import json
from pathlib import Path
from construction import construct, qualify_tail
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
        if fde != (0xdd8df0, 0xdd8e1a):
            raise ValueError('PROMOTED_42BYTE_FDE_CHANGED')
        lo, hi = fde
        if not any(a <= lo < hi <= b and flags & 4 for a, b, off, flags in img.sections):
            raise ValueError('SELECTED_FDE_NOT_EXECUTABLE')
        flow = construct(img.read(lo, hi - lo), lo)
        if flow['resource_limit_hit']:
            terminal, missing = 'ANALYSIS_INCOMPLETE', 'STACK_CONSTRUCTION_INSTRUCTION_FRONTIER'
        elif flow['construction_escape_proven']:
            terminal, missing = 'POSITIVE_EXACT_STACK_CONSTRUCTION_ESCAPE', 'ESCAPED_STACK_REGION_CALLEE_USE_NOT_PROVEN'
        else:
            terminal, missing = 'SOURCE_BLOCKER', 'STACK_CONSTRUCTION_OR_ESCAPE_NOT_PROVEN_AT_' + flow['boundary']['site']
        return {
            'schema': 'otclient.track-a.be4f48-queue-stack.v1',
            'exact_client': {'version': EXPECTED_VERSION, 'size': EXPECTED_SIZE, 'sha256': EXPECTED_SHA256},
            'packaged_qtcore': selected['qtcore'], 'packaged_identity_is_runtime_loaded_identity': False,
            'FACT': {'promoted_tail': {'site': '0xde823a', 'target': '0xdd8df0', 'kind': 'DIRECT_JMP'},
                     'selected_fde': [hex(lo), hex(hi)], 'construction_model': flow},
            'INFERENCE': [],
            'UNKNOWN': ['actual_sendlogin_receiver_identity', 'complete_sendlogin_causal_binding',
                        'logical_stack_object_or_parameter_names', 'qmeta_index_or_activation_identity',
                        'first_target_identity', 'escaped_region_callee_use', 'registered_downstream_receiver',
                        'successful_registration_and_delivery', 'final_queue_writer', 'final_tcp_writer',
                        'final_writer_contract', 'field6_value', 'pre_success_send_sequence'],
            'terminal_result': terminal, 'FIRST_MISSING_BOUNDARY': missing,
            'actual_absence_of_stack_construction_proven': False,
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
