#!/usr/bin/env bash
set +x
set -Eeuo pipefail
umask 077
BASE=/home/runner/_work/_otclient_tibia_re_state
ROOT="$BASE/canonical-live-runtime"; SESSION="$ROOT/session"; WARP="$ROOT/warp"; TOOL="$BASE/toolroot"
SIZE=51965216; SHA=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
MARK='OTCLIENT_TIBIA_RE_TRACK=official-client-re'; RMARK='OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1'
WGCF_VER=2.2.32; WGCF_SHA=2ff97f2201972ce582a424455d50a3719a380eef0cd1f3144f7779348e122a2c
WP_VER=1.1.3; WP_TAR_SHA=e88c1d090740373fc606c1bafd81d9a5eadc642cce5667616e20e9d7a444f51c

die(){ printf 'TRACK_A_CANONICAL_SESSION_ERROR=%s\n' "$1" >&2; exit 1; }
rpid(){ tr -cd '0-9' <"$SESSION/$1.pid" 2>/dev/null || true; }
listen(){ python3 - "$1" <<'PY'
import pathlib,sys
p=f'{int(sys.argv[1]):04X}'
for n in ('tcp','tcp6'):
 f=pathlib.Path('/proc/net')/n
 if not f.exists():continue
 for r in f.read_text().splitlines()[1:]:
  x=r.split()
  if len(x)>3 and x[1].rsplit(':',1)[-1].upper()==p and x[3]=='0A':raise SystemExit(0)
raise SystemExit(1)
PY
}
owned(){ local p="$1" r="$2" e="${3:-}"; [[ "$p" =~ ^[1-9][0-9]*$ && -r /proc/$p/environ ]]||return 1;grep -azFxq "$MARK" /proc/$p/environ||return 1;grep -azFxq "$RMARK" /proc/$p/environ||return 1;grep -azFxq "OTCLIENT_TIBIA_RE_ROLE=$r" /proc/$p/environ||return 1;[[ -z "$e" || "$(readlink -f /proc/$p/exe)" == "$(readlink -f "$e")" ]]; }
nosecret(){ ! grep -azEq '^(TIBIA_TEST_EMAIL|TIBIA_TEST_PASSWORD|TRACK_A_CANONICAL_LEASE_TOKEN|TRACK_A_CANONICAL_LEASE_TOKEN_FILE)=' /proc/$1/environ||die "$2_secret_env_leak"; }
verify_client(){ [[ -x "$1" && ! -L "$1" ]]||die client_not_executable;[[ "$(stat -c %s "$1")" == "$SIZE" ]]||die client_size_mismatch;[[ "$(sha256sum "$1"|awk '{print $1}')" == "$SHA" ]]||die client_sha_mismatch; }
tool(){ local p;p="$(command -v "$1" 2>/dev/null||true)";[[ -n "$p" && -x "$p" ]]&&{ printf '%s\n' "$p";return; };p="$(find "$TOOL" -type f -name "$1" -perm -u+x -print -quit 2>/dev/null||true)";[[ -n "$p" ]]&&printf '%s\n' "$p"; }
free_display(){ local n;for n in $(seq 98 130);do [[ ! -e /tmp/.X$n-lock && ! -e /tmp/.X11-unix/X$n ]]&&{ echo "$n";return; };done;return 1; }
free_port(){ local p;for p in $(seq "$1" "$2");do listen "$p"||{ echo "$p";return; };done;return 1; }
source_pkg(){ local p c;for p in "$BASE/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia" "/work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia";do c="$p/bin/client";if [[ -x "$c" && ! -L "$c" && "$(stat -c %s "$c" 2>/dev/null||true)" == "$SIZE" && "$(sha256sum "$c" 2>/dev/null|awk '{print $1}')" == "$SHA" ]];then echo "$p";return;fi;done;return 1; }
window(){ local pid="$1" d="$2" x="$3" w g a best area bw bh;for _ in $(seq 1 120);do best=;area=0;for w in $(DISPLAY="$d" "$x" search --onlyvisible --pid "$pid" --name '^Tibia$' 2>/dev/null||true);do g="$(DISPLAY="$d" "$x" getwindowgeometry --shell "$w" 2>/dev/null||true)";bw="$(sed -n 's/^WIDTH=//p'<<<"$g")";bh="$(sed -n 's/^HEIGHT=//p'<<<"$g")";[[ "$bw" =~ ^[0-9]+$ && "$bh" =~ ^[0-9]+$ ]]||continue;a=$((bw*bh));((a>area))&&{ best="$w";area=$a; };done;[[ -n "$best" ]]&&{ echo "$best";return; };sleep .25;done;return 1; }

