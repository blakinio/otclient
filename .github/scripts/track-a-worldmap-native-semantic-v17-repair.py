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
# V17 post-auth native semantic character control. The first `continue` above
# returns only when the helper deliberately sends SIGINT after legitimate
# account authentication has produced transport activity and a persistent UI
# transition. No credential/session payload is inspected here.
import os,re,struct,gdb
inf=gdb.selected_inferior(); bias=@BIAS@

def v17_emit(s):
    gdb.write(s+'\n')

def v17_fail(reason):
    v17_emit('WORLDMAP_V17_SEMANTIC_RESULT=FAIL:'+reason)

def v17_rw_ranges():
    out=[]
    try:
        for line in open(f'/proc/{inf.pid}/maps',errors='replace'):
            p=line.split()
            if len(p)<2 or not (p[1].startswith('rw') and 'p' in p[1]): continue
            lo,hi=(int(x,16) for x in p[0].split('-'))
            if hi>lo: out.append((lo,hi))
    except Exception: pass
    return out

def v17_scan_ptr(value):
    needle=struct.pack('<Q',value); hits=[]
    for lo,hi in v17_rw_ranges():
        cur=lo
        while cur<hi:
            try: found=inf.search_memory(cur,hi-cur,needle)
            except Exception: found=None
            if found is None: break
            a=int(found); hits.append(a)
            if len(hits)>16: return hits
            cur=a+8
    return hits

