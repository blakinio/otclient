# OTC-20260817 — retained exact-client UI geometry for OCR-free bootstrap

```yaml
evidence_date: 2026-08-17
task: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
purpose: replace unavailable OCR bootstrap locator with bounded raw-XWD geometry revalidation
client_version: 15.32.df7b29
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
world_semantics_from_ui: forbidden
```

## Retained sources directly re-inspected

Two still-retained Track A Actions artifacts were downloaded and inspected only to recover non-secret UI geometry. No retained account identity is reproduced in this record.

```yaml
login_form_source:
  artifact_id: 9221131366
  artifact_name: track-a-enter-first-character-only
  run_id: 31805408522
  digest: sha256:454feeba9be116d9cbc32d73209e87ff4d042654ad1d52ed3fab02a6ca3dc17b
  file_used: before.xwd
selection_world_source:
  artifact_id: 9221234379
  artifact_name: track-a-software-world-login
  run_id: 31730884814
  digest: sha256:74263c46063edcfca85fa754a3f88076995c18473592f1378bbcb404c206845f
  files_used:
    - pre-login.xwd
    - select.xwd
    - world.xwd
```

All inspected windows are exactly `1020 x 650`. Their XWD headers are version 7, ZPixmap format, 24-bit depth, 32 bits per pixel, 4080 bytes/line, little-endian pixel order with masks `R=0xff0000`, `G=0xff00`, `B=0xff`.

## FACT — safe login control interior points

Visual inspection of the retained empty login-form XWD establishes these interior points in the exact `1020 x 650` client window:

```yaml
email_field_point: [520, 275]
password_field_point: [520, 305]
login_button_point: [590, 389]
```

These points are inside the corresponding controls, not on their borders. The retained image contains empty credential fields; no secret value is recovered or persisted.

## FACT — safe first character-row point

The retained `Select Character` XWD is also `1020 x 650`. The first full character row spans a large table row around `y=184..251`; a safe interior selection point is:

```yaml
first_character_row_point: [300, 195]
activation: Return after selecting the row
```

The accepted historical login procedure already records that the successful workflow selected the **first full character row**, then sent `Return`. This evidence only replaces how that row is located; it does not promote the UI to world-state evidence.

## Mechanical raw-XWD screen classifier

To avoid OCR entirely, a deterministic classifier was calculated directly from retained raw XWD pixels. The sampled ROI is:

```text
x = 135..884 step 5
y = 110..329 step 5
pixel is grayscale when max(R,G,B)-min(R,G,B) <= 3
```

Measured grayscale ratios:

```yaml
empty_login_form: 0.15984848484848485
select_character: 0.9890909090909091
in_game_world: 0.435
loading_game_files: 0.003787878787878788
```

The runtime helper may therefore classify only these bounded bootstrap states:

```yaml
LOGIN_FORM: 0.10 <= grayscale_ratio <= 0.30
SELECT_CHARACTER: grayscale_ratio >= 0.90
OTHER: otherwise
```

It must additionally require the live XWD header to match the exact `1020 x 650`, 32-bpp shape before using fixed control points. Every task-local XWD used for classification must be deleted immediately and never uploaded.

## Acceptance boundary

This classifier is **bootstrap geometry only**. It does not prove login success, character identity, player position, map state or world entry.

Current causal task still requires:

```text
pre-Storage GDB observer ARMED before credentials
LOGIN_FORM classified before credential injection
SELECT_CHARACTER classified before selecting the row
actual FullMap event + map-description strip records for structural IN_GAME
SOCKS-only client transport / zero direct client TCP / zero client UDP
```

A sent click or `Return` remains non-evidence until the structural protocol observer proves progression.
