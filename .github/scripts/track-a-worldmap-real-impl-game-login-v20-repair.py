#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

SIGNAL_BP = "M(0xcfb2e7,'RequestCharacterGameserverLogin')"
SIGNAL_BP_REPL = r'''auth_signal_this_file=os.path.join(os.path.dirname(ev),'v20-auth-signal-this.txt')
try: open(auth_signal_this_file,'w').close(); os.chmod(auth_signal_this_file,0o600)
except: pass
class AuthSignal5(gdb.Breakpoint):
    def __init__(self): super().__init__('*0x%x'%(bias+0xcfb2e7),internal=False)
    def stop(self):
        try:
            with open(ev,'a') as f:f.write(f'{time.time_ns()}\tRequestCharacterGameserverLogin\n')
            with open(auth_signal_this_file,'a') as f:f.write('0x%x\n'%int(gdb.parse_and_eval('$rdi')))
        except: pass
        return False
AuthSignal5()'''

IMPL_ANCHOR = "M(0xd064c8,'GameSessionDisconnected')"
IMPL_REPL = """M(0xd064c8,'GameSessionDisconnected');M(0x767440,'StartGameServerLoginImpl');M(0x6ef1d0,'ConnectExistingImpl');M(0x6fe480,'OnConnectGameserverImpl');M(0x6ee130,'GameSessionConnectedImpl')"""

GDB_TAIL = "end\ncontinue\n'''\n"
GDB_TAIL_REPL = r"""end
continue
python
# V20: only when signal5 was observed but its real state-entry implementation
# did not run, invoke the original AUTH QMeta method27 on the exact same object
# that emitted signal5. No credential/session payload is inspected or created.
import os,re,struct,gdb
inf=gdb.selected_inferior(); bias=@BIAS@; ev20=r'@EV@'

def emit20(s): gdb.write(s+'\n')
def count20(name):
    try:return sum(1 for l in open(ev20,errors='replace') if l.rstrip().endswith('\t'+name))
    except:return 0

def resolve20(mangled,demangled):
    for expr in (f'(void*){mangled}',f"(void*)&'{demangled}'"):
        try:
            v=int(gdb.parse_and_eval(expr))
            if v:return v
        except:pass
    return 0

this_file=os.path.join(os.path.dirname(ev20),'v20-auth-signal-this.txt')
vals=[]
try:
    for l in open(this_file,errors='replace'):
        l=l.strip()
        if re.fullmatch(r'0x[0-9a-fA-F]+',l):vals.append(int(l,16))
except:pass
uniq=sorted(set(vals))
emit20('WORLDMAP_V20_AUTH_SIGNAL_THIS_UNIQUE_COUNT='+str(len(uniq)))
sig=count20('RequestCharacterGameserverLogin'); start=count20('StartGameServerLoginImpl')
emit20('WORLDMAP_V20_PRE_FALLBACK_SIGNAL5_COUNT='+str(sig))
emit20('WORLDMAP_V20_PRE_FALLBACK_START_IMPL_COUNT='+str(start))
if sig<1 or start>0:
    emit20('WORLDMAP_V20_STATE_ENTRY_FALLBACK=REFUSED_PRECONDITION')
elif len(uniq)!=1:
    emit20('WORLDMAP_V20_STATE_ENTRY_FALLBACK=FAIL:auth_signal_this_not_unique')
else:
    auth=uniq[0]
    vp=mem(auth,8); p=mem(bias+0xcfabb0,16)
    if vp is None or struct.unpack('<Q',vp)[0] != bias+0x307f1b0:
        emit20('WORLDMAP_V20_STATE_ENTRY_FALLBACK=FAIL:auth_vptr_mismatch')
    elif p is None or p.hex()!='85f6752c83fa320f87f2000000415448':
        emit20('WORLDMAP_V20_STATE_ENTRY_FALLBACK=FAIL:auth_metacall_bytes')
    else:
        mains=[t for t in inf.threads() if len(t.ptid)>=2 and t.ptid[1]==inf.pid]
        if len(mains)!=1:
            emit20('WORLDMAP_V20_STATE_ENTRY_FALLBACK=FAIL:main_lwp_not_unique')
        else:
            mains[0].switch();gdb.execute('set scheduler-locking on',to_string=True)
            qt=resolve20('_ZNK7QObject6threadEv','QObject::thread() const');qc=resolve20('_ZN7QThread13currentThreadEv','QThread::currentThread()')
            try:
                owner=int(gdb.parse_and_eval(f'((void*(*)(void*))0x{qt:x})((void*)0x{auth:x})')) if qt else 0
                current=int(gdb.parse_and_eval(f'((void*(*)())0x{qc:x})()')) if qc else -1
            except:owner=0;current=-1
            result=''
            if owner==0 or owner!=current:
                result='FAIL:qt_thread_affinity'
            else:
                emit20('WORLDMAP_V20_AUTH_QT_THREAD_AFFINITY=PASS')
                ok=False
                try:
                    gdb.parse_and_eval(f'((void(*)(void*,int,int,void**))0x{bias+0xcfabb0:x})((void*)0x{auth:x},0,27,(void**)0)')
                    ok=True
                except:ok=False
                if ok:
                    emit20('WORLDMAP_V20_AUTH_METHOD27_QMETA_INVOCATION=PASS');result='PASS'
                else:result='FAIL:qmeta_invocation'
            gdb.execute('set scheduler-locking off',to_string=True)
            emit20('WORLDMAP_V20_STATE_ENTRY_FALLBACK='+result)
end
continue
'''
"""

