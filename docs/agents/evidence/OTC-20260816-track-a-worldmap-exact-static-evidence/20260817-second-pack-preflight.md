# World-map exact-static second-pack preflight

Task: `OTC-20260816-track-a-worldmap-exact-static-evidence`  
Producer PR: `#437`  
Consumer task: `OTC-20260816-track-a-worldmap-extent-static-re`  
Consumer PR: `#367`

This checkpoint is a fresh admission/ownership/uniqueness/drift record for the second bounded exact-client static-evidence package. It does not promote researcher conclusions into canonical programme state and does not modify the consumer branch.

## Fresh repository state

```yaml
checked_at: 2026-08-17T08:31:00+02:00
repository: blakinio/otclient
current_main: 8c9486e2c6109a7a39b564804c8acd707659b5e0
producer_branch: research/OTC-20260816-track-a-worldmap-exact-static-evidence
producer_head_before_second_pack: ce8b1f59d02bfc7ecc498dd80f73b09cf2970510
producer_pr: 437
producer_pr_state: open_draft
consumer_branch: research/OTC-20260816-track-a-worldmap-extent-static-re
consumer_head: a69179e5cf4681a9d41014a562a0bfd0d1cd9ffb
consumer_pr: 367
consumer_pr_state: open_draft
consumer_branch_modified_by_producer: false
```

The producer branch and `main` have diverged from merge base `b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4`. At this preflight, `main` is 14 commits ahead of the merge base and the producer is 5 commits ahead of it. The compared `main` drift is confined to other Track-A evidence/task/programme paths and does not overlap the producer's declared writable paths.

## Ownership / uniqueness

```yaml
producer_task_record_matches_branch: true
producer_task_record_matches_pr: true
producer_owned_paths_match_planned_writes: true
open_duplicate_producer_for_task_id: false
consumer_is_read_only_dependency: true
consumer_branch_owned_by_this_worker: false
consumer_branch_write_authorized: false
ownership_overlap_blocker: false
```

A fresh open-PR search for `OTC-20260816-track-a-worldmap-exact-static-evidence` resolves `#437` as the sole producer Draft PR. `#367` references the producer only as its downstream consumer and remains outside this producer's write ownership.

## Track-A runtime admission

```yaml
track_id: official-client-re
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
execution_class: github_hosted
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
owner_funded_ai_api_authorized: false
```

The existing task-scoped source-staging exception remains bounded to a read-only exact-file read on `synology-otclient-01`; it does not authorize process/runtime/session/X11/VNC/network/gameplay access and does not authorize raw-client upload or client-byte mutation. Disassembly and evidence processing remain GitHub-hosted and operate only on bounded sanitized byte windows.

Historical runtime facts are not current authority:

```yaml
display_98_current_canonical_status: UNKNOWN
rfb_6082_current_backend_mapping: UNKNOWN
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
```

## Exact-client fence

The second package must freshly verify the source file against exactly:

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

A mismatch fails closed. No historical PID/session/display is needed or inspected for this static package.

## Non-duplication boundary

The first package already proved the exact identities and Storage geometry summarized in PR #437. The second package must not repeat the exhausted identity-window study. It is limited to materially new discriminators:

1. Storage slot-12 caller/upstream source and the writer/source of the input at `RSI+0x38`;
2. non-destructor/non-meta `TWorldMapRenderProvider` windows and Storage/render edges;
3. actual `TWorldMapCamera` geometry/projection/scale windows, including `0x00ced1b0` only where exact linkage can be established;
4. non-destructor `TWorldMapPicker` transform/bounds windows;
5. fixed-limit/capacity/literal/overflow audit on the recovered paths.

No client patch, byte modification, live process access, canonical runtime access or consumer-branch edit is authorized.

## Next action

Run a fresh exact-fenced bounded source staging that adds target-vtable windows plus caller discriminators, validate/disassemble only the sanitized windows on GitHub-hosted infrastructure, then curate a second durable FACT/INFERENCE/UNKNOWN handoff for PR #367.
