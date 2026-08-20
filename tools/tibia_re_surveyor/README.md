# TIBIA-RE Surveyor

`tools/tibia_re_surveyor` is a deterministic evidence/indexing harness for the official native-Linux Track A programme. It reduces repeated agent census work without changing the repository's evidence standards.

## Surveyor v1 foundation

The v1 foundation, recovered from PR #592 onto current main, provides:

- deterministic parsing and validation of the canonical 169-row coverage matrix;
- current checklist titles and bounded repository evidence indexing;
- optional secret-minimized Docker/KasmVNC runtime identity, X11-window-class and canonical-control-plane observation;
- canonical dependency ranking;
- `coverage.json`, `runtime.json`, `agent_bundle.json` and a compact v1 summary.

Evidence mention counts are discovery aids only. Static presence, a filename match, a visible window or a diagnostic observation never promotes a canonical row to `DONE`.

## Surveyor v2 collect-all

`--collect-all` layers one reusable, passive evidence-distribution bundle over the v1 foundation. It does not create a second runtime controller and does not add gameplay authority.

A collect-all run emits:

```text
surveyor/
  coverage.json
  runtime.json
  agent_bundle.json
  summary.md

telemetry/
  auth-session.json
  player-state.json
  inventory-containers.json
  creature-combat.json
  world-minimap.json
  action-protocol.json
  item-loot.json
  chat-social.json
  features.json
  ui-settings.json
  economy-panels.json

aliases/
  TIBIA-RE-AUTH-SESSION.json
  TIBIA-RE-PLAYER-STATE.json
  TIBIA-RE-INVENTORY-CONTAINERS.json
  TIBIA-RE-CREATURE-COMBAT.json
  TIBIA-RE-WORLD-MINIMAP.json
  TIBIA-RE-ACTION-PROTOCOL.json
  TIBIA-RE-ITEM-LOOT.json
  TIBIA-RE-CHAT-SOCIAL.json
  TIBIA-RE-FEATURES.json
  TIBIA-RE-UI-SETTINGS.json
  TIBIA-RE-ECONOMY-PANELS.json
  TIBIA-RE-COORDINATOR.json

missing-readers.json
privacy-scan.json
summary.md
manifest.sha256
```

The first v2 layer deliberately does not invent typed client-memory readers. Each subsystem gets the repository evidence index plus the allowlisted common runtime observation when available. A missing typed reader is recorded as `UNAVAILABLE / NO_TYPED_READER_IMPLEMENTED` and ranked by current canonical blocker/dependency priority. That gap report is the input for later small reviewed reader tasks.

The v2 runtime snapshot is allowlisted: raw character-bearing window titles, arbitrary environment values, chat contents, packet payloads, credentials and auth/session secret values are not retained. Generated text/JSON is privacy-scanned before `manifest.sha256` is written. Output directories are owner-only where the host filesystem supports POSIX permissions.

## Local repository-only collect-all

This is useful for deterministic schema/tests and produces a gap report without claiming a live client:

```bash
PYTHONPATH=. python3 -m tools.tibia_re_surveyor \
  --collect-all \
  --output-dir /tmp/tibia-re-survey
```

Expected state without a runtime is `REPOSITORY_INPUT_ONLY`; `missing-readers.json` also records `NO_RUNTIME_INPUT_THIS_RUN`.

## Synology Docker read-only collect-all

A physical run must be started only by a separately current-admitted Track A runtime-validation task. The repository-side implementation task does not itself grant runtime access.

When the physical task has proven the intended unique exact client and read-only observation is permitted, Surveyor verifies only the declared Track A runtime namespace. It does not enumerate the Docker host or execute discovery commands in unrelated containers.

```bash
PYTHONPATH=. python3 -m tools.tibia_re_surveyor \
  --collect-all \
  --runtime-docker \
  --runtime-container otclient-track-a-kasmvnc \
  --control-container otclient-synology-runner \
  --display :1 \
  --output-dir /tmp/tibia-re-survey
```

The collect-all path itself sends no keyboard/mouse/gameplay input, does not log in, does not attach/inject a helper, does not write process memory and does not perform an item/economic/network action. If no current reviewed typed reader exists, the result remains `UNKNOWN`/`UNAVAILABLE`.

## No input or anti-idle path

This accepted Surveyor v2 surface contains no keyboard/mouse/gameplay or anti-idle command path. The stale #592 keepalive prototype is intentionally not promoted by this successor because the current collect-all task has `runtime_access:none` and no current owner authorization to add anti-idle mutation. A future anti-idle feature, if ever required, must be introduced by a separate explicitly authorized task and current Track A mutation gates.
