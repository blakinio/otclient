# Local Track A Vision Agent Supervisor Implementation Plan

> **Execution workflow:** use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans`. Execute task-by-task with RED -> GREEN -> focused regression -> commit. Do not skip the approval/authority boundaries below.

**Goal:** Build the repository-owned observable local vision-agent foundation by extending the existing TIBIA RE Control Center with persistent agent sessions, provenance-aware owner/supervisor controls, reusable Qwen3-VL sensing, deterministic state reconciliation, evidence/result envelopes, a narrow supervisor MCP surface, and fake/offline E2E proof. Official Tibia runtime access and physical mutation remain unbound.

**Approved design:** `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`

## Architectural mapping and hard boundaries

The approved “thin persistent Molehill session/control service” is implemented by **extending the already-merged `tools/tibia_re_control_center` backend**, not by creating a second service/store. Reuse its SQLite/WAL store, durable STOP/reset semantics, request idempotency, event/artifact persistence, loopback API/UI/CLI, Package D guarded-dispatch transaction semantics, and Track A authority bridge.

Reuse PR #790 by extracting only its reusable visual-evidence and Ollama-admission primitives into an importable package. Do not rebuild a model bake-off or adopt the stale PR #615 branch wholesale.

Repository implementation remains:

```yaml
runtime_access: none
implementation_authorized: false  # until owner explicitly starts execution after this plan
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
process_memory_access_allowed: false
physical_action_budget: 0
physical_action_count: 0
```

Additional invariants:

- Do not enable `mcp_servers.cua_repl`, start CUA, restart/modify Molehill supervisor services, restart `muse-ollama-proxy`, touch the Official Tibia runtime, or consume credentials while executing this plan.
- Current trusted Track A client fence is `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`.
- `tools/tibia_re_control_center/official_adapter.py` still carries an older promotion fence. **Do not change its `CURRENT_CLIENT_SHA256` simply to make Package D actionable.** Current-client effect binding is separate reviewed work.
- Qwen profile is exactly `qwen3-vl:4b-instruct-q4_K_M`, digest `ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b`, `num_ctx=4096`, `num_predict=256`, `temperature=0`.
- Model output is untrusted, visual-only, structurally non-authoritative; visual evidence never independently promotes `IN_GAME`.
- At most one local model may be resident/inferencing. Unexpected, multiple, or unknown residency fails closed; never evict an unowned model merely to continue.
- Raw secrets are forbidden from task envelopes, agent events, session storage, dashboard/chat persistence, model prompts, artifacts, and logs. `secret_capability_ref` is opaque metadata only and is not resolved in this plan.
- Model-facing actions are named semantics only. No coordinate click, arbitrary text type, shell, Docker, process-control, debugger, process-memory, or secret getter capability is exposed.
- OWNER `STOP`/`PAUSE` dominates SUPERVISOR/MODEL. Restart/reconnect never auto-resumes effect-capable state.
- Production executor remains unbound/null throughout this plan. Physical integration is a later authorization.

---

## Task 1 — Extract PR #790 reusable vision/Ollama safety core

**Files**

- Create `tools/tibia_re_vision/__init__.py`
- Create `tools/tibia_re_vision/evidence.py`
- Create `tools/tibia_re_vision/ollama.py`
- Modify `tools/tibia-re-vision-benchmark/vision_benchmark.py`
- Create `tests/tools/tibia_re_vision/test_evidence.py`
- Create `tests/tools/tibia_re_vision/test_ollama.py`
- Regress `tools/tibia-re-vision-benchmark/tests/test_*.py`

**Required public surface**

`evidence.py` exports:

```python
SCREEN_CLASSES
sha256_file(path)
validate_input_manifest(metadata, image_path)
normalize_ocr_transcription(value)
validate_model_observation(observation)
validate_visual_evidence(payload)
```

`ollama.py` exports:

```python
admit_residency(resident_models, target_model) -> tuple[bool, str]
query_ollama_ps(...)
query_ollama_model_digest(...)
run_ollama_trial(...)
release_ollama_model_if_owned(...)
```

Benchmark-only scoring/hard-gate orchestration remains in `vision_benchmark.py`.

- [ ] Write RED tests that import `tools.tibia_re_vision` and prove: `visual_only` must be true; `structural_authority` must be false; black/empty OCR remains empty; foreign/multiple/unknown model residency fails closed.
- [ ] Run:

```bash
python -m unittest discover -s tests/tools/tibia_re_vision -p "test_*.py" -v
```

Expected RED: import/module missing.

- [ ] Extract reusable functions without changing their PR #790 semantics.
- [ ] Preserve direct benchmark execution. Because `tools/tibia-re-vision-benchmark` has a hyphenated path, before importing `tools.tibia_re_vision`, `vision_benchmark.py` must derive repository root from `Path(__file__).resolve().parents[2]` and prepend it to `sys.path` only when absent. Do not alter provider or scoring behavior.
- [ ] Add direct-script import smoke:

```bash
python tools/tibia-re-vision-benchmark/vision_benchmark.py --help
```

Expected: exit 0/help, no Ollama inference.

- [ ] Run reusable + frozen benchmark suites:

```bash
python -m unittest discover -s tests/tools/tibia_re_vision -p "test_*.py" -v
python -m unittest discover -s tools/tibia-re-vision-benchmark/tests -p "test_*.py" -v
```

- [ ] Commit:

```bash
git add tools/tibia_re_vision tools/tibia-re-vision-benchmark/vision_benchmark.py tests/tools/tibia_re_vision
git commit -m "refactor(track-a): expose reusable vision safety core"
```

---

## Task 2 — Add strict agent protocol, provenance, state, and named-action types

**Files**

- Create `tools/tibia_re_control_center/agent_protocol.py`
- Create `tests/tools/tibia_re_control_center/test_agent_protocol.py`
- Modify `tools/tibia_re_control_center/__init__.py`

**Enums**

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

class AgentVisualState(str, Enum):
    UNKNOWN = "UNKNOWN"
    LOGIN_SCREEN = "LOGIN_SCREEN"
    CHARACTER_SELECT = "CHARACTER_SELECT"
    WORLD_VISUAL = "WORLD_VISUAL"
    WORLD_EXIT_VISUAL = "WORLD_EXIT_VISUAL"
    ERROR_SCREEN = "ERROR_SCREEN"

class NamedAgentAction(str, Enum):
    SCREENSHOT = "SCREENSHOT"
    SUBMIT_AUTHORIZED_LOGIN = "SUBMIT_AUTHORIZED_LOGIN"
    SELECT_CHARACTER = "SELECT_CHARACTER"
    ENTER_WORLD = "ENTER_WORLD"
    EXIT_WORLD = "EXIT_WORLD"

class OwnerControlCommand(str, Enum):
    PAUSE = "PAUSE"
    STOP = "STOP"
    RESUME = "RESUME"
    SCREENSHOT = "SCREENSHOT"

class ResultStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"
```

