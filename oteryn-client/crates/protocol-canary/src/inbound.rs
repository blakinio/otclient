use crate::CANARY_NETWORK_MESSAGE_MAX_BYTES;
use oteryn_foundation::SessionGeneration;
use oteryn_game_domain::{DomainError, GameEvent, GameEventEnvelope, SessionToken};
use oteryn_protocol_core::{BoundedReader, ProtocolError, ProtocolErrorKind, TrailingDataPolicy};
use std::fmt::{Display, Formatter};

/// Canary Current server opcode for the pending-state-entered bootstrap boundary.
pub const OPCODE_PENDING_STATE_ENTERED: u8 = 0x0A;

/// Explicit caller-owned order state for the bounded pending-state decoder.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum CanaryInboundBootstrapState {
    /// The caller has completed the preceding bootstrap steps and expects `0x0A`.
    AwaitingPendingStateEntered,
    /// The exact pending-state boundary was accepted for this session.
    PendingStateEntered,
}

/// Stable failure returned by the bounded Current inbound bootstrap decoder.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CanaryInboundError {
    /// The logical message violated the exact bounded wire layout.
    Protocol(ProtocolError),
    /// The session envelope was stale or otherwise invalid.
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
/// The caller must pass one already decrypted and deframed logical message and
/// must explicitly own the bootstrap order state. The accepted source layout is
/// exactly one byte (`0x0A`) with no payload. Success emits only the shared
/// session-fenced [`GameEvent::BootstrapStarted`] envelope.
///
/// # Errors
///
/// Rejects invalid order, stale sessions, empty or oversized input, an unknown
/// opcode and every trailing byte. The order state advances only after complete
/// parsing and semantic envelope validation succeed.
pub fn decode_current_pending_state_entered(
    input: &[u8],
    state: &mut CanaryInboundBootstrapState,
    session: SessionToken,
    current: SessionGeneration,
) -> Result<GameEventEnvelope, CanaryInboundError> {
    if *state != CanaryInboundBootstrapState::AwaitingPendingStateEntered {
        return Err(CanaryInboundError::InvalidOrder);
    }

    session.ensure_current(current)?;

    let mut reader = BoundedReader::new(input, CANARY_NETWORK_MESSAGE_MAX_BYTES)?;
    let opcode = reader.read_u8()?;
    if opcode != OPCODE_PENDING_STATE_ENTERED {
        return Err(ProtocolError::new(ProtocolErrorKind::UnknownValue).into());
    }
    reader.finish(TrailingDataPolicy::Reject)?;

    let envelope = GameEventEnvelope::v1(session, GameEvent::BootstrapStarted)?;
    envelope.ensure_current(current)?;
    *state = CanaryInboundBootstrapState::PendingStateEntered;
    Ok(envelope)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::error::Error;

    fn session(generation: u64) -> (SessionToken, SessionGeneration) {
        let generation = SessionGeneration::new(generation);
        (SessionToken::new(generation), generation)
    }

    #[test]
    fn exact_pending_state_message_emits_bootstrap_started() -> Result<(), Box<dyn Error>> {
        let (session, current) = session(7);
        let mut state = CanaryInboundBootstrapState::AwaitingPendingStateEntered;

        let envelope = decode_current_pending_state_entered(
            &[OPCODE_PENDING_STATE_ENTERED],
            &mut state,
            session,
            current,
        )?;

        assert_eq!(envelope.session(), session);
        assert_eq!(envelope.event(), &GameEvent::BootstrapStarted);
        assert_eq!(state, CanaryInboundBootstrapState::PendingStateEntered);
        Ok(())
    }

    #[test]
    fn malformed_inputs_fail_without_advancing_order() {
        let (session, current) = session(8);
        for (input, expected) in [
            (&[][..], ProtocolErrorKind::Truncated),
            (&[0x0F][..], ProtocolErrorKind::UnknownValue),
            (
                &[OPCODE_PENDING_STATE_ENTERED, 0x00][..],
                ProtocolErrorKind::TrailingData,
            ),
        ] {
            let mut state = CanaryInboundBootstrapState::AwaitingPendingStateEntered;
            assert_eq!(
                decode_current_pending_state_entered(input, &mut state, session, current),
                Err(CanaryInboundError::Protocol(ProtocolError::new(expected)))
            );
            assert_eq!(
                state,
                CanaryInboundBootstrapState::AwaitingPendingStateEntered
            );
        }
    }

    #[test]
    fn oversized_input_fails_without_advancing_order() {
        let (session, current) = session(9);
        let input = vec![OPCODE_PENDING_STATE_ENTERED; CANARY_NETWORK_MESSAGE_MAX_BYTES + 1];
        let mut state = CanaryInboundBootstrapState::AwaitingPendingStateEntered;

        assert_eq!(
            decode_current_pending_state_entered(&input, &mut state, session, current),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::Oversized
            )))
        );
        assert_eq!(
            state,
            CanaryInboundBootstrapState::AwaitingPendingStateEntered
        );
    }

    #[test]
    fn duplicate_or_out_of_order_message_fails_closed() {
        let (session, current) = session(10);
        let mut state = CanaryInboundBootstrapState::PendingStateEntered;

        assert_eq!(
            decode_current_pending_state_entered(
                &[OPCODE_PENDING_STATE_ENTERED],
                &mut state,
                session,
                current,
            ),
            Err(CanaryInboundError::InvalidOrder)
        );
        assert_eq!(state, CanaryInboundBootstrapState::PendingStateEntered);
    }

    #[test]
    fn stale_session_fails_before_parsing_or_state_change() {
        let (session, _) = session(11);
        let mut state = CanaryInboundBootstrapState::AwaitingPendingStateEntered;

        assert!(matches!(
            decode_current_pending_state_entered(
                &[OPCODE_PENDING_STATE_ENTERED],
                &mut state,
                session,
                SessionGeneration::new(12),
            ),
            Err(CanaryInboundError::Domain(DomainError::StaleSession { .. }))
        ));
        assert_eq!(
            state,
            CanaryInboundBootstrapState::AwaitingPendingStateEntered
        );
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
