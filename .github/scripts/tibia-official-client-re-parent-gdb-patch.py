#!/usr/bin/env python3
"""Patch materialized Track-A helper for Yama-safe parent tracing."""
from pathlib import Path
import sys


def replace_between(text, start, end, replacement, label):
    if text.count(start) != 1:
        raise SystemExit(f"{label}: start count={text.count(start)}")
    if text.count(end) != 1:
        raise SystemExit(f"{label}: end count={text.count(end)}")
    a = text.index(start)
    b = text.index(end, a + len(start))
    return text[:a] + replacement.rstrip() + "\n\n" + text[b:]


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{label}: anchor count={n}")
    return text.replace(old, new, 1)


if len(sys.argv) != 2:
    raise SystemExit("usage: parent-gdb-patch.py EFFECTIVE_HELPER")
path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")

old = '"$td/usr/bin/xdotool"'
new = (
    'env LD_LIBRARY_PATH="$td/usr/lib/x86_64-linux-gnu:'
    '$td/usr/lib/x86_64-linux-gnu/libproxy:$td/lib/x86_64-linux-gnu" '
    '"$td/usr/bin/xdotool"'
)
xdotool_count = text.count(old)
if xdotool_count < 10:
    raise SystemExit(f"xdotool invocation count too low: {xdotool_count}")
text = text.replace(old, new)
if text.count(new) != xdotool_count:
    raise SystemExit("xdotool replacement count mismatch")

parent_gdb = r"""generation_package() {
  local gen="$1"
  printf '%s/home-gen-%s/.local/share/CipSoft GmbH/Tibia/packages/Tibia\n' "$(run_root)" "$gen"
}

make_gdb_script() {
  local out="$1" launcher="$2" client="$3" records="$4" pid_out="$5" pie_out="$6"
  python3 - "$out" "$launcher" "$client" "$records" "$pid_out" "$pie_out" "$MAP_CAPTURE_OFFSET" <<'PY'
import os, shlex, sys
out, launcher, client, records, pid_out, pie_out, offset = sys.argv[1:]
client = os.path.realpath(client)
gdb_text = f'''set pagination off
set confirm off
set startup-with-shell off
set disable-randomization off
set follow-exec-mode same
handle SIGTERM pass nostop noprint
file /bin/bash
unset environment LD_LIBRARY_PATH
unset environment LD_PRELOAD
unset environment PROXYCHAINS_CONF_FILE
unset environment RUNNER_TRACKING_ID
unset environment TIBIA_TEST_EMAIL
unset environment TIBIA_TEST_PASSWORD
set args {shlex.quote(launcher)}
catch exec
run
delete
python
import gdb, os, struct, time
inf = gdb.selected_inferior()
pid = int(inf.pid)
expected = os.path.realpath({client!r})
actual = os.path.realpath(f'/proc/{{pid}}/exe')
if actual != expected:
    raise gdb.GdbError(f'parent tracer exec mismatch: {{actual}} != {{expected}}')
line = None
for _ in range(60):
    try:
        for row in open(f'/proc/{{pid}}/maps', encoding='utf-8', errors='replace'):
            fields = row.rstrip('\\n').split(maxsplit=5)
            if len(fields) >= 6 and 'r-xp' in fields[1] and os.path.realpath(fields[5]) == expected:
                line = fields
                break
    except OSError:
        pass
    if line:
        break
    time.sleep(0.05)
if not line:
    raise gdb.GdbError('exact client mapping not found after exec')
start = int(line[0].split('-',1)[0], 16)
file_off = int(line[2], 16)
bias = start - file_off
open({pid_out!r}, 'w', encoding='ascii').write(str(pid) + '\\n')
open({pie_out!r}, 'w', encoding='ascii').write(f'0x{{bias:x}}\\n')
records_path = {records!r}
offset_value = int({offset!r}, 0)
class MapBP(gdb.Breakpoint):
    def __init__(self):
        super().__init__('*0x%x' % (bias + offset_value))
    def stop(self):
        try:
            rsp = int(gdb.parse_and_eval('$rsp'))
            order = int(gdb.parse_and_eval('$rbp')) & 0xffffffff
            x, y, z = struct.unpack('<III', bytes(inf.read_memory(rsp + 0x88, 12)))
            if 0 < x < 100000 and 0 < y < 100000 and z < 32 and order < 128:
                with open(records_path, 'a', encoding='ascii') as f:
                    f.write(f'{{time.monotonic_ns()}}\\t{{x}}\\t{{y}}\\t{{z}}\\t{{order}}\\n')
                    f.flush()
        except Exception:
            pass
        return False
MapBP()
gdb.write(f'TRACK_A_PARENT_GDB_CHILD_READY pid={{pid}} pie=0x{{bias:x}} offset=0x{{offset_value:x}}\\n')
end
continue
'''
open(out, 'w', encoding='utf-8').write(gdb_text)
PY
  chmod 600 "$out"
}
"""
text = replace_between(text, "make_gdb_script() {", "prepare_generation() {",
                       parent_gdb, "parent-gdb-generator")

