use crate::CANARY_NETWORK_MESSAGE_MAX_BYTES;
use oteryn_foundation::SessionGeneration;
use oteryn_game_domain::{
    DomainError, EntityHandle, EntityId, GameEvent, GameEventEnvelope, SessionEndReason,
    SessionToken,
};
use oteryn_protocol_core::{BoundedReader, ProtocolError, ProtocolErrorKind, TrailingDataPolicy};
use std::fmt::{Display, Formatter};

/// Canary Current server opcode for local-player initialization.
pub const OPCODE_LOCAL_PLAYER_INITIALIZATION: u8 = 0x17;
/// Canary Current server opcode for the fixed bug-report permission boundary.
pub const OPCODE_ALLOW_BUG_REPORT: u8 = 0x1A;
/// Canary Current server opcode for the two-byte world-clock boundary.
pub const OPCODE_TIBIA_TIME: u8 = 0xEF;
/// Canary Current server opcode for the pending-state-entered bootstrap boundary.
pub const OPCODE_PENDING_STATE_ENTERED: u8 = 0x0A;
/// Canary Current server opcode for the enter-world bootstrap boundary.
pub const OPCODE_ENTER_WORLD: u8 = 0x0F;
/// Canary Current server opcode for terminal session-end information.
pub const OPCODE_SESSION_END_INFORMATION: u8 = 0x18;

const CURRENT_LOGIN_SPEED_PRECISION: u8 = 3;
const CURRENT_LOGIN_SPEED_COMPONENTS: usize = 3;
const SESSION_END_LOGOUT: u8 = 0x00;
const SESSION_END_FORCE_CLOSE: u8 = 0x02;

/// Session-fenced caller-owned order state for bounded Current inbound decoding.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct CanaryInboundBootstrapState {
    session: SessionToken,
    local_player: Option<EntityHandle>,
    allow_bug_report_received: bool,
    tibia_time_received: bool,
    pending_state_entered: bool,
    enter_world_received: bool,
    bootstrap_completed: bool,
    session_ended: bool,
}

impl CanaryInboundBootstrapState {
    /// Start one Current bootstrap sequence for the supplied session.
    #[must_use]
    pub const fn new(session: SessionToken) -> Self {
        Self {
            session,
            local_player: None,
            allow_bug_report_received: false,
            tibia_time_received: false,
            pending_state_entered: false,
            enter_world_received: false,
            bootstrap_completed: false,
            session_ended: false,
        }
    }

    /// Return the session token that owns this inbound sequence.
    #[must_use]
    pub const fn session(self) -> SessionToken {
        self.session
    }

    /// Return the normalized session-scoped local-player handle, when proven.
    #[must_use]
    pub const fn local_player(self) -> Option<EntityHandle> {
        self.local_player
    }

    /// Return whether the fixed bug-report permission packet was accepted.
    #[must_use]
    pub const fn allow_bug_report_received(self) -> bool {
        self.allow_bug_report_received
    }

    /// Return whether the login world-clock packet was accepted.
    #[must_use]
    pub const fn tibia_time_received(self) -> bool {
        self.tibia_time_received
    }

    /// Decode the exact Current fixed bug-report permission logical message.
    ///
    /// # Errors
    ///
    /// Returns the same fail-closed errors as [`decode_current_allow_bug_report`].
    pub fn decode_allow_bug_report(
        &mut self,
        input: &[u8],
        current: SessionGeneration,
    ) -> Result<(), CanaryInboundError> {
        decode_current_allow_bug_report(input, self, current)
    }

    /// Decode the exact Current login world-clock logical message.
    ///
    /// # Errors
    ///
    /// Returns the same fail-closed errors as [`decode_current_tibia_time`].
    pub fn decode_tibia_time(
        &mut self,
        input: &[u8],
        current: SessionGeneration,
    ) -> Result<(), CanaryInboundError> {
        decode_current_tibia_time(input, self, current)
    }

