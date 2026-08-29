# Track A Kasm Canonical Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reviewed KasmVNC-aware `create_new` canonical bootstrap that can create exactly one current official Tibia client inside `otclient-track-a-kasmvnc`, register it atomically under the existing Track A canonical authority model, and roll back only the exact process created by the transaction.

**Architecture:** Keep the legacy host/process-group bootstrap unchanged. Extend the narrow Docker/Kasm worker preflight with current boot identity; add a metadata-only `boot-epoch-registration-invalidate` recovery transition for the proven PRESENT-registration/zero-client prior-boot state; then retain the separate `kasm-bootstrap` create-new operation for registration-ABSENT launch/commit/safe-detach. The owner-only live workflow uses two sequential task authorities/leases (recovery, then bootstrap), while PR validation stays GitHub-hosted and the implementation PR remains `runtime_access: none`.

**Tech Stack:** Python 3 standard library, Docker CLI invoked through `subprocess`, existing Track A lease/guard/transition code, existing Kasm read-only adoption probe, GitHub Actions YAML, Python `unittest`/`mock`.

**Spec:** `docs/superpowers/specs/2026-08-29-track-a-kasm-canonical-bootstrap-design.md`

## Global Constraints

- Exact client fence is `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`.
- Physical target is only `otclient-track-a-kasmvnc`, user `kasm-user`, `DISPLAY=:1`.
- Preserve legacy `_bootstrap()` behavior and tests unchanged except additive parser/dispatch coverage.
- Implementation task stays `runtime_access: none`, `mutation_authorized: false`, physical budget/count `0/0`; this PR performs no live runtime action.
- No credentials, login, relogin, character selection, world entry, gameplay, GUI input, packet capture, debugger attach, process-memory observation or semantic promotion.
- No client package download, update, copy or byte mutation; launch only the exact already-present package executable.
- No marker or controller capability is placed in the client environment. Provenance is canonical-flock + zero-client preflight + immediate singleton post-launch binding.
- Rollback may signal only a live process that still exactly matches container full ID/name, PID, start ticks, executable path, size and SHA from the transaction launch record.
- No `pkill`, `killall`, Docker stop/restart/rm, display cleanup, volume cleanup or broad process targeting.
- Kasm registration must reuse the existing Docker/adoption proof fields and force semantic `state: UNKNOWN`; only additive `bootstrap_provenance: kasm_create_new_v1` is new.
- PR-triggered validation is GitHub-hosted only. A self-hosted job must be syntactically gated so `pull_request` cannot schedule it.
- Physical workflow must require repository owner + `workflow_dispatch` + `refs/heads/main` + exact authorization + `GITHUB_RUN_ATTEMPT == 1`; it uses a metadata-only recovery lease first and a separate bootstrap lease only after registration absence is proven.
- Live execution is a separate post-merge task/admission and cannot be authorized by the implementation branch itself.

---

### Task 1: Deterministic Kasm bootstrap worker

**Files:**
- Create: `.github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py`
- Create: `.github/scripts/test_tibia_official_client_re_kasm_bootstrap_worker.py`

**Interfaces:**
- Consumes: Docker CLI; exact constants `TARGET_CONTAINER`, `TARGET_DISPLAY`, `PACKAGE_DIR`, `CLIENT_PATH`, `VER`, `SIZE`, `SHA` defined in the worker.
- Produces CLI operations `preflight "$RECORD_PATH"`, `launch "$RECORD_PATH"`, `rollback "$RECORD_PATH"`.
- Produces preflight schema `otclient.track-a.kasm-bootstrap.preflight.v1` and launch schema `otclient.track-a.kasm-bootstrap.launch.v1` in mode `0600`.
- Exposes importable helpers `collect_preflight(runner=run) -> dict[str, Any]`, `launch_from_preflight(path: Path, runner=run, sleeper=time.sleep) -> dict[str, Any]`, `rollback_launch(path: Path, runner=run, sleeper=time.sleep) -> None` for deterministic tests.

- [ ] **Step 1: Write failing preflight contract tests**

Create tests with a fake command runner that require:

```python
class FakeRunner:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def __call__(self, command):
        key = tuple(command)
        self.calls.append(key)
        value = self.responses[key]
        if isinstance(value, Exception):
            raise value
        return value


def test_preflight_accepts_only_zero_client_exact_kasm_target(self):
    payload = module.collect_preflight(runner=fake)
    self.assertEqual(payload['schema'], 'otclient.track-a.kasm-bootstrap.preflight.v1')
    self.assertEqual(payload['container_name'], 'otclient-track-a-kasmvnc')
    self.assertEqual(len(payload['container_id']), 64)
    self.assertEqual(payload['display'], ':1')
    self.assertEqual(payload['client_size'], 52105824)
    self.assertEqual(payload['client_sha256'], module.SHA)
    self.assertEqual(payload['candidate_count'], 0)
    self.assertEqual(payload['main_window_count'], 0)
    self.assertRegex(payload['preflight_fingerprint'], r'^[0-9a-f]{64}$')
```

