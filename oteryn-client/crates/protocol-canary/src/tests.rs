use super::synthetic::{
    SYNTHETIC_ACCEPTED, SYNTHETIC_CHALLENGE, SYNTHETIC_DENIED, SyntheticDecision,
    SyntheticScript, parse_transcript, success_transcript, write_frame,
};
use super::*;
use oteryn_account_session::AccountSessionId;
use oteryn_foundation::{CancellationSource, Deadline, ManualClock, Moment};
use oteryn_game_session::{EntryPhase, GameEntryCredential};
use oteryn_protocol_core::{BoundedWriter, ProtocolError, ProtocolErrorKind};
use oteryn_world_directory::{
    AccountDirectorySnapshot, Availability, CharacterId, CharacterSummary, Compatibility,
    DirectoryRevision, WorldId, WorldRoute, WorldSummary,
};
use std::error::Error;
use std::sync::Arc;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::Duration;

fn transport_config() -> Result<TransportConfig, Box<dyn Error>> {
    Ok(TransportConfig::new(
        Duration::from_secs(1),
        Duration::from_secs(1),
        Duration::from_secs(1),
        1024,
        1024,
    )?)
}

fn lifecycle_with_credential(
    character_name: &str,
    lifetime: Duration,
) -> Result<(EntryLifecycle, GameEntryAttemptId, ManualClock), Box<dyn Error>> {
    let clock = ManualClock::new(Moment::ZERO);
    let attempt_id = GameEntryAttemptId::new(1)?;
    let account_session_id = AccountSessionId::new(2)?;
    let world_id = WorldId::new(3)?;
    let character_id = CharacterId::new(4)?;
    let world = WorldSummary::new(
        world_id,
        "synthetic".to_owned(),
        "Synthetic".to_owned(),
        "test".to_owned(),
        WorldRoute::new("127.0.0.1".to_owned(), 7172)?,
        Availability::Available,
        Compatibility::Compatible,
    )?;
    let character = CharacterSummary::new(
        character_id,
        world_id,
        character_name.to_owned(),
        1,
        "None".to_owned(),
        Availability::Available,
        Compatibility::Compatible,
    )?;
    let snapshot = AccountDirectorySnapshot::new(
        account_session_id,
        DirectoryRevision::new(1)?,
        vec![world],
        vec![character],
        Vec::new(),
    )?;
    let selection = snapshot.select(snapshot.revision(), character_id, world_id, None)?;
    let request = GameEntryRequest::new(
        attempt_id,
        selection,
        EntryProfile::CanaryCurrent,
        clock.now(),
    );

    let mut lifecycle = EntryLifecycle::new();
    lifecycle.begin_authentication(attempt_id)?;
    lifecycle.account_ready(attempt_id, account_session_id)?;
    lifecycle.directory_ready(attempt_id, snapshot)?;
    lifecycle.request_entry(request)?;
    lifecycle.credential_ready(
        attempt_id,
        GameEntryCredential::new(
            b"original-synthetic-credential".to_vec(),
            Deadline::after(&clock, lifetime)?,
        )?,
        &clock,
    )?;
    Ok((lifecycle, attempt_id, clock))
}

fn script(
    expected_character: &str,
    decision: SyntheticDecision,
    attempts: Arc<AtomicUsize>,
) -> SyntheticScript {
    SyntheticScript::new(
        expected_character.to_owned(),
        b"original-synthetic-credential".to_vec(),
        decision,
        attempts,
    )
}

#[test]
fn exact_profile_metadata_and_unknown_profile_are_closed() {
    assert_eq!(CURRENT_PROFILE.revision(), CANARY_CURRENT_REVISION);
    assert_eq!(CURRENT_PROFILE.release(), "3.6.1");
    assert_eq!(CURRENT_PROFILE.identifier(), "current");
    assert_eq!(CURRENT_PROFILE.client_version(), 1525);
    assert_eq!(CURRENT_PROFILE.max_network_message_bytes(), 65_500);
    assert_eq!(CURRENT_PROFILE.max_input_message_bytes(), 4_096);
    assert_eq!(CURRENT_PROFILE.max_character_name_bytes(), 30);
    assert_eq!(select_profile("current"), Ok(CURRENT_PROFILE));
    assert_eq!(
        select_profile("unknown"),
        Err(CanaryAdmissionOutcome::ProtocolMismatch)
    );
}

