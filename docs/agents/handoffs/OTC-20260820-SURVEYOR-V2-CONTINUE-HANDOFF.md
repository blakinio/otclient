# OTC-20260820 Surveyor v2 continuation handoff

## Current state

Continue from the existing merged Surveyor v2 implementation. Do not redesign.

Completed:

- Surveyor v2 collect-all implementation merged.
- Read-only physical operator merged.
- Unrelated Docker container timeout hardening merged.

Relevant merged work:

- Surveyor v2 implementation: `6f17e25af655854624b34e0b05f9888618269aba`
- Read-only operator: `02fce7e25696ffea3e11c4fc89f458e27f47bef4`
- Timeout hardening: `08b6838dcce3fa62b05ac6a87f10bdbd8b74ebd3`

## Runtime evidence already obtained

Read-only physical run proved:

- exact client candidates: 1
- target exact clients: 1
- target window matches: 1
- target uniqueness: PROVEN
- canonical registration: PRESENT
- lease generation: 17
- registration lease generation: 17
- structural state: `BRIDGE_3_OF_3 PASS`
- owner login required: NO

Do not login, logout, restart, inject, send input, or mutate runtime unless a future task is separately admitted by Track A governance.

## Remaining action

Run the trusted-main Surveyor v2 read-only workflow again after the timeout hardening.

Expected final artifacts:

- coverage bundle
- 12 alias views
- telemetry outputs
- missing-readers.json
- privacy scan PASS
- manifest

Expected final markers:

```
COLLECTOR_READY=YES
STRUCTURAL_IN_GAME=PASS
OWNER_LOGIN_REQUIRED=NO
RUNTIME_MUTATION=false
```

## Next agent prompt

```
Alias:
OTCLIENT-TIBIA-RE-SURVEYOR-V2-FINAL-COLLECT-ALL-CONTINUE

Repository:
blakinio/otclient

Continue autonomously from current main.

First read:
- AGENTS.md
- Track A runtime admission contract
- KasmVNC runtime access contract
- hybrid execution routing
- current task ownership

Verify current main and do not trust historical chat as authority.

Objective:
Complete the final Surveyor v2 read-only collection.

Steps:
1. Verify timeout hardening is present on current main.
2. Run the trusted read-only physical operator.
3. Collect sanitized bundle.
4. Verify all artifacts and privacy scan.
5. If any issue appears, fix minimally with tests and audit.
6. Do not perform login or gameplay actions because current evidence already shows OWNER_LOGIN_REQUIRED=NO.

Finish with exact evidence:
- run id
- CI status
- governance status
- artifact verification
- next action.
```
