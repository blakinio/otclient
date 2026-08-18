# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — replacement-agent handoff

Task: `OTC-20260818-native-login-to-ingame-e2e`  
Branch: `runtime/OTC-20260818-native-login-to-ingame-e2e-v3`  
PR: `#528`  
Alias: `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME`  
Prompt contract after this handoff: `v4.0.0`

This document is a durable recovery checkpoint. Live repository/controller-plane state always wins over this snapshot.

## Repository checkpoint

Last verified `main` while preparing this handoff:

```text
ebbb36f50076ff4072c7218e302614c1dfea00b1
```

PR #528 remained open, Draft and mergeable. It is the active native-login PR and should be continued rather than replaced unless fresh live state proves it terminal or unusable.

The temporary `tibia-official-client-re-native-login-update-package.yml` workflow was retired before this handoff. The PR has no remaining task-specific `native-login-*.yml` physical workflow in its net changed-file set, preventing a replacement-session synchronization from blindly re-triggering an obsolete package mutation.

## Last physical/runtime facts

### noVNC

```text
run=32138989357
job=95717041668
DISPLAY=:99
PID=30067
XID=12582929
RAW_XRES_VIEWABLE_1920X1080=true
RFB=PASS
WEBSOCKET=PASS
```

The viewer subsequently showed the real Tibia client. The black-screen root cause class is persisted in the VNC evidence: verify the active DISPLAY/window with raw XRes, then bind x11vnc -> websockify -> host 6082. `xdotool --pid` is not authoritative absence evidence.

### obsolete client gate

User-visible sanitized message:

```text
Your client version is too old.
Restart Tibia to update your client.
```

Obsolete binary:

```text
version=15.32.df7b29
size=51965216
sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Do not attempt another login with it.

### last-known official current manifest

Read-only probe:

```text
run=32140385842
job=95721374178
packed_sha256=1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked_sha256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
unpacked_size=52109920
version_strings=15.32,11.25
```

Refetch the official manifest before mutation; this is not a timeless target.

### canonical teardown

```text
run=32141408237
job=95724675001
TRACK_A_CANONICAL_TEARDOWN=PASS
TRACK_A_CANONICAL_TEARDOWN_RUNTIME_GONE=true
TRACK_A_CANONICAL_TEARDOWN_REGISTRATION_ABSENT=true
TRACK_A_CANONICAL_TEARDOWN_LEASE_RETAINED=true
TRACK_A_CANONICAL_TEARDOWN_SECRET_ACCESS=false
```

Lease generation 16 was retained at run end. Its replacement-session status is unknown until freshly validated.

### latest package updater attempt

```text
run=32142303624
job=95727636509
TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true
PACKAGE_UPDATE_LEASE16=PASS
```

The job then failed before `PACKAGE_UPDATE_OLD_EXACT=PASS` and before backup/WARP/Xvfb/launcher stages. Thus no package update/mutation occurred in that attempt. The exact failing precondition was not isolated beyond the current source-package client path/executable/size/SHA fence.

## First replacement-session action

Do **not** begin by logging in, rebuilding the old helper or rerunning the old updater.

Perform this sequence:

```text
1. refresh current main / PR #528 / task / reviews / CI / Track A lease state
2. read-only stat+SHA inventory of the canonical source-package bin/client
3. refetch current official CipSoft Linux package manifest
4. classify installed source as already-current / proven-obsolete / unexpected
5. only then authorize and execute the appropriate update-or-skip path
```

The immediate phase has:

```text
CREDENTIALS_ALLOWED=false
LOGIN_ALLOWED=false
MUTATION_AUTHORIZED=false
```

After exact current package installation is proven, update the task admission before any mutation and re-prove all updated-binary native auth/character boundaries. Old helper/offsets are not portable by assumption.

## Secrets

Historical owner authorization for `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` exists and the old-client one-shot dispatch was performed without exposing values. A replacement session must receive current explicit owner authority preserving that bounded permission before consuming the Secrets again.

When authorized later, keep the one-shot sealed-memfd/SCM_RIGHTS native path and never print, persist, commit, place in argv/screenshots/artifacts/model context, or inject into the persistent client environment.

## Prompt and Spark

The canonical alias prompt is updated to `v4.0.0`, continuation-only semantics. Its manual prompt regression matrix is:

```text
docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-prompt-v4-resume-eval.md
```

Current root governance explicitly permits exactly `gpt-5.3-codex-spark` for bounded assistance on this exact alias/task family. Do not send proprietary client binaries or secret-bearing material to Spark.

## Completion remains unchanged

```text
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=NO
CAUSAL_PROOF=INCOMPLETE
```

Only causal structural `IN_GAME` evidence on the freshly admitted current exact client may change that result.
