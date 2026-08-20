# TIBIA-RE Surveyor

`tools/tibia_re_surveyor` is a deterministic evidence/indexing harness for the official native-Linux Track A programme. It reduces repeated agent census work without changing the repository's evidence standards.

## What v1 does

- parses the canonical 169-row coverage matrix and validates its declared counts;
- joins current row titles from the detailed checklist;
- indexes bounded text evidence references and whether each reference contains the current exact-client SHA;
- captures a secret-free Docker/KasmVNC runtime identity, X11-window and canonical-control-plane snapshot when requested;
- ranks unresolved rows from the canonical dependency matrix rather than inventing new semantic conclusions;
- emits `coverage.json`, `agent_bundle.json` and `summary.md` for the next agent.

Evidence mention counts are discovery aids only. The Surveyor never converts static presence, a filename match or a diagnostic observation into a canonical `DONE` status.

## Anti-idle contract

The keepalive implementation reuses the existing Track A campaign contract:

- heartbeat: `/tmp/otclient-track-a-last-activity`;
- GUI input lock: `/tmp/otclient-track-a-gui-input.lock`;
- trigger: 8 minutes by default, keeping intended inactivity below 10 minutes;
- preferred stimulus: one turn in place;
- keepalive events always carry `semantic_evidence=false`.

The default turn modifier is `ctrl`, matching the official Tibia guide's default `Ctrl + cursor key` turn control. Tibia allows the turn modifier to be customized, so `--turn-modifier shift|alt` is available when the admitted runtime configuration requires it.

The keepalive path is deliberately fail-closed. `--keepalive` alone grants no input authority. A positive input path additionally requires an external JSON admission record stating current `canonical_reuse_or_mutation`, Gate A/Gate B, required rebind state, exact target uniqueness, GUI/mutation authority and whole-lifetime supervisor status. The Surveyor then independently checks the current registration, lease generation/expiry, exact process identity, fence, display and `IN_GAME` registration state before attempting the shared lock.

An authority JSON file is evidence input, not a replacement for the repository's canonical guard/supervisor. The caller remains responsible for executing an authorized mutation through the trusted Track A whole-lifetime supervision path.

## Local repository-only run

```bash
PYTHONPATH=. python3 -m tools.tibia_re_surveyor \
  --output-dir /tmp/tibia-re-survey
```

## Synology Docker read-only run

Run from the Docker host so the harness can inspect both the repository runner container and the persistent KasmVNC container. With no valid mutation authority, the expected keepalive result is `KEEPALIVE_SKIPPED_UNAUTHORIZED`; no keyboard or mouse input is sent.
