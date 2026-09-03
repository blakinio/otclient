# BE4F48 Queue Drain Consumption Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove or fail closed on the exact-current static dataflow from the already-proven 16-byte queued `tibia::protobuf::protocol::GameclientMessage` identity into owned `TProtocolMessageQueue` callback `0xbd2190`, then follow at most one uniquely identity-preserving next writer edge.

**Architecture:** Use one exact-SHA-fenced Python/Capstone/pyelftools analyzer on a disposable GitHub-hosted runner. The analyzer independently re-proves the local `sendLogin` adapter pair and queue insertion, then restricts all new analysis to FDE `0xbd2190..0xbd2495`, concrete queue storage members reached there, and at most one next target that receives the exact object/owner identity or a uniquely defined derivative. Any identity fork or non-unique writer edge terminates as sanitized `SOURCE_BLOCKER` instead of broadening into a socket/QMeta/TCP census.

**Tech Stack:** Python 3, `pyelftools`, Capstone, GitHub Actions on Ubuntu 24.04, deterministic sanitized JSON artifacts.

**Spec:** `docs/agents/prompts/OTC_BE4F48_QUEUE_DRAIN_CONSUMPTION.md`

## Global Constraints

- Exact client: `15.32.be4f48`, size `52105824`, SHA-256 `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`.
- Promoted source boundary: exact 16-byte pair `{object=allocation+0x10, owner=allocation}` copied unchanged through queue insertion `0xbd24a0`; unique owned callback `0xbd2190`, FDE `0xbd2190..0xbd2495`.
- `runtime_access: none`; never execute the official client, login, use credentials, inspect process memory, capture packets, use OCR/Vision, or run official-service E2E.
- Do not reopen or extend PR #870's analyzer family. Re-implement only the minimal local proof needed for this new source boundary in a new tool namespace.
- Do not modify Track B PR #284 and do not infer Field6 or any Track B wire delta.
- No global socket/TCP/QMeta/writer sweep, no broad call graph, no address-proximity proof and no historical cross-build address transfer.
- Raw client bytes may exist only transiently inside the hosted job after repository-only GREEN and must be deleted before artifact upload.
- TDD is mandatory: a real repository-only RED must occur before exact-client metadata or bytes are materialized; each evidence-derived implementation correction gets a failing deterministic contract test first.
- Positive causal consumption requires exact object/owner propagation or one uniquely identity-preserving derivative into a semantic consumer.
- Positive final queue writer identity additionally requires exactly one next edge plus an independent vtable/owner/caller cross-check.

---

### Task 1: Repository-only RED gate

**Files:**
- Create: `tools/tibia_re_be4f48_queue_drain_consumption/test_contract.py`
- Create: `.github/workflows/tibia-official-client-re-be4f48-queue-drain-consumption.yml`
- Modify: `docs/agents/tasks/active/OTC-20260903-be4f48-queue-drain-consumption.md`

**Interfaces:**
- Consumes: exact fence and promoted exact-current anchors from the task/spec.
- Produces: a repository-only test that imports `drain_consumption.py` and fails with `drain_consumption.py is missing: expected RED before client materialization`; the workflow runs this step before package metadata access or client materialization.

- [ ] **Step 1: Write the failing contract**

Create a test with this required import gate and exact constants:

```python
ROOT = Path(__file__).resolve().parent
ANALYZER = ROOT / "drain_consumption.py"
assert ANALYZER.is_file(), "drain_consumption.py is missing: expected RED before client materialization"

EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
ADAPTER_FDE = (0xBD3050, 0xBD34DD)
QUEUE_VTABLE_AP = 0x30ED588
QUEUE_INSERT = 0xBD24A0
DRAIN_FDE = (0xBD2190, 0xBD2495)
```

After import exists, the same test must assert the module constants exactly match these values and must exercise pure helpers for hexadecimal formatting, Itanium nested-name parsing, identity-state joining and terminal classification without needing Capstone/ELF imports.

- [ ] **Step 2: Add the hosted workflow with RED ordered before network access**

The first workflow steps are exactly ordered as:

```yaml
- name: Validate repository contract
  run: |
    python3 tools/tibia_re_be4f48_queue_drain_consumption/test_contract.py
    python3 -m py_compile tools/tibia_re_be4f48_queue_drain_consumption/drain_consumption.py
- name: Prepare secret-free current official client metadata through WARP
  # unreachable while RED
- name: Materialize exact client transiently and run bounded static discriminator
  # unreachable while RED
```

