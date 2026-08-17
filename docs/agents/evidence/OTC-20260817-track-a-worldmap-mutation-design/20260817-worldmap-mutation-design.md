# World-map extent mutation design evidence

Task: `OTC-20260817-track-a-worldmap-mutation-design`  
Draft PR: `#452`  
Evidence date: `2026-08-17`  
Execution class: `github_hosted`  
Runtime access: `none`

## Result

```yaml
STATIC_PATCH_GRAPH_READY: true
MUTATION_DESIGN_READY: true
OFFLINE_PATCH_PLAN_READY: true
SAFE_MUTATION_PROVEN: false
PHYSICAL_VALIDATION_CONTRACT_READY: true
PHYSICAL_VALIDATION_EXECUTION_AUTHORIZED: false
client_byte_mutation_authorized: false
client_executed_by_this_task: false
client_bytes_mutated_by_this_task: false
```

`MUTATION_DESIGN_READY=true` means an exact reversible experimental design exists. It does not mean that a larger world-map extent is safe, that a final target has been selected, or that this task may modify or execute the client.

## Exact source fence — FACT

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
elf_class: ELF64
elf_data: little_endian
elf_machine: x86_64
```

This task consumed the coordinator-accepted graph promoted through #367 and producers #437/#446. It did not reacquire, execute, mutate or upload the raw client.

## Frozen mutation anchor — FACT

```yaml
shared_literal_va: 0x01cdd958
preimage_guard_16_hex: 120000000e0000000800000006000000
preimage_dwords_le: [18, 14, 8, 6]
patchable_prefix_length: 8
patchable_pair_le: [18, 14]
trailing_guard_pair_le: [8, 6]
```

Accepted propagation graph:

```text
0x01cdd958 packed 18/14
  -> exact TWorldmapProtocolMessageHandler constructor 0x00803ab0
  -> 0x00803d8b Handler+0xb0/+0xb4
  -> 0x00bc6350 geometry snapshot +0x38
  -> Handler+0x10 exact TWorldMapStorage virtual dispatch
  -> TWorldMapStorage slot 12 0x00cc6cd0
  -> 0x00cc6d2c Storage+0x48/+0x4c
```

The same literal independently initializes `TWorldMapViewport+0x40/+0x44` in constructor `0x00cbf680`. Exact setter `0x00cb2220` later recomputes Viewport geometry from pixel dimensions divided by 32 plus margins; recompute `0x00cbf700` uses a separate `15/11` base pair plus margins. Therefore persistent Viewport equality with the patched constructor literal is not a valid success requirement.

## ELF VA -> file-offset mapping — FACT / design decision

The accepted producer implementation used this mapping:

```text
for each PT_LOAD:
  if p_vaddr <= VA and VA+size <= p_vaddr+p_filesz:
      file_offset = p_offset + (VA - p_vaddr)
