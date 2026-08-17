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

`MUTATION_DESIGN_READY=true` means an exact reversible **experiment design** now exists. It does not mean that a larger world-map extent is safe, that a final target extent has been selected, or that this task may modify/execute the client.

## 1. Exact source fence — FACT

Every future execution of this design must begin by matching the exact source file:

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
elf_class: ELF64
elf_data: little_endian
elf_machine: x86_64
```

Source provenance is the coordinator-accepted graph promoted through #367 and producers #437/#446. This task did not reacquire or upload the raw executable.

## 2. Frozen mutation anchor — FACT

Accepted producer evidence proves the shared literal virtual address and bytes:

```yaml
shared_literal_va: 0x01cdd958
preimage_guard_16_hex: 120000000e0000000800000006000000
preimage_dwords_le: [18, 14, 8, 6]
patchable_prefix_length: 8
patchable_pair_le: [18, 14]
trailing_guard_pair_le: [8, 6]
```

Load-bearing accepted graph:

```text
0x01cdd958 packed 18/14
  -> exact TWorldmapProtocolMessageHandler constructor 0x00803ab0
  -> 0x00803d8b Handler+0xb0/+0xb4
  -> 0x00bc6350 geometry snapshot +0x38
  -> Handler+0x10 exact TWorldMapStorage virtual dispatch
  -> TWorldMapStorage slot 12 0x00cc6cd0
  -> 0x00cc6d2c Storage+0x48/+0x4c
```

The same literal independently initializes `TWorldMapViewport+0x40/+0x44` in constructor `0x00cbf680`. Exact setter `0x00cb2220` later recomputes Viewport geometry from pixel dimensions divided by 32 plus stored margins; exact recompute `0x00cbf700` uses a separate `15/11` base pair plus margins. Therefore a persistent Viewport value equal to the patched constructor literal is **not** a valid success requirement.

## 3. ELF virtual-address mapping — FACT / design decision

The accepted producer implementation used an ELF64 parser whose mapping is:

```text
for each PT_LOAD:
  if p_vaddr <= VA and VA+size <= p_vaddr+p_filesz:
      file_offset = p_offset + (VA - p_vaddr)
