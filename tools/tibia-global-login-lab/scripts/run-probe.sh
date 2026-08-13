#!/usr/bin/env bash
set -Eeuo pipefail
set +x

src="tools/tibia-global-login-lab/scripts/login-probe.sh"
work="$(mktemp)"
trap 'rm -f "$work"' EXIT
cp "$src" "$work"

python3 - "$work" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text()
replacements = {
    'IMAGE="ghcr.io/blakinio/otclient:latest"':
        'IMAGE="otclient-tibia-global-login-lab-runtime:local"',
    'pkill -f "/wireproxy .*wireproxy.conf" 2>/dev/null || true':
        'if [[ -s "$root/wireproxy.pid" ]]; then oldpid=$(cat "$root/wireproxy.pid"); kill "$oldpid" 2>/dev/null || true; rm -f "$root/wireproxy.pid"; fi',
    'nohup "$bin/wireproxy" -c "$state/wireproxy.conf" >"$root/wireproxy.log" 2>&1 </dev/null &':
        'nohup "$bin/wireproxy" -c "$state/wireproxy.conf" >"$root/wireproxy.log" 2>&1 </dev/null & echo $! >"$root/wireproxy.pid"',
}
for old, new in replacements.items():
    if old not in text:
        raise SystemExit(f"required probe fragment missing: {old}")
    text = text.replace(old, new, 1)
path.write_text(text)
PY

bash "$work"