No raw click/type/shell variants may exist.

**Immutable dataclasses — exact fields**

```python
@dataclass(frozen=True)
class ClientIdentity:
    version: str
    size: int | str
    sha256: str

@dataclass(frozen=True)
class TaskEnvelope:
    schema: str
    session_id: str
    task_id: str
    run_id: str
    idempotency_key: str
    trusted_main_sha: str
    client_identity: ClientIdentity
    objective: str
    allowed_actions: tuple[NamedAgentAction, ...]
    physical_action_budget: int
    max_attempts: int
    deadline_epoch_ms: int
    runtime_access: str
    required_evidence: tuple[str, ...]
    secret_capability_ref: str | None

@dataclass(frozen=True)
class AgentEvent:
    schema: str
    session_id: str
    run_id: str | None
    seq: int
    observed_epoch_ms: int
    provenance: AgentProvenance
    kind: str
    state_before: str
    state_after: str
    artifact_refs: tuple[str, ...]
    action_id: str | None
    payload: dict[str, object]

@dataclass(frozen=True)
class ResultEnvelope:
    schema: str
    session_id: str
    run_id: str
    status: ResultStatus
    trusted_main_sha: str
    final_state: str
    action_count: int
    physical_action_budget: int
    evidence_manifest_sha256: str
    unresolved_conflicts: tuple[str, ...]

@dataclass(frozen=True)
class AgentSessionRecord:
    session_id: str
    operational_state: AgentOperationalState
    current_run_id: str | None
    last_event_seq: int
    pause_latched: bool
    stop_latched: bool
    heartbeat_epoch_ms: int | None
```

