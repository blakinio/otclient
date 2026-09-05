#!/usr/bin/env python3
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from static_flow import Image, verify_fence, EXPECTED_VERSION, EXPECTED_SIZE, EXPECTED_SHA256

SYMBOL='_ZN7QObject11connectImplEPKS_PPvS1_S3_PN9QtPrivate15QSlotObjectBaseEN2Qt14ConnectionTypeEPKiPK11QMetaObject'

def qualify_dependency_fence(row):
    if row['unpackedhash']!='03ac3e4e7356399897ec58d42c81ae5c257072d45d539de1def528a8a04911fa' or row['unpackedsize']!=7354472:
        raise ValueError('QTCORE_DISCOVERED_EXACT_FENCE_MOVED')


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


def qualify_core_identity(elfclass,machine,sonames,symbol_type):
    if (elfclass,machine,sonames,symbol_type)!=(64,'EM_X86_64',['libQt6Core.so.6'],'STT_FUNC'):
        raise ValueError('QTCORE_ELF_SONAME_OR_FUNCTION_NOT_QUALIFIED')
