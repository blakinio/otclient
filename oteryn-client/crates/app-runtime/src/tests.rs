use super::*;
use oteryn_account_session::AccountSessionId;
use oteryn_foundation::{Deadline, ManualClock, Moment, MonotonicClock};
use oteryn_game_session::{
    EntryFailure, EntryFailureKind, EntryPhase, GameEntryCredential, RecoveryAction,
};
use oteryn_world_directory::{
    AccountDirectorySnapshot, Availability, CharacterId, CharacterSummary, Compatibility,
    DirectoryRevision, WorldId, WorldRoute, WorldSummary,
};
use std::error::Error;
use std::io;
use std::sync::{Arc, Condvar, Mutex};
use std::thread;
use std::time::Duration;

fn snapshot() -> Result<AccountDirectorySnapshot, Box<dyn Error>> {
    let world_id = WorldId::new(11)?;
    let world = WorldSummary::new(
        world_id,
        "current".to_owned(),
        "Current".to_owned(),
        "eu-central".to_owned(),
        WorldRoute::new("127.0.0.1".to_owned(), 7172)?,
        Availability::Available,
        Compatibility::Compatible,
    )?;
    let character = CharacterSummary::new(
        CharacterId::new(22)?,
        world_id,
        "Synthetic Knight".to_owned(),
        100,
        "Knight".to_owned(),
        Availability::Available,
        Compatibility::Compatible,
    )?;
    Ok(AccountDirectorySnapshot::new(
        AccountSessionId::new(33)?,
        DirectoryRevision::new(7)?,
        vec![world],
        vec![character],
        Vec::new(),
    )?)
}

fn selection() -> Result<TechnicalSelection, Box<dyn Error>> {
    Ok(TechnicalSelection::new(
        CharacterId::new(22)?,
        WorldId::new(11)?,
        None,
    ))
}

fn credential(secret: &[u8]) -> Result<GameEntryCredential, Box<dyn Error>> {
    Ok(GameEntryCredential::new(
        secret.to_vec(),
        Deadline::at(Moment::from_elapsed(Duration::from_secs(30))),
    )?)
}

fn poll_until(
    runtime: &mut TechnicalLoginRuntime,
    expected: EntryPhase,
) -> Result<(), Box<dyn Error>> {
    for _ in 0..10_000 {
        let _progressed = runtime.poll()?;
        if runtime.snapshot().phase() == expected {
            return Ok(());
        }
        thread::yield_now();
    }
    Err(io::Error::other("runtime worker did not reach expected phase").into())
}

