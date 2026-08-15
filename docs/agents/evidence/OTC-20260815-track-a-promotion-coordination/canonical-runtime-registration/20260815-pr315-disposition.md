# PR #315 canonical runtime registration — coordinator disposition

Coordinator task: `OTC-20260815-track-a-promotion-coordination`  
Source PR: `#315`  
Source final handoff head: `129b440195439e7fd813e548d55c76a23ede88a7`  
Semantic code head: `60c19331703d68fa455b14227c8a9aad8a76d26f`  
Semantic run/job: `31910131938` / `95073832354`  
Source CI: `31910340819`  
`CI / Required`: `95074702295` SUCCESS  
Review threads: `0`

## Disposition

`ACCEPT_WITH_EDITS`

The source is accepted only as bounded current-state evidence. Research implementation remains unmerged. The first-pass claim that RFB desktop-name text proved exact `6082 -> :98` mapping was correctly rejected and superseded before promotion.

## Promoted FACT

```yaml
semantic_result: PERSISTENT_DISPLAY_NO_LIVE_CLIENT
persistent_x11_socket_set:
  - ":98"
display_98_present: true
tibia_window_count_all: 0
tibia_window_count_visible: 0
global_exact_client_process_count: 0
exact_window_candidate_count: 0
rfb_6082_reachable: true
rfb_protocol_version: "003.008"
rfb_framebuffer: "1920x1080"
rfb_desktop_name_supports_display_98: true
```

The final probe covered both visible and hidden/minimized exact-title X11 windows and a global `/proc/*/exe` census. A process counted as exact only after matching executable size `51965216` and SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`; process-start ticks and hashed boot ID were available for positive identities. No exact process existed at observation time.

## Promoted interpretation

- historical successful Track A login/world evidence on `:98` remains valid;
- that historical exact-client process/session is no longer running now;
- at final observation time there was no exact-fenced official-client process anywhere visible through the runner namespace, not merely no visible Tibia window;
- persistent X11 `:98` and RFB `6082` infrastructure survive independently of a live Tibia process.

## Preserved INFERENCE / UNKNOWN

```yaml
rfb_desktop_name_supports_6082_to_98_mapping: INFERENCE_SUPPORTING_EVIDENCE
exact_6082_backend_display: UNKNOWN
display_98_is_canonical: false
current_canonical_live_pid: none_observed
current_live_world_session: none_observed
```

Descriptive RFB desktop-name text is not authoritative service configuration and cannot promote exact backend mapping to FACT.

## Safety evidence

The final run emitted that no framebuffer was exported, no process environment/cmdline was read, no ptrace was used and no input was sent. No client launch/stop/login, signals, Docker/host control, Track B access or PR #303 `:115` mutation occurred.

## Programme consequence

There is currently no live exact-client session to register/reuse. Canonical-session **initial creation** is therefore a separate future state transition. It must not be represented as ordinary reuse of an already-registered runtime and must remain fail-closed until Track A has a reviewed creation/bootstrap mechanism compatible with the final authoritative lease supervisor.

PR #311 stays Draft while active PR #316 supervisor remediation and that bootstrap boundary remain unresolved. `:98` remains a candidate namespace only.