Add negative tests for target container missing/multiple, non-64hex container ID, display unavailable, client missing/symlink/wrong size/wrong SHA, pre-existing exact client, official-looking mismatched/unreadable candidate, and existing Tibia main window.

- [ ] **Step 2: Run worker tests and confirm RED**

Run:

```bash
python3 .github/scripts/test_tibia_official_client_re_kasm_bootstrap_worker.py -v
```

Expected: FAIL because the worker module/functions do not exist.

- [ ] **Step 3: Implement minimal zero-client preflight**

Implement these fixed record fields:

```python
{
    'schema': 'otclient.track-a.kasm-bootstrap.preflight.v1',
    'container_name': TARGET_CONTAINER,
    'container_id': full_id,
    'display': TARGET_DISPLAY,
    'package_dir': PACKAGE_DIR,
    'client_path': CLIENT_PATH,
    'client_size': SIZE,
    'client_sha256': SHA,
    'candidate_count': 0,
    'main_window_count': 0,
    'preflight_fingerprint': fingerprint,
}
```

Use `docker ps --no-trunc --format '{{.ID}}\t{{.Names}}'`, exact target-name cardinality, `docker exec -u kasm-user -e DISPLAY=:1 "$FULL_CONTAINER_ID" xdpyinfo`, exact regular/non-symlink package executable verification, and an all-running-container process inventory modeled on the existing Kasm adoption probe. Treat any official-looking unreadable or wrong-fence candidate as a closed failure, not absence. Inspect `xwininfo -root -tree` and reject any Tibia main window before launch.

`preflight_fingerprint` is SHA-256 over canonical JSON of container name/full ID, display, package/client path, exact size/SHA and zero candidate/window counts.

- [ ] **Step 4: Run preflight tests and confirm GREEN**

Run the worker test module. Expected: all preflight positive/negative cases PASS.

- [ ] **Step 5: Write failing launch tests**

Require launch to re-run `collect_preflight`, require its fingerprint and bound target to match the persisted preflight, then issue exactly one direct detached command shaped as:

```text
docker exec -d -u kasm-user -w "$PACKAGE_DIR"
  -e HOME=/home/kasm-user -e DISPLAY=:1 "$FULL_CONTAINER_ID"
  /usr/bin/env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD
  -u TRACK_A_CANONICAL_LEASE_TOKEN -u TRACK_A_CANONICAL_LEASE_TOKEN_FILE
  "$CLIENT_PATH"
```

Do not use `sh -c` for the actual launch. After launch, bounded polling must find exactly one exact current client in the same full container and return:

```python
{
    'schema': 'otclient.track-a.kasm-bootstrap.launch.v1',
    'preflight_fingerprint': preflight['preflight_fingerprint'],
    'container_name': TARGET_CONTAINER,
    'container_id': preflight['container_id'],
    'display': TARGET_DISPLAY,
    'package_dir': PACKAGE_DIR,
    'client_path': CLIENT_PATH,
    'client_size': SIZE,
    'client_sha256': SHA,
    'pid': 123,
    'process_start_ticks': 456,
    'launch_method': 'docker_exec_detached_direct_env',
    'bootstrap_helper_residue': False,
}
```

Add negatives for fingerprint drift, container ID drift, a client appearing before the launch revalidation, no client after launch, more than one candidate, candidate in another container, wrong fence, and client disappearance while capturing start identity.

- [ ] **Step 6: Run launch tests and confirm RED, then implement minimal launch**

Run worker tests before implementation and observe failure. Implement only the tested launch behavior, with bounded polling and no credential/capability variables passed into the client.

- [ ] **Step 7: Write failing rollback tests**

Require rollback to re-read the launch record and re-prove exact container full ID/name plus exact PID/start/path/size/SHA before any signal. Positive path may issue only:

```text
docker exec "$FULL_CONTAINER_ID" /bin/kill -TERM "$PID"
```

After a bounded wait, if the process is still alive and remains exactly the same identity, it may issue:

```text
docker exec "$FULL_CONTAINER_ID" /bin/kill -KILL "$PID"
```

Add negative tests for PID reuse/start drift, full container ID drift, path drift, size/SHA drift and missing/invalid launch record. Assert no command contains `pkill`, `killall`, `docker stop`, `docker restart`, `docker rm` or process-name targeting.

- [ ] **Step 8: Implement rollback and run complete worker suite**

Expected: all worker tests PASS and no broad process-control command is emitted.

- [ ] **Step 9: Verify worker syntax**

Run:

```bash
python3 -m py_compile \
  .github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py \
  .github/scripts/test_tibia_official_client_re_kasm_bootstrap_worker.py
```

Expected: PASS.

- [ ] **Step 10: Commit Task 1**

