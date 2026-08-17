# P0 direct player XYZ — same-session RUNTIME producer handoff v2

Task: `OTC-20260815-track-a-p0-direct-position`  
Consumer PR: #302  
Date: 2026-08-17

## Current trusted state

- current trusted `main` inspected by this continuation: `26c89a7d3b044acf88299f8d68eee4ac16b5d13c`;
- exact client: `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`;
- canonical X11/XRes identity mechanics are complete through merged #457/#461/#465 and must not be repeated;
- fresh canonical admission #482 (`32033237388 / 95397745114`) found lease generation `8` released and authoritative registration `ABSENT`;
- #486 archived/released that RUNTIME admission task;
- `DIRECT_PLAYER_XYZ=INCONCLUSIVE` remains unchanged.

## Strongest exact-build direct candidate

Static exact-client evidence supports the following bounded candidate on the `TPlayerData`-typed route:

```text
primary vptr offset: 0x308ca70
X: object + 0x78, signed i32
Y: object + 0x7c, signed i32
Z: object + 0x80, signed i32
property code site: 0x8367c1 -> playerPosition
```

This is a candidate only. A value match or one movement match is insufficient for promotion.

## New producer helper

P0 now carries a dedicated read-only runtime snapshot helper:

- path: `.github/scripts/tibia-official-client-re-p0-runtime-snapshot.py`;
- helper blob SHA: `afd8cd7023ad667421eddce71dbc1575770e0f32`;
- validation head: `74ee39fc0136142f2dd0b425a34e6e75fa38430e`;
- hosted validation run/job: `32035752607 / 95405675923 = SUCCESS`;
- deterministic tests cover signed-i32 decode, `/proc/PID/stat` start-ticks parsing, exact-vptr typed-object selection, direct offsets, invalid private-pointer rejection and explicit nonsemantic output;
- hosted safety gate rejects `os.pwrite`, `O_RDWR`, `O_WRONLY`, `process_vm_writev` and ptrace POKE surfaces and requires `/proc/PID/mem` to be opened `O_RDONLY` only.

The helper emits, per snapshot:

```text
snapshot_label
PID
process_start_ticks
boot_id_sha256
exact client SHA/size/path fence
main image base
runtime TPlayerData vptr
all relocation-backed typed TPlayerData object addresses
private-data pointer for each typed object
direct signed-i32 XYZ at +0x78/+0x7c/+0x80
wall_time_ns
monotonic_ns
process_memory_access=read_only
process_memory_writes=0
semantic_player_xyz_proven=false
```

It does not select an authoritative object by coordinate value and does not promote semantics.

## Independent RUNTIME provider opportunity

Active RUNTIME PR #475 currently owns a separate `ephemeral_isolated` exact-client experiment. P0 does **not** own or inspect that runtime directly.

Current checked state:

- task: `OTC-20260817-track-a-worldmap-server-delivery-causal-validation`;
- current head: `062cf9396480a6012278cd5e0068aee403bdcc47`;
- current workflow run/job: `32035179935 / 95404298697 = SUCCESS`;
- current job name: `CipSoft persistent-home metadata discriminator (no client)`;
- client executed in that current run: false;
- therefore no current `IN_GAME` lifecycle is available to P0 from #475 at this checkpoint.

The #475 task nevertheless has an independently owner-authorized future baseline login and a single reversible `Right -> Left` movement pair. If its own RUNTIME owner later reaches a legal exact-client `IN_GAME` lifecycle under its own then-current admission, the same owner may produce P0 evidence **without another login and without another movement stimulus**, provided the additional read-only capture is compatible with that task's authority and safety rules.

P0 must not write #475's branch, attach to its runtime, inject input, consume credentials or take over its namespace.

## Requested same-session P0 package

If a legally admitted RUNTIME owner accepts the handoff, capture three snapshots of the exact same PID/start identity:

1. `before` — immediately before the already-authorized adjacent movement;
2. `stepped` — after structural confirmation that the one adjacent step completed;
3. `restored` — after the inverse step returns to the original position.

For each snapshot run the validated helper with the same exact client, PID and `--vptr-offset 0x308ca70`. Do not use `--require-unique-typed-object` unless uniqueness has first been established; if multiple typed objects exist, preserve all of them and let causal correlation discriminate them.

The package must additionally preserve current exact PID/start/XRes ownership evidence and the RUNTIME owner's structural `IN_GAME` proof.

## Independent coordinate/control rule

P0 requires an independent structural world-coordinate reference at the same observation points. World-map-derived data is **not a P0 research target**. It may be used only as a structural coordinate/control after that evidence has independently reached canonical acceptance. If the provider's structural coordinate evidence is not yet canonical, preserve timestamps and raw sanitized coordinate records for later correlation but do not use them to promote P0.

## Required negative controls

Before `PROVEN`, the final package must also discriminate the direct candidate against:

- camera position/origin;
- viewport origin/center;
- map origin/center;
- stale or last-movement copies.

If those controls are unavailable in the same legal lifecycle, the result remains `INCONCLUSIVE` even if `+0x78/+0x7c/+0x80` follows the movement delta.

## Promotion rule

`DIRECT_PLAYER_XYZ=PROVEN` is legal only when all of the following are jointly established:

- exact current PID/start identity and X11/XRes ownership;
- structural `IN_GAME`;
- at least two observations plus known delta and inverse restoration;
- independent structural coordinate agreement;
- exact typed-object identity and stable locator for the winning candidate;
- rejection of camera/viewport/map-origin/stale-copy alternatives;
- repeatability within the available lifecycle and fresh PID/relogin stability when that lifecycle already includes it.

Until then:

```text
DIRECT_PLAYER_XYZ=INCONCLUSIVE
```