```

Historical source implementation: `.github/scripts/tibia-official-client-re-worldmap-exact-static-evidence.py` at producer source head lineage. Its `Elf64.vaddr_to_offset()` and `bytes_at()` functions are the mechanism that recovered bytes at virtual addresses without assuming VA equals file offset.

Independent retained exact-client artifact `9248797952` from run `31892019505` is additionally fenced to the same exact SHA/size and records nearby exact mappings such as:

```text
file_offset=0x1cddd20 vaddr=0x1cddd20 text=N5tibia8worldmap23TWorldMapRenderProviderE
file_offset=0x1cdde3f vaddr=0x1cdde3f text=playerPosition
```

Those nearby identity mappings are corroboration only. This design deliberately does **not** hardcode `file_offset=0x01cdd958` from proximity.

### Required future mapping rule

A future mutation executor must parse the fenced file's own ELF program headers and require **exactly one** file-backed `PT_LOAD` segment to contain all 16 guard bytes at VA `0x01cdd958`. It computes the file offset from that segment at execution time.

If no segment, multiple eligible segments, an out-of-file range, wrong ELF class/data/machine, or any parser contradiction is observed:

```yaml
mutation_result: REFUSED
```

This is stronger than a numeric offset copied from historical prose and remains exact across any allowed file layout only when the full source fence also matches.

## 4. Exact offline patch algorithm — DESIGN READY

The future executor must operate on a **task-owned copy**, never in-place on the canonical installed source file.

Required sequence:

1. Open the source read-only; require regular file and reject symlink ambiguity.
2. Verify exact size `51965216` and SHA-256 `e6c244...ff7fe` before deriving any patch consequence.
3. Verify ELF64 little-endian x86-64 and parse `PT_LOAD` program headers.
4. Derive the unique file offset for VA `0x01cdd958` using the formula above.
5. Read 16 bytes at the derived offset and require exact guard:
   `12 00 00 00 0e 00 00 00 08 00 00 00 06 00 00 00`.
6. Create a task-owned copy with restricted permissions. Preserve the original source unchanged.
7. Replace only the first 8 bytes with `struct.pack('<II', candidate_x, candidate_y)`; keep DWORDs `8,6` untouched.
8. Re-read the copy and require the complete 16-byte postimage to equal:
   `pack_le32(candidate_x) || pack_le32(candidate_y) || 08 00 00 00 || 06 00 00 00`.
9. Byte-compare the entire source and copy; refuse if any difference exists outside the derived 8-byte patch range.
10. Compute and persist the patched-copy SHA-256 and exact diff manifest before any execution.
11. Never replace the canonical source file. Rollback is termination of the task-owned patched runtime if any, followed by deletion of the patched copy; the exact source must still hash to `e6c244...ff7fe`.

### Fail-closed target contract

This design does not authorize arbitrary values. Every future execution task must declare one exact candidate pair before creation of the patched copy.

For the **first physical discriminator only**, the recommended candidate is:

```yaml
candidate_pair: [19, 14]
postimage_prefix_8_hex: 130000000e000000
changed_source_bytes: 1
purpose: width_axis_plus_one_causal_canary
classification: RECOMMENDATION_NOT_FINAL_TARGET
```

Reason: changing 18 -> 19 while retaining 14 changes one byte and one axis only, minimizing the experimental delta and making causal interpretation sharper. It is **not** evidence that `19x14` is a desirable production/final extent.

A later independent height-axis canary may use `[18,15]` only after the first discriminator is safely closed. Larger historical candidates such as `26x20`, `32x24`, or `36x28` remain unproven test ideas and must not be promoted directly from old notes.

## 5. Why only this literal is patched — FACT + safety consequence

No additional patch site is justified by the accepted graph:

- changing only Viewport geometry cannot prove that Storage retains a larger live region;
- Handler constructor default is upstream of the proven snapshot -> Storage path;
- Viewport is dynamically recomputed later, so patching its dynamic formula/base simultaneously would confound the first causal test;
- RenderProvider and Picker already consume dynamic geometry through fixed-32 operations; no independent `18`/`14` cap was recovered there;
- the RenderProvider `65535 x 10-byte` allocation has an unknown semantic role and is not a patch target;
- no direct Camera-field -> Storage/master-extent mutation edge was recovered in the accepted bounded Camera neighborhoods.

Therefore the first discriminator mutates only the shared literal prefix and treats every unexpected downstream clamp/failure as evidence, not as permission to patch a second site.

## 6. Carried unknowns — still open

```yaml
complete_post_constructor_Handler_b0_b4_writer_census: UNKNOWN
exact_source_member_names_and_units: UNKNOWN
network_or_parser_extent_ceiling: UNKNOWN
render_65535x10_semantic_worldmap_ceiling: UNKNOWN
named_camera_projection_or_indirect_coupling: UNKNOWN
safe_final_extent: UNKNOWN
safe_final_client_byte_mutation: NOT_PROVEN
```

These unknowns no longer prevent constructing a bounded reversible canary design. They **do** prevent claiming that the patch is safe or that a larger target extent is ready for routine use.

## 7. Physical-validation contract — CONTRACT READY, EXECUTION NOT AUTHORIZED

A later physical task must re-read then-current governance and create a fresh Track A admission record. This design task cannot grant that authority.

### Runtime class

A patched copy does not have the canonical exact SHA and therefore must never be represented as the exact registered canonical runtime.

The natural future class is a task-owned `ephemeral_isolated` native-Linux experiment with a unique process/display/state namespace. Any login/world-session use must additionally satisfy then-current one-session rules and explicit authorization for the concrete live-session experiment. A second logged-in Track A Global session may not be created merely to test the patch.

If semantic validation requires an in-game session and the permissible session/ownership boundary cannot be proven, the correct result is `BLOCKED`, not a weaker launch.

### Required pre-launch evidence

```yaml
source_exact_sha: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
source_exact_size: 51965216
patch_va: 0x01cdd958
patch_file_offset: freshly_derived_from_PT_LOAD
preimage_guard: exact_16_bytes
candidate_pair: explicitly_declared
patched_sha256: freshly_computed
full_file_diff_outside_patch_range: 0
runtime_class: ephemeral_isolated
runtime_namespace_uniqueness: PROVEN
competing_or_unverifiable_official_client_session: 0_or_execution_refused
client_byte_mutation_authorized: true_required_from_follow_on_authority
```

The current repo state at design time has coordinator promotion PR `#448` still open/draft. Its raw XRes helper is therefore not trusted-main implementation yet. Nothing in this design may treat #448 as already promoted or use historical XID/PID evidence as current identity.

