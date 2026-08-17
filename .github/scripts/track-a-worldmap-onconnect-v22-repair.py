#!/usr/bin/env python3
from pathlib import Path
import argparse
G="end\ncontinue\n'''\n"
GR=r"""end
continue
python
import gdb,struct
inf=gdb.selected_inferior();bias=@BIAS@;ev22=r'@EV@'
def e22(s):gdb.write(s+'\n')
def c22(n):
    try:return sum(1 for l in open(ev22,errors='replace') if l.rstrip().endswith('\t'+n))
    except:return 0
def ranges():
    o=[]
    try:
        for l in open(f'/proc/{inf.pid}/maps',errors='replace'):
            p=l.split()
            if len(p)>=2 and p[1].startswith('rw') and 'p' in p[1]:
                a,b=(int(x,16) for x in p[0].split('-'))
                if b>a:o.append((a,b))
    except:pass
    return o
def scan(v):
    q=struct.pack('<Q',v);h=[]
    for a,b in ranges():
        x=a
        while x<b:
            try:f=inf.search_memory(x,b-x,q)
            except:f=None
            if f is None:break
            y=int(f);h.append(y);x=y+8
            if len(h)>16:return h
    return h
def sym(m,d):
    for z in (f'(void*){m}',f"(void*)&'{d}'"):
        try:
            v=int(gdb.parse_and_eval(z))
            if v:return v
        except:pass
    return 0
def fbytes(va,n):
    try:
        r=open(f'/proc/{inf.pid}/exe','rb').read();ph=struct.unpack_from('<Q',r,32)[0];psz=struct.unpack_from('<H',r,54)[0];pn=struct.unpack_from('<H',r,56)[0]
        for i in range(pn):
            o=ph+i*psz;t,fl=struct.unpack_from('<II',r,o);po,pv,pp,pfs,pms,al=struct.unpack_from('<QQQQQQ',r,o+8)
            if t==1 and pv<=va and va+n<=pv+pfs:
                x=po+va-pv;return r[x:x+n]
    except:pass
    return None
conn=c22('ConnectExistingImpl');onc=c22('OnConnectGameserverImpl');e22('WORLDMAP_V22_PRE_CONNECT_IMPL_COUNT='+str(conn));e22('WORLDMAP_V22_PRE_ONCONNECT_IMPL_COUNT='+str(onc))
if conn<1 or onc>0:e22('WORLDMAP_V22_ONCONNECT_FALLBACK=REFUSED_PRECONDITION')
else:
    h=scan(bias+0x3076908);e22('WORLDMAP_V22_GAMECLIENT_INSTANCE_COUNT='+str(len(h)))
    if len(h)!=1:e22('WORLDMAP_V22_ONCONNECT_FALLBACK=FAIL:gameclient_instance_count')
    else:
        gc=h[0];vp=mem(gc,8);r1=mem(bias+0xd06260,24);f1=fbytes(0xd06260,24);r2=mem(bias+0xd06810,16);f2=fbytes(0xd06810,16)
        if vp is None or struct.unpack('<Q',vp)[0]!=bias+0x3076908:e22('WORLDMAP_V22_ONCONNECT_FALLBACK=FAIL:vptr')
        elif None in (r1,f1,r2,f2) or r1!=f1 or r2!=f2:e22('WORLDMAP_V22_ONCONNECT_FALLBACK=FAIL:runtime_instruction_fence')
        else:
            e22('WORLDMAP_V22_GAMECLIENT_RUNTIME_ADDRESS_PROVEN=PASS');m=[t for t in inf.threads() if len(t.ptid)>=2 and t.ptid[1]==inf.pid]
            if len(m)!=1:e22('WORLDMAP_V22_ONCONNECT_FALLBACK=FAIL:main_lwp')
            else:
                m[0].switch();gdb.execute('set scheduler-locking on',to_string=True);qt=sym('_ZNK7QObject6threadEv','QObject::thread() const');qc=sym('_ZN7QThread13currentThreadEv','QThread::currentThread()')
                try:o=int(gdb.parse_and_eval(f'((void*(*)(void*))0x{qt:x})((void*)0x{gc:x})'));cur=int(gdb.parse_and_eval(f'((void*(*)())0x{qc:x})()'))
                except:o=0;cur=-1
                res=''
                if o==0 or o!=cur:res='FAIL:qt_thread_affinity'
                else:
                    e22('WORLDMAP_V22_GAMECLIENT_QT_THREAD_AFFINITY=PASS');ok=False
                    try:gdb.parse_and_eval(f'((void(*)(void*,int,int,void**))0x{bias+0xd06260:x})((void*)0x{gc:x},0,20,(void**)0)');ok=True
                    except:pass
                    if ok:e22('WORLDMAP_V22_GAMECLIENT_METHOD20_QMETA_INVOCATION=PASS');res='PASS'
                    else:res='FAIL:qmeta_invocation'
                gdb.execute('set scheduler-locking off',to_string=True);e22('WORLDMAP_V22_ONCONNECT_FALLBACK='+res)
end
continue
'''
"""
S='''[[ "$(event_count_v19 ConnectExistingImpl)" -ge 1 ]]||fail v21_real_connect_existing_not_observed

world=0'''
SR='''[[ "$(event_count_v19 ConnectExistingImpl)" -ge 1 ]]||fail v21_real_connect_existing_not_observed
sleep 3
echo "WORLDMAP_V22_PRE_ONCONNECT_IMPL_COUNT=$(event_count_v19 OnConnectGameserverImpl)"
if [[ "$(event_count_v19 OnConnectGameserverImpl)" -eq 0 ]];then
  kill -INT "$GDB_PID" 2>/dev/null||fail v22_onconnect_interrupt_failed
  V22=0
  for _ in $(seq 1 160);do sleep .25;if grep -Fq 'WORLDMAP_V22_ONCONNECT_FALLBACK=PASS' "$GOUT" 2>/dev/null;then V22=1;break;fi;if grep -Fq 'WORLDMAP_V22_ONCONNECT_FALLBACK=FAIL:' "$GOUT" 2>/dev/null||grep -Fq 'WORLDMAP_V22_ONCONNECT_FALLBACK=REFUSED_PRECONDITION' "$GOUT" 2>/dev/null;then break;fi;done
  [[ "$V22" == 1 ]]||fail v22_onconnect_fallback_failed;sleep 6
fi
echo "WORLDMAP_V22_POST_ONCONNECT_IMPL_COUNT=$(event_count_v19 OnConnectGameserverImpl)"
echo "WORLDMAP_V22_SESSION_CONNECTED_IMPL_COUNT=$(event_count_v19 GameSessionConnectedImpl)"
[[ "$(event_count_v19 OnConnectGameserverImpl)" -ge 1 ]]||fail v22_real_onconnect_not_observed

world=0'''
def transform(s):
    if s.count(G)!=1:raise RuntimeError('g')
    s=s.replace(G,GR,1)
    if s.count(S)!=1:raise RuntimeError('s')
    s=s.replace(S,SR,1)
    if s.count('set scheduler-locking on')!=5 or s.count('set scheduler-locking off')!=5:raise RuntimeError('sched')
    if 'Invalid Monk' in s:raise RuntimeError('target')
    return s
def main():
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    try:o=transform(a.source.read_text())
    except Exception as x:print('WORLDMAP_ONCONNECT_V22_REPAIR_REFUSED='+str(x));return 44
    a.output.write_text(o);a.output.chmod(0o700);print('WORLDMAP_ONCONNECT_V22_REPAIR=PASS');return 0
if __name__=='__main__':raise SystemExit(main())
