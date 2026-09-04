# Whole-diff self-falsification

Task: `OTC-20260904-be4f48-sendlogin-receiver-field-88-use-semantics`
Draft PR: #899
Audited pre-audit head: `bb3f61b5739100578699cfa589e05990fb944261`
Audit class: self-falsification (`audit_independent=false`)
Result: `SELF_FALSIFICATION_PASS`
Material findings open: `0`

## Diff scope reviewed

All six changed paths present on the audited head were reviewed:

1. `.github/workflows/tibia-official-client-re-be4f48-sendlogin-receiver-field-88-use-semantics.yml`
2. `tools/tibia_re_be4f48_sendlogin_receiver_field_88_use_semantics/receiver_field_use_semantics.py`
3. `tools/tibia_re_be4f48_sendlogin_receiver_field_88_use_semantics/test_contract.py`
4. `docs/agents/tasks/active/OTC-20260904-be4f48-sendlogin-receiver-field-88-use-semantics.md`
5. `docs/agents/evidence/OTC-20260904-be4f48-sendlogin-receiver-field-88-use-semantics/result.json`
6. `docs/agents/evidence/OTC-20260904-be4f48-sendlogin-receiver-field-88-use-semantics/source-qualification.md`

## Falsification checks

- Exact fence is consistent across analyzer, workflow, task record, and sanitized result: `15.32.be4f48`, size `52105824`, SHA-256 `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`.
- The analysis starts from the promoted `QObject::connectImpl@0x7c6b9f` connection and exact receiver provenance `OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]`; it does not redo #884 caller discovery, #889 owner-FDE type analysis, or #894 callee identity analysis.
- Immediate-use proof is bounded and stack-aware. The exact field load at `0x7c6b18` reaches formal receiver register `rcx` at `QObject::connectImpl@0x7c6b9f`; hidden sret handling is bounded by the matching `QMetaObject::Connection` destructor path.
- The previously falsified generic ABI-register admission mode is absent. Direct object-tied call candidates require the exact receiver value as `this` in `rdi`; `for reg in ARG_REGS` is contract-forbidden.
- On the accepted repaired source run, the exact field-value lifetime contains zero admitted object-tied call/primary-vptr candidates before the selected connect call. The analyzer stops fail-closed at `NO_UNIQUE_OBJECT_TIED_TYPE_EDGE_IN_EXACT_FIELD_VALUE_LIFETIME`; it does not widen into global `+0x88`, RTTI, QMeta, QObject, vtable, owner, caller, queue/QSlot, or writer census.
- The first implemented source run was not silently accepted: its false `operator new(unsigned long)@0x7c6b5e` candidate is documented as scientifically rejected, followed by a repository-only regression RED and minimal repair.
- Workflow ordering preserves TDD and safety: repository-only contract validation precedes WARP/package/client materialization. Exact client bytes are static-analysis-only, deleted by both trap and explicit removal before the sanitized artifact upload; accepted run logs state `RAW_CLIENT_RETAINED=false`.
- No official-client execution, login, credentials/session/cookie/character/world access, process-memory access, packet capture, OCR/Vision, official-service E2E, runtime Field6 observation, or Track B PR #284 mutation is present.
- Changed paths remain confined to this source lane; no queue successor path or Track B path is touched.
- The scientific claim is not overstated: receiver field **use** is proven, receiver **identity** is `UNKNOWN`, complete sender/receiver pair is false, causal binding remains false, pre-success sequence and Field6 remain `UNKNOWN`.
- PR lifecycle remains source-only and Draft. No self-merge or promotion authority is claimed; independent lifecycle review belongs to the clean coordinator.

## Outcome

No material contradiction, scope escape, safety violation, stale rejected result, or unsupported identity/causality claim remains in the reviewed diff. One wording-only metadata cleanup is applied together with this audit record: `0x7c6b18` is labeled `receiver_field_load_site` rather than `receiver_field_definition_site`, avoiding a stronger claim than the evidence supports.

The audit record itself and that wording-only task update must be covered by the final exact-head qualification before coordinator consumption.
