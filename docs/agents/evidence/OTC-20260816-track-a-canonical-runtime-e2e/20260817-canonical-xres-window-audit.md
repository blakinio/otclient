# Canonical XRes window integration — exact-diff audit

Audited implementation head before this audit-only commit: `7c5df8701eb496db8f3ec8b0d20f0483281f7fef`.

## Scope checked

- raw X11/XRes owner resolver;
- retained #457 client-base/PID semantics;
- ambiguity and malformed-reply failure behavior;
- exact-anchor canonical worker adapter;
- generated-worker contract and legacy-selector removal;
- hosted-only workflow boundary;
- active canonical task checkpoint and evidence scope.

## Finding CAN-XRES-AUD-001 — RESOLVED

**Severity:** material before correction.

The first resolver implementation duplicated the LocalClientPid extraction rules instead of exactly preserving the corrected #461 fail-closed contract. In that duplicate check, returned client identifier `0` was not rejected even though the trusted persistent helper rejects it.

Resolution on head `7c5df8701eb496db8f3ec8b0d20f0483281f7fef`:

- returned XRes client identifier must be `1..0xffffffff`;
- zero remains rejected;
- regression `test_rejects_zero_returned_client_identifier` was added;
- retained #457 `0x00c00000 -> PID 13648` fixture remains accepted;
- wrong mask, wrong value shape, zero PID, multi-record and multiple-owned-candidate cases remain fail-closed.

## Validation observed for audited head

- dedicated workflow: run `32018178947`, job `95352026968`, `SUCCESS`;
- deterministic XRes ownership tests: `SUCCESS`;
- generated current canonical worker validation and `bash -n`: `SUCCESS`;
- existing canonical transition regression coverage: `SUCCESS`;
- hosted-only boundary check: `SUCCESS`;
- promoted raw-XRes helper workflow: run `32018178733`, `SUCCESS`;
- Track A runtime governance: run `32018178735`, `SUCCESS`.

Repository-wide CI was still executing when this audit record was written and remains a merge gate on the final PR head.

## Audit result

`PASS_WITH_FINDING_RESOLVED`

Material findings open after correction: `0`.

No physical runtime claim is made by this audit. The integration still requires promotion to trusted main before any fresh physical P0 admission.
