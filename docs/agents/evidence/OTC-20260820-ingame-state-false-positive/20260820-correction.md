# Surveyor in-game false-positive correction

Date: 2026-08-20

## Verified contradiction

A fresh read-only observation of the exact Track A Kasm runtime showed the official client at the login form, not in the game world. The observed top-level Tibia window belonged to PID `19590` and had the non-character title `Tibia`.

At the same observation point, the native bridge socket peer was also PID `19590` and all three existing structural targets still returned a successful scan with exactly one validated hit:

```text
player_protocol_handler  peer_ok=true  scan_status=OK  validated_hits=1
gameserver_game_session  peer_ok=true  scan_status=OK  validated_hits=1
worldmap_handler          peer_ok=true  scan_status=OK  validated_hits=1
```

This directly falsifies the rule that `BRIDGE_3_OF_3` alone proves `IN_GAME`. The three objects may persist or be instantiated while the client is logged out.

## Privacy handling

The read-only screen capture was used only to verify the visible state and was immediately deleted from both the container and host. It is not committed or retained because the login form contained account-identifying text. No credential values were read, copied, logged, or persisted by this correction task.

## Evidence disposition

Final Surveyor run `32362197404` remains valid evidence for:

- exact declared runtime namespace and target identity;
- passive collector execution;
- 169-row coverage bundle;
- 12/12 alias views;
- `missing-readers.json` generation;
- privacy scan PASS;
- manifest integrity;
- no runtime mutation and no credential access.

The same run is **not** valid evidence for:

- `STRUCTURAL_IN_GAME=PASS`;
- `OWNER_LOGIN_REQUIRED=NO`;
- active-world semantic state.

Those two verdict fields are superseded by this correction and must fail closed to `UNKNOWN` until a separate reviewed semantic/causal active-world discriminator exists.

## Canonical registration impact

A fresh allowlisted read of the canonical registration showed that it still contains `state=IN_GAME` with `state_evidence=BRIDGE_3_OF_3` for the same exact PID/client identity and lease generation 17. That semantic state is therefore stale/incorrect and must not authorize later mutation. This repair makes adoption-aware canonical validation fail closed on `IN_GAME` when bridge 3-of-3 is the only semantic evidence. The existing registration file is not manually edited by this repository task.
