# Track A XRes window identity — helper unavailable

## Scope

Task: `OTC-20260816-track-a-xres-window-identity`  
Source Draft: `#442`  
Trusted PR base: `845adabba5f6d2bfecb6d54bc13834c47cc61c94`

The purpose was to use X-Resource v1.2 `QueryClientIds(LocalClientPid)` to bind the raw full-display viewable X11 resource previously observed by #438 to the exact fenced official-client PID.

## Gate history

The initial PR-body substring gate was found unsafe because a negating sentence could still contain the literal authorization token. The gate was replaced with a branch-suffix condition and `cancel-in-progress:true`. The hardened `...-v2` branch subsequently proved its physical job was SKIPPED.

Source Draft #440 also scheduled a physical job under the old body gate, but its stale-base fence emitted `XRES_REFUSED=BASE_MOVED` and exited before the generated client script was run. It is not a client-launch attempt.

## Physical discriminator that did launch

Workflow run: `31973388722`  
Physical job: `95229260820`  
Runner: `synology-otclient-01`

This job passed:

- Track A runtime admission immediately before the boundary;
- exact current base fence `845adabba5f6d2bfecb6d54bc13834c47cc61c94`;
- immutable harness/transform fences;
- exact client source fence;
- contained DRI/swrast support fence.

It launched the exact isolated client once. Historical ephemeral client PID was `1056`; it is not current authority.

## New direct discriminator

At t+05, t+15 and t+35 the helper selection reported:

```text
libxcb=True
libxcb_res=False
libX11=True
```

Therefore the bounded fixed allowlist used by the observer could not resolve `libxcb-res.so.0`, and no `QueryClientIds(LocalClientPid)` call was possible.

The raw X11 observation itself was reproduced:

- full-display non-root XID remained `VIEWABLE` at 1920x1080;
- available WM PID/name/class properties remained unavailable;
- the exact client remained alive post-GLX/RHI.

Final XRes classification from the generated script:

`XRES_IDENTITY_UNRESOLVED`

Window classification remained:

`NONROOT_X11_WINDOWS_PRESENT_NONE_TASK_PID_BOUND`

## Cleanup and cancellation boundary

The generated discriminator reached:

```text
WINDOW_DIAG_RESULT=PASS_DISCRIMINATOR_CAPTURED
WINDOW_DIAG_CLEANUP=COMPLETE
```

A newer hardening workflow generation then cancelled the already-completed job during post-job handling. The cancellation happened after the discriminator result and cleanup, so the run is retained as a valid physical discriminator.

The hardened follow-up workflow generation on commit `c4613fa3b5e4e4547f5d378a2ea3f7c1a4401987` completed hosted preflight successfully and **SKIPPED** its physical job, proving the replacement gate was fail-closed on the non-authorized branch.

## Classification

`PROVEN_XRES_IDENTITY_UNRESOLVED_BECAUSE_LIBXCB_RES_HELPER_UNAVAILABLE_ON_RUNNER_FIXED_ALLOWLIST`

## Boundaries

This result does **not** prove that the viewable XID is foreign to the official client. It does **not** justify changing the canonical window identity contract. It only proves that the chosen libxcb-res helper path was unavailable on this runner/toolroot surface.

No second client launch is authorized for this task.

## Next causal step

Perform a support-only, read-only inventory for XRes client-library capability before any new client launch. The resulting support inventory is promoted separately under the same coordinator review chain.