    /// Return whether the pending-state boundary was already accepted.
    #[must_use]
    pub const fn pending_state_entered(self) -> bool {
        self.pending_state_entered
    }

    /// Return whether the enter-world boundary was already accepted.
    #[must_use]
    pub const fn enter_world_received(self) -> bool {
        self.enter_world_received
    }

    /// Return whether a complete initial map established the local position.
    #[must_use]
    pub const fn bootstrap_completed(self) -> bool {
        self.bootstrap_completed
    }

    pub(crate) const fn mark_bootstrap_completed(&mut self) {
        self.bootstrap_completed = true;
    }

    /// Decode the exact Current local-player initialization logical message.
    ///
    /// # Errors
    ///
    /// Returns the same fail-closed errors as
    /// [`decode_current_local_player_initialization`].
    pub fn decode_local_player_initialization(
        &mut self,
        input: &[u8],
        current: SessionGeneration,
    ) -> Result<EntityHandle, CanaryInboundError> {
        decode_current_local_player_initialization(input, self, current)
    }

    /// Decode the exact Current one-byte enter-world logical message.
    ///
    /// # Errors
    ///
    /// Returns the same fail-closed errors as [`decode_current_enter_world`].
    pub fn decode_enter_world(
        &mut self,
        input: &[u8],
        current: SessionGeneration,
    ) -> Result<(), CanaryInboundError> {
        decode_current_enter_world(input, self, current)
    }

    /// Return whether a terminal session-end boundary was already accepted.
    #[must_use]
    pub const fn session_ended(self) -> bool {
        self.session_ended
    }

    /// Decode one exact Current terminal session-end logical message.
    ///
    /// This public method keeps the wire-specific parser behind the already
    /// exported session-fenced state type rather than exposing raw reason bytes.
    ///
    /// # Errors
    ///
    /// Returns the same fail-closed errors as
    /// [`decode_current_session_end_information`].
    pub fn decode_session_end_information(
        &mut self,
        input: &[u8],
        current: SessionGeneration,
    ) -> Result<GameEventEnvelope, CanaryInboundError> {
        decode_current_session_end_information(input, self, current)
    }
}

/// Stable failure returned by the bounded Current inbound decoder.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CanaryInboundError {
    /// The logical message violated the exact bounded wire layout.
    Protocol(ProtocolError),
    /// The session envelope or inbound owner was stale.
    Domain(DomainError),
    /// The caller did not explicitly permit this message in the current order.
    InvalidOrder,
}

impl Display for CanaryInboundError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Protocol(error) => write!(formatter, "invalid Canary inbound message: {error}"),
            Self::Domain(error) => write!(formatter, "invalid Canary gameplay envelope: {error}"),
            Self::InvalidOrder => formatter
                .write_str("Canary inbound message is not valid in the current session order"),
        }
    }
}

impl std::error::Error for CanaryInboundError {}

impl From<ProtocolError> for CanaryInboundError {
    fn from(error: ProtocolError) -> Self {
        Self::Protocol(error)
    }
}

impl From<DomainError> for CanaryInboundError {
    fn from(error: DomainError) -> Self {
        Self::Domain(error)
    }
}

/// Decode the exact Current local-player branch of `sendAddCreature`.
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
        || state.allow_bug_report_received
        || state.tibia_time_received
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

