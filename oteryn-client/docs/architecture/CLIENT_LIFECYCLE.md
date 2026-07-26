# Client Lifecycle and Gameplay Channels

## 1. State machine

```text
Booting
  -> CheckingInstallation
  -> Updating | RepairRequired | StartingClient
  -> LoggedOut
  -> Authenticating
  -> AccountReady
  -> SelectingCharacter
  -> SelectingChannel
  -> RequestingGameTicket
  -> ConnectingGame
  -> EnteringGame
  -> InGame
```

Session-ending paths:

```text
InGame
  -> Relogging -> SelectingCharacter | SelectingChannel
  -> Reconnecting -> InGame | Disconnected
  -> GameEnded -> SelectingCharacter
  -> LoggedOut -> LoggedOut
  -> FatalClientError -> Exit
```

Every transition is explicit, cancellable where safe and tied to an owner generation. A delayed result from an earlier authentication, directory request or game connection cannot mutate a newer state.

## 2. Session types

### Account session

Owns authenticated access to Oteryn Platform services, subject to token policy and system credential storage. It may survive multiple game relogs.

### Selection context

Owns the latest server-authoritative character, world and gameplay-channel directory response plus the current user selection. It is refreshed when stale or when the server indicates a revision change.

### Game session

Owns exactly one character connected to exactly one world and gameplay channel. It contains no reusable main-password material. Its session credential is single-use or otherwise bound by the exact server contract.

## 3. Normal login

```text
Authenticate account
 -> load characters/worlds/channels
 -> select character
 -> select world when applicable
 -> select or accept recommended gameplay channel
 -> request one-shot game ticket
 -> receive authoritative routing
 -> connect through protocol adapter
 -> consume ticket once
 -> enter game
```

The client may remember the last selected channel as a preference. The directory/gateway remains authoritative about whether it is available and compatible.

## 4. Gameplay-channel semantics

A gameplay channel is a parallel instance of one world.

Examples:

```text
Oteryn World
├── Channel 1
├── Channel 2
└── Channel 3
```

Channel descriptors are server data. The client may display label, population, queue, region, latency estimate, maintenance status and recommendation when supplied. It must not manufacture authoritative capacity or availability.

This term is separate from transport channels or QUIC streams.

## 5. Relog between channels

Changing Channel 1 to Channel 2 is a relog, not a live transfer:

```text
InGame(Channel 1)
 -> user requests Relog
 -> stop accepting new local gameplay actions
 -> request normal game logout
 -> receive committed game-end or explicit failure
 -> destroy Channel 1 session state
 -> retain valid account session and local UI preferences
 -> select Channel 2
 -> request a new ticket scoped to Channel 2
 -> connect and create a new game session
```

The client must not reuse the Channel 1 game credential for Channel 2.

Session-scoped state is discarded, including target, open containers, local entity handles, temporary effects and pending game commands. User-scoped state may remain, including layout, hotkeys, audio settings and permitted chat presentation preferences.

## 6. Relog failure cases

Typed outcomes include:

- logout denied because server-side conditions are not satisfied;
- logout request timeout;
- old session ended but directory refresh failed;
- selected channel became full/offline;
- ticket expired before connection;
- client/protocol/asset version mismatch;
- account session expired;
- old connection closed unexpectedly.

The application chooses one safe action from:

```text
RetryLogout
ReconnectSameSession
ReturnToSelection
ChooseAnotherChannel
RefreshDirectory
AuthenticateAgain
UpdateOrRepair
Exit
```

The client does not guess whether a failed logout committed persistent server state. It follows the authoritative response or the documented reconnect/lease contract.

## 7. Reconnect

Reconnect is not relog.

Reconnect attempts to resume or recreate the same game session on the same gameplay channel according to the protocol contract. It must not replay a one-shot login ticket unless the server explicitly issues a new resume credential.

Reconnect state records:

- exact game-session identity;
- selected world/channel;
- last acknowledged sequence/tick when supported;
- bounded retry policy;
- session generation;
- reason and user-visible progress.

If the server rejects resume, the client returns to selection or requests a fresh ticket only through the account-session flow.

## 8. Directory freshness

Character/world/channel data has a revision or expiration policy. Before issuing a game ticket, the client verifies that the selected identifiers still belong to the current directory generation.

A refresh preserves user intent only when the same typed identifiers remain valid. Display names are never used as stable routing keys.

## 9. User experience rules

- Login occurs once per valid account session.
- Channel selection is visible during initial entry and relog.
- A recommended channel may be preselected but never silently substituted after the user confirms another channel.
- Full/offline/maintenance states have actionable explanations.
- Relog progress distinguishes closing the old session from opening the new one.
- Account logout is visually and behaviorally distinct from game relog.
- Closing the application follows the game-session shutdown policy but does not claim success without server acknowledgement.

## 10. State ownership

| State | Owner | Lifetime |
|---|---|---|
| PKCE verifier/state/callback nonce | identity transaction | one auth attempt |
| account credentials/session handles | account-session service | account session |
| directory response and selection | world-directory service | directory generation |
| one-shot game ticket | game-entry transaction | one connection attempt |
| transport/protocol state | game-session adapter | one game session |
| mutable world/game state | simulation | one game session |
| feature presentation state | owning feature | feature/session scope |
| device/layout/hotkey preferences | settings | configured persistence scope |

## 11. Required lifecycle tests

- stale authentication callback after a new attempt;
- stale directory response after account logout;
- duplicate game-ticket consumption attempt;
- selected channel disappears during ticket request;
- relog Channel 1 -> Channel 2;
- relog back to Channel 1 with a fresh credential;
- reconnect without replaying the initial ticket;
- old game-session callback after replacement session starts;
- game logout timeout with explicit recovery action;
- account-session expiration during selection;
- repeated login/relog/logout without retained session objects.
