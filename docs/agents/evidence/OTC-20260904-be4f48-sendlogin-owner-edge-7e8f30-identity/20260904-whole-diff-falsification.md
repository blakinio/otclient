# Whole-diff falsification — sendLogin owner edge `0x7c67b8 -> 0x7e8f30`

Date: 2026-09-04
Task: `OTC-20260904-be4f48-sendlogin-owner-edge-7e8f30-identity`
PR: #894
Trusted base: `main@7e67c67783b19575ec7f378c7be49cb69d87f1ce`
Scientific source head: `9c68d92657100b054c6d5006ab46ddc5303112ee`

## Review objective

Attempt to falsify the terminal `SOURCE_BLOCKER` claim from the complete PR diff and primary workflow evidence without accepting the worker summary as proof.

## Changed-path boundary

The reviewed PR changes only the declared task scope:

```text
.github/workflows/tibia-official-client-re-be4f48-sendlogin-owner-edge-7e8f30-identity.yml
tools/tibia_re_be4f48_sendlogin_owner_edge_7e8f30_identity/**
docs/agents/tasks/active/OTC-20260904-be4f48-sendlogin-owner-edge-7e8f30-identity.md
docs/agents/evidence/OTC-20260904-be4f48-sendlogin-owner-edge-7e8f30-identity/**
```

No Track B PR #284 path, queue/QSlot/writer path, production/runtime code or unrelated repository surface is modified.

## Falsification matrix

| Check | Evidence | Result |
|---|---|---|
| Exact client fence is fail-closed before analysis | workflow validates version `15.32.be4f48`, unpacked size `52105824`, SHA-256 `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`; source run emitted exact-fence PASS | PASS |
| TDD RED precedes client materialization | run `33879930241`, job `101045813815` failed on missing `edge_identity.py`; WARP/materialization/result/upload steps were skipped | PASS |
| Analysis starts at the promoted callee only | analyzer constant is `OWNER_EDGE_CALLEE = 0x7E8F30` and obtains only that address's containing FDE | PASS |
| Consumed #884/#889 discovery is not repeated | repository contract rejects owner-FDE/caller-discovery tokens; full diff contains no new owner-FDE scan or caller census | PASS |
| At most one internal identity edge can be followed | analyzer admits an internal target only when exactly one same-object direct candidate exists; source result has zero candidates and followed edge `null` | PASS |
| Positive type claim requires object-tied proof | owner is proven only from one exact object-bound vptr/Itanium RTTI identity; no such event existed in source result | PASS |
| Fail-closed boundary matches evidence | source result has no callee object-bound typed vptr and no admissible internal identity edge, therefore owner remains `UNKNOWN` and terminal result is `SOURCE_BLOCKER` | PASS |
| Receiver is not inferred from adjacency/layout | `sendlogin_receiver_identity=UNKNOWN`, `sendlogin_receiver_identity_proven=false` | PASS |
| Withheld protocol claims remain withheld | sender/receiver pair false, causal binding false, `FIELD6_VALUE=UNKNOWN`, pre-success sequence `UNKNOWN` | PASS |
| Static-only safety boundary is preserved | no official-client execution/login/credentials/process-memory/packet capture/OCR/Vision/E2E; Track B #284 not modified | PASS |
| Raw proprietary client bytes are not retained | source run printed `RAW_CLIENT_RETAINED=false`; uploaded artifact contains only sanitized `result.json` | PASS |
| Persisted evidence agrees with primary run | repository `result.json` matches the sanitized JSON emitted by source run `33880393758` | PASS |

## Result

```text
WHOLE_DIFF_FALSIFICATION=PASS
MATERIAL_FINDINGS_OPEN=0
SOURCE_WORKER_SELF_PROMOTION_USED=false
SCIENTIFIC_TERMINAL_RESULT=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=CALLEE_INTERNAL_IDENTITY_EDGE_NOT_FOUND
```

This audit does not promote the source result into programme authority and does not authorize Track B mutation. A clean coordinator must consume this exact-current terminal evidence before admitting any new bounded step.
