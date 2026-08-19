# Track A current-client fence provenance

Date: 2026-08-19
Task: `OTC-20260819-track-a-current-client-fence-advance`
Base: `main@82e5f435c3aa4172115bf7f6a0cd7a5cc6da3d50`

## FACT — direct current public-package verification

A fresh non-secret fetch of the official current Linux package was performed on Synology. The package was decoded with its 45-byte wrapper plus raw LZMA1 stream. The temporary executable was not committed, uploaded or retained.

```yaml
http_status: 200
last_modified: Tue, 18 Aug 2026 08:22:05 GMT
packed_size: 10214529
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08c8dbb32be2840e9755
unpacked_size: 52109920
unpacked_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
embedded_version_token: '15.32'
raw_client_retained: false
```

The unpacked size/SHA is identical to the single live Kasm client fenced by PR #550 and to the independently audited current-package identity recorded by PR #544.

## Decision boundary

The current runtime identity fence advances to `15.32 / 52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`. SHA+size are the exact executable identity; `15.32` is only a bounded embedded version-family token.

The prior `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe` build becomes `SUPERSEDED_FOR_CURRENT_RUNTIME_IDENTITY` while remaining valid historical evidence wherever explicitly fenced. No address, offset, QMeta/vptr assumption, serializer, helper binary or `tibia-15.32.df7b29.json` profile is promoted to the new binary.

## Non-effects

```yaml
login_authority_added: false
credential_authority_added: false
gui_input_authority_added: false
gameplay_authority_added: false
transaction_authority_added: false
process_control_authority_added: false
current_task_runtime_access: none
proprietary_binary_committed_or_uploaded: false
```
