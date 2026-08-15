# Track A RUNTIME — physical canonical-HOME package falsified

Task: `OTC-20260815-track-a-runtime-reacquisition`
Run: `31892698773`
Job: `95031249885`
Head: `4b2653990c400f5011dcff38ce75af946d858db3`
Artifact: `9248979348`
Artifact SHA-256: `21f8432108aa47d8a3def26ada56f088a86566606340a80c29b71c20f8731dc2e`
Runner: `synology-otclient-01`

## Hypothesis

Run #26 had launched through a canonical task-local HOME package pathname backed by a symlink. Run #28 changed only the package-layout distinction: the already task-owned copied exact package was materialized physically under each fresh task-local HOME at `.local/share/CipSoft GmbH/Tibia/packages/Tibia`, with no symlink, and the exact client fence was rechecked at that target.

## FACT

Generation 1 proved the physical target existed and was selected for launch:

```text
TRACK_A_RUNTIME_PHYSICAL_CANONICAL_PACKAGE_READY generation=1 path=.../home-gen-1/.local/share/CipSoft GmbH/Tibia/packages/Tibia
TRACK_A_RUNTIME_PHYSICAL_CANONICAL_PACKAGE_LAUNCH generation=1 path=.../home-gen-1/.local/share/CipSoft GmbH/Tibia/packages/Tibia
TRACK_A_EXACT_CLIENT_VERIFIED size=51965216 sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_CREDENTIAL_ENV_CLEAR role=client-gen-1 pid=10826
TRACK_A_RUNTIME_ERROR=client_gen_1_window_missing
```

The sanitized X11 census recorded:

```text
visible_window_count=0
```

The client log still showed normal asset/config/news startup and a completed network request, but no visible window. Generation-1 setup therefore failed before the protected login step. Generation 2 was not entered. Evidence snapshot and exact current-run cleanup succeeded; no movement, gameplay or economic side effect occurred.

## Classification

### FACT

- physical task-local canonical-HOME package materialization succeeded;
- the target was a real directory, not a symlink;
- exact client size/SHA were rechecked at the physical target before launch;
- the client process was credential-variable-free;
- `visible_window_count` remained zero;
- protected login was not executed;
- cleanup completed.

### DISPROVEN / SUPERSEDED

Physical-versus-symlink canonical package placement is not the cause of the isolated zero-window failure tested by this lane. Do not repeat this discriminator.

### STILL UNKNOWN

The remaining material difference versus the historical successful environment is the provenance/state of the persistent Xvfb `:98`, which was reused by successful historical software-world login attempts. The current lane must not reuse, kill, restart or mutate `:98`.

## New provenance lead

Historical exact commit `f392d76bcaa016cccb7e07012311880f5bf3aa3f`, workflow `.github/workflows/tibia-official-client-re-launch.yml`, documents how persistent `:98` was originally provisioned: a private Xvfb copy had hardcoded `/usr/bin\0` replaced with `.\0`, then was launched after `cd "$toolroot/usr/bin"` with `XKB_CONFIG_ROOT`, `-xkbdir`, `1920x1080x24 -nolisten tcp -noreset`.

The current task helper launches the task-owned/private Xvfb without first changing cwd to `$toolroot/usr/bin`. Because the historical binary patch deliberately resolves the former hardcoded executable directory relative to `.`, Xvfb cwd is a concrete, evidence-backed remaining discriminator. Clone only that cwd onto task-owned `:115`; do not touch persistent `:98`.
