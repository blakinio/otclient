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

# Product support remains capped at 1525. Keep all 1532 compatibility work
# inside the isolated lab. The normal game_things listener resets the client
# version to zero when 15.32 staticdata fails, so disconnect only that listener
# for this bounded login experiment. All other client-version listeners remain
# connected and still configure the normal OTClient feature set.
old_version = '    g_game.setClientVersion(1532)\n'
new_version = (
    "    local gameThingsLoad=modules.game_things and modules.game_things.load or nil\n"
    "    if gameThingsLoad then\n"
    "      disconnect(g_game,{onClientVersionChange=gameThingsLoad})\n"
    "      mark('GAME_THINGS_AUTOLOAD_DISCONNECTED=true')\n"
    "    end\n"
    '    g_gameConfig.setLastSupportedVersion(1532)\n'
    "    mark('CLIENT_VERSION_LIMIT_OVERRIDE=true')\n"
    '    g_game.setClientVersion(1532)\n'
    "    mark('CLIENT_VERSION_ACCEPTED=true')\n"
    "    local thingsPath=resolvepath('/data/things/1532/')\n"
    "    local appearancesCall,appearancesResult=pcall(function() return g_things.loadAppearances(thingsPath) end)\n"
    "    if appearancesCall and appearancesResult then mark('APPEARANCES_LOAD_OK=true') else mark('APPEARANCES_LOAD_FAILED=true') end\n"
    "    local staticCall,staticResult=pcall(function() return g_things.loadStaticData(thingsPath) end)\n"
    "    if staticCall and staticResult then\n"
    "      mark('STATICDATA_LOAD_OK=true')\n"
    "    else\n"
    "      mark('STATICDATA_LOAD_FAILED=true')\n"
    "      mark('STATICDATA_BYPASSED_FOR_LOGIN=true')\n"
    "    end\n"
)
if text.count(old_version) != 1:
    raise SystemExit(f"expected exactly one 1532 client-version site, found {text.count(old_version)}")
text = text.replace(old_version, new_version, 1)

# Run #31 proved that appearances parse successfully while staticdata does not.
# For the login-only experiment require the appearance catalogue (needed for
# game objects) but do not make unrelated staticdata compatibility a gate. This
# does not claim staticdata support; the failure/bypass markers remain explicit.
old_gate = """    if modules.game_things and modules.game_things.isLoaded and not modules.game_things.isLoaded() then
      handoff.sessionKey=nil
      mark('THINGS_NOT_LOADED=true')
      return
    end
    mark('THINGS_LOADED=true')
"""
new_gate = """    if not appearancesCall or not appearancesResult then
      handoff.sessionKey=nil
      mark('THINGS_APPEARANCES_NOT_READY=true')
      return
    end
    mark('THINGS_APPEARANCES_READY=true')
"""
if text.count(old_gate) != 1:
    raise SystemExit(f"expected exactly one normal things gate, found {text.count(old_gate)}")
text = text.replace(old_gate, new_gate, 1)

dst.write_text(text, encoding="utf-8")
PY

chmod 0700 "$tmp"
echo LAB_1532_PROBE_PATCH_VALIDATED=true
exec bash "$tmp"
