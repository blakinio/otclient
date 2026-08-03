from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, found {count}")
    return text.replace(old, new, 1)


root = Path(".")
inbound_path = root / "oteryn-client/crates/protocol-canary/src/inbound.rs"
inbound = inbound_path.read_text(encoding="utf-8")

inbound = replace_once(
    inbound,
    "    DomainError, GameEvent, GameEventEnvelope, SessionEndReason, SessionToken,\n",
    "    DomainError, EntityHandle, EntityId, GameEvent, GameEventEnvelope, SessionEndReason,\n"
    "    SessionToken,\n",
    "domain imports",
)

inbound = replace_once(
    inbound,
    "/// Canary Current server opcode for the pending-state-entered bootstrap boundary.\n"
    "pub const OPCODE_PENDING_STATE_ENTERED: u8 = 0x0A;\n"
    "/// Canary Current server opcode for terminal session-end information.\n"
    "pub const OPCODE_SESSION_END_INFORMATION: u8 = 0x18;\n\n"
    "const SESSION_END_LOGOUT: u8 = 0x00;\n",
    "/// Canary Current server opcode for local-player initialization.\n"
    "pub const OPCODE_LOCAL_PLAYER_INITIALIZATION: u8 = 0x17;\n"
    "/// Canary Current server opcode for the pending-state-entered bootstrap boundary.\n"
    "pub const OPCODE_PENDING_STATE_ENTERED: u8 = 0x0A;\n"
    "/// Canary Current server opcode for the enter-world bootstrap boundary.\n"
    "pub const OPCODE_ENTER_WORLD: u8 = 0x0F;\n"
    "/// Canary Current server opcode for terminal session-end information.\n"
    "pub const OPCODE_SESSION_END_INFORMATION: u8 = 0x18;\n\n"
    "const CURRENT_LOGIN_SPEED_PRECISION: u8 = 3;\n"
    "const CURRENT_LOGIN_SPEED_COMPONENTS: usize = 3;\n"
    "const SESSION_END_LOGOUT: u8 = 0x00;\n",
    "bootstrap opcodes",
)

inbound = replace_once(
    inbound,
    "pub struct CanaryInboundBootstrapState {\n"
    "    session: SessionToken,\n"
    "    pending_state_entered: bool,\n"
    "    session_ended: bool,\n"
    "}\n",
    "pub struct CanaryInboundBootstrapState {\n"
    "    session: SessionToken,\n"
    "    local_player: Option<EntityHandle>,\n"
    "    pending_state_entered: bool,\n"
    "    enter_world_received: bool,\n"
    "    session_ended: bool,\n"
    "}\n",
    "bootstrap state fields",
)

inbound = replace_once(
    inbound,
    "        Self {\n"
    "            session,\n"
    "            pending_state_entered: false,\n"
    "            session_ended: false,\n"
    "        }\n",
    "        Self {\n"
    "            session,\n"
    "            local_player: None,\n"
    "            pending_state_entered: false,\n"
    "            enter_world_received: false,\n"
    "            session_ended: false,\n"
    "        }\n",
    "bootstrap constructor",
)

inbound = replace_once(
    inbound,
    "    /// Return whether the pending-state boundary was already accepted.\n",
    "    /// Return the normalized session-scoped local-player handle, when proven.\n"
    "    #[must_use]\n"
    "    pub const fn local_player(self) -> Option<EntityHandle> {\n"
    "        self.local_player\n"
    "    }\n\n"
    "    /// Return whether the pending-state boundary was already accepted.\n",
    "local player getter",
)

