use super::*;
use oteryn_account_session::AccountSessionId;
use oteryn_foundation::{Deadline, ManualClock, Moment, MonotonicClock};
use oteryn_game_session::{EntryFailure, EntryFailureKind, EntryPhase, GameEntryCredential};
use oteryn_world_directory::{
    AccountDirectorySnapshot, Availability, CharacterId, CharacterSummary, Compatibility,
    DirectoryRevision, WorldId, WorldRoute, WorldSummary,
};
use std::error::Error;
use std::io;
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

fn directory() -> Result<AccountDirectorySnapshot, Box<dyn Error>> {
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

fn credential() -> Result<GameEntryCredential, Box<dyn Error>> {
    Ok(GameEntryCredential::new(
        b"runtime-thread-proof".to_vec(),
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
    Err(io::Error::other("runtime task did not reach expected phase").into())
}

#[test]
fn connection_admission_runs_on_named_tokio_worker_not_caller_thread() -> Result<(), Box<dyn Error>>
{
    let clock: Arc<dyn MonotonicClock> = Arc::new(ManualClock::new(Moment::ZERO));
    let mut runtime = TechnicalLoginRuntime::new(clock);
    runtime.start_authentication(selection()?, |_attempt, _cancellation| {
        Ok((
            AccountSessionId::new(33)
                .map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?,
            directory()
                .map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?,
            credential()
                .map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?,
        ))
    })?;
    poll_until(&mut runtime, EntryPhase::CredentialReady)?;

    let caller_name = thread::current().name().map(str::to_owned);
    let observed_name = Arc::new(Mutex::new(None::<String>));
    let worker_observation = Arc::clone(&observed_name);
    runtime.start_connection(move |mut lifecycle, attempt, cancellation, clock| {
        let current_name = thread::current().name().map(str::to_owned);
        match worker_observation.lock() {
            Ok(mut guard) => *guard = current_name,
            Err(poisoned) => *poisoned.into_inner() = current_name,
        }
        let result = (|| -> Result<_, EntryFailure> {
            if cancellation.is_cancelled() {
                return Err(EntryFailure::for_kind(EntryFailureKind::SafeCancellation));
            }
            let admission = lifecycle.begin_connecting(attempt, clock.as_ref())?;
            drop(admission);
            lifecycle.session_entered(attempt, clock.now())
        })();
        (lifecycle, result)
    })?;
    poll_until(&mut runtime, EntryPhase::SessionEntered)?;

    let observed = match observed_name.lock() {
        Ok(guard) => guard.clone(),
        Err(poisoned) => poisoned.into_inner().clone(),
    }
    .ok_or_else(|| io::Error::other("Tokio worker thread name was not observed"))?;
    assert!(observed.starts_with("oteryn-network"));
    assert_ne!(Some(observed), caller_name);
    runtime.disconnect_to_logged_out()?;
    Ok(())
}
