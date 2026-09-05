"""Selected GNU hash metadata lookup; no function or unrelated symbol reads."""
import struct
NAME = '_ZN11QMetaObject8activateEP7QObjectPKS_iPPv'

def lookup(raw, sections, name=NAME, chain_limit=128, candidate_limit=8):
    def read(s, offset, size):
        overlaps=[x for x in sections if x['flags']&2 and x['size']>0 and
                  x['addr']<s['addr']+s['size'] and s['addr']<x['addr']+x['size']]
        if len(overlaps)!=1 or overlaps[0]['index']!=s['index']:
            raise ValueError('SECTION_MAPPING')
        if not (0 <= offset <= offset+size <= s['size'] and
                0 <= s['off']+offset <= s['off']+offset+size <= len(raw)):
            raise ValueError('SECTION_READ_BOUNDS')
        return raw[s['off']+offset:s['off']+offset+size]

    def selected(addr, typ):
        matches = [s for s in sections if s['flags']&2 and
                   s['addr'] <= addr < s['addr']+s['size']]
        if len(matches)!=1 or matches[0]['addr']!=addr or matches[0]['type']!=typ:
            raise ValueError('SECTION_MAPPING')
        return matches[0]

    dynamic=[s for s in sections if s['type']=='SHT_DYNAMIC' and s['flags']&2]
    if len(dynamic)!=1 or dynamic[0]['entsize']!=16 or dynamic[0]['size']%16:
        raise ValueError('DYNAMIC_SECTION')
    tags={}; terminated=False
    for i in range(min(512,dynamic[0]['size']//16)):
        tag,val=struct.unpack('<QQ',read(dynamic[0],i*16,16))
        if tag==0:
            terminated=True; break
        if tag in (0x6ffffef5,6,11,5):
            if tag in tags: raise ValueError('DYNAMIC_TAGS_DUPLICATE')
            tags[tag]=val
    if not terminated:
        raise ValueError('DYNAMIC_ENTRY_LIMIT' if dynamic[0]['size']//16>=512 else 'DYNAMIC_NOT_TERMINATED')
    if set(tags)!={0x6ffffef5,6,11,5} or tags[11]!=24:
        raise ValueError('DYNAMIC_TAGS')
    gh=selected(tags[0x6ffffef5],'SHT_GNU_HASH')
    sym=selected(tags[6],'SHT_DYNSYM'); strings=selected(tags[5],'SHT_STRTAB')
    for section in (dynamic[0],gh,sym,strings):
        if not 0<=section['off']<=section['off']+section['size']<=len(raw):
            raise ValueError('SECTION_FILE_BOUNDS')
    if gh['link']!=sym['index'] or sym['link']!=strings['index']:
        raise ValueError('SECTION_LINK')
    if sym['entsize']!=24 or sym['size']%24:
        raise ValueError('SYMBOL_WIDTH')
    buckets,symoffset,bloomsize,shift=struct.unpack('<IIII',read(gh,0,16))
    chain_start=16+bloomsize*8+buckets*4
    if not buckets or not bloomsize or bloomsize&(bloomsize-1) or shift>=64 or chain_start>gh['size'] or (gh['size']-chain_start)%4:
        raise ValueError('HASH_HEADER')
    h=5381
    for c in name.encode('ascii'): h=(h*33+c)&0xffffffff
    bloom=struct.unpack('<Q',read(gh,16+((h//64)&(bloomsize-1))*8,8))[0]
    mask=(1<<(h%64))|(1<<((h>>shift)%64))
    if bloom&mask!=mask: raise ValueError('BLOOM_NEGATIVE')
    idx=struct.unpack('<I',read(gh,16+bloomsize*8+(h%buckets)*4,4))[0]
    if idx==0: raise ValueError('BUCKET_EMPTY')
    count=0; candidates=0; matches=[]
    while True:
        if count>=min(chain_limit,128): raise ValueError('HASH_CHAIN_LIMIT')
        if idx<symoffset or idx>=sym['size']//24: raise ValueError('SYMBOL_INDEX')
        chain=struct.unpack('<I',read(gh,chain_start+(idx-symoffset)*4,4))[0]
        count+=1
        if (chain|1)==(h|1):
            if candidates>=min(candidate_limit,8): raise ValueError('HASH_CANDIDATE_LIMIT')
            candidates+=1
            stname,info,other,shndx,value,size=struct.unpack('<IBBHQQ',read(sym,idx*24,24))
            if not 0<=stname<strings['size']: raise ValueError('NAME_OFFSET')
            rawname=read(strings,stname,min(513,strings['size']-stname))
            end=rawname.find(b'\0')
            if end<0 or end>512: raise ValueError('NAME_TERMINATOR')
            try: candidate=rawname[:end].decode('ascii')
            except UnicodeDecodeError: raise ValueError('NAME_ASCII') from None
            if candidate==name: matches.append((idx,info,other,shndx,value,size))
        if chain&1: break
        idx+=1
    if len(matches)!=1: raise ValueError('NAME_MATCH_COUNT')
    idx,info,other,shndx,value,size=matches[0]
    if info&15!=2 or info>>4 not in (1,2) or other&3 or not 0<shndx<0xff00:
        raise ValueError('DEFINITION_RECORD')
    owners=[s for s in sections if s['flags']&2 and s['size']>0 and s['addr']<value+size and value<s['addr']+s['size']]
    if len(owners)!=1 or not owners[0]['addr']<=value<value+size<=owners[0]['addr']+owners[0]['size'] or owners[0]['index']!=shndx or owners[0]['flags']&6!=6 or owners[0]['type']=='SHT_NOBITS':
        raise ValueError('DEFINITION_EXTENT')
    owner=owners[0]
    if not 0<=owner['off']<=owner['off']+owner['size']<=len(raw):
        raise ValueError('DEFINITION_EXTENT_FILE_BOUNDS')
    return dict(name=name,symbol_index=idx,address=hex(value),size=size,
                extent=[hex(value),hex(value+size)],section_index=shndx,
                hash=h,bloom_words=1,buckets_read=1,chain_entries=count,candidate_names=candidates,
                selected_dynamic_tags={str(k):hex(v) for k,v in sorted(tags.items())},
                runtime_resolution_proven=False,symbol_version_resolution_proven=False)
