fn scale_factor_milli(scale_factor: f64) -> Option<u32> {
    if !scale_factor.is_finite() || scale_factor <= 0.0 {
        return None;
    }
    let scaled = (scale_factor * 1_000.0).round();
    if scaled >= f64::from(u32::MAX) {
        Some(u32::MAX)
    } else if scaled < 1.0 {
        Some(1)
    } else {
        Some(scaled as u32)
    }
}

fn spawn_wake_worker(
    proxy: EventLoopProxy<ShellUserEvent>,
) -> Result<JoinHandle<()>, RuntimeError> {
    thread::Builder::new()
        .name(String::from("oteryn-shell-wake"))
        .spawn(move || {
            let _send_result = proxy.send_event(ShellUserEvent::Wake {
                generation: PROCESS_GENERATION,
            });
        })
        .map_err(|_error| RuntimeError::WorkerSpawn)
}

fn run() -> Result<(), RuntimeError> {
    let event_loop = EventLoop::<ShellUserEvent>::with_user_event()
        .build()
        .map_err(|_error| RuntimeError::EventLoopCreation)?;
    event_loop.set_control_flow(ControlFlow::Wait);
    let proxy = event_loop.create_proxy();
    let wake_worker = spawn_wake_worker(proxy.clone())?;
    let mut application = ShellApplication::new(proxy)?;

    let run_result = event_loop
        .run_app(&mut application)
        .map_err(|_error| RuntimeError::EventLoopRun);
    let join_result = wake_worker
        .join()
        .map_err(|_panic_payload| RuntimeError::WorkerJoin);

    run_result?;
    join_result?;
    if let Some(failure) = application.failure {
        return Err(failure);
    }
    Ok(())
}

pub fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("{error}");
            ExitCode::FAILURE
        }
    }
}
