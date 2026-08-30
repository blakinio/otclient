# OTC-20260829 Track A Kasm canonical bootstrap — repository validation

## Scope

Repository-only implementation evidence for PR #801. This document does **not** claim a physical bootstrap, login, character selection, gameplay, process-memory observation or semantic promotion.

## Why prior-boot invalidation is required

Fresh trusted-main memory-free preflight `33261982889 / 99125374010` on `main@d05744b746b33c979b85ba25442ffab7298ba786` completed canonical-registration resolution successfully, proving the authoritative registration was still present for `otclient-track-a-kasmvnc` with registered PID `13947` / start ticks `51652120`. The subsequent all-running-container exact-client inventory failed closed with `OFFICIAL_CLIENT_CANDIDATE_COUNT=0`. No admission, logger, `/proc/<pid>/mem` access or process mutation followed.

This excludes both ordinary `adopt-existing` and `canonical_boot_epoch_recovery`: there is no current singleton client to bind. The accepted design therefore requires metadata-only `prior_boot_zero_client_invalidation_v1` before a separate `create_new` bootstrap admission.

## Deterministic TDD evidence

Validated locally with Linux Python where Linux process primitives are required:

- canonical transition suite: **58 tests PASS**;
- Kasm bootstrap worker suite: **11 tests PASS**;
- existing Kasm runtime probe regression suite: **10 tests PASS**;
- two-phase workflow/security contract: **6 tests PASS**;
- Track A runtime governance with branch-bound sensitive-path audit: PASS;
- independent self-hosted PR boundary audit: PASS;
- workflow YAML parse: PASS;
- Python compilation and `git diff --check`: PASS.

The tests cover zero-client preflight, boot identity, direct detached exact launch, launch/preflight binding, exact PID/start/path/size/SHA rollback, registration races, concurrent replacement preservation, rollback failure, prior-boot invalidation same-boot rejection, newer-generation requirement, registration/container drift, post-delete failure without stale-registration restoration, parser/dispatch boundaries and legacy bootstrap regressions.

## Self-hosted security boundary

The physical job is syntactically unreachable from `pull_request` and requires repository owner + `refs/heads/main` + exact workflow-dispatch authorization + `GITHUB_RUN_ATTEMPT == 1`. It uses `permissions: {}` and anonymously clones the public repository instead of passing `GITHUB_TOKEN` to a checkout action on the Synology runner.

Before either lease is acquired, a fixed task-local `bootstrap-attempt-consumed.json` is created with `O_CREAT|O_EXCL`; any pre-existing marker refuses the transaction. The invalidation and create-new phases use distinct task IDs, token files, sessions and canonical leases.

## Runtime boundaries preserved

- implementation task: `runtime_access: none`;
- invalidation live task: future separate `canonical_recovery`, `mutation_authorized: false`;
- bootstrap live task: future separate `canonical_bootstrap`, one process-control action budget;
- credentials/login/relogin/character selection/gameplay/GUI input remain false;
- no packet capture, debugger attach or process-memory observation;
- semantic state remains `UNKNOWN`;
- semantic promotion remains separate and unauthorized.

## Next gate

Restack PR #801 onto current trusted `main`, run exact-head hosted CI/security review, merge only after green gates, then create the two separate trusted-main live task admissions with the concrete current registration generation. Only after those records are merged may the owner-only workflow be dispatched once.