/// Decode the exact Current `sendAllowBugReport` logical message.
///
/// The pinned non-legacy producer emits exactly `0x1A 0x00` immediately after
/// local-player initialization. The fixed payload byte enables the client-side
/// report action. The decoder retains no capability value and advances only
/// caller-owned bootstrap order.
///
/// # Errors
///
/// Rejects stale or impossible order, wrong opcode/fixed byte, truncation,
/// oversize and every trailing byte. State changes only after full validation.
pub fn decode_current_allow_bug_report(
    input: &[u8],
    state: &mut CanaryInboundBootstrapState,
    current: SessionGeneration,
) -> Result<(), CanaryInboundError> {
    state.session.ensure_current(current)?;
    if state.local_player.is_none()
        || state.allow_bug_report_received
        || state.tibia_time_received
        || state.pending_state_entered
        || state.enter_world_received
        || state.session_ended
    {
        return Err(CanaryInboundError::InvalidOrder);
    }

    let mut reader = BoundedReader::new(input, CANARY_NETWORK_MESSAGE_MAX_BYTES)?;
    if reader.read_u8()? != OPCODE_ALLOW_BUG_REPORT || reader.read_u8()? != 0 {
        return Err(ProtocolError::new(ProtocolErrorKind::UnknownValue).into());
    }
    reader.finish(TrailingDataPolicy::Reject)?;
    state.allow_bug_report_received = true;
    Ok(())
}

