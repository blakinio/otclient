# Track A RUNTIME — canonical task-HOME package path discriminator

Date: 2026-08-15

## Result

`CANONICAL_HOME_PACKAGE_PATH_ALONE_NOT_SUFFICIENT`

The bounded discriminator executed exactly as planned and remained fail-closed before any protected login step.

## Exact run

- workflow run: `31892205905`
- job: `95030054619`
- workflow head: `01b130a9e42a1f313d84f5480bd103f08f1c1b86`
- runner: `synology-otclient-01`
- artifact: `9248852812`
- artifact digest: `sha256:370d6a94e3dc83a0b2ec622f02dbe94a36b5092f7e64c4471711baa2d7a8dc37`

Exact client fence reverified by the executing job:

```text
size=51965216
sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
version_mapping=15.32.df7b29
platform=official_native_linux_only
```

## Discriminator actually executed

The task-local launcher scaffold created the bounded HOME and the effective helper then replaced its physical package pathname with the canonical task-HOME pathname before launch. The job emitted:

```text
TRACK_A_RUNTIME_MINIMAL_HOME_READY generation=1
TRACK_A_RUNTIME_CANONICAL_PACKAGE_LAUNCH generation=1 path=/home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260815-track-a-runtime-reacquisition/runs/31892205905/home-gen-1/.local/share/CipSoft GmbH/Tibia/packages/Tibia
TRACK_A_EXACT_CLIENT_VERIFIED size=51965216 sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_CREDENTIAL_ENV_CLEAR role=client-gen-1 pid=3892
TRACK_A_RUNTIME_ROLE_DISCOVERED role=client-gen-1 pid=3892 launcher_pid=3892
TRACK_A_RUNTIME_ERROR=client_gen_1_window_missing
```

The canonical HOME package entry was required to be a symlink to the exact task-owned copied package before the helper accepted it. Therefore no persistent source package was launched or mutated by this discriminator.

## Sanitized artifact boundary

The uploaded terminal record confirms:

```text
current_run_ownership=true
bundled_qt_precedence=true
software_backend=true
minimal_launcher_home=true
known_good_xvfb_profile=true
canonical_home_package_launch=true
```

The X11 census remained:

```text
visible_window_count=0
```

`gen1-map-records.tsv` was empty because the workflow failed before the structural observer could be armed.

The sanitized client log shows the exact client remained alive long enough to complete asset loading and make task-SOCKS HTTP requests. It also retained the already-known Qt/OpenGL capability warnings and used `QSGSoftwareRenderThread`; nothing in this run proves those warnings are themselves causal.

## Safety / effects

- protected login generation 1: **SKIPPED**
- protected login generation 2: **SKIPPED**
- persistent client credential variables: **clear**
- movement/gameplay/economic action: **none**
- shared display `:98`: **not used**
- persistent source HOME/package: **not mutated**
- task-owned cleanup: **completed**

## Classification

### FACT

- launching the same task-owned exact client through the canonical task-local `$HOME/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client` path/cwd is not sufficient to restore a visible Tibia window under the current isolated runtime;
- path/cwd/argv surface alone is therefore falsified as the missing discriminator;
- exact client, WARP/relay/Xvfb, bundled Qt, software backend, no-secret ownership and cleanup fences remained intact.

### UNKNOWN

- why attempt 14 of historical run `31730884814` produced a visible window while the current isolated runtime does not;
- whether copied package-local crash-report state, another bounded launch-environment difference, or later mutable package/runtime state is causal;
- restart/relogin structural reacquisition remains untested because login was never reached.

## Next bounded hypothesis

Historical successful attempt 14 explicitly deleted the contents of `Tibia/crashdump` before launching the exact client. The isolated RUNTIME bootstrap currently copies the source package into the task namespace and has not yet cleared the copied task-local crashdump. The next high-information discriminator may clear **only the copied task-owned crashdump after bootstrap**, verify it empty, and otherwise keep run-26 semantics unchanged. Do not delete or modify the persistent source crashdump.