#[test]
fn real_admission_is_blocked_before_network_or_credential_use() -> Result<(), Box<dyn Error>> {
    let (lifecycle, _attempt_id, _clock) =
        lifecycle_with_credential("Synthetic Character", Duration::from_secs(5))?;
    let request = lifecycle.request().ok_or("missing synthetic request")?;
    let source = CancellationSource::new();
    let mut adapter = CanaryEntryAdapter::new(transport_config()?);
    assert_eq!(
        adapter.connect(request, &source.token()),
        Err(CanaryAdmissionOutcome::RealAdmissionUnavailable)
    );
    assert_eq!(adapter.state(), CanaryConnectionState::Idle);
    assert_eq!(lifecycle.phase(), EntryPhase::CredentialReady);
    Ok(())
}

#[test]
fn successful_synthetic_admission_returns_shared_session_entered() -> Result<(), Box<dyn Error>> {
    let (mut lifecycle, attempt_id, clock) =
        lifecycle_with_credential("Synthetic Character", Duration::from_secs(5))?;
    let attempts = Arc::new(AtomicUsize::new(0));
    let mut adapter = CanaryEntryAdapter::with_synthetic(
        transport_config()?,
        script(
            "Synthetic Character",
            SyntheticDecision::Entered,
            Arc::clone(&attempts),
        ),
    );
    let source = CancellationSource::new();
    let request = lifecycle
        .request()
        .ok_or("missing synthetic request")?
        .clone();
    adapter.connect(&request, &source.token())?;
    let outcome = adapter.enter_session(&mut lifecycle, attempt_id, &clock, &source.token());
    let CanaryAdmissionOutcome::SessionEntered(entered) = outcome else {
        return Err("synthetic admission did not enter session".into());
    };
    assert_eq!(entered.character_id(), CharacterId::new(4)?);
    assert_eq!(attempts.load(Ordering::SeqCst), 1);
    assert_eq!(adapter.state(), CanaryConnectionState::Closed);
    assert_eq!(lifecycle.phase(), EntryPhase::SessionEntered);
    Ok(())
}

#[test]
fn all_required_server_outcomes_are_typed_and_terminal() -> Result<(), Box<dyn Error>> {
    for (decision, expected) in [
        (
            SyntheticDecision::CharacterRejected,
            CanaryAdmissionOutcome::CharacterRejected,
        ),
        (
            SyntheticDecision::AdmissionDenied,
            CanaryAdmissionOutcome::AdmissionDenied,
        ),
        (
            SyntheticDecision::CredentialExpiredOrConsumed,
            CanaryAdmissionOutcome::CredentialExpiredOrConsumed,
        ),
        (
            SyntheticDecision::ProtocolMismatch,
            CanaryAdmissionOutcome::ProtocolMismatch,
        ),
        (
            SyntheticDecision::ClientOrAssetMismatch,
            CanaryAdmissionOutcome::ClientOrAssetMismatch,
        ),
        (
            SyntheticDecision::ConnectionLost,
            CanaryAdmissionOutcome::ConnectionLost,
        ),
    ] {
        let (mut lifecycle, attempt_id, clock) =
            lifecycle_with_credential("Synthetic Character", Duration::from_secs(5))?;
        let attempts = Arc::new(AtomicUsize::new(0));
        let mut adapter = CanaryEntryAdapter::with_synthetic(
            transport_config()?,
            script("Synthetic Character", decision, Arc::clone(&attempts)),
        );
        let source = CancellationSource::new();
        let request = lifecycle
            .request()
            .ok_or("missing synthetic request")?
            .clone();
        adapter.connect(&request, &source.token())?;
        assert_eq!(
            adapter.enter_session(&mut lifecycle, attempt_id, &clock, &source.token()),
            expected
        );
        assert_eq!(attempts.load(Ordering::SeqCst), 1);
        assert_eq!(adapter.state(), CanaryConnectionState::Closed);
        assert_eq!(lifecycle.phase(), EntryPhase::Failed);
    }
    Ok(())
}