```bash
git add .github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py \
        .github/scripts/test_tibia_official_client_re_kasm_bootstrap_worker.py
git commit -m "feat(track-a): add Kasm bootstrap worker"
```

---

### Task 2: Canonical `kasm-bootstrap` transaction

**Files:**
- Modify: `.github/scripts/tibia-official-client-re-canonical-live-transition.py`
- Modify: `.github/scripts/test_tibia_official_client_re_canonical_live_transition.py`

**Interfaces:**
- Consumes worker `preflight/launch/rollback` records from Task 1.
- Consumes existing Kasm probe operation `probe "$OUTPUT_PATH"` and its `existing_runtime_adoption_v1` manifest.
- Produces new controller operation `kasm-bootstrap --task-id "$TASK_ID" --session-id "$SESSION_ID" --token-file "$TOKEN_FILE" --worker "$WORKER_PATH" --probe "$PROBE_PATH" --worker-timeout 90`.
- Produces canonical schema-v1 registration with the existing Kasm/adoption proof fields plus `bootstrap_provenance: 'kasm_create_new_v1'` and `state: 'UNKNOWN'`.

- [ ] **Step 1: Add failing parser/dispatch tests**

Require `parser()` to accept:

```text
kasm-bootstrap
  --task-id OTC-TEST
  --session-id s
  --token-file /tmp/token
  --worker /repo/.github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py
  --probe /repo/.github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
  --worker-timeout 90
```

and require `_child` dispatch to contain an explicit `kasm-bootstrap` mapping without changing the legacy `bootstrap` mapping.

- [ ] **Step 2: Run transition suite and confirm RED**

Run:

```bash
python3 .github/scripts/test_tibia_official_client_re_canonical_live_transition.py -v
```

Expected: new Kasm bootstrap tests fail while pre-existing legacy tests remain otherwise green.

- [ ] **Step 3: Add Kasm record validation helpers**

Implement bounded helpers:

```python
KASM_BOOTSTRAP_PROVENANCE = 'kasm_create_new_v1'
KASM_PREFLIGHT_SCHEMA = 'otclient.track-a.kasm-bootstrap.preflight.v1'
KASM_LAUNCH_SCHEMA = 'otclient.track-a.kasm-bootstrap.launch.v1'


def _read_kasm_bootstrap_record(path: Path, expected_schema: str) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise E('kasm_bootstrap_record_invalid', str(exc)) from exc
    if not isinstance(data, dict) or data.get('schema') != expected_schema:
        raise E('kasm_bootstrap_record_invalid')
    return data


def _kasm_launch_signature(record: dict[str, Any]) -> tuple[Any, ...]:
    return tuple(record[key] for key in (
        'preflight_fingerprint', 'container_name', 'container_id', 'display',
        'client_path', 'client_size', 'client_sha256', 'pid',
        'process_start_ticks', 'launch_method', 'bootstrap_helper_residue',
    ))


def _require_kasm_launch_matches_manifest(launch: dict[str, Any], manifest: dict[str, Any]) -> None:
    locator = f"docker:{launch['container_name']}:{launch['container_id']}"
    required = {
        'pid': launch['pid'],
        'process_start_ticks': launch['process_start_ticks'],
        'client_size': launch['client_size'],
        'client_sha256': launch['client_sha256'],
        'display': launch['display'],
        'runtime_locator': locator,
        'inventory_scope': 'all_running_docker_containers',
        'inventory_complete': True,
        'candidate_count': 1,
        'state': 'UNKNOWN',
    }
    for key, expected in required.items():
        if manifest.get(key) != expected:
            raise E(f'kasm_bootstrap_manifest_{key}_mismatch')
```

Validation must reject extra/missing critical identity fields, non-64hex full container ID, wrong exact fence, wrong target container/display/path, non-positive PID/start, wrong launch method or `bootstrap_helper_residue is not False`.

Manifest matching must require:
- `proof_kind == existing_runtime_adoption_v1`;
- `state == UNKNOWN`;
- Docker locator exact full container ID/name;
- same PID/start/size/SHA/display;
- `inventory_complete is True`, `inventory_scope == all_running_docker_containers`, `candidate_count == 1`;
- self-consistent candidate fingerprint.

- [ ] **Step 4: Add failing happy-path transaction test**

Mock worker calls and existing Kasm probe. Require exact order:

```text
worker preflight
lease/re-registration absence revalidation
worker launch
probe #1
stage registration
probe #2
lease + registration absence revalidation
atomic commit
probe #3
lease + committed registration revalidation
return success without rollback
```

Require registration fields to copy the probe's exact Docker/adoption evidence, force `state=UNKNOWN`, and add only `bootstrap_provenance=kasm_create_new_v1`.

- [ ] **Step 5: Add failing rollback/atomicity tests**

