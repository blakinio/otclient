"""Exact selected loader binding; no target implementation or runtime lookup."""
import argparse
import json
from pathlib import Path
from elftools.elf.elffile import ELFFile
from binding import qualify_call, plt_slot, relocation_binding
from fence import verify_fence, EXPECTED_VERSION, EXPECTED_SIZE, EXPECTED_SHA256
from package import select_package, qualify_dependency_fence, verify_member


def analyze(selected, client, core):
    raw = client.read_bytes()
    verify_fence(raw, selected['version'])
    qualify_dependency_fence(selected['qtcore'])
    verify_member(core.read_bytes(), selected['qtcore'])
    facts = {}
    with client.open('rb') as handle:
        elf = ELFFile(handle)
        if elf.elfclass != 64 or not elf.little_endian or elf['e_machine'] != 'EM_X86_64':
            raise ValueError('PRIMARY_ELF_IDENTITY_CHANGED')
        sections = [{'name': s.name, 'lo': int(s['sh_addr']),
                     'hi': int(s['sh_addr'])+int(s['sh_size']), 'flags': int(s['sh_flags']),
                     'off': int(s['sh_offset']), 'entsize': int(s['sh_entsize']),
                     'type': s['sh_type']} for s in elf.iter_sections() if s['sh_addr'] and s['sh_size']]
        def read_exec(va, size):
            maps = [s for s in sections if s['lo'] <= va < va+size <= s['hi']]
            if len(maps) != 1 or maps[0]['flags'] & 6 != 6 or maps[0]['type'] == 'SHT_NOBITS':
                raise ValueError('SELECTED_EXECUTABLE_BYTES_NOT_UNIQUELY_MAPPED')
            offset = maps[0]['off']+va-maps[0]['lo']
            if not 0 <= offset < offset+size <= len(raw):
                raise ValueError('SELECTED_EXECUTABLE_BYTES_OUTSIDE_FILE')
            return raw[offset:offset+size]
        try:
            facts['promoted_call'] = qualify_call(read_exec(0xdd8e10,5),0xdd8e10,0x4d7dc0)
            # Never read a native target if the selected address lacks PLT metadata.
            owners = [s for s in sections if s['lo'] <= 0x4d7dc0 < 0x4d7dc0+16 <= s['hi']]
            if len(owners) != 1 or owners[0]['name'] not in ('.plt','.plt.sec'):
                raise ValueError('SELECTED_TARGET_NOT_UNIQUE_PLT_SECTION')
            facts['selected_stub'] = plt_slot(read_exec(0x4d7dc0,16),0x4d7dc0,sections)
            facts['selected_import'] = relocation_binding(elf,int(facts['selected_stub']['got_slot'],16))
            terminal, missing = 'POSITIVE_EXACT_SELECTED_IMPORT_BINDING', 'SELECTED_IMPORT_IMPLEMENTATION_USE_NOT_PROVEN'
        except ValueError as error:
            missing = str(error)
            terminal = 'ANALYSIS_INCOMPLETE' if missing == 'RELOCATION_ROW_LIMIT' else 'SOURCE_BLOCKER'
    return {'schema':'otclient.track-a.be4f48-queue-import.v1',
            'exact_client':{'version':EXPECTED_VERSION,'size':EXPECTED_SIZE,'sha256':EXPECTED_SHA256},
            'packaged_qtcore':selected['qtcore'],'packaged_identity_is_runtime_loaded_identity':False,
            'FACT':facts,'INFERENCE':[],
            'UNKNOWN':['runtime_import_resolution','selected_import_implementation_use','logical_argument_vector',
                       'activation_and_signal_index','actual_sendlogin_receiver_identity','complete_sendlogin_causal_binding',
                       'registered_downstream_receiver','successful_registration_and_delivery',
                       'final_queue_writer','final_tcp_writer','final_writer_contract','field6_value','pre_success_send_sequence'],
            'terminal_result':terminal,'FIRST_MISSING_BOUNDARY':missing,
            'actual_absence_of_import_binding_proven':False,
            'runtime_access':'none','official_client_executed':False,'login_performed':False,'credentials_used':False,
            'process_memory_access':False,'packet_capture':False,'ocr_vision_used':False,'official_service_e2e_count':0,
            'track_b_pr_284_modified':False,'track_b_current_wire_delta':'NOT_PROVEN',
            'field6_value':'UNKNOWN','final_writer_contract':'UNKNOWN','pre_success_send_sequence':'UNKNOWN'}


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--manifest',type=Path)
    p.add_argument('--selection',type=Path,required=True)
    p.add_argument('--client',type=Path)
    p.add_argument('--qtcore',type=Path)
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    if a.manifest:
        a.selection.write_text(json.dumps(select_package(json.loads(a.manifest.read_text())),sort_keys=True)+'\n')
    else:
        result=analyze(json.loads(a.selection.read_text()),a.client,a.qtcore)
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
