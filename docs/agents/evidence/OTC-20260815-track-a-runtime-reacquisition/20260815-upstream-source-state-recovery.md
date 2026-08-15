# Track A RUNTIME upstream/source-state recovery

Task: `OTC-20260815-track-a-runtime-reacquisition`
Draft PR: `#303`
Base main: `8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`
Exact client: `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

## First executable RUNTIME run after selector repair

### FACT

Workflow head `4f5314cfefa4dfeb150f4e5d912ef4180c4efc67` produced run `31884181155`.

- preflight `95010928093`: `SUCCESS`;
- `reacquire` `95010941902`: assigned to runner id `21`, `synology-otclient-01`;
- exact resume-request validation: `SUCCESS`;
- exact helper syntax/blob fence: `SUCCESS`;
- bootstrap: `FAILURE` before generation 1;
- login was never attempted;
- generation 1/2 semantic verification was never entered;
- fail-closed cleanup completed successfully with no X11 residue.

The first material bootstrap error was:

```text
/home/runner/_work/_otclient_tibia_re_state/runtime/wireproxy.pid: No such file or directory
TRACK_A_RUNTIME_ERROR=upstream_wireproxy_unavailable
```

Sanitized terminal artifact: id `9246814693`, uploaded ZIP SHA-256 `488cc29d4844ee7b614d66f21b91c73fa25ace589af56e192307fb74422af10d`.

No credential value was printed. No gameplay action occurred.

## Runner layout provenance

### FACT

Historical successful exact-build Track A job `94785974126` on the same `synology-otclient-01` runner selected state using:

```bash
if [[ -d /work && -w /work ]]; then
  state=/work/_otclient_tibia_re_state
else
  state=/home/runner/_work/_otclient_tibia_re_state
fi
```

That successful job then used the exact client, toolroot and runtime files below the selected state.

Current RUNTIME helper instead hardcodes canonical `/home/runner/_work/_otclient_tibia_re_state` for:

- exact source client package;
- toolroot;
- shared upstream `runtime/wireproxy.pid`;
- optional `runtime/Xvfb-track-a` helper binary.

The task-owned namespace itself is correctly canonical and remains:

```text
/home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260815-track-a-runtime-reacquisition
```

## Recovery design

### FACT

The recovery does **not** start, stop, rewrite or take ownership of shared WARP/wireproxy. It keeps task-owned mutable state canonical and changes only read-only source discovery.

A task-local effective helper is derived from the exact hash-fenced repository helper at runtime. Its compatibility changes are exact-match transformations and must fail if the expected source helper text drifts.

The effective helper:

1. considers `/work/_otclient_tibia_re_state` and canonical state as source candidates;
2. accepts a source state only when its official client matches the exact SHA and size;
3. sources toolroot/client/Xvfb helper from that exact-selected source;
4. inspects wireproxy PID files read-only across the selected, canonical and legacy state;
5. requires exactly one distinct live upstream PID with `OTCLIENT_TIBIA_RE_TRACK=official-client-re`;
6. separately requires local SOCKS port `25354` to listen and Cloudflare trace to report `warp=on` or `warp=plus`;
7. fails closed if zero or multiple eligible upstream owners exist.

### INFERENCE

This addresses a runner-layout compatibility issue rather than weakening the upstream ownership fence. The task remains a consumer of separately owned Track A WARP state, not its owner.

## YAML serialization repair

Workflow head `4573900d7c3c4b042881f22c33ff00a19c684fd5` accidentally emitted embedded transform-string lines outside the YAML block indentation. GitHub rejected the workflow before creating RUNTIME jobs. This was a workflow-serialization defect only; no runner or runtime side effect occurred.

Head `972936ffef081318b6103a6c799feeb3ce36fc92` rewrote those embedded strings with YAML-safe indentation while preserving the same compatibility design. Run `31884531727` parsed correctly; preflight succeeded and `reacquire` job `95011797563` was assigned to runner id `21` / `synology-otclient-01`.

## Current classification

At this checkpoint run `31884531727` is the only semantic RUNTIME operation that should be inspected. Do not dispatch an identical run while it is active.

Still UNKNOWN until that run advances:

- whether a single live Track A upstream wireproxy exists in the proven source state;
- whether WARP verifies through port `25354`;
- whether source client/toolroot/Xvfb dependencies all pass;
- protected credential availability/acceptance;
- generation-1 structural `IN_GAME`;
- clean restart and generation-2 fresh PID/PIE structural reacquisition;
- final transport confinement and cleanup result.
