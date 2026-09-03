# be4f48 sendLogin Sender/Peer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove, or fail closed on, the exact-current sender-side peer identity and sender/receiver direction for the native connection that binds `TProtocolMessageQueue::sendLogin`.

**Architecture:** Use one focused Python static analyzer over the exact fenced Linux ELF. Start from the promoted peer/helper/adapter anchors, recover only the peer FDE, local RTTI/vtable ownership, bounded xrefs, and the single connection-call dataflow. Persist only sanitized JSON. A second implementation change is allowed only when the first exact-client result yields one concrete falsifiable direction hypothesis.

**Tech Stack:** Python 3, `pyelftools`, `capstone`, GNU `c++filt`/binutils on GitHub-hosted Ubuntu 24.04, GitHub Actions.

**Spec:** `docs/agents/prompts/OTC_BE4F48_SENDLOGIN_SENDER_PEER.md`

## Global Constraints

- Exact client: `version=15.32.be4f48`, `size=52105824`, `sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`.
- Promoted peer target: `0xd052a0`; helper target: `0x4d8670`; sendLogin adapter: `0xbd3050`.
- `runtime_access=none`; no official-client execution, login, credentials, process memory, packet capture, OCR/Vision, official-service E2E, or raw-client artifact upload.
- Do not modify Track B PR #284 or investigate the independent final-writer boundary.
- Do not expand into a global BFS/crawler. Search breadth is bounded to the peer FDE, pointer-table memberships, constructor/vtable xrefs, direct callers of the peer, the promoted connection owner FDE, and the helper FDE.
- Scientific `UNKNOWN` is an accepted terminal result.

---

### Task 1: Repository-only RED contract

**Files:**
- Create: `tools/tibia_re_be4f48_sendlogin_sender_peer/test_contract.py`
- Create: `.github/workflows/tibia-official-client-re-be4f48-sendlogin-sender-peer.yml`
- Modify: `docs/agents/tasks/active/OTC-20260903-be4f48-sendlogin-sender-peer.md`

**Interfaces:**
- Consumes: repository paths only; no client bytes.
- Produces: a failing assertion `peer_owner.py is missing` before package materialization.

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ANALYZER = ROOT / "peer_owner.py"


def test_peer_owner_analyzer_exists() -> None:
    assert ANALYZER.is_file(), "peer_owner.py is missing: expected RED before client materialization"


if __name__ == "__main__":
    test_peer_owner_analyzer_exists()
    print("BE4F48_SENDLOGIN_SENDER_PEER_CONTRACT=PASS")
