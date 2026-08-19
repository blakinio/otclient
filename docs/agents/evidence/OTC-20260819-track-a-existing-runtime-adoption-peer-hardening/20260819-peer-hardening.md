# Existing-runtime adoption peer hardening evidence

Source: merged #596 / `a71dda46742d8db1bdddfa5d225e9b32703b2080`.

## Findings

- `P1-PEER-IDENTITY`: the structural bridge script validated returned PING identity fields but did not verify the actual Unix-domain socket peer PID.
- `P1-UNVERIFIABLE-CANDIDATE`: a plausible `client`/`Tibia*` process with an unreadable `/proc/<pid>/exe` could be skipped by the Docker inventory.

## Remediation

- every bridge connection now reads Linux `SO_PEERCRED` and requires peer PID equality with the freshly inventoried exact client PID before accepting a response;
- the embedded bridge script receives the expected PID explicitly and applies the check independently for PING and each of the three discovery requests;
- candidate inventory reads `/proc/<pid>/comm`; if a plausible `client`/`Tibia*` process cannot resolve its executable it emits an explicit `UNREADABLE` candidate which is rejected fail-closed;
- no new runtime, login, credential, input, process-control or transaction authority is introduced.

## Focused tests

Added deterministic tests for correct Unix peer acceptance, wrong Unix peer rejection and plausible unreadable-process rejection. Existing exact target, wrong SHA, second candidate, bridge mismatch, title-only UNKNOWN and X11 PID mismatch tests remain.

## Validation result

```text
Kasm adoption probe: 9/9 PASS
canonical transition regression: 17/17 PASS
Track A runtime governance: PASS
Python compile: PASS
git diff --check: PASS
```
