# Auth/session reader post-merge physical acceptance plan

Implementation merge under acceptance: `16f83cf70548cbbe1eb6cb3838d27fbe6e0430e3` (PR #636).

The pre-implementation physical baseline is already durable: 169 canonical rows, 12 aliases, 10 missing typed readers and privacy PASS; `auth_session_typed_reader` was `NO_TYPED_READER_IMPLEMENTED`.

This closeout uses a temporary trusted-main, self-hosted, read-only workflow. The workflow is inert on pull-request execution and is eligible only after merge to `main`, only for actor `blakinio`, and only when the merge commit contains `ONE_SHOT_SURVEYOR_AUTH_READ_ONLY`.

Before any semantic read it fails closed unless the declared Track A target has no conflicting fresh lease owner, exactly one exact-fenced client, a working display, exactly one matching visible Tibia window, stable process-start identity, and matching canonical registration identity when registration exists.

The only semantic operation is the merged Surveyor `--collect-all`. Acceptance requires the auth reader to be `AVAILABLE`, `process_memory_access=read_only`, `semantic_state=TYPED_AUTH_LIFECYCLE_ONLY`, `in_game_claimed=false`, no credential/session-secret retention, 12 aliases, 9 missing readers and privacy PASS.

No login/logout/relogin, GUI/gameplay input, process control, attach/debug/injection, process-memory write, restart, network mutation, item/economy action or local-model execution is authorized.

The exact causal delta is the implementation delta: auth reader `NO_TYPED_READER_IMPLEMENTED -> AVAILABLE`, missing readers `10 -> 9`, privacy `PASS -> PASS`. The lifecycle boolean may remain unchanged; it is not an `IN_GAME` discriminator.
