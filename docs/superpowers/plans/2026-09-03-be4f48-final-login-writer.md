# BE4F48 Final Login Writer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove, or fail closed on, the exact-current source-only object/buffer path from native `sendLogin` through `TProtocolMessageQueue` to the unique final queue/TCP writer contract.

**Architecture:** Use one exact-SHA-fenced Python/Capstone analyzer on a disposable GitHub-hosted runner. Start only from promoted current `sendLogin`/queue anchors and independently re-prove local dataflow; follow the uniquely bound 16-byte queue item through queue drain and at most one evidence-derived next writer transition. Emit sanitized JSON and terminate `SOURCE_BLOCKER` as soon as the first required ownership/dataflow edge is non-unique.

**Tech Stack:** Python 3, `pyelftools`, Capstone, GitHub Actions on Ubuntu 24.04, deterministic JSON artifacts.

**Spec:** `docs/agents/prompts/OTC_BE4F48_FINAL_LOGIN_WRITER.md`

## Global Constraints

- Exact client: `15.32.be4f48`, size `52105824`, SHA-256 `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`.
- `runtime_access: none`; never execute the official client, login, use credentials, inspect process memory, capture packets, or run official-service E2E.
- No Track B PR #284 mutation and no sender/peer lane work from PR #869.
- No broad TCP/QMeta/socket sweep, address-proximity proof, historical cross-build address transfer, or generic writer architecture.
- Raw client bytes are transient and deleted before artifact upload; only deterministic sanitized JSON may persist.
- TDD is mandatory: real RED before client materialization, minimal GREEN, then one exact-client run.

---

### Task 1: Repository-only RED gate

**Files:**
- Create: `tools/tibia_re_be4f48_final_login_writer/test_contract.py`
- Create: `.github/workflows/tibia-official-client-re-be4f48-final-login-writer.yml`
- Modify: `docs/agents/tasks/active/OTC-20260903-be4f48-final-login-writer.md`

**Interfaces:**
- Consumes: exact fence and promoted current anchors from the task/spec.
- Produces: a repository-only test that imports `writer_path.py` and fails with `writer_path.py is missing: expected RED before client materialization` while the workflow orders this test before every network/package/client step.

- [ ] **Step 1: Write the failing contract**

```python
ANALYZER = ROOT / "writer_path.py"
assert ANALYZER.is_file(), "writer_path.py is missing: expected RED before client materialization"
```

The contract also requires constants for the exact fence, adapter `0xbd3050`, queue vtable AP `0x30ed588`, queue vslot `+0x68 = 0xbd24a0`, packet processor `+0x68 = 0xf4eca0`, and final-frame FDE `0xf4edd0..0xf4ef15`.

- [ ] **Step 2: Add the hosted workflow with RED before download**

```yaml
- name: Validate repository contract
  run: python3 tools/tibia_re_be4f48_final_login_writer/test_contract.py
- name: Prepare exact current client
  # unreachable while RED
```

The preparation step reads `package.json` through the existing WARP pattern, compares the live version/size/SHA to the exact fence, transiently materializes the ELF, runs the analyzer, deletes bytes, then uploads only `result.json`.

- [ ] **Step 3: Verify RED**

Inspect the first workflow run. Expected first actionable failure: missing `writer_path.py`; the package/client preparation step must be skipped.

- [ ] **Step 4: Checkpoint RED evidence**

Update the task with run/job IDs and `phase: red_verified` before adding production analyzer code.

---

### Task 2: Minimal exact-fenced writer discriminator

**Files:**
- Create: `tools/tibia_re_be4f48_final_login_writer/writer_path.py`
- Modify: `tools/tibia_re_be4f48_final_login_writer/test_contract.py`
- Modify: `docs/agents/tasks/active/OTC-20260903-be4f48-final-login-writer.md`

**Interfaces:**
- Consumes: raw exact-current ELF path and exact fence arguments.
- Produces: `result.json` with `serialized_queue_object_identity`, `final_queue_writer_identified`, `final_queue_writer_identity`, `final_tcp_writer_identified`, `final_tcp_writer_identity`, `final_writer_contract`, `terminal_result`, and `FIRST_MISSING_BOUNDARY`.

- [ ] **Step 1: Implement only ELF/FDE helpers needed by bounded seeds**