### Structural discriminator

For first width canary `[19,14]`, the future physical validator should attempt to prove, in order:

1. the spawned process executes the exact patched-copy inode/path/hash owned by the task;
2. exact class identity anchors remain valid for the patched build at unchanged static addresses under the same load base/relocation model;
3. after Handler construction and before any contradictory later writer, `Handler+0xb0/+0xb4` reflects `[19,14]`;
4. after the accepted snapshot/slot-12 propagation point occurs, exact `TWorldMapStorage` (`vptr 0x0308ce70`) `+0x48/+0x4c` reflects `[19,14]`;
5. any observed later reset of Handler or Storage pair is recorded as a writer/consumer discriminator, not patched around;
6. Viewport constructor may initially read `[19,14]`, but later dynamic recomputation is expected and must be recorded rather than treated as patch failure by itself;
7. RenderProvider/Picker behavior is checked for crash, rejection, clipping/indexing anomaly, or an effective clamp before escalating to a larger candidate;
8. if an in-game semantic step is separately authorized, the validator records whether retention/bounds behavior actually expands on the width axis and whether movement/floor/worldmap updates remain coherent;
9. terminate the patched experiment, delete the patched copy, and re-hash the untouched exact source as the final rollback proof.

### Physical success classification

A future run may classify the width canary as `CAUSAL_PROPAGATION_PROVEN` only if the patched process identity plus Handler -> snapshot -> Storage structural propagation are directly observed for the declared output hash.

It may classify a larger extent as `SEMANTICALLY_VALIDATED` only after separately authorized live behavior demonstrates the intended retention/bounds effect without material regression. Structural propagation alone is insufficient.

## 8. Abort conditions

Immediately stop and preserve evidence if any of these occurs:

- wrong source version/size/SHA;
- VA cannot be uniquely mapped through a file-backed `PT_LOAD`;
- 16-byte preimage mismatch;
- any source-byte change outside the declared patch range;
- the exact source file itself is modified;
- patched process identity is ambiguous;
- runtime namespace/ownership conflicts with another task;
- another logged-in or unverifiable official-client session makes the experiment unsafe;
- startup/load failure, crash, unexpected disconnect or material network/session anomaly;
- Handler pair does not take the canary value;
- a later writer overwrites the pair before Storage propagation;
- Storage pair fails to follow the canary;
- RenderProvider/Picker/Camera behavior produces a material regression;
- required current authority/admission is absent.

No abort condition authorizes adding another patch site in the same run.

## 9. Final design classification

```yaml
MUTATION_DESIGN_READY: true
meaning: exact reversible one-anchor experimental mutation design exists
SAFE_MUTATION_PROVEN: false
meaning: no claim of safe routine/final behavior
PHYSICAL_VALIDATION_CONTRACT_READY: true
meaning: future task has explicit structural success/failure/rollback contract
PHYSICAL_VALIDATION_EXECUTION_AUTHORIZED: false
meaning: this docs/static task cannot mutate or launch patched client
client_byte_mutation_authorized: false
final_target_extent: UNKNOWN
first_canary_recommendation: [19,14]
```

The next legitimate step is a **separately admitted physical-validation task**, only after its exact runtime/session/ownership and patched-client mutation authority are proven under then-current governance. It must consume this design rather than repeat the completed static graph recovery.
