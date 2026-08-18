# Track A S3 — player queue receiver static result

Task: `OTC-20260818-track-a-s3-player-queue-receiver-static`  
PR: `#514`  
Execution: GitHub-hosted / repository evidence only, `runtime_access: none`

## Result

The exact static edge:

```text
TProtocolMessageQueue receivedPlayer* signal
  -> QObject::connect / QSlotObject
  -> receiver object/type
  -> receiver member
```

remains **UNKNOWN** after the bounded S3 discriminator. The task found a real external evidence blocker rather than a contradictory player architecture result.

## Current exact-client source drift

The first S3 producer attempted to re-fetch the public current Linux client under the existing exact build fence:

```text
run 32117023999
job 95648736856
```

The packed SHA check failed before any semantic decode:

```text
expected client.lzma sha256
496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b

actual public-current object
DIFFERENT BUILD -> fail closed
```

No old VA/vptr/QMeta address was applied to the changed bytes. The task did not relax the hash fence, and it did not use PR #475's runtime/client as a replacement source.

## Prior exact-SHA evidence reuse

A second path reused only accepted sanitized exact-build job logs already produced by PR #498:

```text
phase4 hosted job 95442653919
phase5 hosted job 95443958584
```

Those logs contain the previously emitted exact-client connection setup around `0x7d51b0`, `QObject`/QSlot construction candidates and queue identity evidence. They contain no raw client bytes, account values or runtime state.

The first normalization run (`32118487756`) exposed a parser defect: historical disassembly lines use `7d52ea:` rather than `0x7d52ea:`. No result from the zero-line parse was accepted.

The corrected normalization run:

```text
run      32118874353
job      95654645734
artifact 9317732982
digest   sha256:2363db29be61748c491e369d8aadf067ba0bed65e86bc3b74aa61594625db312
result   SUCCESS
```

recovered:

```text
334 exact setup instructions
4 bounded connect blocks
member +0x88 references: 4
member +0x9c0 references: 1
0x3085b60 TProtocolMessageQueue staticMetaObject hits: 34
0x4dd800 connect-candidate hits: 60
0x4df670 QSlot/helper hits: 126
```

The available exact-SHA logs contain **zero** hits for all five canonical #513 player receive signal stubs:

```text
0xdf8bc1 receivedPlayerDataCurrentMessage  -> 0
0xdf8d3b receivedPlayerDataBasicMessage    -> 0
0xdf8e0d receivedPlayerStateMessage        -> 0
0xdf8e37 receivedPlayerSkillsMessage       -> 0
0xdf899f receivedPlayerInventoryMessage    -> 0
```

They also contain zero hits for:

```text
TPlayerProtocolMessageHandler primary vptr 0x308a008
TPlayerData primary vptr 0x308ca70
```

## What the reused setup does prove

The prior #498 exact-SHA evidence associates the `0x7d51b0` setup with repeated typed Qt connection construction and independently identifies `[enclosing+0x88]` as `tibia::protocol::TProtocolMessageQueue`. That is useful exact-build predecessor evidence, but the emitted window was produced for auth/session research and does not expose the player signal identities needed by this S3 task.

The task therefore does **not** repurpose an auth connection block into a player connection claim.

## Canonical inputs retained from #513

The following remain canonical main facts and are unaffected:

```text
TProtocolMessageQueue staticMetaObject 0x3085b60
qt_static_metacall 0xdf5fe0
355 methods / 192 signals

34  receivedPlayerDataCurrentMessage @ 0xdf8bc1
43  receivedPlayerDataBasicMessage   @ 0xdf8d3b
48  receivedPlayerStateMessage       @ 0xdf8e0d
49  receivedPlayerSkillsMessage      @ 0xdf8e37
117 receivedPlayerInventoryMessage   @ 0xdf899f

receivedPlayer* direct QMeta ownership by
TPlayerProtocolMessageHandler = DISPROVEN
```

## Classification

```yaml
FACT:
  public_current_client_no_longer_matches_exact_15_32_df7b29_packed_hash: true
  prior_exact_sha_connection_logs_recovered: true
  prior_exact_setup_instruction_count: 334
  prior_exact_connection_blocks: 4
  five_exact_player_signal_stubs_absent_from_available_prior_logs: true
  player_handler_vptr_absent_from_available_prior_setup_logs: true
  player_data_vptr_absent_from_available_prior_setup_logs: true

UNKNOWN:
  queue_signal_to_receiver_connection
  receiver_type
  receiver_member_or_QSlotObject
  handler_to_TPlayerData_mutation

DISPROVEN:
  available_prior_auth_connection_window_is_sufficient_to_prove_player_receiver: true
```

## Stop condition

The S3 frontier is `INCONCLUSIVE_BOUNDED / EXACT_SOURCE_DRIFT`.

A later continuation may resume only when one of these exists without violating current Track A ownership:

```text
1. an approved exact 15.32.df7b29 static source/artifact containing the relevant connection-construction window; or
2. an already-sanitized exact-SHA artifact/log that includes direct references to the canonical player queue signals/PMFs.
```

Do not use a newer public client with the old addresses, weaken hashes, infer the receiver from member proximity, or consume PR #475 physical runtime to manufacture this static evidence.

## Safety

```yaml
runtime_access: none
synology_used: false
x11_or_vnc_used: false
process_memory_used: false
credentials_used: false
login_performed: false
gameplay_performed: false
pr475_runtime_observed: false
pr475_runtime_mutated: false
```