prepare = r"""prepare_generation() {
  require_context
  local gen="$1" root package client td tool_path tool_lib proxy_lib vk_icd swrast dri
  local gdir launcher gdb gp pid window baseline
  root="$(run_root)"; package="$(generation_package "$gen")"; client="$package/bin/client"; td="$(toolroot)"
  tool_path="$td/usr/bin:$td/usr/sbin:/usr/bin:/bin"
  # Preserve the runner support-loader fence validated by the source materializer:
  # /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/libproxy
  tool_lib="$td/usr/lib/x86_64-linux-gnu:$td/usr/lib/x86_64-linux-gnu/libproxy:$td/lib/x86_64-linux-gnu"
  proxy_lib="$(find "$td" -type f -name libproxychains.so.4 -print -quit)"
  vk_icd="$(find "$td/usr/share/vulkan/icd.d" -type f -name 'lvp_icd*.json' -print -quit)"
  swrast="$(find "$td" \( -type f -o -type l \) -name swrast_dri.so -print -quit)"
  [[ -n "$proxy_lib" && -n "$vk_icd" && -n "$swrast" ]] || die software_or_proxy_dependency_missing
  dri="$(dirname "$swrast")"
  [[ -d "$package" && ! -L "$package" ]] || die physical_canonical_package_missing
  verify_client "$client"
  printf 'TRACK_A_RUNTIME_PHYSICAL_CANONICAL_PACKAGE_LAUNCH generation=%s path=%s\n' "$gen" "$package"
  role_owned "$(read_pid xvfb)" xvfb || die xvfb_not_owned
  role_owned "$(read_pid socks-relay)" socks-relay || die relay_not_owned

  gdir="$root/generation-$gen"
  mkdir -p "$gdir" "$root/home-gen-$gen"
  : >"$gdir/map-records.tsv"
  rm -f "$gdir/pid.txt" "$gdir/pie-base.txt"

  launcher="$gdir/client-launcher.sh"
  cat >"$launcher" <<EOF
#!/usr/bin/env bash
set -Eeuo pipefail
unset RUNNER_TRACKING_ID TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD
export OTCLIENT_TIBIA_RE_TRACK=official-client-re
export OTCLIENT_TIBIA_RE_TASK="$TASK_ID"
export OTCLIENT_TIBIA_RE_RUN_ID="$GITHUB_RUN_ID"
export OTCLIENT_TIBIA_RE_ROLE="client-gen-$gen"
export HOME="$root/home-gen-$gen"
export DISPLAY="$TRACK_DISPLAY"
export PATH="$tool_path"
export LD_LIBRARY_PATH="$package/bin/lib:$tool_lib"
export LIBGL_ALWAYS_SOFTWARE=1
export LIBGL_DRIVERS_PATH="$dri"
export QT_QUICK_BACKEND=software QT_XCB_GL_INTEGRATION=none
export XDG_DATA_DIRS="$td/usr/share:/usr/share"
export FONTCONFIG_PATH="$td/etc/fonts"
export FONTCONFIG_FILE="$td/etc/fonts/fonts.conf"
export LD_PRELOAD="$proxy_lib"
export PROXYCHAINS_CONF_FILE="$root/proxychains.conf"
cd "$package"
exec "$client" >"$gdir/client.log" 2>&1 </dev/null
EOF
  chmod 700 "$launcher"

  gdb="$td/usr/bin/gdb"; [[ -x "$gdb" ]] || die gdb_unavailable
  make_gdb_script "$gdir/world.gdb" "$launcher" "$client" "$gdir/map-records.tsv" "$gdir/pid.txt" "$gdir/pie-base.txt"
  env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD -u LD_PRELOAD -u PROXYCHAINS_CONF_FILE \
    OTCLIENT_TIBIA_RE_TRACK=official-client-re OTCLIENT_TIBIA_RE_TASK="$TASK_ID" \
    OTCLIENT_TIBIA_RE_RUN_ID="$GITHUB_RUN_ID" OTCLIENT_TIBIA_RE_ROLE="observer-gen-$gen" \
    HOME="$root/home" PATH="$tool_path" LD_LIBRARY_PATH="$tool_lib" \
    nohup "$gdb" -q -nx -batch -x "$gdir/world.gdb" >"$gdir/gdb.log" 2>&1 </dev/null &
  gp=$!; printf '%s\n' "$gp" >"$(pidfile "observer-gen-$gen")"

  for _ in $(seq 1 120); do
    if [[ -s "$gdir/pid.txt" && -s "$gdir/pie-base.txt" ]]; then break; fi
    kill -0 "$gp" 2>/dev/null || { tail -n 80 "$gdir/gdb.log" >&2 || true; die parent_observer_exited_before_client; }
    sleep .1
  done
  [[ -s "$gdir/pid.txt" && -s "$gdir/pie-base.txt" ]] || die parent_observer_child_metadata_timeout
  pid="$(tr -cd '0-9' <"$gdir/pid.txt")"
  [[ -n "$pid" ]] || die parent_observer_child_pid_missing
  printf '%s\n' "$pid" >"$(pidfile "client-gen-$gen")"

  role_owned "$gp" "observer-gen-$gen" "$gdb" || die observer_ownership_failed
  role_owned "$pid" "client-gen-$gen" "$client" || die client_ownership_failed
  assert_no_secret_env "$gp" "observer-gen-$gen"
  assert_no_secret_env "$pid" "client-gen-$gen"
  [[ "$(awk '/^TracerPid:/{print $2}' "/proc/$pid/status")" == "$gp" ]] || die parent_observer_not_tracing_child
  verify_client "$client"

  window="$(resolve_window "$pid")" || { tail -n 120 "$gdir/client.log" >&2 || true; die "client_gen_${gen}_window_missing"; }
  env LD_LIBRARY_PATH="$tool_lib" DISPLAY="$TRACK_DISPLAY" "$td/usr/bin/xdotool" windowsize "$window" 1020 650 >/dev/null 2>&1 || true
  env LD_LIBRARY_PATH="$tool_lib" DISPLAY="$TRACK_DISPLAY" "$td/usr/bin/xdotool" windowmove "$window" 0 0 >/dev/null 2>&1 || true
  printf '%s\n' "$window" >"$gdir/window.id"

  sleep 5
  baseline="$(wc -l <"$gdir/map-records.tsv")"
  printf '%s\n' "$baseline" >"$gdir/baseline-count.txt"
  [[ "$baseline" == 0 ]] || die "logged_out_worldmap_noise_gen_$gen"
  printf 'TRACK_A_NO_STIMULUS_BASELINE generation=%s records=0\n' "$gen"
  printf 'TRACK_A_GENERATION_PREPARED generation=%s pid=%s pie=%s observer=%s parent_tracer=true\n' \
    "$gen" "$pid" "$(cat "$gdir/pie-base.txt")" "$gp"
}
"""
text = replace_between(text, "prepare_generation() {", "login_generation() {",
                       prepare, "parent-gdb-prepare")