#[test]
fn fake_success_uses_one_handoff_and_returns_session_entered() -> Result<(), Box<dyn Error>> {
    let clock = ManualClock::new(Moment::ZERO);
    let runtime_clock: Arc<dyn MonotonicClock> = Arc::new(clock.clone());
    let mut runtime = TechnicalLoginRuntime::new(runtime_clock);
    let expected_secret = b"synthetic-session-credential".to_vec();
    let worker_secret = expected_secret.clone();

    let attempt = runtime.start_authentication(selection()?, move |_attempt, _cancellation| {
        let directory =
            snapshot().map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?;
        let credential = credential(&worker_secret)
            .map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?;
        Ok((
            AccountSessionId::new(33)
                .map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?,
            directory,
            credential,
        ))
    })?;

    poll_until(&mut runtime, EntryPhase::CredentialReady)?;
    assert_eq!(attempt.get(), 1);
    let before_connection = format!("{runtime:?}");
    assert!(!before_connection.contains("synthetic-session-credential"));
    assert!(before_connection.contains("CredentialReady"));

    runtime.start_connection(move |mut lifecycle, attempt_id, cancellation, clock| {
        let result = (|| -> Result<_, EntryFailure> {
            if cancellation.is_cancelled() {
                return Err(EntryFailure::for_kind(EntryFailureKind::SafeCancellation));
            }
            let admission = lifecycle.begin_connecting(attempt_id, clock.as_ref())?;
            if admission.expose_secret() != expected_secret.as_slice() {
                return Err(EntryFailure::for_kind(EntryFailureKind::InvariantViolation));
            }
            drop(admission);
            lifecycle.session_entered(attempt_id, clock.now())
        })();
        (lifecycle, result)
    })?;

    assert_eq!(
        runtime.start_connection(|lifecycle, _attempt, _token, _clock| {
            (
                lifecycle,
                Err(EntryFailure::for_kind(EntryFailureKind::InvariantViolation)),
            )
        }),
        Err(RuntimeError::ConnectionAlreadyActive)
    );
    poll_until(&mut runtime, EntryPhase::SessionEntered)?;
    let entered = runtime
        .snapshot()
        .entered()
        .ok_or_else(|| io::Error::other("missing SessionEntered"))?;
    assert_eq!(entered.character_id(), CharacterId::new(22)?);
    assert_eq!(entered.world_id(), WorldId::new(11)?);
    assert_eq!(entered.attempt_id(), attempt);
    assert!(!format!("{runtime:?}").contains("synthetic-session-credential"));

    let history = runtime.history().collect::<Vec<_>>();
    assert!(history.contains(&EntryPhase::Authenticating));
    assert!(history.contains(&EntryPhase::AccountReady));
    assert!(history.contains(&EntryPhase::DirectoryReady));
    assert!(history.contains(&EntryPhase::EntryRequested));
    assert!(history.contains(&EntryPhase::CredentialReady));
    assert!(history.contains(&EntryPhase::Connecting));
    assert!(history.contains(&EntryPhase::SessionEntered));

    runtime.disconnect_to_logged_out()?;
    assert_eq!(runtime.snapshot().phase(), EntryPhase::LoggedOut);
    assert!(runtime.snapshot().entered().is_none());
    Ok(())
}

#[test]
fn invalid_world_character_relation_is_typed_and_never_connects() -> Result<(), Box<dyn Error>> {
    let clock: Arc<dyn MonotonicClock> = Arc::new(ManualClock::new(Moment::ZERO));
    let mut runtime = TechnicalLoginRuntime::new(clock);
    let invalid_selection = TechnicalSelection::new(CharacterId::new(99)?, WorldId::new(11)?, None);

    runtime.start_authentication(invalid_selection, |_attempt, _cancellation| {
        Ok((
            AccountSessionId::new(33)
                .map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?,
            snapshot().map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?,
            credential(b"unused-secret")
                .map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?,
        ))
    })?;

    poll_until(&mut runtime, EntryPhase::Failed)?;
    let failure = runtime
        .snapshot()
        .failure()
        .ok_or_else(|| io::Error::other("missing typed selection failure"))?;
    assert_eq!(failure.kind(), EntryFailureKind::SelectedEntryUnavailable);
    assert_eq!(
        failure.recommended_action(),
        RecoveryAction::ChooseAnotherCharacter
    );
    assert_eq!(
        runtime.start_connection(|lifecycle, _attempt, _token, _clock| {
            (
                lifecycle,
                Err(EntryFailure::for_kind(EntryFailureKind::InvariantViolation)),
            )
        }),
        Err(RuntimeError::Entry(EntryFailure::for_kind(
            EntryFailureKind::InvariantViolation
        )))
    );
    Ok(())
}

#[test]
fn concurrent_authentication_is_rejected_and_second_attempt_is_fresh() -> Result<(), Box<dyn Error>>
{
    let clock: Arc<dyn MonotonicClock> = Arc::new(ManualClock::new(Moment::ZERO));
    let mut runtime = TechnicalLoginRuntime::new(clock);
    let first = runtime.start_authentication(selection()?, |_attempt, _cancellation| {
        Ok((
            AccountSessionId::new(33)
                .map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?,
            snapshot().map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?,
            credential(b"first-fresh-secret")
                .map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?,
        ))
    })?;
    assert_eq!(
        runtime.start_authentication(selection()?, |_attempt, _cancellation| {
            Err(EntryFailure::for_kind(EntryFailureKind::InvariantViolation))
        }),
        Err(RuntimeError::AuthenticationAlreadyActive)
    );
    poll_until(&mut runtime, EntryPhase::CredentialReady)?;

    runtime.start_connection|"mut lifecycle, attempt, _token, clock| {
        let result = (|| -> Result<_, EntryFailure> {
            let admission = lifecycle.begin_connecting(attempt, clock.as_ref())?;
            assert_eq!(admission.expose_secret(), b"first-fresh-secret");
            drop(admission);
            lifecycle.session_entered(attempt, clock.now())
        })();
        (lifecycle, result)
    })?;
    poll_until(&mut runtime, EntryPhase::SessionEntered)?;
    runtime.disconnect_to_logged_out()?;

    let second = runtime.start_authentication(selection()?, |_attempt, _cancellation| {
        Ok((
            AccountSessionId::new(33)
                .map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?,
            snapshot().map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?,
            credential(b"second-fresh-secret")
                .map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?,
        ))
    })?;
    assert_ne!(first, second);
    assert_eq!(first.get(), 1);
    assert_eq!(second.get(), 2);
    poll_until(&mut runtime, EntryPhase::CredentialReady)?;
    assert_eq!(runtime.snapshot().active_attempt(), Some(second));
    Ok(())
}

