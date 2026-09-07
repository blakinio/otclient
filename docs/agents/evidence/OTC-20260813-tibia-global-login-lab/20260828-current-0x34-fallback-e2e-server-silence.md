# 2026-08-28 — current `0x34` fallback E2E: server-silence boundary

Classification: **FACT / terminal bounded failure / no retry**.

## Exact evidence

```text
Track B PR                    #284
E2E marker head               dda4eb5328b8f918bac87d451e9c69ef2233d5b8
repair head                   62845fd2783f8e58a80e831ce01103f20367045b
TDD RED head                  1661f42efadb86849b4a861717c3f93471075554
E2E run                       33153487819
exact native build job        98790748187 = SUCCESS
world-entry job               98791849013 = FAILURE
promoted dispatch PR          #738
promoted dispatch merge       5a08ea4834b2bb6eb81ba65de7f22331658de9ef
promotion archive merge       54a0721049cbefcc5ce71cd4f7ca4397ef89cddb
source archive merge          5ac2eef58ebcff2f0e00ec1de008d51f2cd1fe59
disarm head                   4a59adb9423b51dae0fdb4bac0cd7bc9d2d579dc
```

## Verified preconditions

The exact E2E run proved all of the following before the terminal failure:

```text
CURRENT_LOGIN_WIRE_CONTRACT          PASS
EXACT_NATIVE_LINUX_BUILD             PASS
LAB_HTTP_PREFLIGHT_STATUS             200
LAB_HTTP_PREFLIGHT_HAS_SESSION        true
LAB_HTTP_PREFLIGHT_HAS_PLAYDATA       true
LAB_TRANSIENT_HTTP_LOGIN_STATUS       200
LAB_TRANSIENT_LOGIN_RESPONSE_VALID    true
LAB_TRANSIENT_WORLD_COUNT             1
LAB_TRANSIENT_CHARACTER_COUNT         1
LAB_TRANSIENT_GAME_HANDOFF_READY      true
LAB_GAME_TCP_VIA_WARP_SOCKS_GRANTED   true
LAB_GAME_SOCKS_FORWARD_READY          true
LAB_OTCLIENT_PROCESS_STARTED          true
```

No account/session/world/character values or packet payload bytes were logged.

## Terminal transport result

```text
LAB_GAME_FORWARD_CLIENT_BYTES=true
LAB_GAME_FORWARD_CLIENT_LENGTH=102
LAB_GAME_FORWARD_SERVER_BYTES=false
LAB_GAME_FORWARD_SERVER_LENGTH=0
TIBIA_GLOBAL_LAB_GAME_START_PROVEN=false
TIBIA_GLOBAL_LAB_IN_GAME_PROVEN=false
FAILURE_STAGE=after_character_login_call_before_game_callback
```

There was no `GAME_SERVER_OPCODE_*` marker in this run. Therefore the exact-current `0x34` fallback handler added by `62845fd...` was **not exercised**: no server application byte reached OTClient at all.

## What this run does and does not prove

FACT:
- the exact fallback implementation compiles and its focused contract is GREEN;
- the V6 official-service attempt sent the same bounded 102-byte client login frame family but received zero server bytes;
- V6 cannot validate or falsify the `0x34` fallback behavior because the inbound boundary was never reached;
- no identical retry is authorized; the one-shot marker is removed on `4a59adb...`.

UNKNOWN:
- why this attempt received no game-server bytes despite valid HTTP session/playdata and successful TCP/WARP setup;
- whether the missing prerequisite is another current-native client message, service/session state, server-side gating/throttling, timing, or another cause;
- whether the promoted `0x34` fallback would be followed by `0x17 LoginSuccess` on a native-success path.

## Next safe discriminator

Do **not** run another game E2E or add classifier-only network instrumentation.

Recover statically on the exact current official Linux client the outbound sequence immediately surrounding the first game-server connection and `TProtocolMessageQueue::sendLogin`: determine whether any additional `GameclientMessage*` (for example `ClientDetails`, `SetClientOptions`, `EnterWorld`, secondary-login/control messages, or another proved message) is sent before the server login-success boundary. Promote only exact-current, causally bound facts. Track B may mutate and spend another E2E only if that research proves a material outbound delta.