#!/usr/bin/env python3
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from static_flow import Image, trace_paths, verify_fence, EXPECTED_VERSION, EXPECTED_SIZE, EXPECTED_SHA256
from receiver_flow import receiver_flow

SYMBOL='_ZN7QObject11connectImplEPKS_PPvS1_S3_PN9QtPrivate15QSlotObjectBaseEN2Qt14ConnectionTypeEPKiPK11QMetaObject'

def qualify_dependency_fence(row):
    if row['unpackedhash']!='03ac3e4e7356399897ec58d42c81ae5c257072d45d539de1def528a8a04911fa' or row['unpackedsize']!=7354472:
        raise ValueError('QTCORE_DISCOVERED_EXACT_FENCE_MOVED')

def only_external_branches(path):
    rows=path.get('incomplete_boundaries',[])
    return bool(not path['complete'] and rows and all(r['kind']=='BRANCH_OUTSIDE_FDE' and re.fullmatch(r'0x[0-9a-f]+',r['target']) for r in rows))

def safe_row(row):
    keys=('localfile','unpackedhash','unpackedsize','packedhash','packedsize','url')
    out={k:row[k] for k in keys}
    for key in ('localfile','url'):
        v=out[key]
        if not isinstance(v,str) or not re.fullmatch(r'[A-Za-z0-9_./-]+',v) or v.startswith('/') or '..' in PurePosixPath(v).parts:
            raise ValueError('UNSAFE_PACKAGE_MEMBER_PATH')
    for key in ('unpackedhash','packedhash'):
        if not isinstance(out[key],str) or not re.fullmatch('[0-9a-f]{64}',out[key]):raise ValueError('INVALID_MEMBER_HASH')
    for key in ('unpackedsize','packedsize'):
        out[key]=int(out[key])
        if not 0<out[key]<=200_000_000:raise ValueError('MEMBER_SIZE_OUTSIDE_BOUND')
    return out

def select_package(package):
    files=package.get('files',[])
    clients=[r for r in files if isinstance(r,dict) and r.get('localfile')=='bin/client']
    if len(clients)!=1 or package.get('version')!=EXPECTED_VERSION:raise ValueError('EXACT_PACKAGE_FENCE_MISMATCH')
    client=safe_row(clients[0])
    if client['unpackedhash']!=EXPECTED_SHA256 or client['unpackedsize']!=EXPECTED_SIZE:raise ValueError('EXACT_CLIENT_FENCE_MISMATCH')
    cores=[r for r in files if isinstance(r,dict) and re.fullmatch(r'libQt6Core\.so\.6(?:\.\d+)*',PurePosixPath(str(r.get('localfile',''))).name)]
    core=safe_row(cores[0]) if len(cores)==1 else None
    return {'version':EXPECTED_VERSION,'client':client,'qtcore':core,'qtcore_named_member_count':len(cores),
            'selection_boundary':None if core else 'NO_UNIQUE_PACKAGED_QTCORE_MEMBER'}

def verify_member(raw,row):
    if len(raw)!=row['unpackedsize'] or hashlib.sha256(raw).hexdigest()!=row['unpackedhash']:raise ValueError('EXACT_MEMBER_FENCE_MISMATCH')

def unique_definition(rows):
    if len(rows)!=1 or rows[0][0]=='SHN_UNDEF' or rows[0][1]<=0 or not 0<rows[0][2]<=0x4000:
        raise ValueError('NO_UNIQUE_BOUNDED_DEFINED_CONNECTIMPL')
    return rows[0][1],rows[0][2]

def resolved_delegation(complete,rows):
    return bool(complete and len(rows)==1 and re.fullmatch(r'0x[0-9a-f]+',str(rows[0]['target'])) and int(rows[0]['target'],16)>0)

def qualify_core_identity(elfclass,machine,sonames,symbol_type):
    if (elfclass,machine,sonames,symbol_type)!=(64,'EM_X86_64',['libQt6Core.so.6'],'STT_FUNC'):
        raise ValueError('QTCORE_ELF_SONAME_OR_FUNCTION_NOT_QUALIFIED')

