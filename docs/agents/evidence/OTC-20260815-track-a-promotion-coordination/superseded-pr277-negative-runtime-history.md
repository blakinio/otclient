# Track A superseded runtime handover — retained negative history from PR #277

Source PR: `#277`
Disposition: `REJECT/SUPERSEDE` as an active continuation handover
Reason: its continuation path depends on historical Oteryn repository/runtime state, which current `docs/agents/TIBIA_RESEARCH_TRACKS.md` forbids as an active Track A dependency.

This extract preserves only still-useful negative/history identifiers so closing the stale PR does not erase evidence.

## Exact-build facts retained only as historical provenance

The handover used official Linux client mapping `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe` and recorded the already-promoted Worldmap handler/common-routine boundary. Current build-specific use still requires the current Track A exact-client fence and repository-owned evidence.

## Historical world-entry failures retained

These runs reached or exercised historical login/character-selection states but did **not** prove a game-world session:

```text
31612091815 / 94165700952
31612594076 / 94167418903
31613139300 / 94169246915
31614553971 / 94173984093
31615871684 / 94178400132
```

Historical geometry diagnostic:

```text
31614383785 / 94173414953
first-row geometry near y=196
```

Historical proxy/WARP diagnostic:

```text
31613249273 / 94169615390
```

Hosted-runner official-client download attempts retained as negative evidence:

```text
31617541307
31617769586
result: HTTP 403 even after changing egress; do not brute-force or weaken transport controls
```

## Negative conclusions retained

- Kernel `/dev/net/tun` WARP was not viable in the historical Synology/Docker environment; userspace WARP/SOCKS was the working transport approach.
- Correcting character-row geometry did not by itself solve world entry.
- Socket/pixel/window changes were insufficient semantic `IN_GAME` evidence.
- Historical proxy/WARP diagnostics did not support treating the tunnel as the root cause.
- Historical Vulkan-related failures remained a candidate lead, not a proven current root cause.

## Superseded continuation instructions

Do **not** follow PR #277 instructions to inspect or continue through `blakinio/Oteryn-Platform`, Oteryn branches, Oteryn runners or Oteryn containers. Current Track A recovery is repository-only in `blakinio/otclient`; missing facts are UNKNOWN and must be revalidated within the current Track A task/runtime namespace.

Current bounded login/recovery procedure is retained separately in `accepted-historical-login-procedure.md`; active restart/relogin validation belongs to task `OTC-20260815-track-a-runtime-reacquisition` / PR #303.
