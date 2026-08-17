# Track A P2 persistent-buffer downstream chain — coordinator promotion

Date: 2026-08-17
Consumer task: `OTC-20260815-track-a-p2-buffer-downstream-consumer`
Source Draft: PR #310, exact head `9b99b6b4bda2cf01e8fadcd8a00a6827de35d825`
Gap-closing producer: `OTC-20260817-track-a-p2-clientprocessor-sanitized-evidence`, Draft PR #449
Promotion decision: `ACCEPT_WITH_EDITS`

## Exact client fence

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux only
```

## Trust and provenance

The coordinator did not accept either researcher summary or generated `result.json` as proof. Primary bounded bytes from producer source artifact `9279753620` were independently decoded and cross-checked against already accepted exact-SHA evidence and current-main canonical ownership state.

Evidence inputs:

- accepted prior persistent-buffer boundary: PR #308, run `31903490468`, artifact `9251725866`, digest `sha256:f669df2ace3db0e269f60287d82c51b69eff11eaf7c7f5b932e049492632bd1e`;
- original #310 targeted processor bundle: run `31904696996`, artifact `9252025461`, digest `sha256:2a866247558b079944d81c9ad33bd4c5361c8144a7f367b273ab3bc19a080991`;
- gap-closing #449 evidence run `32005141186` at exact evidence head `1b615736726049e70c902a88d0fde5004044e7e0`;
- #449 source artifact `9279753620`, digest `sha256:6c970c23aa95856698eb71024937ed847502fb1f040701ce04c632da32c38d32`;
- #449 hosted final artifact `9279759553`, digest `sha256:8228d6c281cf99f45f5c880b76e7a2817130156fde4cc892a402eccf4af10528`;
- #449 exact evidence-head Track A governance `32005159534 = SUCCESS`;
- #449 exact evidence-head repository CI `32005159706 = SUCCESS`;
- current-main canonical owner typing: `docs/agents/evidence/OTC-20260813-official-client-re/20260814-final-write-reconciliation-generation-5.md`.

The #449 source stage performed exact-fenced read-only file slicing only. It did not disassemble, symbol-resolve or semantically classify on Synology, and did not access a client process, process memory, canonical state, X11/VNC, login/session or gameplay. All disassembly/semantic validation was disposable GitHub-hosted processing. No raw client/package was uploaded.

## Independently decoded setup identity

The accepted #308 artifact identifies calls `0x4dae90` and `0x4dae80` as `QBuffer` construction/open on this exact client. The new exact-file source slice independently contains:

```text
01970c89: mov    edi,0x20
01970c8e: call   0x4df670
01970c96: lea    r15,[rax+0x10]
01970ca3: mov    rdi,r15
01970ca6: mov    QWORD PTR [rbp-0x218],r15
01970cad: call   0x4dae90
01970cbe: mov    rdi,r15
01970cc6: call   0x4dae80
```

Therefore the exact persistent `QBuffer` object pointer is `r15`, retained at scratch `rbp-0x218`.

Later in the same exact setup:

```text
01971038: call   0x4df670
0197104f: lea    rdx,[rax+0x10]
01971056: lea    rcx,[rip+...]        # 0x2f6a208
0197105d: mov    QWORD PTR [rax+0x10],rcx
01971084: mov    rsi,QWORD PTR [rbp-0x218]
0197108f: mov    QWORD PTR [rax+0x28],rsi
019710a7: mov    QWORD PTR [rcx+0xa00],rdx
019710ae: mov    QWORD PTR [rcx+0xa08],rax
```

`rdx = allocation+0x10` is the actual processor object. The same saved QBuffer pointer is written to `allocation+0x28`, which is exactly processor `this+0x18`. Source-extracted vtable words independently give address point `0x02f6a208` slot `+0x10 = 0x00c2df80`.

Classification:

```text
persistent QBuffer -> TProtocolClientMessageProcessor this+0x18 = PROVEN
TProtocolClientMessageProcessor virtual +0x10 entry = PROVEN:0xc2df80
```

## Exact QBuffer consumer

The exact `0xc2df80` body contains:

```text
00c2df86: mov    r12,rdx
00c2df8a: mov    rbp,rsi
00c2df8e: mov    rbx,rdi
00c2dfa5: mov    rdi,QWORD PTR [rbp+0x18]
00c2dfd5: call   0x4ded50
00c2dfeb: lea    rbp,[rbx+0x8]
00c2e012: call   0x4dd3a0
00c2e040: mov    rax,rbx
```

The admitted exact-SHA artifact `9252025461` independently identifies `0x4ded50` as `QIODevice::readAll()` and `0x4dd3a0` as `QByteArray::operator=(QByteArray const&)`.

Classification:

```text
persistent QBuffer direct readAll = PROVEN
first recovered downstream consumer in this processor chain =
  PROVEN:TProtocolClientMessageProcessor+0x10@0xc2df80
