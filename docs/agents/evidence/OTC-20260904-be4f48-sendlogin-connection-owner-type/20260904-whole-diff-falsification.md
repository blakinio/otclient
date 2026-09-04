# Whole-diff falsification — sendLogin connection owner type

Date: 2026-09-04
Task: `OTC-20260904-be4f48-sendlogin-connection-owner-type`
PR: #889
Base: `e94e6c5764851f9cb62691d90c55f42e9c6253a1`
Audited head: `acbf446a5a883741711aa5fcdc0f3d1d91f6d93e`
Audit mode: fresh self-falsification; `audit_independent=false`

## Diff boundary

PR #889 contains six changed files at the audited head. Every changed path is inside the task's declared ownership:

```text
.github/workflows/tibia-official-client-re-be4f48-sendlogin-connection-owner-type.yml
tools/tibia_re_be4f48_sendlogin_connection_owner_type/test_contract.py
tools/tibia_re_be4f48_sendlogin_connection_owner_type/owner_type.py
docs/agents/tasks/active/OTC-20260904-be4f48-sendlogin-connection-owner-type.md
docs/agents/evidence/OTC-20260904-be4f48-sendlogin-connection-owner-type/20260904-source-result.md
docs/agents/evidence/OTC-20260904-be4f48-sendlogin-connection-owner-type/result.json
```

No Track B source or PR #284 path is changed.

## Falsification checks

### 1. Bounded-search violation

Attempted falsification: determine whether the implementation reintroduces the consumed #884 target-wide caller scan, opens a global constructor/RTTI/QMeta/QObject/vtable/`+0x88` census, or follows more than one adjacent identity edge.

Result: not falsified.

- The analyzer starts by disassembling only `0x7c6700..0x7cc933`.
- In-FDE identity recovery is tied exactly to `ENTRY_ARG:rdi`.
- If no in-FDE type is proven, the analyzer only identifies direct calls already inside that FDE whose `rdi` backward-slices to the same entry object.
- It follows a callee only when that set has cardinality exactly one. The exact-current result had one such edge, `0x7c67b8 -> 0x7e8f30`, and only that edge was followed.
- The repository contract explicitly rejects the consumed #884 caller-scan helper from the new analyzer.

### 2. Type overclaim

Attempted falsification: determine whether string proximity, QObject-like shape, historical layout, generic vtable resemblance or a non-unique RTTI result is converted into a positive class claim.

Result: not falsified.

No typed vptr/RTTI event was bound to `ENTRY_ARG:rdi` in the owner FDE. The single admitted edge also failed to prove one exact type. The output therefore remains:

```text
CONNECTION_OWNER_IDENTITY=UNKNOWN
CONNECTION_OWNER_IDENTITY_PROVEN=false
SENDLOGIN_RECEIVER_IDENTITY=UNKNOWN
SENDLOGIN_RECEIVER_IDENTITY_PROVEN=false
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=UNIQUE_ENTRY_OBJECT_EDGE_TYPE_NOT_PROVEN
```

The analyzer does not attempt receiver typing after owner identity fails.

### 3. Exact-current fence failure

Attempted falsification: determine whether analysis can run on a stale or mismatched client.

Result: not falsified.

The workflow guards manifest version, unpacked SHA-256 and unpacked size before materialization. The analyzer independently rejects any input whose size or SHA-256 differs from the exact fence:

```text
15.32.be4f48
52105824
552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

### 4. Proprietary-byte retention or execution

Attempted falsification: determine whether the official client is executed or uploaded/retained.

Result: not falsified.

The workflow only reads the transient unpacked ELF with Python static-analysis libraries. It never invokes the client. Cleanup removes both packed and unpacked client files. Source run `33872240794` uploaded artifact `9936389943`, which contains only `result.json`; artifact size is 1097 bytes and digest is `sha256:f4fcfd66b409c31ddaf7b06c471eccd33a638d7ff6cdaeeae9c4f47bef147636`.

### 5. TDD/lifecycle bypass

Attempted falsification: determine whether exact-client materialization occurred before repository-only RED.

Result: not falsified.

RED head `396849b2ce1ae818c3db42ced133f4e1ffca2674`, run `33871893625`, job `101019573417` failed in `Validate repository-only connection owner-type contract`; all WARP/materialization/result steps were skipped. GREEN was added only afterward.

### 6. Required validation bypass

Attempted falsification: determine whether the source claim relies only on analyzer exit status.

Result: not falsified.

On source head `903b7e6c5f9452d9be545d698355bcb151c62aec`:

```text
source workflow 33872240794 = success
job 101020701224 = success
CI 33872241316 = success
Track A agent runtime governance 33872241004 = success
Track A self-hosted PR boundary 33872240809 = success
```

The source workflow itself runs the repository contract, `py_compile` for the test and analyzer, `git diff --check`, exact-fence validation, sanitized-result validation and sanitized-only artifact upload.

## Findings

Material findings open: **0**.

One non-material lifecycle presentation issue was observed: the Draft PR body still described the intentionally RED initial head after the terminal source result existed. It does not affect code or scientific evidence and should be updated before handoff.

## Terminal audit disposition

The diff supports only the fail-closed scientific result `SOURCE_BLOCKER`. It does not support a positive connection-owner type, receiver type, complete sender/receiver pair, sendLogin causal binding, pre-success send order or Field6 value.

After this audit evidence is committed, the resulting exact head still requires a fresh final set of PR checks before terminal handoff to a clean coordinator promotion.
