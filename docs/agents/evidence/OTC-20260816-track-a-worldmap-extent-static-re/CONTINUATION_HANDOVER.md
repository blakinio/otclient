# Continuation handover — worldmap extent static RE

Continue the existing task; do not create a replacement research programme.

```yaml
repository: blakinio/otclient
task: OTC-20260816-track-a-worldmap-extent-static-re
branch: research/OTC-20260816-track-a-worldmap-extent-static-re
pr: 367
phase: investigate
execution_class: github_hosted
runtime_access: none
mutation_authorized: false
owner_funded_ai_api_authorized: false
run_scope: single_task
continuation_policy: stop_at_task_boundary
```

## Required startup

Read and obey, in authority order where applicable:

1. repository `AGENTS.md` and live governance;
2. `docs/agents/PROMPTING_STANDARD.md`;
3. `docs/agents/PROMPTING_HANDOVER.md`;
4. `docs/agents/prompts/OTCLIENT_TIBIA_RE_VIEWPORT_CONTINUATION.md` if/when it is canonical on the task's live base, otherwise treat the owner's explicit viewport objective plus this handover as task input without overriding main governance;
5. active task record `docs/agents/tasks/active/OTC-20260816-track-a-worldmap-extent-static-re.md`;
6. report `docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md`;
7. all evidence under `docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/`.

Before any write, refresh `main`, PR #367, reviews, CI, ownership and overlapping PRs/tasks. Preserve one-task/one-PR ownership. Do not use Codex, OpenAI API, or owner-funded tokens/limits.

## Objective

Recover the complete static patch/dependency graph required to safely increase official Tibia worldmap viewport/map extent across:

- `TWorldMapExtent`;
- `TWorldMapSubfieldExtent`;
- `TWorldMapViewport`;
- `TWorldMapStorage`;
- `TWorldmapProtocolMessageHandler`;
- `TWorldMapRenderProvider`;
- `TWorldMapCamera`;
- `TWorldMapPicker`.

Do not modify client bytes in this phase. Recover dimension fields, constructors/default writers, all material readers/writers, allocations/capacities, loop bounds, parser assumptions, storage indexing/eviction, clipping/culling, camera transforms and picker bounds. Record FACT/INFERENCE/UNKNOWN/CONFLICT separately.

## Current retained evidence

The task has already recovered:

- raw provenance artifact `9227370490` with 90 strip rows;
- two Z=7 horizontal samples X=`32537..32554` (18 consecutive X) at Y=`32502` and Y=`32516`, with exact delta Y=14;
- exact retained code leads BP1/static `0xcecc70` and BP2/static `0xcecf40`, observer-assigned `CreateOnMap` and `ChangeOnMap`;
- shared `owner+0x10 -> virtual slot +0xa0` path and event reads `+0x18/+0x20/+0x28`, plus `ChangeOnMap` gate `event+0x10 & 1` and helper lead `0xceca50`;
- richer exact-static census artifact `9246756211` with target RTTI/control-block strings and coordinate-to-shared-tile `unordered_map` instantiation;
- historical exact-build leads `0xcd4e20`, `0xcec8d0`, `0x19a8ea3` and typeinfo/relocation anchors already recorded in evidence.

Do not upgrade observer labels to independent symbols without recovering their source provenance. Do not call event offsets viewport dimensions without a direct field/writer proof.

## Newly supplied official package

The owner supplied `/mnt/data/tibia.x64.tar.gz` in the preceding ChatGPT session and stated it was downloaded on 2026-08-16 from the official Tibia website. The bytes are **not committed to the public repository**. Durable metadata is in `20260816-owner-upload-launcher-package.md`.

Verified archive fence:

```text
size    29477141
sha256  04a87c801d3855f4da1b07e201dff1f79acc8528c57c984131c3a2a88cb60ea7
```

`Tibia/Tibia` inside it:

```text
size    1460808
sha256  a5fc6e8ee8246868263c438539a54ea045bd048a1bea45f968fc2f498b682ca0
format  ELF 64-bit PIE x86-64
```

Static strings show launcher/update/package-version logic. It is therefore a launcher/bootstrap candidate, **not** the historical 51,965,216-byte exact game-client ELF. The old exact fence remains historical evidence; do not silently substitute this launcher binary for it.

## Immediate next action

First recover, statically and without GUI/login, the launcher's package metadata/update mechanism sufficiently to determine the current official game-package identity/version and whether its game payload can be materialized on GitHub-hosted infrastructure. Prefer extracting URLs/config/package metadata from the supplied archive or official public metadata rather than executing the launcher.

If a current game payload becomes available, establish a **new explicit immutable fence** (source provenance, version/build, size, SHA-256) before comparing it with historical `15.32.df7b29`. Then determine whether target RTTI/types and worldmap structures persist and continue the graph recovery.

In parallel, continue mining same-repository retained artifacts/history for the historical graph. Priority leads: recover provenance/source for BP1/BP2 observer naming; correlate `0xceca50`, `0xcecc70`, `0xcecf40`, `0xcd4e20`, `0xcec8d0`; recover constructor/typeinfo/vtable/storage/render/camera/picker relationships.

## Runtime boundary

No runtime is currently required. Do not use Synology for static RE. If a later discriminator genuinely requires GUI/runtime, obey Track A admission/ownership/Gate A/rebind/Gate B/target-uniqueness/supervisor governance and reuse only an admissible existing persistent session. Never create a second desktop/X11/VNC/login session as fallback. If safe reuse is impossible, record WAITING/BLOCKED.

## Acceptance

This phase is ready for patch design only when the evidence graph identifies the relevant extent/dimension storage and proves all material consumers/constraints across protocol, storage, render, camera and picker, with fixed allocations/loop/parser/clipping assumptions enumerated. Until then remain `MORE_STATIC_RE_NEEDED` or an exact blocker; do not claim `STATIC_PATCH_GRAPH_READY`.

Persist every material discovery to the existing task/report/evidence and keep PR #367's description/status synchronized with the live task. Validate the exact final head with repository CI before any closeout claim.