text = replace_once(
    text,
    'email="$TIBIA_TEST_EMAIL"; password="$TIBIA_TEST_PASSWORD"; client="$(package_dir)/bin/client"',
    'email="$TIBIA_TEST_EMAIL"; password="$TIBIA_TEST_PASSWORD"; client="$(generation_package "$gen")/bin/client"',
    "login-client-path",
)
text = replace_once(
    text,
    'root="$(run_root)"; td="$(toolroot)"; gdir="$root/generation-$gen"; client="$(package_dir)/bin/client"',
    'root="$(run_root)"; td="$(toolroot)"; gdir="$root/generation-$gen"; client="$(generation_package "$gen")/bin/client"',
    "verify-client-path",
)

stop = r"""stop_generation() {
  require_context
  local gen="$1" root td client gp pid
  root="$(run_root)"; td="$(toolroot)"; client="$(generation_package "$gen")/bin/client"
  gp="$(read_pid "observer-gen-$gen" 2>/dev/null || true)"
  pid="$(read_pid "client-gen-$gen" 2>/dev/null || true)"

  if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
    role_owned "$pid" "client-gen-$gen" "$client" || die refuse_foreign_client_cleanup
    kill -CONT "$pid" 2>/dev/null || true
    kill -TERM "$pid" 2>/dev/null || true
    for _ in $(seq 1 80); do kill -0 "$pid" 2>/dev/null || break; sleep .1; done
    kill -0 "$pid" 2>/dev/null && die client_cleanup_timeout
  fi

  if [[ -n "$gp" ]] && kill -0 "$gp" 2>/dev/null; then
    role_owned "$gp" "observer-gen-$gen" "$td/usr/bin/gdb" || die refuse_foreign_observer_cleanup
    for _ in $(seq 1 40); do kill -0 "$gp" 2>/dev/null || break; sleep .1; done
    if kill -0 "$gp" 2>/dev/null; then
      kill -TERM "$gp" 2>/dev/null || true
      for _ in $(seq 1 40); do kill -0 "$gp" 2>/dev/null || break; sleep .1; done
    fi
    kill -0 "$gp" 2>/dev/null && die observer_cleanup_timeout
  fi
  printf 'TRACK_A_GENERATION_STOPPED generation=%s parent_tracer=true\n' "$gen"
}
"""
text = replace_between(text, "stop_generation() {", "compare_generations() {",
                       stop, "parent-gdb-stop")

for forbidden in ("ptrace_scope_not_zero", "attach {pid}"):
    if forbidden in text:
        raise SystemExit(f"attach-era fragment remains: {forbidden}")
for required in ("set disable-randomization off", "TRACK_A_PARENT_GDB_CHILD_READY", "generation_package"):
    if required not in text:
        raise SystemExit(f"required fragment missing: {required}")

path.write_text(text, encoding="utf-8")
print(f"TRACK_A_PARENT_GDB_PATCH_APPLIED=true xdotool_invocations={xdotool_count} host_ptrace_scope_unchanged=true aslr_preserved=true")