semantic_ok=False
try:
    # Exact current-session controller provenance by relocated primary vptr.
    charsel_hits=v17_scan_ptr(bias+0x308ed68)
    v17_emit('WORLDMAP_V17_POSTAUTH_CHARSEL_INSTANCE_COUNT='+str(len(charsel_hits)))
    if len(charsel_hits)!=1:
        v17_fail('charsel_instance_count')
    else:
        charsel=charsel_hits[0]
        # Runtime-address and instruction-byte proof for qt_static_metacall.
        static_call=bias+0xd46550
        prologue=mem(static_call,16)
        if prologue is None or prologue.hex()!='41574156415541544989cc55534889fb':
            v17_fail('qt_static_metacall_instruction_mismatch')
        else:
            v17_emit('WORLDMAP_V17_RUNTIME_ADDRESS_PROVEN=PASS')
            # Native character-list cardinality and already-live selected
            # TCharacterLoginData vector. No names or payload fields are read.
            cb=mem(charsel+0x108,8); sb=mem(charsel+0x140,16)
            if cb is None or sb is None:
                v17_fail('character_model_memory_unreadable')
            else:
                character_count=struct.unpack('<q',cb)[0]
                selected_start,selected_end=struct.unpack('<QQ',sb)
                span=selected_end-selected_start if selected_end>=selected_start else -1
                selected_count=(span//0x70) if span>=0 and span%0x70==0 else -1
                v17_emit('WORLDMAP_V17_NATIVE_CHARACTER_LIST_COUNT='+str(character_count))
                v17_emit('WORLDMAP_V17_NATIVE_SELECTED_LOGIN_DATA_COUNT='+str(selected_count))
                if not (1<=character_count<=100):
                    v17_fail('native_character_list_cardinality_invalid')
                elif selected_count!=1 or selected_start==0 or mem(selected_start,0x70) is None:
                    v17_fail('single_native_selected_login_data_not_proven')
                else:
                    v17_emit('WORLDMAP_V17_NATIVE_CHARACTER_LIST_DISCOVERY=PASS')
                    v17_emit('WORLDMAP_V17_CHARACTER_SELECTION_RULE=CURRENT_RUNTIME_NATIVE_SELECTION')
                    # Qt thread-affinity hard gate. Execute calls from the main
                    # LWP and require QObject::thread(this)==QThread::currentThread().
                    main_threads=[t for t in inf.threads() if len(t.ptid)>=2 and t.ptid[1]==inf.pid]
                    if len(main_threads)!=1:
                        v17_fail('main_lwp_not_unique')
                    else:
                        main_threads[0].switch()
                        gdb.execute('set scheduler-locking on',to_string=True)
                        try:
                            qobj_thread=int(gdb.parse_and_eval('(void*)_ZNK7QObject6threadEv'))
                            owner_thread=int(gdb.parse_and_eval(f'((void*(*)(void*))0x{qobj_thread:x})((void*)0x{charsel:x})'))
                            current_thread=int(gdb.parse_and_eval(f'((void*(*)())0x{bias+0x4de2a0:x})()'))
                        except Exception:
                            owner_thread=0; current_thread=-1
                        if owner_thread==0 or owner_thread!=current_thread:
                            v17_fail('qt_thread_affinity_mismatch')
                        else:
                            v17_emit('WORLDMAP_V17_QT_THREAD_AFFINITY=PASS')
                            # argv is a trivial two-pointer QMeta call frame.
                            # argv[1] points at the existing client-owned
                            # TCharacterLoginData; the object itself is never copied.
                            try:
                                argv=int(gdb.parse_and_eval('((void*(*)(unsigned long))malloc)(16)'))
                            except Exception:
                                argv=0
                            if argv==0:
                                v17_fail('qmeta_argv_allocation_failed')
                            else:
                                try:
                                    inf.write_memory(argv,struct.pack('<QQ',0,selected_start))
                                    gdb.parse_and_eval(
                                        f'((void(*)(void*,int,int,void**))0x{static_call:x})'
                                        f'((void*)0x{charsel:x},0,0,(void**)0x{argv:x})'
                                    )
                                    semantic_ok=True
                                except Exception:
                                    semantic_ok=False
                                try: gdb.parse_and_eval(f'((void(*)(void*))free)((void*)0x{argv:x})')
                                except Exception: pass
                                if semantic_ok:
                                    v17_emit('WORLDMAP_V17_NATIVE_CHARACTER_QMETA_INVOCATION=PASS')
                                    v17_emit('WORLDMAP_V17_SEMANTIC_RESULT=PASS')
                                else:
                                    v17_fail('native_character_qmeta_invocation_failed')
except Exception:
    v17_fail('unexpected_semantic_exception')
end
continue
'''
"""

CHAR_START = "# V14: account Login is already proven by local SOCKS activity plus a persistent\n"
CHAR_END = '[[ "$world" == 1 ]] || fail structural_world_entry_not_observed_after_native_character_request\n'

CHAR_REPLACEMENT = r'''# V17: account Login is already proven by transport plus persistent post-login
# UI transition. Character control is now exclusively native/QMeta; no keyboard,
# mouse, OCR, row order or imported character identity is used.
echo 'WORLDMAP_V17_CHARACTER_CONTROL=NATIVE_QMETA_CURRENT_RUNTIME_SELECTION'
kill -INT "$GDB_PID" 2>/dev/null || fail v17_gdb_semantic_interrupt_failed
SEMANTIC=0
for _ in $(seq 1 160); do
  sleep .25
  if grep -Fq 'WORLDMAP_V17_SEMANTIC_RESULT=PASS' "$GOUT" 2>/dev/null; then SEMANTIC=1; break; fi
  if grep -Fq 'WORLDMAP_V17_SEMANTIC_RESULT=FAIL:' "$GOUT" 2>/dev/null; then break; fi
  kill -0 "$GDB_PID" 2>/dev/null || break
done
# Surface only explicitly sanitized v17 control markers; never dump GDB output.
grep -E '^WORLDMAP_V17_(POSTAUTH_CHARSEL_INSTANCE_COUNT|RUNTIME_ADDRESS_PROVEN|NATIVE_CHARACTER_LIST_COUNT|NATIVE_SELECTED_LOGIN_DATA_COUNT|NATIVE_CHARACTER_LIST_DISCOVERY|CHARACTER_SELECTION_RULE|QT_THREAD_AFFINITY|NATIVE_CHARACTER_QMETA_INVOCATION|SEMANTIC_RESULT)=' "$GOUT" 2>/dev/null | tail -20 || true
[[ "$SEMANTIC" == 1 ]] || fail v17_native_semantic_character_control_failed

world=0
for _ in $(seq 1 240); do
  sleep .5
  if grep -Fq $'\tFullMap' "$EVENTS" 2>/dev/null && [[ "$(wc -l <"$STRIPS")" -ge 10 ]]; then
    world=1
    break
  fi
done
[[ "$world" == 1 ]] || fail structural_world_entry_not_observed_after_v17_native_character_qmeta
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
    if end<0:
        raise TransformRefused('CHAR_END_MISSING')
    end+=len(CHAR_END)
    out=out[:start]+CHAR_REPLACEMENT+out[end:]

    required=(
        'WORLDMAP_BASELINE_LOGIN_TRANSPORT_ACTIVITY=PASS',
        'WORLDMAP_BASELINE_POST_LOGIN_UI_TRANSITION=PASS',
        'WORLDMAP_V17_POSTAUTH_CHARSEL_INSTANCE_COUNT=',
        'WORLDMAP_V17_RUNTIME_ADDRESS_PROVEN=PASS',
        'WORLDMAP_V17_NATIVE_CHARACTER_LIST_COUNT=',
        'WORLDMAP_V17_NATIVE_SELECTED_LOGIN_DATA_COUNT=',
        'WORLDMAP_V17_NATIVE_CHARACTER_LIST_DISCOVERY=PASS',
        'WORLDMAP_V17_CHARACTER_SELECTION_RULE=CURRENT_RUNTIME_NATIVE_SELECTION',
        'WORLDMAP_V17_QT_THREAD_AFFINITY=PASS',
        'WORLDMAP_V17_NATIVE_CHARACTER_QMETA_INVOCATION=PASS',
        'WORLDMAP_V17_SEMANTIC_RESULT=PASS',
        'WORLDMAP_BASELINE_STRUCTURAL_IN_GAME=PASS',
        '0xd46550','0x308ed68','0x4de2a0','0x70',
    )
    missing=[x for x in required if x not in out]
    if missing:
        raise TransformRefused('REQUIRED_MISSING:'+','.join(missing))
    forbidden=(
        "M(0xd47130,'CharacterSelectionConfirmed')",
        "M(0xd47300,'RequestCharacterLogin')",
        'WORLDMAP_V14_CHARACTER_ATTEMPT=',
        'native_character_request_not_observed_after_bounded_v14_candidates',
        'xdo key --window "$UI_WIN" --clearmodifiers Return\ncheck_activation',
        'DOUBLECLICK_CENTER_735_408',
        'FIELD_DERIVED_ROW_CLICK_RETURN',
        'FIELD_DERIVED_ROW_DOUBLECLICK_RETURN',
        'Invalid Monk',
        '"$XWD" -root',
        'xwd -root',
        'xrandr --output',
        'wmctrl -r',
    )
    survivors=[x for x in forbidden if x in out]
    if survivors:
        raise TransformRefused('FORBIDDEN_SURVIVORS:'+','.join(survivors))
    return out


def main() -> int:
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    try: out=transform(a.source.read_text(encoding='utf-8'))
    except TransformRefused as exc:
        print(f'WORLDMAP_NATIVE_SEMANTIC_V17_REPAIR_REFUSED={exc}');return 44
    a.output.write_text(out,encoding='utf-8');a.output.chmod(0o700)
    print('WORLDMAP_NATIVE_SEMANTIC_V17_REPAIR=PASS');return 0

if __name__=='__main__': raise SystemExit(main())
