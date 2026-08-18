# Track A S3 player queue receiver — coordinator disposition

Date: 2026-08-18  
Source task: `OTC-20260818-track-a-s3-player-queue-receiver-static`  
Source Draft: PR #514  
Source final head: `94b27d117f23bddc541b688e0fa1f54e3db4e507`  
Trusted integration base: `main@592e193a5ada1c40d23193038f350e23c539898b`  
Decision: **ACCEPT_BOUNDED_INCONCLUSIVE**

## Accepted boundary

The prior promoted player path remains:

```text
GameserverMessagePlayer*
  -> exact TProtocolMessageQueue receivedPlayer* typed signal
```

The next edge remains unresolved:

```text
queue signal -> connected receiver/member = UNKNOWN
```

## External exact-source drift

A fresh exact-client producer was attempted on source run `32117023999 / 95648736856`. The public `client.lzma` object failed the pinned packed SHA before any semantic analysis. The task correctly failed closed and did not reuse old addresses on the changed build.

This is not evidence against the queue-to-receiver connection. It is evidence that `static.tibia.com/...current...` is no longer an admissible source for the pinned `15.32.df7b29` build.

## Reused predecessor exact-SHA evidence

The coordinator accepts the normalized inventory of existing #498 hosted exact-SHA static logs only within their original predecessor evidence boundary:

```text
phase4 hosted job 95442653919
phase5 hosted job 95443958584
normalization run/job 32118874353 / 95654645734
artifact 9317732982
sha256:2363db29be61748c491e369d8aadf067ba0bed65e86bc3b74aa61594625db312
```

The corrected parser recovered `334` setup instructions and `4` connect blocks. The logs include the queue/meta/connect/QSlot construction family but contain none of the five exact canonical #513 player signal stubs, no `TPlayerProtocolMessageHandler` primary-vptr hit and no `TPlayerData` primary-vptr hit.

Therefore the following hypothesis is rejected:

```text
available prior auth/session connection logs are sufficient to identify the player receiver
```

The rejection is bounded to the available log window; it does not imply the player connection is absent in the client.

## Retained UNKNOWNs

```yaml
QUEUE_SIGNAL_TO_RECEIVER_CONNECTION: UNKNOWN
RECEIVER_TYPE: UNKNOWN
RECEIVER_MEMBER_OR_QSLOTOBJECT: UNKNOWN
HANDLER_TO_TPLAYERDATA: UNKNOWN
```

No receiver is inferred from enclosing-object member proximity, handler naming or architectural expectation.

## Safety

```yaml
runtime_access: none
new_client_semantic_analysis_after_hash_mismatch: false
hash_fence_weakened: false
pr475_runtime_observed: false
pr475_runtime_mutated: false
synology_used: false
credentials_used: false
```

## Resume condition

Resume this exact frontier only if an approved exact `15.32.df7b29` static source/window or existing sanitized exact-SHA evidence with direct player signal/PMF references becomes available. Do not use a newer client under old addresses and do not consume the current physical Track A runtime to manufacture this static proof.
