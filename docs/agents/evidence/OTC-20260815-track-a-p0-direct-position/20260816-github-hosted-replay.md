# 2026-08-16 — P0 direct-position GitHub-hosted replay

## Scope

This checkpoint refreshes the P0 direct-player-position lane under the current Track A routing rule: P0 is GitHub-hosted/static by default with `runtime_access: none`; physical client/session evidence is produced by the serialized RUNTIME lane and consumed here read-only.

No Synology job, client process, X11/VNC surface, login/session, process memory, input, network traffic, proprietary client bytes, credentials, Codex, OpenAI API or owner-funded paid AI quota were used by this replay.

## Live repository state at replay

```yaml
repository: blakinio/otclient
main: ce9997304e4b771b6243395bf0c3a6084f32a7dc
p0_pr: 302
p0_head_before_replay: 6f838d1089968d216e506cd272e7b98680da9fc8
p0_disposition: WAITING_ON_RUNTIME_PREREQUISITE
runtime_pr: 358
runtime_head: d78e42b955c27ee07fba783f5496588f34d29461
runtime_canonical_registration: ABSENT
runtime_bootstrap: REQUIRED_UNIMPLEMENTED
runtime_target_uniqueness: UNKNOWN
runtime_mutation_authorized: false
runtime_infra_pr: 360
runtime_infra_head: 1d64fab66650b1fcd58388ff5cf6f9a77a392dc4
runtime_infra_state: DRAFT_NOT_PROMOTED
legacy_runtime_pr_303: CLOSED_SUPERSEDED
```

The current RUNTIME Draft therefore does not provide a legal live exact-client observation window to P0. Historical `:98`, `6082`, PID/session and PR #303 surfaces remain non-authoritative.

## Existing exact-build sanitized artifact — FACT

The previously retained static artifact remains available from GitHub Actions:

```yaml
workflow_run: 31892019505
artifact_id: 9248797952
artifact_name: track-a-p0-static-elf-31892019505
artifact_digest: sha256:04835ab0bac7ffc43e161e8b2118c90a3d2197f7011385a6758cd7706c93a584
run_head: a3068a6a9460525cb1946186cf439caf7832e176
exact_client_version: 15.32.df7b29
exact_client_size: 51965216
exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Inspection of the sanitized text proves the previously recorded structural anchors:

```text
playerPosition literal: 0x1cdde3f
bounded RIP-relative code site: 0x8367c1 -> 0x1cdde3f
TWorldMapRenderProvider RTTI relocation: 0x3089b78 -> 0x1cddd20
TWorldMapViewport RTTI relocation:       0x308b598 -> 0x1ce1b60
IPlayerDataProvider RTTI relocation:     0x308b5b0 -> 0x1ce1ba0
TPlayerData RTTI relocation:             0x308b5c0 -> 0x1ce1bd0
TPlayerData primary vptr:                0x308ca70
```

The same artifact does **not** contain a successful instruction window for the load-bearing `0x8367c1` site. `player-position-disasm.txt` records `TRACK_A_P0_GRAPH_DISASM_COMMAND_FAILED` for `0x8367c1` and every attempted bounded target because the task-local GDB invocation could not load its runtime dependency. The sanitized artifact also omits proprietary client machine-code bytes, so this replay cannot reconstruct the failed instruction window from the artifact alone.

## GitHub-hosted exact-binary input boundary — FACT

Current P2 Draft PR #310 independently exercised the current Track A hosted-only exact-client staging path. Its two compliant GitHub-hosted attempts ended in DNS failure for `download.tibia.com` and HTTP 403 from `static.tibia.com`, and it is now `BLOCKED_INPUT_STAGING`. Its durable blocker is the absence of a legally and technically compliant GitHub-hosted-readable staging source for this exact fenced native-Linux client, with no Synology static fallback.

P0 shares that exact binary fence. Therefore a fresh hosted disassembly around `0x8367c1` cannot currently be produced without first resolving the same staging dependency.

## Classification

### FACT

- the exact client identity and existing structural P0 anchors above remain reproducible from the retained sanitized artifact;
- the retained artifact has no successful disassembly for `0x8367c1`;
- current RUNTIME #358 has no authoritative canonical client registration and no mutation authority;
- current GitHub-hosted exact-client staging is blocked by the same input problem already demonstrated in #310;
- no current live player-position claim is authorized.

### UNKNOWN / INCONCLUSIVE

- direct authoritative player XYZ member/accessor offset;
- instruction semantics and owning function around `0x8367c1`;
- discrimination against map/camera/viewport/copy candidates by live semantics;
- repeatability and fresh PID/relogin stability;
- direct comparison against current structural world evidence.

## Next action

After a coordinator-approved, legally and technically compliant GitHub-hosted-readable staging source for the exact fenced client exists, run one bounded hosted static analysis around `0x8367c1` (and only structurally justified `TPlayerData` / `IPlayerDataProvider` neighbors) to recover accessor/member candidates. Any physical semantic confirmation must be supplied separately by RUNTIME and consumed here as durable evidence; P0 must not take over the canonical desktop/session.
