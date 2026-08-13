---
task_id: OTC-20260813-official-client-re-continuation
status: investigating
track_id: official-client-re
alias: OTCLIENT-TIBIA-RE
branch: ci/OTC-20260813-official-client-re-continuation
base_branch: main
pr: 289
task_kind: runtime-research
phase: live-state-revalidation
risk: medium
runtime_platform: native_linux_only
owned_paths:
  - .github/workflows/tibia-official-client-re-*.yml
  - .github/scripts/tibia-official-client-re-*
  - tests/tools/test_tibia_official_client_re_*.py
  - docs/agents/tasks/active/OTC-20260813-official-client-re-continuation.md
  - docs/agents/evidence/OTC-20260813-official-client-re/**
modules_touched:
  - official-client-re workflow and evidence only
reuses:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-login-recovery-import.md
  - closed PR 48 repository-owned official-client scripts as versioned leads only
  - PR 283 runtime bridge after exact-SHA validation
depends_on:
  - synology-otclient-01 availability
blocks: []
cross_repository_tasks: []
---

# OTC-20260813 — Official Linux client RE continuation

## Objective

Continue Track A from current `blakinio/otclient` durable state: establish an
isolated native-Linux official-client runtime on `synology-otclient-01`, recover
structural `IN_GAME`, correlate the stable bridge, and proceed through player,
map, creature, inventory/container, protocol/action and OTBM evidence gates.

## Runtime ownership

```yaml
runner: synology-otclient-01
subject: official native Linux Tibia client only
state_directory: /home/runner/_work/_otclient_tibia_re_state
compatibility_state_directory_while_legacy_runner_image_is_live: /work/_otclient_tibia_re_state
display: :98
warp_socks_port: 25354
bridge_socket: <state_directory>/runtime/otclient-tibia-re.sock
process_marker: OTCLIENT_TIBIA_RE_TRACK=official-client-re
container_names: none
```

Track B owns its own branch, PR, workflow, runtime, display, ports and state.
This task never reads or mutates them and never uses broad process or Docker
cleanup.

## Acceptance inventory

- [x] Live Track A namespace is proven isolated on the dedicated runner.
- [x] Exact current official Linux client version, size and SHA are verified.
- [x] Official client is reconstructed and launched normally through verified WARP.
- [ ] Login recovery consumes secrets only in the approved Actions step and does not persist them.
- [ ] `IN_GAME` is proven from decoded structural state, not OCR/pixels/sockets.
- [ ] Bridge session status is correlated with decoded world state.
- [ ] Authoritative player position and one reversible movement transition are proven.
- [ ] Subsequent capability evidence is persisted with exact run/job/head/SHA references.

## Context checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-13T16:05:00+02:00
head: 7a9d4a4ccf0411466540621556ec846220b37c46
branch: ci/OTC-20260813-official-client-re-continuation
pr: 289
status: paused_by_owner
context_routes:
  - official-client-re
  - native-linux-runtime
owned_paths:
  - .github/workflows/tibia-official-client-re-*.yml
  - .github/scripts/tibia-official-client-re-*
  - tests/tools/test_tibia_official_client_re_*.py
  - docs/agents/tasks/active/OTC-20260813-official-client-re-continuation.md
  - docs/agents/evidence/OTC-20260813-official-client-re/**
proven:
  - official native-Linux client version 15.32.df7b29, size 51965216, SHA256 e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  - isolated Track A state, owned WARP SOCKS 127.0.0.1:25354, display :98 and process marker are live on synology-otclient-01
  - official runtime reconstruction succeeded in run 31702126665
  - isolated private toolroot succeeded in run 31710205236
  - normal official-client launch succeeded in run 31707899241 job 94473004427 with owned display and no unresolved libraries
  - lavapipe/Vulkan startup is usable for the official client; private Xvfb and XKB startup are usable
  - login runs 31713018398, 31713638527 and 31713902095 proved the live exact client process and that both credential fields materially changed without persisting secrets
derived:
  - socket counts alone are bootstrap/session indicators and are not structural IN_GAME evidence
unknown:
  - current structural session state
  - whether the exact historically proven explicit coordinate sequence transitions this isolated runtime from Account Login to Select Character
  - decoded current-world records and authoritative player position
first_failure:
  marker: prior transition comparison used changed XWD bytes rather than the historical ImageMagick AE changed-pixel unit
  evidence: runs through 31715206847 remain valid for process, click, field-mutation and transport observations, but their numeric transition values cannot be compared directly to the historical >45000 pixel threshold
rejected_hypotheses:
  - missing WARP, missing lavapipe, missing Xvfb/XKB, missing private toolroot, or absent current official client: rejected by current Track A runs
  - treating proxied socket counts, pixels, or a visible window as IN_GAME proof: rejected by canonical structural-evidence requirement
  - invoking private proxychains4 without a global library path: rejected because the wrapper hard-codes the runner-global libproxychains location and exits before client startup
changed_paths:
  - .github/scripts/tibia-official-client-re-reconstruct.py
  - .github/workflows/tibia-official-client-re-identity.yml
  - .github/workflows/tibia-official-client-re-live-state.yml
  - .github/workflows/tibia-official-client-re-reconstruct.yml
  - .github/workflows/tibia-official-client-re-toolroot.yml
  - docs/agents/tasks/active/OTC-20260813-official-client-re-continuation.md
  - tests/tools/test_tibia_official_client_re_reconstruct.py
validation:
  - command: Track A official Linux client reconstruction run 31702126665
    result: PASS
  - command: Track A official-client RE toolroot run 31710205236
    result: PASS
  - command: Track A official native Linux launch run 31707899241 job 94473004427
    result: PASS
  - command: Track A structural login run 31713018398 job 94490585180
    result: FAIL_FOR_LOGIN_TRANSITION
    evidence: exact client/process/WARP/lavapipe gates passed; field changes 12569; login transition 5231 < 45000; no structural IN_GAME claim
  - command: Track A structural login run 31713638527 job 94492697675
    result: FAIL_FOR_LOGIN_TRANSITION
    evidence: faithful explicit coordinate baseline; field changes 4654; transition 5259 < 45000; no structural IN_GAME claim
  - command: Track A structural login run 31713902095 job 94493601193
    result: FAIL_FOR_LOGIN_TRANSITION
    evidence: faithful explicit coordinate baseline plus non-secret telemetry; transition 4174 < 45000; local SOCKS max stayed 2; process I/O deltas are non-attributable due rendering
  - command: Track A structural login run 31714150143 job 94494444800
    result: INCONCLUSIVE_FOR_VERSIONED_BASELINE
    evidence: pointer coordinates exactly matched the three historical coordinates, but key/type delivery differed from the versioned successful workflow
  - command: Track A structural login run 31714475543 job 94495543093
    result: FAIL_FOR_VERSIONED_INPUT_BASELINE
    evidence: exact versioned key/type and explicit-click implementation; coordinates matched; transition 4785 < 45000; no post-submit SOCKS increase; no structural IN_GAME claim
  - command: Track A structural login run 31714821056 job 94496738127
    result: FAIL_FOR_FRESH_HOME_BASELINE
    evidence: fresh client HOME/XDG config was used and removed; versioned input delivery; transition 4813 < 45000; no structural IN_GAME claim
  - command: Track A structural login run 31715045843 job 94497518892
    result: INVALID_PRELOGIN_VALIDATION
    evidence: fresh-home 1280x800 attempt stopped at the owned-client marker pipeline because tr|grep returned SIGPIPE under pipefail; no secrets were injected
  - command: Track A structural login run 31715206847 job 94498079465
    result: FAIL_FOR_DISPLAY_ALIGNED_BASELINE
    evidence: pipe-safe marker checks; fresh HOME/XDG; historical display/timing; versioned input delivery; transition 4483 < 45000; no structural IN_GAME claim
  - command: Track A structural login run 31715484884 job 94499024983
    result: INVALID_PRELOGIN_TRANSPORT_VARIANT
    evidence: private proxychains4 wrapper exited before client startup with 'couldnt locate libproxychains.so.4'; no secrets were injected and no runner-global library path was modified
  - command: python -m unittest tests.tools.test_tibia_official_client_re_reconstruct tests.tools.test_tibia_official_client_re_xwd_diff
    result: PASS
    evidence: six tests, including XWD changed-pixel rather than changed-byte semantics
  - command: Track A structural login run 31716060387 job 94500972188
    result: INVALID_COMPARATOR_EXECUTION
    evidence: normal client start and credential injection reached the comparator, but this minimal workflow had no checkout, so the helper path was absent; no numeric transition result was produced
  - command: Track A structural login run 31716296567 job 94501758491
    result: FAIL_FOR_PIXEL_ALIGNED_BASELINE
    evidence: pinned checkout made the versioned XWD changed-pixel comparator available; exact 1280x800 fresh-home explicit-click sequence reached the official client with the three historical pointer coordinates, but changed pixels were 1624 < 45000. No structural IN_GAME claim was made.
  - command: python -c "import yaml; yaml.safe_load(open('.github/workflows/tibia-official-client-re-login.yml'))"
    result: PASS
    evidence: workflow YAML remained syntactically parseable after adding the bounded static auth-state trace.
  - command: python -m unittest tests.tools.test_tibia_official_client_re_reconstruct tests.tools.test_tibia_official_client_re_xwd_diff
    result: PASS
    evidence: six tests passed after adding the auth trace workflow change.
  - command: Track A structural login run 31716923856 job 94503872080
    result: INCONCLUSIVE_FOR_PRELOGIN_GDB_TRACE
    evidence: the version-pinned trace armed before credential input, but emitted no state label and the pixel transition remained 1846 < 45000. Repository-owned recovery evidence says a pre-login GDB attach changes Qt/UI timing, so this run does not establish that the submit handler was not reached; the trace is disabled before the next live attempt.
  - command: Track A structural login run 31717327457 job 94505245329
    result: FAIL_FOR_RETURN_THEN_BUTTON_SUBMIT_VARIANT
    evidence: without pre-login GDB, Return was sent after the verified credential-field mutation; after four seconds the same changed-pixel comparator did not transition, so the exact historical button coordinate was used as fallback. The final value was 1632 < 45000, with no structural IN_GAME claim.
blockers: []
paused_by: owner request at 2026-08-13T16:05:00+02:00
next_action: do not run another client experiment until the owner explicitly resumes Track A; on resume, revalidate the current repository/PR/runner state before selecting a new non-GDB, non-OCR input-delivery diagnostic
```