inbound = replace_once(
    inbound,
    "    /// Return whether a terminal session-end boundary was already accepted.\n",
    "    /// Return whether the enter-world boundary was already accepted.\n"
    "    #[must_use]\n"
    "    pub const fn enter_world_received(self) -> bool {\n"
    "        self.enter_world_received\n"
    "    }\n\n"
    "    /// Decode the exact Current local-player initialization logical message.\n"
    "    ///\n"
    "    /// # Errors\n"
    "    ///\n"
    "    /// Returns the same fail-closed errors as\n"
    "    /// [`decode_current_local_player_initialization`].\n"
    "    pub fn decode_local_player_initialization(\n"
    "        &mut self,\n"
    "        input: &[u8],\n"
    "        current: SessionGeneration,\n"
    "    ) -> Result<EntityHandle, CanaryInboundError> {\n"
    "        decode_current_local_player_initialization(input, self, current)\n"
    "    }\n\n"
    "    /// Decode the exact Current one-byte enter-world logical message.\n"
    "    ///\n"
    "    /// # Errors\n"
    "    ///\n"
    "    /// Returns the same fail-closed errors as [`decode_current_enter_world`].\n"
    "    pub fn decode_enter_world(\n"
    "        &mut self,\n"
    "        input: &[u8],\n"
    "        current: SessionGeneration,\n"
    "    ) -> Result<(), CanaryInboundError> {\n"
    "        decode_current_enter_world(input, self, current)\n"
    "    }\n\n"
    "    /// Return whether a terminal session-end boundary was already accepted.\n",
    "bootstrap methods",
)

pending_anchor = "/// Decode the exact Current `sendPendingStateEntered` logical message.\n"
new_decoders = r'''/// Decode the exact Current local-player branch of `sendAddCreature`.
///
/// The pinned Current profile is client version 1525, non-legacy and enables
/// `LoginSpeedFormula`. Its local-player initialization message is therefore:
/// opcode `0x17`, player id `u32`, server beat `u16`, three encoded doubles
/// (`precision=3` plus `u32` each), two fixed zero capability bytes, one opaque
/// `u16`-length store URL, coin-packet `u16`, and one boolean exiva flag.
///
/// The store URL bytes and numeric tuning values are validated structurally but
/// are not retained or exposed. Success normalizes only the non-zero creature id
/// into one session-fenced protocol-neutral [`EntityHandle`]. No simulation event
/// is emitted because the message contains no player position.
///
/// # Errors
///
/// Rejects stale or invalid order, malformed field widths, non-Current precision,
/// non-zero fixed capability bytes, an invalid exiva flag, a zero player id,
/// oversized input and every trailing byte. State changes only after complete
/// parsing and handle validation.
pub fn decode_current_local_player_initialization(
    input: &[u8],
    state: &mut CanaryInboundBootstrapState,
    current: SessionGeneration,
) -> Result<EntityHandle, CanaryInboundError> {
    state.session.ensure_current(current)?;
    if state.local_player.is_some()
        || state.pending_state_entered
        || state.enter_world_received
        || state.session_ended
    {
        return Err(CanaryInboundError::InvalidOrder);
    }

    let mut reader = BoundedReader::new(input, CANARY_NETWORK_MESSAGE_MAX_BYTES)?;
    let opcode = reader.read_u8()?;
    if opcode != OPCODE_LOCAL_PLAYER_INITIALIZATION {
        return Err(ProtocolError::new(ProtocolErrorKind::UnknownValue).into());
    }

    let player_id = reader.read_u32_le()?;
    let _server_beat = reader.read_u16_le()?;
    for _ in 0..CURRENT_LOGIN_SPEED_COMPONENTS {
        if reader.read_u8()? != CURRENT_LOGIN_SPEED_PRECISION {
            return Err(ProtocolError::new(ProtocolErrorKind::UnknownValue).into());
        }
        let _scaled_speed = reader.read_u32_le()?;
    }

    if reader.read_u8()? != 0 || reader.read_u8()? != 0 {
        return Err(ProtocolError::new(ProtocolErrorKind::UnknownValue).into());
    }

    let store_url_length = usize::from(reader.read_u16_le()?);
    let _store_url = reader.read_exact(store_url_length)?;
    let _coin_packet = reader.read_u16_le()?;
    if !matches!(reader.read_u8()?, 0 | 1) {
        return Err(ProtocolError::new(ProtocolErrorKind::UnknownValue).into());
    }
    reader.finish(TrailingDataPolicy::Reject)?;

    let player = EntityHandle::new(state.session, EntityId::try_new(player_id)?);
    player.ensure_session(state.session)?;
    state.local_player = Some(player);
    Ok(player)
}

/// Decode the exact Current `sendEnterWorld` logical message.
///
/// This one-byte boundary advances only caller-owned bootstrap order. It does not
/// emit [`GameEvent::BootstrapCompleted`], because the producer message contains
/// no position. A later fully validated map-description family must provide that
/// position before simulation bootstrap can complete.
///
/// # Errors
///
/// Rejects stale state, missing local-player identity or pending-state boundary,
/// duplicate/terminal order, wrong opcode, oversized input and trailing bytes.
pub fn decode_current_enter_world(
    input: &[u8],
    state: &mut CanaryInboundBootstrapState,
    current: SessionGeneration,
) -> Result<(), CanaryInboundError> {
    state.session.ensure_current(current)?;
    if state.local_player.is_none()
        || !state.pending_state_entered
        || state.enter_world_received
        || state.session_ended
    {
        return Err(CanaryInboundError::InvalidOrder);
    }

    let mut reader = BoundedReader::new(input, CANARY_NETWORK_MESSAGE_MAX_BYTES)?;
    if reader.read_u8()? != OPCODE_ENTER_WORLD {
        return Err(ProtocolError::new(ProtocolErrorKind::UnknownValue).into());
    }
    reader.finish(TrailingDataPolicy::Reject)?;
    state.enter_world_received = true;
    Ok(())
}

'''
inbound = replace_once(inbound, pending_anchor, new_decoders + pending_anchor, "new decoders")

