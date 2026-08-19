# Existing unregistered runtime adoption — implementation/evaluation

Task: `OTC-20260819-track-a-existing-runtime-adoption`
PR: #596

## Expected behavior

- registration absent + current lease/flock + one exact Kasm client + stable repeated proof -> atomically create schema-v1 registration generation 1;
- adoption probe inventories every running Docker container, rejects any official-looking mismatched candidate and requires exactly one exact target;
- target proof contains boot hash, PID, process-start ticks, exact size/SHA, display, X11 window owner/class and a hash rather than the character-bearing window title;
- title shape is never gameplay proof: `IN_GAME` requires exact-peer bridge `PING` plus exactly one validated player-protocol, game-session and worldmap handler; without that structural bridge the state remains `UNKNOWN`;
- adoption persists and later Gate B reproduces the Docker runtime locator, inventory scope/count/completeness and candidate fingerprint, preventing PID-only cross-container reinterpretation;
- the Kasm adoption probe does not read `/proc/<pid>/environ`; `:1` is the fixed target locator and actual X11 window ownership is proven directly;
- identity/uniqueness/lease/registration drift before commit -> no registration;
- failure after commit -> remove only the exact adoption-created registration;
- existing client receives no signal, restart, login, GUI input, attach or injection;
- bootstrap zero-client semantics and legacy owned-process-group manifests remain unchanged;
- rebind/Gate B accept the same reviewed external proof only after a registration exists.

## Forbidden behavior

- treating adoption as GUI/gameplay authorization;
- launching a second client because registration is absent;
- manual `runtime-registration.json` editing;
- adopting more than one or an unverifiable/mismatched candidate;
- persisting the raw character-bearing X11 title;
- deleting or overwriting a registration that changed concurrently;
- killing/stopping/signalling the pre-existing client on adoption failure.

## Evaluation matrix

| Case | Expected |
|---|---|
| one exact target, stable proof | PASS + registration |
| second exact target | fail closed |
| official-looking wrong SHA | fail closed |
| X11 PID mismatch | fail closed |
| character-style title but structural bridge absent | state `UNKNOWN`, never `IN_GAME` |
| bridge discriminator not exactly 3-of-3 | fail closed |
| adopted runtime locator changes before Gate B | fail closed |
| adoption manifest candidate_count=2 | fail closed |
| identity drift before commit | fail closed, no registration |
| identity drift after commit | fail closed, own registration rolled back |
| registration already exists | refuse before probe |
| legacy bootstrap tests | unchanged PASS |
| legacy rebind tests | unchanged PASS |

No live client operation is part of this implementation task. A later invocation based on merged trusted `main` is required before physical adoption or GUI input.

## Post-implementation falsification repair — 2026-08-19

A fresh local falsification pass found two material weaknesses in the first implementation candidate: the Kasm probe inferred `IN_GAME` from `Tibia - <character>` and the committed registration did not preserve the Docker runtime locator/fingerprint used to select the process. Both were repaired before publication.

Current repaired validation:

```text
canonical transition tests: 17/17 PASS
Kasm adoption probe tests: 6/6 PASS
Track A governance: PASS
Python compile: PASS
workflow YAML parse: PASS
git diff --check: PASS
```

No live mutation or registration write occurred during this implementation/audit repair. The separately observed current client was queried read-only only to establish that a structural 3-of-3 discriminator is technically available for a later authorized adoption invocation.