`TaskEnvelope.from_mapping()` requires exact keys and rejects unknown or secret-bearing fields. `AgentEvent.new(...)` uses `seq=0`; persistence assigns the durable positive sequence.

- [ ] RED tests: raw credential field rejected; exact keys; SHA exactly 40 lowercase hex; bounded non-negative budgets/attempts; runtime class in current admission vocabulary; opaque IDs cannot contain separators; unknown action rejected; `WORLD_VISUAL` distinct from runtime `IN_GAME`.
- [ ] Run:

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_protocol -v
```

Expected RED: module missing.

- [ ] Implement using existing `ValidationError`, `checked_non_negative`, `require_exact_keys`, `validate_opaque_id` from `model.py`.
- [ ] GREEN:

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_protocol -v
python -m compileall -q tools/tibia_re_control_center/agent_protocol.py
```

- [ ] Commit:

```bash
git add tools/tibia_re_control_center/agent_protocol.py tools/tibia_re_control_center/__init__.py tests/tools/tibia_re_control_center/test_agent_protocol.py
git commit -m "feat(control-center): add local agent protocol"
```

---

## Task 3 — Extend existing SQLite store with durable agent sessions/tasks/results

**Files**

- Modify `tools/tibia_re_control_center/persistent_store.py`
- Create `tests/tools/tibia_re_control_center/test_agent_persistence.py`

**Interfaces**

```python
write_agent_session(record: AgentSessionRecord) -> None
load_agent_session(session_id: str) -> AgentSessionRecord | None
accept_agent_task(envelope: TaskEnvelope) -> dict[str, object]
load_agent_task(idempotency_key: str) -> dict[str, object] | None
finish_agent_task(idempotency_key: str, result: ResultEnvelope) -> None
append_agent_event(event: AgentEvent) -> AgentEvent
```

Same idempotency key + canonical-equivalent envelope is replay-safe. Same key + different envelope raises `IDEMPOTENCY_CONFLICT`. Event sequence comes from committed SQLite ordering, never from an in-memory counter.

Additive schema only:

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

Use the existing `events` table for `AgentEvent`; do not create a second event log or database.

- [ ] RED restart test uses keyword arguments:

```python
record = AgentSessionRecord(
    session_id="session-1",
    operational_state=AgentOperationalState.PAUSED,
    current_run_id=None,
    last_event_seq=7,
    pause_latched=True,
    stop_latched=False,
    heartbeat_epoch_ms=None,
)
```

Also test positive/strict event sequence, idempotent task replay, conflicting idempotency rejection, privacy-guard rejection, and old Package B database readability.

- [ ] RED:

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_persistence -v
```

- [ ] Implement with existing canonical `_dump`, `_load`, transactions, privacy checks.
- [ ] GREEN + Package B restart/event regressions:

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_persistence -v
python -m unittest tests.tools.tibia_re_control_center.test_package_b.PackageBTests.test_24_restart_preserves_run_activation_action_and_budget_truth -v
python -m unittest tests.tools.tibia_re_control_center.test_package_b.PackageBTests.test_26_bounded_event_polling_reports_backpressure_for_stale_cursor -v
```

- [ ] Commit:

```bash
git add tools/tibia_re_control_center/persistent_store.py tests/tools/tibia_re_control_center/test_agent_persistence.py
git commit -m "feat(control-center): persist local agent sessions"
```

---

## Task 4 — Implement deterministic agent session coordinator and owner-control precedence

**Files**

- Create `tools/tibia_re_control_center/agent_session.py`
- Create `tests/tools/tibia_re_control_center/test_agent_session.py`
- Modify `tools/tibia_re_control_center/control_domain.py`

**Exact action/capture types**

```python
@dataclass(frozen=True)
class AgentActionRequest:
    action_id: str
    session_id: str
    run_id: str
    action: NamedAgentAction
    expected_source_states: tuple[str, ...]
    remaining_budget: int
    deadline_epoch_ms: int
    secret_capability_ref: str | None

@dataclass(frozen=True)
class AgentActionReceipt:
    action_id: str
    status: str
    performed: bool
    outcome_known: bool
    low_level_event_count: int
    evidence_refs: tuple[str, ...]

@dataclass(frozen=True)
class CaptureReceipt:
    status: str
    artifact_ref: str | None
    sha256: str | None
    secret_safe: bool
```