Cover:
- registration already present -> no worker call;
- preflight failure -> no launch;
- lease drift before launch -> no launch;
- launch record/probe mismatch -> rollback once, no registration left;
- probe drift before commit -> rollback once, no registration left;
- registration race before commit -> rollback once and never overwrite concurrent registration;
- commit succeeds but final probe fails -> remove only the exact registration created by this transaction, then exact worker rollback;
- concurrent registration replacement after commit -> refuse to overwrite/delete the concurrent record;
- rollback worker failure -> surface `kasm_bootstrap_rollback_failed` without broad cleanup;
- successful transaction never invokes legacy `_kill()` and never invokes worker rollback.

- [ ] **Step 6: Implement `_kasm_bootstrap` minimally**

Use files under `STATE` for temporary preflight, launch and probe records. All worker/probe calls occur from the existing `_supervise` child while the canonical coordination flock is held.

Do not call local `_candidates()` for Docker Kasm identity; the worker's zero-client all-container preflight and the existing Kasm probe are the Docker-aware authorities.

Build registration from the first Kasm probe:

```python
registration = {
    'schema_version': 1,
    'runtime_id': RID,
    'registration_generation': 1,
    'lease_generation': generation,
    'registered_at': int(time.time()),
    'boot_id_sha256': first['boot_id_sha256'],
    'pid': first['pid'],
    'process_start_ticks': first['process_start_ticks'],
    'client_version': VER,
    'client_size': SIZE,
    'client_sha256': SHA,
    'display': first['display'],
    'window_identity': first['window_identity'],
    'remote_view_endpoint': first['remote_view_endpoint'],
    'remote_view_mapping': first['remote_view_mapping'],
    'state': 'UNKNOWN',
    'proof_kind': first['proof_kind'],
    'runtime_locator': first['runtime_locator'],
    'inventory_scope': first['inventory_scope'],
    'inventory_complete': first['inventory_complete'],
    'candidate_count': first['candidate_count'],
    'candidate_fingerprint': first['candidate_fingerprint'],
    'state_evidence': first['state_evidence'],
    'bootstrap_provenance': KASM_BOOTSTRAP_PROVENANCE,
    'source_task': args.task_id,
    'source_run': _runid(),
}
```

Reuse `_stage`, `_commit`, `_read`, `_remove`, `_adoption_signature`, `_match`, `_lease`, `_cancel` and the existing conflict/rollback principles. On any post-launch failure call worker `rollback` using the launch record path only after own registration cleanup/conflict handling.

- [ ] **Step 7: Extend `_read()` only additively**

Because `FIELDS` is a required subset, additive provenance is already schema-compatible. Add validation only when `bootstrap_provenance` exists: it must equal `kasm_create_new_v1` and coexist with `proof_kind == existing_runtime_adoption_v1`. Do not make the new field mandatory for historical/adopted Kasm registrations.

- [ ] **Step 8: Extend parser and dispatch**

Add `kasm-bootstrap` to parser and `_child` map. It receives both `--worker` and `--probe`, plus bounded `--worker-timeout`; legacy `bootstrap` continues to receive its current arguments exactly.

- [ ] **Step 9: Run canonical regression suites**

Run:

```bash
python3 .github/scripts/test_tibia_official_client_re_canonical_live_transition.py -v
python3 .github/scripts/test_tibia_official_client_re_kasm_existing_runtime_probe.py -v
python3 .github/scripts/test_tibia_official_client_re_kasm_bootstrap_worker.py -v
python3 -m py_compile \
  .github/scripts/tibia-official-client-re-canonical-live-transition.py \
  .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
```

Expected: all PASS, including pre-existing legacy bootstrap/adoption/rebind/recovery/boot-epoch/Gate-B regressions.

- [ ] **Step 10: Commit Task 2**

```bash
git add .github/scripts/tibia-official-client-re-canonical-live-transition.py \
        .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
git commit -m "feat(track-a): add Kasm canonical bootstrap transition"
```

---

### Task 2A: Prior-boot zero-client registration invalidation

**Files:**
- Modify: `.github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py`
- Modify: `.github/scripts/test_tibia_official_client_re_kasm_bootstrap_worker.py`
- Modify: `.github/scripts/tibia-official-client-re-canonical-live-transition.py`
- Modify: `.github/scripts/test_tibia_official_client_re_canonical_live_transition.py`
- Modify: `.github/scripts/test_track_a_agent_runtime_governance.py`
- Modify: `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`

**Interfaces:**
- Kasm preflight adds required `boot_id_sha256: str` (64 lowercase hex) and includes it in `preflight_fingerprint`.
- Controller adds `boot-epoch-registration-invalidate --task-id ... --session-id ... --token-file ... --worker ... --worker-timeout ...`.
- Governance adds `canonical_recovery` mode `prior_boot_zero_client_invalidation_v1`; this mode is metadata-only and requires canonical registration PRESENT.
- The invalidation operation never invokes `launch`, `rollback`, `_kill`, Docker stop/restart/rm, GUI input, credentials or memory observation.

- [ ] **Step 1: Write failing worker boot-identity tests**

