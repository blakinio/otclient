# BE4F48 sendLogin peer metaowner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve the exact-current `0x30b68a0` Qt metaobject owner and, only if uniquely proven in the already bounded `0x7c6700..0x7cc933` construction neighborhood, the real Qt connection primitive, sender/receiver direction, and causal binding to the `sendLogin` adapter.

**Architecture:** Add one isolated GitHub-hosted static-analysis lane. A repository-only contract runs first and must be observed RED before the analyzer exists; after GREEN, the workflow transiently materializes the exact public Linux client, validates its version/size/SHA, runs one bounded ELF/Qt analyzer, prints and uploads only sanitized JSON, then deletes client bytes. The analyzer decodes only the exact static `QMetaObject` anchor and the local adapter-reference neighborhood; it never performs global Qt/RTTI/callgraph discovery.

**Tech Stack:** Python 3, `pyelftools`, Capstone, `c++filt`, GitHub Actions Ubuntu 24.04, public Tibia launcher package through the existing WARP retrieval pattern.

**Spec:** `docs/agents/prompts/OTC_BE4F48_SENDLOGIN_PEER_METAOWNER.md`

## Global Constraints

- Exact client: `15.32.be4f48`, size `52105824`, SHA-256 `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`.
- `runtime_access: none`; no official-client execution, login, credentials, process memory, packet capture, OCR/Vision or official-service E2E.
- Never treat `0x4d8670` as a connection primitive; it is `operator new(unsigned long)`.
- Do not edit Track B PR #284 or its paths.
- No broad Qt census, global RTTI sweep, broad BFS/callgraph or generic writer/socket search.
- Raw client bytes are transient runner inputs only and must be deleted before artifact upload.
- Positive sender/receiver direction requires the exact Qt primitive/call contract plus uniquely traced object/function dataflow; adjacency or register position without a proven contract is insufficient.

---

### Task 1: Establish repository-only RED

**Files:**
- Create: `tools/tibia_re_be4f48_sendlogin_peer_metaowner/test_contract.py`
- Create: `.github/workflows/tibia-official-client-re-be4f48-sendlogin-peer-metaowner.yml`
- Modify: `docs/agents/tasks/active/OTC-20260903-be4f48-sendlogin-peer-metaowner.md`

**Interfaces:**
- Consumes: exact task constants from the registered prompt.
- Produces: a repository-only gate that fails by assertion while `peer_metaowner.py` is absent, before package metadata or client bytes are fetched.

- [ ] **Step 1: Write the failing repository contract**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "peer_metaowner.py"


def main() -> None:
    assert TARGET.exists(), "peer_metaowner.py must exist"
    text = TARGET.read_text(encoding="utf-8")
    for token in (
        'EXPECTED_VERSION = "15.32.be4f48"',
        "EXPECTED_SIZE = 52105824",
        'EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"',
        "METAOBJECT_ANCHOR = 0x30B68A0",
        "SIGNAL_INDEX = 0",
        "PEER_TARGET = 0xD052A0",
        "ADAPTER_TARGET = 0xBD3050",
        "ADAPTER_REFERENCE_SITE = 0x7C6B34",
        "CONNECTION_OWNER_FDE = (0x7C6700, 0x7CC933)",
        '"runtime_access": "none"',
        '"track_b_pr_284_modified": False',
    ):
        assert token in text, f"missing contract token: {token}"
    print("BE4F48_SENDLOGIN_PEER_METAOWNER_REPOSITORY_CONTRACT=PASS")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Configure the workflow so the contract runs before any network/client materialization**

The first executable step after checkout must run:

```bash
python3 tools/tibia_re_be4f48_sendlogin_peer_metaowner/test_contract.py
python3 -m py_compile tools/tibia_re_be4f48_sendlogin_peer_metaowner/test_contract.py
```

Every exact-client download/decompression/analyzer step must follow that gate under normal `set -Eeuo pipefail` failure propagation.

- [ ] **Step 3: Open a Draft PR and verify RED**

Expected first workflow result: `FAIL` at `peer_metaowner.py must exist`; all client materialization steps are `SKIPPED`.

- [ ] **Step 4: Persist the RED run/job/head IDs in the task checkpoint**

Commit the task update before the GREEN implementation so the TDD ordering is durable.

### Task 2: Implement the smallest bounded analyzer

**Files:**
- Create: `tools/tibia_re_be4f48_sendlogin_peer_metaowner/peer_metaowner.py`
- Modify: `.github/workflows/tibia-official-client-re-be4f48-sendlogin-peer-metaowner.yml` only if the exact evidence format needs a bounded correction.

**Interfaces:**
- Consumes: exact client path and the constants above.
- Produces: one deterministic JSON document containing exact-client fence, static-metaobject decode, signal-index-0 raw binding, local connection-call census, any proven Qt primitive, endpoint/function dataflow, terminal result, and first missing boundary.

- [ ] **Step 1: Add exact-fence and ELF helpers**

Implement `Image` helpers for mapped section reads, RELA addends/symbols, DWARF FDE lookup and Capstone disassembly. Fail before analysis unless file size and SHA-256 exactly match the fence.