**Executor contract**

```python
class BoundedActionExecutor(Protocol):
    def execute(self, request: AgentActionRequest) -> AgentActionReceipt: ...
    def screenshot(self, session_id: str, run_id: str) -> CaptureReceipt: ...
```

Production default is `NullBoundedActionExecutor`: every mutating action -> `REFUSED_EXECUTOR_UNBOUND`, `performed=False`, `outcome_known=True`, `low_level_event_count=0`; screenshot -> `UNAVAILABLE` without effect.

**Coordinator**

```python
AgentSessionCoordinator(store, control, executor=None)
ensure_session(session_id)
submit_task(envelope)
owner_control(session_id, command)
record_message(session_id, provenance, text)
propose_named_action(...)
complete_run(...)
snapshot(session_id)
```

- [ ] RED tests: STOP dominates supervisor/model; PAUSE blocks effects but preserves run/evidence; reconstruction preserves pause/stop latches; RESUME cannot bypass unresolved global STOP/recovery; MODEL may propose but never approve; SCREENSHOT does not consume physical budget; null executor gives zero effect; duplicate task never executes twice; pre-effect exception -> NOT_PERFORMED; explicit post-effect unknown -> `PERFORMED_UNKNOWN`/INCONCLUSIVE and no replay.
- [ ] Run RED:

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_session -v
```

- [ ] Implement fail closed. Existing `MutationCoordinator.control_state.stop_latched` is consulted before any mutating proposal.
- [ ] Integrate into `ControlDomainService` as `self.agent = AgentSessionCoordinator(self.store, self.coordinator)`. Do not change Package B `FakeAdapter` default and do not instantiate `OfficialTibiaAdapter` here.
- [ ] Extend `status()` additively; preserve all existing Package B fields.
- [ ] GREEN/regression:

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_session -v
python -m unittest tests.tools.tibia_re_control_center.test_package_a -v
python -m unittest tests.tools.tibia_re_control_center.test_package_b -v
```

- [ ] Commit:

```bash
git add tools/tibia_re_control_center/agent_session.py tools/tibia_re_control_center/control_domain.py tests/tools/tibia_re_control_center/test_agent_session.py
git commit -m "feat(control-center): add persistent agent session coordinator"
```

---

## Task 5 — Add exact Qwen3-VL model-slot scheduler and visual sensor

**Files**

- Create `tools/tibia_re_control_center/agent_vision.py`
- Create `tests/tools/tibia_re_control_center/test_agent_vision.py`
- Reuse `tools/tibia_re_vision/evidence.py`, `tools/tibia_re_vision/ollama.py`

**Exact public types**

```python
class ModelSlotUnavailable(RuntimeError):
    code: str

@dataclass(frozen=True)
class SecretSafeCapture:
    run_id: str
    evidence_ref: str
    path: Path
    sha256: str
    secret_safe: bool
    source_monotonic_ns: int | None

@dataclass(frozen=True)
class VisionObservation:
    screen_class: str
    visible_text: tuple[str, ...]
    confidence: float | None
    model_profile_id: str
    evidence_ref: str
    capture_sha256: str
    visual_only: bool = True
    structural_authority: bool = False
```

Constants:

```python
QWEN_VISION_MODEL = "qwen3-vl:4b-instruct-q4_K_M"
QWEN_VISION_DIGEST = "ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b"
QWEN_VISION_PROFILE_ID = f"ollama:{QWEN_VISION_MODEL}@sha256:{QWEN_VISION_DIGEST}"
QWEN_NUM_CTX = 4096
QWEN_NUM_PREDICT = 256
QWEN_TEMPERATURE = 0
```

`ModelSlotScheduler` takes injectable `ps`, `digest`, `infer`, `unload` functions. `AgentVisionSensor.observe(capture)` validates secret-safe capture and strict `VisualEvidence` before returning `VisionObservation`.