```

Historical source implementation: `.github/scripts/tibia-official-client-re-worldmap-exact-static-evidence.py` in the producer source lineage. `Elf64.vaddr_to_offset()` and `bytes_at()` recovered exact virtual-address bytes without assuming VA equals file offset.

Independent retained exact-client run `31892019505`, artifact `9248797952`, is fenced to the same exact SHA/size and records nearby mappings such as:

```text
file_offset=0x1cddd20 vaddr=0x1cddd20 text=N5tibia8worldmap23TWorldMapRenderProviderE
file_offset=0x1cdde3f vaddr=0x1cdde3f text=playerPosition
```

Those are corroboration only. This design deliberately does not hardcode target file offset `0x01cdd958` from proximity.

A future executor must parse the fenced file's own program headers and require exactly one file-backed `PT_LOAD` containing all 16 guard bytes at VA `0x01cdd958`. No matching segment, more than one eligible segment, out-of-file range, wrong ELF format/machine, or parser contradiction means `REFUSED`.

## Exact offline patch algorithm — DESIGN READY

The future executor operates on a task-owned copy; in-place modification of the canonical installed source is forbidden.

1. Open the source read-only; require a regular file and reject symlink ambiguity.
2. Require exact size `51965216` and SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
3. Require ELF64 little-endian x86-64 and parse `PT_LOAD` headers.
4. Derive the unique file offset for VA `0x01cdd958` using the exact mapping above.
5. Require exact 16-byte guard `120000000e0000000800000006000000` at that offset.
6. Require one exact candidate pair declared by the future authorized task. As a conservative encoding constraint, reject either component outside `1..0x7fffffff`; this avoids introducing the signed high bit into downstream signed geometry operations and is not a claim that the full range is semantically safe.
7. Create a task-owned copy with restricted permissions; preserve the source unchanged.
8. Replace only the first 8 bytes with `struct.pack('<II', candidate_x, candidate_y)` and keep DWORDs `8,6` untouched.
9. Re-read the copy and require the complete 16-byte postimage to be `pack_le32(candidate_x) || pack_le32(candidate_y) || 08000000 || 06000000`.
10. Byte-compare the whole source and copy; require zero differences outside the derived 8-byte patch range.
11. Compute and persist the patched-copy SHA-256 and exact diff manifest before any execution.
12. Rollback is termination of any task-owned patched runtime, deletion of the patched copy, and re-hash of the untouched source to exact SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

## First causal discriminator — RECOMMENDATION, not final target

For the first physical experiment only:

```yaml
candidate_pair: [19, 14]
postimage_prefix_8_hex: 130000000e000000
actual_changed_bytes: 1
purpose: width_axis_plus_one_causal_canary
classification: RECOMMENDATION_NOT_FINAL_TARGET
```

Changing only `18 -> 19` changes one byte and one axis, minimizing the experimental delta. It does not prove that `19x14` is desirable or safe for routine use. A later independent height-axis canary `[18,15]` may be considered only after the width discriminator is safely closed. Historical candidates `26x20`, `32x24`, `36x28` remain unproven ideas.

## Why no second patch site is included

FACT:

- changing only Viewport geometry cannot prove Storage retains a larger live region;
- Handler's constructor default is upstream of the proven snapshot -> Storage path;
- Viewport is dynamically recomputed later;
- RenderProvider and Picker consume dynamic geometry through fixed-32 operations and no independent `18/14` cap was recovered;
- the RenderProvider `65535 x 10-byte` allocation has unknown semantic role;
- no direct Camera-field -> Storage/master-extent mutation edge was recovered in accepted bounded Camera neighborhoods.

SAFETY CONSEQUENCE: the first discriminator mutates only the shared literal prefix. An unexpected clamp/failure is evidence, not authorization to patch another site in the same run.

## Carried unknowns

```yaml
complete_post_constructor_Handler_b0_b4_writer_census: UNKNOWN
exact_source_member_names_and_units: UNKNOWN
network_or_parser_extent_ceiling: UNKNOWN
render_65535x10_semantic_worldmap_ceiling: UNKNOWN
named_camera_projection_or_indirect_coupling: UNKNOWN
safe_final_extent: UNKNOWN
safe_final_client_byte_mutation: NOT_PROVEN
```

These no longer prevent a bounded reversible canary design, but they prevent any `SAFE_MUTATION_PROVEN=true` or final-size claim.

## Physical-validation contract — CONTRACT READY / EXECUTION NOT AUTHORIZED

A patched copy has a different SHA and must never be represented as the exact registered canonical runtime. A future physical task must re-read then-current governance and establish fresh Track A authority. The natural experiment class is task-owned `ephemeral_isolated` native Linux with unique process/display/state namespace; this is a design recommendation, not authority granted by this file.

Any login/world-session use must additionally satisfy then-current one-session rules and explicit authority for that concrete live-session experiment. A second logged-in Track A Global session is not implied. If semantic proof requires an in-game session and that boundary cannot be proven, result is `BLOCKED`.

Required pre-launch record:

```yaml
source_exact_sha: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
source_exact_size: 51965216
patch_va: 0x01cdd958
patch_file_offset: freshly_derived_from_PT_LOAD
preimage_guard_16: exact
candidate_pair: explicitly_declared
patched_sha256: freshly_computed
full_file_diff_outside_patch_range: 0
runtime_namespace_uniqueness: PROVEN
competing_or_unverifiable_official_client_session: 0_or_execution_refused
client_byte_mutation_authorized: true_required_from_follow_on_authority
```

At design time coordinator promotion PR #448 is still open/draft; its raw XRes helper is therefore not trusted-main implementation. Historical XID/PID values remain non-authoritative.

For canary `[19,14]`, future structural proof should establish, in order:

1. spawned process executes the declared patched-copy path/inode/hash;
2. patched build retains the same static class anchors/file layout expected from the one-byte data change, with process addresses interpreted through the actual load base;
3. exact Handler `+0xb0/+0xb4` reflects `[19,14]` after construction and before any contradictory later write;
4. after the accepted snapshot/slot-12 propagation, exact `TWorldMapStorage` (`vptr 0x0308ce70` relative to the correct image base) `+0x48/+0x4c` reflects `[19,14]`;
5. later resets/clamps are recorded as discriminators, not patched around;
6. Viewport dynamic recomputation is recorded separately and is not failure by itself;
7. RenderProvider/Picker/Camera/runtime behavior has no material regression before any larger candidate is considered;
8. if separately authorized in-game semantics run, record whether width-axis retention/bounds behavior actually expands coherently;
9. terminate patched runtime, delete patched copy, and prove the untouched exact source SHA again.

`CAUSAL_PROPAGATION_PROVEN` requires direct patched-process identity plus Handler -> snapshot -> Storage propagation for the declared output hash. `SEMANTICALLY_VALIDATED` additionally requires separately authorized live behavior; structural propagation alone is insufficient.

## Abort conditions

Refuse or stop on: wrong fence; non-unique VA mapping; preimage mismatch; any byte delta outside the patch range; modification of the exact source; ambiguous patched-process identity; runtime ownership/namespace conflict; competing/unverifiable official-client session; startup/crash/disconnect/session anomaly; Handler canary absent; later writer overwrites before propagation; Storage canary absent; material RenderProvider/Picker/Camera regression; or missing current authority/admission.

No abort condition authorizes adding a second patch site in the same run.

## Final classification

```yaml
MUTATION_DESIGN_READY: true
SAFE_MUTATION_PROVEN: false
PHYSICAL_VALIDATION_CONTRACT_READY: true
PHYSICAL_VALIDATION_EXECUTION_AUTHORIZED: false
client_byte_mutation_authorized: false
final_target_extent: UNKNOWN
first_canary_recommendation: [19,14]
```

Next legitimate stage: separately admitted physical validation consuming this frozen design, not duplicate static discovery.
