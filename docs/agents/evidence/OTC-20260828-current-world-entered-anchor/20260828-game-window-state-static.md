# Exact-current game-window state static proof

Task: `OTC-20260828-current-qt-world-correlation`

Producer run `33173004656`, job `98854514406`, exact head `b31d21caa2f142d9b439b9a247ffcc78db97cec2`.
Artifact `9686450777` (`track-a-current-world-entered-anchor-33173004656`).
Artifact ZIP digest: `sha256:d77a919a4a20f9fc1a9bc099dda4309326803120da596b28ae58a82731dd689e`.
Durable-state JSON SHA-256: `cad9437282929dc6324b1140b0939a3ef4b7c425dc133269af4735c2c9ca908f`.

Exact client fence:

```text
version  15.32.75d4a0
size     52105824
sha256   d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
```

## Proven property backing

Current `tibia::gamewindow::TGameWindowController` QMeta is `0x30a99a0`.
Its `gameWindowState` property is current property index `2`, type `QString`, notify signal index `4` (`gameWindowStateChanged`).

The generated Qt `ReadProperty` path is selected by `QMetaObject::Call == 1`, full property range `0..33`, and resolves property index `2` to case `0xd7a5f4`.The exact `qt_static_metacall` prologue binds `rbx <- rdi`, and the read case copies one contiguous 24-byte Qt6 QString-shaped value from `[rbx+0x60 .. +0x70]` before any helper call.
This yields:

```text
gameWindowState backing = TGameWindowController + 0x60
classification           = PROVEN_STATIC_QMETA_BACKING_MEMBER
```

This is a static property/backing proof only. It does not yet establish which runtime value means `IN_GAME`.

## Display lifecycle signals

The same current QMeta surface contains:

```text
startScreenNowDisplayed  signal index 23  unique normal emitter 0xd6acd3
gameScreenNowDisplayed   signal index 24  unique normal emitter 0xd6acf3
```

Their generated signal cases and activation paths are exact-current QMeta facts. They are stronger semantic surfaces than TCP count or window-title context, but an event alone is not a durable state.

## Direct gameWindowState assignments

Whole-text exact-current signal-emitter recovery found direct assignments to the proven `+0x60` backing immediately before `gameWindowStateChanged` activation. Both use the same helper `0x4d5e20`:

```text
site 0x6ec864  source 0x31b29b0
site 0x85fa78  source 0x31b5940
site 0x85fa99  source 0x31b5940
```
Both source objects reside in ELF NOBITS/BSS rather than file-backed static data:

```text
0x31b29b0 -> STATIC_QSTRING_VA_NOT_MAPPED
0x31b5940 -> STATIC_QSTRING_VA_NOT_MAPPED
```

Therefore their actual QString values must be recovered from the exact-current global initializer code. Treating either source address itself as a semantic state is forbidden.

## Current classification

```text
GAME_WINDOW_STATE_PROPERTY=PROVEN_STATIC
GAME_WINDOW_STATE_BACKING=PROVEN_STATIC_QMETA_BACKING_MEMBER
START_SCREEN_SIGNAL=PROVEN_STATIC
GAME_SCREEN_SIGNAL=PROVEN_STATIC
GAME_WINDOW_STATE_LITERAL_VALUES=NOT_YET_PROVEN
IN_GAME_CLAIMED=false
SEMANTIC_PROMOTION_PERFORMED=false
```

Next: resolve executable RIP xrefs to only `0x31b29b0` and `0x31b5940`, identify their bounded startup initializers, and recover the literal values if structurally provable. No live client action is required for that step.