- [ ] **Step 2: Decode only `0x30b68a0`**

Read the fixed QMetaObject pointer-sized fields, validate candidate metadata using a bounded moc-header shape, and recover a class/owner only when its string-table relation is internally consistent and unique. Preserve raw numeric fields when a semantic name cannot be proven.

- [ ] **Step 3: Bind signal index 0 without inventing a name**

Require a validated signal count that includes index `0`; expose the corresponding method/string indices when decoded. If metadata cannot uniquely name the signal, record `UNKNOWN` rather than synthesizing a name.

- [ ] **Step 4: Inspect only the existing local construction neighborhood**

Disassemble `0x7c6700..0x7cc933`, anchor the unique adapter reference at `0x7c6b34`, restrict connection candidate analysis to a small instruction window around that site, and resolve direct PLT calls through GOT relocation symbols before assigning semantics.

- [ ] **Step 5: Prove direction only through exact Qt call contract + dataflow**

For a unique demangled Qt connection primitive, backward-slice only its ABI arguments in the local window. Record sender/receiver identities and peer/adapter function identities only when their definitions are unique; otherwise emit `UNKNOWN` and the exact unresolved argument/dataflow edge.

- [ ] **Step 6: Return fail-closed terminal classification**

```python
if all_positive_gates:
    terminal_result = "SENDLOGIN_PEER_METAOWNER_AND_DIRECTION_PROVEN"
else:
    terminal_result = "SOURCE_BLOCKER"
```

No positive field may be inferred solely from adjacency, allocation, generic QObject presence or an unresolved PLT target.

- [ ] **Step 7: Run repository contract GREEN**

Run in Actions before exact-client materialization. Expected: `BE4F48_SENDLOGIN_PEER_METAOWNER_REPOSITORY_CONTRACT=PASS`.

### Task 3: Run exact-current static evidence and bounded repair if needed

**Files:**
- Create: `docs/agents/evidence/OTC-20260903-be4f48-sendlogin-peer-metaowner/result.json`
- Create: `docs/agents/evidence/OTC-20260903-be4f48-sendlogin-peer-metaowner/20260903-source-result.md`
- Modify: `docs/agents/tasks/active/OTC-20260903-be4f48-sendlogin-peer-metaowner.md`

**Interfaces:**
- Consumes: sanitized workflow result from the exact fenced client.
- Produces: repository evidence sufficient for a clean coordinator promotion without raw binaries or hidden chat context.

- [ ] **Step 1: Execute the exact-client workflow**

The workflow must fetch manifest/package only after GREEN, verify exact version/packed/unpacked sizes and SHA, decompress transiently, run the analyzer, delete raw bytes, validate sanitized booleans, print JSON, and upload only JSON.

- [ ] **Step 2: Inspect the first exact result**

If it identifies a precise missing edge inside the allowed static-metaobject/local-connection boundary, make at most an evidence-derived bounded analyzer repair. Do not broaden to global discovery.

- [ ] **Step 3: Independently falsify any positive owner/direction claim**

Cross-check the positive owner against separate metadata/string consistency and the connection direction against the exact demangled primitive signature plus independent local argument/function provenance. Any contradiction downgrades the affected field to `UNKNOWN`/`SOURCE_BLOCKER`.

- [ ] **Step 4: Persist sanitized evidence**

The committed `result.json` must contain no raw client bytes, credentials, process/runtime data or proprietary extracts beyond bounded addresses/metadata facts needed for the research conclusion.

### Task 4: Validate and close the source lane

**Files:**
- Modify: `docs/agents/tasks/active/OTC-20260903-be4f48-sendlogin-peer-metaowner.md`
- Modify: `docs/agents/evidence/OTC-20260903-be4f48-sendlogin-peer-metaowner/20260903-source-result.md`

**Interfaces:**
- Consumes: final branch diff, exact-head Actions results and evidence.
- Produces: terminal source result consumable by a clean coordinator; no Track B mutation.

- [ ] **Step 1: Inspect complete changed-file list and diff**

Require every changed path to be inside the declared ownership list and confirm PR #874/Track B paths are untouched.

- [ ] **Step 2: Perform fresh audit**

Use a fresh validator role to check scope, exact fence, TDD ordering, fail-closed classifications, absence of forbidden broad discovery, secret/binary hygiene and consistency between JSON/report/task.

- [ ] **Step 3: Record E2E as NOT_APPLICABLE**

Reason: static source discriminator explicitly forbids official-client execution/login/runtime observation; exact-current hosted static analysis is the required real system boundary for this task.

- [ ] **Step 4: Verify exact-head CI**

Require the focused discriminator workflow plus repository-emitted Track A governance/self-hosted-boundary/CI checks applicable to the final exact head.

- [ ] **Step 5: Persist one terminal outcome**

Use only `SENDLOGIN_PEER_METAOWNER_AND_DIRECTION_PROVEN` or `SOURCE_BLOCKER`, keep the source PR Draft for clean coordinator consumption unless current repository governance explicitly requires another terminal lifecycle, and leave exactly one coordinator `next_action`.
