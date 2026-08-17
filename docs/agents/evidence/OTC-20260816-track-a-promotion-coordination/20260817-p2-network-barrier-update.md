# OTCLIENT-TIBIA-RE coordinator barrier — P2-NETWORK refresh

Date: 2026-08-17
Trusted base at promotion start: `main@8c9486e2c6109a7a39b564804c8acd707659b5e0`
Coordinator promotion PR: #450

## Scope of this checkpoint

This is a **lane-local current barrier refresh for P2-NETWORK only**. It intentionally does not rewrite or reclassify other programme lanes. For P2 it supersedes the older coordinator checkpoint text that still classified PR #310 as `BLOCKED_INPUT_STAGING`.

The earlier shared direct-hosted staging blocker remains historically valid for guessed/direct HTTP acquisition, but it is no longer the blocker for the bounded #310 object-identity question: that question was resolved through a separate exact-fenced bounded file-byte staging producer whose semantic analysis ran on GitHub-hosted infrastructure.

## P2 current disposition

```yaml
P2-NETWORK:
  consumer_task: OTC-20260815-track-a-p2-buffer-downstream-consumer
  source_pr: 310
  source_pr_state: closed_unmerged
  source_pr_disposition: ACCEPT_WITH_EDITS
  producer_task: OTC-20260817-track-a-p2-clientprocessor-sanitized-evidence
  producer_pr: 449
  producer_pr_state: closed_unmerged
  producer_pr_disposition: ACCEPT
  promotion_pr: 450
  promotion_state: final_closeout_and_exact_head_ci
  exact_client:
    version: 15.32.df7b29
    size: 51965216
    sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  bounded_chain:
    persistent_qbuffer_to_clientprocessor_this_plus_0x18: PROVEN
    first_downstream_consumer: PROVEN:TProtocolClientMessageProcessor+0x10@0xc2df80
    first_downstream_transform: PROVEN:TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
    same_message_to_dualconnection_plus_0x80_plus_0x78: PROVEN
    protocol_stage_order: PROVEN_PARTIAL
  remaining_unknown:
    - framing
    - sequence
    - compression
    - encryption
    - final_binary_egress
    - final_socket_ownership
    - complete_transport_stage_order_beyond_recovered_processor_chain
  material_findings_open_for_bounded_package: 0
  physical_e2e_required: false
  e2e: NOT_APPLICABLE
```

## Evidence transition that resolved the blocker

Source Draft #310 originally lacked the setup bytes that prove object identity from the persistent QBuffer into `TProtocolClientMessageProcessor this+0x18`. That produced findings `TACOORD-310-20260817-001` and `TACOORD-310-20260817-002` and a `RETURN_FOR_EVIDENCE` disposition.

Producer #449 created one bounded exact-file source slice and one GitHub-hosted decode generation:

- evidence run `32005141186 = SUCCESS`;
- source artifact `9279753620`, digest `sha256:6c970c23aa95856698eb71024937ed847502fb1f040701ce04c632da32c38d32`;
- hosted final artifact `9279759553`, digest `sha256:8228d6c281cf99f45f5c880b76e7a2817130156fde4cc892a402eccf4af10528`;
- evidence-head Track A governance `32005159534 = SUCCESS`;
- evidence-head repository CI `32005159706 = SUCCESS`;
- final producer closeout head `dbd75c152957ae945804f81313f485430b6cb768`;
- final producer Track A governance `32006193081 = SUCCESS`;
- final producer repository CI `32006193202 = SUCCESS`.

The coordinator independently re-decoded the source artifact and cross-checked it with accepted #308 persistent-buffer evidence and current-main canonical DualConnection typing. Both previous HIGH findings are closed.

## Safety and routing

The new producer did **not** reinstate Synology as the semantic/static-analysis executor. On the host-local source runner it only:

1. verified the exact regular-file size/SHA fence;
2. copied a narrowly enumerated set of file-byte windows as sanitized hex plus bounded vtable words;
3. uploaded no raw executable/package.

Disassembly and semantic validation occurred on `ubuntu-latest`. No client process, process memory, canonical runtime state, X11/VNC, login/session, gameplay or owner-funded AI quota was used.

PR #374 remains terminal `INPUT_BLOCKED` for its exhausted direct hosted-discovery approach. No guessed/direct HTTP staging was reopened. Quarantined run `31944051248` remains excluded from current proof.

## Barrier effect

The bounded #310 downstream-consumer task is no longer a programme blocker and becomes terminal when promotion PR #450 merges. P2 as a **programme lane is not complete**: framing, sequence, compression, encryption and final binary egress/socket ownership remain unresolved and must be selected as separate future READY research only under fresh ownership/admission.

Other programme-lane states are not refreshed by this checkpoint and must be resolved from their own current tasks/PRs rather than inferred from the older coordinator snapshot.
