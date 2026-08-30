# Local Track A Vision Agent Supervisor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the repository-owned, observable local vision-agent foundation by extending the existing TIBIA RE Control Center with persistent agent sessions, provenance-aware owner/supervisor control, reusable Qwen3-VL visual sensing, deterministic state reconciliation, evidence/result envelopes, a narrow supervisor MCP surface, and fake/offline execution proof while keeping Official Tibia runtime access and physical mutation unbound.

**Architecture:** The approved “thin persistent Molehill session/control service” is realized by extending the already-merged `tools/tibia_re_control_center` Package A/B/C/D foundation rather than creating a second service. PR #790 visual/Ollama safety primitives are extracted into an importable reusable module and consumed by Control Center. Existing Package D guarded-dispatch and Track A bridge semantics are reused as the future effect boundary, but this plan does not promote the current Official adapter to the current client fence, bind credentials, or perform any Official Tibia action.

**Tech Stack:** Python 3.12-compatible stdlib, `unittest`, SQLite/WAL, `http.server` loopback Control API/UI, stdio JSON-RPC MCP, Ollama loopback HTTP, existing Control Center artifact/recorder/canonical JSON utilities.

**Spec:** `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`

## Global Constraints

- Implementation work starts only from a fresh implementation branch/worktree after live `main`, open-PR ownership, and this plan/spec are revalidated. Use `superpowers:using-git-worktrees` before edits.
- The implementation task is repository-only: `runtime_access: none`, `mutation_authorized: false`, `credentials_allowed: false`, `login_allowed: false`, `character_selection_allowed: false`, `gui_input_authorized: false`, `process_control_authorized: false`, `process_memory_access_allowed: false`, `physical_action_budget: 0`, `physical_action_count: 0`.
- Never enable `mcp_servers.cua_repl`, start CUA, modify the Molehill supervisor services, restart `muse-ollama-proxy`, touch the Official Tibia runtime, or consume credentials while executing this plan.
- Reuse Control Center `SQLitePersistentStore`, durable `ControlState` STOP/reset semantics, request idempotency, events/artifacts, `MutationCoordinator`, `OfficialTibiaAdapter`, and `CanonicalTrackAAuthorityBridge`. Do not create a second persistence/control backend.
- The current `tools/tibia_re_control_center/official_adapter.py` promotion fence is intentionally not the current Track A fence. Do not change `CURRENT_CLIENT_SHA256` merely to make Package D actionable. Current-client physical binding requires a separate reviewed task and runtime authorization.
- The canonical current Track A client fence remains `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`; this plan may record it as evidence metadata but must not claim a live matching runtime.
- Qwen visual profile is exactly `qwen3-vl:4b-instruct-q4_K_M`, digest `ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b`, `num_ctx=4096`, `num_predict=256`, `temperature=0`.
- Model output remains untrusted, `visual_only: true`, `structural_authority: false`; visual evidence alone never becomes `IN_GAME`.
- One local model resident/inferencing at a time. Different, multiple, or unknown residency fails closed. Never evict an unowned resident model to continue.
- Raw secrets are rejected from task envelopes, agent events, session storage, dashboard/chat persistence, model prompts, artifacts, and logs. `secret_capability_ref` is opaque metadata only and is not resolved in this plan.
- Model-facing capabilities contain named semantic operations only. No raw coordinate click, arbitrary text typing, shell, Docker, process control, debugger, memory or credential getter is exposed.
- Owner `STOP`/`PAUSE` dominates supervisor/model proposals. Restart/reconnect never auto-resumes a stopped or paused physical-action state.
- PR #615 is an old untrusted/open PoC branch. Reuse only independently revalidated invariants (loopback-only Ollama, digest verification, strict output validation, secret rejection, one-model lifecycle). Do not merge/cherry-pick its stale runtime assumptions wholesale.
- Credential broker implementation, authenticated Synology↔Molehill production transport deployment, and Official-client physical transition execution are excluded from this repository-only foundation and require separate plans/authorizations.

---

### Task 1: Extract the PR #790 vision/Ollama safety core into an importable module

**Files:**
- Create: `tools/tibia_re_vision/__init__.py`
- Create: `tools/tibia_re_vision/evidence.py`
- Create: `tools/tibia_re_vision/ollama.py`
- Modify: `tools/tibia-re-vision-benchmark/vision_benchmark.py`
- Create: `tests/tools/tibia_re_vision/test_evidence.py`
- Create: `tests/tools/tibia_re_vision/test_ollama.py`
- Existing regression tests: `tools/tibia-re-vision-benchmark/tests/test_vision_benchmark.py`, `tools/tibia-re-vision-benchmark/tests/test_ollama_adapter.py`

**Interfaces:**
- Produces `tools.tibia_re_vision.evidence.validate_visual_evidence(payload: object) -> list[str]`.
- Produces `validate_model_observation(observation: object) -> list[str]`, `normalize_ocr_transcription(...) -> dict[str, object]`, `validate_input_manifest(metadata: object, image_path: str | Path) -> str`, and `sha256_file(path: str | Path) -> str`.
- Produces `tools.tibia_re_vision.ollama.admit_residency(resident_models: list[str] | None, target: str) -> tuple[bool, str]`, `query_ollama_ps`, `query_ollama_model_digest`, `run_ollama_trial`, and `release_ollama_model_if_owned` with the same behavior as PR #790.
- `tools/tibia-re-vision-benchmark/vision_benchmark.py` must import/re-export these names so its frozen tests and runner scripts remain source-compatible.

- [ ] **Step 1: Write RED tests for reusable imports and unchanged hard gates**

