# Canary Current invisible/default outfit appearance

Status: focused implementation validation and fresh audit passed for PR `#270`; current-main exact-final validation remains pending.

## Source provenance

```yaml
producer_repository: blakinio/canary
producer_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
producer_profile: ProtocolProfileId::Current
producer_wire_family: CipsoftVanilla
consumer_repository: blakinio/otclient
consumer_adapter: oteryn-client/crates/protocol-canary
```

`ProtocolGame::AddCreature` passes a default-constructed `Outfit_t` to `AddOutfit` for invisible or ghost creatures. Under Current non-OTCR serialization, the complete default payload is exactly:

```yaml
look_type_u16_le: 0
look_type_ex_u16_le: 0
mount_u16_le: 0
trailing_outfit_bytes: 0
```

Visible outfit serialization remains unchanged: nonzero look type, five color/addon bytes, mount id and four mount color bytes only when mounted.

## Consumer mapping

The shared structural parser is consumed by unknown-player, known-player and non-player/player-summon appearance parsers. These existing adapters already discard outfit values after structural validation, so the change does not add presentation or authority semantics to the domain.

## Fixture provenance

All positive messages are original inline synthetic already-decrypted logical messages. Coordinates, identities, names and outfit bytes are invented test values. No credentials, private captures, deployed configuration or proprietary assets are included.

## Claim boundary

Nonzero `lookTypeEx`, nonzero mount after the zero/default branch, OTCR extensions, hidden-health type `5`, nonzero known-cache eviction, item decoding and local-player map strips remain fail-closed.

## Focused validation

```yaml
implementation_pr: 270
focused_head: d26c308be08474d36deb9b5cd0fff71cdc8a2ec4
rust_client_run: 30931418621
windows_job: 92066803009
supply_chain_job: 92066802553
repository_ci_run: 30931419201
repository_required_job: 92071083755
locked_metadata: PASS
formatting: PASS
strict_workspace_clippy: PASS
workspace_tests: PASS
architecture_policy: PASS
supply_chain: PASS
repository_required_ci: PASS
result: PASS
```

## Fresh audit

```yaml
audit_comment: 5182288763
audited_head: d26c308be08474d36deb9b5cd0fff71cdc8a2ec4
critical_open: 0
high_open: 0
material_medium_open: 0
unresolved_review_threads: 0
result: PASS
```

## Finalization

```yaml
current_main: d52b0a91de4e166b5d95c52715a138041fd4c722
exact_final_head: pending_clean_restack
exact_final_ci: pending
protected_merge: pending
```