```python
EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
ADAPTER_FDE = (0xBD3050, 0xBD34DD)
QUEUE_VTABLE_AP = 0x30ED588
QUEUE_VSLOT_68 = 0xBD24A0
PACKET_PROCESSOR_VSLOT_68 = 0xF4ECA0
FINAL_FRAME_FDE = (0xF4EDD0, 0xF4EF15)
```

Helpers read ELF PT_LOAD bytes, decode only requested FDE instruction ranges, read relocations, resolve an Itanium RTTI type name from a concrete vtable address point, enumerate that vtable's executable slots, and collect direct/RIP references only for the concrete addresses already reached by local dataflow.

- [ ] **Step 2: Prove adapter -> 16-byte queue item -> queue insertion**

Require the adapter to build a stack pair from one newly created object/control allocation and to call exactly `TProtocolMessageQueue` vslot `+0x68`. Require the queue insertion FDE to copy exactly 16 bytes from the incoming pair into its queue storage and advance the queue end by `0x10`. If either local pattern is absent, emit `SOURCE_BLOCKER` without broader search.

- [ ] **Step 3: Classify the concrete queued object's vtable**

Derive the object vtable address from the adapter's actual RIP-relative `lea` that is stored into the queued object, then decode its RTTI and executable vslots. Do not infer class identity from address adjacency.

- [ ] **Step 4: Prove or reject one queue-drain transition**

Inspect only current `TProtocolMessageQueue` executable vslots and their concrete bounded callers for the method that reads the same queue storage and consumes the 16-byte item. Preserve pointer/control identity through local register/stack/member dataflow. If no unique drain exists, terminate with:

```text
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=queued 16-byte sendLogin item -> unique TProtocolMessageQueue drain/consumer
```

- [ ] **Step 5: Follow only a uniquely reached writer object**

If the drain uniquely invokes a queued-object virtual method or forwards its payload to a concrete writer, resolve that object's RTTI/vslot and follow exactly that edge. Compare the reached path to current `TGameserverNetworkPacketProcessor +0x68` and final frame FDE only when the object/buffer identity reaches them. Stop at the first non-unique edge rather than searching other socket writers.

- [ ] **Step 6: Cross-check the final identity**

A positive contract requires a second independent static check from the reached node: concrete vtable ownership, unique direct caller, or concrete writer member ownership. Generic symbol presence is insufficient.

- [ ] **Step 7: Verify GREEN contract**

Run the repository-only test. Expected: `BE4F48_FINAL_LOGIN_WRITER_CONTRACT=PASS` and `py_compile` succeeds without client access.

---

### Task 3: Exact-current evidence and closeout

**Files:**
- Create: `docs/agents/evidence/OTC-20260903-be4f48-final-login-writer/result.json`
- Create: `docs/agents/evidence/OTC-20260903-be4f48-final-login-writer/20260903-source-result.md`
- Modify: `docs/agents/tasks/active/OTC-20260903-be4f48-final-login-writer.md`

**Interfaces:**
- Consumes: exact-current analyzer artifact from the hosted workflow.
- Produces: durable sanitized source result suitable for a separate clean coordinator promotion, never a Track B mutation.

- [ ] **Step 1: Run exactly once against the live current package**

The workflow must prove the public package still resolves to the exact fence before materialization. If it moved, record `SOURCE_BLOCKER` with the new public fence and do not run stale-address analysis.

- [ ] **Step 2: Inspect sanitized result and allow at most one evidence-derived correction**

If one concrete assumption is falsified, make one smallest correction justified by the emitted local structural evidence and rerun. Do not add a second architecture or broaden discovery.

- [ ] **Step 3: Persist primary evidence**

Copy only sanitized result fields plus run/job/artifact IDs and artifact/result hashes into the evidence directory. Preserve all unsupported fields as `UNKNOWN`.

- [ ] **Step 4: Independent audit**

Freshly inspect the exact branch diff, result artifact, fence, safety markers, object/buffer chain, and PR #284 unchanged state. Material ambiguity prevents a positive writer claim.

- [ ] **Step 5: Exact-head validation**

Require focused contract/`py_compile`, task-specific hosted static job, repository governance/CI applicable to the changed paths, and whitespace/diff validation. E2E is `NOT_APPLICABLE` because source-only safety forbids it.

- [ ] **Step 6: Terminalize accurately**

If the full unique path is proven, set `terminal_result=FINAL_WRITER_CONTRACT_PROVEN`; otherwise set `terminal_result=SOURCE_BLOCKER` and name the exact first missing ownership/dataflow edge. In either case, do not modify #284; hand the durable source result to a later clean coordinator promotion.