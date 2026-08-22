# Control Center parallel prompts post-merge repair evidence

- merged source PR: #650
- merged source commit: `9c54c1a4e22db974109298a23be39d9b04305e76`
- triggering independent finding: P1 `Use a declared completion-policy value`
- affected headers: Package B/C/D-prep canonical prompts and aliases
- preserved routing: `run_scope: single_task`, `continuation_policy: stop_at_task_boundary`
- repaired completion policy: `task_completion_policy: finalize_archive_and_continue`
- rationale: Prompting Standard 2.1 declares `checkpoint_only | finalize_archive_and_continue`; the stop-at-task-boundary routing prevents follow-on task selection while allowing normal archival semantics.
- runtime access: none
- official client access: none
- credentials/login/gameplay/mutation: not authorized

Validation before publication: `git diff --check` PASS; branch diff from merged main is limited to the six header one-line repairs, original task evidence update, this repair task/evidence.