SHELL_ANCHOR = r'''[[ "$(event_count_v19 GameSessionLoginError)" -eq 0 ]] || fail v19_explicit_game_session_login_error

world=0'''
SHELL_REPL = r'''[[ "$(event_count_v19 GameSessionLoginError)" -eq 0 ]] || fail v19_explicit_game_session_login_error

echo "WORLDMAP_V20_REAL_START_IMPL_COUNT=$(event_count_v19 StartGameServerLoginImpl)"
echo "WORLDMAP_V20_REAL_CONNECT_EXISTING_IMPL_COUNT=$(event_count_v19 ConnectExistingImpl)"
echo "WORLDMAP_V20_REAL_ONCONNECT_IMPL_COUNT=$(event_count_v19 OnConnectGameserverImpl)"
echo "WORLDMAP_V20_REAL_SESSION_CONNECTED_IMPL_COUNT=$(event_count_v19 GameSessionConnectedImpl)"
if [[ "$(event_count_v19 StartGameServerLoginImpl)" -eq 0 ]]; then
  kill -INT "$GDB_PID" 2>/dev/null || fail v20_state_entry_fallback_interrupt_failed
  V20FB=0
  for _ in $(seq 1 160); do
    sleep .25
    if grep -Fq 'WORLDMAP_V20_STATE_ENTRY_FALLBACK=PASS' "$GOUT" 2>/dev/null; then V20FB=1;break;fi
    if grep -Fq 'WORLDMAP_V20_STATE_ENTRY_FALLBACK=FAIL:' "$GOUT" 2>/dev/null || grep -Fq 'WORLDMAP_V20_STATE_ENTRY_FALLBACK=REFUSED_PRECONDITION' "$GOUT" 2>/dev/null; then break;fi
    kill -0 "$GDB_PID" 2>/dev/null || break
  done
  grep -E '^WORLDMAP_V20_(AUTH_SIGNAL_THIS_UNIQUE_COUNT|PRE_FALLBACK_SIGNAL5_COUNT|PRE_FALLBACK_START_IMPL_COUNT|AUTH_QT_THREAD_AFFINITY|AUTH_METHOD27_QMETA_INVOCATION|STATE_ENTRY_FALLBACK)=' "$GOUT" 2>/dev/null | tail -20 || true
  [[ "$V20FB" == 1 ]] || fail v20_state_entry_fallback_failed
  sleep 5
fi
for name in StartGameServerLoginImpl ConnectExistingImpl OnConnectGameserverImpl GameSessionConnectedImpl; do
  echo "WORLDMAP_V20_EVENT_${name}=$(event_count_v19 "$name")"
done
[[ "$(event_count_v19 StartGameServerLoginImpl)" -ge 1 ]] || fail v20_real_start_game_server_login_not_observed

world=0'''


