---
task_id: OTC-20260821-surveyor-action-protocol-reader
status: completed
phase: archived
agent: ChatGPT
project_lane: otclient
lane: P0-ACTION
track_id: official-client-re
task_kind: implementation
risk: medium
policy_version: 2
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: canonical-live-runtime
target_uniqueness: PROVEN
mutation_authorized: false
gui_input_authorized: false
process_control_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
implementation_pr: 645
implementation_merge_sha: f80dd43f741c39ce5ee4296396cb07891d04c324
acceptance_pr: 646
acceptance_merge_sha: b7fa88ef2d772c70ca7250b587e7f584327ee37b
repair_pr: 648
repair_merge_sha: dbc05824fb539a5dfffb0bd8cb48dbfb3a9a01e1
diagnostic_repair_pr: 652
diagnostic_repair_merge_sha: 53485c70f2532faa7588afc788f53cc67813b121
rw_bound_repair_pr: 654
rw_bound_repair_merge_sha: a28550bf5ad0880d947aa2ebc2de13f438cef6bd
physical_e2e_required: true
physical_e2e_result: PASS
physical_e2e_run: 32514243771
physical_e2e_job: 96872176204
physical_e2e_artifact: 9458204826
physical_e2e_artifact_digest: sha256:1368e91ee2206f050d253775f0a607f3c14c5e741721337f552231ccf8c92e5e
final_trigger_pr: 653
closeout_pr: pending
---

# Surveyor v2 action-protocol typed reader — completed

PR #645 introduced the exact-fenced `action_protocol_typed_reader`, and PR #646 installed the owner-controlled trusted-main read-only physical acceptance path. Subsequent physical failures were isolated without weakening acceptance: PR #648 removed unavailable external ELF tooling, PR #652 exposed only bounded failure diagnostics, and PR #654 raised only the action-protocol aggregate RW scan ceiling from 1536 MiB to 2 GiB after fresh measurement proved the exact runtime required `1934311424` bytes across 468 eligible writable mappings. The generic typed-presence probe remained unchanged at 1536 MiB.

Final repair head validation passed Track A Surveyor tests, Track A agent runtime governance, repository CI, zero review threads, and fresh validator audit with zero material findings. PR #654 merged as `a28550bf5ad0880d947aa2ebc2de13f438cef6bd`.

Final physical read-only acceptance used trusted `main@a28550bf5ad0880d947aa2ebc2de13f438cef6bd` in workflow run `32514243771`, acceptance job `96872176204`. Fresh target proof found exactly one exact-fenced client and one matching visible Tibia window: PID `19590`, start ticks `76611792`, executable `/home/kasm-user/otclient-track-a/Tibia-32177065988-1/bin/client`, size `52109920`, SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`, display `:1`, target uniqueness `PROVEN`. Canonical lease generation `19` was released/expired; registration was present and identity-matching, registration generation `2`, registration lease generation `19`.

Physical collect-all PASS: 169 rows, 12 aliases, 8 missing readers, privacy PASS, `action_protocol_typed_reader=AVAILABLE`, exact `tibia::game::TPlayerProtocolMessageHandler` object count `1`, `typed_object_identity=PROVEN`, process memory `read_only`, semantic state `TYPED_ACTION_PROTOCOL_OBJECT_IDENTITY_ONLY`, vptr `0x30bf620`, typeinfo `0x30bf298`, all action/protocol/opcode/payload/`IN_GAME` promotion flags false, and runtime mutation false.

Causal implementation delta: action-protocol reader `NO_TYPED_READER_IMPLEMENTED -> AVAILABLE`; missing readers `9 -> 8`; privacy `PASS -> PASS`.

Canonical evidence: `docs/agents/evidence/OTC-20260821-surveyor-action-protocol-reader/20260821-live-physical-e2e.md`.

Request-only trigger PR #653 was closed without merge after evidence capture. The temporary acceptance workflow is removed by the closeout change. The broader Surveyor program remains open with eight missing typed-reader gaps after this slice.