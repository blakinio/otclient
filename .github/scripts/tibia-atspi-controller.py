#!/usr/bin/env python3
"""Control the official Tibia login UI through AT-SPI semantics, never OCR.

The script never prints accessible text except fixed allow-listed UI markers.
Secrets are read from environment and passed only to EditableText.setTextContents.
Authenticated account/character strings are never emitted.
"""
from __future__ import annotations

import os
import sys
import time

import pyatspi


def children(obj):
    try:
        return [obj.getChildAtIndex(i) for i in range(obj.childCount)]
    except Exception:
        return []


def walk(root, max_nodes=5000):
    stack=[root]
    seen=0
    while stack and seen < max_nodes:
        obj=stack.pop()
        seen += 1
        yield obj
        try:
            stack.extend(reversed(children(obj)))
        except Exception:
            pass


def role_name(obj):
    try:
        return (obj.getRoleName() or '').lower()
    except Exception:
        return ''


def safe_name(obj):
    try:
        return (obj.name or '').strip()
    except Exception:
        return ''


def action_names(obj):
    try:
        a=obj.queryAction()
        return [(i,(a.getName(i) or '').lower()) for i in range(a.nActions)]
    except Exception:
        return []


def find_tibia_app():
    desk=pyatspi.Registry.getDesktop(0)
    apps=[]
    for i in range(desk.childCount):
        try:
            app=desk.getChildAtIndex(i)
            name=safe_name(app).lower()
            if 'tibia' in name:
                apps.append(app)
        except Exception:
            pass
    return apps[0] if apps else None


def wait_app(timeout=30):
    end=time.time()+timeout
    while time.time()<end:
        app=find_tibia_app()
        if app is not None:
            return app
        time.sleep(0.5)
    raise RuntimeError('Tibia AT-SPI application not found')


def editable_nodes(app):
    out=[]
    for obj in walk(app):
        try:
            obj.queryEditableText()
        except Exception:
            continue
        r=role_name(obj)
        if any(x in r for x in ('text','entry','password')) or r:
            out.append(obj)
    return out


def marker_flags(app):
    account=False; login=False; select=False; character=False
    editable=0; buttons=0; actionable=0
    roles={}
    for obj in walk(app):
        r=role_name(obj)
        roles[r]=roles.get(r,0)+1
        n=safe_name(obj).lower()
        if n in {'account','account login'}: account=True
        if n == 'login': login=True
        if n == 'select character': select=True
        if n == 'character': character=True
        try:
            obj.queryEditableText(); editable += 1
        except Exception:
            pass
        acts=action_names(obj)
        if acts:
            actionable += 1
            if 'button' in r or 'push' in r:
                buttons += 1
    print(f'ATSPI_EDITABLE_COUNT={editable}', flush=True)
    print(f'ATSPI_ACTIONABLE_COUNT={actionable}', flush=True)
    print(f'ATSPI_BUTTON_COUNT={buttons}', flush=True)
    print(f'ATSPI_ACCOUNT_MARKER={str(account).lower()}', flush=True)
    print(f'ATSPI_LOGIN_MARKER={str(login).lower()}', flush=True)
    print(f'ATSPI_SELECT_CHARACTER_MARKER={str(select).lower()}', flush=True)
    print(f'ATSPI_CHARACTER_HEADER_MARKER={str(character).lower()}', flush=True)
    return {'account':account,'login':login,'select':select,'character':character,'editable':editable}


def invoke_named_action(app, allowed_names):
    allowed={x.lower() for x in allowed_names}
    for obj in walk(app):
        n=safe_name(obj).lower()
        if n not in allowed:
            continue
        try:
            a=obj.queryAction()
            if a.nActions:
                ok=a.doAction(0)
                print('ATSPI_NAMED_ACTION_INVOKED=true', flush=True)
                return bool(ok) or True
        except Exception:
            pass
    return False


