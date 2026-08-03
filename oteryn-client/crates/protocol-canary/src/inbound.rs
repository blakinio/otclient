use crate::CANARY_NETWORK_MESSAGE_MAX_BYTES;
use oteryn_foundation::SessionGeneration;
use oteryn_game_domain::{DomainError, GameEvent, GameEventEnvelope, SessionToken};
use oteryn_protocol_core::{BoundedReader, ProtocolError, ProtocolErrorKind, TrailingDataPolicy};
use std::fmt::{Display, Formatter};

/// Canary Current server opcode for the pending-state-entered bootstrap boundary.
pub const OPCODE_PENDING_STATE_ENTERED: u8 = 0x0A;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
enum CanaryInboundBootstrapStage {
    AwaitingPendingStateEntered,
    PendingStateEntered,
}

/// Session-fenced caller-owned order state for the bounded bootstrap decoder.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct CanaryInboundBootstrapState {
    session: SessionToken,
    stage: CanaryInboundBootstrapStage,
}

impl CanaryInboundBootstrapState {
    /// Start one Current bootstrap sequence for the supplied session.
    #[must_use]
    pub const fn new(session: SessionToken) -> Self {
        Self {
            session,
            stage: CanaryInboundBootstrapStage::AwaitingPendingStateEntered,
        }
    }

    /// Return the session token that owns this bootstrap sequence.
    #[must_use]
    pub const fn session(self) -> SessionToken {
        self.session
    }

    /// Return whether the pending-state boundary was already accepted.
    #[must_use]
    pub const fn pending_state_entered(self) -> bool {
        matches!(self.stage, CanaryInboundBootstrapStage::PendingStateEntered)
    }
}

/// Stable failure returned by the bounded Current inbound bootstrap decoder.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CanaryInboundError {
    /// The logical message violated the exact bounded wire layout.
    Protocol(ProtocolError),
    /// The session envelope or bootstrap owner was stale.
    Domain(DomainError),
    /// The caller did not explicitly await this bootstrap boundary.
    InvalidOrder,
}

impl Display for CanaryInboundError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Protocol(error) => write!(formatter, "invalid Canary inbound message: {error}"),
            Self::Domain(error) => write!(formatter, "invalid Canary gameplay envelope: {error}"),
            Self::InvalidOrder => formatter.write_str(
                "Canary pending-state message is not valid in the current bootstrap order",
            ),
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
/// bootstrap order state owns its session token, so it cannot be reused after a
/// relog without failing the current-generation check. The accepted source
/// layout is exactly one byte (`0x0A`) with no payload. Success emits only the
/// shared session-fenced [`GameEvent::BootstrapStarted`] envelope.
///
/// # Errors
///
/// Rejects invalid order, stale bootstrap state, empty or oversized input, an
/// unknown opcode and every trailing byte. The order state advances only after
/// complete parsing and semantic envelope validation succeed.
pub fn decode_current_pending_state_entered(
    input: &[u8],
    state: &mut CanaryInboundBootstrapState,
    current: SessionGeneration,
) -> Result<GameEventEnvelope, CanaryInboundError> {
    state.session.ensure_current(current)?;
    if state.stage != CanaryInboundBootstrapStage::AwaitingPendingStateEntered {
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
    state.stage = CanaryInboundBootstrapStage::PendingStateEntered;
    Ok(envelope)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::error::Error;

    fn state(generation: u64) -> (CanaryInboundBootstrapState, SessionGeneration) {
        let generation = SessionGeneration::new(generation);
        (
            CanaryInboundBootstrapState::new(SessionToken::new(generation)),
            generation,
        )
    }

    #[test]
    fn exact_pending_state_message_emits_bootstrap_started() -> Result<(), Box<dyn Error>> {
        let (mut state, current) = state(7);
        let session = state.session();

        let envelope = decode_current_pending_state_entered(
            &[OPCODE_PENDING_STATE_ENTERED],
            &mut state,
            current,
        )?;

        assert_eq!(envelope.session(), session);
        assert_eq!(envelope.event(), &GameEvent::BootstrapStarted);
        assert!(state.pending_state_entered());
        Ok(())
    }

    #[test]
    fn malformed_inputs_fail_without_advancing_order() {
        let (_, current) = state(8);
        for (input, expected) in [
            (&[][..], ProtocolErrorKind::Truncated),
            (&[0x0F][..], ProtocolErrorKind::UnknownValue),
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
        }
    }

    #[test]
    fn oversized_input_fails_without_advancing_order() {
        let (mut state, current) = state(9);
        let input = vec![OPCODE_PENDING_STATE_ENTERED; CANARY_NETWORK_MESSAGE_MAX_BYTES + 1];

        assert_eq!(
            decode_current_pending_state_entered(&input, &mut state, current),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::Oversized
            )))
        );
        assert!(!state.pending_state_entered());
    }

    #[test]
    fn duplicate_or_out_of_order_message_fails_closed() -> Result<(), Box<dyn Error>> {
        let (mut state, current) = state(10);
        decode_current_pending_state_entered(
            &[OPCODE_PENDING_STATE_ENTERED],
            &mut state,
            current,
        )?;

        assert_eq!(
            decode_current_pending_state_entered(
                &[OPCODE_PENDING_STATE_ENTERED],
                &mut state,
                current,
            ),
            Err(CanaryInboundError::InvalidOrder)
        );
        assert!(state.pending_state_entered());
        Ok(())
    }

    #[test]
    fn stale_bootstrap_state_fails_before_parsing_or_state_change() {
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
    }

    #[test]
    fn generated_index_contains_exact_pending_state_entry() {
        const CURRENT_INDEX: &str =
            include_str!("../../../tools/canary-protocol-index/generated/current-index.json");
        let opcode_fragment = format!("\"opcode\": {OPCODE_PENDING_STATE_ENTERED}");
        let entry_exists = CURRENT_INDEX
            .split("\"direction\": \"server-to-client\"")
            .skip(1)
            .filter_map(|suffix| suffix.split("    },").next())
            .any(|entry| {
                entry.contains("\"dispatch_phase\": \"server-send\"")
                    && entry.contains("\"family\": \"bootstrap\"")
                    && entry.contains("\"method\": \"sendPendingStateEntered\"")
                    && entry.contains(&opcode_fragment)
                    && entry.contains("\"line\": 8502")
                    && entry.contains(
                        "\"path\": \"src/server/network/protocol/protocolgame.cpp\"",
                    )
            });
        assert!(entry_exists, "missing exact pending-state producer entry");
    }
}