#[test]
fn wrong_character_is_rejected_without_secret_text() -> Result<(), Box<dyn Error>> {
    let (mut lifecycle, attempt_id, clock) =
        lifecycle_with_credential("Synthetic Character", Duration::from_secs(5))?;
    let attempts = Arc::new(AtomicUsize::new(0));
    let mut adapter = CanaryEntryAdapter::with_synthetic(
        transport_config()?,
        script(
            "Different Character",
            SyntheticDecision::Entered,
            Arc::clone(&attempts),
        ),
    );
    let source = CancellationSource::new();
    let request = lifecycle
        .request()
        .ok_or("missing synthetic request")?
        .clone();
    adapter.connect(&request, &source.token())?;
    assert_eq!(
        adapter.enter_session(&mut lifecycle, attempt_id, &clock, &source.token()),
        CanaryAdmissionOutcome::CharacterRejected
    );
    assert_eq!(attempts.load(Ordering::SeqCst), 1);
    assert!(!format!("{adapter:?}").contains("original-synthetic-credential"));
    assert!(!CanaryAdmissionOutcome::CharacterRejected
        .to_string()
        .contains("original-synthetic-credential"));
    Ok(())
}

#[test]
fn overlong_character_is_rejected_before_network_attempt() -> Result<(), Box<dyn Error>> {
    let overlong_name = "A".repeat(CANARY_CHARACTER_NAME_MAX_BYTES + 1);
    let (lifecycle, _attempt_id, _clock) =
        lifecycle_with_credential(&overlong_name, Duration::from_secs(5))?;
    let attempts = Arc::new(AtomicUsize::new(0));
    let mut adapter = CanaryEntryAdapter::with_synthetic(
        transport_config()?,
        script(
            &overlong_name,
            SyntheticDecision::Entered,
            Arc::clone(&attempts),
        ),
    );
    let source = CancellationSource::new();
    let request = lifecycle.request().ok_or("missing overlong request")?;
    assert_eq!(
        adapter.connect(request, &source.token()),
        Err(CanaryAdmissionOutcome::CharacterRejected)
    );
    assert_eq!(attempts.load(Ordering::SeqCst), 0);
    assert_eq!(lifecycle.phase(), EntryPhase::CredentialReady);
    Ok(())
}

#[test]
fn expired_and_consumed_credentials_fail_before_network_attempt() -> Result<(), Box<dyn Error>> {
    let (mut expired, expired_attempt, expired_clock) =
        lifecycle_with_credential("Synthetic Character", Duration::from_secs(1))?;
    expired_clock.advance(Duration::from_secs(1))?;
    let expired_attempts = Arc::new(AtomicUsize::new(0));
    let mut expired_adapter = CanaryEntryAdapter::with_synthetic(
        transport_config()?,
        script(
            "Synthetic Character",
            SyntheticDecision::Entered,
            Arc::clone(&expired_attempts),
        ),
    );
    let source = CancellationSource::new();
    let request = expired
        .request()
        .ok_or("missing expired request")?
        .clone();
    expired_adapter.connect(&request, &source.token())?;
    assert_eq!(
        expired_adapter.enter_session(
            &mut expired,
            expired_attempt,
            &expired_clock,
            &source.token(),
        ),
        CanaryAdmissionOutcome::CredentialExpiredOrConsumed
    );
    assert_eq!(expired_attempts.load(Ordering::SeqCst), 0);

    let (mut consumed, consumed_attempt, consumed_clock) =
        lifecycle_with_credential("Synthetic Character", Duration::from_secs(5))?;
    let moved = consumed.begin_connecting(consumed_attempt, &consumed_clock)?;
    drop(moved);
    let consumed_attempts = Arc::new(AtomicUsize::new(0));
    let mut consumed_adapter = CanaryEntryAdapter::with_synthetic(
        transport_config()?,
        script(
            "Synthetic Character",
            SyntheticDecision::Entered,
            Arc::clone(&consumed_attempts),
        ),
    );
    let request = consumed
        .request()
        .ok_or("missing consumed request")?
        .clone();
    consumed_adapter.connect(&request, &source.token())?;
    assert_eq!(
        consumed_adapter.enter_session(
            &mut consumed,
            consumed_attempt,
            &consumed_clock,
            &source.token(),
        ),
        CanaryAdmissionOutcome::CredentialExpiredOrConsumed
    );
    assert_eq!(consumed_attempts.load(Ordering::SeqCst), 0);
    Ok(())
}

