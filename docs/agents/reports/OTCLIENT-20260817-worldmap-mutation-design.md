# OTCLIENT-TIBIA-RE — world-map extent mutation design

## Status

```yaml
task: OTC-20260817-track-a-worldmap-mutation-design
pr: 452
track: official-client-re
execution_class: github_hosted
runtime_access: none
STATIC_PATCH_GRAPH_READY: true
MUTATION_DESIGN_READY: true
OFFLINE_PATCH_PLAN_READY: true
SAFE_MUTATION_PROVEN: false
PHYSICAL_VALIDATION_CONTRACT_READY: true
PHYSICAL_VALIDATION_EXECUTION_AUTHORIZED: false
client_byte_mutation_authorized: false
physical_e2e: NOT_APPLICABLE
```

This report closes the design-only stage after merged static consumer #367 and producers #437/#446. It defines one exact reversible experimental mutation anchor and a future physical discriminator. It does **not** modify or execute the official client and does not claim a safe final larger extent.

## Exact client fence

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux only
```

## Exact design

The accepted shared constructor literal is at virtual address `0x01cdd958` with 16-byte guard:

```text
12 00 00 00  0e 00 00 00  08 00 00 00  06 00 00 00
|--- 18 ---|  |--- 14 ---|  |--- 8 ----|  |--- 6 ----|
```

Only the first two DWORDs are candidates. The `8,6` suffix is a mandatory unchanged guard.

Future tooling must not assume VA equals file offset. It must parse the exact file's ELF64 `PT_LOAD` program headers and compute:

```text
file_offset = p_offset + (0x01cdd958 - p_vaddr)
```

only when exactly one file-backed load segment contains all 16 guard bytes. The exact source size/SHA and 16-byte preimage must both pass before a task-owned copy is created.

The canonical installed source must never be patched in place. A future authorized executor creates a task-owned copy, patches only the derived 8-byte pair, verifies the whole-file diff is zero outside that range, computes the patched-copy SHA, and uses deletion of the copy plus re-hash of the untouched exact source as rollback.

## First causal discriminator

The recommended first physical canary is **`[19,14]`**, not a final product target:

```yaml
source_pair: [18,14]
candidate_pair: [19,14]
postimage_prefix_8_hex: 130000000e000000
actual_byte_delta: one byte
purpose: isolate width-axis propagation with the smallest useful mutation
```

A height-axis `[18,15]` canary is a later independent discriminator only after the width run is safely closed. Historical ideas `26x20`, `32x24`, and `36x28` remain unproven and are not promoted by this task.

## Expected causal path

```text
shared literal 18/14 -> candidate 19/14
  -> Handler constructor +0xb0/+0xb4
  -> geometry snapshot +0x38
  -> exact Storage slot 12
  -> Storage+0x48/+0x4c
```

The shared literal also seeds the Viewport constructor. Viewport later recomputes geometry dynamically from pixel dimensions/32 plus margins, so persistent Viewport equality with the constructor canary is not required and must not be forced by a second patch in the same experiment.

RenderProvider and Picker consume dynamic fixed-32 geometry; no independent `18/14` limit was recovered. The RenderProvider `65535 x 10-byte` allocation remains semantically unknown and is not a patch target. Camera remains a bounded downstream validation dependency, not a recovered extent writer.

## Safety boundary

The design is experiment-ready but **not safety-proven**. These remain explicit unknowns:

- complete later-writer census for Handler `+0xb0/+0xb4`;
- exact source member names/units;
- network/parser extent ceiling;
- semantic role of the RenderProvider fixed allocation;
- named Camera projection/indirect coupling outside accepted neighborhoods;
- safe final extent and safe routine client-byte mutation.

An unexpected later writer, Storage clamp, render/picker regression, crash, disconnect or session anomaly is a failed/inconclusive discriminator. It never authorizes patching another site in the same run.

## Future physical validation boundary

A patched copy has a different SHA from the accepted canonical client and must not be represented as the exact registered canonical runtime. A future physical task must re-evaluate Track A admission and use a task-owned isolated runtime model consistent with then-current governance.

Before launch it must prove: exact source fence, freshly derived patch offset, exact preimage, declared candidate pair, patched output SHA, zero diff outside the patch range, unique runtime namespace/ownership, and explicit client-byte mutation authority. Login/world-session use additionally requires the then-current one-session/live-session authority boundary; no second logged-in Global session is implied by this design.

The physical structural proof for `[19,14]` is:

1. prove the process executes the declared patched-copy path/inode/hash;
2. observe exact Handler identity and `+0xb0/+0xb4 = [19,14]` before contradictory later write;
3. observe the accepted snapshot/slot-12 path and exact `TWorldMapStorage` `+0x48/+0x4c = [19,14]`;
4. record Viewport dynamic recompute separately;
5. reject material RenderProvider/Picker/Camera/runtime regressions;
6. terminate patched runtime, delete patched copy, and prove the original source still has the exact source SHA.

Structural propagation may prove `CAUSAL_PROPAGATION_PROVEN`. It cannot by itself prove `SEMANTICALLY_VALIDATED` larger-world behavior; that needs separately authorized live semantics.

At the time of this design, raw-XRes helper coordinator PR #448 is still open/draft, so it is not trusted-main runtime identity implementation. Historical XID/PID values remain non-authoritative.

## Evidence

Primary design/evidence record:

`docs/agents/evidence/OTC-20260817-track-a-worldmap-mutation-design/20260817-worldmap-mutation-design.md`

Frozen source records:

- `docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md`
- `docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/CONTINUATION_HANDOVER.md`
- `docs/agents/evidence/OTC-20260816-track-a-worldmap-exact-static-evidence/20260817-worldmap-second-pack-evidence.json`
- `docs/agents/evidence/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence/`

Additional exact-fence mapping corroboration: historical run `31892019505`, artifact `9248797952`, which records exact-client file-offset/vaddr mappings; this report does not hardcode a target file offset from those neighboring mappings.

## Completion boundary

```yaml
worldmap_static_re: complete
mutation_experiment_design: complete
safe_final_mutation: not_proven
physical_mutation_executed: false
physical_validation_executed: false
user_facing_larger_extent_delivered: false
```

E2E for this documentation/design task is `NOT_APPLICABLE`: no executable/client/runtime behavior is changed by the PR. Physical validation is a separate protected effect, not a substitute for documentation CI.
