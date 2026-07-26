# OTC-20260727 — Tibia Linux runner analysis

## Status

Active — one-off infrastructure analysis. Do not merge proprietary assets or installed client bytes.

## Purpose

Use the existing Synology self-hosted GitHub Actions runner to install the official Tibia Linux package in an isolated Docker container and produce a text-only static-analysis report for comparison with the Windows client and OTClient architecture.

## Owned paths

- `.github/workflows/tibia-linux-runner-analysis.yml`
- `docs/agents/tasks/active/OTC-20260727-tibia-linux-runner-analysis.md`

## Modules touched

- GitHub Actions infrastructure only
- No runtime client modules

## Reuses

- self-hosted runner label `oteryn-staging`
- host Docker socket exposed to the runner
- host staging-state root `/var/lib/oteryn-staging-state`

## Dependencies

- official CipSoft Linux launcher download
- outbound HTTPS and DNS from the Synology Docker host
- Docker-compatible x86-64 Synology host

## Safety boundaries

- run only inside a disposable Ubuntu container;
- persist downloaded/installed bytes only under `/var/lib/oteryn-staging-state/tibia-linux-analysis` on the NAS;
- do not commit or upload CipSoft binaries, assets, archives, credentials, cookies or session data;
- publish only text logs, hashes, ELF metadata, dependency lists and selected string indicators in workflow logs;
- do not touch Oteryn staging containers, ports, databases, volumes or secrets;
- do not log into a Tibia account or connect a character.

## Acceptance criteria

- runner job executes on `oteryn-synology-staging` / label `oteryn-staging`;
- official launcher archive is downloaded over HTTPS;
- launcher is executed under Xvfb with an isolated HOME;
- any installed package remains on the NAS under the dedicated state path;
- report identifies whether a separate game-client ELF was installed and records its hash, ELF metadata, dependencies and relevant BattlEye/protected/unprotected/login strings;
- no proprietary binary is uploaded to GitHub.

## Validation

Pending workflow run and log inspection.

## Next action

Add and trigger the one-off workflow, then inspect the exact runner job result and report.