The workflow is branch/path-scoped to this task and uses no secrets.

- [ ] **Step 3: Commit only RED surfaces**

Commit only the failing contract, workflow and task checkpoint. Do not add `drain_consumption.py` in this commit.

- [ ] **Step 4: Verify RED from hosted Actions**

Expected first actionable failure:

```text
AssertionError: drain_consumption.py is missing: expected RED before client materialization
```

The metadata/WARP step, client materialization step and artifact upload must all be skipped. Record workflow/job IDs in the task before production analyzer code is added.

---

### Task 2: Minimal exact-fenced local analyzer

**Files:**
- Create: `tools/tibia_re_be4f48_queue_drain_consumption/drain_consumption.py`
- Modify: `tools/tibia_re_be4f48_queue_drain_consumption/test_contract.py`
- Modify: `docs/agents/tasks/active/OTC-20260903-be4f48-queue-drain-consumption.md`

**Interfaces:**
- Consumes: exact-current ELF path plus version/size/SHA arguments.
- Produces: `result.json` with exact fence, independently re-proven queue identity, drain-callback local evidence, causal-consumption classification, at most one next writer edge, safety markers and a terminal result.

- [ ] **Step 1: Implement only the ELF/FDE primitives required by the fixed local seeds**

Define:

```python
EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
ADAPTER_FDE = (0xBD3050, 0xBD34DD)
QUEUE_VTABLE_AP = 0x30ED588
QUEUE_INSERT = 0xBD24A0
DRAIN_FDE = (0xBD2190, 0xBD2495)
```

Implement lazy Capstone/pyelftools imports, section/FDE mapping, relocation-aware qword reads, concrete vtable decoding, direct/indirect-call extraction, RIP-relative target resolution and bounded instruction-context serialization. Do not implement a repository/global function scanner.

- [ ] **Step 2: Independently re-prove the 16-byte queued identity before drain analysis**

Require the exact adapter-local facts:

```text
0xbd3070 call 0x4d8670
0xbd3087 mov rbx, rax
0xbd3099 lea r15, [rbx + 0x10]
0xbd31b4 mov rax, [r12]
0xbd31b8 mov rax, [rax + 0x68]
0xbd31bc mov [rsp], r15
0xbd31c0 mov [rsp + 8], rbx
0xbd31de mov rsi, rsp
0xbd31e1 mov rdi, r12
0xbd31e4 call rax
```

Resolve the concrete queue vtable at `0x30ed588`; require RTTI `tibia::protocol::TProtocolMessageQueue` and slot `+0x68 -> 0xbd24a0`.

Require queue insertion to copy a 16-byte value from incoming `rsi` into queue storage and advance the queue end by `0x10`, including the exact current local instructions already promoted at `0xbd24cf`, `0xbd24d3`, `0xbd24d7`, `0xbd24f3` and `0xbd24f7`. If any assertion fails, exit nonzero as fence/local-proof failure rather than searching for replacements.

- [ ] **Step 3: Build a bounded symbolic identity tracker for one FDE**

Represent tracked values as immutable labels:

```python
UNKNOWN = frozenset()
OBJECT = frozenset({"object"})
OWNER = frozenset({"owner"})
PAIR = frozenset({"object", "owner"})
```

Track only register/stack/memory moves, `lea`, simple add/sub constant address derivations and 16-byte SIMD copies that occur inside `DRAIN_FDE`. Record a value as identity-preserving only when its definition has exactly one predecessor label; merging two distinct possible predecessors produces `UNKNOWN` rather than a guess. Track queue-memory addresses only when their base derives from callback `this` and their displacement is one of the concrete queue members touched by both insertion/owned-callback evidence (`0x90`, `0xa0`, plus any directly adjacent 16-byte element load proven inside the callback).

The tracker must emit deterministic `identity_events` containing instruction address, source label, destination label and proof kind. It must never scan another FDE to fill a missing identity.

- [ ] **Step 4: Classify callback consumption conservatively**

Decode exactly `0xbd2190..0xbd2495`. Require the actual FDE to equal `DRAIN_FDE` and collect all queue-member accesses, direct calls, indirect calls and full bounded instruction records.

