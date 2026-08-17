# Track A canonical runtime v5 — bounded worker-timeout evidence

## Exact physical run

- PR: `#393`
- branch: `ci/OTC-20260816-track-a-canonical-runtime-e2e-v5`
- head: `fc329b23fa8e30fb6110fb162e9c57ed2d3d4e5d`
- workflow run: `31956030015`
- job: `95186692121`
- runner: `synology-otclient-01`
- result: `FAIL_CLOSED / worker_timeout`

## Fresh admission and support facts

The physical job directly proved:

```text
RUNTIME_SUPPORT_ROOT_PREFLIGHT=PASS
RUNTIME_SYSTEM_XKBCOMP_PREFLIGHT=PASS
pre-admission lease status=released generation=3
TRACK_A_CANONICAL_LEASE_ACQUIRE=true
TRACK_A_CANONICAL_LEASE_GENERATION=4
```

The trusted worker then resolved `/work/_otclient_tibia_re_state/toolroot`, regenerated its canonical-owned WARP profile, and did not return before the transition's bounded 300-second worker timeout:

```text
TRACK_A_CANONICAL_TOOLROOT=/work/_otclient_tibia_re_state/toolroot
Successfully generated WireGuard profile: wgcf-profile.conf
TRACK_A_CANONICAL_TRANSITION_ERROR=worker_timeout
```

No sanitized registration block or Gate-B marker was emitted. The transition's failure path kills the bootstrap-owned process group, invokes rollback, removes any committed registration on failure, and the workflow cleanup releases controller authority. No login credentials were supplied by this phase.

## Deterministic source defect discovered after the run

Current trusted worker function `window(pid, display, xdotool)` already polls up to `120 * 0.25s`, approximately 30 seconds, for a visible `^Tibia$` window.

`bootstrap()` then wraps that blocking helper in a second loop of 100 iterations:

```text
for 1..100:
    win = window(...)   # itself up to ~30 seconds
    if win: break
    sleep 0.25
```

Therefore, if the expected window is absent, the worker's nominal missing-window path can take roughly 50 minutes before `client_window_missing`, while the trusted transition is deliberately bounded to 300 seconds. The supervisor must therefore report `worker_timeout` first. This prevents the physical run from distinguishing a slow/missing client window from later bootstrap stages.

Classification: `DETERMINISTIC_BOUNDED_WAIT_DEFECT / HOSTED_FIX_REQUIRED_BEFORE_RETRY`.

This finding does not prove that the client window was absent for the full run; it proves that the current nested wait structure can exceed the supervisor budget and masks the intended fail-closed discriminator.

## Required remediation

Before any new physical bootstrap attempt:

1. replace the nested client-window wait with one bounded wait whose maximum is comfortably below the transition worker timeout;
2. preserve `client_exited` versus `client_window_missing` classification;
3. add deterministic tests proving the bootstrap window wait cannot multiply into an unbounded/over-budget duration;
4. promote the fix to trusted `main` using GitHub-hosted validation only;
5. then redispatch a fresh RUNTIME task/PR from the new current main.

The v5 one-shot workflow was removed immediately after the terminal result. No blind physical retry is authorized from this branch.
