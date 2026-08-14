# Official login origin and QIODevice write xrefs

Track: `official-client-re` / `OTCLIENT-TIBIA-RE`  
Evidence date: 2026-08-14  
Exact executable SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`  
Exact executable size: `51965216`

## Purpose

Bound two independent static paths without another official-service login:

1. recover the enclosing function around the already-proven primary login `QObject::connectImpl` call at `0x7d564f`;
2. enumerate every direct executable call to `QIODevice::write(QByteArray const&)@plt` at `0x4de370` and classify the resulting candidate writer functions.

This evidence intentionally does not equate the login receiver path with any writer candidate until a structural relation is proven.

## Run identity — PROVEN

Workflow:

```text
.github/workflows/tibia-official-client-re-login-origin-write-xrefs.yml
```

Run/job:

```yaml
run_id: 31826270686
job_id: 94851048204
result: SUCCESS
head: 0a0d3e9d752ed56531aee956e355526c9465f640
```

Artifact:

```yaml
name: track-a-login-origin-write-xrefs-31826270686
artifact_id: 9228921041
zip_sha256: 12a7be3354be1f5d4d925417fea3c0aa8be23ab0146669f663431443fd96838a
```

The downloaded artifact and the final job log agree on the counts and addresses below. They supersede a transient/truncated intermediate rendering that incorrectly suggested 14 direct writes and one direct call to `0xbd36a0`.

## Login connect enclosing function — PROVEN

The exact `0x7d564f` connect call lies in one FDE:

```text
LOGIN_CONNECT_FDE_COUNT=1
LOGIN_CONNECT_FDE start=0x7d0fe0 end=0x7d5e4d size=0x4e6d
LOGIN_ENCLOSING_START_CALLERS target=0x7d0fe0 count=0 sites=none
```

No direct `E8` call to the exact FDE start was found. This does not imply that the function is unreachable; it only makes the direct-caller-to-entry strategy insufficient for recovering the enclosing object's constructor/provenance.

The same whole-executable scan found:

```text
LOGIN_SLOT_TARGET_DIRECT_CALL_COUNT=0
LOGIN_SLOT_TARGET_DIRECT_CALL_SITES=none
```

Therefore the primary slot target `0xbd36a0` remains a captured PMF/indirect target rather than a directly called function in the executable scan.

## Direct QIODevice::write census — PROVEN

Exact symbol identity:

```text
0x4de370 = QIODevice::write(QByteArray const&)@plt
```

Whole executable direct-call count:

```text
QIODEVICE_WRITE_DIRECT_CALL_COUNT=5
QIODEVICE_WRITE_DIRECT_CALL_SITES=
  0x7dd563
  0xb40675
  0xb46ca4
  0xc4a92f
  0xd0868f
