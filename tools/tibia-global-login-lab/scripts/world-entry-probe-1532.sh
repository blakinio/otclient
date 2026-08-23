#!/usr/bin/env bash
set -Eeuo pipefail

root=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
src="$root/world-entry-probe.sh"
tmp=$(mktemp "${TMPDIR:-/tmp}/otclient-tibia-1532-probe.XXXXXX.sh")
cleanup() { rm -f "$tmp"; }
trap cleanup EXIT

python3 - "$src" "$tmp" <<'PY'
from pathlib import Path
import re
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

# Track B is a login/session experiment, not a full content-install proof. The
# historical Synology cache happened to contain 5k+ sprite files, but game-login
# construction only requires the current catalog plus the typed data explicitly
# loaded below. Replace the historical file-count gate with semantic file gates.
old_full_asset_gate = '''asset_count=$(docker exec "$CONTAINER" bash -lc 'find /lab/state/things/1532 -maxdepth 1 -type f | wc -l')
[[ "$asset_count" -ge 5088 ]]
'''
new_minimal_asset_gate = '''docker exec "$CONTAINER" bash -lc '
set -Eeuo pipefail
root=/lab/state/things/1532
test -s "$root/catalog-content.json"
test -s "$root/assets.json.sha256"
find "$root" -maxdepth 1 -type f -name 'appearances-*.dat' -print -quit | grep -q .
find "$root" -maxdepth 1 -type f -name 'staticdata-*.dat' -print -quit | grep -q .
'
echo LAB_LOGIN_MINIMAL_ASSETS_READY=true
'''
if text.count(old_full_asset_gate) != 1:
    raise SystemExit(f"expected exactly one historical full-asset gate, found {text.count(old_full_asset_gate)}")
text = text.replace(old_full_asset_gate, new_minimal_asset_gate, 1)

old_asset_marker = "echo LAB_RUNTIME_ASSET_IDENTIFIER_LENGTH=64\n"
new_asset_marker = old_asset_marker + r'''docker exec -i "$CONTAINER" python3 - <<'PY_STATICDATA'
from pathlib import Path
import re

path = Path('/otclient/modules/game_things/things.lua')
text = path.read_text(encoding='utf-8')
old = ''' + '"""' + '''        if not g_things.loadStaticData(filePath) then
            errorList[#errorList + 1] = "Couldn't load staticdata"
        end
''' + '"""' + '''
new = ''' + '"""' + '''        -- Track B 15.32 lab: staticdata is probed explicitly below, but its
        -- known parser failure must not reset client/protocol version before
        -- the game-login packet can be tested with valid appearances.
''' + '"""' + '''
if text.count(old) == 1:
    path.write_text(text.replace(old, new, 1), encoding='utf-8')
elif new not in text:
    raise SystemExit(f'expected original or already-patched staticdata fatal gate, found {text.count(old)}')

game_path = Path('/otclient/modules/gamelib/game.lua')
game_text = game_path.read_text(encoding='utf-8')
supported_client_end = re.compile(r'(?m)(?P<version>\\b1525)(?P<closing>\\s*\\n})')
if len(supported_client_end.findall(game_text)) == 1:
    game_path.write_text(supported_client_end.sub(r'\\g<version>, 1532\\g<closing>', game_text, count=1), encoding='utf-8')
elif re.search(r'(?m)\\b1525, 1532\\s*\\n}', game_text) is None:
    raise SystemExit('expected original or already-patched supported-client tail')
PY_STATICDATA
echo LAB_STATICDATA_FATAL_GATE_BYPASSED=true
echo LAB_CLIENT_VERSION_CAP_RAISED=true
'''
if text.count(old_asset_marker) != 1:
    raise SystemExit(f"expected exactly one runtime asset marker, found {text.count(old_asset_marker)}")
text = text.replace(old_asset_marker, new_asset_marker, 1)