inbound = replace_once(
    inbound,
    "    const SESSION_END_TRAILING_FIXTURE: &str = include_str!(\n"
    "        \"../../../tests/integration/canary-world-protocol/fixtures/session-end-trailing.hex\"\n"
    "    );\n",
    "    const SESSION_END_TRAILING_FIXTURE: &str = include_str!(\n"
    "        \"../../../tests/integration/canary-world-protocol/fixtures/session-end-trailing.hex\"\n"
    "    );\n"
    "    const LOCAL_PLAYER_INITIALIZATION_FIXTURE: &str = include_str!(\n"
    "        \"../../../tests/integration/canary-world-protocol/fixtures/local-player-initialization.hex\"\n"
    "    );\n"
    "    const LOCAL_PLAYER_BAD_PRECISION_FIXTURE: &str = include_str!(\n"
    "        \"../../../tests/integration/canary-world-protocol/fixtures/local-player-bad-precision.hex\"\n"
    "    );\n"
    "    const LOCAL_PLAYER_ZERO_ID_FIXTURE: &str = include_str!(\n"
    "        \"../../../tests/integration/canary-world-protocol/fixtures/local-player-zero-id.hex\"\n"
    "    );\n"
    "    const LOCAL_PLAYER_TRAILING_FIXTURE: &str = include_str!(\n"
    "        \"../../../tests/integration/canary-world-protocol/fixtures/local-player-trailing.hex\"\n"
    "    );\n"
    "    const ENTER_WORLD_FIXTURE: &str = include_str!(\n"
    "        \"../../../tests/integration/canary-world-protocol/fixtures/enter-world.hex\"\n"
    "    );\n",
    "fixture constants",
)

