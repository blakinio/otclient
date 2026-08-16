# Track A bootstrap admission reconciliation

## Problem

Trusted `main` already contains the reviewed canonical bootstrap/rebind/Gate-B implementation from PR #371, merged as `d16091ca29ff7c9330115e9ce0fdbfb41646e0dc`, and its lifecycle archive PR #375 merged as `259e418b2c526f93bd697f07c42b73b1fd40a914`.

The deterministic admission validator nevertheless still unconditionally rejected `runtime_access: canonical_bootstrap` whenever `mutation_authorized: true`, producing the v7 policy failure `bootstrap is not currently implemented/authorized` even though the implementation had already been promoted.

The repository contract itself is conditional: before a reviewed implementation is promoted and a concrete execution is separately authorized, bootstrap must remain fail-closed. Both the implementation and its archive are now present on trusted main; this owner invocation separately requests completion of the existing RUNTIME task. The remaining work is therefore to reconcile the validator with those already-promoted facts without weakening the bootstrap transaction.

## Reconciled semantics

An active task may claim `canonical_bootstrap` + `mutation_authorized: true` only to invoke the reviewed fail-closed bootstrap transaction, and only when all of these task-level pre-run facts are explicit:

- authoritative registration is `ABSENT`;
- pre-run lease generation is `UNKNOWN` rather than a stale authority claim;
- `gate_a: REQUIRED_NOT_PROVEN` because the reviewed transaction must acquire/validate the current lease under the canonical flock;
- `bootstrap: PASS` means the reviewed implementation is present on the trusted base;
- `target_uniqueness: UNKNOWN` because complete absence/uniqueness must be freshly proven under the flock immediately before child creation;
- `bootstrap_attempt_limit: 1`;
- a non-empty `live_runtime_authorization_source`;
- credentials, login and gameplay remain false.

`mutation_authorized: true` does not authorize an out-of-band launch. The transition must still fail closed unless its internal Gate A and under-lock all-official-client inventory pass.

## Trusted implementation proof

The deterministic validator now verifies the trusted base directly:

- transition file exists and contains the cancellation-safe bootstrap/rebind/Gate-B implementation, canonical flock acquisition, bootstrap worker dispatch, staging/atomic commit and candidate inventory;
- archive task `OTC-20260816-track-a-canonical-bootstrap-implementation` exists with `status: completed`, `implementation_pr: 371`, exact merge `d16091ca29ff7c9330115e9ce0fdbfb41646e0dc`, and released ownership.

A task claim cannot fabricate these repository facts.

## Safety boundary

This reconciliation branch has `runtime_access: none` and `mutation_authorized: false`. It does not run Synology, acquire a canonical lease, inspect registration/session state, launch the official client, use credentials, log in, perform gameplay, or touch Track B / historical PR #303 runtime surfaces.

The reconciliation cannot authorize its own physical use while unmerged. A physical attempt is allowed only after this change reaches trusted main and the canonical-runtime task is freshly re-admitted from that new base.

## Validation

A temporary GitHub-hosted validator exercises positive and negative transactional-admission cases and is removed before final merge. Standard Track A governance and repository CI must also pass on the exact final head.

## Expected next action after promotion

Freshly re-admit `OTC-20260816-track-a-canonical-runtime-e2e` from the new trusted main for exactly one no-credential canonical bootstrap + immediate same-generation Gate B attempt using the repaired Xvfb DRI-provider environment. No blind retry is authorized after a new discriminator.
