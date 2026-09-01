# OTC Vision P2 Read-Only — Owner Alias Registry

```yaml
alias_registry_version: 1.1.0
programme_id: OTC-VISION-P2-READONLY
repository: blakinio/otclient
canonical_prompt_family: docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md
coordination_contract: docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md
```

## Start here

Run the coordinator first:

```text
Uruchom OTC-VISION-P2-COORDINATOR autonomicznie.
```

The coordinator must refresh live state, create/reconcile concrete worker tasks/branches/ownership and prepare Wave 1. When coordinator-managed Codex execution is available, it also selects and invokes the subordinate workers itself. Do not manually invent worker branches, select worker models/effort, or duplicate tasks when the coordinator can resolve and dispatch them.

## Wave 1 — up to five workers

Normal mode: the supervising coordinator invokes these worker aliases itself through available Codex execution tooling after live anti-duplication/ownership checks. The commands below are manual fallback/resume entry points only when the execution bridge is unavailable or the owner explicitly chooses separate worker windows:

```text
Uruchom OTC-VISION-P2-RUNTIME-ADMISSION autonomicznie.
Uruchom OTC-VISION-P2-CAPTURE-EDGE autonomicznie.
Uruchom OTC-VISION-P2-RUNTIME-SIGNALS autonomicznie.
Uruchom OTC-VISION-P2-EDGE-TRANSPORT autonomicznie.
Uruchom OTC-VISION-P2-CONTROL-BRIDGE autonomicznie.
```

Repository/static work may run concurrently. The coordinator serializes actual observation of the one official-client runtime; a worker may touch the real runtime only after its own current `runtime_access: read_only` admission and assigned observation window.

## Wave 2

After the coordinator accepts the required Wave 1 contracts:

```text
Uruchom OTC-VISION-P2-VISION-RECONCILIATION autonomicznie.
```

## Wave 3 — fresh validator

After an exact integration head exists:

```text
Uruchom OTC-VISION-P2-E2E-AUDIT autonomicznie.
```

Use a **fresh agent window/context** for this alias. It is a falsification role and should not inherit implementer narrative.

## Resume after effort/context/session exhaustion

No long handoff prompt is required. For the same worker, open a new window and run only:

```text
Kontynuuj <ALIAS> autonomicznie.
```

Examples:

```text
Kontynuuj OTC-VISION-P2-RUNTIME-SIGNALS autonomicznie.
Kontynuuj OTC-VISION-P2-CAPTURE-EDGE autonomicznie.
Kontynuuj OTC-VISION-P2-COORDINATOR autonomicznie.
```

The canonical prompt requires the outgoing worker to persist a coherent task checkpoint, branch/head/Draft PR, validation evidence and exactly one `next_action` after every meaningful subtask and before unsafe context/effort/tool exhaustion. The replacement worker resumes the existing task; it must not recreate completed discovery or open a duplicate task/PR.

## Recommended agent and effort

| Alias | Primary agent/mode | Reasoning effort | Why |
|---|---|---:|---|
| `OTC-VISION-P2-COORDINATOR` | Chat/GitHub supervising coordinator; invokes subordinate Codex workers for execution/audit and uses its own checkout only when coordinator-owned edits require it | **xhigh coordinator reasoning; worker model/effort dynamic** | cross-lane dependencies, authority, dispatch, acceptance and final integration |
| `OTC-VISION-P2-RUNTIME-ADMISSION` | Codex | **xhigh** | live target identity/governance mistakes have high downstream blast radius |
| `OTC-VISION-P2-CAPTURE-EDGE` | Codex | **high** | bounded implementation with secret-safe capture/integrity constraints |
| `OTC-VISION-P2-RUNTIME-SIGNALS` | Codex | **xhigh** | provenance/freshness/semantic-authority discrimination is subtle and safety-critical |
| `OTC-VISION-P2-EDGE-TRANSPORT` | Codex | **high** | bounded transport/security implementation, no runtime semantics authority |
| `OTC-VISION-P2-CONTROL-BRIDGE` | Codex | **high** | existing Control Center integration with durable failure/restart semantics |
| `OTC-VISION-P2-VISION-RECONCILIATION` | Codex | **xhigh** | combines untrusted model evidence with authoritative runtime evidence |
| `OTC-VISION-P2-E2E-AUDIT` | **fresh Codex validator** | **xhigh** | must actively falsify the exact integration result with independent context |

Worker effort values in this table are historical risk recommendations, not mandatory fixed dispatch settings. A coordinator-managed Codex dispatch follows `EXECUTION_PROTOCOL.md` and its empirical calibration, selecting the smallest sufficient model/effort for the live task. If a manually selected client exposes only `low/medium/high`, use **high** where a manual fallback explicitly requires `xhigh`.

## Spark note

Do not treat this registry as standing permission for direct owner-funded Spark use. Current trusted-base `AGENTS.md` and the owner's current invocation decide whether a specific model/provider is authorized. The repository's central advisory Spark PR pre-review remains separate from worker execution.

## Phase boundary

All aliases in this registry are Phase 2 read-only. They grant no GUI/anti-idle input, login, credentials, character selection, gameplay, process control, process memory, packet/payload capture or physical executor authority. Phase 3+ requires a separate prompt/task/authorization family.