```python
# tests/tools/tibia_re_vision/test_evidence.py
import unittest
from tools.tibia_re_vision.evidence import validate_visual_evidence


class ReusableVisionEvidenceTests(unittest.TestCase):
    def test_visual_only_non_authority_is_mandatory(self):
        payload = {
            "schema_version": 1,
            "capture": {"evidence_ref": "fixture:black", "sha256": "a" * 64, "source_monotonic_ns": None},
            "model": {"model_profile_id": "profile"},
            "observation": {"screen_class": "UNKNOWN", "visible_text": [], "ui_objects": [], "appeared": [], "disappeared": [], "changed": []},
            "quality": {"schema_valid": True, "visual_only": False, "structural_authority": False, "unknown_fields": []},
        }
        self.assertIn("quality.visual_only must be true", validate_visual_evidence(payload))
```

```python
# tests/tools/tibia_re_vision/test_ollama.py
import unittest
from tools.tibia_re_vision.ollama import admit_residency


class ReusableOllamaTests(unittest.TestCase):
    def test_foreign_or_multiple_residency_fails_closed(self):
        self.assertEqual((False, "DIFFERENT_RESIDENT_MODEL"), admit_residency(["gemma4:12b"], "qwen3-vl:4b-instruct-q4_K_M"))
        self.assertEqual((False, "MULTIPLE_RESIDENT_MODELS"), admit_residency(["qwen3-vl:4b-instruct-q4_K_M", "gemma4:12b"], "qwen3-vl:4b-instruct-q4_K_M"))
```

- [ ] **Step 2: Run RED tests**

Run:
```bash
python -m unittest discover -s tests/tools/tibia_re_vision -p "test_*.py" -v
```
Expected: FAIL because `tools.tibia_re_vision` does not exist.

- [ ] **Step 3: Move only reusable evidence/provider functions, preserving behavior**

Create `evidence.py` with the existing PR #790 constants/functions and `ollama.py` with the existing loopback/provider/residency functions. Keep scoring/benchmark-only functions (`WEIGHTS`, `score_profile`, `evaluate_hard_gates`, benchmark trial logic) in `vision_benchmark.py`.

`tools/tibia_re_vision/__init__.py` must explicitly export only the reusable surface:

```python
from .evidence import (
    SCREEN_CLASSES,
    normalize_ocr_transcription,
    sha256_file,
    validate_input_manifest,
    validate_model_observation,
    validate_visual_evidence,
)
from .ollama import (
    admit_residency,
    query_ollama_model_digest,
    query_ollama_ps,
    release_ollama_model_if_owned,
    run_ollama_trial,
)

__all__ = [name for name in globals() if not name.startswith("_")]
```

In `vision_benchmark.py`, import these names from `tools.tibia_re_vision` and remove only their duplicate definitions. Do not change the fixture schema, allowed screen classes, hard-gate semantics, endpoint loopback restriction, or provider payload.

- [ ] **Step 4: Run reusable and frozen benchmark tests**

Run:
```bash
python -m unittest discover -s tests/tools/tibia_re_vision -p "test_*.py" -v
python -m unittest discover -s tools/tibia-re-vision-benchmark/tests -p "test_*.py" -v
```
Expected: PASS; the existing benchmark tests remain unchanged in behavior.

- [ ] **Step 5: Commit**

```bash
git add tools/tibia_re_vision tools/tibia-re-vision-benchmark/vision_benchmark.py tests/tools/tibia_re_vision
git commit -m "refactor(track-a): expose reusable vision safety core"
```

---

### Task 2: Add strict agent protocol, provenance, state and named-action types

**Files:**
- Create: `tools/tibia_re_control_center/agent_protocol.py`
- Create: `tests/tools/tibia_re_control_center/test_agent_protocol.py`
- Modify: `tools/tibia_re_control_center/__init__.py`

**Interfaces:**
- Produces enums `AgentOperationalState`, `AgentProvenance`, `AgentVisualState`, `NamedAgentAction`, `OwnerControlCommand`, `ResultStatus`.
- Produces immutable dataclasses `ClientIdentity`, `TaskEnvelope`, `AgentEvent`, `ResultEnvelope`, `AgentSessionRecord`.
- `TaskEnvelope.from_mapping(value: Mapping[str, Any]) -> TaskEnvelope` requires exact keys and rejects unknown/secret-bearing data.
- `AgentEvent.new(...)` creates an event with `seq=0`; persistence assigns the durable positive sequence.
- Named mutating actions are exactly `SUBMIT_AUTHORIZED_LOGIN`, `SELECT_CHARACTER`, `ENTER_WORLD`, `EXIT_WORLD`; `SCREENSHOT` is read-only and not part of the physical mutation budget.

- [ ] **Step 1: Write protocol RED tests**

```python
import unittest
from tools.tibia_re_control_center.agent_protocol import TaskEnvelope, ValidationError


class AgentProtocolTests(unittest.TestCase):
    def test_raw_credentials_are_rejected(self):
        body = {
            "schema": "otclient.local-agent.task.v1",
            "session_id": "session-1",
            "task_id": "task-1",
            "run_id": "run-1",
            "idempotency_key": "idem-1",
            "trusted_main_sha": "a" * 40,
            "client_identity": {"version": "NOT_APPLICABLE", "size": "NOT_APPLICABLE", "sha256": "NOT_APPLICABLE"},
            "objective": "offline fixture classification",
            "allowed_actions": ["SCREENSHOT"],
            "physical_action_budget": 0,
            "max_attempts": 1,
            "deadline_epoch_ms": 2_000_000_000_000,
            "runtime_access": "none",
            "required_evidence": ["VISUAL_EVIDENCE"],
            "secret_capability_ref": None,
            "password": "forbidden",
        }
        with self.assertRaises(ValidationError):
            TaskEnvelope.from_mapping(body)
```

Add tests proving:
- exact-key validation;
- `trusted_main_sha` is exactly 40 lowercase hex chars;
- `physical_action_budget` and `max_attempts` are bounded non-negative integers;
- runtime class is from the current admission vocabulary;
- `secret_capability_ref` uses `validate_opaque_id` and cannot contain path separators;
- no action outside the named allowlist is accepted;
- `WORLD_VISUAL` is distinct from any runtime `IN_GAME` state.