Extend positive preflight fixtures to return a deterministic current container boot id and require:

```python
payload = module.collect_preflight(runner=fake)
self.assertRegex(payload['boot_id_sha256'], r'^[0-9a-f]{64}$')
unsigned = dict(payload); fingerprint = unsigned.pop('preflight_fingerprint')
self.assertEqual(fingerprint, module._fingerprint(unsigned))
```

Add negatives for unreadable/malformed boot id. Run worker tests and observe RED before implementation.

- [ ] **Step 2: Implement boot identity in Kasm preflight and confirm GREEN**

Read `/proc/sys/kernel/random/boot_id` inside the exact target container, validate the UUID text, and SHA-256 the exact file bytes (including its line ending) to match the existing Kasm probe's `sha256sum` semantics. Do not use host boot identity. Include the hash in the persisted preflight record and fingerprint.

- [ ] **Step 3: Write failing invalidation transaction tests**

Add deterministic transition tests requiring all of:

```text
registration PRESENT and exact-current-fenced
proof_kind == existing_runtime_adoption_v1
state == UNKNOWN
state_evidence in approved fail-closed values
current lease generation > registration lease generation
worker preflight #1 => exact target + current boot != registered boot + 0 candidates + 0 windows
lease/current-registration revalidation
worker preflight #2 => identical stable signature
_remove(old) only
lease revalidation
worker preflight #3 => still 0 candidates/windows on same current boot/container/package
registration ABSENT
```

Negative cases: same boot epoch, registration absent, legacy/non-adoption registration, non-fail-closed state, old/current lease generation not newer, runtime-locator namespace mismatch, current container id incompatible with registered locator, preflight drift, candidate/window presence, registration race, and candidate appearance after deletion. Assert no launch/rollback/process signal occurs.

- [ ] **Step 4: Implement `boot-epoch-registration-invalidate` minimally**

Reuse the worker `preflight` operation, existing `_read()`, `_remove(old)`, `_lease()` and cancellation checks. Compare registration locator `docker:otclient-track-a-kasmvnc:<recorded-id>` against the preflight full id; accept only exact full-id equality or an unambiguous recorded hex prefix of at least 12 characters. Never restore the prior-boot registration after successful `_remove(old)`.

- [ ] **Step 5: Add governance mode under existing `canonical_recovery`**

Add constant `PRIOR_BOOT_ZERO_CLIENT_INVALIDATION_MODE = 'prior_boot_zero_client_invalidation_v1'`. Require:

```yaml
runtime_access: canonical_recovery
canonical_registration: PRESENT
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
mutation_authorized: false
recovery_mode: prior_boot_zero_client_invalidation_v1
gate_a: REQUIRED_NOT_PROVEN  # or PASS after live acquisition
target_uniqueness: UNKNOWN   # zero-client proof is established by the transition, not a singleton target claim
```

For pending admission allow `canonical_lease_generation: UNKNOWN` and require a positive known `registration_lease_generation`; after Gate A PASS require a newer positive current generation. Document that this recovery mode can only invalidate a prior-boot fail-closed registration after the reviewed zero-client proof; it cannot replace/rebind/register/launch a client.

- [ ] **Step 6: Run focused GREEN regression**

```bash
python3 .github/scripts/test_tibia_official_client_re_kasm_bootstrap_worker.py -v
python3 .github/scripts/test_tibia_official_client_re_canonical_live_transition.py -v
python3 .github/scripts/test_track_a_agent_runtime_governance.py
python3 -m py_compile .github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py .github/scripts/tibia-official-client-re-canonical-live-transition.py .github/scripts/test_track_a_agent_runtime_governance.py
```

Expected: all new invalidation tests and all existing bootstrap/adoption/rebind/recovery/Gate-B regressions PASS.

- [ ] **Step 7: Commit Task 2A**

```bash
git add .github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py \
        .github/scripts/test_tibia_official_client_re_kasm_bootstrap_worker.py \
        .github/scripts/tibia-official-client-re-canonical-live-transition.py \
        .github/scripts/test_tibia_official_client_re_canonical_live_transition.py \
        .github/scripts/test_track_a_agent_runtime_governance.py \
        docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
git commit -m "feat(track-a): invalidate prior-boot zero-client registration"
```

---

### Task 3: Main-only physical workflow and deterministic security contract

**Files:**
- Create: `.github/workflows/track-a-kasm-canonical-bootstrap.yml`
- Create: `.github/scripts/test_track_a_kasm_canonical_bootstrap_workflow.py`

