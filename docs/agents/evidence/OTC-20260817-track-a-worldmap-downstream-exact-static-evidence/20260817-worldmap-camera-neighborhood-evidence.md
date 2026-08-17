# TWorldMapCamera exact neighborhood evidence — supplement for PR #367

## Disposition

```text
camera exact identity: PROVEN
camera exact-vptr neighborhoods: 11/11 staged and hosted-disassembled
camera direct Storage/18x14 mutation edge: NOT RECOVERED in bounded neighborhoods
camera preidentified patch site: false
camera post-change validation dependency: true
```

This is a camera-only supplement to `20260817-worldmap-downstream-exact-static-evidence.md`. It was produced because Camera projection/scale coupling remained the last named downstream semantic gap after the broader producer pass. It does not broaden runtime access or authorize client mutation.

## Exact provenance

```text
client version  15.32.df7b29
client size     51965216
client SHA256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe

run             32003150333
source job      95307268007       SUCCESS
source artifact 9279105537
digest          sha256:9b44a39558c50ce86243dece3b3fac19bb1f7619112e913fa45b647878d9e28d
hosted job      95307487191       SUCCESS
final artifact  9279111731
digest          sha256:81620b3fd866e2203b2ed0a39a1a0979ba52b5e3af41b47ac7e247b09082effa

exact Camera-vptr xrefs     11
bounded source windows      11
bounded source code bytes   225280
unique hosted instructions  37325
```

Source access was read-only exact-file access on `synology-otclient-01`. The client was not executed; process memory, canonical state, X11/VNC, login/gameplay and client-byte mutation were not used. The raw executable was never uploaded.

## Exact Camera identity

```text
vptr       0x03083968
typeinfo   0x03080500
relation   RELA:R_X86_64_RELATIVE
name ptr   0x01cabce0
RTTI       N5tibia8renderer15TWorldMapCameraE
class      tibia::renderer::TWorldMapCamera
```

The eleven exact vptr xrefs staged were:

```text
0x007e73ca
0x0082b630
0x00833dd0
0x00b39b48
0x00def35b
0x016bd85d
0x016bd97d
0x016c948b
0x016c967e
0x016e734d
0x016e746d
```

## Exact Camera constructor/layout

At `0x00def35b`:

```text
0x00def35b  lea  rax,[rip+...] -> 0x03083968
0x00def370  mov  QWORD PTR [rbx],rax
0x00def373  lea  rax,[rip+...] -> 0x02f69278
0x00def389  mov  QWORD PTR [rbx+0x98],rax
0x00def390  mov  QWORD PTR [rbx+0xb8],rax
0x00def39e  mov  DWORD PTR [rbx+0x50],0
0x00def3a5  mov  DWORD PTR [rbx+0x94],0
0x00def3af  mov  QWORD PTR [rbx+0xa0],0
0x00def3ba  mov  DWORD PTR [rbx+0xa8],0
0x00def3c4  mov  QWORD PTR [rbx+0xb0],0
0x00def3cf  mov  QWORD PTR [rbx+0xc0],0
0x00def3da  mov  DWORD PTR [rbx+0xc8],0
0x00def3e4  mov  DWORD PTR [rbx+0xd0],0x3f800000
0x00def3f5  mov  BYTE PTR [rbx+0xdc],0
0x00def3fc..0x00def408 -> vector block Camera+0x10..+0x40
0x00def40c..0x00def418 -> vector block Camera+0x54..+0x84
```

**FACT:** Camera initializes two four-vector state blocks, two embedded address points around `+0x98/+0xb8`, scalar `Camera+0xd0 = 1.0`, and zero/default surrounding state.

**INFERENCE:** the vector/scalar state is transform/scale-like.

**UNKNOWN:** the bytes alone do not justify renaming these fields as a projection matrix or selecting a Camera mutation site.

## Exact Camera ↔ Viewport co-ownership/coordination

One exact higher-level constructor neighborhood around Camera vptr xref `0x007e73ca` proves both objects are coordinated by the same owner.

Camera counted allocation and installation:

```text
0x007e73a4  lea  rax,[rip+...] -> 0x02f692a0
            # counted TWorldMapCamera wrapper vptr
0x007e73ad  lea  r15,[rbp+0x10]
            # inline Camera object
0x007e73ca  lea  rax,[rip+...] -> 0x03083968
0x007e73e6  mov  QWORD PTR [rbp+0x10],rax
...
0x007e7478  mov  QWORD PTR [higher_owner+0xc8],r15
0x007e7471  mov  QWORD PTR [higher_owner+0xd0],rbp
```

Later in the same exact higher-level construction path:

```text
0x007e7bbd  mov  rbp,QWORD PTR [higher_owner+0xa8]
0x007e7bf5  call 0x00cbf700
```

`0x00cbf700` is the already exact-recovered `TWorldMapViewport` geometry recomputation routine. An alternate dispatch at `0x007e7c2e` jumps to the same routine.

**FACT:** one higher-level world-map owner keeps a Viewport-compatible object at `+0xa8` and counted Camera at `+0xc8/+0xd0`, and invokes Viewport recomputation after Camera construction/state installation.

This establishes a coordination/ownership edge without inventing a direct Camera-field formula for the Viewport extent.

## Bounded dependency result

Across all 11 exact Camera-vptr neighborhoods — 225,280 source bytes and 37,325 unique hosted instructions — the curated scan did **not** recover a type-anchored Camera-field chain to:

```text
TWorldMapStorage vptr      0x0308ce70
TWorldMapRenderProvider    0x02f6c258
TWorldMapPicker            0x02f6b7c8
Storage slot12             0x00cc6cd0
Storage+0x48/+0x4c         exact 18/14 pair
Handler+0xb0/+0xb4         master 18/14 pair
```

This is a **bounded negative result**, not a global absence proof.

The same neighborhoods do contain the adjacent exact `TWorldMapViewport` constructor and the shared `18/14` literal because Camera/Viewport construction code is colocated. In particular `0x00def4c0` begins a distinct Viewport constructor, and its use of `0x01cdd958` is not promoted as a Camera write.

## Consumer consequence

For the current static dependency graph:

```yaml
FACT:
  camera_layout_and_identity: recovered
  camera_viewport_coownership: recovered
  direct_camera_extent_mutation_edge_in_all_exact_vptr_neighborhoods: not recovered
RECOMMENDATION_FOR_GRAPH_ONLY:
  preidentified_camera_patch_site: none
  camera_role: post-change validation dependency / transform-state observer
UNKNOWN:
  named_camera_projection_formula: not recovered
  indirect_camera_coupling_outside_the_staged_neighborhoods: not globally excluded
```

This result removes the need to invent a Camera mutation site merely to complete the graph. Any future mutation design must still validate Camera behavior physically, but no client bytes are changed or proposed here.
