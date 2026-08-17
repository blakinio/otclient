#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


class RepairRefused(RuntimeError):
    pass


OLD_LAUNCH = (
    '  OTCLIENT_TIBIA_RE_TRACK=official-client-re "$EPHEMERAL_MARK" '
    'OTCLIENT_TIBIA_RE_ROLE=worldmap-observer \\\n'
    '  "$GDB" -q -nx -batch -x "$GCMD" >"$GOUT" 2>&1 </dev/null &'
)

NEW_LAUNCH = (
    '  OTCLIENT_TIBIA_RE_TRACK=official-client-re "$EPHEMERAL_MARK" '
    'OTCLIENT_TIBIA_RE_ROLE=worldmap-observer \\\n'
    '  HOME="$SESSION/home" DISPLAY="$DISPLAY" \\\n'
    '  PATH="$TOOL/usr/bin:$TOOL/usr/sbin:/usr/bin:/bin" \\\n'
    '  LD_LIBRARY_PATH="$TOOL/usr/lib/x86_64-linux-gnu:$TOOL/lib/x86_64-linux-gnu" \\\n'
    '  "$GDB" -q -nx -batch -x "$GCMD" >"$GOUT" 2>&1 </dev/null &'
)

OLD_FAILURE = 'kill -0 "$GDB_PID" || fail gdb_observer_not_alive'
NEW_FAILURE = (
    'if ! kill -0 "$GDB_PID" 2>/dev/null; then\n'
    "  echo 'WORLDMAP_BASELINE_GDB_ATTACH_DIAGNOSTIC_BEGIN'\n"
    '  sed -n \'1,20p\' "$GOUT" 2>/dev/null | '
    "sed -E 's#(/home|/work)/[^ ]+#<PATH>#g; s/[0-9]{4,}/<NUM>/g'\n"
    "  echo 'WORLDMAP_BASELINE_GDB_ATTACH_DIAGNOSTIC_END'\n"
    '  fail gdb_observer_not_alive\n'
    'fi'
)


def transform(text: str) -> str:
    if text.count(OLD_LAUNCH) != 1:
        raise RepairRefused(f"GDB_LAUNCH_ANCHOR_COUNT:{text.count(OLD_LAUNCH)}")
    text = text.replace(OLD_LAUNCH, NEW_LAUNCH, 1)
    if text.count(OLD_FAILURE) != 1:
        raise RepairRefused(f"GDB_FAILURE_ANCHOR_COUNT:{text.count(OLD_FAILURE)}")
    text = text.replace(OLD_FAILURE, NEW_FAILURE, 1)
    if text.count('LD_LIBRARY_PATH="$TOOL/usr/lib/x86_64-linux-gnu:$TOOL/lib/x86_64-linux-gnu"') != 1:
        raise RepairRefused("GDB_TOOLROOT_ENV_NOT_UNIQUE")
    if 'libpython3.12.so.1.0' in text:
        raise RepairRefused("HARD_CODED_LIBRARY_ERROR_NOT_ALLOWED")
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    source = args.source.read_text(encoding="utf-8")
    try:
        repaired = transform(source)
    except RepairRefused as exc:
        print(f"WORLDMAP_GDB_ENV_REPAIR_REFUSED={exc}")
        return 44
    args.output.write_text(repaired, encoding="utf-8")
    args.output.chmod(0o700)
    print("WORLDMAP_GDB_ENV_REPAIR=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