```

## Same-message processor order

The exact invoker uses one stack message (`rbp = rsp`) and passes it sequentially:

```text
007dd66c: mov    rbp,rsp
007dd672: mov    rdi,rbp
007dd675: mov    rsi,QWORD PTR [rax+0xa00]
007dd67f: call   QWORD PTR [rax+0x10]
007dd686: mov    rsi,rbp
007dd689: mov    rdi,QWORD PTR [rax+0xa10]
007dd693: call   QWORD PTR [rax+0x10]
007dd69a: mov    rsi,rbp
007dd69d: mov    rdi,QWORD PTR [rax+0xc18]
007dd6a7: call   QWORD PTR [rax+0x80]
007dd6b1: mov    rsi,rbp
007dd6b4: mov    rdi,QWORD PTR [rax+0xc18]
007dd6be: call   QWORD PTR [rax+0x78]
```

Source-extracted vtable words give RawDataProcessor address point `0x02f6a230`, slot `+0x10 = 0x00b47130`.

The exact RawDataProcessor body starts from the same message `QByteArray` at `message+0x8` and contains:

```text
00b47132: lea    rax,[rsi+0x8]
00b47151: mov    QWORD PTR [rsp+0x8],rax
00b47189: call   0x4de730
00b47206: call   0x4df070
00b472f8: mov    rdi,QWORD PTR [rsp+0x8]
00b47300: call   0x4dd3a0
```

Exact-SHA artifact `9252025461` identifies these imported targets as `QByteArray::insert`, `QByteArray::append` and `QByteArray::operator=` respectively.

Classification:

```text
first recovered downstream byte transform in this chain =
  PROVEN:TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
same stack message passed ClientProcessor -> RawDataProcessor = PROVEN
```

## DualConnection handoff

Current-main canonical evidence already establishes:

```text
owner +0xc18/+0xc20 -> TGameserverDualConnection
virtual +0x80 = 0xb56d60
virtual +0x78 = 0xb56970
precondition +0x90 = 0xb40370
```

The independently decoded invoker above proves the same post-RawDataProcessor stack message is passed as `rsi = rbp` to owner `+0xc18` virtual `+0x80`, then again to `+0x78`.

Classification:

```text
same-message handoff to TGameserverDualConnection +0x80/+0x78 = PROVEN
protocol stage order = PROVEN_PARTIAL
```

`PROVEN_PARTIAL` means only the concrete recovered local order above. It is not a claim about all protocol transforms or transport ownership.

## Required UNKNOWN boundary

The following remain `UNKNOWN`:

- framing semantics;
- sequence semantics;
- compression semantics;
- encryption semantics;
- final binary egress;
- final socket ownership;
- complete end-to-end transport stage order beyond the recovered processor chain.

No name such as `RawDataProcessor` is used to infer framing/compression/encryption. Neither DualConnection virtual is labelled final egress.

## Negative controls

The promotion does **not** use as proof:

- generic `QIODevice` / `QBuffer` / `QByteArray` census;
- vtable adjacency as temporal order;
- historical final-socket evidence;
- quarantined Synology static-analysis run `31944051248`;
- the rejected/superseded PR #368 replay of that quarantined source;
- `RawDataProcessor` naming as transport semantics;
- DualConnection `+0x80/+0x78` as final socket/egress ownership.

PR #374 remains terminal `INPUT_BLOCKED`; no guessed/direct HTTP staging path was reopened.

## Audit and E2E

Fresh coordinator audit: `PASS_BOUNDED`, material findings open: `0` for this package.

Closed findings:

- `TACOORD-310-20260817-001` — missing persistent-QBuffer -> ClientMessageProcessor object identity;
- `TACOORD-310-20260817-002` — stronger source-Draft classifications exceeded then-admitted evidence.

E2E: `NOT_APPLICABLE` — static reverse-engineering/evidence promotion only; no runtime behavior, client process, login/session, gameplay or transport state changed.

## Integration edit

PR #310 is accepted **with edits** because its old workflow contains obsolete direct exact-client staging behavior. That workflow and researcher branch are intentionally not promoted. Only this bounded evidence and terminal lifecycle records are eligible for current-main integration.