index_test_anchor = "    #[test]\n    fn generated_index_contains_exact_pending_state_entry() {\n"
new_tests = r'''    #[test]
    fn exact_local_player_initialization_stores_only_domain_handle() -> Result<(), Box<dyn Error>> {
        let (mut state, current) = state(30);
        let input = parse_hex_fixture(LOCAL_PLAYER_INITIALIZATION_FIXTURE)?;

        let player = state.decode_local_player_initialization(&input, current)?;

        assert_eq!(player.id().get(), 0x0102_0304);
        assert_eq!(state.local_player(), Some(player));
        assert!(!state.pending_state_entered());
        assert!(!state.enter_world_received());
        assert!(!state.session_ended());
        let debug = format!("{state:?}");
        assert!(!debug.contains("synthetic://store"));
        Ok(())
    }

    #[test]
    fn malformed_local_player_initialization_is_atomic() -> Result<(), Box<dyn Error>> {
        let bad_precision = parse_hex_fixture(LOCAL_PLAYER_BAD_PRECISION_FIXTURE)?;
        let trailing = parse_hex_fixture(LOCAL_PLAYER_TRAILING_FIXTURE)?;
        let (_, current) = state(31);
        for (input, expected) in [
            (&[][..], ProtocolErrorKind::Truncated),
            (&[0x16][..], ProtocolErrorKind::UnknownValue),
            (&bad_precision[..], ProtocolErrorKind::UnknownValue),
            (&trailing[..], ProtocolErrorKind::TrailingData),
        ] {
            let (mut state, _) = state(31);
            assert_eq!(
                state.decode_local_player_initialization(input, current),
                Err(CanaryInboundError::Protocol(ProtocolError::new(expected)))
            );
            assert_eq!(state.local_player(), None);
        }
        Ok(())
    }

    #[test]
    fn zero_or_stale_local_player_identity_fails_closed() -> Result<(), Box<dyn Error>> {
        let zero_id = parse_hex_fixture(LOCAL_PLAYER_ZERO_ID_FIXTURE)?;
        let (mut zero_state, current) = state(32);
        assert!(matches!(
            zero_state.decode_local_player_initialization(&zero_id, current),
            Err(CanaryInboundError::Domain(DomainError::ZeroIdentifier(_)))
        ));
        assert_eq!(zero_state.local_player(), None);

        let valid = parse_hex_fixture(LOCAL_PLAYER_INITIALIZATION_FIXTURE)?;
        let (mut stale, _) = state(33);
        assert!(matches!(
            stale.decode_local_player_initialization(&valid, SessionGeneration::new(34)),
            Err(CanaryInboundError::Domain(DomainError::StaleSession { .. }))
        ));
        assert_eq!(stale.local_player(), None);
        Ok(())
    }

    #[test]
    fn oversized_local_player_initialization_fails_before_state_change() {
        let (mut state, current) = state(35);
        let input = vec![OPCODE_LOCAL_PLAYER_INITIALIZATION; CANARY_NETWORK_MESSAGE_MAX_BYTES + 1];
        assert_eq!(
            state.decode_local_player_initialization(&input, current),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::Oversized
            )))
        );
        assert_eq!(state.local_player(), None);
    }

    #[test]
    fn exact_bootstrap_order_reaches_enter_world_without_claiming_completion(
    ) -> Result<(), Box<dyn Error>> {
        let local = parse_hex_fixture(LOCAL_PLAYER_INITIALIZATION_FIXTURE)?;
        let pending = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;
        let enter = parse_hex_fixture(ENTER_WORLD_FIXTURE)?;
        let (mut state, current) = state(36);

        assert_eq!(
            state.decode_enter_world(&enter, current),
            Err(CanaryInboundError::InvalidOrder)
        );
        state.decode_local_player_initialization(&local, current)?;
        decode_current_pending_state_entered(&pending, &mut state, current)?;
        state.decode_enter_world(&enter, current)?;

        assert!(state.local_player().is_some());
        assert!(state.pending_state_entered());
        assert!(state.enter_world_received());
        assert!(!state.session_ended());
        assert_eq!(
            state.decode_enter_world(&enter, current),
            Err(CanaryInboundError::InvalidOrder)
        );
        Ok(())
    }

    #[test]
    fn malformed_enter_world_does_not_advance_order() -> Result<(), Box<dyn Error>> {
        let local = parse_hex_fixture(LOCAL_PLAYER_INITIALIZATION_FIXTURE)?;
        let pending = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;
        let (mut state, current) = state(37);
        state.decode_local_player_initialization(&local, current)?;
        decode_current_pending_state_entered(&pending, &mut state, current)?;

        for (input, expected) in [
            (&[][..], ProtocolErrorKind::Truncated),
            (&[0x10][..], ProtocolErrorKind::UnknownValue),
            (&[OPCODE_ENTER_WORLD, 0x00][..], ProtocolErrorKind::TrailingData),
        ] {
            assert_eq!(
                state.decode_enter_world(input, current),
                Err(CanaryInboundError::Protocol(ProtocolError::new(expected)))
            );
            assert!(!state.enter_world_received());
        }
        Ok(())
    }

    #[test]
    fn terminal_session_prevents_identity_and_enter_world_advancement(
    ) -> Result<(), Box<dyn Error>> {
        let local = parse_hex_fixture(LOCAL_PLAYER_INITIALIZATION_FIXTURE)?;
        let enter = parse_hex_fixture(ENTER_WORLD_FIXTURE)?;
        let ended = parse_hex_fixture(SESSION_END_LOGOUT_FIXTURE)?;
        let (mut state, current) = state(38);
        state.decode_session_end_information(&ended, current)?;
        assert_eq!(
            state.decode_local_player_initialization(&local, current),
            Err(CanaryInboundError::InvalidOrder)
        );
        assert_eq!(
            state.decode_enter_world(&enter, current),
            Err(CanaryInboundError::InvalidOrder)
        );
        Ok(())
    }

    #[test]
    fn generated_index_contains_exact_enter_world_entry() {
        assert!(generated_index_contains_entry(
            "unclassified",
            "sendEnterWorld",
            OPCODE_ENTER_WORLD,
            8512,
        ));
    }

'''
inbound = replace_once(inbound, index_test_anchor, new_tests + index_test_anchor, "bootstrap tests")
inbound_path.write_text(inbound, encoding="utf-8", newline="\n")

