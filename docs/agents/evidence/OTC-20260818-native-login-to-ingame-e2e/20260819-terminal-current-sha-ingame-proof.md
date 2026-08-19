# Current-SHA native login → IN_GAME proof and post-handoff stability result

Task: `OTC-20260818-native-login-to-ingame-e2e`  
PR: `#528`  
Date: 2026-08-19  
Runner/runtime: `synology-otclient-01` / `otclient-track-a-kasmvnc` / `DISPLAY=:1`

## Proven E2E event

```text
RESULT=SUCCESS_AT_PROOF_POINT
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=YES
CAUSAL_PROOF=COMPLETE
STRUCTURAL_IN_GAME=PASS
CURRENTLY_LOGGED_IN_AFTER_LATER_HANDOFF=NO
RESTART_RELOGIN_STABILITY=NOT_PROVEN
```

## Exact client identity at the successful proof point

```text
PID=27368
EXE=/home/kasm-user/otclient-track-a/Tibia-32177065988-1/bin/client
SIZE=52109920
SHA256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
START_TICKS=74880981
PERSISTENT_SECRET_ENVIRONMENT=false
```

The exact SHA/size is the current Track A official-client fence promoted by merged PR #555.

## Native auth handoff discriminator

GitHub Actions run `32233929770`, job `96009597899`, proved the exact current helper/runtime prerequisites and reached the bounded credential step. The one-shot native credential ingress then returned `NATIVE_AUTH_RESPONSE_FAILED` because the native call caused a process handoff/re-exec before `auth.so` could return its IPC response.

Fresh read-only inspection showed that the replacement process used the same exact official executable but had a sanitized environment with no `LD_PRELOAD` and no `OTCLIENT_TIBIA_RE_*` variables. No second credential attempt was made.

A subsequent exact-client restart with the already-proven current-SHA helper set, **without credentials**, restored the authenticated play session and entered the game. No GUI credential entry, OCR, image matching, coordinate login, blind Tab/Return automation, TLS weakening, server-response fabrication, or authentication bypass was used.

## Direct visible proof

A local X11 capture of real `DISPLAY=:1` was inspected directly on Synology at the successful proof point. It showed the Tibia world view with the player character rendered in-game, health/status HUD present, and the application title `Tibia - Gant Elmyn`.

The capture was not committed or uploaded. All local/container screenshot files were deleted after inspection.

## Structural causal proof

On that same live exact process `PID=27368`, the current-SHA runtime bridge independently discovered exactly one validated Qt object for each required in-game discriminator:

```text
player_protocol_handler
  vptr_hits=1
  validated_hits=1
  class=tibia::game::TPlayerProtocolMessageHandler

gameserver_game_session
  vptr_hits=1
  validated_hits=1
  class=tibia::game::TGameserverGameSession

worldmap_handler
  vptr_hits=1
  validated_hits=1
  class=tibia::worldmap::TWorldmapProtocolMessageHandler
```

All three responses came from bridge peer PID `27368`. This proves that the exact current official client genuinely reached the world and owned the expected live game-session structures.

## Post-proof stability check

After the successful proof point, the client performed another process handoff. A fresh bridge `PING` identified exact current client PID `11365`, but the three in-game discriminators each returned `validated_hits=0`. A fresh local `DISPLAY=:1` observation showed the normal Tibia login screen rather than the world view.

Therefore the correct terminal interpretation is:

- the native-login-to-world E2E event **did occur and is causally proven**;
- the resulting session did **not remain stable across the later process handoff**;
- the client is **not currently left logged in**;
- no second bounded credential attempt was made, preserving one-shot secret scope.

## Secret handling

```text
TIBIA_TEST_EMAIL value logged=false
TIBIA_TEST_PASSWORD value logged=false
persistent secret environment=false
second secret attempt after handoff=false
GUI credential entry=false
session secret committed=false
local screenshot artifacts retained=false
```

## Final disposition

```yaml
CURRENT_BUILD_NATIVE_AUTH: PASS_WITH_PROCESS_HANDOFF
VISIBLE_IN_GAME_AT_PROOF_POINT: PASS
STRUCTURAL_IN_GAME_AT_PROOF_POINT: PASS_3_OF_3
CHARACTER_ACTUALLY_LOGGED_INTO_GAME: YES
CAUSAL_PROOF: COMPLETE
CURRENTLY_LOGGED_IN: NO
POST_HANDOFF_SESSION_STABILITY: FAIL_NOT_RETAINED
SECOND_SECRET_ATTEMPT: NOT_PERFORMED
```

The earlier `NATIVE_AUTH_RESPONSE_FAILED` marker is not evidence that authentication itself failed; it is evidence that the helper response channel was lost across the native process handoff. The later visible + structural in-game proof resolves the E2E event, while the subsequent handoff establishes a separate remaining stability defect.