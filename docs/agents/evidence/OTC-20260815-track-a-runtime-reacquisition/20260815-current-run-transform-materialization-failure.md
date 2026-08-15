# Track A RUNTIME current-run PID transform materialization checkpoint

Task: `OTC-20260815-track-a-runtime-reacquisition`
Draft PR: `#303`
Failed execution head: `bd1ccaed23d583bd22cb9694a455e157c1a95977`
Run: `31885464699`
Job: `95014013014`
Runner: `synology-otclient-01`, id `21`
Conclusion: `FAILURE`
Artifact id: `9247133315`
Artifact ZIP SHA-256: `3a1a36f1c5ab6fae18e0453164b26a44c070e29e89f55a2caa7b4f88963e87eb`

## FACT

The run passed checkout and the exact resume-request/helper/client fences, then failed inside the task-local helper-materialization step before residue recovery, bootstrap, Xvfb/client launch or login.

The exact failure was:

```text
compatibility transform match count 0, expected 1:
'  OTCLIENT_TIBIA_RE_ROLE="client-gen-$gen" HOME="$root/home-gen-$gen" DISPLAY="$TRACK_DISPLAY" ...'
```

This is a workflow code-generation mismatch: the attempted bulk client block normalized indentation differently from the exact repository helper. Because the fail-closed transform never reached `out.write_text`, no effective helper was exported and no RUNTIME process was started by run #14.

The fallback cleanup invoked the original helper against a run root that had never been bootstrapped and therefore reported `refuse_unmarked_run_root_cleanup`; generation stop probes themselves were harmless and no task X11 residue was present. No protected login step ran and no gameplay action occurred.

## Repair

Execution head `6e4a203d7d7d79818d7b199708c3d75a8c20a62c` replaces the fragile whole-client/whole-observer block matchers with small exact-match transformations for:

1. current-run marker injection;
2. `setsid` launch line;
3. the short post-launch client PID block;
4. the short post-launch observer PID block.

The design remains fail-closed: each source fragment must occur exactly once. PID discovery still requires Track + Task + current workflow Run + Role + exact executable before a canonical PID file is written. Cleanup now explicitly exits without invoking the original helper when materialization failed and no effective helper exists.

Run `31885655644` is the only active execution of this repair. No conceptual duplicate should be dispatched while it is active.
