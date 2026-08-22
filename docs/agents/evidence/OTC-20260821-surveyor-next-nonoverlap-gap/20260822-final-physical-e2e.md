# Final physical E2E — ui_settings_typed_reader

Task: `OTC-20260821-surveyor-next-nonoverlap-gap`  
Trusted code base: `main@4c5b3f216510b4f583b49779f0a22f1ba4f5b927` (merged repair PR #659)  
Date: 2026-08-22

## Fresh read-only admission

Before the final acceptance probe, the task admission was persisted on this closeout branch as `runtime_access: read_only` for exactly `synology:otclient-track-a-kasmvnc:display-1:client-646`.

Fresh control-plane metadata census found both canonical files absent:

- `runtime-registration.json`: ABSENT
- `lease.json`: ABSENT

The declared namespace contained exactly one target client and one matching visible Tibia window:

- PID: `646`
- process start ticks: `1394843`
- client size: `52109920`
- client SHA-256: `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`
- visible Tibia XID: `27262999`
- `_NET_WM_PID`: `646`
- `target_uniqueness`: `PROVEN`
- mutation authorized: `false`

No external runtime container census was used for target selection.

## Final exact-reader probe

The exact `STATIC_SETTINGS_PROBE` and `READ_ONLY_SETTINGS_PROBE` strings from trusted `tools/tibia_re_surveyor/ui_settings.py` were executed passively against the admitted client.

Static result:

```json
{"clientoptions_literal_count":1,"state":"AVAILABLE","type_name":"tibia::config::TClientOptions","type_string_count":2}
```

Read-only live result:

```json
{"filesystem_access":"read_only","master_volume":100,"master_volume_old":100,"persistence_relative_path":"conf/clientoptions.json","process_memory_access":"not_used","reader_id":"ui_settings_typed_reader","state":"AVAILABLE"}
```

This closes the earlier trusted-main failure `CLIENTOPTIONS_PARENT_OPEN_FAILED`. The repaired package-root/executable-dentry binding reaches the current exact package's `conf/clientoptions.json` and preserves the fail-closed no-follow/identity fences.

## Collect-all / privacy

A fresh repository-only `--collect-all` from the same trusted main snapshot was executed under Python 3.12.14 and reported:

```text
TIBIA_RE_SURVEYOR_ROWS=169
TIBIA_RE_SURVEYOR_COLLECT_ALL_ALIASES=12
TIBIA_RE_SURVEYOR_MISSING_READERS=7
PRIVACY=PASS
```

The generated `privacy-scan.json` contained an empty findings list and `result: PASS`.

The Synology host's system Python is 3.8 and cannot import the current Surveyor type aliases. Therefore the repo-only collect-all was executed in an existing read-only Python 3.12 environment, while the physical reader itself was executed directly and read-only against the admitted runtime. No production code was patched for interpreter compatibility.

## Safety / acceptance

```text
ui_settings_typed_reader=AVAILABLE
filesystem_access=read_only
process_memory_access=not_used
target_uniqueness=PROVEN
runtime_mutation=false
credential_access=false
gameplay_input=false
relogin=false
client_restart=false
transaction_or_economy_action=false
privacy=PASS
```

The owner had already logged the client into the world manually. The agent generated no gameplay input and did not perform login/relogin during this acceptance.

Task-level physical acceptance: **PASS**.