```

Their containing FDEs are:

```text
0x7dd563 -> 0x7dd3f0..0x7dd62d
0xb40675 -> 0xb40630..0xb4068c
0xb46ca4 -> 0xb46bd0..0xb46cce
0xc4a92f -> 0xc49ee0..0xc4a9e5
0xd0868f -> 0xd085e0..0xd0872e
```

## Candidate classification

### Candidate A: `0x7dd3f0..0x7dd62d` — HIGH PRIORITY

Immediately before its `QIODevice::write` path, the function reads virtual slot `+0xd0` from an object and compares the target against the exact function entry `0xb40630`:

```asm
mov rdi,QWORD PTR [r12]
mov rdx,QWORD PTR [rdi]
mov rdx,QWORD PTR [rdx+0xd0]
lea rax,[rip+...]        # 0xb40630
cmp rdx,rax
jne ...
...
0x7dd560: mov rdi,r12
0x7dd563: call 0x4de370  # QIODevice::write(QByteArray const&)@plt
```

It also uses `QMetaObject::activate` and several local helpers. The exact class/semantic role is UNKNOWN, but the explicit virtual-slot comparison against Candidate B makes this the strongest structural bridge currently visible between a Qt object and the final write API.

### Candidate B: `0xb40630..0xb4068c` — HIGH PRIORITY

This is a thin adapter around a virtual `+0xd0` operation followed by `QIODevice::write`:

```asm
mov rdi,QWORD PTR [rdi+0x8]
...
mov rax,QWORD PTR [rax+0xd0]
call rax
...
mov rdi,rbp
mov rsi,rbx
call 0x4de370
```

Its exact class is UNKNOWN. Because Candidate A explicitly compares a virtual target to `0xb40630`, the next useful static test is to identify all vtable/data references containing `0xb40630` and compare those vtables with already recovered network-owner vtables.

### Candidate C: `0xb46bd0..0xb46cce` — MEDIUM PRIORITY

This function creates/uses a QByteArray-like stack temporary and calls `QIODevice::write` through receiver `r13`. Its network relevance is currently UNKNOWN and should be tested only after Candidates A/B.

### Candidate D: `0xc49ee0..0xc4a9e5` — LOWER PRIORITY, NOT DISPROVEN

This is a large string/UTF-8-heavy function that eventually calls `QIODevice::write`. Its shape suggests a text/log/export path, but that is only an INFERENCE. It must not be discarded without class/caller evidence.

### Candidate E: `0xd085e0..0xd0872e` — DISPROVEN AS GAME-SOCKET SINK

This function explicitly constructs and opens a `QFile`, invokes `QIODevice::write`, and destroys the `QFile`:

```text
QFile::QFile(QString const&)
QFile::open(QIODeviceBase::OpenMode)
QIODevice::write(QByteArray const&)
QFile::~QFile()
```

Therefore this direct write site is a file-output path, not the final game-network socket writer.

## Relation to the previously recovered network owner — UNKNOWN

Canonical Track A task evidence independently records this exact outbound convergence:

```text
primary network-owner vtable:        0x308c408
primary owner slot +0x90:            0x8409d0
contained subobject at owner +0x88
contained subobject vtable:          0x2f66288
contained subobject slot +0xb8:      0xb5b880
```

Source run/job for that promoted convergence:

```yaml
run_id: 31812572191
job_id: 94806473825
result: SUCCESS
```

No relation between either `0x308c408` or `0x2f66288` and `0xb40630` has yet been proven. In particular, do not infer that the contained network subobject at owner `+0x88` is the same object as the primary login receiver loaded from `[rbx+0x88]` at `0x7d55c8`; identical member offsets in unrelated enclosing classes are not identity evidence.

A short-lived draft of this evidence incorrectly named `0x2f66350` as the primary network-owner vtable. Reconciliation against the canonical active task corrected that mistake before any writer-vtable conclusion was promoted. The canonical primary network-owner address point is `0x308c408`.

## Corrected proof boundary

### FACT

- the exact executable has five direct executable calls to `QIODevice::write(QByteArray const&)@plt`;
- `0xd0868f` is a QFile write path and can be excluded from the game-socket sink search;
- Candidate A (`0x7dd3f0`) structurally compares an object's `vtable+0xd0` target against Candidate B (`0xb40630`) before a direct QIODevice write path;
- the primary login connect call belongs to FDE `0x7d0fe0..0x7d5e4d`;
- there are zero direct executable calls to slot PMF target `0xbd36a0` in this scan;
- canonical outbound evidence promotes primary owner vtable `0x308c408` and contained subobject vtable `0x2f66288`.

### UNKNOWN

- which remaining QIODevice writer is used by the game connection;
- class/vtable owning virtual target `0xb40630`;
- whether `0xb40630` occurs in either canonical network vtable `0x308c408` or `0x2f66288`;
- structural relation between the primary login adapter path and the final Qt writer;
- actual 15.32 game-login wire field order and version representation.

## Next action

Perform an exact-SHA static vtable/data-reference census centered on `0xb40630`, with explicit reads of canonical network-owner vtables `0x308c408` and `0x2f66288` through at least slot `+0xd0`. Recover all direct/data references to Candidate A/B, resolve any candidate vtable/typeinfo context, and disassemble only proven callers/owners. If a canonical network vtable contains `0xb40630`, promote that structural bridge; otherwise keep the paths separate and continue caller/vtable provenance without guessing.