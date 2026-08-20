# TIBIA RE Control Center Policy Boundary v1

```yaml
contract_id: TIBIA-RE-CONTROL-CENTER-POLICY-BOUNDARY-V1
version: 1.0
major_version: 1
status: normative_design
producer_repository: blakinio/otclient
runtime_authority: none
implementation_phase: future_policy_consumer
```

## 1. Purpose

Define the stable interfaces a future automation/bot decision engine may consume without turning the Control Center itself into an unrestricted gameplay bot or bypassing Track A governance.

The invariant is:

```text
State/Observation
-> Policy/Decision
-> bounded semantic ActionProposal
-> Control Center validation/Scenario Engine
-> Safety/Authority
-> Adapter
-> Recorder
-> Result
```

Policy output is untrusted intent. It is never authority.

This contract is a future-consumer boundary. It does not authorize implementation of autonomous official-client gameplay, does not authorize runtime access, and is not required for Package A/B execution beyond preserving compatible interfaces.

## 2. Stable ports

Control Center exposes or internally preserves these logical boundaries:

```text
ObservationPort   -> read normalized state/status/evidence/freshness
PolicyIngress     -> submit bounded semantic proposal/no-op/control intent
ResultPort        -> read accepted/refused/action/run results and evidence refs
```

Concrete in-process/IPC/HTTP transport is not defined here. A future transport requires its own security review and cannot weaken Control API v1 or Track A authority.

No policy consumer receives a concrete adapter handle.

## 3. Observation envelope

A policy consumer reasons only over normalized, bounded, non-secret state:

```yaml
PolicyObservationEnvelope:
  schema_version: 1
  observation_id: string
  adapter_id: string
  adapter_kind: string
  backend_epoch: string
  observed_monotonic_ns: integer
  freshness: FRESH | STALE | UNKNOWN
  snapshot: GameSnapshot
  capability_refs: [string]
  evidence_refs: [string]
  active_run_summary: object | null
  budget_available: object
  control_state:
    stop_latched: bool
    recovery_required: bool
    mutation_locally_blocked: bool
```

`GameSnapshot` is the normalized Adapter-v1 view. UNKNOWN remains UNKNOWN.

The envelope must never include:

- account credentials, 2FA, cookies, tickets or auth/session secrets;
- Control API nonce;
- shell/environment secrets;
- raw memory pointers/addresses;
- raw packet payloads by default;
- raw keyboard/mouse handles;
- Track A lease tokens or writable registration handles;
- arbitrary process-control handles.

Capability/evidence/authority/freshness remain distinct. A capability advertised in the envelope does not imply current mutation authority.

## 4. Policy decision

```yaml
PolicyDecision:
  schema_version: 1
  decision_id: string
  observation_id: string
  observation_hash: string
  kind: NO_OP | REQUEST_ACTION | REQUEST_SCENARIO | REQUEST_ABORT | REQUEST_PAUSE
  proposal: PolicyActionProposal | PolicyScenarioProposal | null
  reason_codes: [SemanticKey]
  safe_summary: string | null
```

`reason_codes` and `safe_summary` are bounded non-secret operator evidence. No implementation requires or persists hidden chain-of-thought/model reasoning.

A stale/missing `observation_id`/hash is grounds for deterministic refusal or fresh re-evaluation; the policy cannot request that stale state be treated as authoritative.

## 5. Bounded action proposal

```yaml
PolicyActionProposal:
  kind: SemanticKey
  parameters: ScenarioV1ActionParameters
  timeout_ms: integer
  requested_budget_ceiling: SideEffectBudget | null
```

Rules:

- `kind`/`parameters` must be representable by an admitted Scenario-v1 semantic action; raw coordinates/keys/opcodes/function addresses/process IDs are not an escape hatch;
- proposal timeout/budget may only narrow accepted deterministic limits, never raise configured run/operator limits;
- proposal contains no authority grant, lease token, credential, shell command, memory write, arbitrary process action, raw network action or unrestricted input primitive;
- the domain converts the proposal into the same validated Scenario/ActionRequest path used by human/browser/CLI operations;
- a rejected proposal is a normal result and cannot be retried through a bypass path.

For multi-step behavior, `PolicyScenarioProposal` is a bounded validated Scenario-v1 document/request. The policy may choose among admitted semantics; it may not define new raw adapter operations at runtime.

## 6. Deterministic enforcement outside policy

The policy/model never owns or overrides:

