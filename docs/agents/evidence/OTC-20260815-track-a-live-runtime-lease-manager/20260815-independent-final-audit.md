# Independent final audit — Track A canonical live lease manager

Task: `OTC-20260815-track-a-live-runtime-lease-manager`  
Final audit run: `31910612285`  
Audit job: `95074977302`  
Unit job: `95074977275`  
Isolated Synology job: `95074977279`  
Audited head: `ecf8600fe11556a78944149efc5c10b47ade8259`  
Validator: fresh GitHub-hosted `ubuntu-24.04` Actions job  
Implementation authorization: false  
Objective: falsify acceptance and the material concurrency/safety findings from PRs #312/#313/#316 without trusting the implementer summary.

## Result

```yaml
audit:
  result: PASS
  findings_open_material: 0
  runtime_e2e: NOT_APPLICABLE
```

## Review-remediation cycle — FACT

The first fresh audit run (`31910490313` / `95074686558`) passed the lease/supervisor acceptance checks. A separate automatic PR review then found a material P1 in the new **test cleanup**: after successful lock release the test still sent `SIGKILL` to a daemon's saved numeric PID, which could have been reused by an unrelated same-UID process on the shared Synology runner.

Commit `024a71f929e331af26b6edc9d03aee3697b412e6` removed that signal path entirely. Once the independent flock can be reacquired, the supervisor has already waited/reaped the daemon; no numeric PID cleanup is necessary or safe. The regression now cleans only the task-owned guard caller and its pipes.

Because this was a material safety finding, all affected gates were rerun. Final audit run `31910612285` passed:

```text
unit=95074977275 SUCCESS
isolated_synology=95074977279 SUCCESS
fresh_audit=95074977302 SUCCESS
```

## Direct audit checks — PASS

The fresh audit job checked the resulting repository files directly and required all of the following before PASS:

- production shell entrypoint names the dedicated canonical guard supervisor helper;
- production `guard-run` routes through that helper at the fixed canonical state root;
- supervisor helper uses Linux `PR_SET_CHILD_SUBREAPER`;
- supervisor launches the guarded command with `close_fds=True`;
- supervisor helper contains no `pass_fds=` path that would give the guarded command control of the flock descriptor;
- lease and supervisor helpers compile under Python;
- the full existing lease-manager deterministic suite passes;
- the supervisor adversarial suite passes after the P1 test-cleanup fix;
- Python `ResourceWarning` is elevated during the audit job for new supervisor-test resource handling.

The audit emits `TRACK_A_CANONICAL_LEASE_FRESH_AUDIT_PASS=true` on success.

## Prior material findings rechecked

| Finding | Audit evidence | Result |
|---|---|---|
| concurrent controller acquisition must serialize | existing deterministic lease suite | PASS |
| expired holder must not bypass stale-takeover reason through release | existing deterministic lease suite | PASS |
| lease-sensitive time must be sampled after flock acquisition | existing deterministic lease suite | PASS |
| guard caller death must not release serialization while mutation survives | supervisor adversarial suite | PASS |
| guarded command must not control/close the flock descriptor | static production-route check + `close_fds=True` + no `pass_fds=` in supervisor helper | PASS |
| daemonized descendant must keep serialization held after caller death and FD closure | adversarial caller-kill + FD-close + fork/`setsid()` regression | PASS |
| shared-runner test cleanup must not signal a potentially reused PID | P1 remediation `024a71f...` + final unit/Synology/audit rerun | PASS |
| production canonical state must not be mutated by isolated Synology validation | final isolated Synology job `95074977279` plus existing self-test invariant | PASS |

## Scope/security audit

- fixed production entrypoint and task-local token confinement remain in the shell wrapper;
- shared state stores token digest rather than raw capability token, as covered by the existing suite;
- status remains token-redacted, as covered by the existing suite;
- no Tibia runtime/client/login/display/input/ptrace/VNC state is part of this manager validation;
- no production canonical runtime identity is asserted;
- `:98` remains unregistered/not proven canonical;
- PR #303/#309 runtime-owned surfaces and Track B are outside the changed-file set;
- no owner-funded Codex/OpenAI API or paid AI quota was used to run this deterministic audit.

## Compatibility and residual boundary

The supervisor is intentionally native-Linux-only, matching Track A runtime policy. The manager is cooperative same-UID programme coordination, not a hostile-local-user security boundary. A malicious same-UID process that deliberately kills the supervisor is outside the accepted threat model; ordinary guarded-program FD cleanup and daemonization are covered.

## E2E classification

`NOT_APPLICABLE` for live Tibia runtime mutation: this manager is infrastructure that must not mutate a live client during validation. Its complete applicable path is public lease CLI/production routing -> serialized processing -> isolated state transition/descendant lifetime -> observable exit/status semantics, covered by deterministic, isolated Synology and fresh audit runs.

## Final-head consequence

After final audit, only durable audit/task evidence and removal of the temporary remediation-branch workflow trigger change the branch. Production supervisor/wrapper/test logic audited at `ecf8600...` is unchanged. Repository `CI / Required` must still pass on the exact final merge head before PR #316 can merge.