`queued_gameclientmessage_causal_consumption=true` only when both conditions hold:

1. a concrete 16-byte queue element derived from the same storage written by `QUEUE_INSERT` is reconstructed as `{object, owner}` or its object pointer is loaded from that exact element while the owner/control identity remains uniquely paired; and
2. that identity reaches one semantic consumption call/virtual call argument with no fork or competing indistinguishable target.

Otherwise keep it false and set `FIRST_MISSING_BOUNDARY` to the first exact failed local relation, never to a generic networking gap.

- [ ] **Step 5: Follow at most one next writer edge**

If and only if causal consumption is proven and exactly one call target receives the preserved identity, resolve that target/FDE. Follow no other calls. A positive `next_unique_writer_edge` requires one independent cross-check chosen from:

```text
A. the call is through a concrete vtable slot whose RTTI owner is decoded from the same object identity; or
B. one unique concrete owner/caller relation in the already-reached FDE confirms the same target.
```

If neither cross-check passes, emit the target as a candidate inside analysis evidence but keep `NEXT_UNIQUE_WRITER_EDGE=UNKNOWN` and `FINAL_QUEUE_WRITER_IDENTIFIED=false`.

Never claim a final TCP writer merely because a reached local target has a networking-looking call/string; `FINAL_TCP_WRITER_IDENTIFIED` remains false unless the exact identity itself reaches a separately causal TCP boundary, which this task is not authorized to search globally.

- [ ] **Step 6: Emit the required terminal schema**

The result must include:

```json
{
  "schema": "otclient.track-a.be4f48-queue-drain-consumption.source.v1",
  "exact_client": {"version": "15.32.be4f48", "size": 52105824, "sha256": "552d...09e4e1", "fence_proven": true},
  "serialized_queue_object_identity_proven": true,
  "owned_drain_callback": "0xbd2190",
  "queued_gameclientmessage_causal_consumption": false,
  "next_unique_writer_edge": "UNKNOWN",
  "final_queue_writer_identified": false,
  "final_tcp_writer_identified": false,
  "final_writer_contract": "UNKNOWN",
  "runtime_access": "none",
  "official_client_execution": false,
  "official_service_e2e_count": 0,
  "track_b_pr_284_modified": false,
  "raw_client_uploaded": false,
  "terminal_result": "SOURCE_BLOCKER",
  "FIRST_MISSING_BOUNDARY": "<first exact local missing relation>",
  "next_action": "<one bounded continuation or coordinator promotion>"
}
```

The example false/UNKNOWN values are the fail-closed baseline; promote only fields directly proved by the analyzer.

- [ ] **Step 7: Verify repository-only GREEN**

The contract must print `BE4F48_QUEUE_DRAIN_CONSUMPTION_CONTRACT=PASS`, and `py_compile` must succeed before the workflow proceeds to WARP/package metadata.

---

### Task 3: Exact-current static evidence and one evidence-derived correction budget

**Files:**
- Modify only if a new failing contract justifies it: `tools/tibia_re_be4f48_queue_drain_consumption/test_contract.py`
- Modify only after that RED: `tools/tibia_re_be4f48_queue_drain_consumption/drain_consumption.py`
- Modify: `docs/agents/tasks/active/OTC-20260903-be4f48-queue-drain-consumption.md`

**Interfaces:**
- Consumes: exact-current public launcher metadata and transient exact ELF.
- Produces: sanitized deterministic static evidence artifact; no raw client bytes persist.

- [ ] **Step 1: Materialize only the exact fenced public client through the existing WARP pattern**

Read `https://static.tibia.com/launcher/tibiaclient-linux-current/package.json` through a transient WARP/wireproxy tunnel. Require the live package tuple to match the exact version/size/SHA before downloading the packed client. Verify packed hash/size from package metadata, decompress transiently, verify unpacked hash/size, run the analyzer without executing the ELF, delete packed/unpacked bytes, and upload only sanitized JSON.

- [ ] **Step 2: Inspect the first sanitized result**

Accept a terminal result immediately if it already proves/falsifies the boundary without ambiguity. If the emitted `0xbd2190` local evidence exposes exactly one previously unmodelled deterministic identity-preserving instruction form, consume the task's one evidence-derived correction budget; otherwise stop at the first missing boundary.

- [ ] **Step 3: For one admissible correction, write RED first**

