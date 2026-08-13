# Tibia Global Login Lab

Isolated runtime project for investigating whether this OTClient fork can authenticate to and enter the official Tibia service.

## Execution target

All runtime work is executed on the dedicated GitHub self-hosted runner:

```text
[self-hosted, otclient, synology]
runner name: synology-otclient-01
```

The repository source is transient GitHub Actions checkout data. Persistent lab state lives under:

```text
${RUNNER_WORKSPACE}/_otclient-labs/tibia-global-login
```

The bootstrap creates a lab-owned container named:

```text
otclient-tibia-global-login-lab
```

with labels identifying `blakinio/otclient` and task `OTC-20260813-tibia-global-login-lab`.

## Scope

The lab is intended to progress through these evidence gates:

1. deterministic runner and Docker preflight;
2. isolated OTClient runtime/container bootstrap;
3. current official-client version/asset metadata discovery without committing proprietary material;
4. HTTP login compatibility analysis;
5. character-list/session handoff analysis;
6. game-server connection and protocol handshake analysis;
7. proof of `GAME_START` or an exact, evidence-backed compatibility boundary.

Each gate must emit only non-secret structural markers. A successful HTTP response alone is not proof of game entry.

## Credential boundary

The canonical Track B workflow is authorized to consume the existing GitHub Actions test-account secrets only for its bounded HTTP preflight and controlled game-entry probe. The values remain inside the workflow/container's transient secret path and must never be committed, printed, uploaded, or reused by local scripts. Session keys, cookies and account/character data remain prohibited from repository persistence.

## Proprietary data boundary

Official Tibia binaries/assets may be fetched only transiently at runtime when a later bounded experiment requires them and licensing/security rules permit it. They are never committed to this repository or uploaded as CI artifacts.

## Non-OCR proof

OCR/Tesseract is not part of the login/world-entry proof path. Proof should come from OTClient events, protocol/runtime state, deterministic logs and network/process evidence.

## Bootstrap

The workflow `.github/workflows/tibia-global-login-lab.yml` runs `scripts/bootstrap.sh`. The bootstrap is deliberately idempotent and touches only the lab-owned state/container namespace.
