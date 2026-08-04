# Canary Current player-owned monster summon appearance

Status: merged through PR `#268`.

## Source provenance

```yaml
producer_repository: blakinio/canary
producer_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
profile: ProtocolProfileId::Current
consumer_repository: blakinio/otclient
consumer_path: oteryn-client/crates/protocol-canary
```

At the pinned producer revision, `Monster::getType()` returns monster type `1`. `ProtocolGame::AddCreature` writes that type in the unknown `0x61` header. After the common payload, it rewrites a monster with a player master to final type `3` and appends the master identity.

```yaml
opcode: 0x6A
position: [x_u16_le, y_u16_le, z_u8]
stack: u8_0_through_9
marker_u16_le: 0x61
cache_eviction_u32_le: 0
entity_id: nonzero_nonlocal
header_type: 1
name: nonempty_domain_bounded
health: 1_through_100
visible_outfit: required
final_type: 3
master_id: nonzero_u32_le
output: GameEvent::EntityAppeared
output_kind: EntityKind::Creature
master_relationship_exposed_to_domain: false
cache_mutation: false
```

Direct header types `3` and `4`, zero master identity, hidden health, invisible outfit, nonzero cache eviction, malformed/truncated messages, trailing bytes and OTCR extensions remain rejected.

## Fixture provenance

The positive summon message is an original inline synthetic already-decrypted logical message. Its coordinates, entity identity, master identity, name and appearance bytes are invented test values. It contains no credentials, private capture, deployed configuration, proprietary assets or copied producer implementation body.

## Validation and audit

```yaml
focused_head: 029782e9246a6a3e5f9663214053b2f302902c15
focused_rust_client_run: 30927430884
focused_windows_job: 92053432011
focused_supply_chain_job: 92053432190
focused_repository_ci_run: 30927437588
focused_repository_required_job: 92053819757
exact_final_head: 392883490dc7a66cfd05094b7bd5af1e58118efa
exact_final_base: b6a76a264c9c1cc62d063fba3c968d1b8582ef8c
exact_rust_client_run: 30928206240
exact_windows_job: 92056006376
exact_supply_chain_job: 92056006319
exact_repository_ci_run: 30928203871
exact_repository_required_job: 92056360956
ready_state_repository_ci_run: 30928649446
ready_state_repository_required_job: 92057728494
focused_audit_comment: 5181653994
exact_final_audit_comment: 5181748881
critical_open: 0
high_open: 0
material_medium_open: 0
unresolved_review_threads: 0
result: PASS
```

## Merge

```yaml
implementation_pr: 268
implementation_merge: 85f3b91ab19114e0b4fd2f1259c7f28a66ea977e
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
```

## Claim boundary

This slice does not claim complete creature compatibility, known-cache reconciliation, item decoding, non-empty map decoding, local-player map strips, live admission or M2 completion. The parent task remains active until every remaining source-proven branch is exhausted and external dependencies are normalized.