- [ ] RED tests: foreign model never unloaded; multiple/unknown residency fails; exact digest mismatch refuses; unsafe capture refuses before provider call; strict schema failure rejects; visual-only/structural-authority invariants enforced; `IN_GAME_VISUAL` remains visual only; release unloads only scheduler-owned target and verifies empty.
- [ ] Run RED:

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_vision -v
```

- [ ] Implement. Initial production inference uses `keep_alive="0s"`; later non-zero keep-alive requires measurement, not assumption.
- [ ] Initial deterministic prefilter: byte non-empty, SHA-256, manifest/secret-safe validation, exact duplicate-frame detection. Do not add Pillow/OpenCV in this phase.
- [ ] GREEN/regressions:

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_vision -v
python -m unittest discover -s tools/tibia-re-vision-benchmark/tests -p "test_*.py" -v
```

- [ ] Commit:

```bash
git add tools/tibia_re_control_center/agent_vision.py tests/tools/tibia_re_control_center/test_agent_vision.py
git commit -m "feat(control-center): add bounded qwen vision sensor"
```

---

## Task 6 — Add deterministic visual/runtime reconciliation

**Files**

- Create `tools/tibia_re_control_center/agent_reconcile.py`
- Create `tests/tools/tibia_re_control_center/test_agent_reconcile.py`

**Types**

```python
class RuntimeEvidenceClass(str, Enum):
    UNKNOWN = "UNKNOWN"
    STRUCTURAL_ONLY = "STRUCTURAL_ONLY"
    REVIEWED_CAUSAL = "REVIEWED_CAUSAL"

@dataclass(frozen=True)
class RuntimeObservation:
    state: str
    evidence_class: RuntimeEvidenceClass
    evidence_refs: tuple[str, ...]

class ReconciledState(str, Enum):
    UNKNOWN = "UNKNOWN"
    LOGIN_SCREEN = "LOGIN_SCREEN"
    CHARACTER_SELECT = "CHARACTER_SELECT"
    WORLD_CONFIRMED = "WORLD_CONFIRMED"
    WORLD_EXIT = "WORLD_EXIT"
    CONFLICT = "CONFLICT"
```

`reconcile_state(visual, runtime) -> ReconciliationResult` is table-driven. Runtime adapters may emit `REVIEWED_CAUSAL` only when a separately reviewed producer contract supports it; this plan supplies no live producer and defaults runtime evidence to UNKNOWN.

- [ ] RED test explicitly instantiates a visual observation:

```python
visual = VisionObservation(
    screen_class="IN_GAME_VISUAL",
    visible_text=(),
    confidence=None,
    model_profile_id="test-profile",
    evidence_ref="fixture",
    capture_sha256="a" * 64,
)
result = reconcile_state(
    visual=visual,
    runtime=RuntimeObservation("UNKNOWN", RuntimeEvidenceClass.UNKNOWN, ()),
)
assert result.state is not ReconciledState.WORLD_CONFIRMED
```

Also prove: `WORLD_CONFIRMED` requires runtime state `IN_GAME` + `REVIEWED_CAUSAL`; STRUCTURAL_ONLY cannot confirm; reviewed-causal IN_GAME conflicting with visual LOGIN/CHARACTER -> CONFLICT; missing/stale evidence -> UNKNOWN/INCONCLUSIVE; output retains both provenance refs.