- Scenario-v1 parser/schema/hash rules;
- MutationCoordinator;
- `dispatch_gate`;
- ActionLedger/RequestLedger idempotency;
- BudgetLedger;
- STOP/reset/recovery-required state;
- capability validation;
- freshness/identity fences;
- current Track A lease/registration/Gate/guard/input-lock authority;
- adapter one-shot dispatch commit;
- Recorder privacy classification;
- artifact finalization/recovery.

Every accepted policy proposal is revalidated by deterministic Control Center code at submission and again at the final mutation boundary exactly like any other operator-originated request.

Policy/model failure, timeout, malformed output or unavailability resolves to bounded NO_OP/refusal/fallback chosen by deterministic code. It never disables STOP or safety checks.

## 7. Decision-loop ownership

A future automation engine may repeatedly request observations and make decisions, but deterministic orchestration owns:

- maximum decision rate;
- maximum active/pending proposals;
- scenario/run timeouts;
- side-effect budgets;
- cancellation;
- backpressure;
- STOP precedence;
- recovery after crash/restart;
- policy process health/timeouts.

Unknown/unbounded policy scheduling requirements fail closed.

## 8. Ollama / model consumers

`TIBIA-RE-OLLAMA-LOCAL-RESEARCH-AGENT-POC` or another model may later implement a consumer of this boundary.

It must not:

- create a second Control Center;
- become a dependency of deterministic safety-critical execution;
- receive credentials/Control API nonce/Track A writable authority merely to reason;
- call adapters, shell, process control, raw memory writes or unrestricted input directly;
- promote its own output to capability/evidence/authority;
- bypass Scenario/MutationCoordinator/Recorder on timeout or refusal.

Model output is treated as untrusted structured policy intent. Deterministic parsing, schema validation, limits, safety and final authority remain outside the model.

## 9. Result feedback

```yaml
PolicyResultEnvelope:
  schema_version: 1
  decision_id: string
  accepted: bool
  resource_id: string | null
  status: string
  reason_codes: [string]
  result_ref: string | null
  evidence_refs: [string]
  next_observation_required: bool
```

The result envelope is a projection of canonical Control Center run/action state. It cannot rewrite ActionLedger/Artifact truth.

An ambiguous mutation remains AMBIGUOUS to the policy. The policy cannot reinterpret it as failure/no-effect and automatically request a duplicate retry.

## 10. Idempotency and replay

A future policy ingress must map each decision submission to the existing RequestLedger semantics and each semantic action attempt to ActionLedger semantics.

Same logical decision/request replay must not create duplicate runs/actions. A deliberate logical retry uses a new request/action identity and is permitted only when deterministic execution semantics allow it.

Policy-local IDs are never sufficient to override backend-global RequestLedger or ActionLedger truth.

## 11. Recorder/evidence

Recorder may persist bounded decision provenance:

```text
decision_id
policy implementation/version
observation_id/hash
proposal hash
reason_codes
safe_summary when admitted
accept/refuse/result refs
```

Do not persist secret prompts, credentials, raw hidden reasoning, arbitrary model debug dumps or unsanitized exception text into normal artifacts.

A policy/model statement is not causal/capability evidence by itself.

## 12. Versioning

Policy Boundary major version 1 is additive-only.

Changing these invariants requires explicit contract review:

- policy output is untrusted intent;
- no direct adapter/credential/shell/process/raw-memory/unrestricted-input authority;
- deterministic safety/authority remains outside policy;
- policy proposals re-enter the ordinary Scenario/ActionRequest path;
- STOP/ledgers/budgets/recovery remain authoritative;
- model unavailability cannot block deterministic safety.

## 13. Future implementation acceptance

Before enabling any automated official-client policy loop, prove at minimum:

1. malformed/oversized policy output is rejected before domain execution;
2. stale observation proposal refuses or revalidates against fresh state;
3. policy cannot increase configured budget/timeout/rate ceilings;
4. policy cannot construct raw adapter/input/process/memory/network actions;
5. policy timeout/crash becomes bounded NO_OP/refusal without disabling STOP;
6. duplicate decision/request cannot duplicate a semantic action;
7. AMBIGUOUS result cannot be auto-retried as proven no-effect;
8. STOP/recovery-required blocks policy-originated mutation exactly as human-originated mutation;
9. current Track A final authority is still required at physical dispatch;
10. policy artifacts contain only bounded non-secret structured provenance;
11. Ollama/model process has no direct credential/Track A writable-authority channel;
12. disabling/removing the policy consumer leaves deterministic Control Center safety and manual research workflows operational.