**Interfaces:**
- PR event produces only hosted contract validation.
- `workflow_dispatch` live job requires exact input `RECOVER_PRIOR_BOOT_AND_CREATE_NEW_KASM_CANONICAL`.
- Live execution consumes two task checkpoints: `OTC-20260829-track-a-kasm-prior-boot-registration-invalidation` (metadata-only canonical recovery) and `OTC-20260829-track-a-kasm-canonical-bootstrap-live` (create-new bootstrap).
- Live job consumes a separate future task `docs/agents/tasks/active/OTC-20260829-track-a-kasm-canonical-bootstrap-live.md`; this implementation PR does not create that file.
- Live job invokes the merged controller operation `kasm-bootstrap` directly after acquiring the canonical lease, then releases the lease in a cleanup trap.

- [ ] **Step 1: Write failing workflow security contract test**

The Python test must parse/read the workflow and assert:

```python
self.assertIn('pull_request:', text)
self.assertIn('workflow_dispatch:', text)
self.assertIn("github.event_name == 'workflow_dispatch'", live_prefix)
self.assertIn('github.actor == github.repository_owner', live_prefix)
self.assertIn("github.ref == 'refs/heads/main'", live_prefix)
self.assertIn("inputs.authorization == 'CREATE_NEW_KASM_CANONICAL_BOOTSTRAP'", live_prefix)
self.assertIn('runs-on: [otclient, synology]', live_job)
self.assertNotIn('${{ secrets.', text)
self.assertNotIn('TIBIA_TEST_EMAIL', text)
self.assertNotIn('TIBIA_TEST_PASSWORD', text)
self.assertIn('GITHUB_RUN_ATTEMPT', live_job)
self.assertIn('kasm-bootstrap', live_job)
self.assertNotIn('docker exec -d', live_job)
```

Also assert the implementation task has `runtime_access: none`, `mutation_authorized: false`, credentials/login/process-control false and physical action budget/count `0/0`.

Require the live workflow to validate the future live task exactly as:

```yaml
runtime_access: canonical_bootstrap
runtime_owner_task: OTC-20260829-track-a-kasm-canonical-bootstrap-live
runtime_namespace: canonical-live-runtime
canonical_registration: ABSENT
canonical_lease_generation: UNKNOWN
registration_lease_generation: NOT_APPLICABLE
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: PASS
target_uniqueness: UNKNOWN
mutation_authorized: true
bootstrap_mode: create_new
bootstrap_attempt_limit: 1
credentials_allowed: false
login_allowed: false
relogin_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: true
physical_action_budget: 1
physical_action_count: 0
```

and a non-empty `live_runtime_authorization_source`.

- [ ] **Step 2: Run workflow test and confirm RED**

Run:

```bash
python3 .github/scripts/test_track_a_kasm_canonical_bootstrap_workflow.py -v
```

Expected: FAIL because workflow does not exist.

- [ ] **Step 3: Implement hosted PR contract job**

Use `pull_request` path filters for the worker, transition, focused tests, workflow test, workflow, task, plan, catalogue/changelog/evidence paths.

The hosted job must:

```bash
python3 .github/scripts/test_tibia_official_client_re_kasm_bootstrap_worker.py -v
python3 .github/scripts/test_tibia_official_client_re_canonical_live_transition.py -v
python3 .github/scripts/test_tibia_official_client_re_kasm_existing_runtime_probe.py -v
python3 .github/scripts/test_track_a_kasm_canonical_bootstrap_workflow.py -v
python3 .github/scripts/test_track_a_agent_runtime_governance.py \
  --changed-from "$BASE_SHA" --expected-branch "$HEAD_BRANCH"
python3 .github/scripts/audit_track_a_selfhosted_pr_boundary.py --base "$BASE_SHA"...HEAD
python3 -m py_compile .github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py .github/scripts/test_tibia_official_client_re_kasm_bootstrap_worker.py .github/scripts/tibia-official-client-re-canonical-live-transition.py .github/scripts/test_tibia_official_client_re_canonical_live_transition.py .github/scripts/test_track_a_kasm_canonical_bootstrap_workflow.py
git diff --check "$BASE_SHA"...HEAD
```

Parse YAML with Ruby as used elsewhere in the repo.

- [ ] **Step 4: Implement live job scheduling gate**

The self-hosted job `if:` must appear before `runs-on` and be exactly a conjunction of owner/trusted-dispatch facts; no `pull_request` branch is admissible:

```yaml
if: >-
  github.event_name == 'workflow_dispatch' &&
  github.actor == github.repository_owner &&
  github.ref == 'refs/heads/main' &&
  inputs.authorization == 'CREATE_NEW_KASM_CANONICAL_BOOTSTRAP'
runs-on: [otclient, synology]
```

Add `concurrency` with `cancel-in-progress: false` for the Kasm canonical bootstrap live lane.

- [ ] **Step 5: Implement trusted-main/admission preflight**

Before lease acquisition:
- checkout `ref: main`, `persist-credentials: false`, `fetch-depth: 0`;
- require `RUNNER_NAME == synology-otclient-01`, exact repository and `GITHUB_RUN_ATTEMPT == 1`;
- prove checkout SHA equals current `git ls-remote origin refs/heads/main`;
- run focused deterministic tests;
- require the separate live task file and validate it with `test_track_a_agent_runtime_governance.py` plus an exact frontmatter dictionary check for every field above;
- reject empty/UNKNOWN/NONE `live_runtime_authorization_source`.

