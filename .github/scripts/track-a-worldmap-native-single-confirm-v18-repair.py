#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

GDB_WRONG = ";M(0xcfb374,'ShowCharacterSelection');M(0xd47130,'CharacterSelectionConfirmed');M(0xd47300,'RequestCharacterLogin')"
GDB_CORRECTED = ";M(0xcfb374,'ShowCharacterSelection')"

GDB_TAIL = "S()\nend\ncontinue\n'''\n"
GDB_TAIL_REPLACEMENT = r"""S()
end
continue
python
# V18 post-auth semantic control. The helper sends SIGINT only after the
# legitimate account login has proven transport activity and a persistent UI
# transition. No credential/session payload is read here.
import re,struct,gdb
inf=gdb.selected_inferior(); bias=@BIAS@

def emit18(s):
    gdb.write(s+'\n')

def fail18(reason):
    emit18('WORLDMAP_V18_SEMANTIC_RESULT=FAIL:'+reason)

def rw_ranges18():
    out=[]
    try:
        for line in open(f'/proc/{inf.pid}/maps',errors='replace'):
            p=line.split()
            if len(p)<2 or not (p[1].startswith('rw') and 'p' in p[1]): continue
            lo,hi=(int(x,16) for x in p[0].split('-'))
            if hi>lo: out.append((lo,hi))
    except Exception: pass
    return out

def scan_ptr18(value):
    needle=struct.pack('<Q',value); hits=[]
    for lo,hi in rw_ranges18():
        cur=lo
        while cur<hi:
            try: found=inf.search_memory(cur,hi-cur,needle)
            except Exception: found=None
            if found is None: break
            a=int(found); hits.append(a)
            if len(hits)>16: return hits
            cur=a+8
    return hits

def resolve18(mangled,demangled):
    for expr in (f'(void*){mangled}',f"(void*)&'{demangled}'"):
        try:
            v=int(gdb.parse_and_eval(expr))
            if v: return v
        except Exception: pass
    try:
        out=gdb.execute('info address '+mangled,to_string=True)
        m=re.search(r'0x[0-9a-fA-F]+',out)
        if m: return int(m.group(0),16)
    except Exception: pass
    return 0

def selected_count18(obj):
    b=mem(obj+0x140,16)
    if b is None:return -1
    a,z=struct.unpack('<QQ',b)
    if z<a:return -1
    span=z-a
    if span%0x70:return -1
    return span//0x70

try:
    hits=scan_ptr18(bias+0x308ed68)
    emit18('WORLDMAP_V18_POSTAUTH_CHARSEL_INSTANCE_COUNT='+str(len(hits)))
    if len(hits)!=1:
        fail18('charsel_instance_count')
    else:
        charsel=hits[0]
        static_call=bias+0xd46550
        prologue=mem(static_call,16)
        if prologue is None or prologue.hex()!='41574156415541544989cc55534889fb':
            fail18('qt_static_metacall_instruction_mismatch')
        else:
            emit18('WORLDMAP_V18_RUNTIME_ADDRESS_PROVEN=PASS')
            cb=mem(charsel+0x108,8); pb=mem(charsel+0x100,8)
            if cb is None or pb is None:
                fail18('character_model_memory_unreadable')
            else:
                character_count=struct.unpack('<q',cb)[0]
                first_model=struct.unpack('<Q',pb)[0]
                emit18('WORLDMAP_V18_NATIVE_CHARACTER_LIST_COUNT='+str(character_count))
                if character_count!=1 or first_model==0 or mem(first_model,8) is None:
                    fail18('single_native_character_not_proven')
                else:
                    emit18('WORLDMAP_V18_NATIVE_CHARACTER_LIST_DISCOVERY=PASS')
                    emit18('WORLDMAP_V18_NATIVE_SELECTION_INDEX=0')
                    # Invoke only on the object's owning Qt thread.
                    mains=[t for t in inf.threads() if len(t.ptid)>=2 and t.ptid[1]==inf.pid]
                    if len(mains)!=1:
                        fail18('main_lwp_not_unique')
                    else:
                        mains[0].switch()
                        gdb.execute('set scheduler-locking on',to_string=True)
                        qobj_thread=resolve18('_ZNK7QObject6threadEv','QObject::thread() const')
                        qthread_current=resolve18('_ZN7QThread13currentThreadEv','QThread::currentThread()')
                        if not qobj_thread or not qthread_current:
                            fail18('qt_thread_symbols_unresolved')
                        else:
                            try:
                                owner=int(gdb.parse_and_eval(f'((void*(*)(void*))0x{qobj_thread:x})((void*)0x{charsel:x})'))
                                current=int(gdb.parse_and_eval(f'((void*(*)())0x{qthread_current:x})()'))
                            except Exception:
                                owner=0;current=-1
                            if owner==0 or owner!=current:
                                fail18('qt_thread_affinity_mismatch')
                            else:
                                emit18('WORLDMAP_V18_QT_THREAD_AFFINITY=PASS')
                                before=selected_count18(charsel)
                                emit18('WORLDMAP_V18_SELECTED_LOGIN_DATA_BEFORE='+str(before))
                                # Exact-SHA static proof establishes that method 11 passes
                                # argv[1] directly as QList<int> const&, and while RSI->R14
                                # aliases that input, the implementation observes only +8
                                # data pointer and +16 size; the header/refcount is untouched.
                                # This is therefore a transient non-owning const selection view,
                                # not a fabricated persistent Qt object or character object.
                                idxbuf=listview=argv=0
                                ok=False
                                try:
                                    idxbuf=int(gdb.parse_and_eval('((void*(*)(unsigned long))malloc)(8)'))
                                    listview=int(gdb.parse_and_eval('((void*(*)(unsigned long))malloc)(24)'))
                                    argv=int(gdb.parse_and_eval('((void*(*)(unsigned long))malloc)(16)'))
                                    if idxbuf and listview and argv:
                                        inf.write_memory(idxbuf,struct.pack('<iI',0,0))
                                        inf.write_memory(listview,struct.pack('<QQq',0,idxbuf,1))
                                        inf.write_memory(argv,struct.pack('<QQ',0,listview))
                                        emit18('WORLDMAP_V18_CONST_SELECTION_VIEW=PASS')
                                        gdb.parse_and_eval(
                                            f'((void(*)(void*,int,int,void**))0x{static_call:x})'
                                            f'((void*)0x{charsel:x},0,11,(void**)0x{argv:x})'
                                        )
                                        ok=True
                                except Exception:
                                    ok=False
                                after=selected_count18(charsel) if ok else -1
                                emit18('WORLDMAP_V18_SELECTED_LOGIN_DATA_AFTER='+str(after))
                                for p in (argv,listview,idxbuf):
                                    if p:
                                        try:gdb.parse_and_eval(f'((void(*)(void*))free)((void*)0x{p:x})')
                                        except Exception:pass
                                if not ok:
                                    fail18('native_character_confirmation_qmeta_call_failed')
                                elif after<1:
                                    fail18('native_character_confirmation_did_not_build_login_data')
                                else:
                                    emit18('WORLDMAP_V18_NATIVE_CHARACTER_CONFIRMATION_QMETA=PASS')
                                    emit18('WORLDMAP_V18_SEMANTIC_RESULT=PASS')
except Exception:
    fail18('unexpected_semantic_exception')
end
continue
'''
"""