# Product support remains capped at 1525. Keep all 1532 compatibility work
# inside the isolated lab. The normal game_things listener resets the client
# version to zero when 15.32 staticdata fails, so disconnect only that listener
# for this bounded login experiment. All other client-version listeners remain
# connected and still configure the normal OTClient feature set.
old_version = '    g_game.setClientVersion(1532)\n'
new_version = (
    "    mark('GAME_WIRE_FULL_VERSION_NOT_ASSUMED=true')\n"
    "    mark('CLIENT_VERSION_LIMIT_OVERRIDE=true')\n"
    "    if g_game.getClientVersion()==1532 then\n"
    "      g_game.setClientVersion(0)\n"
    "      mark('CLIENT_VERSION_FEATURE_RESET=true')\n"
    "    end\n"
    '    g_game.setClientVersion(1532)\n'
    "    mark('CLIENT_VERSION_ACCEPTED=true')\n"
    "    if not g_game.getFeature(GameSessionKey) then\n"
    "      g_game.enableFeature(GameSessionKey)\n"
    "      mark('SESSION_KEY_FEATURE_LAB_OVERRIDE=true')\n"
    "    end\n"
    "    g_game.disableFeature(GameChallengeOnLogin)\n"
    "    mark('FEATURE_CHALLENGE_FIRST_REJECTED=true')\n"
    "    g_game.enableFeature(GameLoginPacketEncryption)\n"
    "    g_game.enableFeature(GameProtocolChecksum)\n"
    "    g_game.enableFeature(GameClientVersion)\n"
    "    g_game.enableFeature(GameLoginPending)\n"
    "    g_game.enableFeature(GamePreviewState)\n"
    "    g_game.enableFeature(GameSequencedPackets)\n"
    "    mark('LOGIN_PACKET_FEATURES_LAB_RESTORED=true')\n"
    "    if g_game.getFeature(GameChallengeOnLogin) then mark('FEATURE_CHALLENGE_ON_LOGIN=true') end\n"
    "    if g_game.getFeature(GameProtocolChecksum) then mark('FEATURE_PROTOCOL_CHECKSUM=true') end\n"
    "    if g_game.getFeature(GameClientVersion) then mark('FEATURE_CLIENT_VERSION=true') end\n"
    "    if g_game.getFeature(GameAuthenticator) then mark('FEATURE_AUTHENTICATOR=true') end\n"
    "    if g_game.getFeature(GameLoginPending) then mark('FEATURE_LOGIN_PENDING=true') end\n"
    "    if g_game.getFeature(GamePreviewState) then mark('FEATURE_PREVIEW_STATE=true') end\n"
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

old_rsa = "    g_game.chooseRsa('www.tibia.com')\n"
new_rsa = (
    "    if g_game.getClientVersion()~=1532 then\n"
    + "      g_game.setClientVersion(1532)\n"
    + "      mark('CLIENT_VERSION_RESTORED_AFTER_STATICDATA=true')\n"
    + "    end\n"
    + old_rsa
    + "    mark('CLIENT_VERSION_VALUE='..tostring(g_game.getClientVersion()))\n"
    + "    mark('PROTOCOL_VERSION_VALUE='..tostring(g_game.getProtocolVersion()))\n"
)
if text.count(old_rsa) != 1:
    raise SystemExit(f"expected exactly one official RSA selection site, found {text.count(old_rsa)}")
text = text.replace(old_rsa, new_rsa, 1)

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

# Run #33 failed before OTClient launch because Xvfb did not become reachable.
# Keep display recovery inside the lab: remove stale per-container lock/socket,
# verify the binary exists, require a live Xvfb PID and emit its non-secret log
# only when display startup actually fails.
old_xvfb = """docker exec "$CONTAINER" bash -lc ': >/lab/runtime/otclient.stdout.log; nohup Xvfb :100 -screen 0 1280x800x24 -nolisten tcp >/lab/runtime/xvfb.log 2>&1 </dev/null &'
for _ in $(seq 1 30); do docker exec "$CONTAINER" xdpyinfo -display :100 >/dev/null 2>&1 && break; sleep 1; done
docker exec "$CONTAINER" xdpyinfo -display :100 >/dev/null
"""
new_xvfb = """docker exec "$CONTAINER" bash -lc '
set -Eeuo pipefail
command -v Xvfb >/dev/null
rm -f /tmp/.X100-lock /tmp/.X11-unix/X100
mkdir -p /tmp/.X11-unix
: >/lab/runtime/otclient.stdout.log
: >/lab/runtime/xvfb.log
nohup Xvfb :100 -screen 0 1280x800x24 -nolisten tcp >/lab/runtime/xvfb.log 2>&1 </dev/null &
echo $! >/lab/runtime/xvfb.pid
'
xvfb_ready=false
for _ in $(seq 1 60); do
  if docker exec "$CONTAINER" xdpyinfo -display :100 >/dev/null 2>&1; then xvfb_ready=true; break; fi
  docker exec "$CONTAINER" bash -lc 'test -s /lab/runtime/xvfb.pid && kill -0 "$(cat /lab/runtime/xvfb.pid)" 2>/dev/null' || break
  sleep 0.5
done
if [[ "$xvfb_ready" != true ]]; then
  echo 'LAB_XVFB_READY=false'
  docker exec "$CONTAINER" bash -lc 'tail -n 80 /lab/runtime/xvfb.log || true'
  exit 1
fi
echo LAB_XVFB_READY=true
"""
if text.count(old_xvfb) != 1:
    raise SystemExit(f"expected exactly one Xvfb bootstrap block, found {text.count(old_xvfb)}")
text = text.replace(old_xvfb, new_xvfb, 1)

dst.write_text(text, encoding="utf-8")
PY

chmod 0700 "$tmp"
echo LAB_1532_PROBE_PATCH_VALIDATED=true
exec bash "$tmp"
