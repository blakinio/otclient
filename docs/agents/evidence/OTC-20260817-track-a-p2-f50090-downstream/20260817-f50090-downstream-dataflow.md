# Track A P2 — `0xf50090` downstream dataflow

Date: 2026-08-17  
Task: `OTC-20260817-track-a-p2-f50090-downstream`  
Research status: **DRAFT / NOT PROMOTED**

## Exact-client fence

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux only
```

No live client process, process memory, login/gameplay, canonical runtime state or world-map evidence was used. The Synology source stage only verified the retained regular file and copied one file-backed window; disassembly and interpretation ran on GitHub-hosted Ubuntu.

## Producer generation

The initial marketplace-action producer failed before source access because GitHub could not download `actions/checkout` from `codeload.github.com` (HTTP 503/429). The replacement producer removed all marketplace actions without changing the research byte range.

Successful bounded generation:

```text
producer head    ea8113028a07ef84518f4a8b705bcecd97604376
run              32037248323 = SUCCESS
source job       95410048084 = SUCCESS
hosted job       95410072413 = SUCCESS
code window      0xf50040..0xf50480
code length      1088 bytes
code sha256      1d14d72f683455daa3ab065bd48c3588f8755798ce63e70b838569353c3e2cea
source candidate 1
runtime_access   none
```

Source job `95410048084` independently revalidated exact file size and SHA-256, ELF64 little-endian structure and file-backed range before emitting only the 1088 bounded bytes. Source-side disassembly/semantic classification, process access, process-memory access, client execution and client mutation were all absent.

## Function boundary and canonical argument

Hosted decode gives an aligned function entry at `0xf50090`; the next aligned function entry is `0xf501e0`.

At entry:

```text
f50090: push r12
f50092: push rbp
f50093: mov  rbp,rsi
f50096: push rbx
f50097: mov  rbx,rdi
```

The coordinator-promoted predecessor proves that the `0xb56c93` virtual call invokes exact target `0xf50090` with the canonical same message in SysV second argument `rsi`. Therefore:

```yaml
f50090_second_argument: FACT:canonical_same_message
f50090_saved_message_pointer: FACT:rbp
```

## Message decomposition

`0xf50090` immediately snapshots message fields instead of forwarding the original object pointer:

```text
f5009e: movdqu xmm0,[rsi+0x8]
f500a3: mov    rax,[rsi+0x18]
f500a7: mov    rdx,[rsi+0x8]
f500ab: mov    [rsp+0x10],rax
f500b0: movaps [rsp],xmm0
```

This preserves the values from:

```text
message+0x08 -> stack+0x00
message+0x10 -> stack+0x08
message+0x18 -> stack+0x10
```

The original message pointer remains in `rbp` for later field reads.

## Exact downstream field-bearing calls

### Length-derived helper

The first concrete call receives a scalar derived from `message+0x18`, not the original message pointer:

```text
f500c6: lea rsi,[rax+0xe]
f500ca: add rax,0x7
...
f500dc: sar rsi,0x3
...
f500f7: call 0x4dc3d0
```

Classification:

```yaml
target_0x4dc3d0: FACT
input_relation: FACT:length-derived scalar from message+0x18
whole_message_pointer_forwarded: false
```

### Message `+0x00` scalar helper

```text
f50107: mov esi,[rbp+0x0]
...
f50121: call 0x4daaf0
```

Classification:

```yaml
target_0x4daaf0: FACT
input_relation: FACT:scalar from message+0x00
whole_message_pointer_forwarded: false
```

### Raw payload pointer/length edge

The strongest downstream payload edge is:

```text
f5013d: mov rsi,[rsp+0x8]   # value copied from message+0x10
f50142: mov rdi,[rdi+0x18]
f50146: mov rdx,[rsp+0x10]  # value copied from message+0x18
...
f50153: call 0x4dd250
```

Therefore:

```yaml
f50153_target: FACT:0x4dd250
f50153_rsi: FACT:value from canonical message+0x10
f50153_rdx: FACT:value from canonical message+0x18
f50153_receiver_provenance: FACT:nested receiver derived from f50090 this+0x08 then +0x18
raw_payload_pointer_length_edge_to_0x4dd250: FACT
```

This is sufficient to advance the P2 frontier from the whole-message object to the exact payload-pointer/length call at `0x4dd250`.

## Negative control — whole-message forwarding

No downstream call in the decoded `0xf50090` function receives the original saved message pointer `rbp` as its argument. The fallback virtual calls also use transformed/scalar/local values; for example `f501a3` explicitly replaces `rsi` with the local snapshot address before `call rax`.

```yaml
f50090_forwards_original_message_pointer_as_whole: DISPROVEN
f50090_decomposes_message_into_fields: FACT
```

This does **not** mean the message payload is lost: its pointer/length values are directly carried to `0x4dd250` as proven above.

## What is not proven

The current evidence deliberately does not assign a name or transport-layer semantic to `0x4dd250` merely from its calling convention.

```yaml
semantic_role_of_0x4dd250: UNKNOWN
receiver_exact_dynamic_type_at_0x4dd250: UNKNOWN
0x4dd250_is_final_binary_socket_write: UNKNOWN
final_binary_egress: UNKNOWN
final_socket_ownership: UNKNOWN
framing: UNKNOWN
sequence: UNKNOWN
compression: UNKNOWN
encryption: UNKNOWN
```

## Result / next exact frontier

The bounded task's stop condition is satisfied:

```text
canonical same message
 -> 0xf50090
 -> message decomposed into exact fields
 -> raw payload pointer (message+0x10) + length (message+0x18)
 -> concrete target 0x4dd250
```

The next smallest falsifiable P2 question is the exact identity/receiver/downstream dataflow of `0x4dd250`. It must not be called a socket sink, framing, compression or encryption stage until independent exact evidence proves that semantic role.

E2E: `NOT_APPLICABLE` — exact static file/disassembly evidence only.
