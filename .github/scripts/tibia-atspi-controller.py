#!/usr/bin/env python3
"""Control official Tibia UI through AT-SPI semantics; never OCR.

Only fixed allow-listed UI markers/counters are printed. Secrets and account /
character strings are never emitted.
"""
from __future__ import annotations
import os, subprocess, sys, time
import pyatspi


def children(o):
    try: return [o.getChildAtIndex(i) for i in range(o.childCount)]
    except Exception: return []


def walk(root, limit=5000):
    stack=[root]; seen=0
    while stack and seen < limit:
        o=stack.pop(); seen+=1; yield o; stack.extend(reversed(children(o)))


def name(o):
    try: return (o.name or '').strip()
    except Exception: return ''


def role(o):
    try: return (o.getRoleName() or '').lower()
    except Exception: return ''


def actions(o):
    try:
        a=o.queryAction(); return a if a.nActions else None
    except Exception: return None


def app_now():
    d=pyatspi.Registry.getDesktop(0)
    for i in range(d.childCount):
        try:
            a=d.getChildAtIndex(i)
            if 'tibia' in name(a).lower(): return a
        except Exception: pass
    return None


def wait_app(timeout=30):
    end=time.time()+timeout
    while time.time()<end:
        a=app_now()
        if a is not None: return a
        time.sleep(.5)
    raise RuntimeError('Tibia AT-SPI application not found')


def edits(app):
    out=[]
    for o in walk(app):
        try: o.queryEditableText(); out.append(o)
        except Exception: pass
    def key(o):
        try:
            e=o.queryComponent().getExtents(pyatspi.DESKTOP_COORDS); return (e.y,e.x)
        except Exception: return (10**9,10**9)
    out.sort(key=key); return out


def flags(app):
    vals={'account':False,'login':False,'select':False,'character':False}; ed=act=0
    for o in walk(app):
        n=name(o).lower()
        if n in {'account','account login'}: vals['account']=True
        if n=='login': vals['login']=True
        if n=='select character': vals['select']=True
        if n=='character': vals['character']=True
        try: o.queryEditableText(); ed+=1
        except Exception: pass
        if actions(o): act+=1
    print(f'ATSPI_EDITABLE_COUNT={ed}',flush=True)
    print(f'ATSPI_ACTIONABLE_COUNT={act}',flush=True)
    for k,v in vals.items(): print(f'ATSPI_{k.upper()}_MARKER={str(v).lower()}',flush=True)
    vals['editable']=ed; return vals


def invoke(app, allowed):
    allowed={x.lower() for x in allowed}
    for o in walk(app):
        if name(o).lower() not in allowed: continue
        a=actions(o)
        if a:
            a.doAction(0); print('ATSPI_NAMED_ACTION_INVOKED=true',flush=True); return True
    return False


def wait_select(timeout=40):
    end=time.time()+timeout
    while time.time()<end:
        a=wait_app(3); f=flags(a)
        if f['select'] or f['character']:
            print('ATSPI_SELECT_CHARACTER_PROVEN=true',flush=True); return a
        time.sleep(1)
    return None


def semantic_character(app):
    candidates=[]
    for o in walk(app):
        a=actions(o)
        if not a: continue
        try: e=o.queryComponent().getExtents(pyatspi.DESKTOP_COORDS)
        except Exception: continue
        if 120 <= e.x <= 650 and 130 <= e.y <= 330 and e.width>20 and e.height>5:
            if name(o).lower() not in {'select character','character','status','login','cancel','ok'}:
                candidates.append((e.y,e.x,o))
    candidates.sort(key=lambda x:(x[0],x[1]))
    print(f'ATSPI_CHARACTER_ACTION_CANDIDATES={len(candidates)}',flush=True)
    if not candidates: return False
    a=actions(candidates[0][2]); a.doAction(0)
    print('ATSPI_FIRST_CHARACTER_ACTION_INVOKED=true',flush=True); return True


def main():
    mode=sys.argv[1] if len(sys.argv)>1 else 'inspect'; app=wait_app(); f=flags(app)
    if mode=='inspect':
        print(f'ATSPI_SEMANTIC_UI_AVAILABLE={str(f["editable"]>0).lower()}'); raise SystemExit(0 if f['editable'] else 3)
    if mode=='login':
        email=os.environ.get('TIBIA_TEST_EMAIL',''); password=os.environ.get('TIBIA_TEST_PASSWORD','')
        if not email or not password: raise SystemExit(2)
        if len(edits(app))<2:
            invoke(app,{'login','account login'}); time.sleep(2); app=wait_app(); flags(app)
        es=edits(app); print(f'ATSPI_LOGIN_EDITABLE_CANDIDATES={len(es)}',flush=True)
        if len(es)<2: raise SystemExit(4)
        es[0].queryEditableText().setTextContents(email); es[1].queryEditableText().setTextContents(password)
        print('ATSPI_EMAIL_SET=true',flush=True); print('ATSPI_PASSWORD_SET=true',flush=True)
        del email,password
        if invoke(app,{'login'}): print('ATSPI_LOGIN_ACTION=true',flush=True)
        else:
            try: es[1].queryComponent().grabFocus()
            except Exception: pass
            subprocess.run(['xdotool','key','Return'],check=True); print('ATSPI_LOGIN_ENTER_FALLBACK=true',flush=True)
        if wait_select() is None: raise SystemExit(5)
        return
    if mode=='character':
        app=wait_select(5)
        if app is None: raise SystemExit(5)
        if not semantic_character(app):
            print('ATSPI_CHARACTER_ACTION_UNAVAILABLE=true',flush=True); raise SystemExit(6)
        return
    raise SystemExit(2)

if __name__=='__main__': main()
