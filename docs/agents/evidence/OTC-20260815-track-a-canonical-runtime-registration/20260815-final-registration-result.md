# Track A canonical runtime candidate registration — final read-only result

Task: `OTC-20260815-track-a-canonical-runtime-registration`  
PR: `#315`  
Final semantic code head: `60c19331703d68fa455b14227c8a9aad8a76d26f`  
Run: `31910131938`  
Job: `95073832354`  
Runner: `synology-otclient-01`  
Conclusion: `SUCCESS`

## Purpose

Determine whether the persistent Track A display candidate `:98` currently hosts a live official Linux Tibia client matching the exact Track A fence, without mutating the runtime.

Exact fence:

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

## Final semantic result — FACT

```text
TRACK_A_CANONICAL_REGISTRATION_RESULT=PERSISTENT_DISPLAY_NO_LIVE_CLIENT
TRACK_A_CANONICAL_REGISTRATION_X11_DISPLAYS=:98
TRACK_A_CANONICAL_REGISTRATION_DISPLAY98_PRESENT=true
TRACK_A_CANONICAL_REGISTRATION_TIBIA_WINDOWS_ALL=0
TRACK_A_CANONICAL_REGISTRATION_TIBIA_WINDOWS_VISIBLE=0
TRACK_A_CANONICAL_REGISTRATION_EXACT_PROCESSES_GLOBAL=0
TRACK_A_CANONICAL_REGISTRATION_EXACT_WINDOW_CANDIDATES=0
TRACK_A_CANONICAL_REGISTRATION_RFB_REACHABLE=true
TRACK_A_CANONICAL_REGISTRATION_RFB_NAME_SUPPORTS_DISPLAY98=true
TRACK_A_CANONICAL_REGISTRATION_6082_BACKEND_DISPLAY=UNKNOWN
TRACK_A_CANONICAL_REGISTRATION_FRAMEBUFFER_EXPORTED=false
TRACK_A_CANONICAL_REGISTRATION_PROCESS_ENV_READ=false
TRACK_A_CANONICAL_REGISTRATION_PROCESS_CMDLINE_READ=false
TRACK_A_CANONICAL_REGISTRATION_PTRACE_USED=false
TRACK_A_CANONICAL_REGISTRATION_INPUT_SENT=false
```

The sanitized JSON result additionally records:

```yaml
persistent_x11_displays:
  - ":98"
display_98_present: true
tibia_window_count_all: 0
tibia_window_count_visible: 0
global_exact_client_processes: []
candidates: []
rfb_6082:
  reachable: true
  protocol_version: "003.008"
  width: 1920
  height: 1080
  security_types_hex: "01"
  desktop_name_sha256: f8a34765f47247e9744e8b1fe308c60fd3a4f582dbddd8c586b8e080d62e9cd6
  desktop_name_references_display_98: true
exact_6082_backend_display: UNKNOWN
display_98_is_canonical: false
read_only: true
```

## Interpretation

### FACT

- the persistent X11 display socket `:98` exists;
- no X11 window named exactly `Tibia` exists on `:98`, whether visible or hidden/minimized;
- a global `/proc/*/exe` census found **zero currently running processes** matching the exact fenced client size and SHA;
- therefore the previously successful historical Track A live client/session is **not currently running** on this runner at the observation time;
- host-facing `6082` still provides RFB metadata with a `1920x1080` framebuffer;
- the RFB desktop name, inspected only in memory and never printed raw, contains a pattern supporting display `98`;
- no framebuffer payload, process environment, command line, credentials, ptrace attach, signal or input was used.

### INFERENCE

```yaml
6082_backend_is_likely_display_98: HIGH_CONFIDENCE_SUPPORTING_EVIDENCE
```

The RFB desktop name explicitly referencing 98 strengthens the earlier display-candidate inference, but server desktop names are descriptive metadata rather than authoritative service configuration. Exact `6082 -> :98` backend mapping therefore remains `UNKNOWN`.

### NOT PROVEN / CURRENTLY FALSE

```yaml
display_98_is_current_canonical_live_runtime: false
current_exact_live_client_pid: none_observed
current_live_world_session: none_observed
exact_6082_backend_display: UNKNOWN
```

This result does **not** mean the historical login evidence was wrong. It means the historical live process/session no longer exists now.

## Superseded first-pass detail

Initial read-only run `31909992524` correctly found no visible Tibia window, but its result field overclaimed `exact_6082_backend_display=PROVEN_98` from desktop-name text alone and did not census hidden windows/global exact-client processes. That overclaim was rejected before promotion. The final run above supersedes it with fail-closed mapping classification and a full read-only process census.

## Consequence for Track A

There is currently no live exact-client session available to register/reuse. After the canonical-live governance/lease supervisor chain is fully promoted, Track A must create or reacquire one canonical persistent session under authoritative controller lease, then perform a fresh identity registration (PID + process-start identity + exact fence + display/window + state) before subsequent mutation/reuse.

This Draft does not authorize that mutation and does not start/login the client.
