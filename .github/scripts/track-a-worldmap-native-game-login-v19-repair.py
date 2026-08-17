#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

BREAKPOINT_ANCHOR = "M(0xcfb374,'ShowCharacterSelection')"
BREAKPOINT_REPLACEMENT = (
    "M(0xcfb374,'ShowCharacterSelection');"
    "M(0x856880,'RequestCharacterLoginSignalActivate');"
    "M(0xcfb2e7,'RequestCharacterGameserverLogin');"
    "M(0xcfb122,'StartGameServerLogin');"
    "M(0xd06660,'ConnectExistingCredentials');"
    "M(0xd06810,'OnConnectGameserver');"
    "M(0xd067b0,'AbortGameserverConnect');"
    "M(0xd066e0,'GameSessionConnected');"
    "M(0xd066c8,'GameSessionLoginSuccessful');"
    "M(0xd064d8,'GameSessionLoginError');"
    "M(0xd064c8,'GameSessionDisconnected')"
)

SCHED_ANCHOR = """emit18('WORLDMAP_V18_NATIVE_CHARACTER_CONFIRMATION_QMETA=PASS')
                                    emit18('WORLDMAP_V18_SEMANTIC_RESULT=PASS')"""
SCHED_REPLACEMENT = """gdb.execute('set scheduler-locking off',to_string=True)
                                    emit18('WORLDMAP_V19_SCHEDULER_LOCKING_RESTORED=PASS')
                                    emit18('WORLDMAP_V18_NATIVE_CHARACTER_CONFIRMATION_QMETA=PASS')
                                    emit18('WORLDMAP_V18_SEMANTIC_RESULT=PASS')"""

GDB_FINAL = "end\ncontinue\n'''\n"
GDB_FINAL_REPLACEMENT = r"""end
continue
python
# V19 conditional original-state-machine continuation. This block runs only
# if the helper sends a second SIGINT after proving that the native character
# signal fired but its connected AUTH transition did not.
import re,struct,gdb
inf=gdb.selected_inferior(); bias=@BIAS@; ev19=r'@EV@'

def emit19(s):
    gdb.write(s+'\n')

def count19(name):
    try:
        return sum(1 for line in open(ev19,errors='replace') if line.rstrip().endswith('\t'+name))
    except Exception:return 0

def ranges19():
    out=[]
    try:
        for line in open(f'/proc/{inf.pid}/maps',errors='replace'):
            p=line.split()
            if len(p)<2 or not (p[1].startswith('rw') and 'p' in p[1]):continue
            lo,hi=(int(x,16) for x in p[0].split('-'))
            if hi>lo:out.append((lo,hi))
    except Exception:pass
    return out

def scan19(value):
    needle=struct.pack('<Q',value);hits=[]
    for lo,hi in ranges19():
        cur=lo
        while cur<hi:
            try:found=inf.search_memory(cur,hi-cur,needle)
            except Exception:found=None
            if found is None:break
            a=int(found);hits.append(a)
            if len(hits)>16:return hits
            cur=a+8
    return hits

def resolve19(mangled,demangled):
    for expr in (f'(void*){mangled}',f"(void*)&'{demangled}'"):
        try:
            v=int(gdb.parse_and_eval(expr))
            if v:return v
        except Exception:pass
    return 0

sig=count19('RequestCharacterLoginSignalActivate')
req=count19('RequestCharacterGameserverLogin')
emit19('WORLDMAP_V19_FALLBACK_PRE_SIGNAL_COUNT='+str(sig))
emit19('WORLDMAP_V19_FALLBACK_PRE_REQUEST_GAMESERVER_COUNT='+str(req))
if sig<1 or req>0:
    emit19('WORLDMAP_V19_AUTH_FALLBACK=REFUSED_PRECONDITION')
else:
    hits=scan19(bias+0x307f1b0)
    emit19('WORLDMAP_V19_POSTAUTH_AUTH_INSTANCE_COUNT='+str(len(hits)))
    if len(hits)!=1:
        emit19('WORLDMAP_V19_AUTH_FALLBACK=FAIL:auth_instance_count')
    else:
        auth=hits[0]; static_call=bias+0xcfabb0
        p=mem(static_call,16); c=mem(bias+0xcfb2e7,12)
        if p is None or p.hex()!='85f6752c83fa320f87f2000000415448' or c is None or c.hex()!='31c9ba05000000e981faffff':
            emit19('WORLDMAP_V19_AUTH_FALLBACK=FAIL:runtime_instruction_fence')
        else:
            emit19('WORLDMAP_V19_AUTH_RUNTIME_ADDRESS_PROVEN=PASS')
            mains=[t for t in inf.threads() if len(t.ptid)>=2 and t.ptid[1]==inf.pid]
            if len(mains)!=1:
                emit19('WORLDMAP_V19_AUTH_FALLBACK=FAIL:main_lwp_not_unique')
            else:
                mains[0].switch();gdb.execute('set scheduler-locking on',to_string=True)
                qt=resolve19('_ZNK7QObject6threadEv','QObject::thread() const')
                qc=resolve19('_ZN7QThread13currentThreadEv','QThread::currentThread()')
                try:
                    owner=int(gdb.parse_and_eval(f'((void*(*)(void*))0x{qt:x})((void*)0x{auth:x})')) if qt else 0
                    current=int(gdb.parse_and_eval(f'((void*(*)())0x{qc:x})()')) if qc else -1
                except Exception:
                    owner=0;current=-1
                if owner==0 or owner!=current:
                    gdb.execute('set scheduler-locking off',to_string=True)
                    emit19('WORLDMAP_V19_AUTH_FALLBACK=FAIL:qt_thread_affinity')
                else:
                    emit19('WORLDMAP_V19_AUTH_QT_THREAD_AFFINITY=PASS')
                    ok=False
                    try:
                        gdb.parse_and_eval(
                            f'((void(*)(void*,int,int,void**))0x{static_call:x})'
                            f'((void*)0x{auth:x},0,5,(void**)0)'
                        )
                        ok=True
                    except Exception:ok=False
                    gdb.execute('set scheduler-locking off',to_string=True)
                    if ok:
                        emit19('WORLDMAP_V19_AUTH_METHOD5_QMETA_INVOCATION=PASS')
                        emit19('WORLDMAP_V19_AUTH_FALLBACK=PASS')
                    else:
                        emit19('WORLDMAP_V19_AUTH_FALLBACK=FAIL:qmeta_invocation')
end
continue
'''
"""

