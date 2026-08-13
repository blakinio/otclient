#!/usr/bin/env python3
"""Control the official Linux Tibia UI through AT-SPI semantics; never OCR.

Only allow-listed markers/counters are printed. Secrets and account/character
strings are never emitted.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time

import pyatspi


def children(obj):
    try:
        return [obj.getChildAtIndex(i) for i in range(obj.childCount)]
    except Exception:
        return []


def walk(root, limit=5000):
    stack = [root]
    seen = 0
    while stack and seen < limit:
        obj = stack.pop()
        seen += 1
        yield obj
        stack.extend(reversed(children(obj)))


def name(obj):
    try:
        return (obj.name or "").strip()
    except Exception:
        return ""


def actions(obj):
    try:
        action = obj.queryAction()
        return action if action.nActions else None
    except Exception:
        return None


def app_now():
    desktop = pyatspi.Registry.getDesktop(0)
    for i in range(desktop.childCount):
        try:
            app = desktop.getChildAtIndex(i)
            if "tibia" in name(app).lower():
                return app
        except Exception:
            pass
    return None


def wait_app(timeout=30):
    end = time.time() + timeout
    while time.time() < end:
        app = app_now()
        if app is not None:
            return app
        time.sleep(0.5)
    raise RuntimeError("Tibia AT-SPI application not found")


def edits(app):
    result = []
    for obj in walk(app):
        try:
            obj.queryEditableText()
            result.append(obj)
        except Exception:
            pass

    def key(obj):
        try:
            ext = obj.queryComponent().getExtents(pyatspi.DESKTOP_COORDS)
            return (ext.y, ext.x)
        except Exception:
            return (10**9, 10**9)

    result.sort(key=key)
    return result


def flags(app):
    values = {"account": False, "login": False, "select": False, "character": False}
    editable = actionable = 0
    for obj in walk(app):
        obj_name = name(obj).lower()
        if obj_name in {"account", "account login"}:
            values["account"] = True
        if obj_name == "login":
            values["login"] = True
        if obj_name == "select character":
            values["select"] = True
        if obj_name == "character":
            values["character"] = True
        try:
            obj.queryEditableText()
            editable += 1
        except Exception:
            pass
        if actions(obj):
            actionable += 1
    print(f"ATSPI_EDITABLE_COUNT={editable}", flush=True)
    print(f"ATSPI_ACTIONABLE_COUNT={actionable}", flush=True)
    for key, value in values.items():
        print(f"ATSPI_{key.upper()}_MARKER={str(value).lower()}", flush=True)
    values["editable"] = editable
    return values


def invoke(app, allowed):
    allowed = {value.lower() for value in allowed}
    for obj in walk(app):
        if name(obj).lower() not in allowed:
            continue
        action = actions(obj)
        if action:
            action.doAction(0)
            print("ATSPI_NAMED_ACTION_INVOKED=true", flush=True)
            return True
    return False


def wait_select(timeout=40):
    end = time.time() + timeout
    while time.time() < end:
        app = wait_app(3)
        current = flags(app)
        if current["select"] or current["character"]:
            print("ATSPI_SELECT_CHARACTER_PROVEN=true", flush=True)
            return app
        time.sleep(1)
    return None


def semantic_character(app):
    candidates = []
    for obj in walk(app):
        action = actions(obj)
        if not action:
            continue
        try:
            ext = obj.queryComponent().getExtents(pyatspi.DESKTOP_COORDS)
        except Exception:
            continue
        if 120 <= ext.x <= 650 and 130 <= ext.y <= 330 and ext.width > 20 and ext.height > 5:
            if name(obj).lower() not in {"select character", "character", "status", "login", "cancel", "ok"}:
                candidates.append((ext.y, ext.x, obj))
    candidates.sort(key=lambda value: (value[0], value[1]))
    print(f"ATSPI_CHARACTER_ACTION_CANDIDATES={len(candidates)}", flush=True)
    if not candidates:
        return False
    action = actions(candidates[0][2])
    action.doAction(0)
    print("ATSPI_FIRST_CHARACTER_ACTION_INVOKED=true", flush=True)
    return True


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "inspect"
    app = wait_app()
    current = flags(app)

    if mode == "inspect":
        available = current["editable"] > 0 or current["select"] or current["character"]
        print(f"ATSPI_SEMANTIC_UI_AVAILABLE={str(available).lower()}", flush=True)
        raise SystemExit(0 if available else 3)

    if mode == "login":
        email = os.environ.get("TIBIA_TEST_EMAIL", "")
        password = os.environ.get("TIBIA_TEST_PASSWORD", "")
        if not email or not password:
            raise SystemExit(2)
        if len(edits(app)) < 2:
            invoke(app, {"login", "account login"})
            time.sleep(2)
            app = wait_app()
            flags(app)
        editables = edits(app)
        print(f"ATSPI_LOGIN_EDITABLE_CANDIDATES={len(editables)}", flush=True)
        if len(editables) < 2:
            raise SystemExit(4)
        editables[0].queryEditableText().setTextContents(email)
        editables[1].queryEditableText().setTextContents(password)
        print("ATSPI_EMAIL_SET=true", flush=True)
        print("ATSPI_PASSWORD_SET=true", flush=True)
        del email, password
        if invoke(app, {"login"}):
            print("ATSPI_LOGIN_ACTION=true", flush=True)
        else:
            try:
                editables[1].queryComponent().grabFocus()
            except Exception:
                pass
            subprocess.run(["xdotool", "key", "Return"], check=True)
            print("ATSPI_LOGIN_ENTER_FALLBACK=true", flush=True)
        if wait_select() is None:
            raise SystemExit(5)
        return

    if mode == "character":
        app = wait_select(5)
        if app is None:
            raise SystemExit(5)
        if not semantic_character(app):
            print("ATSPI_CHARACTER_ACTION_UNAVAILABLE=true", flush=True)
            raise SystemExit(6)
        return

    raise SystemExit(2)


if __name__ == "__main__":
    main()
