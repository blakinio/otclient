# Track A RUNTIME observer cleanup hardening

Task: `OTC-20260815-track-a-runtime-reacquisition`

Classification: `FACT / SAFETY_REPAIR`

Exact repair head at creation: `4bd5cbc47fbfd816a6ab5dd66b57c88b3ff981f4`.

## Finding

The task helper's `stop_generation()` sends `SIGINT` to the task-owned GDB observer and waits, but does not itself fail if that observer remains alive. Its final `cleanup_all()` also invokes `stop_generation 1 || true` and `stop_generation 2 || true`, so a stop failure can be suppressed before the task run root is removed.

That combination is unsafe for this validation lane: a surviving observer or an ownership/cleanup failure must prevent deletion of the run-local PID/evidence namespace rather than allowing later cleanup to discard recovery state.

## Bounded repair

The task workflow now fail-closes around the existing helper without broadening ownership:

- after the explicit generation-1 stop, it checks the run-local `observer-gen-1.pid` and fails if that observer still exists;
- the final always-run cleanup first calls `stop` for generations 1 and 2 without suppressing failures;
- after each stop it checks the corresponding task-local observer PID and aborts if still alive;
- only after both generation stops are clean does it invoke the helper's namespace cleanup.

No process outside the task marker/state namespace is signalled by this repair. No X11 socket/lock is deleted. Track B is untouched. No credential value is read, printed, persisted or artifacted.

## Evidence boundary

This repair improves fail-closed cleanup semantics only. It does **not** prove:

- that `synology-otclient-01` is currently online;
- that protected Tibia login secrets are populated or valid;
- structural `IN_GAME` in generation 1 or 2;
- fresh PID/PIE restart/relogin reacquisition;
- bridge `session_epoch` / R4 semantics;
- A3 or A4.

The runtime semantic experiment remains waiting on assignment of the serialized self-hosted lane after the separately owned P0 job.