def analyze(selected,client,core):
    verify_fence(client.read_bytes(),selected['version'])
    img=Image(client)
    try:
        if img.elf.elfclass!=64 or img.elf['e_machine']!='EM_X86_64':raise ValueError('CLIENT_ELF_ARCHITECTURE_MISMATCH')
        dyn=img.elf.get_section_by_name('.dynamic')
        needed=[t.needed for t in dyn.iter_tags() if t.entry.d_tag=='DT_NEEDED' and t.needed=='libQt6Core.so.6']
        imports=[s for s in img.elf.get_section_by_name('.dynsym').iter_symbols() if s.name==SYMBOL]
        if len(needed)!=1 or len(imports)!=1 or imports[0]['st_shndx']!='SHN_UNDEF':raise ValueError('CLIENT_QTCORE_DEPENDENCY_OR_IMPORT_NOT_QUALIFIED')
    finally:img.close()
    result={'schema':'otclient.track-a.be4f48-qt-receiver-delegation.v1',
            'exact_client':{'version':EXPECTED_VERSION,'size':EXPECTED_SIZE,'sha256':EXPECTED_SHA256},
            'client_dt_needed':'libQt6Core.so.6','selected_symbol':SYMBOL,
            'packaged_qtcore':selected['qtcore'],'qtcore_named_member_count':selected['qtcore_named_member_count'],
            'packaged_identity_is_runtime_loaded_identity':False,'runtime_loaded_qtcore':'UNKNOWN',
            'receiver_delegation_proven':False,'external_qt_receiver_binding':'NOT_PROVEN',
            'terminal_result':'SOURCE_BLOCKER','FIRST_MISSING_BOUNDARY':selected['selection_boundary'],
            'runtime_access':'none','official_client_executed':False,'login_performed':False,
            'credentials_used':False,'process_memory_access':False,'packet_capture':False,'ocr_vision_used':False,
            'official_service_e2e_count':0,'track_b_pr_284_modified':False,
            'field6_value':'UNKNOWN','final_writer_contract':'UNKNOWN','pre_success_send_sequence':'UNKNOWN'}
    if not selected['qtcore']:return result
    qualify_dependency_fence(selected['qtcore'])
    verify_member(core.read_bytes(),selected['qtcore'])
    img=Image(core)
    try:
        syms=[s for s in img.elf.get_section_by_name('.dynsym').iter_symbols() if s.name==SYMBOL]
        address,size=unique_definition([(s['st_shndx'],int(s['st_value']),int(s['st_size'])) for s in syms])
        sonames=[t.soname for t in img.elf.get_section_by_name('.dynamic').iter_tags() if t.entry.d_tag=='DT_SONAME']
        qualify_core_identity(img.elf.elfclass,img.elf['e_machine'],sonames,syms[0]['st_info']['type'])
        fde=img.containing_fde(address)
        if not fde or fde[0]!=address or fde[1]-fde[0]>0x4000:raise ValueError('CONNECTIMPL_FDE_NOT_EXACT_OR_BOUNDED')
        path=receiver_flow(img.read(fde[0],fde[1]-fde[0]),fde[0])
        candidates={json.dumps(c,sort_keys=True):c for c in path['receiver_delegations']}
        result.update({'qt_connectimpl_address':hex(address),'qt_connectimpl_fde':[hex(x) for x in fde],
                       'qt_connectimpl_symbol_size':size,'analysis_complete':path['complete'],
                       'analysis_fixedpoint_reached':path['fixedpoint_reached'],
                       'analysis_state_updates':path['state_updates'],
                       'analysis_reachable_instructions':path['reachable_instructions'],
                       'receiver_delegations':list(candidates.values()),
                       'receiver_delegation_scope':'conditional modeled in-FDE paths only; no completeness across external continuations',
                       'incomplete_boundaries':path['incomplete_boundaries']})
        proven=resolved_delegation(path['complete'],list(candidates.values()))
        if proven:
            target=int(next(iter(candidates.values()))['target'],16)
            target_fde=img.containing_fde(target)
            proven=bool((target_fde and target_fde[0]==target) or img.plt_symbol(target))
        result['qtcore_elf_identity']={'class':64,'machine':'EM_X86_64','soname':sonames[0],'symbol_type':'STT_FUNC'}
        result['receiver_delegation_proven']=proven
        result['terminal_result']='SOURCE_BLOCKER' if path['complete'] else 'ANALYSIS_INCOMPLETE'
        result['FIRST_MISSING_BOUNDARY']='DELEGATED_QT_RECEIVER_REGISTRATION_STORAGE_AND_DELIVERY_NOT_PROVEN' if proven else 'NO_UNIQUE_PROVEN_QT_RECEIVER_DELEGATION' if path['complete'] else 'COMPLETE_BOUNDED_QT_CONNECTIMPL_FLOW_REQUIRED'
        if only_external_branches(path):
            result['terminal_result']='SOURCE_BLOCKER'
            result['FIRST_MISSING_BOUNDARY']='EXACT_QT_CONNECTIMPL_OUT_OF_FDE_CONTINUATION_SEMANTICS_NOT_PROVEN'
        return result
    finally:img.close()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--manifest',type=Path);p.add_argument('--selection',type=Path,required=True);p.add_argument('--client',type=Path);p.add_argument('--qtcore',type=Path);p.add_argument('--output',type=Path)
    a=p.parse_args()
    if a.manifest:
        selected=select_package(json.loads(a.manifest.read_text()))
        a.selection.write_text(json.dumps(selected,sort_keys=True)+'\n')
    else:
        result=analyze(json.loads(a.selection.read_text()),a.client,a.qtcore)
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
