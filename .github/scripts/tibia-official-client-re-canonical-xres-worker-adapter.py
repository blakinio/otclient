#!/usr/bin/env python3
"""Build a canonical worker variant that uses raw XRes PID window ownership."""
from __future__ import annotations

import argparse
from pathlib import Path
import shlex

OLD_WINDOW = '''window() {
  local pid="$1" display="$2" xdotool="$3" attempts="$4" delay="$5"
  local win geometry candidate_area best='' best_area=0 width height
  [[ "$attempts" =~ ^[1-9][0-9]*$ ]] || return 3
  for _ in $(seq 1 "$attempts"); do
    kill -0 "$pid" 2>/dev/null || return 2
    best=''
    best_area=0
    for win in $(DISPLAY="$display" "$xdotool" search --onlyvisible --pid "$pid" --name '^Tibia$' 2>/dev/null || true); do
      geometry="$(DISPLAY="$display" "$xdotool" getwindowgeometry --shell "$win" 2>/dev/null || true)"
      width="$(sed -n 's/^WIDTH=//p' <<<"$geometry")"
      height="$(sed -n 's/^HEIGHT=//p' <<<"$geometry")"
      [[ "$width" =~ ^[0-9]+$ && "$height" =~ ^[0-9]+$ ]] || continue
      candidate_area=$((width * height))
      if ((candidate_area > best_area)); then
        best="$win"
        best_area=$candidate_area
      fi
    done
    if [[ -n "$best" ]]; then
      echo "$best"
      return 0
    fi
    sleep "$delay"
  done
  kill -0 "$pid" 2>/dev/null || return 2
  return 1
}
'''


def replacement(owner_helper: Path, wire_helper: Path) -> str:
    owner = shlex.quote(str(owner_helper.resolve()))
    wire = shlex.quote(str(wire_helper.resolve()))
    return '''window() {
  local pid="$1" display="$2" _legacy_xdotool="$3" attempts="$4" delay="$5"
  local rc=0
  [[ "$attempts" =~ ^[1-9][0-9]*$ ]] || return 3
  kill -0 "$pid" 2>/dev/null || return 2
  python3 OWNER_HELPER \
    --display "$display" \
    --pid "$pid" \
    --toolroot "$TOOL" \
    --wire-helper WIRE_HELPER \
    --attempts "$attempts" \
    --delay "$delay" || rc=$?
  if (( rc != 0 )); then
    kill -0 "$pid" 2>/dev/null || return 2
    return 3
  fi
}
'''.replace("OWNER_HELPER", owner).replace("WIRE_HELPER", wire)


def patch(source: str, owner_helper: Path, wire_helper: Path) -> str:
    count = source.count(OLD_WINDOW)
    if count != 1:
        raise ValueError(f"canonical window anchor count is {count}, expected 1")
    result = source.replace(OLD_WINDOW, replacement(owner_helper, wire_helper), 1)
    if "search --onlyvisible --pid" in result:
        raise ValueError("legacy xdotool PID/name selector remains")
    if owner_helper.name != "tibia-official-client-re-xres-window-owner.py":
        raise ValueError("unexpected XRes owner helper path")
    if wire_helper.name != "tibia-official-client-re-xres-wire.py":
        raise ValueError("unexpected XRes wire helper path")
    return result


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("source", type=Path)
    result.add_argument("output", type=Path)
    result.add_argument("--owner-helper", required=True, type=Path)
    result.add_argument("--wire-helper", required=True, type=Path)
    return result


def main() -> int:
    args = parser().parse_args()
    if not args.source.is_file():
        raise SystemExit("TRACK_A_CANONICAL_XRES_ADAPTER_ERROR=source_missing")
    if not args.owner_helper.is_file() or not args.wire_helper.is_file():
        raise SystemExit("TRACK_A_CANONICAL_XRES_ADAPTER_ERROR=helper_missing")
    try:
        result = patch(
            args.source.read_text(encoding="utf-8"),
            args.owner_helper,
            args.wire_helper,
        )
    except ValueError as exc:
        raise SystemExit(f"TRACK_A_CANONICAL_XRES_ADAPTER_ERROR={exc}") from exc
    args.output.write_text(result, encoding="utf-8")
    args.output.chmod(0o755)
    print("TRACK_A_CANONICAL_XRES_ADAPTER=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
