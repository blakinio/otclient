# Surveyor auth/session typed reader — physical read-only acceptance

Date: 2026-08-21

Task: `OTC-20260820-surveyor-auth-session-reader`

## Result

**PASS**

The auth/session typed reader merged by PR #636 was accepted on the physical official-client runtime through a bounded read-only Surveyor `--collect-all` run. The causal discriminator is implementation availability, not a login-state transition.

## Implementation under acceptance

- implementation PR: #636
- implementation merge SHA: `16f83cf70548cbbe1eb6cb3838d27fbe6e0430e3`
- trusted main snapshot used by the physical job: `301e3f57d4537b9cc1d97a320c0cc8060feb2026`
- reader: `auth_session_typed_reader`
- semantic state: `TYPED_AUTH_LIFECYCLE_ONLY`
- `in_game_claimed=false`
- `semantic_promotion_allowed=false`
- `credentials_retained=false`
- `session_secrets_retained=false`
- process memory access: `read_only`

## Physical run

- workflow run: `32478932597`
- authority job: PASS
- physical acceptance job: `96760979049`, PASS
- sanitized artifact: `9445354500`
- artifact name: `track-a-surveyor-auth-session-postmerge-32478932597`
- artifact size: `45586` bytes
- artifact digest: `sha256:f62c0a0034d1bbbdc372aa9ff2db6fbadc70300249609c90ab0dacfd9065ccdc`

The physical job checked out exact trusted main `301e3f57d4537b9cc1d97a320c0cc8060feb2026`, proved implementation ancestry, then revalidated the target from scratch before opening the read-only observation path.

## Fresh exact target identity

- target container: `otclient-track-a-kasmvnc`
- display: `:1`
- exact client processes in namespace: `1`
- matching visible Tibia windows: `1`
- target uniqueness: `PROVEN`
- PID: `19590`
- process start ticks: `76611792`
- executable path: `/home/kasm-user/otclient-track-a/Tibia-32177065988-1/bin/client`
- executable size: `52109920`
- SHA-256: `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`

Canonical control-plane state during admission:

- runtime owner task: `NOT_APPLICABLE`
- lease status: `released`
- lease generation: `19`
- canonical registration: present and identity-matching
- registration generation: `2`
- registration lease generation: `19`
- registration semantic state: `UNKNOWN`

`UNKNOWN` registration semantic state and bridge structural presence were not promoted to `IN_GAME` evidence.

## Live reader observation and causal delta

Physical `--collect-all` result:

- canonical rows: `169`
- aliases: `12`
- runtime admission: `READ_ONLY_ADMITTED`
- auth reader after: `AVAILABLE`
- authentication state-machine running: `false`
- missing typed readers after: `9`
- privacy: `PASS`

Pre-implementation baseline:

- auth reader before: `NO_TYPED_READER_IMPLEMENTED`
- missing typed readers before: `10`
- privacy before: `PASS`

Exact causal implementation delta:

- reader: `NO_TYPED_READER_IMPLEMENTED -> AVAILABLE`
- missing typed readers: `10 -> 9`
- privacy: `PASS -> PASS`

The lifecycle boolean was observed as `false`; it is deliberately not used as an `IN_GAME` discriminator and was not required to transition for this implementation-causal acceptance.

## Safety evidence

The physical job declared and enforced:

- credential access: none;
- GUI/gameplay input: none;
- process control: none;
- process-memory writes: none;
- network mutation: none;
- runtime mutation: none;
- PR-head code execution on the self-hosted runner: none.

No login/logout/relogin, character selection, client/container restart, attach/debug/injection, inventory action, attack, trade, economic action or local-model execution was performed.

## Validation chain

Implementation exact head `18bee436f57915bf61d59f0d068448a5b91e6ab1`:

- 40/40 focused Surveyor tests: PASS;
- repository-only collect-all: 169 rows / 12 aliases / 9 missing readers / privacy PASS;
- CI `32452573404`: PASS;
- Track A agent runtime governance `32452573189`: PASS;
- Track A canonical-live governance `32452573109`: PASS;
- fresh exact-head validator audit: PASS, material findings 0.

Final direct physical trigger exact head `c526d6582535b14be742fc37d32a29789cd5199b`:

- CI `32478932786`: PASS;
- physical workflow `32478932597`: PASS;
- authority: PASS;
- trusted checkout and implementation ancestry: PASS;
- fresh target/control-plane preflight: PASS;
- passive collect-all/assertions: PASS;
- sanitized artifact upload: PASS.

This evidence closes only the auth/session typed-reader slice. The broader Surveyor program still has nine missing typed-reader gaps after this acceptance.