lib_path = root / "oteryn-client/crates/protocol-canary/src/lib.rs"
lib = lib_path.read_text(encoding="utf-8")
lib = replace_once(
    lib,
    "pub use inbound::{\n"
    "    CanaryInboundBootstrapState, CanaryInboundError, OPCODE_PENDING_STATE_ENTERED,\n"
    "    decode_current_pending_state_entered,\n"
    "};\n",
    "pub use inbound::{\n"
    "    CanaryInboundBootstrapState, CanaryInboundError, OPCODE_ENTER_WORLD,\n"
    "    OPCODE_LOCAL_PLAYER_INITIALIZATION, OPCODE_PENDING_STATE_ENTERED,\n"
    "    decode_current_enter_world, decode_current_local_player_initialization,\n"
    "    decode_current_pending_state_entered,\n"
    "};\n",
    "inbound exports",
)
lib_path.write_text(lib, encoding="utf-8", newline="\n")

fixtures = root / "oteryn-client/tests/integration/canary-world-protocol/fixtures"
positive = """17 04 03 02 01 32 00\n03 FF FF FF 7F\n03 00 00 00 80\n03 01 00 00 80\n00 00\n11 00 73 79 6E 74 68 65 74 69 63 3A 2F 2F 73 74 6F 72 65\n19 00 00\n"""
(fixtures / "local-player-initialization.hex").write_text(positive, encoding="utf-8", newline="\n")
(fixtures / "local-player-bad-precision.hex").write_text(
    positive.replace("03 FF FF FF 7F", "04 FF FF FF 7F", 1), encoding="utf-8", newline="\n"
)
(fixtures / "local-player-zero-id.hex").write_text(
    positive.replace("17 04 03 02 01", "17 00 00 00 00", 1), encoding="utf-8", newline="\n"
)
(fixtures / "local-player-trailing.hex").write_text(positive + "00\n", encoding="utf-8", newline="\n")
(fixtures / "enter-world.hex").write_text("0F\n", encoding="utf-8", newline="\n")

readme_path = fixtures / "README.md"
readme = readme_path.read_text(encoding="utf-8")
readme = replace_once(
    readme,
    "- pending-state producer: `sendPendingStateEntered`, source line 8502\n",
    "- local-player producer: Current/non-legacy local branch of `sendAddCreature`, source body beginning after `sendAllowBugReport`\n"
    "- pending-state producer: `sendPendingStateEntered`, source line 8502\n"
    "- enter-world producer: `sendEnterWorld`, source line 8512\n",
    "fixture provenance",
)
readme = replace_once(
    readme,
    "The fixtures contain no credential, session key, private capture, proprietary asset byte or copied producer implementation body. Unknown session-end reason `0x01` and trailing data are negative cases and must fail closed.\n",
    "The fixtures contain no credential, session key, private capture, proprietary asset byte or copied producer implementation body. The local-player values and store URL are original synthetic field values used only to exercise the proven Current layout; the URL is never exposed by the decoder. Unknown session-end reason `0x01`, invalid login precision, zero identity and trailing data are negative cases and must fail closed.\n",
    "fixture policy",
)
readme_path.write_text(readme, encoding="utf-8", newline="\n")

