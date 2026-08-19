# Terminal current-SHA native login → IN_GAME proof

Task: `OTC-20260818-native-login-to-ingame-e2e`  
PR: `#528`  
Date: 2026-08-19  
Runner/runtime: `synology-otclient-01` / `otclient-track-a-kasmvnc` / `DISPLAY=:1`

## Result

```text
RESULT=SUCCESS
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=YES
CAUSAL_PROOF=COMPLETE
STRUCTURAL_IN_GAME=PASS
```

## Exact client identity

The live post-auth proof process was revalidated directly in the Kasm container:

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

GitHub Actions run `32233929770`, job `96009597899`, proved:

```text
CURRENT_HELPER_SET=PASS
HELPER_RUNTIME_RELAUNCH=PASS
SECRET_ACCESS=false   # before the bounded auth step
```

The bounded one-shot native credential ingress then returned `NATIVE_AUTH_RESPONSE_FAILED` after the native call caused a process handoff/re-exec before the helper could return its response. This was initially classified as a transport failure.

Fresh read-only inspection of the resulting exact client showed that the replacement process had the same exact executable but a sanitized environment with no `LD_PRELOAD` and no `OTCLIENT_TIBIA_RE_*` variables. No second credential attempt was made at that point.

A subsequent exact-client restart with the already-proven current-SHA helper set, **without credentials**, restored the helper observation channel. The client restored the authenticated play session and entered the game. No GUI credential entry, OCR, image matching, coordinate login, blind Tab/Return automation, TLS weakening, server-response fabrication, or authentication bypass was used.

## Direct visible runtime proof

A local X11 capture of real `DISPLAY=:1` was inspected directly on Synology. It showed the Tibia world view with the player character rendered in-game, health/status HUD present, and the application title `Tibia - Gant Elmyn`.

The capture was used only for direct local observation and was **not committed or uploaded as repository evidence**.

## Structural causal proof

On the same live exact process `PID=27368`, the current-SHA runtime bridge independently discovered exactly one validated Qt object for each required in-game discriminator:

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

All three responses came from bridge peer PID `27368`.

Therefore the final E2E claim is not based only on a screenshot or UI state: the exact current official binary is visibly in the world and simultaneously owns all three exact-build structural game-session objects.

## Secret handling

```text
TIBIA_TEST_EMAIL value logged=false
TIBIA_TEST_PASSWORD value logged=false
persistent secret environment=false
second secret attempt after handoff=false
GUI credential entry=false
session secret committed=false
```

The owner-authorized bounded GitHub Secrets ingress was the only credential-bearing path used.

## Final disposition

```yaml
CURRENT_BUILD_NATIVE_AUTH: PASS_WITH_PROCESS_HANDOFF
CURRENT_BUILD_SESSION_RESTORE_WITHOUT_REENTERING_CREDENTIALS: PASS
VISIBLE_IN_GAME: PASS
STRUCTURAL_IN_GAME: PASS_3_OF_3
CHARACTER_ACTUALLY_LOGGED_INTO_GAME: YES
CAUSAL_PROOF: COMPLETE
```

The earlier `NATIVE_AUTH_RESPONSE_FAILED` marker is superseded as a terminal result: it represented loss of the helper response across the native client handoff, not failure to authenticate. The later no-secret session restoration plus exact-process structural proof resolves that ambiguity.