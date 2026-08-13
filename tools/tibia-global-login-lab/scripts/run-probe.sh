#!/usr/bin/env bash
set -Eeuo pipefail
set +x

src="tools/tibia-global-login-lab/scripts/login-probe.sh"
work="$(mktemp)"
trap 'rm -f "$work"' EXIT
cp "$src" "$work"

# The bootstrap phase preserves the expensive dependency layer in this runner-local image.
sed -i 's|^IMAGE="ghcr.io/blakinio/otclient:latest"$|IMAGE="otclient-tibia-global-login-lab-runtime:local"|' "$work"

# Never use pkill -f from inside bash -lc: the command line of that shell can match
# the pattern and terminate itself (observed as exit 143 in run 31679583955).
sed -i 's|^pkill -f "/wireproxy .*wireproxy.conf" 2>/dev/null || true$|if [[ -s "$root/wireproxy.pid" ]]; then oldpid=$(cat "$root/wireproxy.pid"); kill "$oldpid" 2>/dev/null || true; rm -f "$root/wireproxy.pid"; fi|' "$work"
sed -i 's|^nohup "$bin/wireproxy" -c "$state/wireproxy.conf" >"$root/wireproxy.log" 2>&1 </dev/null &$|nohup "$bin/wireproxy" -c "$state/wireproxy.conf" >"$root/wireproxy.log" 2>&1 </dev/null \& echo $! >"$root/wireproxy.pid"|' "$work"

bash "$work"
