# OTC Vision P2 Read-Only — Owner Alias Registry

```yaml
alias_registry_version: 1.3.0
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

The coordinator refreshes live state, owns worker selection and invokes subordinate workers itself. The owner should normally provide only the coordinator/programme goal; routine worker model/effort choice is coordinator work.

For supported Wave 1 aliases the coordinator uses the bounded bridge. Mechanical dispatch safeguards belong to the bridge; GitHub/CI/status/restack lifecycle remains coordinator work.

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

## Worker routing

The coordinator selects the smallest sufficient worker model/effort from `docs/agents/EXECUTION_PROTOCOL.md` using the live task's risk and evidence. Historical per-alias effort labels are not dispatch commands and are intentionally omitted here so the owner and coordinator do not micromanage routing from this registry.

Manual worker commands remain fallback/resume entry points; they do not change the coordinator-first operating model.

## Spark note

Do not treat this registry as standing permission for direct owner-funded Spark use. Current trusted-base `AGENTS.md` and the owner's current invocation decide whether a specific model/provider is authorized. The repository's central advisory Spark PR pre-review remains separate from worker execution. Low/exhausted Luna/Terra/Sol quota is not itself a routing reason or authorization to spill execution into Spark; persist the budget stop and wait/rotate unless Spark has an independent authorized task reason.

## Phase boundary

All aliases in this registry are Phase 2 read-only. They grant no GUI/anti-idle input, login, credentials, character selection, gameplay, process control, process memory, packet/payload capture or physical executor authority. Phase 3+ requires a separate prompt/task/authorization family.