/// Decode the exact Current `sendTibiaTime` logical message.
///
/// The pinned producer emits opcode `0xEF`, followed by two opaque `u8` clock
/// components derived from its caller-owned light-hour value. The components
/// are validated structurally but are not retained or exposed because this
/// adapter does not own world-light simulation.
///
/// # Errors
///
/// Rejects stale or impossible order, wrong opcode, truncation, oversize and
/// every trailing byte. State changes only after full validation.
pub fn decode_current_tibia_time(
    input: &[u8],
    state: &mut CanaryInboundBootstrapState,
    current: SessionGeneration,
) -> Result<(), CanaryInboundError> {
    state.session.ensure_current(current)?;
    if state.local_player.is_none()
        || !state.allow_bug_report_received
        || state.tibia_time_received
        || state.pending_state_entered
        || state.enter_world_received
        || state.session_ended
    {
        return Err(CanaryInboundError::InvalidOrder);
    }

    let mut reader = BoundedReader::new(input, CANARY_NETWORK_MESSAGE_MAX_BYTES)?;
    if reader.read_u8()? != OPCODE_TIBIA_TIME {
        return Err(ProtocolError::new(ProtocolErrorKind::UnknownValue).into());
    }
    let _hour_component = reader.read_u8()?;
    let _minute_component = reader.read_u8()?;
    reader.finish(TrailingDataPolicy::Reject)?;
    state.tibia_time_received = true;
    Ok(())
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

/// Decode the exact Current `sendPendingStateEntered` logical message.
///
/// The caller must pass one already decrypted and deframed logical message. The
/// inbound order state owns its session token, so it cannot be reused after a
/// relog without failing the current-generation check. The accepted source
/// layout is exactly one byte (`0x0A`) with no payload. Success emits only the
/// shared session-fenced [`GameEvent::BootstrapStarted`] envelope.
///
/// # Errors
///
/// Rejects invalid order, stale state, empty or oversized input, an unknown
/// opcode and every trailing byte. The order state advances only after complete
/// parsing and semantic envelope validation succeed.
pub fn decode_current_pending_state_entered(
    input: &[u8],
    state: &mut CanaryInboundBootstrapState,
    current: SessionGeneration,
) -> Result<GameEventEnvelope, CanaryInboundError> {
    state.session.ensure_current(current)?;
    if state.local_player.is_none()
        || !state.allow_bug_report_received
        || !state.tibia_time_received
        || state.pending_state_entered
        || state.enter_world_received
        || state.session_ended
    {
        return Err(CanaryInboundError::InvalidOrder);
    }

    let mut reader = BoundedReader::new(input, CANARY_NETWORK_MESSAGE_MAX_BYTES)?;
    let opcode = reader.read_u8()?;
    if opcode != OPCODE_PENDING_STATE_ENTERED {
        return Err(ProtocolError::new(ProtocolErrorKind::UnknownValue).into());
    }
    reader.finish(TrailingDataPolicy::Reject)?;

    let envelope = GameEventEnvelope::v1(state.session, GameEvent::BootstrapStarted)?;
    envelope.ensure_current(current)?;
    state.pending_state_entered = true;
    Ok(envelope)
}

/// Decode the exact Current `sendSessionEndInformation` logical message.
///
/// The pinned producer emits opcode `0x18` followed by one
/// `SessionEndInformations` byte and immediately disconnects. Only the proven
/// `SESSION_END_LOGOUT` (`0x00`) and `SESSION_END_FORCECLOSE` (`0x02`) values are
/// accepted. Both are normalized conservatively to
/// [`SessionEndReason::ServerClosed`], because this isolated decoder has no
/// caller-owned command history that could prove a local-requested cause. The
/// unknown `0x01` and `0x03` values fail closed.
///
/// A terminal session-end message may arrive before or after the pending-state
/// boundary, but it may be accepted only once for one current session. Success
/// prevents every later bootstrap message from advancing this state.
///
/// # Errors
///
/// Rejects stale or already-ended state, empty, truncated, oversized, unknown,
/// or trailing input. State changes only after complete parsing and semantic
/// envelope validation.
pub fn decode_current_session_end_information(
    input: &[u8],
    state: &mut CanaryInboundBootstrapState,
    current: SessionGeneration,
) -> Result<GameEventEnvelope, CanaryInboundError> {
    state.session.ensure_current(current)?;
    if state.session_ended {
        return Err(CanaryInboundError::InvalidOrder);
    }

    let mut reader = BoundedReader::new(input, CANARY_NETWORK_MESSAGE_MAX_BYTES)?;
    let opcode = reader.read_u8()?;
    if opcode != OPCODE_SESSION_END_INFORMATION {
        return Err(ProtocolError::new(ProtocolErrorKind::UnknownValue).into());
    }
    let reason = reader.read_u8()?;
    reader.finish(TrailingDataPolicy::Reject)?;

    if !matches!(reason, SESSION_END_LOGOUT | SESSION_END_FORCE_CLOSE) {
        return Err(ProtocolError::new(ProtocolErrorKind::UnknownValue).into());
    }

    let envelope = GameEventEnvelope::v1(
        state.session,
        GameEvent::SessionEnded {
            reason: SessionEndReason::ServerClosed,
        },
    )?;
    envelope.ensure_current(current)?;
    state.session_ended = true;
    Ok(envelope)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::error::Error;
    use std::num::ParseIntError;

    const ALLOW_BUG_REPORT_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/allow-bug-report.hex"
    );
    const TIBIA_TIME_FIXTURE: &str =
        include_str!("../../../tests/integration/canary-world-protocol/fixtures/tibia-time.hex");
    const PENDING_STATE_ENTERED_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/pending-state-entered.hex"
    );
    const PENDING_STATE_WRONG_OPCODE_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/pending-state-wrong-opcode.hex"
    );
    const SESSION_END_LOGOUT_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/session-end-logout.hex"
    );
    const SESSION_END_FORCE_CLOSE_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/session-end-force-close.hex"
    );
    const SESSION_END_UNKNOWN_REASON_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/session-end-unknown-reason.hex"
    );
    const SESSION_END_TRAILING_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/session-end-trailing.hex"
    );
    const LOCAL_PLAYER_INITIALIZATION_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/local-player-initialization.hex"
    );
    const LOCAL_PLAYER_BAD_PRECISION_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/local-player-bad-precision.hex"
    );
    const LOCAL_PLAYER_ZERO_ID_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/local-player-zero-id.hex"
    );
    const LOCAL_PLAYER_TRAILING_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/local-player-trailing.hex"
    );
    const ENTER_WORLD_FIXTURE: &str =
        include_str!("../../../tests/integration/canary-world-protocol/fixtures/enter-world.hex");

    fn state(generation: u64) -> (CanaryInboundBootstrapState, SessionGeneration) {
        let generation = SessionGeneration::new(generation);
        (
            CanaryInboundBootstrapState::new(SessionToken::new(generation)),
            generation,
        )
    }

    fn parse_hex_fixture(input: &str) -> Result<Vec<u8>, ParseIntError> {
        input
            .split_whitespace()
            .map(|token| u8::from_str_radix(token, 16))
            .collect()
    }

    fn initialize_login_side_preamble(
        state: &mut CanaryInboundBootstrapState,
        current: SessionGeneration,
    ) -> Result<(), Box<dyn Error>> {
        let local = parse_hex_fixture(LOCAL_PLAYER_INITIALIZATION_FIXTURE)?;
        state.decode_local_player_initialization(&local, current)?;
        let permission = parse_hex_fixture(ALLOW_BUG_REPORT_FIXTURE)?;
        state.decode_allow_bug_report(&permission, current)?;
        let time = parse_hex_fixture(TIBIA_TIME_FIXTURE)?;
        state.decode_tibia_time(&time, current)?;
        Ok(())
    }

    #[test]
    fn exact_login_side_preamble_advances_only_order_state() -> Result<(), Box<dyn Error>> {
        let (mut state, current) = state(5);
        let local = parse_hex_fixture(LOCAL_PLAYER_INITIALIZATION_FIXTURE)?;
        let permission = parse_hex_fixture(ALLOW_BUG_REPORT_FIXTURE)?;
        let time = parse_hex_fixture(TIBIA_TIME_FIXTURE)?;

        state.decode_local_player_initialization(&local, current)?;
        state.decode_allow_bug_report(&permission, current)?;
        assert!(state.allow_bug_report_received());
        assert!(!state.tibia_time_received());
        state.decode_tibia_time(&time, current)?;

        assert!(state.allow_bug_report_received());
        assert!(state.tibia_time_received());
        assert!(!state.pending_state_entered());
        assert!(!state.enter_world_received());
        Ok(())
    }

    #[test]
    fn login_side_preamble_rejects_wrong_order_and_malformed_fields() -> Result<(), Box<dyn Error>>
    {
        let local = parse_hex_fixture(LOCAL_PLAYER_INITIALIZATION_FIXTURE)?;
        let permission = parse_hex_fixture(ALLOW_BUG_REPORT_FIXTURE)?;
        let time = parse_hex_fixture(TIBIA_TIME_FIXTURE)?;
        let (mut state, current) = state(6);

        assert_eq!(
            state.decode_allow_bug_report(&permission, current),
            Err(CanaryInboundError::InvalidOrder)
        );
        state.decode_local_player_initialization(&local, current)?;
        assert_eq!(
            state.decode_tibia_time(&time, current),
            Err(CanaryInboundError::InvalidOrder)
        );
        assert_eq!(
            state.decode_allow_bug_report(&[OPCODE_ALLOW_BUG_REPORT, 0x01], current),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::UnknownValue,
            )))
        );
        assert!(!state.allow_bug_report_received());
        state.decode_allow_bug_report(&permission, current)?;

        for (input, expected) in [
            (&[][..], ProtocolErrorKind::Truncated),
            (&[OPCODE_TIBIA_TIME][..], ProtocolErrorKind::Truncated),
            (&[OPCODE_TIBIA_TIME, 0x0C][..], ProtocolErrorKind::Truncated),
            (&[0xEE, 0x0C, 0x22][..], ProtocolErrorKind::UnknownValue),
            (
                &[OPCODE_TIBIA_TIME, 0x0C, 0x22, 0x00][..],
                ProtocolErrorKind::TrailingData,
            ),
        ] {
            assert_eq!(
                state.decode_tibia_time(input, current),
                Err(CanaryInboundError::Protocol(ProtocolError::new(expected)))
            );
            assert!(!state.tibia_time_received());
        }
        state.decode_tibia_time(&time, current)?;
        assert_eq!(
            state.decode_tibia_time(&time, current),
            Err(CanaryInboundError::InvalidOrder)
        );
        Ok(())
    }

    #[test]
    fn pending_state_requires_complete_login_side_preamble() -> Result<(), Box<dyn Error>> {
        let local = parse_hex_fixture(LOCAL_PLAYER_INITIALIZATION_FIXTURE)?;
        let permission = parse_hex_fixture(ALLOW_BUG_REPORT_FIXTURE)?;
        let pending = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;
        let (mut state, current) = state(7);

        state.decode_local_player_initialization(&local, current)?;
        assert_eq!(
            decode_current_pending_state_entered(&pending, &mut state, current),
            Err(CanaryInboundError::InvalidOrder)
        );
        state.decode_allow_bug_report(&permission, current)?;
        assert_eq!(
            decode_current_pending_state_entered(&pending, &mut state, current),
            Err(CanaryInboundError::InvalidOrder)
        );
        assert!(!state.pending_state_entered());
        Ok(())
    }

    #[test]
    fn pending_state_requires_local_player_identity() -> Result<(), Box<dyn Error>> {
        let (mut state, current) = state(6);
        let input = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;
        assert_eq!(
            decode_current_pending_state_entered(&input, &mut state, current),
            Err(CanaryInboundError::InvalidOrder)
        );
        assert_eq!(state.local_player(), None);
        assert!(!state.pending_state_entered());
        Ok(())
    }

    #[test]
    fn exact_pending_state_fixture_emits_bootstrap_started() -> Result<(), Box<dyn Error>> {
        let (mut state, current) = state(7);
        let session = state.session();
        let input = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;
        initialize_login_side_preamble(&mut state, current)?;

        let envelope = decode_current_pending_state_entered(&input, &mut state, current)?;

        assert_eq!(envelope.session(), session);
        assert_eq!(envelope.event(), &GameEvent::BootstrapStarted);
        assert!(state.pending_state_entered());
        assert!(!state.session_ended());
        Ok(())
    }

    #[test]
    fn malformed_pending_state_inputs_fail_without_advancing_order() -> Result<(), Box<dyn Error>> {
        let wrong_opcode = parse_hex_fixture(PENDING_STATE_WRONG_OPCODE_FIXTURE)?;
        let (_, current) = state(8);
        for (input, expected) in [
            (&[][..], ProtocolErrorKind::Truncated),
            (&wrong_opcode[..], ProtocolErrorKind::UnknownValue),
            (
                &[OPCODE_PENDING_STATE_ENTERED, 0x00][..],
                ProtocolErrorKind::TrailingData,
            ),
        ] {
            let (mut state, _) = state(8);
            initialize_login_side_preamble(&mut state, current)?;
            assert_eq!(
                decode_current_pending_state_entered(input, &mut state, current),
                Err(CanaryInboundError::Protocol(ProtocolError::new(expected)))
            );
            assert!(!state.pending_state_entered());
            assert!(!state.session_ended());
        }
        Ok(())
    }

    #[test]
    fn oversized_pending_state_input_fails_without_advancing_order() -> Result<(), Box<dyn Error>> {
        let (mut state, current) = state(9);
        let input = vec![OPCODE_PENDING_STATE_ENTERED; CANARY_NETWORK_MESSAGE_MAX_BYTES + 1];
        initialize_login_side_preamble(&mut state, current)?;

        assert_eq!(
            decode_current_pending_state_entered(&input, &mut state, current),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::Oversized
            )))
        );
        assert!(!state.pending_state_entered());
        assert!(!state.session_ended());
        Ok(())
    }

    #[test]
    fn duplicate_pending_state_message_fails_closed() -> Result<(), Box<dyn Error>> {
        let (mut state, current) = state(10);
        let input = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;
        initialize_login_side_preamble(&mut state, current)?;
        decode_current_pending_state_entered(&input, &mut state, current)?;

        assert_eq!(
            decode_current_pending_state_entered(&input, &mut state, current),
            Err(CanaryInboundError::InvalidOrder)
        );
        assert!(state.pending_state_entered());
        assert!(!state.session_ended());
        Ok(())
    }

    #[test]
    fn stale_pending_state_fails_before_parsing_or_state_change() {
        let (mut state, _) = state(11);

        assert!(matches!(
            decode_current_pending_state_entered(
                &[OPCODE_PENDING_STATE_ENTERED],
                &mut state,
                SessionGeneration::new(12),
            ),
            Err(CanaryInboundError::Domain(DomainError::StaleSession { .. }))
        ));
        assert!(!state.pending_state_entered());
        assert!(!state.session_ended());
    }

    #[test]
    fn exact_session_end_fixtures_emit_server_closed() -> Result<(), Box<dyn Error>> {
        for (generation, fixture) in [
            (20, SESSION_END_LOGOUT_FIXTURE),
            (21, SESSION_END_FORCE_CLOSE_FIXTURE),
        ] {
            let (mut state, current) = state(generation);
            let input = parse_hex_fixture(fixture)?;
            let envelope = state.decode_session_end_information(&input, current)?;

            assert_eq!(
                envelope.event(),
                &GameEvent::SessionEnded {
                    reason: SessionEndReason::ServerClosed,
                }
            );
            assert!(!state.pending_state_entered());
            assert!(state.session_ended());
        }
        Ok(())
    }

    #[test]
    fn malformed_session_end_inputs_fail_without_ending_session() -> Result<(), Box<dyn Error>> {
        let unknown_reason = parse_hex_fixture(SESSION_END_UNKNOWN_REASON_FIXTURE)?;
        let trailing = parse_hex_fixture(SESSION_END_TRAILING_FIXTURE)?;
        let (_, current) = state(22);
        for (input, expected) in [
            (&[][..], ProtocolErrorKind::Truncated),
            (
                &[OPCODE_SESSION_END_INFORMATION][..],
                ProtocolErrorKind::Truncated,
            ),
            (
                &[0x19, SESSION_END_LOGOUT][..],
                ProtocolErrorKind::UnknownValue,
            ),
            (&unknown_reason[..], ProtocolErrorKind::UnknownValue),
            (&trailing[..], ProtocolErrorKind::TrailingData),
        ] {
            let (mut state, _) = state(22);
            assert_eq!(
                state.decode_session_end_information(input, current),
                Err(CanaryInboundError::Protocol(ProtocolError::new(expected)))
            );
            assert!(!state.session_ended());
        }
        Ok(())
    }

    #[test]
    fn oversized_session_end_input_fails_without_ending_session() {
        let (mut state, current) = state(23);
        let input = vec![OPCODE_SESSION_END_INFORMATION; CANARY_NETWORK_MESSAGE_MAX_BYTES + 1];

        assert_eq!(
            state.decode_session_end_information(&input, current),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::Oversized
            )))
        );
        assert!(!state.session_ended());
    }

    #[test]
    fn session_end_is_terminal_before_or_after_pending_state() -> Result<(), Box<dyn Error>> {
        let session_end = parse_hex_fixture(SESSION_END_LOGOUT_FIXTURE)?;
        let pending = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;

        let (mut before_pending, current) = state(24);
        before_pending.decode_session_end_information(&session_end, current)?;
        assert_eq!(
            decode_current_pending_state_entered(&pending, &mut before_pending, current),
            Err(CanaryInboundError::InvalidOrder)
        );

        let (mut after_pending, current) = state(25);
        initialize_login_side_preamble(&mut after_pending, current)?;
        decode_current_pending_state_entered(&pending, &mut after_pending, current)?;
        after_pending.decode_session_end_information(&session_end, current)?;
        assert!(after_pending.pending_state_entered());
        assert!(after_pending.session_ended());
        Ok(())
    }

    #[test]
    fn duplicate_or_stale_session_end_fails_closed() -> Result<(), Box<dyn Error>> {
        let input = parse_hex_fixture(SESSION_END_FORCE_CLOSE_FIXTURE)?;
        let (mut ended, current) = state(26);
        ended.decode_session_end_information(&input, current)?;
        assert_eq!(
            ended.decode_session_end_information(&input, current),
            Err(CanaryInboundError::InvalidOrder)
        );

        let (mut stale, _) = state(27);
        assert!(matches!(
            stale.decode_session_end_information(&input, SessionGeneration::new(28)),
            Err(CanaryInboundError::Domain(DomainError::StaleSession { .. }))
        ));
        assert!(!stale.session_ended());
        Ok(())
    }

    #[test]
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
    fn exact_bootstrap_order_reaches_enter_world_without_claiming_completion()
    -> Result<(), Box<dyn Error>> {
        let local = parse_hex_fixture(LOCAL_PLAYER_INITIALIZATION_FIXTURE)?;
        let permission = parse_hex_fixture(ALLOW_BUG_REPORT_FIXTURE)?;
        let time = parse_hex_fixture(TIBIA_TIME_FIXTURE)?;
        let pending = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;
        let enter = parse_hex_fixture(ENTER_WORLD_FIXTURE)?;
        let (mut state, current) = state(36);

        assert_eq!(
            state.decode_enter_world(&enter, current),
            Err(CanaryInboundError::InvalidOrder)
        );
        state.decode_local_player_initialization(&local, current)?;
        state.decode_allow_bug_report(&permission, current)?;
        state.decode_tibia_time(&time, current)?;
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
        let (mut state, current) = state(37);
        initialize_login_side_preamble(&mut state, current)?;
        let pending = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;
        decode_current_pending_state_entered(&pending, &mut state, current)?;

        for (input, expected) in [
            (&[][..], ProtocolErrorKind::Truncated),
            (&[0x10][..], ProtocolErrorKind::UnknownValue),
            (
                &[OPCODE_ENTER_WORLD, 0x00][..],
                ProtocolErrorKind::TrailingData,
            ),
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
    fn terminal_session_prevents_identity_and_enter_world_advancement() -> Result<(), Box<dyn Error>>
    {
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

    #[test]
    fn generated_index_contains_exact_pending_state_entry() {
        assert!(generated_index_contains_entry(
            "bootstrap",
            "sendPendingStateEntered",
            OPCODE_PENDING_STATE_ENTERED,
            8502,
        ));
    }

    #[test]
    fn generated_index_contains_exact_session_end_entry() {
        assert!(generated_index_contains_entry(
            "bootstrap",
            "sendSessionEndInformation",
            OPCODE_SESSION_END_INFORMATION,
            2932,
        ));
    }

    fn generated_index_contains_entry(family: &str, method: &str, opcode: u8, line: u32) -> bool {
        const CURRENT_INDEX: &str =
            include_str!("../../../tools/canary-protocol-index/generated/current-index.json");
        let family_fragment = format!("\"family\": \"{family}\"");
        let method_fragment = format!("\"method\": \"{method}\"");
        let opcode_fragment = format!("\"opcode\": {opcode}");
        let line_fragment = format!("\"line\": {line}");
        CURRENT_INDEX
            .split("\"direction\": \"server-to-client\"")
            .skip(1)
            .filter_map(|suffix| suffix.split("    },").next())
            .any(|entry| {
                entry.contains("\"dispatch_phase\": \"server-send\"")
                    && entry.contains(&family_fragment)
                    && entry.contains(&method_fragment)
                    && entry.contains(&opcode_fragment)
                    && entry.contains(&line_fragment)
                    && entry.contains("\"path\": \"src/server/network/protocol/protocolgame.cpp\"")
            })
    }
}
