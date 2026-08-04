# Canary Current invisible/default outfit appearance

Status: merged through PR `#270`.

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

Visible outfits remain unchanged: nonzero look type, five color/addon bytes, mount id and four mount color bytes only when mounted.

## Consumer mapping

One shared structural parser is consumed by unknown-player, known-player and non-player/player-summon appearance parsers. Outfit bytes remain structural only and do not add presentation or authority semantics to the domain.

## Validation and audit

```yaml
focused_head: d26c308be08474d36deb9b5cd0fff71cdc8a2ec4
focused_rust_client_run: 30931418621
focused_windows_job: 92066803009
focused_supply_chain_job: 92066802553
focused_repository_ci_run: 30931419201
focused_repository_required_job: 92071083755
exact_final_head: 518fbe27ee85ae943110bad6ce693bbebadab016
exact_final_base: d52b0a91de4e166b5d95c52715a138041fd4c722
exact_rust_client_run: 30933043153
exact_windows_job: 92072249531
exact_supply_chain_job: 92072249589
exact_repository_ci_run: 30933043306
exact_repository_required_job: 92073142000
ready_state_repository_ci_run: 30933437515
ready_state_repository_required_job: 92074052297
focused_audit_comment: 5182288763
exact_final_audit_comment: 5182367276
critical_open: 0
high_open: 0
material_medium_open: 0
unresolved_review_threads: 0
result: PASS
```

## Merge

```yaml
implementation_pr: 270
implementation_merge: 8002e2b51d9f0ba825f788815d814aed5101c925
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
```

## Claim boundary

Nonzero `lookTypeEx`, nonzero default-branch mount, OTCR extensions, hidden-health type `5`, nonzero known-cache eviction, item decoding and local-player map strips remain fail-closed. No live gameplay or M2 completion claim is made.