struct WorkerRelease {
    state: Arc<(Mutex<bool>, Condvar)>,
}

impl WorkerRelease {
    fn new() -> Self {
        Self {
            state: Arc::new((Mutex::new(false), Condvar::new())),
        }
    }

    fn worker_state(&self) -> Arc<(Mutex<bool>, Condvar)> {
        Arc::clone(&self.state)
    }

    fn release(&self) {
        let (lock, wake) = &*self.state;
        let mut released = match lock.lock() {
            Ok(guard) => guard,
            Err(poisoned) => poisoned.into_inner(),
        };
        *released = true;
        wake.notify_all();
    }
}

impl Drop for WorkerRelease {
    fn drop(&mut self) {
        self.release();
    }
}

#[test]
fn shutdown_is_nonblocking_reports_overdue_and_eventually_joins() -> Result<(), Box<dyn Error>> {
    let clock = ManualClock::new(Moment::ZERO);
    let runtime_clock: Arc<dyn MonotonicClock> = Arc::new(clock.clone());
    let mut runtime = TechnicalLoginRuntime::new(runtime_clock);
    let release = WorkerRelease::new();
    let worker_release = release.worker_state();

    runtime.start_authentication(selection()?, move |_attempt, cancellation| {
        while !cancellation.is_cancelled() {
            thread::yield_now();
        }
        let (lock, wake) = &*worker_release;
        let mut released = match lock.lock() {
            Ok(guard) => guard,
            Err(poisoned) => poisoned.into_inner(),
        };
        while !*released {
            released = match wake.wait(released) {
                Ok(guard) => guard,
                Err(poisoned) => poisoned.into_inner(),
            };
        }
        Err(EntryFailure::for_kind(EntryFailureKind::SafeCancellation))
    })?;

    assert_eq!(
        runtime.poll_shutdown(),
        Err(RuntimeError::ShutdownNotStarted)
    );
    assert_eq!(
        runtime.begin_shutdown()?,
        ShutdownProgress::Pending(WorkerKind::Identity)
    );
    assert!(runtime.has_active_worker());
    assert_eq!(runtime.snapshot().phase(), EntryPhase::Closing);
    assert!(runtime.snapshot().shutting_down());

    clock.advance(SHUTDOWN_OVERDUE_AFTER)?;
    assert_eq!(
        runtime.poll_shutdown()?,
        ShutdownProgress::Overdue(WorkerKind::Identity)
    );
    assert!(runtime.has_active_worker());
    assert_eq!(
        runtime.start_authentication(selection()?, |_attempt, _cancellation| {
            Err(EntryFailure::for_kind(EntryFailureKind::InvariantViolation))
        }),
        Err(RuntimeError::ShuttingDown)
    );

    release.release();
    for _ in 0..10_000 {
        if runtime.poll_shutdown()? == ShutdownProgress::Complete {
            assert!(!runtime.has_active_worker());
            assert_eq!(runtime.snapshot().phase(), EntryPhase::LoggedOut);
            assert!(runtime.snapshot().shutting_down());
            return Ok(());
        }
        thread::yield_now();
    }
    Err(io::Error::other("shutdown worker did not finish after release").into())
}
