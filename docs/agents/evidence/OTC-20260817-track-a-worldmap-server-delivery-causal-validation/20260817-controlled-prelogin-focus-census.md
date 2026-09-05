# Worldmap causal baseline — controlled pre-login focus census

Task: `OTC-20260817-track-a-worldmap-server-delivery-causal-validation`  
PR: #475  
Date: 2026-08-17

## Provenance

Physical no-secret run:

- workflow run: `32037418588`
- physical job: `95410518369`
- head: `d0031b3f177874dcd9a3134d2aa080bd76d971c2`
- runner: `synology-otclient-01`
- result: `SUCCESS`

The workflow intentionally had no credential-submission path and executed with `TIBIA_TEST_EMAIL` / `TIBIA_TEST_PASSWORD` absent.

## FACT — exact runtime fence

```text
WORLDMAP_XRES_OWNED_VIEWABLE_COUNT=1
WORLDMAP_XRES_OWNED_GEOMETRY=1020x650;count=1
WORLDMAP_XRES_SELECTED_GEOMETRY=1020x650
WORLDMAP_BASELINE_MANIFEST_FENCE=PASS
WORLDMAP_BASELINE_CLIENT_PID=13460
WORLDMAP_BASELINE_WINDOW_IDENTITY=x11-window:12582929
WORLDMAP_BASELINE_TARGET_UNIQUENESS=PROVEN
WORLDMAP_BASELINE_GDB_ATTACH=PASS
WORLDMAP_BASELINE_PRE_STORAGE_OBSERVER=ARMED
```

The XRes selector retained exact `LocalClientPid` ownership as the authority, enumerated owned `VIEWABLE` resources and selected the unique largest owned window. This removes the former hardcoded-window-size ambiguity without weakening the exact-PID fence.

## FACT — no-secret noise-controlled focus census

Mode:

```text
WORLDMAP_PRELOGIN_FOCUS_SCAN_SECRET_ENV=ABSENT
WORLDMAP_PRELOGIN_FOCUS_SCAN_MODE=TAB_NOISE_MASK_CONTROLLED_REVERSIBLE_DUMMY_TEXT
```

For every Tab state the probe measured temporal idle repaint masks, entered harmless dummy text, cleared it, measured post-clear noise, subtracted the measured noise mask and accepted only a spatially local reversible signal.

Accepted candidates:

| Tab | Noise pixels | Causal signal | Overlap | Signal bbox | Residual |
|---:|---:|---:|---:|---|---:|
| 2 | 1123 | 228 | 0.596859 | `911,485,1020,496` | 395 |
| 3 | 1065 | 460 | 1.000000 | `908,513,985,527` | 13 |
| 5 | 1107 | 460 | 1.000000 | `908,513,985,527` | 8 |

Other Tab states either had no surviving causal signal or were rejected because their surviving bbox covered a large portion of the client surface. Examples around `15,11,974,497` were correctly rejected by the locality gate.

Terminal markers:

```text
WORLDMAP_PRELOGIN_CONTROLLED_EDITABLE_CANDIDATE_COUNT=3
WORLDMAP_PRELOGIN_CONTROLLED_FOCUS_SCAN=COMPLETE_NO_SECRET
WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_BASELINE_CLEANUP=COMPLETE
```

## Claim boundary

### FACT

- Tabs `2`, `3` and `5` are localized focus states where reversible dummy-text input caused a signal surviving measured repaint-noise subtraction.
- Tabs `3` and `5` are the strongest current candidates: identical local bbox, overlap `1.0`, residual `13` / `8`.
- No protected credentials were used.
- No login was submitted.
- No character was activated.
- No gameplay stimulus occurred.
- Baseline login budget remains unconsumed.

### UNKNOWN

- whether any candidate is the account/e-mail field;
- whether any candidate is the password field;
- whether Tabs `3` and `5` are distinct widgets or revisit the same widget;
- semantic identity of the current startup surface;
- authoritative baseline FullMap extent;
- any effect of `[19,14]`.

### INFERENCE — not proof

Tabs `3` and `5` are currently the best candidates for a genuine text-editable widget because their causal masks are fully overlapping and tightly localized, unlike animation-contaminated whole-surface states. Their semantic role must still be independently classified before any credential use.

## Next discriminator

Keep the physical workflow on no-client safety hold. Use a separately statically validated no-secret probe on the accepted local candidates to distinguish masked versus unmasked text behavior and determine whether Tabs `3` and `5` address the same widget. Do not expose protected credentials until the required login fields are independently discriminated without relying on historical coordinates.
