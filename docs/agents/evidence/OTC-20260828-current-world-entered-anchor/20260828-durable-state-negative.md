# Exact-current durable world-state probe — negative result

Task: `OTC-20260828-current-qt-world-correlation`

Producer run `33168156681`, exact head `1fc7eecf11349f7395122412f3c286ada5af7ffa`.

```text
artifact id    9684443359
artifact name  track-a-current-world-entered-anchor-33168156681
artifact zip   sha256:7ac0bb12efda6ce2db887765a491d96b923016ebcd7270bc006e7c3aed60ba97
durable JSON   sha256:a1f4f6bf492fb0b8fcbeb9de89a7db80ad921a97da22d1e818ec8ec64f3b71d3
```

The exact client fence remained `15.32.75d4a0 / 52105824 / d1a16819...` and the client was never executed by this static workflow.

## Result

```text
candidate.state  NOT_PROVEN
candidate.reason DURABLE_FIELD_NOT_FOUND
```

The tested hypothesis required one simple `this+offset` field to be set by `onWorldEntered` and reset by at least two independent world-exit paths. The exact binary did not satisfy that contract.
Observed simple writes were intentionally not promoted:

```text
onGameSessionDisconnected               this+0x1b8 <- 0
onDialogResponseShowCharacterSelection  this+0x0eb <- 1
onWorldEntered                          no qualifying simple this-immediate write
```

Those offsets belong to different lifecycle effects and are **not** an `IN_GAME` oracle.

```text
SIMPLE_DURABLE_FIELD_HYPOTHESIS=REJECTED
OFFSET_0xEB_AS_IN_GAME=REJECTED
OFFSET_0x1B8_AS_IN_GAME=REJECTED
IN_GAME_CLAIMED=false
SEMANTIC_PROMOTION_PERFORMED=false
```

The next static frontier is a richer receiver/property/state-propagation analysis, starting with the current `TGameWindowController` QMeta properties and exact `worldEntered` connection edges.