- [ ] RED/GREEN:

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_reconcile -v
```

- [ ] Commit:

```bash
git add tools/tibia_re_control_center/agent_reconcile.py tests/tools/tibia_re_control_center/test_agent_reconcile.py
git commit -m "feat(control-center): reconcile visual and runtime evidence"
```

---

## Task 7 — Extend existing loopback API/UI/CLI with agent task/chat/control views

**Files**

- Modify `tools/tibia_re_control_center/control_domain.py`
- Modify `tools/tibia_re_control_center/control_api.py`
- Modify `tools/tibia_re_control_center/control_cli.py`
- Modify `tools/tibia_re_control_center/control_ui.py`
- Create `tests/tools/tibia_re_control_center/test_agent_api.py`

**Exact routes**

```text
GET  /v1/agent/session?session_id=<opaque-id>
GET  /v1/agent/events?session_id=<opaque-id>&cursor=<N>&limit=<N>
GET  /v1/agent/result?run_id=<opaque-id>
POST /v1/agent/tasks
POST /v1/agent/chat
POST /v1/agent/control
```

Unknown/missing required query parameters are rejected; `limit` is bounded by existing event paging policy. Every POST keeps existing exact Host/loopback/nonce/Origin/request-id/body-size/no-cookie/no-CORS boundaries.

Bodies:

```json
{"session_id":"...","command":"PAUSE|STOP|RESUME|SCREENSHOT"}
```

```json
{"session_id":"...","text":"owner message"}
```

`/v1/agent/tasks` accepts exactly one `TaskEnvelope.v1` mapping and records SUPERVISOR provenance. It grants no physical authority.

**Exact owner-control semantics**

- `STOP`: first invoke existing durable `MutationCoordinator.stop_all`; only after its durable result persist session `STOPPED`/`stop_latched=True` and OWNER event. Any failure remains fail closed and must not record a false successful stop transition.
- `PAUSE`: persist session `PAUSED`/`pause_latched=True`; do not clear or modify global STOP/recovery state.
- `RESUME`: OWNER only. If global STOP is latched, invoke existing reset/recovery semantics; if reset fails, remain STOPPED. After successful reset, clear only the session pause/stop latch needed for session operation and set IDLE. RESUME never grants Track A authority.
- `SCREENSHOT`: call `executor.screenshot`; zero physical mutation budget; no GUI input authority.

- [ ] RED HTTP tests: nonce boundary; task request-id replay; same request-id + different envelope -> conflict; STOP converges on durable Control Center STOP; PAUSE/RESUME semantics above; SCREENSHOT zero-budget; OWNER chat provenance; secret-like data rejected before persistence; responses never expose nonce/token/credentials/resolved secret material.
- [ ] Run RED:

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_api -v
```

- [ ] Route POSTs through the existing RequestLedger/process_post path; do not add a second HTTP server/store.
- [ ] Extend existing UI with an **Agent** section/tab: session heartbeat/state, task/run/main SHA, latest secret-safe capture hash/ref, visual-only label/OCR, runtime evidence class, reconciliation state, action status/budget, provenance timeline, chat and PAUSE/STOP/RESUME/SCREENSHOT controls. Keep existing top-level STOP ALL.
- [ ] Extend CLI:

```text
agent-status --session SESSION_ID
agent-task --file TASK_JSON
agent-chat --session SESSION_ID --text TEXT
agent-control --session SESSION_ID --command PAUSE|STOP|RESUME|SCREENSHOT
agent-events --session SESSION_ID --cursor N --limit N
agent-result --run RUN_ID
```

CLI never accepts Tibia credential values.

- [ ] GREEN/regression:

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_api -v
python -m unittest tests.tools.tibia_re_control_center.test_package_b -v
python tests/tools/tibia_re_control_center/audit_package_b.py
```

- [ ] Commit:

```bash
git add tools/tibia_re_control_center/control_domain.py tools/tibia_re_control_center/control_api.py tools/tibia_re_control_center/control_cli.py tools/tibia_re_control_center/control_ui.py tests/tools/tibia_re_control_center/test_agent_api.py
git commit -m "feat(control-center): expose local agent dashboard controls"
```

---

## Task 8 — Add a separate narrow supervisor MCP bridge

**Files**

- Create `tools/tibia_re_control_center/agent_mcp.py`
- Create `tests/tools/tibia_re_control_center/test_agent_mcp.py`
- Modify `docs/agents/MODULE_CATALOG.md` only after tests establish the public integration point

Dependency-free stdio MCP server: name `tibia-re-agent`, protocol `2024-11-05`. It talks to the Control API via `ControlApiClient`; it never instantiates OfficialTibiaAdapter, CanonicalTrackAAuthorityBridge, subprocesses, Docker, xdotool, process-memory readers, or Ollama directly.

**Exact tool surface and arguments**

```text
agent_session_status
  {"session_id": str}

agent_submit_task
  {"request_id": str, "task": <exact TaskEnvelope.v1 mapping>}

agent_control
  {"request_id": str, "session_id": str, "command": "PAUSE|STOP|RESUME|SCREENSHOT"}

agent_events
  {"session_id": str, "cursor": int=0, "limit": int=100}