- [ ] **Step 2: Run RED test**

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_protocol -v
```
Expected: FAIL because `agent_protocol.py` is absent.

- [ ] **Step 3: Implement strict dataclasses and validators**

Use existing `ValidationError`, `checked_non_negative`, `require_exact_keys`, and `validate_opaque_id` from `model.py`. The critical enum definitions are:

```python
class AgentOperationalState(str, Enum):
    OFFLINE = "OFFLINE"
    IDLE = "IDLE"
    OBSERVING = "OBSERVING"
    RUNNING = "RUNNING"
    WAITING_MODEL_SLOT = "WAITING_MODEL_SLOT"
    PAUSED = "PAUSED"
    PAUSED_AUTHORITY = "PAUSED_AUTHORITY"
    DEGRADED = "DEGRADED"
    STOPPED = "STOPPED"
    TERMINAL = "TERMINAL"


class AgentProvenance(str, Enum):
    OWNER = "OWNER"
    SUPERVISOR = "SUPERVISOR"
    SYSTEM = "SYSTEM"
    MODEL = "MODEL"
    SENSOR = "SENSOR"
    RUNTIME = "RUNTIME"


class NamedAgentAction(str, Enum):
    SCREENSHOT = "SCREENSHOT"
    SUBMIT_AUTHORIZED_LOGIN = "SUBMIT_AUTHORIZED_LOGIN"
    SELECT_CHARACTER = "SELECT_CHARACTER"
    ENTER_WORLD = "ENTER_WORLD"
    EXIT_WORLD = "EXIT_WORLD"
```

Do not define raw click/type/shell action variants.

- [ ] **Step 4: Run protocol tests and compile**

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_protocol -v
python -m compileall -q tools/tibia_re_control_center/agent_protocol.py
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/tibia_re_control_center/agent_protocol.py tools/tibia_re_control_center/__init__.py tests/tools/tibia_re_control_center/test_agent_protocol.py
git commit -m "feat(control-center): add local agent protocol"
```

---

### Task 3: Extend the existing SQLite store with durable agent sessions and task/result idempotency

**Files:**
- Modify: `tools/tibia_re_control_center/persistent_store.py`
- Create: `tests/tools/tibia_re_control_center/test_agent_persistence.py`

**Interfaces:**
- Produces `write_agent_session(record: AgentSessionRecord) -> None` and `load_agent_session(session_id: str) -> AgentSessionRecord | None`.
- Produces `accept_agent_task(envelope: TaskEnvelope) -> dict[str, Any]`; same idempotency key + same canonical envelope is replay-safe, while the same key + different envelope raises `IDEMPOTENCY_CONFLICT`.
- Produces `finish_agent_task(idempotency_key: str, result: ResultEnvelope) -> None` and `load_agent_task(idempotency_key: str) -> dict[str, Any] | None`.
- Produces `append_agent_event(event: AgentEvent) -> AgentEvent` by using the existing `events` table sequence; returned `event.seq` equals the committed SQLite sequence.
- Existing `append_events`/`list_events`, action/budget stores, artifacts, RequestLedger and schema remain backward compatible.

- [ ] **Step 1: Write restart/idempotency/secret RED tests**

```python
import tempfile
import unittest
from pathlib import Path
from tools.tibia_re_control_center.agent_protocol import AgentOperationalState, AgentSessionRecord
from tools.tibia_re_control_center.persistent_store import SQLitePersistentStore


class AgentPersistenceTests(unittest.TestCase):
    def test_session_survives_restart(self):
        with tempfile.TemporaryDirectory() as td:
            first = SQLitePersistentStore(Path(td))
            first.write_agent_session(AgentSessionRecord("session-1", AgentOperationalState.PAUSED, None, 7, True))
            first.close()
            second = SQLitePersistentStore(Path(td))
            self.assertEqual(AgentOperationalState.PAUSED, second.load_agent_session("session-1").operational_state)
            self.assertTrue(second.load_agent_session("session-1").pause_latched)
            second.close()
```

Add tests that:
- event sequence is positive and strictly increasing;
- task replay does not create a second run;
- conflicting idempotency envelope is rejected;
- persisted event/task/result containing a secret-class key is rejected by the existing privacy guard;
- existing Package B database opened after schema upgrade remains readable.

