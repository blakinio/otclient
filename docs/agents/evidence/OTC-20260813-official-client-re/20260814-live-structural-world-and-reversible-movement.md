# Track A — live structural world and reversible movement

## Exact subject

Official Linux client `15.32.df7b29`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`, on `synology-otclient-01` in the owned Track A namespace.

## Live chain

Run `31730884814`, job `94785048338`, re-established the owned session through WARP and left the exact client running. Its visual transition markers (`466099` login pixels, `660094` world pixels) are bootstrap evidence only, not structural world proof. The process had seven established connections to the local SOCKS endpoint, no direct established connection and no UDP socket.

Run `31806223531`, job `94785688088`, armed the exact PIE-relative map decoder at `+0x19a8ea3`. Run `31806312967`, job `94785974126`, then sent `Up` followed by its inverse `Down` and completed successfully.

## Structural result

The forward step appended 33 decoded strip/object rows and the inverse appended another 55 (`0,33,88`). The first floor-7 forward strip spans `x=32537..32554`, `y=32502`; the inverse floor-7 strip spans the same 18-column range at `y=32516`. Companion floor-6 rows occur at `y=32503` and `y=32517`, preserving the floor projection relationship. Every captured record contains bounded `x`, `y`, `z`, order, object address and a bounded raw object prefix; this is executable-state evidence, not OCR.

The 18-column viewport fixes its horizontal player column at `x=32546`. The decoded top/bottom strip geometry is asymmetric around the player (`7` rows north, `6` rows south), yielding this reversible transition:

```text
(32546,32510,7) -> (32546,32509,7) -> (32546,32510,7)
```

This position is **DERIVED** from the authoritative decoded map-strip coordinates and the proven 18-by-14 viewport geometry. It is not claimed as a direct read of a standalone player-position member. The structural direction, one-tile delta, floor and exact restoration are proven. Pixel deltas (`146599`, `150668`) are supporting UI-change evidence only.

## Handler/layout implication

The live rows validate the selected map-strip field layout used by the observer: three little-endian 32-bit coordinates at `rsp+0x88`, followed independently by bounded order/object data. Together with the exact QMeta census, this closes the selected handler/layout gate without inventing a creature dispatch table: `TCreatureProtocolMessageHandler` has a relocation-backed static metacall at `+0xd12510` with zero own methods and a one-instruction `ret`; `TPlayerProtocolMessageHandler` has static metacall `+0xd1a920` and 22 exact methods.

## Boundary

- **FACT:** the exact live client produced coherent floor-7 map strips for forward and inverse movement and returned to the initial derived coordinate.
- **DERIVED:** the player coordinate is the fixed viewport center calculated from those authoritative strip coordinates.
- **UNKNOWN:** a direct standalone player-object position member address remains unpromoted.

