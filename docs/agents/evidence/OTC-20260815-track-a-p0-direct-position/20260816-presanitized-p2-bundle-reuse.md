# P0 reuse of pre-sanitized exact-client P2 bundle — 2026-08-16

## Scope

GitHub-hosted, `runtime_access: none`. This check consumed only a retained sanitized GitHub Actions artifact; it did not obtain or upload the proprietary client binary, contact the physical Synology runtime, observe a process/display/network session, or perform gameplay input.

## Input provenance — FACT

Live PR #310 (`research(track-a): trace retained byte-container consumer`) identifies run `31904696996` / artifact `9252025461` as a pre-sanitized exact-binary evidence bundle suitable for GitHub-hosted reuse. The artifact metadata observed during this continuation was:

```yaml
artifact_id: 9252025461
name: track-a-p2-buffer-downstream-consumer-31904696996
expired: false
size_bytes: 11208
artifact_digest: sha256:2a866247558b079944d81c9ad33bd4c5361c8144a7f367b273ab3bc19a080991
source_head: 3138b94ebc477ee5075b458c16de72f620f49c67
```

The bundle's own `validation.log` and `result.txt` independently retain the exact client fence used by P0:

```text
CLIENT_SIZE=51965216
CLIENT_SHA256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

The retained evidence is sanitized disassembly/output only; no client/package bytes are present.

## Target-window search — FACT

The downloaded artifact contained exactly these evidence files:

```text
evidence.txt
validation.log
result.txt
result.json
```

A bounded content search for P0's load-bearing anchors found no matches for:

```text
0x8367c1
0x8367c2
playerPosition
TPlayerData
0x1cdde3f
```

Manual inspection confirms the artifact is intentionally scoped to the P2 network processor path. Its retained disassembly ranges include, among others:

```text
0x7dd630..0x7dd9a0
0xc2df80..0xc2e680
0xb47130..0xb47880
0xb56970..0xb56d60
```

and the connection edge around `0x19716a3`; none intersects the required P0 instruction window around `0x8367c1`.

## Classification

### PROVEN

- artifact `9252025461` is a current, non-expired, pre-sanitized exact-fence evidence source that P0 may consume without physical runtime access;
- its retained size/SHA fence matches P0's exact client (`51965216`, `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`);
- the artifact does not retain the `0x8367c1`/`playerPosition`/`TPlayerData` instruction evidence required to recover the direct-position member/accessor.

### UNKNOWN / INCONCLUSIVE

- direct standalone authoritative player XYZ member/accessor offset;
- owning function/instruction semantics around `0x8367c1`;
- discrimination against camera/map-origin/viewport/copy candidates;
- physical value correlation and fresh-PID/relogin stability.

## Current RUNTIME boundary — FACT

Current trusted-main task `docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md` remains blocked. Its v7 checkpoint records `canonical_registration: ABSENT`, `current_exact_client_pid: NOT_REGISTERED`, `current_exact_client_session: NOT_REGISTERED`, Gate B not reached, and no current mutation authorization. Therefore it has not yet produced the direct-position physical discriminator requested by P0.

## Disposition

This is materially new evidence compared with the prior P0 artifact-search checkpoint, but it does not satisfy the missing instruction-window gate. It also does not justify a fourth guessed HTTP retrieval attempt.

`P0-STATE` remains `WAITING / DRAFT_NOT_PROMOTED`.

Exact next action: consume a coordinator-approved sanitized exact-client bundle that actually includes the bounded `0x8367c1` instruction window, or obtain another compliant GitHub-hosted exact-client evidence source that can produce that window; physical direct-XYZ/world correlation and relogin confirmation remain exclusively RUNTIME-owned.
