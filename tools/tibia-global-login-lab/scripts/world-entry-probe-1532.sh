#!/usr/bin/env bash
set -Eeuo pipefail

root=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
src="$root/world-entry-probe.sh"
tmp=$(mktemp "${TMPDIR:-/tmp}/otclient-tibia-1532-probe.XXXXXX.sh")
cleanup() { rm -f "$tmp"; }
trap cleanup EXIT

python3 - "$src" "$tmp" <<'PY'
from pathlib import Path
import sys

src = Path(sys.argv[1])
dst = Path(sys.argv[2])
text = src.read_text(encoding="utf-8")

# The handoff validator is fed through stdin. Without docker-exec -i, Python
# starts with an empty stdin stream, exits successfully without executing the
# validator, and no tmpfs handoff file is created.
old_stdin = 'docker exec "$CONTAINER" python3 - <<\'PY\''
new_stdin = 'docker exec -i "$CONTAINER" python3 - <<\'PY\''
if text.count(old_stdin) != 1:
    raise SystemExit(f"expected exactly one handoff docker-exec stdin site, found {text.count(old_stdin)}")
text = text.replace(old_stdin, new_stdin, 1)

# Product support remains capped at 1525. This lab-only override uses the
# existing Lua binding and never changes modules/gamelib/game.lua or game.cpp.
old_version = '    g_game.setClientVersion(1532)\n'
new_version = (
    '    g_gameConfig.setLastSupportedVersion(1532)\n'
    "    mark('CLIENT_VERSION_1532_LIMIT_OVERRIDE=true')\n"
    '    g_game.setClientVersion(1532)\n'
    "    mark('CLIENT_VERSION_1532_ACCEPTED=true')\n"
)
if text.count(old_version) != 1:
    raise SystemExit(f"expected exactly one 1532 client-version site, found {text.count(old_version)}")
text = text.replace(old_version, new_version, 1)

dst.write_text(text, encoding="utf-8")
PY

chmod 0700 "$tmp"
echo LAB_1532_PROBE_PATCH_VALIDATED=true
exec bash "$tmp"
