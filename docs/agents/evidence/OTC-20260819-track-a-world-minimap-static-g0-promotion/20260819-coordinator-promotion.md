# Track A world/minimap static G0 — coordinator promotion

Date: 2026-08-19  
Source Draft: PR #545  
Source head: `55034d31a3cfd55c597f463c97ebf97065192c8b`  
Promotion base: `main@5940913a325288cfd9985be54af1a56b65e5560e`  
Decision: **ACCEPT_WITH_EDITS**

## Independent evidence verification

The coordinator did not trust the Draft summary as terminal evidence.

The original GitHub Actions artifact `9345368809` was downloaded and inspected independently. Its ZIP SHA-256 is exactly:

```text
c3c32ad9ce527e5ff7d469ae41914f3802fb55d465a993c8dbb32be2840e9755
```

matching the retained GitHub artifact digest. The ZIP contains exactly:

```text
fence.txt
minimap-qmeta.txt
minimap-strings.txt
```

and no raw official-client executable/package.

`fence.txt` independently confirms the producer's exact public-package fingerprint:

```text
PACKED_SHA256=1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
UNPACKED_SHA256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
UNPACKED_SIZE=52109920
CURRENT_PACKAGE_FENCE=PASS
MINIMAP_STRING_LINES=291
RAW_CLIENT_RETAINED=false
```

The package was the public `tibiaclient-linux-current/bin/client.lzma` fetched by producer run `32194443653`; this is an exact fingerprint of that public package at that run, not proof that any currently installed/canonical runtime process uses the same bytes.

## Material audit finding

```yaml
finding_id: WM-MINIMAP-AUD-001
severity: medium
confidence: high
subject: per-method static-metacall targets
source_claim: emitted `target=... direct=true` values are exact per-method destinations
result: rejected
```

The producer script heuristically scans for candidate 32-bit jump tables near each Qt `static_metacall`, chooses the candidate with the most executable computed destinations, and marks it `direct=true` whenever all computed entries are executable. That criterion is insufficient to prove that the chosen table belongs to the method dispatch.

The retained artifact directly falsifies exactness: unrelated classes/methods receive identical targets. Examples:

```text
TMinimapMarkerStorage methods 0..4
TMinimapTileStorage methods 0..4
  -> same five reported addresses

TMinimapVisibleArea::restoreZoomLevelFromOptions
TMinimapProtocolMessageHandler::handleCyclopediaMapDataMessage
TMinimapTileManager::publishGameAction
TMinimapTileManager::handleGameAction
  -> all reported as 0xde15a0
```

Therefore no per-method target address or `direct=true` classification from this producer is promoted.

## Accepted evidence boundary

The following survive independent falsification and are promoted:

- the exact public-package packed/unpacked SHA and unpacked size from the producer artifact;
- Qt metaobject ownership: class names, metaobject/static-metacall addresses, method/signal names and method counts parsed from Qt metadata;
- exact static strings for minimap floor/scroll/zoom action names and marker/QML/protobuf/disk surfaces;
- separate minimap controller/visible-area/tile/render-info and marker controller/storage/overlay/render-info responsibility surfaces;
- world-map camera/viewport conversion and layer-translation method-name surfaces;
- source Draft's strict `runtime_access: none` / no-login / no-client-mutation boundary.

The rejected per-method destination addresses are preserved only as negative/audit evidence.

## Coverage disposition

Against PR #536's status contract:

```text
F11 Minimap controller / visible area / floor state: NOT_STARTED -> PARTIAL
F12 Minimap markers:                              NOT_STARTED -> PARTIAL
F13 World<->screen transforms:                    PARTIAL -> PARTIAL
F08 server-delivered extent:                      BLOCKED unchanged
F10 worldmap patch causality:                     BLOCKED unchanged
```

F11/F12 qualify for `PARTIAL` because there is now a dedicated current-public-package subsystem package beyond broad lexical presence: exact Qt metaobject ownership plus coherent storage/action/persistence surfaces. They are not `DONE`; data layout, field semantics, formulas, causal runtime behavior and stability remain unproven.

The package does not modify PR #536's shared matrix/checklist paths; the coverage delta remains task-local until the coverage owner incorporates it.

## Safety / E2E

```yaml
runtime_access: none
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
client_byte_mutation_authorized: false
physical_e2e_required: false
e2e: NOT_APPLICABLE
```

No Synology/KasmVNC runtime, credential, login, gameplay, installed client or runtime process was used by this coordinator promotion.

## Source validation

Source head `55034d31a3cfd55c597f463c97ebf97065192c8b`:

```text
Track A agent runtime governance 32194785639 = SUCCESS
CI 32194785866 = SUCCESS
changed paths = exactly 3 source task/report/evidence paths
source review threads = 0
coordinator review = 4969045959
```

After this corrected promotion reaches `main`, source Draft #545 must be closed unmerged as superseded.