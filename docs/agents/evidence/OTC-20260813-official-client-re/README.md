# Track A official Linux client RE — evidence index

Repository: `blakinio/otclient`
Track: Track A / `official-client-re`

Read these checkpoints chronologically and treat newer directly verified evidence as superseding older hypotheses:

1. `20260813-canonical-artifact-correction.md`
   - corrects the original false-positive world-entry claim;
   - records the launcher/package-state recovery;
   - records the first visually verified real world entry;
   - contains the reproducible canonical login recipe.

2. `20260814-map-observation-and-dynamic-provenance-checkpoint.md`
   - records post-login structural map observation;
   - proves current-floor aware range `18x14` versus visible viewport `15x11`;
   - records structured `(x,y,z,stack,type_id)` extraction without OCR;
   - records the controlled second-player item provenance experiments;
   - proves `+0x19a8ea3` is insufficient for dynamic changes on already-aware tiles;
   - records the BattlEye/early-GDB boundary;
   - records binary-analysis progress and current dynamic mutation candidates `+0xcecc70` and `+0xcecf40`;
   - defines the provenance architecture required before writing canonical OTBM;
   - defines the exact next controlled experiment.

Current continuation rule:

```text
Verify actual in-world state first.
If logged out/server-save/crashed, use the canonical full restart/login recipe.
Do not use pre-world GDB attach or bypass BattlEye.
Post-login, arm the dynamic mutation candidate callbacks before asking the owner to move another item.
Do not write every observed world object directly into canonical OTBM.
```
