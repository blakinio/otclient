# OTC Vision P2 Central Fence Finalization Handoff

```yaml
prompt_contract_version: 1.0.0
alias: OTC-VISION-P2-CENTRAL-FENCE-FINALIZE
repository: blakinio/otclient
programme_id: OTC-VISION-P2-READONLY
role: finalizer_and_coordinator
run_scope: autonomous_until_terminal_or_real_external_stop
anti_loop: strict
codex_spark_allowed: true
```

## Owner invocation

```text
Uruchom OTC-VISION-P2-CENTRAL-FENCE-FINALIZE autonomicznie.
```

## Mission

Resume existing work; do not restart discovery or redesign the architecture.
Finish the already-implemented central current-client fence change, promote it safely,
then finish the previously blocked Vision P2 Wave 3 live E2E and close the existing PR chain.
## Trusted starting state

Resolve GitHub again before writes, but the checkpoint floor is:

```text
trusted main after #861:
  30fc46ce4dbff96d2484e624a58fcd85f2a9ecad

centralization branch:
  feat/OTC-20260902-central-current-client-fence

centralization committed head:
  30879f705cfeaf84567356b8f90e35cb886af822

commit sequence:
  881e71e4a  docs(track-a): design central current-client fence
  9c9a72597  feat(track-a): add canonical current-client fence manifest
  8d0bccbdc  test(track-a): require centralized current-client fence
  30879f705  feat(track-a): centralize current-client fence
```

The handoff task/prompt documentation is committed and the branch is pushed. Treat `30879f705...` as the GREEN implementation head, not as a promise about the latest remote branch head; resolve the current remote branch head before work. No centralization PR existed when this handoff was prepared.
## What is already implemented — do not redo

Central manifest:

```text
docs/agents/contracts/TRACK_A_CURRENT_CLIENT_FENCE_V1.json
```

It contains strict `current`, `current_provenance`, and `approved_history`.
Current at this checkpoint is:

```text
15.32.be4f48
size 52105824
sha256 552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

`approved_history` is reconciliation-source-only. It grants no current runtime or semantic authority.
The loader is `tools/tibia_re_control_center/current_client_fence.py`.
Identity/admission consumers have been migrated to it; build-specific semantic/offset/QMeta workflows intentionally remain version-pinned.
Canonical client-fence reconciliation has also been generalized:

- source registration must equal `manifest.current` or one exact `approved_history` tuple;
- fresh probe must always prove exactly `manifest.current`;
- existing guard/lease/three-probe stability/atomic replace/fsync/rollback semantics remain unchanged;
- no client-process mutation, memory observation, login, GUI input or semantic promotion is added.

Surveyor now loads the current fence dynamically and checks version + size + SHA.
Canonical live transition/session, Kasm bootstrap, existing-runtime probe and Control Center read-only admission also load the same manifest.
The executable current-literal scan at GREEN head found zero copies of the current version/SHA outside the manifest.
## Verified local results at handoff

Do not claim these as fresh after modifying the head; rerun appropriate gates after any commit.

```text
Windows/static:
  current-fence + governance: PASS
  Control Center/Vision/Surveyor matrix: 66/66 PASS
  Ruff I/F: PASS
  py_compile: PASS
  YAML parse: PASS
  git diff --check: PASS

Linux/WSL:
  canonical transition: 58/58 PASS
  Kasm bootstrap worker: 11/11 PASS
  existing-runtime adoption probe: 10/10 PASS
  client-fence reconciliation: 17/17 PASS
  canonical live session: 14/14 PASS
  Kasm workflow contract: 7/7 PASS
  total listed Linux/workflow tests: 117/117 PASS