#[test]
fn cancellation_is_terminal_and_precedes_handoff() -> Result<(), Box<dyn Error>> {
    let (mut lifecycle, attempt_id, clock) =
        lifecycle_with_credential("Synthetic Character", Duration::from_secs(5))?;
    let attempts = Arc::new(AtomicUsize::new(0));
    let mut adapter = CanaryEntryAdapter::with_synthetic(
        transport_config()?,
        script(
            "Synthetic Character",
            SyntheticDecision::Entered,
            Arc::clone(&attempts),
        ),
    );
    let source = CancellationSource::new();
    let request = lifecycle
        .request()
        .ok_or("missing synthetic request")?
        .clone();
    adapter.connect(&request, &source.token())?;
    assert!(source.cancel());
    assert_eq!(
        adapter.enter_session(&mut lifecycle, attempt_id, &clock, &source.token()),
        CanaryAdmissionOutcome::Cancelled
    );
    assert_eq!(attempts.load(Ordering::SeqCst), 0);
    assert_eq!(adapter.state(), CanaryConnectionState::Closed);
    assert_eq!(lifecycle.phase(), EntryPhase::Failed);
    Ok(())
}

#[test]
fn synthetic_transcript_accepts_only_ordered_bounded_entry() -> Result<(), ProtocolError> {
    let transcript = success_transcript()?;
    assert_eq!(
        parse_transcript(&transcript, 64),
        Ok(SyntheticDecision::Entered)
    );

    let mut reordered = BoundedWriter::new(64)?;
    write_frame(&mut reordered, SYNTHETIC_ACCEPTED, None)?;
    write_frame(&mut reordered, SYNTHETIC_CHALLENGE, None)?;
    assert_eq!(
        parse_transcript(&reordered.into_inner(), 64),
        Err(ProtocolError::new(ProtocolErrorKind::UnknownValue))
    );
    Ok(())
}

#[test]
fn synthetic_transcript_rejects_malformed_truncated_oversized_and_invalid_text(
) -> Result<(), ProtocolError> {
    assert_eq!(
        parse_transcript(&[5, 0, SYNTHETIC_CHALLENGE], 64),
        Err(ProtocolError::new(ProtocolErrorKind::Truncated))
    );
    assert_eq!(
        parse_transcript(&[65, 0], 64),
        Err(ProtocolError::new(ProtocolErrorKind::Oversized))
    );
    let invalid_text = [4_u8, 0, SYNTHETIC_DENIED, 1, 0, 0xFF];
    assert_eq!(
        parse_transcript(&invalid_text, 64),
        Err(ProtocolError::new(ProtocolErrorKind::InvalidUtf8))
    );
    Ok(())
}

#[test]
fn arbitrary_bounded_synthetic_transcripts_never_panic_and_are_deterministic() {
    for length in 0..=256 {
        let bytes = vec![length as u8; length];
        let first = parse_transcript(&bytes, 256);
        let second = parse_transcript(&bytes, 256);
        assert_eq!(first, second);
    }
}
