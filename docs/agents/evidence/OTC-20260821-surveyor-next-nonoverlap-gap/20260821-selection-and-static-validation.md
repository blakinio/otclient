# Surveyor v2 next-gap selection and static validation

Date: 2026-08-21 Europe/Warsaw
Task: `OTC-20260821-surveyor-next-nonoverlap-gap`
Implementation PR: `#658`
Starting trusted main: `dce8bbd0e78ceea3681a1fe1dab40d3c19ed7458`

## Fresh repository-only baseline

The current-main source was collected without any runtime input:

```text
PYTHONPATH=. python -m tools.tibia_re_surveyor --collect-all --output-dir <temporary>
TIBIA_RE_SURVEYOR_ROWS=169
TIBIA_RE_SURVEYOR_COLLECT_ALL_ALIASES=12
TIBIA_RE_SURVEYOR_MISSING_READERS=8
privacy-scan.result=PASS
runtime=REPOSITORY_INPUT_ONLY / NO_RUNTIME_INPUT_THIS_RUN
```

Fresh missing-reader ranking:

```text
1  world_minimap_typed_reader       125
2  ui_settings_typed_reader          65
3  chat_social_typed_reader          60
4  economy_panels_typed_reader       60
5  features_typed_reader             60
6  item_loot_typed_reader            60
7  creature_combat_typed_reader      40
8  inventory_containers_typed_reader 40
```

## Non-overlap decision

`world_minimap_typed_reader` is not admissible for this slice because open PR #475 still owns causal worldmap server-delivery work and open PR #593 still owns current world/minimap static G1 work. The owner command explicitly requires avoiding that overlap.

No open PR matched the UI/settings alias/surface. The prior exact-build task `docs/agents/tasks/archive/OTC-20260819-track-a-ui-settings-static-model.md` is terminal with `session_role: released` / `ownership_released: true`. Its promoted evidence on current exact build `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8` establishes compiled `tibia::config::TClientOptions`, one `clientoptions.json` literal, and reversible causal persistence for exactly:

```text
options.soundMasterVolume
options.soundMasterVolumeOld
```

Therefore `ui_settings_typed_reader` is the highest-ranked current P0/P1-family gap that can be implemented without the active world/minimap ownership collision.

## Reader boundary

The implementation exact-fences PID start identity plus client size/SHA before static/runtime reads. It requires compiled `tibia::config::TClientOptions` presence and the unique `clientoptions.json` literal, then reads only the two causally established Master Volume integer fields. Physical repair evidence later binds the current persistent runtime file specifically as `conf/clientoptions.json` under the exact executable package root.

Both embedded probe outputs are revalidated by the outer reader before acceptance; malformed or inconsistent static/live payloads fail closed without retaining arbitrary exception text.

It explicitly does **not**:

- read or write `/proc/<pid>/mem`;
- read arbitrary process environment;
- write the settings file;
- retain arbitrary JSON fields;
- claim current UI-applied volume, all settings, QSettings linkage, or `TClientOptions -> clientoptions.json` ownership;
- promote canonical coverage status.

## Static/focused validation

After implementation:

```text
python -m unittest tests.tools.tibia_re_surveyor.test_ui_settings -v
6/6 PASS

python -m unittest discover -s tests/tools/tibia_re_surveyor -p 'test_*.py' -v
57/57 PASS

git diff --check
PASS
```

Fresh repository-only post-implementation collect-all:

```text
ROWS=169
ALIASES=12
MISSING=7
PRIVACY=PASS
ui_settings_typed_reader removed from missing-reader gaps
world_minimap_typed_reader remains rank 1 and intentionally untouched
```

No official-client runtime was observed during this implementation/static-validation phase; task admission remains `runtime_access:none` until the separately gated trusted-main physical acceptance phase.

## Independent audit findings and remediation

Fresh Codex validator review `PRR_kwDOTVmdjs8AAAABKddk8A` inspected exact head `e91504bb8dcfcb7d582baf122710981e76c957e0` and opened two findings.

`AUD-658-001` — P1, high confidence: accepted probe dictionaries were later embedded as full `static_evidence` / live output. An unexpected future probe field could therefore escape the intended telemetry allowlist. Remediation rejects any static/live key set other than the exact expected contract and rebuilds both accepted dictionaries from explicit scalar fields before publication.

`AUD-658-002` — P2, high confidence: the fixed settings path used `Path.resolve()` before `O_NOFOLLOW`, allowing symlink traversal to be normalized away. Remediation opens the passwd home and every fixed path component with directory descriptors plus `O_NOFOLLOW`, opens only `clientoptions.json` relative to the final directory descriptor, and requires the opened object to be a regular file owned by the target process uid.

No authority or semantic scope was broadened by either repair. The reader still performs no process-memory access, no file write, no GUI input, no process control, no login/relogin and no gameplay action.

Post-remediation deterministic validation:

```text
UI/settings focused tests: 8/8 PASS
all Surveyor tests:         59/59 PASS
Python compileall:           PASS
repository-only collect-all: 169 rows / 12 aliases / 7 gaps
privacy scan:                PASS
Track A runtime governance:  PASS
git diff --check:            PASS
```

A fresh exact-head independent re-audit is required after the remediation commit; the original review is not treated as PASS after code changed.