def set_login_fields(app, email, password):
    edits=editable_nodes(app)
    print(f'ATSPI_LOGIN_EDITABLE_CANDIDATES={len(edits)}', flush=True)
    if len(edits) < 2:
        return False
    # Prefer top-to-bottom screen order when component extents are available.
    def key(o):
        try:
            c=o.queryComponent(); ext=c.getExtents(pyatspi.DESKTOP_COORDS)
            return (ext.y,ext.x)
        except Exception:
            return (10**9,10**9)
    edits.sort(key=key)
    chosen=edits[:2]
    vals=[email,password]
    for obj,val in zip(chosen,vals):
        try:
            e=obj.queryEditableText()
            e.setTextContents(val)
        except Exception as exc:
            raise RuntimeError('AT-SPI EditableText set failed') from exc
    print('ATSPI_EMAIL_SET=true', flush=True)
    print('ATSPI_PASSWORD_SET=true', flush=True)
    return True


def activate_first_character_semantic(app):
    # Prefer actionable objects in the body under a Select Character state.
    candidates=[]
    for obj in walk(app):
        r=role_name(obj)
        acts=action_names(obj)
        if not acts:
            continue
        try:
            c=obj.queryComponent(); ext=c.getExtents(pyatspi.DESKTOP_COORDS)
            x,y,w,h=ext.x,ext.y,ext.width,ext.height
        except Exception:
            continue
        # Same bounded central list region as the proven 1020x650 dialog, but
        # the activation is semantic AT-SPI action, not pixel clicking.
        if 120 <= x <= 650 and 130 <= y <= 330 and w > 20 and h > 5:
            n=safe_name(obj).lower()
            # Avoid known headers/buttons; never print any remaining name.
            if n in {'select character','character','status','login','cancel','ok'}:
                continue
            candidates.append((y,x,obj))
    candidates.sort(key=lambda t:(t[0],t[1]))
    print(f'ATSPI_CHARACTER_ACTION_CANDIDATES={len(candidates)}', flush=True)
    for _,_,obj in candidates:
        try:
            a=obj.queryAction()
            if a.nActions:
                a.doAction(0)
                print('ATSPI_FIRST_CHARACTER_ACTION_INVOKED=true', flush=True)
                return True
        except Exception:
            continue
    return False


def main():
    mode=sys.argv[1] if len(sys.argv)>1 else 'inspect'
    app=wait_app()
    flags=marker_flags(app)
    if mode == 'inspect':
        if flags['editable'] < 1:
            raise SystemExit(3)
        print('ATSPI_SEMANTIC_UI_AVAILABLE=true')
        return
    if mode != 'login':
        raise SystemExit('unknown mode')

    email=os.environ.get('TIBIA_TEST_EMAIL','')
    password=os.environ.get('TIBIA_TEST_PASSWORD','')
    if not email or not password:
        raise SystemExit('missing secrets')

    # Some builds expose a landing Login action before fields; invoke only the
    # allow-listed semantic name, then rescan. If fields already exist, skip it.
    if len(editable_nodes(app)) < 2:
        invoke_named_action(app, {'login','account login'})
        time.sleep(2)
        app=wait_app()
        marker_flags(app)

    if not set_login_fields(app,email,password):
        raise SystemExit(4)
    del email, password

    if not invoke_named_action(app, {'login'}):
        # Focus the password field and use Enter as semantic keyboard fallback.
        edits=editable_nodes(app)
        if len(edits) >= 2:
            edits.sort(key=lambda o: (o.queryComponent().getExtents(pyatspi.DESKTOP_COORDS).y,
                                      o.queryComponent().getExtents(pyatspi.DESKTOP_COORDS).x))
            try:
                edits[1].queryComponent().grabFocus()
            except Exception:
                pass
        import subprocess
        subprocess.run(['xdotool','key','Return'],check=True)
        print('ATSPI_LOGIN_ENTER_FALLBACK=true', flush=True)
    else:
        print('ATSPI_LOGIN_ACTION=true', flush=True)

    # Wait for Select Character semantic marker; never emit its child text.
    deadline=time.time()+35
    selected=False
    while time.time()<deadline:
        app=wait_app(3)
        flags=marker_flags(app)
        if flags['select'] or flags['character']:
            print('ATSPI_SELECT_CHARACTER_PROVEN=true', flush=True)
            selected=True
            break
        time.sleep(1)
    if not selected:
        raise SystemExit(5)

    if not activate_first_character_semantic(app):
        # Character row action may not be exposed; signal caller for a bounded
        # coordinate fallback only after Select Character was semantically proven.
        print('ATSPI_CHARACTER_ACTION_UNAVAILABLE=true', flush=True)
        raise SystemExit(6)


if __name__ == '__main__':
    main()
