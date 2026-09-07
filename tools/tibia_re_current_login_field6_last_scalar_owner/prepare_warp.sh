#!/usr/bin/env bash
set -Eeuo pipefail
: "${FIELD6_LAST_SCALAR_ROOT:?FIELD6_LAST_SCALAR_ROOT is required}"
WARP_PROFILE_ATTEMPTS=2
root="$FIELD6_LAST_SCALAR_ROOT"; wgcf="$root/bin/wgcf"; wireproxy="$root/bin/wireproxy"; ports=(25352 25353)
for attempt in $(seq 1 "$WARP_PROFILE_ATTEMPTS"); do
  port="${ports[$((attempt - 1))]}"; state="$root/state-$attempt"; mkdir -p "$state"; pushd "$state" >/dev/null
  if ! "$wgcf" register --accept-tos >/dev/null 2>&1; then popd >/dev/null; continue; fi
  if ! "$wgcf" generate >/dev/null 2>&1; then popd >/dev/null; continue; fi
  printf 'WGConfig = %s\n\n[Socks5]\nBindAddress = 127.0.0.1:%s\n' "$state/wgcf-profile.conf" "$port" > wireproxy.conf
  "$wireproxy" -c wireproxy.conf >"$state/wireproxy.log" 2>&1 </dev/null & proxy_pid=$!
  ready=false
  for _ in $(seq 1 15); do
    if curl --socks5-hostname "127.0.0.1:$port" -fsS --max-time 4 https://www.cloudflare.com/cdn-cgi/trace >"$state/trace" 2>/dev/null && grep -Eq '^warp=(on|plus)$' "$state/trace"; then ready=true; break; fi
    sleep 2
  done
  if [[ "$ready" == true ]]; then
    printf '%s\n' "$port" > "$root/active-socks-port"; printf '%s\n' "$proxy_pid" > "$root/active-wireproxy-pid"
    echo 'WARP_BOOTSTRAP_FALLBACK=PASS'; echo "WARP_PROFILE_ATTEMPT=$attempt"; popd >/dev/null; exit 0
  fi
  kill "$proxy_pid" 2>/dev/null || true; wait "$proxy_pid" 2>/dev/null || true; popd >/dev/null
done
echo 'WARP_BOOTSTRAP_FALLBACK=FAIL' >&2; exit 1