```

Direct Codex usage during this implementation was zero.
## Strict anti-loop rules

1. Do not create another architecture/refactor task unless a concrete failing gate proves the current design cannot be completed.
2. Do not re-centralize build-pinned semantic workflows. Their old fences are intentional until their own semantic evidence is revalidated.
3. Do not redo already-green test matrices merely to consume time. Rerun them only after relevant head changes or for final exact-head verification.
4. Do not create a new runtime daemon, semantic producer, capture subsystem or transport path.
5. Do not manually edit `runtime-registration.json`.
6. Do not increase freshness timeouts to force Vision P2 PASS.
7. Do not fake a physical E2E with fixtures/localhost in place of the live target.
8. If a new blocker would require a new subsystem or another broad refactor, stop and report that blocker instead of automatically expanding scope.
9. Codex Spark is allowed by the owner, but use it only when it materially reduces work; never use it to rediscover the architecture. Independently verify all Codex output.
## Required execution order

### 1. Finish and promote centralization

Freshly resolve `main`, branch and working tree. Preserve existing commits.
Finish the task checkpoint and add only the exact Package A branch/base/repository exception required by the existing governance boundary. Do not add a broad prefix exception.
Run the central fence gate, Track A governance, focused Windows/Linux suites, YAML/Ruff/compile/diff-check, and exact Package A positive + wrong-branch/wrong-base/fork falsification.

Open one Draft PR from `feat/OTC-20260902-central-current-client-fence` to `main`.
Require terminal exact-head GitHub Actions, inspect changed paths/review threads, classify ACCEPT only if scope is still central identity/admission infrastructure, then Ready + squash merge with expected head SHA.
Do not merge from static local green alone.
### 2. Repair the existing stale canonical registration only after merge

The last live Surveyor run was `33667152187` on trusted main after #861.
It proved one exact current target and X11 owner, then failed closed at admission with:

```text
CANONICAL_REGISTRATION_IDENTITY_MISMATCH=pid,process_start_ticks,client_sha256
```

Known live target from that run:

```text
PID 28379
process_start_ticks 36180734
current fence 15.32.be4f48 / 52105824 / 552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
TARGET_NAMESPACE_CLIENTS=1
TARGET_EXACT_CLIENTS=1
TARGET_WINDOW_MATCHES=1
TARGET_UNIQUENESS=PROVEN
```

After centralization is merged, use the existing reviewed canonical client-fence reconciliation path. Re-resolve its current contract/workflow first. Do not manually rewrite/delete registration and do not restart the client merely to make registration match.
### 3. Re-run one fresh Surveyor admission

Use the existing owner-gated `Track A Surveyor v2 read-only` workflow on `synology-otclient-01` with runtime task:

```text
OTC-20260902-vision-p2-e2e-audit
```

Require fresh exact current version/size/SHA, singleton PID/start identity, one PID-owned visible Tibia window, and `runtime_access=read_only` admission. If it fails, diagnose that exact failure; do not launch another duplicate Surveyor while one is active.

### 4. Finish Vision P2 Wave 3

Existing PRs before this handoff:

```text
#856 feat/OTC-20260902-vision-p2-vision-reconciliation
checkpoint head 2346ffb704c213f2e3050f87fc80aaa611454cd3
Draft/unmerged; prior coordinator ACCEPT review 5091459576

#857 test/OTC-20260902-vision-p2-e2e-audit
checkpoint head c0fd6cf09ed106cf5e03e5516114ffee814da396
Draft/unmerged; runtime_access was returned to none after the prior endpoint stop
```

Freshly restack/revalidate them on the new trusted main rather than trusting those checkpoint SHAs.
For the final live gate, use only one fresh read-only admission window and one physical capture. The already-proven architecture is:

- real Synology→Molehill production edge transport was previously physically proven;
- KasmVNC framebuffer is reachable from Molehill in encrypted `view_only` mode even when the Synology Remote Desktop Commander endpoint is offline;
- no persistent edge daemon is required for Phase 2 acceptance;
- no reviewed semantic runtime evidence is required for the visual-only final state;
- with no current semantic evidence, valid reconciliation is `UNKNOWN` with `runtime_current=false` and empty runtime evidence refs.

Exact Qwen production profile:

```text
model qwen3-vl:4b-instruct-q4_K_M
digest ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b
num_ctx 4096
num_predict 256
temperature 0
```

Use the existing strict six-key Vision prompt/schema. Keep Ollama loopback-only and unload/stop the task-owned provider after the run.
Required truthful final result for the full-mask visual-only path is expected to be:

```text
visual screen_class=UNKNOWN
reconciliation state=UNKNOWN
runtime_current=false
runtime evidence refs empty
physical_action_count=0
```

Do not extend the default 15-second capture/edge freshness window merely to obtain PASS. If exact Qwen cannot finish while the admitted edge/capture remains current, record INCONCLUSIVE/STALE.

No credentials, login, relogin, character selection, gameplay, GUI/anti-idle input, process control, process memory access or network payload capture are authorized.

### 5. Close the PR chain

After the final live gate is truthfully resolved, update #857 audit evidence/task, return `runtime_access:none`, rerun exact-head governance/CI, then classify and merge #856/#857 according to current repository rules. Do not claim the historical broad suite as fully green; prior Windows baseline had unrelated pre-existing failures.

## Terminal report

Report only fresh verified facts: new trusted main SHA, centralization PR/head/merge SHA, canonical reconciliation run result, fresh Surveyor run, final Vision P2 observation/reconciliation result, #856/#857 final heads/merge status, and any real external blocker.
