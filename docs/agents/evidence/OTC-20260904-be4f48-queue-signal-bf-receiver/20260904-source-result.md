# OTC-BE4F48 queue signal `0xbf` receiver — terminal source result

Exact-current source-only analysis for Tibia Linux client `15.32.be4f48` completed at analysis head `b2dd0fac6c58c325b93566c3f150e86e807ae208`.

## Proven

- exact client fence: size `52105824`, SHA-256 `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`;
- the already-proven queue callback `0xbd2190` / FDE `0xbd2190..0xbd2495` causally consumes the exact queued `GameclientMessage` pair;
- QMeta owner is `tibia::protocol::TProtocolMessageQueue`;
- signal `0xbf` is `clientMessageReadyToProcess`;
- the exact static-metaobject argument is independently re-proven in the bounded drain FDE by `0xbd221d: rbp=0x30b73e0 -> 0xbd22ae: rsi=rbp -> 0xbd22c2`;
- exact RIP-relative signal-body xref discovery yields one bounded `QObject::connectImpl` candidate at `0xbe2eee`, FDE `0xbe2a50..0xbe3086`, from signal-body reference `0xbe2e86`;
- receiver provenance reaches `ENTRY_ARG:rdi`.

## Withheld / terminal boundary

The selected connection's slot object is passed as `r9 <- rax` after a call-return boundary at `0xbe2eb1`. Within this bounded task no unique QSlot function target is proven. Therefore:

```text
queue_signal_receiver_identity=UNKNOWN
queue_signal_slot_identity=UNKNOWN
queue_signal_writer_identity=UNKNOWN
next_unique_writer_edge=UNKNOWN
final_queue_writer_identified=false
final_tcp_writer_identified=false
final_writer_contract=UNKNOWN
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=QUEUE_SIGNAL_BF_QSLOT_FUNCTION_NOT_UNIQUELY_PROVEN
```

Do not extend #880 into another QSlot/Qt writer discovery loop. Any later QSlot identity discriminator must be a new coordinator-admitted bounded source task.

## TDD / exact-head evidence

Repository-only REDs were observed before any client materialization, including run `33855995246` for the bounded-xref repair and run `33856595302` for the static-metaobject register-chain proof. Final exact-current source analysis:

```text
SOURCE_ANALYSIS_HEAD=b2dd0fac6c58c325b93566c3f150e86e807ae208
SOURCE_RUN=33856767530 success
SOURCE_JOB=100971771959 success
ARTIFACT_ID=9930504401
ARTIFACT_DIGEST=sha256:0eae231ded57a47aa7ea2dfa37339b2a2e465a0e1b031e618e95dccd04da8f6f
CI_RUN=33856767713 success
GOVERNANCE_RUN=33856767680 success
SELF_HOSTED_BOUNDARY_RUN=33856767493 success
```

Safety remained source-only: no official-client execution, login, credentials, process memory, packet capture, OCR/Vision, official-service E2E, or Track B PR #284 mutation.