```

- [ ] **Step 2: Add a PR workflow whose first executable check is the RED test**

The workflow must run `python3 tools/tibia_re_be4f48_sendlogin_sender_peer/test_contract.py` before installing analysis dependencies or downloading `package.json`/client bytes. Later steps may be present but must be unreachable while RED fails.

- [ ] **Step 3: Open the Draft PR and verify RED**

Expected exact-head workflow result: FAIL in the repository-only contract step with `peer_owner.py is missing`; no `Prepare exact public client package` step may execute.

- [ ] **Step 4: Record the run/job identity in the task**

Commit only the task checkpoint after the RED evidence is known.

---

### Task 2: Minimal GREEN peer-owner discriminator

**Files:**
- Create: `tools/tibia_re_be4f48_sendlogin_sender_peer/peer_owner.py`
- Modify: `tools/tibia_re_be4f48_sendlogin_sender_peer/test_contract.py`
- Modify: `.github/workflows/tibia-official-client-re-be4f48-sendlogin-sender-peer.yml`

**Interfaces:**
- Consumes: exact ELF path plus promoted constants.
- Produces: `artifacts/be4f48-sendlogin-sender-peer/result.json` with exact-fence, peer FDE, tail transfer, pointer-table/vtable memberships, RTTI class names, constructor/vtable xrefs, bounded peer callers, connection owner/callsite argument provenance, helper FDE/direct calls, and fail-closed owner/direction classifications.

- [ ] **Step 1: Extend tests before production code**

After the existence test, load `peer_owner.py` and require these pure helpers:

```python
assert mod.hx(0xD052A0) == "0xd052a0"
assert mod.signed64(0xFFFFFFFFFFFFFFFF) == -1
assert mod.signed64(0x10) == 0x10
assert mod.is_plausible_offset_to_top(0)
assert mod.is_plausible_offset_to_top(-0x20)
assert not mod.is_plausible_offset_to_top(0x100000)
```

The test must also inspect module constants and fail unless they equal the exact promoted fence/targets.

- [ ] **Step 2: Verify the new RED**

Run the repository-only contract. Expected failure: module/function/constants missing because `peer_owner.py` has not yet been created.

- [ ] **Step 3: Implement the exact-fenced ELF image helper**

`peer_owner.py` must define:

```python
EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
PEER_TARGET = 0xD052A0
HELPER_TARGET = 0x4D8670
ADAPTER_TARGET = 0xBD3050
CONNECTION_OWNER_FDE = (0x7C6700, 0x7CC933)
```

Implement an `Image` wrapper using ELF sections, relocations, `.eh_frame` FDEs and Capstone. Required methods: `va_to_off`, `off_to_va`, `mapped`, `executable`, `bytes`, `u64`, `qword`, `fde`, `instructions`, and iteration over relocations/sections.

- [ ] **Step 4: Recover peer FDE and local callable shape**

For `PEER_TARGET`, require exactly one containing FDE. Disassemble only that FDE. Record:

```text
peer_fde=[start,end]
peer_instruction_count=<n>
peer_first_unconditional_tail_target=<target or UNKNOWN>
peer_direct_call_targets=[...]
```

Do not infer role from address proximity.

- [ ] **Step 5: Recover only pointer-table/vtable memberships for the peer**

Search mapped non-executable sections for relocated or literal qwords equal to `PEER_TARGET` and, separately, the single tail target if one exists. For each pointer slot scan backward at most `0x200` bytes in 8-byte increments for an Itanium vtable header candidate:

```text
[offset_to_top][typeinfo_ptr][address-point entries...]
```

Accept a header only when offset-to-top is a small signed value, `typeinfo_ptr` is mapped non-executable data, and `typeinfo_ptr+8` resolves to a NUL-terminated Itanium type-name string. Demangle only with `c++filt`; retain the mangled name as the primary deterministic identity.

Deduplicate memberships by `(address_point, typeinfo_ptr, mangled_name, slot_offset)`.

- [ ] **Step 6: Independently cross-check class ownership with constructor/vtable xrefs**

For every unique accepted address point, search executable sections for instruction-aligned RIP-relative references to that address point. Keep only refs whose containing FDE is unique. Record at most 32 bounded xrefs with site/FDE and whether the reference is followed within eight instructions by a store of the referenced pointer through a register into memory. This is the independent construction/ownership cross-check; it is not a global call-graph traversal.

- [ ] **Step 7: Recover bounded peer callers**

Search executable instructions only for direct `call`/`jmp` immediates equal to `PEER_TARGET` or its unique tail target. Deduplicate by caller FDE and record at most 32 entries. Do not recurse.

- [ ] **Step 8: Recover connection callsite argument provenance**

Disassemble only promoted `CONNECTION_OWNER_FDE`. Locate exactly one instruction-aligned RIP reference to `ADAPTER_TARGET`, then locate the following direct call to `HELPER_TARGET` within 32 instructions. For the window from 40 instructions before the adapter reference through that helper call, record only instructions that:

- materialize `ADAPTER_TARGET` or `PEER_TARGET` via RIP-relative `lea`;
- load an object member into a register;
- move registers into SysV argument registers `rdi,rsi,rdx,rcx,r8,r9`;
- store registers to `[rsp+disp]`;
- perform the helper call.

The analyzer must backward-slice register provenance without crossing the bounded window and classify each helper argument as one of `ADAPTER_FUNCTION`, `PEER_FUNCTION`, `OBJECT_FIELD:<base><disp>`, `STACK_TEMP`, `CONSTANT`, or `UNKNOWN`.

- [ ] **Step 9: Inspect the helper FDE only**

Find the FDE containing `HELPER_TARGET`; record direct calls and direct tail jumps. Resolve dynamic symbols when an exact target maps to a symbol/PLT relocation; otherwise retain address only. No recursive traversal is allowed.

- [ ] **Step 10: Fail-closed owner/direction classification**

Set `peer_owner_identity` only if exactly one peer/tail vtable membership resolves to one mangled/demangled class and at least one independent constructor/vtable xref agrees. Otherwise use `UNKNOWN`.

Set `sender_endpoint_identity`, `receiver_endpoint_identity`, and `sendlogin_causal_binding_proven` to `UNKNOWN/false` on this first implementation unless exact helper symbol + argument positions establish a documented Qt sender/signal/receiver/slot contract without guessing. The first run is allowed to stop at that boundary.

- [ ] **Step 11: Verify GREEN repository tests**

Expected: `BE4F48_SENDLOGIN_SENDER_PEER_CONTRACT=PASS` before materialization.

- [ ] **Step 12: Run once on the exact client**

The workflow must:

1. install `python3-capstone python3-pyelftools binutils`;
2. establish the same WARP-only public package path used by the accepted #865 static workflow;
3. fetch `package.json` and fail closed unless exact version/hash/size match;
4. materialize the client transiently;
5. run `peer_owner.py --client ... --output artifacts/be4f48-sendlogin-sender-peer/result.json`;
6. delete raw/packed client bytes before artifact upload;
7. validate `runtime_access=none`, exact SHA, `raw_client_uploaded=false`;
8. upload only the sanitized JSON for three days.

---

### Task 3: One evidence-derived direction discriminator or SOURCE_BLOCKER

**Files:**
- Modify only if justified: `tools/tibia_re_be4f48_sendlogin_sender_peer/peer_owner.py`
- Modify only if justified: `tools/tibia_re_be4f48_sendlogin_sender_peer/test_contract.py`
- Modify: `docs/agents/tasks/active/OTC-20260903-be4f48-sendlogin-sender-peer.md`

**Interfaces:**
- Consumes: the exact sanitized Task 2 result.
- Produces: either one falsifiable static direction rule or a terminal first missing boundary.

- [ ] **Step 1: Inspect the exact Task 2 artifact**

Accept a follow-up only if the artifact supplies both a unique peer owner and a concrete helper/callsite fact that maps the function/object arguments to a known connect contract. Otherwise set:

```text
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=exact first peer ownership or helper argument-direction edge absent from the artifact
```

- [ ] **Step 2: If justified, write the direction RED first**

Add one pure test asserting the exact callsite-shape invariant derived from Task 2 (for example, a helper argument-position classifier). Verify it fails before changing production code.

- [ ] **Step 3: Implement only that direction rule**

No new search class is permitted. Reuse only already emitted peer owner, helper symbol, callsite argument provenance and Qt contract positions.

- [ ] **Step 4: Run exact client once more only if production logic changed**

Require the same exact fence and sanitized artifact contract.

---

### Task 4: Persist terminal evidence and validate exact head

**Files:**
- Create: `docs/agents/evidence/OTC-20260903-be4f48-sendlogin-sender-peer/result.json`
- Create: `docs/agents/evidence/OTC-20260903-be4f48-sendlogin-sender-peer/20260903-source-result.md`
- Modify: `docs/agents/tasks/active/OTC-20260903-be4f48-sendlogin-sender-peer.md`

**Interfaces:**
- Consumes: exact workflow artifact and run identities.
- Produces: repository-owned sanitized source evidence suitable for a separate clean coordinator promotion.

- [ ] **Step 1: Persist only sanitized structural fields and exact run/artifact identities**

Required terminal fields:

```text
trusted_main
source_head
current_client_version
current_client_sha256
peer_target
peer_owner_identity
peer_role
sender_endpoint_identity
receiver_endpoint_identity
sendlogin_causal_binding_proven
pre_login_sequence_advanced
runtime_access=none
official_service_e2e_count=0
track_b_pr_284_modified=false
terminal_result
FIRST_MISSING_BOUNDARY
next_action
```

- [ ] **Step 2: Run exact-head checks**

Require focused workflow success, repository CI/governance success, full changed-file review, and `git diff --check` from CI. If a required environment/check cannot run, record it exactly and do not claim completion.

- [ ] **Step 3: Keep PR Draft unless the repository merge gate is fully satisfied**

A positive result still does not authorize #284 mutation. Handoff is to a clean coordinator promotion that combines this lane with the independent final-writer lane.