No secret access appears anywhere in this workflow. The live job first validates/runs the metadata-only prior-boot invalidation task under its own recovery lease, releases it, proves `runtime-registration.json` is absent, then acquires a new lease for the bootstrap task and invokes `python3 "$transition" kasm-bootstrap` exactly once.

- [ ] **Step 6: Implement lease + transition + release**

Use:

```bash
task='OTC-20260829-track-a-kasm-canonical-bootstrap-live'
session="github-${GITHUB_RUN_ID}-${GITHUB_RUN_ATTEMPT}"
token_root="/home/runner/_work/_otclient_tibia_re_state/tasks/$task/runtime"
token="$token_root/canonical-lease-token"
lease='.github/scripts/tibia-official-client-re-canonical-live-lease'
transition='.github/scripts/tibia-official-client-re-canonical-live-transition.py'
worker='.github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py'
probe='.github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py'
```

Acquire/validate the lease with a cleanup trap. Recheck `main` immediately before process control. Invoke:

```bash
python3 "$transition" kasm-bootstrap \
  --task-id "$task" \
  --session-id "$session" \
  --token-file "$token" \
  --worker "$worker" \
  --probe "$probe" \
  --worker-timeout 120
```

Then release the lease and remove the token. Do not nest `kasm-bootstrap` under ordinary `guard-run`; the transition's `_supervise` owns the canonical flock for this creation transaction.

- [ ] **Step 7: Add sanitized post-transaction verification**

Without process-memory access, read only the canonical registration metadata and require exact fence, `proof_kind == existing_runtime_adoption_v1`, full Docker runtime locator for `otclient-track-a-kasmvnc`, `candidate_count == 1`, `state == UNKNOWN`, `bootstrap_provenance == kasm_create_new_v1`, positive registration/lease generation and positive PID/start. Print only non-secret scalar/boolean PASS markers and run/job/SHA identifiers; do not print raw window title or environment.

- [ ] **Step 8: Run workflow/security/static suites**

Run:

```bash
python3 .github/scripts/test_track_a_kasm_canonical_bootstrap_workflow.py -v
python3 .github/scripts/test_track_a_selfhosted_pr_boundary.py
python3 .github/scripts/audit_track_a_selfhosted_pr_boundary.py --base "$BASE_SHA"...HEAD
python3 .github/scripts/test_track_a_agent_runtime_governance.py \
  --changed-from "$BASE_SHA" --expected-branch feat/OTC-20260829-track-a-kasm-canonical-bootstrap-v2
ruby -e 'require "yaml"; YAML.load_file(ARGV[0]); puts "YAML_PARSE=PASS"' \
  .github/workflows/track-a-kasm-canonical-bootstrap.yml
git diff --check "$BASE_SHA"...HEAD
```

Expected: PASS; self-hosted job cannot be scheduled by a PR.

- [ ] **Step 9: Commit Task 3**

```bash
git add .github/workflows/track-a-kasm-canonical-bootstrap.yml \
        .github/scripts/test_track_a_kasm_canonical_bootstrap_workflow.py
git commit -m "ci(track-a): add guarded Kasm bootstrap workflow"
```

---

### Task 4: Repository integration, evidence and final exact-head validation

**Files:**
- Modify: `docs/agents/tasks/active/OTC-20260829-track-a-kasm-canonical-bootstrap.md`
- Modify: `docs/agents/MODULE_CATALOG.md`
- Modify: `docs/agents/CHANGELOG.md`
- Create: `docs/agents/evidence/OTC-20260829-track-a-kasm-canonical-bootstrap/repository-validation.md`
- Existing: `docs/superpowers/plans/2026-08-29-track-a-kasm-canonical-bootstrap.md`

**Interfaces:**
- Documents the reusable Kasm bootstrap worker/controller operation and exact safety boundary.
- Does not claim physical E2E; physical execution remains `NOT_APPLICABLE` for this repository-only implementation task.

- [ ] **Step 1: Update module catalogue narrowly**

Add/extend the Track A canonical runtime tooling row to name the Kasm `create_new` bootstrap worker/operation, exact fence, Docker/Kasm target and rollback identity boundary. State clearly that implementation presence does not itself grant live authority.

- [ ] **Step 2: Update changelog**

Record behavior-level availability of the reviewed Kasm-aware creation path and its separation from legacy host bootstrap/adopt-existing. Do not claim a live runtime was created.

- [ ] **Step 3: Run complete focused validation**

On exact branch head run all three new/focused test modules, existing Kasm probe tests, canonical transition suite, Track A governance, reusable self-hosted boundary scanner/audit, YAML parse, Python compile and `git diff --check`.

- [ ] **Step 4: Persist repository validation evidence**

