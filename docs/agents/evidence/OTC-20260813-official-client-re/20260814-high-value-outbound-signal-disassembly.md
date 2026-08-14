# Track A — high-value outbound GameAction signal disassembly

Date: 2026-08-14
Track: Track A / `official-client-re`
Repository: `blakinio/otclient`
Official Linux client SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

## Verification source

Workflow: `.github/workflows/tibia-official-client-re-high-value-send-disassembly.yml`

Successful run: `31793188185`

Successful job: `94744455372`

Head commit containing the vendored-GDB fix: `1c4ef6b612220e24cb312dfa6fce032b5c13d484`

The workflow performs file-only GDB disassembly of the pinned official-client ELF. It does not start the client process and does not emit a game action.

## Result

The six previously mapped high-value `send*` QMeta methods are Qt signal-emission wrappers, not direct protocol serializers. Each wrapper obtains the argument pointer from the QMeta argv array and invokes `QMetaObject::activate` through PLT address `0x4dedc0` against the class static metaobject.

| QMeta method | Case entry | Static metaobject used | Signal index passed to `QMetaObject::activate` | Verified wrapper behavior |
|---|---:|---:|---:|---|
| `TCreaturesGameActionHandler::sendAttack` | `0xd166f0` | `0x3085060` | `1` | loads `argv[1]`, emits Qt signal, returns through shared epilogue |
| `TCreaturesGameActionHandler::sendFollow` | `0xd164e0` | `0x3085060` | `2` | loads `argv[1]`, emits Qt signal, returns |
| `TChatGameActionHandler::sendTalkMessage` | `0xcffb90` | `0x30851a0` | `9` | loads `argv[1]`, emits Qt signal, returns through shared epilogue |
| `TContainerGameActionHandler::sendMoveObject` | `0xd1df30` | `0x30850a0` | `1` | loads `argv[1]`, emits Qt signal, returns through shared epilogue |
| `TPlayerTradeGameActionHandler::sendTradeObject` | `0xded060` | `0x3085360` | `1` | loads `argv[1]`, emits Qt signal, returns |
| `TWorldMapGameActionHandler::sendMoveObject` | `0xdedac0` | `0x30850e0` | `0` | loads `argv[1]`, emits Qt signal, returns |

Representative exact pattern (`sendAttack`):

```text
0xd166f0  mov rax,QWORD PTR [rcx+0x8]
0xd166f4  mov edx,0x1
0xd166f9  mov rcx,rsp
0xd166fc  lea rsi,[rip+...]  # 0x3085060
0xd16703  mov QWORD PTR [rsp],0x0
0xd1670b  mov QWORD PTR [rsp+0x8],rax
0xd16710  call 0x4dedc0 <QMetaObject::activate@plt>
0xd16715  jmp 0xd16505
```

`sendFollow` is structurally the same with signal index `2`; Trade and WorldMap use the same one-argument signal pattern. Chat and Container use a larger local stack frame but still pass the QMeta argument pointer into `QMetaObject::activate`.

## Correction to the previous working hypothesis

The prior phrase "final sender/dispatcher" for the common return/tail regions is too strong. In the disassembly covered here, the mapped `send*` methods are signal emitters. Therefore their downstream protocol builder/serializer cannot be recovered by simply following an intra-case tail.

The Player range also proves that `0xd1abc0` itself is only:

```text
0xd1abc0  add rsp,0x38
0xd1abc4  ret
```

Adjacent Player QMeta cases emit signals through static metaobject `0x30852a0`; for example the observed neighboring cases use signal indices `0x0e`, `0x10`, `0x14`, `0x15`. Thus `0xd1abc0` must not be labeled a serializer or network sender.

## Additional structural observation

The Container disassembly after the `sendMoveObject` wrapper enters unrelated adjacent code at `0xd1df70` and then the next QMeta family at `0xd1e000`. That adjacent code is not evidence for the `sendMoveObject` serializer. Boundaries must continue to be derived from actual instruction/control-flow structure rather than arbitrary disassembly windows.

## Boundary

This checkpoint proves signal-emission behavior and exact QMeta signal indices for the six high-value methods. It does **not** yet identify:

- the connected receiver/slot;
- the protocol message builder;
- wire opcode/message ID;
- field layout or serialization order;
- final socket/network-send function.

## Next gate

Recover Qt signal-to-receiver connections for static metaobjects `0x3085060`, `0x30851a0`, `0x30850a0`, `0x3085360`, `0x30850e0` and Player `0x30852a0`. Prefer relocation-backed function-pointer/constructor evidence and exact disassembly of connection setup. Once receiver slots are identified, follow those slots to outbound message construction and serializers.