agent_result
  {"run_id": str}
```

Tool descriptions explicitly say that model/task text cannot expand Track A authority, credential permission, action allowlists, or budgets.

- [ ] RED tests: exact five-tool set; initialize/tools-list; unknown tool safe error; raw password/token/credential task fields rejected before API call; `agent_control` cannot express click/type/shell/process control; no token/credential file read; bounded API errors; `--self-test` does not contact Ollama/runtime.
- [ ] Run RED:

```bash
python -m unittest tests.tools.tibia_re_control_center.test_agent_mcp -v
```

- [ ] Implement MCP as API client only.
- [ ] GREEN:

```bash
python -m tools.tibia_re_control_center.agent_mcp --self-test
python -m unittest tests.tools.tibia_re_control_center.test_agent_mcp -v
```

- [ ] Commit:

```bash
git add tools/tibia_re_control_center/agent_mcp.py tests/tools/tibia_re_control_center/test_agent_mcp.py docs/agents/MODULE_CATALOG.md
git commit -m "feat(control-center): add narrow agent supervisor mcp"
```

---

## Task 9 — Fake/offline vertical-slice E2E and security falsification

**Files**

- Create `tests/tools/tibia_re_control_center/e2e_agent_foundation.py`
- Create `tests/tools/tibia_re_control_center/audit_agent_foundation.py`
- Modify Tasks 1–8 files only if a proven defect requires repair

E2E uses real Control Center store/domain/API/session/protocol and fake vision/runtime/executor dependencies. Production executor remains Null; a test-only fake executor is scoped only to the test module. No real Ollama or Official runtime is required.

- [ ] E2E scenarios:

```text
A. SUPERVISOR task + safe fixture -> visual LOGIN_SCREEN -> PASS evidence, physical effects=0
B. visual IN_GAME_VISUAL + runtime UNKNOWN -> never WORLD_CONFIRMED, effects=0
C. visual LOGIN_SCREEN + reviewed-causal runtime IN_GAME -> CONFLICT, effects=0
D. OWNER PAUSE before ENTER_WORLD proposal -> refused, effects=0
E. OWNER STOP after proposal before fake commit -> refused/not dispatched, effects=0
F. duplicate task/action idempotency -> at most one test effect
G. test executor reports performed-but-unknown -> INCONCLUSIVE/PERFORMED_UNKNOWN, no replay
H. backend restart after STOP/PAUSE -> latch preserved, no auto-resume
I. foreign model residency -> WAITING_MODEL_SLOT, no unload/inference
J. secret-bearing task/chat/capture metadata -> rejected before persistence/provider call
```

- [ ] Run:

```bash
python tests/tools/tibia_re_control_center/e2e_agent_foundation.py
```

Expected:

```text
AGENT_FOUNDATION_E2E=PASS
OFFICIAL_RUNTIME_ACCESS=NONE
PHYSICAL_EFFECTS=0
```

- [ ] Static audit must fail on production exposure of `xdotool`, `pyautogui`, `shell=True`, direct `docker exec`, `/proc/*/mem`, generic `get_secret`, credential persistence, CUA enablement, or a production non-null action executor. `subprocess` use is allowed only in pre-existing reviewed Control Center/Track A transport code and must not be introduced in new agent modules.
- [ ] Audit asserts exact Qwen model/digest/profile, reusable PR #790 validation, exact MCP allowlist, default Null executor, and no change to `OfficialTibiaAdapter.CURRENT_CLIENT_SHA256` under this plan.
- [ ] Run:

```bash
python tests/tools/tibia_re_control_center/audit_agent_foundation.py
python -m unittest discover -s tests/tools/tibia_re_control_center -p "test_agent_*.py" -v
python -m unittest discover -s tools/tibia-re-vision-benchmark/tests -p "test_*.py" -v
```

- [ ] Commit:

```bash
git add tests/tools/tibia_re_control_center/e2e_agent_foundation.py tests/tools/tibia_re_control_center/audit_agent_foundation.py
git commit -m "test(control-center): prove local agent foundation e2e"
```

---

## Task 10 — Documentation, exact-head validation, independent audit, and stale PoC disposition

**Files**

- Modify `docs/agents/MODULE_CATALOG.md`
- Modify `docs/agents/CHANGELOG.md`
- Create/update the implementation task/report/evidence selected at execution preflight
- Do not rewrite the approved spec except to correct a proven factual contradiction

**Completion classification:** `repository_control_foundation`, `runtime_access:none`. Never claim “autonomous Tibia agent complete”.

- [ ] Document actual delivered boundary: Control Center owns persistent session/provenance/dashboard/MCP foundation; `tools.tibia_re_vision` exports PR #790 safety primitives; production action executor remains unbound; credentials, Synology transport deployment, Official runtime transitions are separate work; CUA remains disabled; Hermes unchanged.
- [ ] Freeze one final implementation head and run:

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

Every applicable command must PASS on the same exact head; if an existing command name/path has changed on live main, resolve it from current repository state rather than guessing or silently skipping it.

- [ ] Fresh independent validator checks: no hidden physical path; STOP/PAUSE/restart/idempotency; no visual-only IN_GAME promotion; no secret exposure; one-model fail-closed; MCP/API cannot bypass Control Center/Track A authority; Package A/B/C/D not weakened; old Package D fence not silently promoted. Zero material findings required.
- [ ] Push/freeze exact head, inspect full changed-file inventory, required GitHub checks, reviews/threads, and rerun only validation invalidated by any repair.
- [ ] PR #615 disposition **only after replacement is merged**. Close it as superseded only if final evidence proves all six revalidated invariants: loopback-only Ollama, exact digest, strict model-output schema, secret rejection, one-model residency, deterministic unload. If any invariant is missing, leave #615 open and record the exact gap.
- [ ] Commit final docs/evidence:

```bash
git add docs/agents/MODULE_CATALOG.md docs/agents/CHANGELOG.md docs/agents/tasks docs/agents/reports docs/agents/evidence
git commit -m "docs(control-center): record local agent foundation"
```

---

## Explicit future work — not hidden tasks in this plan

These cross separate trust/authority boundaries and require their own design/authorization:

1. **Molehill deployment/registration** — register/deploy `agent_mcp`, choose durable data root, update local supervisor/Codex config. No Official runtime authority implied.
2. **Authenticated Synology↔Molehill production transport** — implement pairing/identity/key provisioning, replay protection, and deployment. Security-sensitive separate task.
3. **Read-only Kasm capture/runtime-signal binding** — separately admit Track A `read_only`, prove target uniqueness/non-invasiveness, then connect secret-safe screenshot and reviewed runtime-signal adapters. No GUI input.
4. **Credential broker** — separately authorize/design opaque secret capability provider and injection boundary; raw credentials still never enter model/session/evidence channels.
5. **Current-client named physical actions** — separately review current-client executors for `SUBMIT_AUTHORIZED_LOGIN`, `SELECT_CHARACTER`, `ENTER_WORLD`, `EXIT_WORLD`, bind through current Gate A/rebind/recovery/Gate B/whole-lifetime supervisor/`input.lock`, define exact per-action low-level budgets, then run staged physical E2E. Updating the stale Package D fence is not a shortcut.

Completion of this plan means **repository-owned observable agent/control foundation complete; physical runtime integration remains not authorized**.

## Plan self-review gate

Before starting implementation, verify all of the following from the saved file and live repository state:

- no `TODO`, `TBD`, placeholder path, or undefined type/helper remains;
- `AgentSessionRecord`, `AgentActionRequest`, `AgentActionReceipt`, `CaptureReceipt`, `SecretSafeCapture`, `VisionObservation`, `RuntimeObservation`, and all MCP/API routes have one exact definition;
- approved spec coverage is complete: persistence/state, provenance, dashboard/chat, owner controls, Qwen sensor, model slot, reconciliation, evidence/result envelopes, supervisor bridge, named-action boundary, failure/recovery, tests;
- Control Center/PR #790 reuse is explicit and no second service/store/action authority is invented;
- CUA/Hermes/credentials/Official runtime/process-memory/physical effects are not introduced;
- production executor remains Null/unbound;
- current Package D promotion fence is not silently changed;
- #615 is not closed until merged replacement evidence proves its bounded reusable invariants;
- implementation still requires an explicit owner execution choice/authorization after this planning checkpoint.