evidence_path = root / "oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md"
evidence = evidence_path.read_text(encoding="utf-8")
evidence = replace_once(
    evidence,
    "Status: bounded pending-state and known session-end inbound families are merged; the parent task is blocked on complete remaining layouts and identity resolution.  \n",
    "Status: local-player identity and enter-world bootstrap normalization are under exact-head validation; pending-state and known session-end families remain merged.  \n",
    "evidence status",
)
identity_section = r'''## Proven local-player identity and enter-world boundaries

The exact Current/non-legacy local-player branch of `sendAddCreature` precedes
`sendPendingStateEntered`, `sendEnterWorld` and `sendMapDescription`. At client
version 1525 with `LoginSpeedFormula` enabled, its first logical message has the
complete structural layout:

```yaml
local_player_initialization:
  opcode_u8: 0x17
  player_id_u32_le: non_zero
  server_beat_u16_le: opaque_timing_value
  speed_formula_components: 3
  each_speed_component:
    precision_u8: 3
    scaled_value_u32_le: opaque_tuning_value
  pvp_framing_change_u8: 0
  expert_mode_u8: 0
  store_url: u16_length_plus_opaque_bytes
  store_coin_packet_u16_le: opaque_configuration_value
  exiva_enabled_u8: boolean
semantic_normalization:
  retained: session_fenced_EntityHandle
  discarded: timing_speed_store_and_capability_values
  emitted_event: none
```

`sendEnterWorld` is exactly one byte `0x0F`. The caller-owned bootstrap state
accepts it only after local-player identity and pending-state entry. It records
order but emits no `BootstrapCompleted`, because position remains absent until a
complete map-description family is validated. This closes local identity
ownership without partially mutating simulation or exposing Canary-specific
configuration fields.

Original synthetic fixtures use invented field values and a synthetic store URL;
no producer body, private capture, credential or deployed configuration is copied.

'''
evidence = replace_once(
    evidence,
    "## Proven inbound pending-state boundary\n",
    identity_section + "## Proven inbound pending-state boundary\n",
    "identity evidence section",
)
evidence = replace_once(
    evidence,
    "| session bootstrap | `PARTIAL` | `sendPendingStateEntered` is `PROVEN` and implemented. `sendEnterWorld` is a proven one-byte `0x0F` layout at line 8512, but it carries neither local-player identity nor position required by `GameEvent::BootstrapCompleted`; semantic completion is `BLOCKED`. |\n",
    "| session bootstrap | `PARTIAL` | Current local-player `0x17` identity, pending-state `0x0A` and enter-world `0x0F` are `PROVEN` and normalized in exact source order. The map-description position and complete nested map body remain required before `GameEvent::BootstrapCompleted`; semantic completion is `BLOCKED`. |\n",
    "readiness row",
)
active_phase = r'''## Active bootstrap identity validation phase

```yaml
phase: bootstrap-identity-and-enter-world-normalization
branch: feat/OTC2-20260803-canary-bootstrap-identity
base: c91a5872a66cd9a31add2f3f1efc79ceefe7d150
new_layouts:
  - current_local_player_initialization_0x17
  - enter_world_0x0F_order_boundary
identity_contract:
  owner: caller_owned_CanaryInboundBootstrapState
  mapping: nonzero_Canary_creature_id_to_session_fenced_EntityHandle
  raw_id_escape: false
  map_stack_identity: unresolved
simulation_mutation: false
real_admission_changed: false
validation: running
```

'''
evidence = replace_once(
    evidence,
    "## Terminal validation checkpoint\n",
    active_phase + "## Terminal validation checkpoint\n",
    "active evidence checkpoint",
)
evidence_path.write_text(evidence, encoding="utf-8", newline="\n")

