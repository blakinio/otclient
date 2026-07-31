use super::{AdmissionExchange, CanaryAdmissionOutcome, GameEntryRequest};
use oteryn_foundation::CancellationToken;
use oteryn_game_session::AdmissionCredential;
use oteryn_protocol_core::{
    BoundedReader, BoundedWriter, ProtocolError, ProtocolErrorKind, TrailingDataPolicy,
};
use std::sync::Arc;
use std::sync::atomic::{AtomicUsize, Ordering};

pub(super) const SYNTHETIC_CHALLENGE: u8 = 1;
pub(super) const SYNTHETIC_ACCEPTED: u8 = 2;
pub(super) const SYNTHETIC_PENDING: u8 = 3;
pub(super) const SYNTHETIC_ENTERED: u8 = 4;
pub(super) const SYNTHETIC_DENIED: u8 = 5;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(super) enum SyntheticDecision {
    Entered,
    AdmissionDenied,
    CredentialExpiredOrConsumed,
    CharacterRejected,
    ProtocolMismatch,
    ClientOrAssetMismatch,
    ConnectionLost,
}

pub(super) struct SyntheticScript {
    expected_character: String,
    expected_credential: Vec<u8>,
    decision: SyntheticDecision,
    network_attempts: Arc<AtomicUsize>,
}

impl SyntheticScript {
    pub(super) fn new(
        expected_character: String,
        expected_credential: Vec<u8>,
        decision: SyntheticDecision,
        network_attempts: Arc<AtomicUsize>,
    ) -> Self {
        Self {
            expected_character,
            expected_credential,
            decision,
            network_attempts,
        }
    }

    pub(super) fn exchange(
        &mut self,
        request: &GameEntryRequest,
        credential: &AdmissionCredential,
        cancellation: &CancellationToken,
    ) -> AdmissionExchange {
        self.network_attempts.fetch_add(1, Ordering::SeqCst);
        if cancellation.is_cancelled() {
            return AdmissionExchange::Outcome(CanaryAdmissionOutcome::Cancelled);
        }
        if request.selected_entry().character().name() != self.expected_character {
            return AdmissionExchange::Outcome(CanaryAdmissionOutcome::CharacterRejected);
        }
        if credential.expose_secret() != self.expected_credential {
            return AdmissionExchange::Outcome(CanaryAdmissionOutcome::CredentialExpiredOrConsumed);
        }
        match self.decision {
            SyntheticDecision::Entered => AdmissionExchange::Entered,
            SyntheticDecision::AdmissionDenied => {
                AdmissionExchange::Outcome(CanaryAdmissionOutcome::AdmissionDenied)
            }
            SyntheticDecision::CredentialExpiredOrConsumed => {
                AdmissionExchange::Outcome(CanaryAdmissionOutcome::CredentialExpiredOrConsumed)
            }
            SyntheticDecision::CharacterRejected => {
                AdmissionExchange::Outcome(CanaryAdmissionOutcome::CharacterRejected)
            }
            SyntheticDecision::ProtocolMismatch => {
                AdmissionExchange::Outcome(CanaryAdmissionOutcome::ProtocolMismatch)
            }
            SyntheticDecision::ClientOrAssetMismatch => {
                AdmissionExchange::Outcome(CanaryAdmissionOutcome::ClientOrAssetMismatch)
            }
            SyntheticDecision::ConnectionLost => {
                AdmissionExchange::Outcome(CanaryAdmissionOutcome::ConnectionLost)
            }
        }
    }
}

pub(super) fn success_transcript() -> Result<Vec<u8>, ProtocolError> {
    let mut writer = BoundedWriter::new(64)?;
    write_frame(&mut writer, SYNTHETIC_CHALLENGE, None)?;
    write_frame(&mut writer, SYNTHETIC_ACCEPTED, None)?;
    write_frame(&mut writer, SYNTHETIC_PENDING, None)?;
    write_frame(&mut writer, SYNTHETIC_ENTERED, None)?;
    Ok(writer.into_inner())
}

pub(super) fn write_frame(
    transcript: &mut BoundedWriter,
    tag: u8,
    detail: Option<&str>,
) -> Result<(), ProtocolError> {
    let mut payload = BoundedWriter::new(32)?;
    payload.write_u8(tag)?;
    if let Some(detail) = detail {
        payload.write_u16_string(detail, 16)?;
    }
    let payload = payload.into_inner();
    transcript.write_u16_le(
        u16::try_from(payload.len())
            .map_err(|_| ProtocolError::new(ProtocolErrorKind::InvalidLength))?,
    )?;
    transcript.write_bytes(&payload)
}

pub(super) fn parse_transcript(
    bytes: &[u8],
    max_frame_bytes: usize,
) -> Result<SyntheticDecision, ProtocolError> {
    let mut transcript = BoundedReader::new(bytes, 256)?;
    let expected = [
        SYNTHETIC_CHALLENGE,
        SYNTHETIC_ACCEPTED,
        SYNTHETIC_PENDING,
        SYNTHETIC_ENTERED,
    ];
    let mut index = 0;

    while !transcript.is_empty() {
        let frame_length = usize::from(transcript.read_u16_le()?);
        if frame_length == 0 {
            return Err(ProtocolError::new(ProtocolErrorKind::InvalidLength));
        }
        if frame_length > max_frame_bytes {
            return Err(ProtocolError::new(ProtocolErrorKind::Oversized));
        }
        let frame_bytes = transcript.read_exact(frame_length)?;
        let mut frame = BoundedReader::new(frame_bytes, max_frame_bytes)?;
        let tag = frame.read_u8()?;
        if tag == SYNTHETIC_DENIED {
            let _detail = frame.read_u16_string(16)?;
            frame.finish(TrailingDataPolicy::Reject)?;
            return Ok(SyntheticDecision::AdmissionDenied);
        }
        if index >= expected.len() || tag != expected[index] {
            return Err(ProtocolError::new(ProtocolErrorKind::UnknownValue));
        }
        frame.finish(TrailingDataPolicy::Reject)?;
        index += 1;
    }

    transcript.finish(TrailingDataPolicy::Reject)?;
    if index == expected.len() {
        Ok(SyntheticDecision::Entered)
    } else {
        Err(ProtocolError::new(ProtocolErrorKind::Truncated))
    }
}
