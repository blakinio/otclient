# Track A — protocol literal xref v2 closure

## Scope

Official native Linux Tibia client only.

Exact client SHA256:

```text
e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

## Recovery of the previously pending experiment

The capability matrix referenced workflow run `31788735824` (`Track A protocol metadata xref graph`) as pending. Direct Actions inspection now establishes:

```yaml
v1_run: 31788735824
head: 55dc75c830e571490be30a5c83a922a528c5931f
result: CANCELLED
```

No conclusion is promoted from that cancelled run.

A successor workflow completed successfully:

```yaml
workflow: Track A protocol xref graph v2
path: .github/workflows/tibia-official-client-re-xref-graph-v2.yml
head: cfbe04c03de34f83646a82569c90dafaf342c129
run: 31789670398
job: 94733517691
runner: synology-otclient-01
result: SUCCESS
scanner: linear executable-segment pass for x86-64 RIP-relative LEA/MOV references
```

The exact client SHA gate passed before the scan.

## Result

The successful v2 run reports:

```text
TOTAL_DIRECT_RIPREFS=0
TRACK_A_XREF_V2_COMPLETE=true
```

Every selected high-value literal occurrence had `direct_riprefs=0`, including the selected handler-class/method strings and these generated message names:

```text
GameclientMessageMoveObject
GameclientMessageAttack
GameclientMessageFollow
GameclientMessageTalk
GameclientMessageTradeObject
GameclientMessageGoPath
GameserverMessageMoveCreature
GameserverMessagePlayerDataCurrent
GameserverMessageContainer
GameserverMessageTalk
```

Representative exact literal occurrence sets recovered by the successful v2 run are:

```yaml
GameclientMessageMoveObject:
  - 0x1cb047b
  - 0x1cb1912
  - 0x1cb2317
  - 0x1cc2c5b
  - 0x1cd133e
  - 0x1d5003b
GameclientMessageAttack:
  - 0x1cb0f16
  - 0x1cc24fb
  - 0x1cd1d42
  - 0x1d56edb
GameclientMessageFollow:
  - 0x1cb0f62
  - 0x1cc24bb
  - 0x1cd1d8e
  - 0x1d56e9b
GameclientMessageGoPath:
  - 0x1cb5322
  - 0x1cc2d9b
  - 0x1cd1188
  - 0x1d4ffbb
GameserverMessageMoveCreature:
  - 0x1cc5fdb
  - 0x1ccc0d2
  - 0x1d52cfb
  - 0x1d607b7
GameserverMessagePlayerDataCurrent:
  - 0x1cc5cbb
  - 0x1ccc5f3
  - 0x1d5243b
  - 0x1d5feb7
GameserverMessageContainer:
  - 0x1caf3f8
  - 0x1cc559b
  - 0x1ccd1af
  - 0x1d52cbb
  - 0x1d5ea57
GameserverMessageTalk:
  - 0x1cc601b
  - 0x1ccc079
  - 0x1cd847a
  - 0x1d5221b
  - 0x1d60877
```

## Classification

**FACT:** the selected literal names exist in the exact binary.

**FACT:** the successful bounded scanner found zero direct executable RIP-relative `LEA/MOV` references to all selected literal addresses.

**DISPROVEN AS A DIRECT RECOVERY ROUTE:** treating those literal names as a direct code-xref path to concrete handlers/builders is not supported by this exact-binary experiment.

This does not mean the messages are unused. The names can be descriptor/metadata/string-table data and the concrete code path may reference descriptor tables, generated functions or relocated metadata instead of the literal bytes.

## Consequence

Do not spend additional Track A experiment budget repeating direct literal-name xref scans for these targets. Continue through evidence-backed structural routes instead:

1. relocation-backed QMeta records and already decoded handler jump-table cases where available;
2. exact generated-code/protobuf descriptor layouts for selected messages;
3. direct caller/callee analysis from already proven handler tails and outbound builders;
4. live version-fenced bridge/object correlation once runtime ownership permits.

This closes the stale `31788735824` pending item in the capability matrix without estimating any semantic coverage percentage.
