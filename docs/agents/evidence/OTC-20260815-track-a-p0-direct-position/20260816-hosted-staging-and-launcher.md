# 2026-08-16 — P0 hosted staging and owner-supplied launcher evidence

## Scope

This checkpoint records input/provenance and static-routing evidence for exact P0 direct-position research. It does not promote a direct player-position member and does not use the Synology physical runtime.

## Exact research fence

```yaml
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

## Owner-supplied current Linux download — FACT

The repository owner supplied the current official Linux download archive. It was inspected statically outside Git and was not committed or uploaded to GitHub.

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

Static launcher evidence includes:

```text
package.json
partial.package.json.version
launcherConfiguration
launcherConfiguration=https://static.tibia.com/launcher/tibiametadata.json
cdnDiagnosticsTrace=https://static.tibia.com/cdn-cgi/trace
QNetworkAccessManager::get
QHostInfo::fromName
QNetworkRequest::setRawHeader
QNetworkRequest::setPeerVerifyName
Host
```

No launcher executable was run. No Service Agreement was accepted programmatically. No credentials, login, client session or gameplay action was used.

## Hosted retrieval attempt A — FACT

```yaml
head: d0b56ce562eb3ef6e59c1635687204917553dd32
workflow_run: 31947502633
job: 95165743019
strategy: top_level_archive_browser_user_agent_plus_same_url_referer
execution_class: github_hosted
runtime_access: none
result: INPUT_BLOCKED
http_result: 403
sanitized_artifact: 9263704543
proprietary_input_cleanup: PASS
```

Exact-client analysis did not run.

## Hosted retrieval attempt B — FACT

```yaml
head: 4d93050f5ee3a9d1ba1b8d3b326c1f8b0ff6c4c0
workflow_run: 31948000086
job: 95166976133
strategy: launcher_package_feed_package_json_version
resource: https://static.tibia.com/launcher/tibiaclient-linux-current/package.json.version
execution_class: github_hosted
runtime_access: none
result: INPUT_BLOCKED
http_result: 403
sanitized_artifact: 9263837982
proprietary_input_cleanup: PASS
```

The manifest and packed `bin/client` were never obtained.

## Hosted retrieval attempt C — FACT

The third and final evidence-based staging repair mirrored the launcher networking model more closely and tested both ordinary DNS routing and a bounded direct-IP fallback while retaining correct TLS SNI/Host identity.

```yaml
head: 5b581a6a64edb9c05143a855dbfd1cb2fffea316
workflow_run: 31948567275
job: 95168377109
strategy: launcher_equivalent_no_custom_user_agent_plus_resolved_ipv4_fallback
resource: https://static.tibia.com/launcher/tibiaclient-linux-current/package.json.version
domain_request: HTTP_403
resolved_ipv4_count: 2
resolved_ipv4_request_1: HTTP_403
resolved_ipv4_request_2: HTTP_403
result: INPUT_BLOCKED
sanitized_artifact: 9263987119
proprietary_input_cleanup: PASS
```

No exact client bytes were received. Per the Track A anti-stall repair limit, hosted staging repair cycles are now exhausted; a fourth HTTP-bypass hypothesis is not authorized without materially new evidence.

## Hardened dormant staging harness — FACT

The P0 workflow is GitHub-hosted only and fail-closed. It requires exact version, one `localfile == bin/client` manifest entry, packed and unpacked manifest hashes/sizes, and then the independent exact P0 size/SHA fence. It supports a normal LZMA stream and a historical 32-byte-prefixed LZMA form only when all manifest and exact-fence checks pass. Temporary package/client bytes are removed before artifact upload.

A prior coherent harness head `41396384650c329dab7fc159867a8ffb2afa2e35` passed Track A governance run `31948197816` and repository CI run `31948197910`. Later staging variants changed only the bounded retrieval strategy and retained the same no-runtime/exact-fence/cleanup boundary.

## Existing sanitized artifact search — FACT

The task also attempted to avoid new proprietary staging by searching retained sanitized Track A artifacts and exact-client logs for the missing instruction window. Directly inspected material included:

- P0 static artifacts `9246756211` and `9248797952`;
- `track-a-login-envelope-static-provenance` artifact `9233690471`;
- `track-a-login-origin-write-xrefs` artifact `9228921041`;
- `track-a-tcp-member-rtti` artifact `9231716774`;
- `track-a-outgoing-payload-consumers` artifact `9225203231`;
- `track-a-login-signal-oracle` artifact `9225585838`;
- `track-a-persistent-provenance-dump` artifact `9227370490`, including its >2 MB GDB log and map strips;
- runtime parent-GDB reacquisition artifact `9252114795`.

Search targets included `0x8367c1`, `0x8367c2`, `playerPosition`, `TPlayerData`, `0x843e20`, `0x843f60`, `0xd1cbd0`, `0xd2ac70` and `0xd2ef30`. Only the already-known P0 artifacts contain the player-position anchors; none contains a successful disassembly window for `0x8367c1` or a direct player-position member/accessor proof.

The full successful P0 job log for run `31892019505` independently confirms the exact `playerPosition` xrefs and TPlayerData vtable targets, but the bounded GDB disassembly commands failed because the retained task-local GDB could not load `libpython3.12.so.1.0`; no instruction body was preserved.

## Historical exact-package provenance — FACT

Closed historical RUNTIME PR #303 is not current runtime authority, but its durable source is evidence that prior exact-client tasks copied from this SHA-fenced source package path after `verify_client`:

```text
/home/runner/_work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia
```

That fact does not authorize P0 to execute static RE on Synology. The current hybrid routing contract explicitly requires coordinator-selected compliant evidence staging when deterministic analysis depends on host-local retained material.

## Public-source check — FACT

The public `dudantas/tibia-client` source already used elsewhere by this repository currently exposes `15.25.0a00a0`; exact release tag `15.32.df7b29` is absent. Public web/GitHub searches for the exact SHA, exact version token and `0x8367c1` produced no usable exact-client source or disassembly. No different-version binary was substituted.

## Classification

### FACT

- the owner-supplied current Linux file is launcher-only and contains no game `bin/client`;
- three materially distinct GitHub-hosted/no-runtime staging strategies fail with HTTP 403 before exact client bytes are available;
- the staging repair-cycle limit is exhausted;
- no proprietary client bytes were uploaded to GitHub by these attempts;
- retained sanitized artifacts/logs do not contain the missing successful instruction window at `0x8367c1`;
- exact historical source-package provenance exists on Synology, but P0 has no authority to use it as static fallback;
- RUNTIME remains independently responsible for physical semantic confirmation.

### UNKNOWN / INCONCLUSIVE

- direct player XYZ backing member/accessor;
- owning function and instruction semantics around `0x8367c1`;
- live discrimination from viewport/map/camera copies;
- restart/relogin stability of any future direct read.

## Exact unblockers

One of these must occur before P0 can materially advance:

1. coordinator-approved compliant evidence staging of the exact fenced `bin/client` or a sufficiently narrow derived instruction window, without committing proprietary bytes; or
2. the owner supplies the exact installed `packages/Tibia/bin/client`, which must first match size `51965216` and SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`; or
3. RUNTIME supplies durable causal player-position evidence after canonical runtime admission becomes legal.