class TransformRefused(RuntimeError):pass

def transform(text:str)->str:
    if text.count(SIGNAL_BP)!=1:raise TransformRefused(f'SIGNAL_BP_COUNT:{text.count(SIGNAL_BP)}')
    out=text.replace(SIGNAL_BP,SIGNAL_BP_REPL,1)
    if out.count(IMPL_ANCHOR)!=1:raise TransformRefused(f'IMPL_ANCHOR_COUNT:{out.count(IMPL_ANCHOR)}')
    out=out.replace(IMPL_ANCHOR,IMPL_REPL,1)
    if out.count(GDB_TAIL)!=1:raise TransformRefused(f'GDB_TAIL_COUNT:{out.count(GDB_TAIL)}')
    out=out.replace(GDB_TAIL,GDB_TAIL_REPL,1)
    if out.count(SHELL_ANCHOR)!=1:raise TransformRefused(f'SHELL_ANCHOR_COUNT:{out.count(SHELL_ANCHOR)}')
    out=out.replace(SHELL_ANCHOR,SHELL_REPL,1)
    required=(
      'v20-auth-signal-this.txt','WORLDMAP_V20_AUTH_SIGNAL_THIS_UNIQUE_COUNT=',
      "M(0x767440,'StartGameServerLoginImpl')","M(0x6ef1d0,'ConnectExistingImpl')",
      "M(0x6fe480,'OnConnectGameserverImpl')","M(0x6ee130,'GameSessionConnectedImpl')",
      'WORLDMAP_V20_AUTH_QT_THREAD_AFFINITY=PASS','WORLDMAP_V20_AUTH_METHOD27_QMETA_INVOCATION=PASS',
      'WORLDMAP_V20_STATE_ENTRY_FALLBACK=PASS','WORLDMAP_V20_REAL_START_IMPL_COUNT=',
      'WORLDMAP_V20_EVENT_StartGameServerLoginImpl=',
    )
    miss=[x for x in required if x not in out]
    if miss:raise TransformRefused('REQUIRED_MISSING:'+','.join(miss))
    forbidden=('Invalid Monk',"M(0xd47300,'RequestCharacterLogin')","M(0xd47130,'CharacterSelectionConfirmed')",'WORLDMAP_V14_CHARACTER_ATTEMPT=','DOUBLECLICK_CENTER_735_408','FIELD_DERIVED_ROW_CLICK_RETURN','FIELD_DERIVED_ROW_DOUBLECLICK_RETURN','"$XWD" -root','xwd -root','xrandr --output','wmctrl -r')
    surv=[x for x in forbidden if x in out]
    if surv:raise TransformRefused('FORBIDDEN_SURVIVORS:'+','.join(surv))
    if out.count('set scheduler-locking on')!=3 or out.count('set scheduler-locking off')!=3:
        raise TransformRefused(f"SCHEDULER_LOCKING_EXPECTED_3_3:{out.count('set scheduler-locking on')}:{out.count('set scheduler-locking off')}")
    return out

def main()->int:
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    try:out=transform(a.source.read_text())
    except TransformRefused as e:print('WORLDMAP_REAL_IMPL_GAME_LOGIN_V20_REPAIR_REFUSED='+str(e));return 44
    a.output.write_text(out);a.output.chmod(0o700);print('WORLDMAP_REAL_IMPL_GAME_LOGIN_V20_REPAIR=PASS');return 0
if __name__=='__main__':raise SystemExit(main())
