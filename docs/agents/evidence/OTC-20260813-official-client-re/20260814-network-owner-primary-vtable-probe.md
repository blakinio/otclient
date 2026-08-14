# Track A — primary-vtable candidate falsification

## Scope

Track A / `official-client-re` only. Subject: official native Linux Tibia client `15.32.df7b29`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

This experiment directly tested the prior strong candidate address point `0x3084648`, which constructor-shaped function `0x7e7130` stores into `this`.

## Exact experiment

```yaml
workflow: .github/workflows/tibia-official-client-re-network-owner-primary-vtable-probe.yml
workflow_commit: 900e99ae1337ddfa8de1a052633ad9d22f59fa16
run: 31812354764
job: 94805770137
result: PASS
runner: synology-otclient-01
```

## Exact relocated vtable facts

For address point `0x3084648`:

```text
offset_to_top = 0
RTTI = 0x30776c0
+0x60 = 0x7ec950
+0x68 = 0x7e7db0
+0x70 = 0x7e06d0
+0x78 = 0x7e6b70
+0x80 = 0x7e0b60
+0x88 = 0x6afe60
+0x90 = 0x0
+0xa0 = 0x7ce980
+0x4a8 = 0x7e9e80
+0x4b0 = 0x804620
+0x4b8 = 0x808d70
+0x4c0 = 0x800cc0
+0x4c8 = 0x801100
+0x4d8 = 0x7fe370
```

The candidate has two direct LEA references in executable code:

```text
0x7e16d0
0x7e71bb
```

`0x7e71bb` is the constructor store in `0x7e7130`. `0x7e16d0` is a destructor-like vptr restore before releasing many owned fields.

`0x7e7130` has two direct callsites:

```text
0x6fcc63
0x8362b2
```

At `0x8362b2`, the caller invokes `0x7e7130` and then immediately overwrites the primary vptr:

```text
0x8362b2  call 0x7e7130
0x8362b7  lea rax, 0x308c408
0x8362cd  mov [rbx], rax
```

This demonstrates that `0x7e7130` is usable as a base constructor and that `0x3084648` need not be the final most-derived runtime vtable.

The static direct-call scanner found zero direct `call rel32` references to `0x7e7fe0`; therefore the setup function may be reached through a virtual/indirect edge rather than a direct call.

## Classification

- **FACT:** run `31812354764` / job `94805770137` completed successfully on the exact fenced client.
- **FACT:** address point `0x3084648` has a null `+0x90` entry.
- **FACT:** prior live/static queue-connection evidence requires the concrete containing owner receiving `clientMessageReadyToProcess` through pointer-to-member virtual offset `+0x90`; therefore `0x3084648` cannot be the final concrete vtable for that receiving runtime object.
- **FACT:** `0x7e7130` installs `0x3084648`, while at least one direct caller (`0x8362b2`) subsequently replaces the primary vptr with `0x308c408`.
- **FACT:** `0x3084648 + 0x68` resolves to `0x7e7db0`, matching the queue-facing nested-object installation helper called from `0x7e7fe0`.
- **DISPROVEN:** the inference that `0x3084648` itself is the final containing network-owner vtable.
- **DERIVED:** the owner object is likely a more-derived class whose constructor reuses `0x7e7130` and later overwrites the primary vptr.
- **UNKNOWN:** exact most-derived owner vtable and concrete `+0x90` receiver.
- **UNKNOWN:** exact serialization/framing point downstream of queue processing.

## Next action

Enumerate relocated data/vtable references to function `0x7e7fe0` and the derived vtables written by callers of `0x7e7130`. Intersect candidates with the mandatory non-null `+0x90` entry and the proven high-slot virtual-call shape. This avoids guessing from constructor proximity and should identify the most-derived network owner structurally.
