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
## Exact source-B payload and RTTI proof

Exact run `33175306133` / artifact `9687437490` (head `065bd557a6416abfcf59038054c694a617f1cc5b`) decoded the `0x31b5940` initializer source through its proven C-string constructor wrapper `0x6a7200`. The bounded payload is:

```text
literal VA        0x20cea63
length            0
byte_values       []
sha256            e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
classification    PROVEN_EMPTY_C_STRING_TO_QSTRING
```

The durable-state JSON SHA-256 for that run is `b5b329c395aae48331788c1ff767b53939ed6c833b96d90e82af9e71d0cf8ebf`. This proves source B is an empty QString state; it does **not** by itself prove whether empty means start screen, character selection, or gameplay.

Exact RTTI run `33174987862` / artifact `9687279558` (head `f7a0d0a7581675ec6119c296b626c4890207a331`) independently recovered:

```text
typeinfo  0x30c2250
primary vptr 0x30c3488
mangled N5tibia10gamewindow21TGameWindowControllerE
```

That result JSON SHA-256 is `a4886d573e63cc491287548dfbcb1521f059904966dc5e88051afe3342b66e36`. It is sufficient for future exact-current unique-object discovery without reusing historical object addresses.

Source A (`0x31b29b0`) remains semantically unresolved. Its bounded xref window ends before the next use, so the next static step is to extend only that source initializer context.

## Source-A semantic resolution

Exact extended-initializer run `33175923574` / artifact `9687657554` on head `df157928c73af80de0ecb6474408d80a59808304` resolved the remaining BSS source `0x31b29b0`. The bounded constructor path is:

```text
source object    0x31b29b0
literal VA       0x28c4e8c
helper           0x6a7200
length           6
UTF-8            INGAME
payload SHA-256  c2fffc542eee743e8ff96c90698a369f8d0b075fe22bb411fca5b61ba8373d1e
```

The exact durable-state JSON SHA-256 is `5a3bf25a1d7bc0250b4a4303d4af3f1b7fdce9ed26b65e0311b9c1868494042d`; artifact ZIP digest is `sha256:cb8aff18c477d9b2f5ea69d4e9e573265446975647dd8efee9077000d8599a94`.

Together with the separately proven empty source B, the current static model is now:

```text
TGameWindowController + 0x60 == gameWindowState : QString
source A 0x31b29b0               == "INGAME"
source B 0x31b5940               == ""
static semantic candidate         == gameWindowState == "INGAME"
```

This is an exact-current **static semantic candidate**, not a live `IN_GAME` promotion. The remaining requirement is fresh read-only causal validation across login screen, character selection, visible world, and world exit on one admitted exact process.
