# OTC-BE4F48 sendLogin receiver field owner — whole-diff falsification

Audit class: `fresh_self_falsification`.
Independent closeout audit: deferred to the clean coordinator promotion; this source worker does not represent its own audit as independent.

## Scope checked

Current PR #884 changed paths are exactly:

1. `.github/workflows/tibia-official-client-re-be4f48-sendlogin-receiver-field-owner.yml`
2. `docs/agents/evidence/OTC-20260904-be4f48-sendlogin-receiver-field-owner/20260904-source-result.md`
3. `docs/agents/evidence/OTC-20260904-be4f48-sendlogin-receiver-field-owner/result.json`
4. `docs/agents/tasks/active/OTC-20260904-be4f48-sendlogin-receiver-field-owner.md`
5. `tools/tibia_re_be4f48_sendlogin_receiver_field_owner/receiver_field_owner.py`
6. `tools/tibia_re_be4f48_sendlogin_receiver_field_owner/test_contract.py`

No Track B file is changed.

## Falsification checks

- The TDD RED was a real first-step failure caused by the absent production analyzer and occurred before WARP or exact-client materialization.
- The exact-current source run subsequently fenced version, size and SHA-256 before analysis and deleted transient raw client bytes before artifact upload.
- The analyzer's direct-caller search is target-specific: it scans executable sections for `E8 rel32` candidates targeting exactly `0x7c6700`, then accepts only candidates whose decoded instruction is an exact direct `call` to that target in a unique containing FDE.
- The current exact result contains zero accepted direct caller candidates. The code therefore exits the bounded owner chain before any field-store, constructor or RTTI identity can be claimed.
- The positive identity path is not evidence for this result and was not used. Its existence does not upgrade the current `UNKNOWN` receiver identity or sender/receiver causality.
- The workflow uploads only sanitized `result.json`; no raw client or package is retained as an artifact.
- The terminal report preserves `PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN`, `FIELD6_VALUE=UNKNOWN`, `TRACK_B_PR_284_MODIFIED=false` and all no-runtime/no-login safety facts.
- PR #884 had zero submitted reviews and zero review threads at this falsification pass.

## Result

```text
SELF_FALSIFICATION=PASS
MATERIAL_FINDINGS_OPEN=0
SCIENTIFIC_RESULT=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=CONNECTION_OWNER_FDE_DIRECT_CALLER_NOT_UNIQUE
INDEPENDENT_CLOSEOUT_AUDIT=DEFERRED_TO_CLEAN_COORDINATOR_PROMOTION
```

The source result is ready for exact-head qualification and clean coordinator consumption. No broader constructor/RTTI/QMeta/QObject/`+0x88` census is justified inside this task.
