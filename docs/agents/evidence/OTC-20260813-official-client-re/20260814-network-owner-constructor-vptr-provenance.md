# Track A — network-owner constructor/vptr provenance

## Scope

Track A / `official-client-re` only. Subject: official native Linux Tibia client `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

This is a bounded static S2 continuation of the proven `TProtocolMessageQueue -> containing network owner -> QTcpSocket` handoff.

## Exact experiment

```yaml
workflow: .github/workflows/tibia-official-client-re-network-owner-constructor-vptr.yml
workflow_commit: fa4e8ff97109aba60ddb1491d310a1daa32de9d8
run: 31812064093
job: 94804814210
result: PASS
runner: synology-otclient-01
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

## Proven constructor/setup structure

### Containing-owner setup function

Prior exact-version evidence identifies `0x7e7fe0` as the containing-owner setup function. Its prologue preserves `rdi` as `r14`, and later virtual calls dereference `[r14]` at offsets `+0x4a8`, `+0x4b0`, `+0x4b8`, `+0x4c0`, `+0x4c8`, and `+0x4d8`. The same `r14` is passed to `0x196fee0`, which constructs the `QTcpSocket`-owning receiver setup.

At function entry:

```text
0x7e7fe6  r15 = rsi
0x7e7feb  r14 = rdi
0x7e8001  call 0x7e7db0
```

### Nested queue-facing object installed by `0x7e7db0`

The disassembly of `0x7e7db0` shows a separate allocation whose base pointer receives vtable address point `0x2f69168`. The function then stores the inner pointer `base+0x10` into the containing owner at `+0x88` and the base pointer into the containing owner at `+0x90`.

This is consistent with the independently proven connection edge where `[owner+0x88]` is the `TProtocolMessageQueue` sender pointer.

Therefore:

- `0x2f69168` belongs to the nested allocated/base object created by `0x7e7db0`;
- it is **not** promoted as the primary vtable of the containing network owner merely because it was the highest-ranked nearby candidate in the broad vtable census.

### Direct primary-vptr store observed in the same owner-setup region

A distinct constructor-shaped function beginning at `0x7e7130` preserves `rdi` as `rbx` and performs:

```text
0x7e71d0  lea rax,[rip+...]  # 0x3084648
0x7e71d7  mov [rbx],rax
```

It subsequently initializes many object fields, including zeroing `+0x88/+0x90`, and constructs owned subobjects. This is a direct primary-vptr store for the object constructed by `0x7e7130`.

The candidate address point `0x3084648` has `+0x90 -> 0x17d7080` under the exact relocated image.

## Classification

- **FACT:** run `31812064093` / job `94804814210` completed successfully on the exact fenced official-client SHA.
- **FACT:** `0x7e7db0` is called immediately from `0x7e7fe0` with the containing owner as `rdi` and installs a nested queue-facing allocation into owner fields `+0x88/+0x90`.
- **FACT:** the nested allocation's base object receives vtable address point `0x2f69168`.
- **FACT:** `0x7e7130` has constructor shape and directly stores address point `0x3084648` into its `this` vptr.
- **FACT:** `0x7e7fe0` later makes the proven high-offset virtual calls through the vptr of its `rdi`/`r14` object.
- **DERIVED:** the earlier broad static vtable-shape census cannot identify the containing owner by proximity alone and conflated at least one nested allocation with the containing owner candidate set.
- **INFERENCE:** `0x3084648` is a strong primary-vtable candidate for the concrete containing owner used by `0x7e7fe0`; this is not yet promoted because the call/xref/RTTI relationship between constructor `0x7e7130` and the concrete object reaching `0x7e7fe0` has not yet been closed.
- **UNKNOWN:** the exact primary vtable address point of the containing owner.
- **UNKNOWN:** therefore the exact concrete function behind the owner's `+0x90` queue-processing receiver remains unpromoted.
- **UNKNOWN:** the exact point where `GameclientMessage` becomes framed network bytes.

## Rejected interpretation

Do not promote `0x2f69168` as the containing network-owner vtable. Constructor provenance shows it is written to a separately allocated nested/base object in `0x7e7db0`, while the queue-facing inner pointer is installed into `[owner+0x88]`.

## Next action

Probe address point `0x3084648` directly: resolve its exact relocated entries at `+0x90` and the proven high virtual-call offsets, enumerate code xrefs to `0x3084648`, and enumerate callers of `0x7e7130` and `0x7e7fe0`. Promote it only if constructor/callsite provenance ties the same concrete object/class to both paths.
