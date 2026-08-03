use crate::CANARY_NETWORK_MESSAGE_MAX_BYTES;
use oteryn_foundation::SessionGeneration;
use oteryn_game_domain::{
    DomainError, GameEvent, GameEventEnvelope, SessionEndReason, SessionToken,
};
use oteryn_protocol_core::{BoundedReader, ProtocolError, ProtocolErrorKind, TrailingDataPolicy};
use std::fmt::{Display, Formatter};

/// Canary Current server opcode for the pending-state-entered bootstrap boundary.
pub const OPCODE_PENDING_STATE_ENTERED: u8 = 0x0A;
/// Canary Current server opcode for terminal session-end information.
pub const OPCODE_SESSION_END_INFORMATION: u8 = 0x18;

const SESSION_END_LOGOUT: u8 = 0x00;
const SESSION_END_FORCE_CLOSE: u8 = 0x02;

/// Session-fenced caller-owned order state for bounded Current inbound decoding.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct CanaryInboundBootstrapState {
    session: SessionToken,
    pending_state_entered: bool,
    session_ended: bool,
}

impl CanaryInboundBootstrapState {
    /// Start one Current bootstrap sequence for the supplied session.
    #[must_use]
    pub const fn new(session: SessionToken) -> Self {
        Self {
            session,
            pending_state_entered: false,
            session_ended: false,
        }
    }

    /// Return the session token that owns this inbound sequence.
    #[must_use]
    pub const fn session(self) -> SessionToken {
        self.session
    }

    /// Return whether the pending-state boundary was already accepted.
    #[must_use]
    pub const fn pending_state_entered(self) -> bool {
        self.pending_state_entered
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
    if state.pending_state_entered || state.session_ended {
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

    #[test]
    fn exact_pending_state_fixture_emits_bootstrap_started() -> Result<(), Box<dyn Error>> {
        let (mut state, current) = state(7);
        let session = state.session();
        let input = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;

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
    fn oversized_pending_state_input_fails_without_advancing_order() {
        let (mut state, current) = state(9);
        let input = vec![OPCODE_PENDING_STATE_ENTERED; CANARY_NETWORK_MESSAGE_MAX_BYTES + 1];

        assert_eq!(
            decode_current_pending_state_entered(&input, &mut state, current),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::Oversized
            )))
        );
        assert!(!state.pending_state_entered());
        assert!(!state.session_ended());
    }

    #[test]
    fn duplicate_pending_state_message_fails_closed() -> Result<(), Box<dyn Error>> {
        let (mut state, current) = state(10);
        let input = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;
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
            (&[0x19, SESSION_END_LOGOUT][..], ProtocolErrorKind::UnknownValue),
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

    fn generated_index_contains_entry(
        family: &str,
        method: &str,
        opcode: u8,
        line: u32,
    ) -> bool {
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
