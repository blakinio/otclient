"""Exact packaged definition metadata; no body or runtime lookup."""
import argparse
import json
from pathlib import Path
from elftools.elf.elffile import ELFFile
from definition import lookup
from fence import verify_fence, EXPECTED_VERSION, EXPECTED_SIZE, EXPECTED_SHA256
from package import select_package, qualify_dependency_fence, verify_member


def section_metadata(elf):
    count=elf.num_sections()
    if elf['e_shentsize']!=64 or not 0<=elf['e_shoff']<=elf['e_shoff']+count*64<=elf.stream_len:
        raise ValueError('ELF_SECTION_HEADER_TABLE_BOUNDS')
    sections=[]
    for i in range(count):
        # iter_sections/get_section instantiate GNUHashSection and eagerly read
        # all bloom words and buckets. Only the fixed-width header is allowed.
        s=elf._get_section_header(i)
        if s is None: raise ValueError('ELF_SECTION_HEADER_MISSING')
        sections.append(dict(index=i, type=s['sh_type'], addr=int(s['sh_addr']),
                             off=int(s['sh_offset']), size=int(s['sh_size']), flags=int(s['sh_flags']),
                             entsize=int(s['sh_entsize']), link=int(s['sh_link'])))
    return sections


def analyze(selected, client, core):
    raw = client.read_bytes()
    verify_fence(raw, selected['version'])
    qualify_dependency_fence(selected['qtcore'])
    verify_member(core.read_bytes(), selected['qtcore'])
    facts = {}
    with core.open('rb') as handle:
        elf = ELFFile(handle)
        if elf.elfclass != 64 or not elf.little_endian or elf['e_machine'] != 'EM_X86_64':
            raise ValueError('QTCORE_ELF_IDENTITY_CHANGED')
        sections = section_metadata(elf)
        try:
            facts['packaged_definition'] = lookup(core.read_bytes(), sections)
            terminal, missing = 'POSITIVE_EXACT_PACKAGED_DYNAMIC_DEFINITION', 'PACKAGED_DEFINITION_BODY_USE_NOT_PROVEN'
        except ValueError as error:
            missing = str(error)
            terminal = 'ANALYSIS_INCOMPLETE' if missing in ('DYNAMIC_ENTRY_LIMIT','HASH_CHAIN_LIMIT','HASH_CANDIDATE_LIMIT') else 'SOURCE_BLOCKER'
    return {'schema':'otclient.track-a.be4f48-qt-definition.v1',
            'exact_client':{'version':EXPECTED_VERSION,'size':EXPECTED_SIZE,'sha256':EXPECTED_SHA256},
            'packaged_qtcore':selected['qtcore'],'packaged_identity_is_runtime_loaded_identity':False,
            'FACT':facts,'INFERENCE':[],
            'UNKNOWN':['symbol_version_resolution','runtime_import_resolution','selected_import_implementation_use','logical_argument_vector',
                       'activation_and_signal_index','actual_sendlogin_receiver_identity','complete_sendlogin_causal_binding',
                       'registered_downstream_receiver','successful_registration_and_delivery',
                       'final_queue_writer','final_tcp_writer','final_writer_contract','field6_value','pre_success_send_sequence'],
            'terminal_result':terminal,'FIRST_MISSING_BOUNDARY':missing,
            'actual_absence_of_definition_proven':False,
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
