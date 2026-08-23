# Package C checkpoint — 2026-08-23

## Scope

This checkpoint preserves the current state of `OTCLIENT-TIBIA-RE-CONTROL-CENTER-PACKAGE-C` without changing the audited implementation PR head.

- implementation PR: `#663`
- implementation branch: `feat/OTC-20260822-tibia-re-control-center-package-c`
- final candidate head: `7e4c6435c3715b7e97d8b7827ca052cf33743cf8`
- last restacked base: `762436c25433b7bb192e6014cb4e46afc58dfc4b`
- current main observed while checkpointing: `56499ec5767093f69f09c581c54957714382e107`
- current main advances are Package D transport/governance only and do not touch the two Package C implementation files.
- runtime access remained `none`; Official Tibia runtime/client was not accessed.

## Delivered implementation

Package C adds a strict repository-only Surveyor bundle provider and its regression suite. The provider validates the pinned producer/interface, schemas, provenance, privacy, bounded file-set/size rules, typed-reader evidence envelopes, runtime admission evidence and non-promotion semantics before emitting normalized Control Center read models.

The PR continues to change exactly:

- `tools/tibia_re_control_center/surveyor_provider.py`
- `tests/tools/tibia_re_control_center/test_package_c_surveyor_provider.py`

## Material hardening completed

Independent audits found and the branch repaired all material findings observed during the task, including:

- privacy scanning of decoded and non-JSON producer-scanned text payloads;
- bounded file reads, directory traversal and JSON structural/integer parsing;
- strict runtime, lease, registration, executable fence, window and typed-reader provenance;
- stable POSIX `dir_fd`/`O_NOFOLLOW` traversal plus nonblocking final opens;
- Windows reparse-point/junction rejection;
- Windows transient-junction TOCTOU closure using stable directory handles, handle-relative `NtCreateFile`, handle-based bounded directory enumeration, and removal of pathname fallback.

The final Windows race regression transiently replaces `telemetry` with a junction only during one `player-state.json` leaf read and restores the original pathname immediately after leaf close. The provider remains bound to the original parent handle and consumes the original manifest-selected payload.

## Fresh validation on `7e4c6435c3715b7e97d8b7827ca052cf33743cf8`

- Windows Control Center suite: `210 passed, 2 skipped, 125 subtests passed`.
- WSL/POSIX focused hardening: `4 passed, 54 deselected`.
- Ruff: PASS.
- `git diff --check`: PASS.
- Package A workflow `32644841117`: SUCCESS.
- independent Codex exact-head audit: PASS; comment `5386480934` says no major issues and identifies reviewed commit `7e4c6435c3`.
- pull request review threads: zero unresolved.

## Remaining terminal gate

Repository CI run `32644841268` is still `in_progress` for the exact final candidate head. All fast checks are green; the only pending jobs are:

- `Build - Linux / Compile (linux-tests)` — `Run CMake` in progress;
- `Build - Linux / Compile (linux-release)` — `Run CMake` in progress.

This is the only remaining implementation-PR gate recorded by this checkpoint. Do not claim terminal completion until that exact-head run succeeds and PR `#663` reaches a terminal merged state.

## Handoff

Exactly one next action:

`Verify CI run 32644841268 is SUCCESS for 7e4c6435c3715b7e97d8b7827ca052cf33743cf8; then merge PR #663 with expected-head protection and perform the mandatory terminal archive/ownership-release closeout.`

Shared `docs/agents/MODULE_CATALOG.md` and `docs/agents/CHANGELOG.md` remain deferred because open PR `#23` owns those shared files. This checkpoint does not modify them.
