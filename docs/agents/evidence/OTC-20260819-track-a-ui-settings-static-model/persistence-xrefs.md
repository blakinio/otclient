# Current-build settings persistence xrefs

Date: 2026-08-19 (Europe/Warsaw)  
Task: `OTC-20260819-track-a-ui-settings-static-model`  
Alias: `TIBIA-RE-UI-SETTINGS`  
Track: `official-client-re`  
Researcher delivery: Draft PR only; coordinator-only promotion

## Exact probe and subject fence

Second-stage bounded static discriminator:

- workflow: `.github/workflows/track-a-ui-settings-static-model.yml`
- workflow source commit: `7b7d230f358a43a34693a3c477446b4169f0e3a8`
- workflow run: `32194426242`
- job: `95895411896`, `Recover official-client UI/settings static model`
- conclusion: `success`
- `UI_SETTINGS_XREF_SCAN=PASS`
- `runtime_access: none`
- `client_executed: false`
- `proprietary_binary_retained: false`

Subject identity reproduced from the first-stage scan:

```yaml
packed_size: 10214529
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
```

## Evidence classification

- **FACT** — directly emitted by the successful static discriminator on the exact subject above.
- **INFERENCE** — structural interpretation that follows from multiple FACT items but is not runtime proof.
- **UNKNOWN** — not established by this discriminator.

## `clientoptions.json` code references

### FACT

The scan found exactly one retained NUL-terminated literal named:

```text
clientoptions.json
```

at virtual address `0x20d2406`.

A linear Capstone decode of executable ELF sections reported `38` RIP-relative instruction references to that literal. The bounded report emitted the first 32 reference addresses; they range from `0x5f50a0` through `0x692752` in the retained sample.

The nearby relevant-string context for these references consistently included a file/resource-name cluster containing:

```text
config.ini
client.log
gpublacklist.json
minimapmarkers.bin
compendium.json
onlinenumbers.json
boostedcreature.json
eventschedule.json
assets.json.sha256
Tibia
```

The bounded nearby imported-call context was not a JSON read/write chain; in the emitted sample it was limited to `__cxa_atexit@plt`.

### INFERENCE

`clientoptions.json` is part of a compiled current-build file/resource-name topology and is referenced from executable code. This is stronger than literal-string presence alone.

### UNKNOWN / negative control

The emitted xref context did **not** establish a call chain from those references to:

- `tibia::config::TClientOptions`;
- `shared::TFileSystemHelper::readJsonFileAsQJsonDocument`;
- `QJsonDocument::fromJson` / `toJson`;
- an observed file-open/read/write primitive.

Therefore this evidence does **not** prove that `TClientOptions` serializes to `clientoptions.json`, nor whether the file is a template, resource, migration source, runtime store, or another configuration artifact. The linear-disassembly reference count is retained as a reproducible static result, not promoted into a semantic persistence claim.

## `QSettings` code references

### FACT: resolved PLT surface

The exact current binary exposes four resolved PLT targets used by the discriminator:

```text
0x4d44e0  QSettings::value(QAnyStringView, QVariant const&) const@plt
0x4d78e0  QSettings::beginGroup(QAnyStringView)@plt
0x4d7970  QSettings::setValue(QAnyStringView, QVariant const&)@plt
0x4d9150  QSettings::endGroup()@plt
```

The static decode found `51` direct callsites to these four targets.

### FACT: renderer-adjacent read path

A cluster beginning at `0x6ba00a` performs the direct sequence:

```text
QSettings::beginGroup
QSettings::value
QSettings::endGroup
```

The bounded preceding-call context for this cluster includes current-build Qt renderer/bootstrap calls such as:

```text
QVulkanInstance::setApiVersion
QVulkanInstance::create
QQuickWindow::setGraphicsApi
QQuickWindow::setTextRenderType
```

The `QSettings::value` result is followed by `QVariant::toString` in the emitted context.

### FACT: renderer-adjacent write paths

A nearby cluster beginning at `0x6bab00` includes repeated direct sequences of:

```text
QSettings::beginGroup
QVariant::QVariant(unsigned int)
QSettings::setValue
QSettings::endGroup
```

Its bounded preceding-call context includes:

```text
QQuickWindow::setGraphicsApi
QRhi::probe
QVulkanInstance::destroy
```

The same repeated begin/set/end pattern occurs in this code region at emitted callsites including `0x6bab34`, `0x6baba4`, `0x6bac14`, and `0x6bac84` for `QSettings::setValue`.

Other current-build `QSettings` clusters were also found, including read/value groups around `0x6c3cd5` and `0x76de4d`, and write groups around `0x6c4ffb`, `0x6edb24`, `0x6f5ac1`, `0x76e531`, and `0x76e5ed`. The bounded relevance filter did not recover their group/key strings.

### INFERENCE

The current official client has real code-level `QSettings` read and write behavior; these are not merely imported but unused APIs. At least one direct `QSettings` read/write region is structurally adjacent to Qt graphics-backend selection/probing, so `QSettings` participates in renderer/bootstrap configuration state in this exact build.

This strengthens H10's persistence-side model beyond options-page names alone.

### UNKNOWN / boundary

The probe did not recover the actual `QSettings` group names or keys, and it did not connect these `QSettings` callsites to `TGraphicsQMLOptionsPage`, `TClientOptions`, or `clientoptions.json`.

Accordingly, the following remain **UNKNOWN**:

1. which renderer/bootstrap fields are stored in each `QSettings` group;
2. whether H10's user-visible graphics options and low-level renderer/bootstrap settings share the same store;
3. which H11-H13 values, if any, use `QSettings`;
4. how `clientoptions.json` relates to `QSettings`;
5. exact profile/migration behavior;
6. runtime readback after UI mutation;
7. persistence after reload/restart.

## Coverage consequence — no self-promotion

**RECOMMENDATION:** H10 and H14 now have current-build code-level STATIC evidence in addition to lexical/model evidence:

- H10: a concrete `QSettings` read/write region is adjacent to renderer/backend setup calls;
- H14: `QSettings` is demonstrably called for reads and writes, and `clientoptions.json` has executable-code references, but the relationship between these persistence mechanisms remains unresolved.

This is not sufficient for `DONE` and does not satisfy the alias's required `read -> reversible write -> reload/restart persistence` runtime chain. The researcher does not modify PR #536's canonical matrix.

## Smallest next discriminator

The static phase has established real persistence-capable callsites but not the high-level object-to-store relationship. The next useful discriminator should be one of:

1. a stronger static function-boundary/call-graph recovery around `clientoptions.json` and the JSON helper calls, if it can produce object-level linkage without speculative matching; or
2. after fresh Track A runtime admission, a single low-risk reversible setting with exact before/read/write/reload/rollback evidence under the shared input lock.

No live setting change, client execution, login, credential use, display/renderer mutation, or network mutation was performed in this phase.
