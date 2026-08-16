# OTC-20260816 — user-supplied Tibia Linux launcher archive

```yaml
evidence_date: 2026-08-16
repository: blakinio/otclient
task: OTC-20260816-track-a-worldmap-extent-static-re
pr: 367
source_class: USER_SUPPLIED_PLUS_OFFICIAL_SOURCE_REPRODUCTION
runtime_used: false
client_executed: false
client_bytes_modified: false
```

## User-supplied file fence

The owner supplied `tibia.x64.tar.gz` directly to the research session.

```yaml
file_name: tibia.x64.tar.gz
size_bytes: 29477141
sha256: 04a87c801d3855f4da1b07e201dff1f79acc8528c57c984131c3a2a88cb60ea7
```

Local inspection establishes that this archive is the Linux **launcher/updater distribution**, not the previously fenced installed game-client ELF. In particular, its top-level executable `Tibia/Tibia` is a launcher binary and is not the exact installed client ELF with the task fence `size=51965216`, `sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

## Repository artifact

A one-shot GitHub Actions transfer reproduced the owner-supplied archive from the official CipSoft Linux download source and refused to upload unless both the size and SHA-256 matched the owner-supplied file exactly.

```yaml
workflow_run: 31949840853
workflow_head: 1de1066af94c6d159ee8d40fdeb1c255b2f489a9
workflow_conclusion: success
runner: synology-otclient-01
operation: download_fence_and_archive_only
source_url: https://static.tibia.com/download/tibia.x64.tar.gz
expected_size: 29477141
expected_sha256: 04a87c801d3855f4da1b07e201dff1f79acc8528c57c984131c3a2a88cb60ea7
artifact_id: 9264329820
artifact_name: tibia-x64-launcher-user-upload-04a87c80
artifact_archive_size_bytes: 29477287
artifact_digest: sha256:d743d7db83bf4638cc322c7e48a1d4792b53e8d4d871e9bf55094c0399b3cb3f
artifact_expires_at: 2026-11-14T13:26:57Z
```

The artifact ZIP was downloaded back from GitHub and its contained `tibia.x64.tar.gz` was compared with the original owner upload:

```yaml
returned_inner_size: 29477141
returned_inner_sha256: 04a87c801d3855f4da1b07e201dff1f79acc8528c57c984131c3a2a88cb60ea7
cmp_result: BIT_IDENTICAL
```

Therefore the GitHub artifact contains the exact bytes supplied by the owner.

## Scope/provenance note

This operation used the Synology runner solely as a bounded byte-transfer endpoint because the connected GitHub API cannot accept a 29.5 MB local binary file parameter. No Tibia process was launched, no runtime session/display/PID was touched, and no static RE was executed on Synology as part of this transfer. The existing rule against using Synology as a static-analysis fallback remains unchanged.

The binary itself is intentionally kept out of public Git history; the repository stores this evidence index while GitHub Actions stores the exact archive as the bounded artifact above.
