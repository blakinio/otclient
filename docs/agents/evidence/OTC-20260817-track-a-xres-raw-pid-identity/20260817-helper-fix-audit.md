# Fresh audit — XRes CLIENTIDVALUE length repair

```yaml
task: OTC-20260817-track-a-xres-raw-pid-identity
pr: 455
audit_role: fresh_validator
scope: helper repair plus deterministic tests and v1 evidence/checkpoint
runtime_access: none
client_executed_by_audit: false
material_findings_open: 0
result: PASS
```

## Audit inputs

The validator inspected the current full PR #455 changed-file set rather than relying on the implementer summary. The terminal set at audit time is exactly:

- `.github/scripts/tibia-official-client-re-xres-wire.py`
- `.github/scripts/test_tibia_official_client_re_xres_wire.py`
- `docs/agents/evidence/OTC-20260817-track-a-xres-raw-pid-identity/20260817-v1-physical-parser-discriminator.md`
- `docs/agents/tasks/active/OTC-20260817-track-a-xres-raw-pid-identity.md`

The consumed one-shot v1 runtime workflow and both transform patchers are absent from the final diff.

Primary environment evidence inspected:

```yaml
physical_run: 32013868595
hosted_preflight_job: 95339063640
physical_job: 95339104951
runtime_admission: PASS
exact_client_launch_count: 1
xres_query_version: PASS_1_2
query_client_ids_failure: QueryClientIds client-id value payload is truncated
cleanup: COMPLETE
```

The protocol interpretation was cross-checked against the X.Org XRes 1.2 protocol/server source lineage. `CLIENTIDVALUE` carries a CARD32 `length` describing the value payload size, and the LocalClientPid server response uses `length=4` with one CARD32 PID. The physical failure is exactly predicted by the old helper's erroneous `length * 4` calculation.

## Falsification checks

### AUD-XRES-001 — byte/count unit mismatch repaired

PASS. The parser now names the field `value_length_bytes`, requires CARD32 alignment, derives `value_count = value_length_bytes // 4`, bounds the public count, and advances by the actual byte length.

### AUD-XRES-002 — valid LocalClientPid fixture represents the real wire shape

PASS. The fixture builder writes `len(values) * 4`. The explicit LocalClientPid regression requires `length=4` and a total 48-byte one-record reply. Both little- and big-endian parse/extract tests consume the same corrected fixture convention.

### AUD-XRES-003 — malformed lengths still fail closed

PASS. Existing truncated-payload validation remains. A new test rejects non-CARD32-aligned byte lengths. Reply-size, id-count, value-count, sequence, mask, value-shape, duplicate/extra-record and zero-PID guards remain intact.

### AUD-XRES-004 — no transport/runtime authority leaked into helper

PASS. The helper remains pure byte processing only. The dedicated workflow independently AST-checks imports/names to keep it transport-free. No socket, subprocess, process, display, canonical-state or credential capability was added to the helper.

### AUD-XRES-005 — no false physical conclusion

PASS. V1 evidence preserves `XRES_QUERY_CLIENT_IDS_PID_IDENTITY: NOT_PROVEN`. It does not reinterpret the parser failure as proof of ownership or foreign ownership. The task requires a fresh v2 physical admission only after the corrected helper reaches trusted main.

### AUD-XRES-006 — physical retry boundary preserved

PASS. The v1 task branch no longer contains the one-shot physical workflow or its patchers. The task records one consumed client launch and forbids a second v1 physical retry. This prevents a helper-only correction commit from silently causing another live launch.

## Findings

No critical/high/material-medium findings remain.

One non-blocking observation is retained: the v1 run aborted at the first t05 QueryClientIds parse failure, so it did not reach the later t35 viewable-window discriminator. This is expected and is precisely why XID-to-PID identity remains unproven. The v2 physical retry should preserve raw reply diagnostics and continue safely through early non-viewable resources instead of converting the first non-final resource into a whole-run failure.

## Audit disposition

```yaml
helper_protocol_repair: ACCEPT
v1_evidence_classification: ACCEPT
one_shot_v1_retirement: ACCEPT
xid_to_pid_identity_proven: false
physical_v2_required: true
material_findings_open: 0
audit_result: PASS
```
