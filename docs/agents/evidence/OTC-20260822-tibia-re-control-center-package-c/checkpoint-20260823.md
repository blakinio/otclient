# Package C terminal closeout evidence ? 2026-08-23

## Scope

This record supersedes the earlier waiting checkpoint for `OTC-20260822-tibia-re-control-center-package-c`.

Package C remained repository-only throughout the continuation:

- `runtime_access: none`
- Official Tibia client/runtime/process/container/KasmVNC access: NONE
- credentials/login/gameplay/UI input: NONE
- mutation/transaction/network-listener authority: NONE

## Final implementation identity

- implementation PR: #663 ? MERGED
- implementation branch: `feat/OTC-20260822-tibia-re-control-center-package-c`
- exact final implementation head: `0c551951b6f40b810f3e69cbd138edb85c70fe3a`
- implementation base immediately before merge: `main@5ac05b2640e818a1efc3e065e2ed4e501eaed058`
- squash merge on `main`: `de14f7a3659af51c055ab426fe46ada838f54141`
- implementation changed files: exactly:
  - `tools/tibia_re_control_center/surveyor_provider.py`
  - `tests/tools/tibia_re_control_center/test_package_c_surveyor_provider.py`

## Producer and schema pins

- producer commit: `1affb3a094a06f2a250140e8173501b3a6938164`
- accepted aggregate schema: `otclient.tibia-re-surveyor.collect-all.v2`
- alias schema: `otclient.tibia-re-surveyor.alias-view.v2`
- telemetry schema: `otclient.tibia-re-surveyor.telemetry.v2`
- missing-reader schema: `otclient.tibia-re-surveyor.missing-readers.v2`
- producer acceptance anchor: `815245ab3cac38a96f60f3ee3395b67f81b81c11`
- producer blobs reverified during continuation:
  - `collect_all.py`: `43494964ed20cbadeb5e27cda6d441cf4c054b50`
  - `survey.py`: `17d54afa3bce401e6d88c85ea7dcf292e1d31f2c`
  - `reader_registry.py`: `62a2bc38687f48d6756d5f5eab9d637a110d9f26`
  - `README.md`: `5f544a6060fbe714ccf9106b929b97897bba2e5f`

## Material continuation findings closed

Two fresh exact-head Codex audits after the original checkpoint found real P1 producer-boundary defects; both were reproduced, repaired with regressions and re-audited before merge:

1. a manifest-valid non-admitted runtime with scalar `visible_tibia_windows=1` could reach `len()` and escape as raw `TypeError`; the provider now validates the producer collection shape before projection;
2. the first fix was too broad for the producer's legitimate target-down shape: `DockerRuntimeProbe.snapshot()` emits `READ_ONLY_UNAVAILABLE` without `visible_tibia_windows` when the target is stopped. The final logic permits omission only for that producer variant and still rejects a malformed value when present.

The final target-down regression was RED before the fix and GREEN after it; the earlier malformed non-admitted regression remained GREEN.

## Exact-head validation ? `0c551951b6f40b810f3e69cbd138edb85c70fe3a`

- Windows full Control Center suite: `214 tests`, PASS, `2` POSIX-only skips
- Package C focused suite: `60 tests`, PASS, `2` POSIX-only skips
- WSL/POSIX hardening: `4/4` PASS
- owned Package C Ruff: PASS
- `git diff origin/main...HEAD --check`: PASS
- Package A workflow `32650478511`: SUCCESS
- repository CI run `32650478885`: SUCCESS
- required aggregate job `97221314928` (`CI / Required`): SUCCESS
- independent Codex audit request: comment `5386963167`
- independent Codex audit result: comment `5386978151` ? "Didn't find any major issues"; reviewed commit `0c551951b6`
- unresolved implementation review threads at merge gate: `0`

## Closeout lifecycle

- task claim PR #664: MERGED
- implementation PR #663: MERGED
- closeout PR #679: reused as the mandatory archive/evidence/ownership-release PR
- active task is moved to `docs/agents/tasks/archive/OTC-20260822-tibia-re-control-center-package-c.md` in #679
- archive record sets `ownership_released: true` and `owned_paths: []`
- `docs/agents/MODULE_CATALOG.md` and `docs/agents/CHANGELOG.md` remain deferred because open draft PR #23 still changes both paths
- Official Tibia access remained NONE

PR #679 must pass its own exact-head lifecycle validation, required GitHub checks and independent documentation/closeout audit before merge. Its merge makes the archive authoritative on `main`; final foreground verification then confirms the active task is absent and Package C ownership is released.
