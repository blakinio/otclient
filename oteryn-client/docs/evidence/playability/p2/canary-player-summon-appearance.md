# Canary Current player-owned monster summon appearance

Status: focused implementation validation and fresh audit passed for PR `#268`; current-main exact-head validation remains pending.

## Source provenance

```yaml
producer_repository: blakinio/canary
producer_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
profile: ProtocolProfileId::Current
consumer_repository: blakinio/otclient
consumer_path: oteryn-client/crates/protocol-canary
```

At the pinned producer revision, `Monster::getType()` returns monster type `1`. `ProtocolGame::AddCreature` writes that type in the unknown `0x61` header. After the common payload, it rewrites a monster with a player master to final type `3` and appends the master identity. Therefore the admitted source-reachable branch is:

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

## Focused validation

```yaml
validated_head: 029782e9246a6a3e5f9663214053b2f302902c15
rust_client_run: 30927430884
windows_job: 92053432011
supply_chain_job: 92053432190
repository_ci_run: 30927437588
repository_required_job: 92053819757
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
audit_comment: 5181653994
audited_head: 029782e9246a6a3e5f9663214053b2f302902c15
critical_open: 0
high_open: 0
material_medium_open: 0
unresolved_review_threads: 0
result: PASS
```

## Finalization

```yaml
current_main: b6a76a264c9c1cc62d063fba3c968d1b8582ef8c
exact_final_head: pending_clean_restack
exact_final_ci: pending
protected_merge: pending
```

## Claim boundary

This slice does not claim complete creature compatibility, known-cache reconciliation, item decoding, non-empty map decoding, local-player map strips, live admission or M2 completion. The parent task remains active until every remaining source-proven branch is exhausted and external dependencies are normalized.
