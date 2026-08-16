# 2026-08-16 — P0 hosted staging and owner-supplied launcher evidence

## Scope

This checkpoint records only input/provenance and static-routing evidence for the exact P0 direct-position task. It does not promote a direct player-position member and does not use the Synology physical runtime.

## Exact research fence

```yaml
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

## Owner-supplied current Linux download — FACT

The repository owner supplied the file downloaded from the current official Linux download flow. It was inspected statically outside Git and was not committed or uploaded to GitHub.

```yaml
archive_size: 29477141
archive_sha256: 04a87c801d3855f4da1b07e201dff1f79acc8528c57c984131c3a2a88cb60ea7
bin_client_entries: 0
launcher_member: Tibia/Tibia
launcher_size: 1460808
launcher_sha256: a5fc6e8ee8246868263c438539a54ea045bd048a1bea45f968fc2f498b682ca0
launcher_type: ELF64_x86_64_PIE_stripped
```

The archive is therefore a launcher/bootstrap bundle, not the installed game package containing `packages/Tibia/bin/client` or `bin/client`.

Static strings in the launcher include:

```text
package.json
partial.package.json.version
launcherConfiguration
launcherConfiguration=https://static.tibia.com/launcher/tibiametadata.json
cdnDiagnosticsTrace=https://static.tibia.com/cdn-cgi/trace
```

No launcher executable was run. No Service Agreement was accepted programmatically. No credentials, login, client session or network/gameplay action was used.

## Hosted retrieval attempt A — FACT

P0 replaced its stale Synology static workflow with an `ubuntu-latest`, `runtime_access: none` job and tested one materially different request hypothesis after P2's User-Agent-only HTTP 403: browser-like User-Agent plus same-URL Referer against the official Linux archive.

```yaml
head: d0b56ce562eb3ef6e59c1635687204917553dd32
workflow_run: 31947502633
job: 95165743019
execution_class: github_hosted
runtime_access: none
result: INPUT_BLOCKED
http_result: 403
sanitized_artifact: 9263704543
proprietary_input_cleanup: PASS
```

The analysis step did not run because exact client materialization failed.

## Hosted retrieval attempt B — FACT

A second distinct strategy avoided the top-level archive and targeted the launcher package feed directly. It attempted only:

```text
https://static.tibia.com/launcher/tibiaclient-linux-current/package.json.version
```

with the intent to read `package.json`, select the single `localfile == bin/client` entry, fetch only that packed file, verify manifest hashes/sizes, and then verify the exact P0 fence before any disassembly.

```yaml
head: 4d93050f5ee3a9d1ba1b8d3b326c1f8b0ff6c4c0
workflow_run: 31948000086
job: 95166976133
execution_class: github_hosted
runtime_access: none
result: INPUT_BLOCKED
http_result: 403
failed_resource: package.json.version
sanitized_artifact: 9263837982
proprietary_input_cleanup: PASS
```

The manifest and `bin/client` packed file were never obtained; semantic/static analysis did not run.

## Hardened dormant staging harness — FACT

Current P0 workflow head after the two semantic staging attempts includes a fail-closed hosted harness that:

1. requires `ubuntu-latest` / `RUNNER_ENVIRONMENT=github-hosted`;
2. requires `runtime_access: none` and never targets Synology;
3. reads `package.json.version` and requires exact version `15.32.df7b29`;
4. reads `package.json` and requires exactly one `localfile == bin/client` record;
5. verifies packed hash/size before decoding;
6. supports both a normal LZMA stream and a 32-byte-prefixed LZMA stream, but accepts neither unless manifest unpacked hash/size match;
7. additionally requires the exact research size/SHA above;
8. deletes the package manifest, packed client and decoded client before any artifact upload;
9. uploads only sanitized derived text evidence.

The task checkpoint path is no longer a trigger for this workflow, preventing documentation-only updates from repeating a blocked external request.

## Public mirror check — FACT

The public `dudantas/tibia-client` source already used elsewhere by this repository was checked as a possible non-CipSoft staging source. Its current visible package version is `15.25.0a00a0`; an exact release tag `15.32.df7b29` was not present. It is therefore not an exact-fence source and was not substituted.

## Classification

### FACT

- the owner-supplied current Linux file is launcher-only and contains no game `bin/client`;
- two distinct GitHub-hosted/no-runtime retrieval strategies against the official current distribution endpoints fail with HTTP 403 before exact client bytes are available;
- no proprietary client bytes were uploaded to GitHub by these attempts;
- the existing retained sanitized artifact `9248797952` still lacks the successful instruction window needed at `0x8367c1`;
- RUNTIME remains independently responsible for physical semantic confirmation.

### UNKNOWN / INCONCLUSIVE

- direct player XYZ backing member/accessor;
- owning function and instruction semantics around `0x8367c1`;
- live discrimination from viewport/map/camera copies;
- restart/relogin stability of any future direct read.

## Exact unblockers

At least one of the following must occur before P0 can advance materially:

1. coordinator-approved GitHub-hosted-readable staging of the exact fenced `bin/client`, without committing proprietary bytes; or
2. RUNTIME supplies durable causal player-position evidence after canonical runtime admission becomes legal.

A manually supplied exact installed `packages/Tibia/bin/client` may be used to verify identity/provenance and to design a compliant staging strategy, but it must not be committed or uploaded as a normal repository artifact.