contract_test(){ [[ "${TRACK_A_CANONICAL_WORKER_CONTRACT_TEST:-}" == 1 ]]||return 1;case "${1:-}" in bootstrap) [[ $# == 2 ]]||die usage;python3 - "$2" <<'PY'
import json,os,sys
json.dump({'pid':os.getpid(),'process_group_id':os.getpgrp(),'display':':199','window_identity':'test','remote_view_endpoint':'127.0.0.1:6199','remote_view_mapping':'UNKNOWN','state':'UNKNOWN'},open(sys.argv[1],'w'))
PY
;;probe) [[ $# == 2 ]]||die usage;python3 - "$2" <<'PY'
import json,os,sys
json.dump({'pid':os.getpid(),'display':':199','window_identity':'test','remote_view_endpoint':'127.0.0.1:6199','remote_view_mapping':'UNKNOWN','state':'UNKNOWN'},open(sys.argv[1],'w'))
PY
;;rollback) [[ $# == 2 ]]||die usage;;*)die usage;;esac;exit 0; }

warp_tools(){ local b="$WARP/bin" t wp;mkdir -p "$b" "$WARP/state";chmod 700 "$WARP" "$WARP/state";if [[ ! -x "$b/wgcf" || "$(sha256sum "$b/wgcf" 2>/dev/null|awk '{print $1}')" != "$WGCF_SHA" ]];then t="$b/.wgcf";curl -fL --retry 3 --connect-timeout 10 -o "$t" "https://github.com/ViRb3/wgcf/releases/download/v$WGCF_VER/wgcf_${WGCF_VER}_linux_amd64";[[ "$(sha256sum "$t"|awk '{print $1}')" == "$WGCF_SHA" ]]||die wgcf_hash_mismatch;chmod 755 "$t";mv -f "$t" "$b/wgcf";fi
t="$b/wireproxy.tar.gz";if [[ ! -s "$t" || "$(sha256sum "$t" 2>/dev/null|awk '{print $1}')" != "$WP_TAR_SHA" ]];then curl -fL --retry 3 --connect-timeout 10 -o "$t.tmp" "https://github.com/windtf/wireproxy/releases/download/v$WP_VER/wireproxy_linux_amd64.tar.gz";[[ "$(sha256sum "$t.tmp"|awk '{print $1}')" == "$WP_TAR_SHA" ]]||die wireproxy_archive_hash_mismatch;mv -f "$t.tmp" "$t";fi
rm -rf "$b/.wpx";mkdir "$b/.wpx";tar -xzf "$t" -C "$b/.wpx";wp="$(find "$b/.wpx" -type f -name wireproxy -print -quit)";[[ -n "$wp" ]]||die wireproxy_binary_missing;install -m755 "$wp" "$b/wireproxy";rm -rf "$b/.wpx"; }
start_warp(){ local b="$WARP/bin" s="$WARP/state" p pid;warp_tools;cd "$s";if [[ ! -s wgcf-account.toml ]];then "$b/wgcf" register --accept-tos >/dev/null;fi;chmod 600 wgcf-account.toml;"$b/wgcf" generate >/dev/null;chmod 600 wgcf-profile.conf;p="$(free_port 25354 25420)"||die no_free_warp_port;cat >"$SESSION/wireproxy.conf" <<EOF
WGConfig = $s/wgcf-profile.conf
[Socks5]
BindAddress = 127.0.0.1:$p
EOF
chmod 600 "$SESSION/wireproxy.conf";"$b/wireproxy" -n -c "$SESSION/wireproxy.conf" >/dev/null;env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1 OTCLIENT_TIBIA_RE_ROLE=wireproxy nohup "$b/wireproxy" -c "$SESSION/wireproxy.conf" >"$SESSION/wireproxy.log" 2>&1 </dev/null &pid=$!;echo "$pid">"$SESSION/wireproxy.pid";echo "$p">"$SESSION/warp-port";echo "$b/wireproxy">"$SESSION/wireproxy-bin";for _ in $(seq 1 40);do kill -0 "$pid" 2>/dev/null||die wireproxy_exited;listen "$p"&&break;sleep .25;done;owned "$pid" wireproxy "$b/wireproxy"||die wireproxy_ownership_failed;nosecret "$pid" wireproxy;listen "$p"||die wireproxy_not_listening;curl --socks5-hostname "127.0.0.1:$p" -fsS --max-time 15 https://www.cloudflare.com/cdn-cgi/trace|grep -Eq '^warp=(on|plus)$'||die warp_egress_not_verified; }

bootstrap(){ local m="$1" src home pkg d dn vp xv vnc xd pl c pid w pg meta wp;[[ "${RUNNER_NAME:-}" == synology-otclient-01 ]]||die wrong_runner;[[ "${GITHUB_REPOSITORY:-}" == blakinio/otclient ]]||die wrong_repository;[[ ! -e "$SESSION" ]]||die session_root_exists;pg="$(ps -o pgid= -p $$|tr -d ' ')";[[ "$pg" == "$$" ]]||die bootstrap_not_group_leader;src="$(source_pkg)"||die exact_source_missing;mkdir -p "$SESSION";chmod 700 "$SESSION";echo "$pg">"$SESSION/bootstrap-pgid";start_warp;wp="$(cat "$SESSION/warp-port")";xv="$(tool Xvfb)"||die xvfb_unavailable;vnc="$(tool x11vnc)"||die vnc_unavailable;xd="$(tool xdotool)"||die xdotool_unavailable;pl="$(find "$TOOL" -type f -name libproxychains.so.4 -print -quit 2>/dev/null||true)";[[ -n "$pl" ]]||die proxychains_unavailable;dn="$(free_display)"||die no_free_display;d=":$dn";vp="$(free_port 6082 6120)"||die no_free_vnc_port;home="$SESSION/home";pkg="$home/.local/share/CipSoft GmbH/Tibia/packages/Tibia";mkdir -p "$(dirname "$pkg")";cp -a --reflink=auto "$src" "$pkg";c="$pkg/bin/client";verify_client "$c";meta="$(dirname "$src")/../../launchermetadata.json";[[ ! -f "$meta" || -L "$meta" ]]||install -m600 "$meta" "$(dirname "$(dirname "$pkg")")/launchermetadata.json";cat >"$SESSION/proxychains.conf" <<EOF
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5 127.0.0.1 $wp
EOF
chmod 600 "$SESSION/proxychains.conf";env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1 OTCLIENT_TIBIA_RE_ROLE=xvfb HOME="$home" PATH="$TOOL/usr/bin:$TOOL/usr/sbin:/usr/bin:/bin" LD_LIBRARY_PATH="$TOOL/usr/lib/x86_64-linux-gnu:$TOOL/lib/x86_64-linux-gnu" XKB_CONFIG_ROOT="$TOOL/usr/share/X11/xkb" nohup "$xv" "$d" -screen 0 1920x1080x24 -xkbdir "$TOOL/usr/share/X11/xkb" -nolisten tcp -noreset >"$SESSION/xvfb.log" 2>&1 </dev/null &echo $!>"$SESSION/xvfb.pid";for _ in $(seq 1 60);do [[ -e /tmp/.X11-unix/X$dn ]]&&break;sleep .2;done;[[ -e /tmp/.X11-unix/X$dn ]]||die xvfb_socket_missing
env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1 OTCLIENT_TIBIA_RE_ROLE=vnc HOME="$home" DISPLAY="$d" nohup "$vnc" -display "$d" -rfbport "$vp" -forever -shared -viewonly -localhost -nopw -noxdamage >"$SESSION/vnc.log" 2>&1 </dev/null &echo $!>"$SESSION/vnc.pid";for _ in $(seq 1 60);do listen "$vp"&&break;sleep .2;done;listen "$vp"||die vnc_not_listening
(cd "$pkg";env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1 OTCLIENT_TIBIA_RE_ROLE=client HOME="$home" DISPLAY="$d" PATH="$TOOL/usr/bin:$TOOL/usr/sbin:/usr/bin:/bin" LD_LIBRARY_PATH="$pkg/bin/lib:$TOOL/usr/lib/x86_64-linux-gnu:$TOOL/usr/lib/x86_64-linux-gnu/libproxy:$TOOL/lib/x86_64-linux-gnu" QT_QUICK_BACKEND=software QT_XCB_GL_INTEGRATION=none XDG_DATA_DIRS="$TOOL/usr/share:/usr/share" FONTCONFIG_PATH="$TOOL/etc/fonts" FONTCONFIG_FILE="$TOOL/etc/fonts/fonts.conf" LD_PRELOAD="$pl" PROXYCHAINS_CONF_FILE="$SESSION/proxychains.conf" nohup "$c" >"$SESSION/client.log" 2>&1 </dev/null &echo $!>"$SESSION/client.pid")
pid="$(rpid client)";for _ in $(seq 1 100);do kill -0 "$pid" 2>/dev/null||die client_exited;w="$(window "$pid" "$d" "$xd"||true)";[[ -n "$w" ]]&&break;sleep .25;done;[[ -n "${w:-}" ]]||die client_window_missing;verify_client "$c";owned "$pid" client "$c"||die client_ownership_failed;nosecret "$pid" client;echo "$d">"$SESSION/display";echo "$w">"$SESSION/window";echo "$vp">"$SESSION/vnc-port";python3 - "$m" "$pid" "$pg" "$d" "$w" "$vp" <<'PY'
import json,sys
o,p,g,d,w,v=sys.argv[1:];json.dump({'pid':int(p),'process_group_id':int(g),'display':d,'window_identity':'x11-window:'+w,'remote_view_endpoint':'127.0.0.1:'+v,'remote_view_mapping':'PROVEN','state':'UNKNOWN'},open(o,'w'))
PY
}
probe(){ local m="$1" pid d w vp c xd r p b;[[ -d "$SESSION" ]]||die session_missing;pid="$(rpid client)";d="$(cat "$SESSION/display")";vp="$(cat "$SESSION/vnc-port")";c="$SESSION/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client";verify_client "$c";owned "$pid" client "$c"||die client_ownership_failed;kill -0 "$pid"||die client_dead;nosecret "$pid" client;for r in xvfb vnc wireproxy;do p="$(rpid "$r")";b=;[[ "$r" != wireproxy ]]||b="$(cat "$SESSION/wireproxy-bin")";owned "$p" "$r" "$b"||die "${r}_ownership_failed";kill -0 "$p"||die "${r}_dead";nosecret "$p" "$r";done;listen "$vp"||die vnc_not_listening;listen "$(cat "$SESSION/warp-port")"||die wireproxy_not_listening;xd="$(tool xdotool)"||die xdotool_unavailable;w="$(window "$pid" "$d" "$xd")"||die client_window_missing;echo "$w">"$SESSION/window";python3 - "$m" "$pid" "$d" "$w" "$vp" <<'PY'
import json,sys
o,p,d,w,v=sys.argv[1:];json.dump({'pid':int(p),'display':d,'window_identity':'x11-window:'+w,'remote_view_endpoint':'127.0.0.1:'+v,'remote_view_mapping':'PROVEN','state':'UNKNOWN'},open(o,'w'))
PY
}
rollback(){ local pg="$1" r p dn;[[ -d "$SESSION" ]]||return 0;[[ "$(cat "$SESSION/bootstrap-pgid" 2>/dev/null||true)" == "$pg" ]]||die rollback_pgid_mismatch;for r in client xvfb vnc wireproxy;do p="$(rpid "$r")";[[ -z "$p" || ! -e /proc/$p ]]||die rollback_role_still_alive;done;dn="$(sed 's/^://' "$SESSION/display" 2>/dev/null||true)";if [[ -n "$dn" && -e /tmp/.X$dn-lock ]];then p="$(tr -cd '0-9' </tmp/.X$dn-lock 2>/dev/null||true)";[[ -z "$p" || ! -e /proc/$p ]]||die rollback_x11_owner_alive;rm -f "/tmp/.X$dn-lock" "/tmp/.X11-unix/X$dn";elif [[ -n "$dn" && -e /tmp/.X11-unix/X$dn ]];then die rollback_x11_ambiguous;fi;rm -rf --one-file-system "$SESSION"; }

contract_test "$@" || true
case "${1:-}" in bootstrap)[[ $# == 2 ]]||die usage;bootstrap "$2";;probe)[[ $# == 2 ]]||die usage;probe "$2";;rollback)[[ $# == 2 ]]||die usage;rollback "$2";;*)die usage;;esac
