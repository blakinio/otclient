# OTCLIENT Track A — player queue receiver static frontier

Date: 2026-08-18  
Task: `OTC-20260818-track-a-s3-player-queue-receiver-static`  
PR: `#514`

## Executive result

The player inbound chain is currently proven to:

```text
GameserverMessagePlayer*
  -> exact TProtocolMessageQueue receivedPlayer* typed Qt signal
```

but the next edge:

```text
queue signal -> connected receiver/member
```

remains `UNKNOWN`.

This task did not fail because the receiver was absent. It hit an evidence-source boundary: the public `client.lzma` endpoint advanced away from the exact `15.32.df7b29` build, while the reusable exact-SHA sanitized connection logs available in the repository were generated for auth/session setup and do not contain any of the five exact player signal stubs.

## Fail-closed source drift

The current public client was rejected before semantic analysis when its packed SHA no longer matched:

```text
496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
```

No build substitution, hash relaxation or old-address reuse occurred.

## Exact-SHA predecessor evidence reuse

The task normalized prior #498 hosted exact-client logs:

```text
95442653919
95443958584
```

Corrected normalization:

```text
run 32118874353
job 95654645734
artifact 9317732982
sha256 2363db29be61748c491e369d8aadf067ba0bed65e86bc3b74aa61594625db312
```

Recovered setup inventory:

```text
334 setup instructions
4 connect blocks
+0x88 refs = 4
+0x9c0 refs = 1
TProtocolMessageQueue metaobject hits = 34
connect-candidate hits = 60
QSlot/helper hits = 126
```

The same logs contain zero direct hits for:

```text
0xdf8bc1
0xdf8d3b
0xdf8e0d
0xdf8e37
0xdf899f
0x308a008
0x308ca70
```

Therefore the emitted auth/session connection window cannot establish the player receiver.

## Durable conclusion

```yaml
QUEUE_TO_PLAYER_RECEIVER: UNKNOWN
PLAYER_RECEIVER_TYPE: UNKNOWN
PLAYER_RECEIVER_MEMBER: UNKNOWN
HANDLER_TO_TPLAYERDATA: UNKNOWN
S3_RESULT: INCONCLUSIVE_BOUNDED_EXACT_SOURCE_DRIFT
```

The correct recovery path is to resume this static edge only after an approved exact-build source/window becomes available. PR #475 runtime must not be used to bypass that boundary.

## What remains available for independent work

Other static/repository-only work can continue where sufficient exact-SHA sanitized evidence already exists. This S3 blocker is specific to the missing player connection-construction window; it does not invalidate the promoted S1/S2 protocol/QMeta results.
