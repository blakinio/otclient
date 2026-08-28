# Exact-current `worldEntered` activation boundary

Task: `OTC-20260828-current-qt-world-correlation`

Producer run `33166836780`, job `98834160830`, exact head `71d653dd3b550e1fa3d066fd976bcee27cc23283`.

Artifact:

```text
id      9683917257
name    track-a-current-world-entered-anchor-33166836780
zip     sha256:7fafb96ebe9595192def8b7228d4c8ea6e3bf02d3a587fc902971eecf07ba1ba
result  sha256:b0ad58787424f62c6ea4ed19e0d83227c51cc820ac64ef21190ac9bf26fc05fa
```

The workflow re-fenced the exact public client before analysis:

```text
version   15.32.75d4a0
size      52105824
sha256    d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
```
## Proven current activation boundary

The current generated `TPlayerProtocolMessageHandler` QMeta dispatch contains 22 signals. Static analysis of all 22 generated signal cases found one common external branch target and proved the expected arguments for `worldEntered`:

```text
worldEntered QMeta index       17
worldEntered generated case    0xd28890
TPlayerProtocolMessageHandler staticMetaObject 0x30b6ba0
common QMetaObject::activate boundary          0x4d7dc0
activation mode                DIRECT_FROM_GENERATED_CASE
signal traces checked          22
world EDX values               [17]
world RIP references           [0x30b6ba0]
activation state               PROVEN
```

The `0x4d7dc0` address is current-build-fenced only. It is not reused from historical evidence.

This establishes the exact semantic Qt signal-emission boundary. It still does **not** authorize instrumentation of the canonical runtime: Track A `read_only` explicitly forbids altering instrumentation state.
## Classification

```text
STATIC_QMETA_SIGNAL_IDENTITY=PROVEN
STATIC_GENERATED_DISPATCH_CASE=PROVEN
STATIC_QMETA_ACTIVATION_BOUNDARY=PROVEN
CANONICAL_RUNTIME_INSTRUMENTATION=NOT_AUTHORIZED_BY_READ_ONLY
DURABLE_WORLD_STATE_FOR_READ_ONLY_POLLING=NOT_YET_PROVEN
RUNTIME_WORLD_ENTERED_EVENT=NOT_YET_OBSERVED
IN_GAME_CLAIMED=false
SEMANTIC_PROMOTION_PERFORMED=false
```

The safe next step is static recovery of a receiver or durable field changed by `worldEntered` and reset on world exit, followed by ordinary read-only process-memory polling after a fresh runtime admission.
