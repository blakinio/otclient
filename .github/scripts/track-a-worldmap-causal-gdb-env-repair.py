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

OLD_ATTACH_BLOCK = '''sleep 2
kill -0 "$PID" || fail client_died_while_arming_observer
kill -0 "$GDB_PID" || fail gdb_observer_not_alive
[[ "$(awk '/^TracerPid:/{print $2}' "/proc/$PID/status")" == "$GDB_PID" ]] || fail gdb_not_attached_to_exact_client'''

NEW_ATTACH_BLOCK = r'''emit_gdb_attach_diagnostic() {
  echo 'WORLDMAP_BASELINE_GDB_ATTACH_DIAGNOSTIC_BEGIN'
  sed -n '1,20p' "$GOUT" 2>/dev/null | \
    sed -E 's#(/home|/work)/[^ ]+#<PATH>#g; s/[0-9]{4,}/<NUM>/g'
  echo 'WORLDMAP_BASELINE_GDB_ATTACH_DIAGNOSTIC_END'
}

GDB_ATTACHED=0
for _ in $(seq 1 40); do
  kill -0 "$PID" 2>/dev/null || fail client_died_while_arming_observer
  if ! kill -0 "$GDB_PID" 2>/dev/null; then
    emit_gdb_attach_diagnostic
    fail gdb_observer_not_alive
  fi
  TRACER_PID="$(awk '/^TracerPid:/{print $2}' "/proc/$PID/status")"
  if [[ "$TRACER_PID" == "$GDB_PID" ]]; then
    GDB_ATTACHED=1
    break
  fi
  sleep .25
done
if [[ "$GDB_ATTACHED" != 1 ]]; then
  emit_gdb_attach_diagnostic
  fail gdb_not_attached_to_exact_client
fi
echo 'WORLDMAP_BASELINE_GDB_ATTACH=PASS' '''


def transform(text: str) -> str:
    if text.count(OLD_LAUNCH) != 1:
        raise RepairRefused(f"GDB_LAUNCH_ANCHOR_COUNT:{text.count(OLD_LAUNCH)}")
    text = text.replace(OLD_LAUNCH, NEW_LAUNCH, 1)
    if text.count(OLD_ATTACH_BLOCK) != 1:
        raise RepairRefused(f"GDB_ATTACH_ANCHOR_COUNT:{text.count(OLD_ATTACH_BLOCK)}")
    text = text.replace(OLD_ATTACH_BLOCK, NEW_ATTACH_BLOCK, 1)
    if text.count('LD_LIBRARY_PATH="$TOOL/usr/lib/x86_64-linux-gnu:$TOOL/lib/x86_64-linux-gnu"') != 1:
        raise RepairRefused("GDB_TOOLROOT_ENV_NOT_UNIQUE")
    if text.count("WORLDMAP_BASELINE_GDB_ATTACH=PASS") != 1:
        raise RepairRefused("GDB_ATTACH_PASS_MARKER_NOT_UNIQUE")
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
