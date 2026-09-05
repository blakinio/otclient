#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

GDB_TAIL="end\ncontinue\n'''\n"
GDB_REPL=r"""end
continue
python
# V21: after native character confirmation and real AUTH start-state execution,
# invoke original TGameClient::connectClientToGameserverWithExistingCredentials
# only if its real implementation has not run. No auth/session payload is read.
import gdb,struct,re
inf=gdb.selected_inferior();bias=@BIAS@;ev21=r'@EV@'
def emit21(s):gdb.write(s+'\n')
def count21(n):
    try:return sum(1 for l in open(ev21,errors='replace') if l.rstrip().endswith('\t'+n))
    except:return 0
def rw21():
    out=[]
    try:
        for l in open(f'/proc/{inf.pid}/maps',errors='replace'):
            p=l.split()
            if len(p)>=2 and p[1].startswith('rw') and 'p' in p[1]:
                a,b=(int(x,16) for x in p[0].split('-'))
                if b>a:out.append((a,b))
    except:pass
    return out
def scan21(v):
    needle=struct.pack('<Q',v);hits=[]
    for a,b in rw21():
        cur=a
        while cur<b:
            try:f=inf.search_memory(cur,b-cur,needle)
            except:f=None
            if f is None:break
            x=int(f);hits.append(x)
            if len(hits)>16:return hits
            cur=x+8
    return hits
def resolve21(mangled,demangled):
    for e in (f'(void*){mangled}',f"(void*)&'{demangled}'"):
        try:
            v=int(gdb.parse_and_eval(e))
            if v:return v
        except:pass
    return 0
def elf_file_bytes21(va,n):
    try:
        raw=open(f'/proc/{inf.pid}/exe','rb').read()
        if raw[:4]!=b'\x7fELF' or raw[4]!=2 or raw[5]!=1:return None
        phoff=struct.unpack_from('<Q',raw,32)[0];phentsz=struct.unpack_from('<H',raw,54)[0];phnum=struct.unpack_from('<H',raw,56)[0]
        for i in range(phnum):
            o=phoff+i*phentsz
            if o+56>len(raw):break
            p_type,p_flags=struct.unpack_from('<II',raw,o);p_offset,p_vaddr,p_paddr,p_filesz,p_memsz,p_align=struct.unpack_from('<QQQQQQ',raw,o+8)
            if p_type==1 and p_vaddr<=va and va+n<=p_vaddr+p_filesz:
                q=p_offset+(va-p_vaddr);return raw[q:q+n]
    except:pass
    return None
start=count21('StartGameServerLoginImpl');conn=count21('ConnectExistingImpl')
emit21('WORLDMAP_V21_PRE_FALLBACK_START_IMPL_COUNT='+str(start));emit21('WORLDMAP_V21_PRE_FALLBACK_CONNECT_IMPL_COUNT='+str(conn))
if start<1 or conn>0:
    emit21('WORLDMAP_V21_GAMECLIENT_FALLBACK=REFUSED_PRECONDITION')
else:
    hits=scan21(bias+0x3076908);emit21('WORLDMAP_V21_GAMECLIENT_INSTANCE_COUNT='+str(len(hits)))
    if len(hits)!=1:emit21('WORLDMAP_V21_GAMECLIENT_FALLBACK=FAIL:gameclient_instance_count')
    else:
        gc=hits[0];vp=mem(gc,8);rv=mem(bias+0xd06260,24);fv=elf_file_bytes21(0xd06260,24);rc=mem(bias+0xd06660,16);fc=elf_file_bytes21(0xd06660,16)
        if vp is None or struct.unpack('<Q',vp)[0]!=bias+0x3076908:emit21('WORLDMAP_V21_GAMECLIENT_FALLBACK=FAIL:vptr')
        elif rv is None or fv is None or rv!=fv or rc is None or fc is None or rc!=fc:emit21('WORLDMAP_V21_GAMECLIENT_FALLBACK=FAIL:runtime_instruction_fence')
        else:
            emit21('WORLDMAP_V21_GAMECLIENT_RUNTIME_ADDRESS_PROVEN=PASS')
            mains=[t for t in inf.threads() if len(t.ptid)>=2 and t.ptid[1]==inf.pid]
            if len(mains)!=1:emit21('WORLDMAP_V21_GAMECLIENT_FALLBACK=FAIL:main_lwp')
            else:
                mains[0].switch();gdb.execute('set scheduler-locking on',to_string=True)
                qt=resolve21('_ZNK7QObject6threadEv','QObject::thread() const');qc=resolve21('_ZN7QThread13currentThreadEv','QThread::currentThread()')
                try:
                    owner=int(gdb.parse_and_eval(f'((void*(*)(void*))0x{qt:x})((void*)0x{gc:x})')) if qt else 0
                    current=int(gdb.parse_and_eval(f'((void*(*)())0x{qc:x})()')) if qc else -1
                except:owner=0;current=-1
                result=''
                if owner==0 or owner!=current:result='FAIL:qt_thread_affinity'
                else:
                    emit21('WORLDMAP_V21_GAMECLIENT_QT_THREAD_AFFINITY=PASS');ok=False
                    try:
                        gdb.parse_and_eval(f'((void(*)(void*,int,int,void**))0x{bias+0xd06260:x})((void*)0x{gc:x},0,11,(void**)0)');ok=True
                    except:ok=False
                    if ok:emit21('WORLDMAP_V21_GAMECLIENT_METHOD11_QMETA_INVOCATION=PASS');result='PASS'
                    else:result='FAIL:qmeta_invocation'
                gdb.execute('set scheduler-locking off',to_string=True);emit21('WORLDMAP_V21_GAMECLIENT_FALLBACK='+result)
end
continue
'''
"""
SHELL=r'''[[ "$(event_count_v19 StartGameServerLoginImpl)" -ge 1 ]] || fail v20_real_start_game_server_login_not_observed

world=0'''
SHELL_REPL=r'''[[ "$(event_count_v19 StartGameServerLoginImpl)" -ge 1 ]] || fail v20_real_start_game_server_login_not_observed
sleep 3
echo "WORLDMAP_V21_PRE_CONNECT_IMPL_COUNT=$(event_count_v19 ConnectExistingImpl)"
if [[ "$(event_count_v19 ConnectExistingImpl)" -eq 0 ]];then
  kill -INT "$GDB_PID" 2>/dev/null||fail v21_gameclient_fallback_interrupt_failed
  V21FB=0
  for _ in $(seq 1 160);do
    sleep .25
    if grep -Fq 'WORLDMAP_V21_GAMECLIENT_FALLBACK=PASS' "$GOUT" 2>/dev/null;then V21FB=1;break;fi
    if grep -Fq 'WORLDMAP_V21_GAMECLIENT_FALLBACK=FAIL:' "$GOUT" 2>/dev/null||grep -Fq 'WORLDMAP_V21_GAMECLIENT_FALLBACK=REFUSED_PRECONDITION' "$GOUT" 2>/dev/null;then break;fi
    kill -0 "$GDB_PID" 2>/dev/null||break
  done
  grep -E '^WORLDMAP_V21_(PRE_FALLBACK_START_IMPL_COUNT|PRE_FALLBACK_CONNECT_IMPL_COUNT|GAMECLIENT_INSTANCE_COUNT|GAMECLIENT_RUNTIME_ADDRESS_PROVEN|GAMECLIENT_QT_THREAD_AFFINITY|GAMECLIENT_METHOD11_QMETA_INVOCATION|GAMECLIENT_FALLBACK)=' "$GOUT" 2>/dev/null|tail -20||true
  [[ "$V21FB" == 1 ]]||fail v21_gameclient_fallback_failed
  sleep 6
fi
echo "WORLDMAP_V21_POST_CONNECT_IMPL_COUNT=$(event_count_v19 ConnectExistingImpl)"
echo "WORLDMAP_V21_POST_ONCONNECT_IMPL_COUNT=$(event_count_v19 OnConnectGameserverImpl)"
echo "WORLDMAP_V21_POST_SESSION_CONNECTED_IMPL_COUNT=$(event_count_v19 GameSessionConnectedImpl)"
[[ "$(event_count_v19 ConnectExistingImpl)" -ge 1 ]]||fail v21_real_connect_existing_not_observed

world=0'''
class Refused(RuntimeError):pass
def transform(s:str)->str:
    if s.count(GDB_TAIL)!=1:raise Refused(f'GDB_TAIL:{s.count(GDB_TAIL)}')
    s=s.replace(GDB_TAIL,GDB_REPL,1)
    if s.count(SHELL)!=1:raise Refused(f'SHELL:{s.count(SHELL)}')
    s=s.replace(SHELL,SHELL_REPL,1)
    req=('WORLDMAP_V21_GAMECLIENT_INSTANCE_COUNT=','WORLDMAP_V21_GAMECLIENT_RUNTIME_ADDRESS_PROVEN=PASS','WORLDMAP_V21_GAMECLIENT_QT_THREAD_AFFINITY=PASS','WORLDMAP_V21_GAMECLIENT_METHOD11_QMETA_INVOCATION=PASS','WORLDMAP_V21_GAMECLIENT_FALLBACK=PASS','elf_file_bytes21','WORLDMAP_V21_POST_CONNECT_IMPL_COUNT=')
    m=[x for x in req if x not in s]
    if m:raise Refused('MISSING:'+','.join(m))
    bad=('Invalid Monk',"M(0xd47300,'RequestCharacterLogin')","M(0xd47130,'CharacterSelectionConfirmed')",'WORLDMAP_V14_CHARACTER_ATTEMPT=','"$XWD" -root','xwd -root')
    b=[x for x in bad if x in s]
    if b:raise Refused('BAD:'+','.join(b))
    if s.count('set scheduler-locking on')!=4 or s.count('set scheduler-locking off')!=4:raise Refused('SCHED')
    return s
def main():
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    try:o=transform(a.source.read_text())
    except Refused as e:print('WORLDMAP_GAMECLIENT_CONNECT_V21_REPAIR_REFUSED='+str(e));return 44
    a.output.write_text(o);a.output.chmod(0o700);print('WORLDMAP_GAMECLIENT_CONNECT_V21_REPAIR=PASS');return 0
if __name__=='__main__':raise SystemExit(main())