task_path = root / "docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md"
task = task_path.read_text(encoding="utf-8")
task = replace_once(task, "status: blocked\n", "status: validating\n", "task status")
task = replace_once(
    task,
    "phase: inbound-provenance-and-identity-contract-blocker\n",
    "phase: bootstrap-identity-and-enter-world-normalization\n",
    "task phase",
)
task = replace_once(
    task,
    "branch: docs/OTC2-20260803-canary-p2-barrier-refresh\n",
    "branch: feat/OTC2-20260803-canary-bootstrap-identity\n",
    "task branch",
)
task = replace_once(task, "updated: 2026-08-03T13:58:00+02:00\n", "updated: 2026-08-03T14:55:00+02:00\n", "task updated")
task = replace_once(
    task,
    'required_base_commit: "bf764ee5c3cb546f5507fc1fbb2b7cad79a00cd0"\n',
    'required_base_commit: "c91a5872a66cd9a31add2f3f1efc79ceefe7d150"\n',
    "task base",
)
task = replace_once(
    task,
    "related_prs: [188, 190, 191, 192, 193, 194, 195, 196, 198, 199, 200, 201, 202]\n",
    "related_prs: [188, 190, 191, 192, 193, 194, 195, 196, 198, 199, 200, 201, 202, 203]\n",
    "task related prs",
)
task = replace_once(task, "last_progress_at: 2026-08-03T13:58:00+02:00\n", "last_progress_at: 2026-08-03T14:55:00+02:00\n", "task progress")
task = replace_once(task, "ci_check_generation: blocker-refresh\n", "ci_check_generation: bootstrap-identity-focused\n", "task generation")
phase_section = r'''# Active bootstrap identity phase

Exact source review established two complete Current bootstrap layouts that do
not require map inference:

```yaml
local_player_initialization:
  source: ProtocolGame::sendAddCreature local-player branch
  opcode: 0x17
  result: normalize nonzero creature id to session-fenced EntityHandle
  retained_configuration: none
enter_world:
  source: ProtocolGame::sendEnterWorld
  bytes: [0x0F]
  prerequisite: local identity plus pending-state boundary
  result: caller-owned order transition only
bootstrap_completed: not_emitted_without_validated_map_position
```

This phase does not relax real admission, parse map contents, mutate simulation,
add a domain event or claim M2. General position/stack identity resolution remains
unresolved; only the producer-supplied local creature id is normalized.

'''
task = replace_once(task, "# Completed protocol slices\n", phase_section + "# Completed protocol slices\n", "task phase section")
stop_old = "The accepted evidence at the pinned source revision remains unchanged. It does not establish complete Current map/entity/movement/removal layouts or an accepted owner for position/stack-to-domain-handle identity resolution. Guessing either contract is forbidden. The parent task remains active and blocked; it is not archived and exclusive protocol ownership remains held. No shared lease is retained.\n"
stop_new = "The exact source now establishes local-player identity and enter-world order without inference, so those bounded transitions are being validated. Complete Current map/entity/movement/removal layouts and general position/stack-to-domain-handle identity resolution remain unavailable. The parent task stays active, exclusive protocol ownership remains held and no shared lease is retained.\n"
task = replace_once(task, stop_old, stop_new, "task stop condition")
checkpoint_start = task.index("# Durable checkpoint\n")
task = task[:checkpoint_start] + r'''# Durable checkpoint

```yaml
checkpoint_version: 17
updated_at: 2026-08-03T14:55:00+02:00
observed_main: c91a5872a66cd9a31add2f3f1efc79ceefe7d150
status: validating
phase: bootstrap-identity-and-enter-world-normalization
branch: feat/OTC2-20260803-canary-bootstrap-identity
new_contracts:
  local_player_identity:
    opcode: 0x17
    output: session_fenced_EntityHandle
    raw_configuration_retained: false
  enter_world:
    opcode: 0x0F
    output: caller_owned_order_state
    bootstrap_completed_emitted: false
validation: focused_workflow_running
p2_barrier:
  simulation_snapshot: archived
  asset_decode: archived
  renderer_resource: archived
  input_platform: archived
  canary_world_protocol: active_validating
  visible_world_integration: not_ready
shared_path_lease: []
ownership:
  protocol_canary: retained_by_parent_task
  shared_paths: released
remaining_blocker: Complete provenance-safe Current map/entity/movement/removal layouts and general position/stack-to-domain-handle identity resolution remain unavailable.
next_action: Validate and merge the exact local-player/enter-world phase, then resume full map-description normalization without inferring nested fields.
```
'''
task_path.write_text(task, encoding="utf-8", newline="\n")