CHAR_START = "# V14: account Login is already proven by local SOCKS activity plus a persistent\n"
CHAR_END = '[[ "$world" == 1 ]] || fail structural_world_entry_not_observed_after_native_character_request\n'

CHAR_REPLACEMENT = r'''# V18: account login is proven before this point. Character control is native:
# one current-session character -> index 0 -> onCharacterSelectionConfirmed.
echo 'WORLDMAP_V18_CHARACTER_CONTROL=NATIVE_QMETA_SINGLE_RUNTIME_CHARACTER'
kill -INT "$GDB_PID" 2>/dev/null || fail v18_gdb_semantic_interrupt_failed
SEMANTIC=0
for _ in $(seq 1 160); do
  sleep .25
  if grep -Fq 'WORLDMAP_V18_SEMANTIC_RESULT=PASS' "$GOUT" 2>/dev/null; then SEMANTIC=1; break; fi
  if grep -Fq 'WORLDMAP_V18_SEMANTIC_RESULT=FAIL:' "$GOUT" 2>/dev/null; then break; fi
  kill -0 "$GDB_PID" 2>/dev/null || break
done
grep -E '^WORLDMAP_V18_(POSTAUTH_CHARSEL_INSTANCE_COUNT|RUNTIME_ADDRESS_PROVEN|NATIVE_CHARACTER_LIST_COUNT|NATIVE_CHARACTER_LIST_DISCOVERY|NATIVE_SELECTION_INDEX|QT_THREAD_AFFINITY|SELECTED_LOGIN_DATA_BEFORE|CONST_SELECTION_VIEW|SELECTED_LOGIN_DATA_AFTER|NATIVE_CHARACTER_CONFIRMATION_QMETA|SEMANTIC_RESULT)=' "$GOUT" 2>/dev/null | tail -30 || true
[[ "$SEMANTIC" == 1 ]] || fail v18_native_single_character_confirmation_failed

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


class TransformRefused(RuntimeError):
    pass


def transform(text: str) -> str:
    if text.count(GDB_WRONG) != 1:
        raise TransformRefused(f"GDB_WRONG_COUNT:{text.count(GDB_WRONG)}")
    out=text.replace(GDB_WRONG,GDB_CORRECTED,1)
    if out.count(GDB_TAIL) != 1:
        raise TransformRefused(f"GDB_TAIL_COUNT:{out.count(GDB_TAIL)}")
    out=out.replace(GDB_TAIL,GDB_TAIL_REPLACEMENT,1)
    if out.count(CHAR_START) != 1:
        raise TransformRefused(f"CHAR_START_COUNT:{out.count(CHAR_START)}")
    start=out.index(CHAR_START)
    end=out.find(CHAR_END,start)
    if end<0:raise TransformRefused('CHAR_END_MISSING')
    end+=len(CHAR_END)
    out=out[:start]+CHAR_REPLACEMENT+out[end:]
    required=(
        'WORLDMAP_BASELINE_LOGIN_TRANSPORT_ACTIVITY=PASS',
        'WORLDMAP_BASELINE_POST_LOGIN_UI_TRANSITION=PASS',
        'WORLDMAP_V18_POSTAUTH_CHARSEL_INSTANCE_COUNT=',
        'WORLDMAP_V18_RUNTIME_ADDRESS_PROVEN=PASS',
        'WORLDMAP_V18_NATIVE_CHARACTER_LIST_COUNT=',
        'WORLDMAP_V18_NATIVE_CHARACTER_LIST_DISCOVERY=PASS',
        'WORLDMAP_V18_NATIVE_SELECTION_INDEX=0',
        'WORLDMAP_V18_QT_THREAD_AFFINITY=PASS',
        'WORLDMAP_V18_CONST_SELECTION_VIEW=PASS',
        'WORLDMAP_V18_NATIVE_CHARACTER_CONFIRMATION_QMETA=PASS',
        'WORLDMAP_V18_SEMANTIC_RESULT=PASS',
        'WORLDMAP_BASELINE_STRUCTURAL_IN_GAME=PASS',
        '0xd46550','0x308ed68','0x70',
    )
    missing=[x for x in required if x not in out]
    if missing:raise TransformRefused('REQUIRED_MISSING:'+','.join(missing))
    forbidden=(
        "M(0xd47130,'CharacterSelectionConfirmed')",
        "M(0xd47300,'RequestCharacterLogin')",
        'WORLDMAP_V14_CHARACTER_ATTEMPT=',
        'DOUBLECLICK_CENTER_735_408',
        'FIELD_DERIVED_ROW_CLICK_RETURN',
        'FIELD_DERIVED_ROW_DOUBLECLICK_RETURN',
        'Invalid Monk',
        '"$XWD" -root','xwd -root','xrandr --output','wmctrl -r',
    )
    survivors=[x for x in forbidden if x in out]
    if survivors:raise TransformRefused('FORBIDDEN_SURVIVORS:'+','.join(survivors))
    return out


def main() -> int:
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    try:out=transform(a.source.read_text(encoding='utf-8'))
    except TransformRefused as exc:
        print(f'WORLDMAP_NATIVE_SINGLE_CONFIRM_V18_REPAIR_REFUSED={exc}');return 44
    a.output.write_text(out,encoding='utf-8');a.output.chmod(0o700)
    print('WORLDMAP_NATIVE_SINGLE_CONFIRM_V18_REPAIR=PASS');return 0

if __name__=='__main__':raise SystemExit(main())
