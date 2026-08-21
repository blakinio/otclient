# Surveyor auth/session current-build lifecycle evidence

Task: `OTC-20260820-surveyor-auth-session-reader`
Implementation PR: #636
Exact client fence: `15.32 / 52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`

## Selection baseline

Fresh current-main repository-only and admitted physical `--collect-all` runs before this implementation both produced 169 canonical rows, 12 alias views, privacy PASS and 10 missing typed readers. `auth_session_typed_reader` ranked first at score 125. `world_minimap_typed_reader` tied at 125 but overlapped active #475/#593, so auth/session was selected.

The physical pre-implementation baseline had no auth/session typed reader. This is the before-side of the post-merge implementation causal comparison; it does not assert a login-state transition.

## FACT — exact-current static ownership chain

Exact-current ELF RTTI/relocation discovery independently resolved:

```text
TGameClient
  typeinfo = 0x30a7778
  primary vptr = 0x30adce8

TAuthenticationProcessController
  typeinfo = 0x30b4410
  primary vptr = 0x30b5290
```

The exact current `TGameClient::onGameSessionConnected` QMeta entry dispatches through target `0xd19580` into the current implementation at `0x6e10d0`. The implementation contains:

```text
0x6e10eb: mov 0x8d0(%rdi), %rbx
```

A bounded pre-implementation read-only object correlation on the already admitted exact target showed that the pointer at `TGameClient + 0x8d0` has the exact `TAuthenticationProcessController` primary vptr/typeinfo identity above. No credential/play-session payload fields were inspected.

## FACT — exact Qt lifecycle predicate

The exact deployed `libQt6StateMachine.so.6` fence is:

```text
size = 394824
sha256 = 26f504ae723fa15c77e0c33a93a964a305c63577f2bed3f136c098b7b06921e8
```

Its exported `QStateMachine::isRunning() const` implementation is structurally equivalent to:

```text
private = *(this + 0x8)
return *(u32 *)(private + 0xf0) == 2
```

The exact disassembly contains the private-pointer load, comparison against state `2` at private offset `0xf0`, and `sete %al`. The Surveyor reader therefore reports only the boolean equivalent of this exact library predicate.

A bounded read-only pre-implementation observation of the current controller returned private state `0`, hence `authentication_state_machine_running=false` under the exact Qt predicate.

## Reader boundary

The implementation:

- exact-fences the client size/SHA before any semantic read;
- exact-fences the deployed Qt StateMachine library size/SHA;
- scans only the single process heap for the exact `TGameClient` primary vptr and requires exactly one object;
- validates `TGameClient + 0x8d0` against the exact auth-controller vptr;
- validates the Qt private pointer before reading the single lifecycle word;
- opens `/proc/PID/mem` only with `O_RDONLY|O_CLOEXEC`;
- rechecks process start ticks after the read;
- emits no addresses, credentials, email, tokens, play-session data, packet payloads or window-title values;
- returns `UNAVAILABLE` on any fence, uniqueness, pointer, read or payload-validation failure;
- emits `semantic_state=TYPED_AUTH_LIFECYCLE_ONLY`, `in_game_claimed=false` and `semantic_promotion_allowed=false`.

`authentication_state_machine_running` is not an `IN_GAME` discriminator. In particular, bridge 3-of-3 structural presence remains non-authoritative for gameplay state.

## Post-merge acceptance contract

The post-merge physical read-only E2E must freshly re-admit the runtime and show the implementation causal delta against the pre-implementation baseline:

- `auth_session_typed_reader`: missing/unimplemented -> `AVAILABLE`;
- missing typed readers: `10 -> 9`;
- privacy scan: `PASS -> PASS`;
- exact client/runtime identity remains stable or is freshly re-bound by the admission evidence;
- auth lifecycle value is reported without claiming an auth-state transition or `IN_GAME`.

No logout/relogin, client/container restart, agent-generated keyboard/mouse input, process control, attach/debug/injection, memory write, network mutation, credential access, item/economic action or local-model execution is required or authorized for this acceptance.