- [ ] **Step 2: Run RED test**

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_persistence -v
```
Expected: FAIL because agent persistence methods/tables are absent.

- [ ] **Step 3: Add additive schema and persistence methods**

Extend `_create_schema()` only additively:

```sql
CREATE TABLE IF NOT EXISTS agent_sessions (
    session_id TEXT PRIMARY KEY,
    body TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS agent_tasks (
    idempotency_key TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    run_id TEXT NOT NULL UNIQUE,
    envelope_hash TEXT NOT NULL,
    body TEXT NOT NULL,
    result TEXT
);
```

Use existing canonical `_dump`, `_load`, transactions and secret checks. Do not introduce another SQLite file.

For event persistence, insert the event body without a trusted sequence, read `lastrowid`, rebuild the immutable `AgentEvent` with that sequence, then update the same row within the same transaction before commit. Do not derive sequence in memory.

- [ ] **Step 4: Run new and Package B persistence regressions**

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_persistence -v
python -m unittest tests.tools.tibia_re_control_center.test_package_b.PackageBTests.test_24_restart_preserves_run_activation_action_and_budget_truth -v
python -m unittest tests.tools.tibia_re_control_center.test_package_b.PackageBTests.test_26_bounded_event_polling_reports_backpressure_for_stale_cursor -v
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/tibia_re_control_center/persistent_store.py tests/tools/tibia_re_control_center/test_agent_persistence.py
git commit -m "feat(control-center): persist local agent sessions"
```

---

### Task 4: Implement the deterministic agent session coordinator and owner-control precedence

**Files:**
- Create: `tools/tibia_re_control_center/agent_session.py`
- Create: `tests/tools/tibia_re_control_center/test_agent_session.py`
- Modify: `tools/tibia_re_control_center/control_domain.py`

**Interfaces:**
- Produces `BoundedActionExecutor` protocol with `execute(request: AgentActionRequest) -> AgentActionReceipt` and `screenshot(session_id: str, run_id: str) -> CaptureReceipt`.
- Produces `NullBoundedActionExecutor` which refuses every mutating named action and returns no physical effect.
- Produces `AgentSessionCoordinator(store: SQLitePersistentStore, control: MutationCoordinator, executor: BoundedActionExecutor | None = None)`.
- Coordinator methods: `ensure_session(session_id)`, `submit_task(envelope)`, `owner_control(session_id, command)`, `record_message(session_id, provenance, text)`, `propose_named_action(...)`, `complete_run(...)`, `snapshot(session_id)`.
- Production default executor is always `NullBoundedActionExecutor` in this plan.

- [ ] **Step 1: Write RED tests for STOP/PAUSE/restart/idempotency**

```python
class AgentSessionTests(unittest.TestCase):
    def test_stop_dominates_supervisor_action(self):
        session = self.coordinator.ensure_session("session-1")
        self.coordinator.owner_control("session-1", OwnerControlCommand.STOP)
        result = self.coordinator.propose_named_action(
            session_id="session-1",
            run_id="run-1",
            action=NamedAgentAction.ENTER_WORLD,
            provenance=AgentProvenance.SUPERVISOR,
        )
        self.assertEqual("REFUSED_STOP_LATCHED", result.status)
        self.assertEqual(0, result.low_level_event_count)
```

Add tests proving:
- `PAUSE` blocks effects but preserves session/run/evidence state;
- service reconstruction from the same store preserves `PAUSE` and global STOP latches;
- `RESUME` refuses while Control Center recovery/STOP safety cannot be reset;
- model provenance can propose but never approve an action;
- supervisor cannot override owner STOP/PAUSE;
- `SCREENSHOT` is read-only and does not decrement physical action budget;
- mutating action with default `NullBoundedActionExecutor` is refused with zero effect;
- duplicate task idempotency never invokes executor twice;
- an executor exception before effect is `FAIL/NOT_PERFORMED`; an explicit unknown post-effect receipt is `INCONCLUSIVE/PERFORMED_UNKNOWN` and is not retried.

- [ ] **Step 2: Run RED tests**

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_session -v
```
Expected: FAIL because the coordinator does not exist.

- [ ] **Step 3: Implement minimal fail-closed coordinator**

Use these production-safe defaults:

```python
class NullBoundedActionExecutor:
    def execute(self, request: AgentActionRequest) -> AgentActionReceipt:
        return AgentActionReceipt(
            action_id=request.action_id,
            status="REFUSED_EXECUTOR_UNBOUND",
            performed=False,
            outcome_known=True,
            low_level_event_count=0,
            evidence_refs=(),
        )

    def screenshot(self, session_id: str, run_id: str) -> CaptureReceipt:
        return CaptureReceipt(status="UNAVAILABLE", artifact_ref=None, sha256=None, secret_safe=False)
```

The coordinator must consult existing `MutationCoordinator.control_state.stop_latched` before any action proposal and must never clear that latch in response to a model/supervisor message. Only an `OWNER` `RESUME` path may request existing reset semantics, and reset refusal remains fail-closed.

- [ ] **Step 4: Integrate coordinator into `ControlDomainService` without changing Package B adapter**

Construct `self.agent = AgentSessionCoordinator(self.store, self.coordinator)` after the existing `MutationCoordinator`. Do not change `self.adapter = FakeAdapter(...)` or make Package B Official-Tibia-capable.

Extend `status()` with an additive `agent` summary only; preserve every existing Package B key/value that current tests assert.

- [ ] **Step 5: Run coordinator plus Package A/B regression suites**

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_session -v
python -m unittest discover -s tests/tools/tibia_re_control_center -p "test_package_a.py" -v
python -m unittest discover -s tests/tools/tibia_re_control_center -p "test_package_b.py" -v
```
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add tools/tibia_re_control_center/agent_session.py tools/tibia_re_control_center/control_domain.py tests/tools/tibia_re_control_center/test_agent_session.py
git commit -m "feat(control-center): add persistent agent session coordinator"
```

---

### Task 5: Add the Qwen3-VL model-slot scheduler and visual sensor adapter

**Files:**
- Create: `tools/tibia_re_control_center/agent_vision.py`
- Create: `tests/tools/tibia_re_control_center/test_agent_vision.py`
- Reuse: `tools/tibia_re_vision/evidence.py`, `tools/tibia_re_vision/ollama.py`
- Reuse fixtures: `tools/tibia-re-vision-benchmark/fixtures/synthetic-login-smoke.png`, `tools/tibia-re-vision-benchmark/fixtures/black-negative.png`

**Interfaces:**
- Produces constants `QWEN_VISION_MODEL`, `QWEN_VISION_DIGEST`, `QWEN_VISION_PROFILE_ID` with exact approved values.
- Produces `ModelSlotScheduler` with `admit(target_model, expected_digest)`, `infer(callable)`, and `release_owned()`; provider functions are dependency-injected in tests.
- Produces `AgentVisionSensor.observe(capture: SecretSafeCapture) -> VisionObservation`.
- `SecretSafeCapture` requires bytes/path hash + `secret_safe=True`; populated credential frames are rejected before provider invocation.
- Duplicate frame SHA may reuse the last observation only inside the same run/model profile and must emit a new SENSOR event referencing the prior evidence, not rewrite history.

- [ ] **Step 1: Write RED tests for model residency, digest and secret-safe admission**

```python
class AgentVisionTests(unittest.TestCase):
    def test_foreign_resident_model_never_gets_evicted(self):
        stopped = []
        scheduler = ModelSlotScheduler(
            ps=lambda: ["gemma4:12b"],
            digest=lambda _model: QWEN_VISION_DIGEST,
            unload=lambda model: stopped.append(model),
        )
        with self.assertRaises(ModelSlotUnavailable):
            scheduler.admit(QWEN_VISION_MODEL, QWEN_VISION_DIGEST)
        self.assertEqual([], stopped)
```

Add tests proving:
- exact empty slot and exact-owned target are admitted;
- multiple/unknown residency is refused;
- digest mismatch refuses before inference;
- unsafe capture refuses before any model call;
- model response failing strict `VisualEvidence` schema is rejected;
- `quality.visual_only` must remain true and `structural_authority` false;
- `IN_GAME_VISUAL` is returned as visual evidence only;
- final `release_owned()` unloads only the exact owned target and verifies empty residency.

- [ ] **Step 2: Run RED tests**

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_vision -v
```
Expected: FAIL because `agent_vision.py` is absent.

- [ ] **Step 3: Implement exact profile and dependency-injected scheduler**

```python
QWEN_VISION_MODEL = "qwen3-vl:4b-instruct-q4_K_M"
QWEN_VISION_DIGEST = "ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b"
QWEN_VISION_PROFILE_ID = f"ollama:{QWEN_VISION_MODEL}@sha256:{QWEN_VISION_DIGEST}"
QWEN_NUM_CTX = 4096
QWEN_NUM_PREDICT = 256
QWEN_TEMPERATURE = 0
```

Initial production model calls use `keep_alive="0s"` to make ownership/release deterministic. Performance tuning to a bounded non-zero keep-alive is a measured follow-up, not required for correctness.

- [ ] **Step 4: Add deterministic prefilter that requires no new image dependency**

The initial prefilter computes SHA-256, validates the secret-safe manifest, detects exact duplicate frames, and rejects empty bytes. Do not add Pillow/OpenCV merely for this phase. Template/perceptual matching remains optional until representative data proves value.

- [ ] **Step 5: Run offline tests plus existing PR #790 suite**

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_vision -v
python -m unittest discover -s tools/tibia-re-vision-benchmark/tests -p "test_*.py" -v
```
Expected: PASS without contacting real Ollama. Provider calls in unit tests are fakes.

- [ ] **Step 6: Commit**

```bash
git add tools/tibia_re_control_center/agent_vision.py tests/tools/tibia_re_control_center/test_agent_vision.py
git commit -m "feat(control-center): add bounded qwen vision sensor"
```

---

### Task 6: Add deterministic visual/runtime reconciliation with no visual semantic promotion

**Files:**
- Create: `tools/tibia_re_control_center/agent_reconcile.py`
- Create: `tests/tools/tibia_re_control_center/test_agent_reconcile.py`

**Interfaces:**
- Produces `RuntimeEvidenceClass` with `UNKNOWN`, `STRUCTURAL_ONLY`, `REVIEWED_CAUSAL`.
- Produces `RuntimeObservation(state: str, evidence_class: RuntimeEvidenceClass, evidence_refs: tuple[str, ...])`.
- Produces `ReconciledState` with `UNKNOWN`, `LOGIN_SCREEN`, `CHARACTER_SELECT`, `WORLD_CONFIRMED`, `WORLD_EXIT`, `CONFLICT`.
- Produces `reconcile_state(visual: VisionObservation | None, runtime: RuntimeObservation | None) -> ReconciliationResult`.
- A runtime adapter is allowed to emit `REVIEWED_CAUSAL` only when a separately reviewed producer contract says it can. This plan supplies no live producer and defaults to `UNKNOWN`.

- [ ] **Step 1: Write RED tests for the semantic hard boundary**

```python
class ReconcileTests(unittest.TestCase):
    def test_visual_in_game_never_confirms_world(self):
        result = reconcile_state(
            visual=vision("IN_GAME_VISUAL"),
            runtime=RuntimeObservation("UNKNOWN", RuntimeEvidenceClass.UNKNOWN, ()),
        )
        self.assertNotEqual(ReconciledState.WORLD_CONFIRMED, result.state)
```

Add tests proving:
- `LOGIN_SCREEN`/`CHARACTER_SELECT` visual states may remain visual operational states but do not grant authority;
- `WORLD_CONFIRMED` requires runtime state `IN_GAME` with `REVIEWED_CAUSAL` evidence;
- `STRUCTURAL_ONLY IN_GAME` cannot confirm world;
- reviewed-causal `IN_GAME` conflicting with visual login/character-select returns `CONFLICT`;
- missing/stale evidence returns `UNKNOWN`/`INCONCLUSIVE`, never optimistic promotion;
- all output references preserve both visual and runtime provenance.

- [ ] **Step 2: Run RED tests**

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_reconcile -v
```
Expected: FAIL because the module is absent.

- [ ] **Step 3: Implement a table-driven reconciler**

Keep the critical world rule explicit:

```python
if runtime and runtime.state == "IN_GAME" and runtime.evidence_class is RuntimeEvidenceClass.REVIEWED_CAUSAL:
    if visual and visual.screen_class in {"LOGIN_SCREEN", "CHARACTER_SELECT"}:
        return conflict("VISUAL_RUNTIME_DISAGREEMENT", visual, runtime)
    return confirmed_world(visual, runtime)
```

There must be no branch where `visual.screen_class == "IN_GAME_VISUAL"` alone returns `WORLD_CONFIRMED`.

- [ ] **Step 4: Run tests**

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_reconcile -v
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/tibia_re_control_center/agent_reconcile.py tests/tools/tibia_re_control_center/test_agent_reconcile.py
git commit -m "feat(control-center): reconcile visual and runtime evidence"
```

---

### Task 7: Expose agent tasks, chat, controls, events and result views through the existing loopback Control API/UI/CLI

**Files:**
- Modify: `tools/tibia_re_control_center/control_domain.py`
- Modify: `tools/tibia_re_control_center/control_api.py`
- Modify: `tools/tibia_re_control_center/control_cli.py`
- Modify: `tools/tibia_re_control_center/control_ui.py`
- Create: `tests/tools/tibia_re_control_center/test_agent_api.py`

**Interfaces:**
- New GET routes: `/v1/agent/session`, `/v1/agent/events`, `/v1/agent/result`.
- New POST routes: `/v1/agent/tasks`, `/v1/agent/chat`, `/v1/agent/control`.
- Every POST still requires exact Host, loopback binding, nonce header, exact Origin rules when present, request-id idempotency, bounded JSON body and no cookies/CORS.
- `/v1/agent/control` body is exactly `{"session_id": str, "command": "PAUSE|STOP|RESUME|SCREENSHOT"}`.
- `/v1/agent/chat` body is exactly `{"session_id": str, "text": str}` and records provenance `OWNER`; secret-class content is rejected before persistence.
- `/v1/agent/tasks` accepts the exact `TaskEnvelope.v1` mapping and records provenance `SUPERVISOR`; it does not grant physical authority.

- [ ] **Step 1: Write HTTP RED tests reusing Package B transport helper conventions**

```python
class AgentApiTests(unittest.TestCase):
    def test_agent_routes_require_existing_nonce_boundary(self):
        status, _, body = http_call(self.server, "GET", "/v1/agent/session", nonce=None)
        self.assertEqual(401, status)
        self.assertEqual("CONTROL_AUTH_REQUIRED", decode(body)["code"])
```

Add tests proving:
- POST task idempotency replays same response;
- same request id + different task envelope returns 409;
- `STOP` route durably latches existing Control Center STOP and writes OWNER AgentEvent;
- `PAUSE`/`RESUME` affect session state but cannot bypass unresolved global STOP/recovery;
- `SCREENSHOT` stays zero-budget/read-only with default unbound capture;
- chat provenance is OWNER and secret-like key/value content is rejected;
- API response never returns nonce, credential values, token-file content or `secret_capability_ref` resolved material;
- loopback/CSP/no-cookie/no-CORS tests remain green.

- [ ] **Step 2: Run RED test**

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_api -v
```
Expected: FAIL because routes are absent.

- [ ] **Step 3: Add domain operations using existing RequestLedger path**

Extend `normalize_post_body`, `_resource_prefix`, and route handlers with `AGENT_TASK`, `AGENT_CHAT`, `AGENT_CONTROL`; route them through existing `process_post()` so request hashes and terminal replay semantics stay centralized.

Do not add a second HTTP server for the dashboard.

- [ ] **Step 4: Extend the existing UI instead of replacing it**

Add an `Agent` tab showing:
- session id / heartbeat / operational state;
- task/run id and trusted-main SHA;
- latest secret-safe capture hash/reference;
- visual observation explicitly labeled `VISUAL_ONLY / UNTRUSTED`;
- runtime evidence class and reconciliation state;
- requested/performed action state and physical budget count;
- provenance-aware event timeline;
- owner chat box and PAUSE/STOP/RESUME/SCREENSHOT controls.

Keep the existing top-level STOP ALL button. Agent STOP must converge on the same durable stop latch, not create an independent weaker stop.

- [ ] **Step 5: Extend CLI with matching narrow commands**

Add:
```text
agent-status
agent-task --file TASK_JSON
agent-chat --session SESSION_ID --text TEXT
agent-control --session SESSION_ID --command PAUSE|STOP|RESUME|SCREENSHOT
agent-events --cursor N
agent-result --run RUN_ID
```

CLI continues reading the private loopback nonce file and never accepts Tibia credentials.

- [ ] **Step 6: Run API/UI/CLI and Package B regressions**

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_api -v
python -m unittest tests.tools.tibia_re_control_center.test_package_b -v
python tests/tools/tibia_re_control_center/audit_package_b.py
```
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add tools/tibia_re_control_center/control_domain.py tools/tibia_re_control_center/control_api.py tools/tibia_re_control_center/control_cli.py tools/tibia_re_control_center/control_ui.py tests/tools/tibia_re_control_center/test_agent_api.py
git commit -m "feat(control-center): expose local agent dashboard controls"
```

---

### Task 8: Add a separate narrow MCP supervisor bridge over the agent contract

**Files:**
- Create: `tools/tibia_re_control_center/agent_mcp.py`
- Create: `tests/tools/tibia_re_control_center/test_agent_mcp.py`
- Modify: `docs/agents/MODULE_CATALOG.md` only after tests establish the public integration point.

**Interfaces:**
- Dependency-free stdio MCP server name `tibia-re-agent` using protocol `2024-11-05`.
- Tools exposed:
  - `agent_session_status` (read-only)
  - `agent_submit_task` (accepts `TaskEnvelope.v1`; does not grant authority)
  - `agent_control` (`PAUSE|STOP|RESUME|SCREENSHOT` only)
  - `agent_events` (read-only cursor page)
  - `agent_result` (read-only terminal result)
- MCP talks to the loopback Control API through `ControlApiClient`; it does not import or expose Track A process/GUI helpers directly.
- MCP tool descriptions explicitly state that model/task input cannot expand Track A authority or credential permissions.

- [ ] **Step 1: Write RED MCP contract tests**

```python
class AgentMcpTests(unittest.TestCase):
    def test_tool_surface_contains_no_raw_effect_or_secret_tool(self):
        names = {item["name"] for item in tool_definitions()}
        self.assertEqual(
            {"agent_session_status", "agent_submit_task", "agent_control", "agent_events", "agent_result"},
            names,
        )
        self.assertTrue(all("click" not in name and "type" not in name and "secret" not in name for name in names))
```

Add tests proving:
- initialize/tools-list JSON-RPC works;
- unknown tool fails safely;
- raw `password`, `token`, `credential` fields in a task are rejected before Control API call;
- `agent_control` enum cannot express shell/click/type/process control;
- no MCP method can read a token file or local credential file;
- API errors are returned as bounded tool errors without stack traces/secrets;
- `--self-test` exits zero without contacting Ollama or Track A runtime.

- [ ] **Step 2: Run RED tests**

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_mcp -v
```
Expected: FAIL because `agent_mcp.py` is absent.

- [ ] **Step 3: Implement the stdio MCP server as a Control API client only**

Use the same compact message loop shape as the existing local worker MCP, but do not copy its model delegation tools. Core dispatch shape:

```python
if name == "agent_session_status":
    return tool_text(client.get("/v1/agent/session"))
if name == "agent_submit_task":
    envelope = TaskEnvelope.from_mapping(arguments["task"])
    return tool_text(client.post("/v1/agent/tasks", envelope.as_dict(), request_id=arguments["request_id"]))
```

The bridge must never instantiate `OfficialTibiaAdapter`, `CanonicalTrackAAuthorityBridge`, subprocesses, Docker, xdotool, or Ollama directly.

- [ ] **Step 4: Run MCP self-test and tests**

```bash
python -m tools.tibia_re_control_center.agent_mcp --self-test
python -m unittest tests.tools.tibia_re_control_center.test_agent_mcp -v
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/tibia_re_control_center/agent_mcp.py tests/tools/tibia_re_control_center/test_agent_mcp.py docs/agents/MODULE_CATALOG.md
git commit -m "feat(control-center): add narrow agent supervisor mcp"
```

---

### Task 9: Add repository-only fake/offline vertical-slice E2E and security falsification

**Files:**
- Create: `tests/tools/tibia_re_control_center/e2e_agent_foundation.py`
- Create: `tests/tools/tibia_re_control_center/audit_agent_foundation.py`
- Modify only if a real defect is found: agent/control-center modules from Tasks 1-8.

**Interfaces:**
- E2E uses real `SQLitePersistentStore`, `ControlDomainService`, Control API, agent coordinator, strict protocol, MCP/client surface and a fake vision provider.
- No real Ollama inference is required for the deterministic E2E; PR #790 fixtures are read locally and model response is injected deterministically.
- Production executor stays `NullBoundedActionExecutor`; a test-only fake executor may be injected only inside this test module.

- [ ] **Step 1: Write a complete fake vertical slice**

The E2E must execute these exact scenarios:

```text
A. SUPERVISOR task -> safe fixture -> visual LOGIN_SCREEN -> result/evidence PASS, effects=0
B. visual IN_GAME_VISUAL + runtime UNKNOWN -> never WORLD_CONFIRMED, effects=0
C. visual LOGIN_SCREEN + reviewed-causal runtime IN_GAME -> CONFLICT, effects=0
D. OWNER PAUSE before proposed ENTER_WORLD -> refused, effects=0
E. OWNER STOP after proposal but before fake commit -> refused/not dispatched, effects=0
F. duplicate task/action idempotency -> exactly one test effect maximum
G. test executor reports performed-but-unknown -> INCONCLUSIVE/PERFORMED_UNKNOWN, no replay
H. backend restart after STOP/PAUSE -> latch preserved, no auto-resume
I. foreign model residency -> WAITING_MODEL_SLOT, no unload and no inference
J. secret-bearing task/chat/capture metadata -> rejected before persistence/provider call
```

- [ ] **Step 2: Run E2E**

```bash
python tests/tools/tibia_re_control_center/e2e_agent_foundation.py
```
Expected terminal output:
```text
AGENT_FOUNDATION_E2E=PASS
OFFICIAL_RUNTIME_ACCESS=NONE
PHYSICAL_EFFECTS=0
```

- [ ] **Step 3: Implement static security/audit assertions**

`audit_agent_foundation.py` must inspect the changed agent modules and fail if it finds production exposure of:

```text
xdotool
pyautogui
subprocess.Popen
shell=True
docker exec
/proc/*/mem
get_secret
password field persistence
cua_repl enablement
```

The audit must also assert:
- Qwen exact model/digest/profile constants;
- `visual_only=True` / `structural_authority=False` validation remains imported from reusable vision core;
- MCP tool allowlist has only the five declared tools;
- production coordinator constructs `NullBoundedActionExecutor` by default;
- no change to `OfficialTibiaAdapter.CURRENT_CLIENT_SHA256` in this implementation branch unless a separately approved design/task is linked (for this plan, any change is a failure).

- [ ] **Step 4: Run audit and all focused suites**

```bash
python tests/tools/tibia_re_control_center/audit_agent_foundation.py
python -m unittest discover -s tests/tools/tibia_re_control_center -p "test_agent_*.py" -v
python -m unittest discover -s tools/tibia-re-vision-benchmark/tests -p "test_*.py" -v
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/tools/tibia_re_control_center/e2e_agent_foundation.py tests/tools/tibia_re_control_center/audit_agent_foundation.py
git commit -m "test(control-center): prove local agent foundation e2e"
```

---

### Task 10: Documentation, exact-head validation, independent audit, and stale PoC disposition

**Files:**
- Modify: `docs/agents/MODULE_CATALOG.md`
- Modify: `docs/agents/CHANGELOG.md`
- Create/update the new implementation task/report/evidence paths selected at execution preflight.
- Do not alter the approved spec except to correct a proven factual contradiction; implementation mapping belongs in task/report/plan.

**Interfaces:**
- Durable result must classify the implementation as `repository_control_foundation` / `runtime_access:none`, not “autonomous Tibia agent complete”.
- Final evidence records exact implementation head, commands/results, E2E status, independent audit status and explicit non-claims.

- [ ] **Step 1: Update module catalog and changelog with the actual delivered boundary**

Document:
- Control Center now owns persistent local agent session/provenance/dashboard/MCP foundation;
- reusable `tools.tibia_re_vision` exports PR #790 evidence/Ollama safety primitives;
- production action executor remains unbound;
- credentials, Synology transport deployment and Official Tibia physical transitions remain separate work;
- CUA remains disabled/not primary; Hermes unchanged.

- [ ] **Step 2: Run full repository-focused validation on the frozen head**

```bash
python -m compileall -q tools/tibia_re_control_center tools/tibia_re_vision tests/tools/tibia_re_control_center tests/tools/tibia_re_vision
python -m unittest discover -s tests/tools/tibia_re_control_center -p "test_*.py" -v
python -m unittest discover -s tools/tibia-re-vision-benchmark/tests -p "test_*.py" -v
python tests/tools/tibia_re_control_center/audit_package_a.py
python tests/tools/tibia_re_control_center/audit_package_a_p1.py
python tests/tools/tibia_re_control_center/audit_package_b.py
python tests/tools/tibia_re_control_center/e2e_package_b.py
python tests/tools/tibia_re_control_center/audit_agent_foundation.py
python tests/tools/tibia_re_control_center/e2e_agent_foundation.py
python -m ruff check tools/tibia_re_control_center tools/tibia_re_vision tests/tools/tibia_re_control_center tests/tools/tibia_re_vision
git diff --check
```
Expected: every command PASS on the same exact head.

- [ ] **Step 3: Run fresh independent audit before readiness**

Fresh validator must verify at minimum:
- no hidden physical runtime path;
- STOP/PAUSE/restart/idempotency behavior;
- no visual-only `IN_GAME` promotion;
- no secret persistence/model exposure;
- one-model residency fail-closed behavior;
- MCP/control API cannot bypass Control Center or Track A authority;
- existing Package A/B/C/D behavior not weakened;
- old Package D fence was not silently promoted.

Zero unresolved P0/P1/material findings are required before readiness.

- [ ] **Step 4: Run exact-head GitHub checks and review full changed-file inventory**

Freeze the final head, push once, inspect required checks for that exact SHA, review every changed file, and resolve all review threads. Do not rerun heavy validation after unrelated edits; any edit invalidating evidence requires the relevant focused/component/final gate again.

- [ ] **Step 5: Terminally disposition old PR #615 only after replacement coverage is proven**

After the new foundation is merged and the final evidence proves these six #615 invariants are covered — loopback-only Ollama, exact model digest, strict output schema, secret rejection, single-model residency, deterministic unload — close PR #615 as **superseded by the merged Control Center vision-agent foundation**. Preserve its historical evidence; do not merge its stale branch. If any one of those six invariants is not yet covered, leave #615 open and record the exact missing invariant instead of falsely superseding it.

- [ ] **Step 6: Commit documentation/closeout changes on the implementation branch**

```bash
git add docs/agents/MODULE_CATALOG.md docs/agents/CHANGELOG.md docs/agents/tasks docs/agents/reports docs/agents/evidence
git commit -m "docs(control-center): record local agent foundation"
```

---

## Post-plan boundaries: separate future work, not hidden implementation steps

The following are intentionally **not** executable tasks in this plan because each changes a separate trust/authority boundary:

1. **Molehill deployment/registration:** install or register the new `agent_mcp` with the local supervisor/Codex configuration and choose its durable data root. This requires a local-environment deployment task but no Official Tibia authority.
2. **Authenticated Synology↔Molehill runtime-edge transport:** choose and implement the mutually authenticated channel, certificate/key provisioning, replay policy and deployment. This is a security-sensitive integration task and must be reviewed independently.
3. **Read-only Kasm capture/runtime-signal binding:** admit a Track A `read_only` task, prove target uniqueness/non-invasiveness, then connect secret-safe screenshot production and reviewed runtime-signal adapters. No GUI input.
4. **Credential broker:** separately authorize and design the secret capability provider/injection boundary. Raw credentials still never enter model/session/evidence channels.
5. **Current-client named physical actions:** separately review exact current-client executor workers for `SUBMIT_AUTHORIZED_LOGIN`, `SELECT_CHARACTER`, `ENTER_WORLD`, `EXIT_WORLD`, bind them through current Gate A/rebind/recovery/Gate B/whole-lifetime supervisor/`input.lock`, set explicit per-action low-level event budgets, and run staged physical E2E. Updating the stale Package D promotion fence is not a shortcut.

Completion of this plan therefore means **repository-owned observable agent/control foundation complete, physical runtime integration not yet authorized**, not “autonomous Tibia agent complete”.

## Plan self-review checklist

- Spec coverage: Control/session persistence, provenance, owner control precedence, vision/OCR, one-model scheduling, reconciliation, evidence/result envelopes, dashboard/chat, supervisor bridge and named-action boundary are assigned to Tasks 1-9. Credential/physical transport/effect phases are explicitly separated because the approved spec itself requires separate authorization.
- Reuse: Control Center Package A/B/C/D and PR #790 are reused; no second service/store/action bridge is invented. PR #615 is treated as untrusted/stale candidate evidence and has an explicit terminal disposition rule.
- Safety: no task enables CUA, Hermes planner runtime, credentials, Official-client observation/mutation, process memory or physical input. Production executor stays unbound.
- Type consistency: `TaskEnvelope`, `AgentEvent`, `ResultEnvelope`, `AgentSessionRecord`, `AgentSessionCoordinator`, `ModelSlotScheduler`, `AgentVisionSensor`, `RuntimeObservation`, `ReconciledState`, and MCP/API names are defined once and reused with the same names in later tasks.
- Placeholder scan: all implementation tasks have concrete files, signatures, RED/GREEN commands, expected outcomes and commit boundaries; excluded future trust-boundary work is named explicitly rather than left as an implicit implementation gap.
