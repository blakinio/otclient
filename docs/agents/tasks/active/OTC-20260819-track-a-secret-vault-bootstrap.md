---
task_id: OTC-20260819-track-a-secret-vault-bootstrap
status: validating
agent: ChatGPT
branch: ci/OTC-20260819-track-a-secret-vault-bootstrap
base_branch: main
lane: RUNTIME
track_id: official-client-re
risk: high
owned_paths:
  - .github/workflows/track-a-secret-vault-bootstrap.yml
  - tools/tibia_runtime_bridge/secret_vault.py
  - docs/agents/tasks/active/OTC-20260819-track-a-secret-vault-bootstrap.md
runtime_access: none
credentials_allowed: repository_secrets_only_for_vault_seeding
login_allowed: false
mutation_authorized: vault_state_only
---

# Track A machine-local secret vault bootstrap

Objective: seed `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` from GitHub Actions Secrets into an encrypted machine-local vault on `synology-otclient-01`, without persisting plaintext credentials or exposing them in logs, argv, artifacts, repository files, or the Tibia client environment.

Implemented design:

- persistent encrypted CMS envelope under `/work/_otclient_tibia_re_state/secret-vault` in the self-hosted runner Docker volume;
- RSA-4096 private key generated only on Synology, mode `0600`; vault directory mode `0700`;
- Secrets consumed only by the bounded self-hosted seed step with shell tracing disabled and core dumps disabled;
- plaintext credential frame exists only in process memory during sealing/use;
- `secret_vault.decrypt_to_sealed_memfd()` decrypts directly to memory and returns a fully sealed anonymous memfd for the existing native-auth transport;
- final workflow is `workflow_dispatch` only; the temporary branch push trigger was removed after the first successful seed;
- this task performs no Tibia login and does not expand PR #528 runtime admission.

Verified 2026-08-19:

```text
runner: synology-otclient-01
runner container: otclient-synology-runner
persistent mount: /work -> Docker volume otclient-runner_runner_work
bootstrap job result: SUCCESS
vault directory mode: 700
private key mode: 600
CMS envelope mode: 600
SECRET_VAULT_VERIFY=PASS
plaintext credential file created: NO
```

A normal Synology or runner-container restart reuses the encrypted vault from the persistent Docker volume and does not require GitHub Secrets again. A destructive rebuild that removes that volume requires one manual `Track A secret vault bootstrap` workflow dispatch to reseed the machine-local vault.