SHELL_ANCHOR = r'''[[ "$SEMANTIC" == 1 ]] || fail v18_native_single_character_confirmation_failed

world=0
for _ in $(seq 1 240); do
  sleep .5
  if grep -Fq $'\tFullMap' "$EVENTS" 2>/dev/null && [[ "$(wc -l <"$STRIPS")" -ge 10 ]]; then
    world=1
    break
  fi
done
[[ "$world" == 1 ]] || fail structural_world_entry_not_observed_after_v18_native_confirmation
'''

SHELL_REPLACEMENT = r'''[[ "$SEMANTIC" == 1 ]] || fail v18_native_single_character_confirmation_failed
grep -Fq 'WORLDMAP_V19_SCHEDULER_LOCKING_RESTORED=PASS' "$GOUT" || fail v19_scheduler_locking_not_restored

event_count_v19() {
  local name="$1"
  awk -F '\t' -v n="$name" '$2==n{c++} END{print c+0}' "$EVENTS" 2>/dev/null || echo 0
}

# Give the normal synchronous/asynchronous native signal chain a bounded chance
# with all inferior threads restored before considering any fallback.
sleep 3
SIG_COUNT="$(event_count_v19 RequestCharacterLoginSignalActivate)"
REQ_COUNT="$(event_count_v19 RequestCharacterGameserverLogin)"
echo "WORLDMAP_V19_REQUEST_CHARACTER_SIGNAL_COUNT=$SIG_COUNT"
echo "WORLDMAP_V19_REQUEST_CHARACTER_GAMESERVER_LOGIN_COUNT=$REQ_COUNT"
[[ "$SIG_COUNT" -ge 1 ]] || fail v19_native_character_signal_not_observed

if [[ "$REQ_COUNT" -eq 0 ]]; then
  kill -INT "$GDB_PID" 2>/dev/null || fail v19_auth_fallback_interrupt_failed
  FALLBACK_DONE=0
  for _ in $(seq 1 160); do
    sleep .25
    if grep -Fq 'WORLDMAP_V19_AUTH_FALLBACK=PASS' "$GOUT" 2>/dev/null; then FALLBACK_DONE=1;break;fi
    if grep -Fq 'WORLDMAP_V19_AUTH_FALLBACK=FAIL:' "$GOUT" 2>/dev/null || grep -Fq 'WORLDMAP_V19_AUTH_FALLBACK=REFUSED_PRECONDITION' "$GOUT" 2>/dev/null; then break;fi
    kill -0 "$GDB_PID" 2>/dev/null || break
  done
  grep -E '^WORLDMAP_V19_(FALLBACK_PRE_SIGNAL_COUNT|FALLBACK_PRE_REQUEST_GAMESERVER_COUNT|POSTAUTH_AUTH_INSTANCE_COUNT|AUTH_RUNTIME_ADDRESS_PROVEN|AUTH_QT_THREAD_AFFINITY|AUTH_METHOD5_QMETA_INVOCATION|AUTH_FALLBACK)=' "$GOUT" 2>/dev/null | tail -20 || true
  [[ "$FALLBACK_DONE" == 1 ]] || fail v19_auth_fallback_failed
  sleep 3
fi

for name in RequestCharacterLoginSignalActivate RequestCharacterGameserverLogin StartGameServerLogin ConnectExistingCredentials OnConnectGameserver AbortGameserverConnect GameSessionConnected GameSessionLoginSuccessful GameSessionLoginError GameSessionDisconnected FullMap; do
  c="$(event_count_v19 "$name")"
  echo "WORLDMAP_V19_EVENT_${name}=$c"
done

[[ "$(event_count_v19 RequestCharacterGameserverLogin)" -ge 1 ]] || fail v19_request_character_gameserver_login_not_observed
[[ "$(event_count_v19 AbortGameserverConnect)" -eq 0 ]] || fail v19_explicit_gameserver_connect_abort
[[ "$(event_count_v19 GameSessionLoginError)" -eq 0 ]] || fail v19_explicit_game_session_login_error

world=0
for _ in $(seq 1 240); do
  sleep .5
  if grep -Fq $'\tFullMap' "$EVENTS" 2>/dev/null && [[ "$(wc -l <"$STRIPS")" -ge 10 ]]; then
    world=1
    break
  fi
done
[[ "$world" == 1 ]] || fail structural_world_entry_not_observed_after_v19_game_login
'''