Add a pure deterministic synthetic test that models only the newly observed instruction/dataflow form and fails because the current identity tracker returns `UNKNOWN`. Verify this repository-only RED without current-client materialization.

- [ ] **Step 4: Implement only that one observed local form and return GREEN**

Add the smallest identity rule needed by the failing test, rerun the contract to GREEN, then permit one final exact-client static rerun. Do not add generic call graph, socket, QMeta or writer discovery.

- [ ] **Step 5: Freeze the source result**

After the final exact-client run, no second repair cycle is allowed inside this alias. Classify one of:

```text
QUEUE_DRAIN_CONSUMPTION_PROVEN
FINAL_QUEUE_WRITER_PROVEN
SOURCE_BLOCKER
```

`FINAL_QUEUE_WRITER_PROVEN` requires both causal consumption and one unique next writer edge with the independent cross-check. `SOURCE_BLOCKER` names the first exact missing identity/ownership relation.

---

### Task 4: Durable evidence, falsification and source-PR closeout

**Files:**
- Create: `docs/agents/evidence/OTC-20260903-be4f48-queue-drain-consumption/result.json`
- Create: `docs/agents/evidence/OTC-20260903-be4f48-queue-drain-consumption/20260903-source-result.md`
- Modify: `docs/agents/tasks/active/OTC-20260903-be4f48-queue-drain-consumption.md`
- Modify: PR #874 description only through GitHub metadata; do not promote source analyzer to `main` from this source PR.

**Interfaces:**
- Consumes: final sanitized exact-head workflow artifact and live PR/CI state.
- Produces: a durable source result that a separate clean coordinator promotion can consume without trusting chat or raw artifacts.

- [ ] **Step 1: Persist only sanitized evidence**

Record exact source head, workflow/job/artifact IDs, artifact digest, result JSON digest, exact fence, proved/withheld fields, safety markers and terminal classification. Never commit raw ELF bytes, compressed client bytes, credentials, packet material or unsanitized disassembly dumps that contain proprietary binary bytes.

- [ ] **Step 2: Independently falsify every positive claim**

Re-read the exact final diff and sanitized JSON without relying on the implementer summary. For each positive field, verify:

```text
EXACT_CLIENT_FENCE_PROVEN -> live public package + analyzer fence agree
SERIALIZED_QUEUE_OBJECT_IDENTITY_PROVEN -> adapter and insertion are independently asserted
OWNED_DRAIN_CALLBACK -> exact FDE is 0xbd2190..0xbd2495
QUEUED_GAMECLIENTMESSAGE_CAUSAL_CONSUMPTION -> exact object/owner identity reaches the semantic consumer with no fork
NEXT_UNIQUE_WRITER_EDGE -> exactly one identity-preserving edge and independent ownership/vtable/caller cross-check
FINAL_QUEUE_WRITER_IDENTIFIED -> previous two conditions both hold
FINAL_TCP_WRITER_IDENTIFIED -> only if exact identity causally reaches that boundary; otherwise false
```

Any failed falsification demotes the affected field to false/`UNKNOWN` and usually makes the source result `SOURCE_BLOCKER`.

- [ ] **Step 3: Verify safety and cross-track isolation**

Confirm changed files are limited to this task's owned paths, PR #284 head is unchanged by this task, `runtime_access=none`, official-client execution/login/process-memory/packet-capture/OCR are false, raw client upload is false and official-service E2E count is zero.

- [ ] **Step 4: Run exact-head validation**

Require the task-specific hosted workflow plus emitted repository `CI`, Track A runtime governance and self-hosted PR boundary checks that apply to the final source head. Inspect any first failure directly. Also verify `git diff --check` inside the workflow and zero unresolved material review threads.

- [ ] **Step 5: Update source PR #874 to the exact terminal result**

Keep it Draft and do not merge the disposable source analyzer. The PR body must include exact final head, run/job/artifact IDs, terminal fields, first missing boundary, safety markers and `NEXT_ACTION=clean coordinator promotion from fresh trusted main`.

- [ ] **Step 6: Hand off to clean coordinator promotion**

The source result is complete only as a source discriminator; repository promotion is a separate clean task from fresh `main`. That coordinator must promote only sanitized facts, close #874 unmerged as consumed after promotion, archive lifecycle state, and decide the next independent boundary. No Track B change is authorized directly from the source PR.
