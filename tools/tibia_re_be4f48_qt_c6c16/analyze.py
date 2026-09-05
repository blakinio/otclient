"""Exact two-file qualification followed by one continuation, no callee traversal."""
import argparse
import json
from pathlib import Path
from package import (select_package, verify_member, qualify_dependency_fence,
                     qualify_core_identity, unique_definition, SYMBOL)
from static_flow import Image, verify_fence, EXPECTED_VERSION, EXPECTED_SIZE, EXPECTED_SHA256
from continuation import qualify_branch, bounded_region, first_transfers, plt_binding, plt_extent


def analyze(selected,client,core):
    verify_fence(client.read_bytes(),selected['version'])
    primary=Image(client)
    try:
        assert primary.elf.elfclass==64 and primary.elf['e_machine']=='EM_X86_64'
        needed=[t.needed for t in primary.elf.get_section_by_name('.dynamic').iter_tags() if t.entry.d_tag=='DT_NEEDED' and t.needed=='libQt6Core.so.6']
        imports=[s for s in primary.elf.get_section_by_name('.dynsym').iter_symbols() if s.name==SYMBOL]
        if len(needed)!=1 or len(imports)!=1 or imports[0]['st_shndx']!='SHN_UNDEF':
            raise ValueError('PRIMARY_IMPORT_IDENTITY_CHANGED')
    finally: primary.close()
    if not selected['qtcore']: raise ValueError('NO_UNIQUE_EXACT_QTCORE')
    qualify_dependency_fence(selected['qtcore']); verify_member(core.read_bytes(),selected['qtcore'])
    img=Image(core)
    try:
        syms=[s for s in img.elf.get_section_by_name('.dynsym').iter_symbols() if s.name==SYMBOL]
        address,size=unique_definition([(s['st_shndx'],int(s['st_value']),int(s['st_size'])) for s in syms])
        sonames=[t.soname for t in img.elf.get_section_by_name('.dynamic').iter_tags() if t.entry.d_tag=='DT_SONAME']
        qualify_core_identity(img.elf.elfclass,img.elf['e_machine'],sonames,syms[0]['st_info']['type'])
        if (address,size,img.containing_fde(address))!=(0x1d3570,506,(0x1d3570,0x1d376a)):
            raise ValueError('PROMOTED_CONNECTIMPL_IDENTITY_CHANGED')
        qualify_branch(img.read(0x1d36fb,6),0x1d36fb,0xc6c16)
        lo,hi=bounded_region(img.fdes,0xc6c16)
        if not any(slo<=lo and hi<=shi and flags&4 for slo,shi,off,flags in img.sections):
            raise ValueError('CONTINUATION_NOT_EXECUTABLE')
        flow=first_transfers(img.read(lo,hi-lo),lo,0xc6c16)
        for edge in flow['boundaries']:
            if edge['kind']!='CALL': continue
            target=int(edge['target'],16)
            extent=plt_extent([(s.name,int(s['sh_addr']),int(s['sh_addr'])+int(s['sh_size'])) for s in img.elf.iter_sections()],target)
            edge['static_import_symbol']=plt_binding(img.read(target,extent),target,img.symbol_relocations) if extent else None
            edge['callee_implementation_semantics']='UNKNOWN'
        return {
            'schema':'otclient.track-a.be4f48-qt-c6c16.v1',
            'exact_client':{'version':EXPECTED_VERSION,'size':EXPECTED_SIZE,'sha256':EXPECTED_SHA256},
            'packaged_qtcore':selected['qtcore'],
            'packaged_identity_is_runtime_loaded_identity':False,
            'FACT':{'branch_site':'0x1d36fb','branch_target':'0xc6c16','branch_kind':'jne',
                    'containing_fde':[hex(lo),hex(hi)],'entry_equals_fde_start':lo==0xc6c16,
                    'first_transfer_flow':flow},
            'INFERENCE':[],
            'UNKNOWN':['cold_partition_semantic_owner','runtime_loaded_qtcore','callee_implementation_semantics','sendlogin_receiver','sendlogin_causal_binding','final_queue_writer','final_tcp_writer','final_writer_contract','field6_value','pre_success_send_sequence'],
            'terminal_result':'POSITIVE_EXACT_CONTINUATION_FIRST_TRANSFER' if flow['complete'] else 'ANALYSIS_INCOMPLETE',
            'FIRST_MISSING_BOUNDARY':'QT_CONTINUATION_FIRST_TRANSFER_CALLEE_SEMANTICS_NOT_PROVEN' if flow['complete'] else 'BOUNDED_CONTINUATION_MODEL_INCOMPLETE',
            'normal_control_only':True,'exceptional_control_not_modeled':True,
            'runtime_access':'none','official_client_executed':False,'login_performed':False,
            'credentials_used':False,'process_memory_access':False,'packet_capture':False,'ocr_vision_used':False,
            'official_service_e2e_count':0,'track_b_pr_284_modified':False,'track_b_current_wire_delta':'NOT_PROVEN',
            'field6_value':'UNKNOWN','final_writer_contract':'UNKNOWN','pre_success_send_sequence':'UNKNOWN'}
    finally: img.close()


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--manifest',type=Path);p.add_argument('--selection',type=Path,required=True)
    p.add_argument('--client',type=Path);p.add_argument('--qtcore',type=Path);p.add_argument('--output',type=Path)
    a=p.parse_args()
    if a.manifest:
        a.selection.write_text(json.dumps(select_package(json.loads(a.manifest.read_text())),sort_keys=True)+'\n')
    else:
        result=analyze(json.loads(a.selection.read_text()),a.client,a.qtcore)
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