Record exact branch head, exact base, commands/results, RED evidence commit/run if available, final GREEN run/job IDs, changed-file scope, `runtime_access:none`, physical E2E `NOT_APPLICABLE` reason, no secrets/runtime action and remaining post-merge live prerequisite.

- [ ] **Step 5: Update task checkpoint to `validating`**

Set exact base/head, tests and one next action: obtain exact-head GitHub checks, independent audit/review, zero threads, current-main verification, then merge.

- [ ] **Step 6: Review full diff and changed filenames**

Require every changed path to be inside the declared `owned_paths`; reject unrelated formatting or changes to PR #796/#798-owned security files unless an explicit restack conflict made a narrow update unavoidable.

- [ ] **Step 7: Mark PR Ready only after local/hosted GREEN**

Observe ready-state `CI / Required` and any Track A focused/governance/self-hosted audit workflows on the exact final head. If main advances, sync without discarding concurrent work and rerun exact-head checks.

- [ ] **Step 8: Resolve material review findings**

Treat central Spark P0/P1 comments, independent reviewer findings, requested changes and unresolved inline threads as blockers. Fix root cause and rerun invalidated tests; never self-approve as independent review.

- [ ] **Step 9: Squash merge only after all gates PASS**

Use expected exact head SHA. Immediately fresh-check `main` after merge and verify the merged worker/transition/workflow bytes are the reviewed version.

- [ ] **Step 10: Repository-only closeout/archive**

Archive the implementation task with ownership released, physical E2E `NOT_APPLICABLE` because runtime access was `none`, merge SHA, validation evidence and exactly one next action: create a separate live RUNTIME admission task for one Kasm canonical bootstrap invocation.

---

### Task 5: Post-merge two-phase live admission and return to `gameWindowState`

**Files:**
- Separate follow-up PR/task only after Task 4 is terminal. Do not include it in the implementation PR.

**Interfaces:**
- Creates `OTC-20260829-track-a-kasm-canonical-bootstrap-live` with exact `canonical_bootstrap/create_new` authority and one physical action budget.
- Consumes merged `track-a-kasm-canonical-bootstrap.yml` only from protected current `main`.
- On PASS, releases canonical lease and hands back to `OTC-20260828-game-window-state-qualification`.

- [ ] **Step 1: Fresh-check current main and runtime facts without process control**

Require current Kasm container locator and exact zero-client condition. If an exact client already exists, do not run `create_new`; route to the applicable adopt/recovery lifecycle instead.

- [ ] **Step 2: Create/review/merge one-shot live admission task**

Create and merge two separate live authority records required by Task 3: (1) `OTC-20260829-track-a-kasm-prior-boot-registration-invalidation` using `canonical_recovery` + `recovery_mode: prior_boot_zero_client_invalidation_v1`, PRESENT registration and zero physical action budget; (2) `OTC-20260829-track-a-kasm-canonical-bootstrap-live` using `canonical_bootstrap` + `create_new`, ABSENT registration checkpoint and one launch budget. Bind both to the owner's approval of this recovery continuation. Do not weaken implementation workflow checks.

- [ ] **Step 3: Dispatch exactly one main workflow attempt**

Use authorization `CREATE_NEW_KASM_CANONICAL_BOOTSTRAP`, reject rerun attempts, and inspect run/job logs for Gate A, zero-client preflight, exact launch, three stable Kasm proofs, registration commit, safe detach and lease release.

- [ ] **Step 4: If bootstrap fails, terminalize fail-closed before gameWindow memory work**

Verify rollback outcome and canonical registration disposition. Do not manually launch the client or reuse a partial registration.

- [ ] **Step 5: If bootstrap passes, release/close live authority and rerun gameWindow preflight**

Post `PREFLIGHT_GAME_WINDOW_STATE_QUALIFICATION` on PR #756 from fresh current main. Require memory-free READY before START.

- [ ] **Step 6: Start one continuous logger and engage owner only when capture is active**

Post `START_GAME_WINDOW_STATE_QUALIFICATION`, prove `Capture continuous bounded state log` is `in_progress`, then ask owner for the four manual phases only:

```text
1 = LOGIN_SCREEN
2 = CHARACTER_SELECT
3 = WORLD
4 = WORLD_EXIT
```

Revalidate the same run before each phase marker; never splice sessions.

- [ ] **Step 7: Validate causal artifact and preserve non-promotion flags**

Require:

```text
LOGIN_SCREEN        != INGAME
CHARACTER_SELECT    != INGAME
WORLD               == INGAME
WORLD_EXIT          != INGAME
IN_GAME_CLAIMED=false
semantic_promotion_performed=false
```

If incomplete/ambiguous, terminal `BLOCKED_FAIL_CLOSED` with durable evidence and no semantic promotion.

- [ ] **Step 8: Only after causal PASS create a separate semantic-promotion PR**

Require independent exact-head review. No silent promotion and no self-approval as independent reviewer.