class TransformRefused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(BREAKPOINT_ANCHOR) != 1:
        raise TransformRefused(f"BREAKPOINT_ANCHOR_COUNT:{text.count(BREAKPOINT_ANCHOR)}")
    out=text.replace(BREAKPOINT_ANCHOR,BREAKPOINT_REPLACEMENT,1)
    if out.count(SCHED_ANCHOR) != 1:
        raise TransformRefused(f"SCHED_ANCHOR_COUNT:{out.count(SCHED_ANCHOR)}")
    out=out.replace(SCHED_ANCHOR,SCHED_REPLACEMENT,1)
    if out.count(GDB_FINAL) != 1:
        raise TransformRefused(f"GDB_FINAL_COUNT:{out.count(GDB_FINAL)}")
    out=out.replace(GDB_FINAL,GDB_FINAL_REPLACEMENT,1)
    if out.count(SHELL_ANCHOR) != 1:
        raise TransformRefused(f"SHELL_ANCHOR_COUNT:{out.count(SHELL_ANCHOR)}")
    out=out.replace(SHELL_ANCHOR,SHELL_REPLACEMENT,1)

    required=(
        'WORLDMAP_V19_SCHEDULER_LOCKING_RESTORED=PASS',
        "M(0x856880,'RequestCharacterLoginSignalActivate')",
        "M(0xcfb2e7,'RequestCharacterGameserverLogin')",
        "M(0xcfb122,'StartGameServerLogin')",
        "M(0xd06660,'ConnectExistingCredentials')",
        "M(0xd066e0,'GameSessionConnected')",
        "M(0xd066c8,'GameSessionLoginSuccessful')",
        'WORLDMAP_V19_REQUEST_CHARACTER_SIGNAL_COUNT=',
        'WORLDMAP_V19_AUTH_RUNTIME_ADDRESS_PROVEN=PASS',
        'WORLDMAP_V19_AUTH_QT_THREAD_AFFINITY=PASS',
        'WORLDMAP_V19_AUTH_METHOD5_QMETA_INVOCATION=PASS',
        'WORLDMAP_V19_AUTH_FALLBACK=PASS',
        '85f6752c83fa320f87f2000000415448',
        '31c9ba05000000e981faffff',
        'structural_world_entry_not_observed_after_v19_game_login',
    )
    missing=[x for x in required if x not in out]
    if missing:raise TransformRefused('REQUIRED_MISSING:'+','.join(missing))
    forbidden=(
        'set scheduler-locking on\',
        'Invalid Monk',
        "M(0xd47300,'RequestCharacterLogin')",
        "M(0xd47130,'CharacterSelectionConfirmed')",
        'WORLDMAP_V14_CHARACTER_ATTEMPT=',
        'DOUBLECLICK_CENTER_735_408',
        'FIELD_DERIVED_ROW_CLICK_RETURN',
        'FIELD_DERIVED_ROW_DOUBLECLICK_RETURN',
        '"$XWD" -root','xwd -root','xrandr --output','wmctrl -r',
    )
    # Scheduler-locking is allowed only when paired with an explicit off in the
    # same semantic/fallback block; do not use the crude string check for it.
    survivors=[x for x in forbidden[1:] if x in out]
    if survivors:raise TransformRefused('FORBIDDEN_SURVIVORS:'+','.join(survivors))
    if out.count("set scheduler-locking on") != out.count("set scheduler-locking off"):
        raise TransformRefused(f"SCHEDULER_LOCKING_UNBALANCED:{out.count('set scheduler-locking on')}:{out.count('set scheduler-locking off')}")
    return out


def main() -> int:
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    try:out=transform(a.source.read_text(encoding='utf-8'))
    except TransformRefused as exc:
        print(f'WORLDMAP_NATIVE_GAME_LOGIN_V19_REPAIR_REFUSED={exc}');return 44
    a.output.write_text(out,encoding='utf-8');a.output.chmod(0o700)
    print('WORLDMAP_NATIVE_GAME_LOGIN_V19_REPAIR=PASS');return 0

if __name__=='__main__':raise SystemExit(main())
