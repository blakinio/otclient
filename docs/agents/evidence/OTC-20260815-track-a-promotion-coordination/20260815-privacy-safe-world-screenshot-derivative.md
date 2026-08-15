# Track A privacy-safe world screenshot derivative

Coordinator task: `OTC-20260815-track-a-promotion-coordination`
Track: `official-client-re`
Classification: `FACT / PRIVACY-SAFE DERIVATIVE METADATA`

## Source evidence

The derivative was produced from the accepted exact-build structural reversible-step evidence:

- workflow run: `31806312967`;
- job: `94785974126`;
- source artifact: `track-a-persistent-reversible-step`;
- artifact id: `9221332209`;
- source artifact ZIP SHA-256: `bd4be5b2f9d6cebf19fff6bdfa3677ad57c00ae4a376987f32b42e8a27907a4a`;
- exact client SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

The same source run is already accepted for structural Worldmap movement evidence. This record does not promote the screenshot itself as a substitute for structural state.

## Privacy transform

A local derivative was produced from the source `before.xwd` frame by:

1. decoding the XWD frame without OCR;
2. cropping to the central rendered world viewport only, excluding chat, minimap, sidebars, login UI and account/character-selection surfaces;
3. masking the remaining in-world character-name label;
4. retaining the visible world scene around the player.

Derivative geometry: `482x353` pixels.

Derivative SHA-256:

```text
7a26103850e886aa3f191b36813e1caaa76ba1d03957eefac387182f52025540
```

The binary derivative is intentionally **not committed** to the repository because official-client visual assets are not repository distributable assets. The hash and transformation provenance are retained here so the owner-visible derivative can be correlated with the accepted source artifact without storing proprietary visual bytes in Git.

## Claim boundary

- **FACT:** the derivative contains only the central world viewport from an already accepted exact-build structural-world run, with the visible character label masked and surrounding account/chat/sidebar UI excluded.
- **FACT:** no OCR or text interpretation was used to establish world semantics.
- **FACT:** structural world proof remains the decoded Worldmap evidence from run `31806312967`; the screenshot is supporting visual evidence only.
- **UNKNOWN:** this derivative does not prove that a client session is live now.
