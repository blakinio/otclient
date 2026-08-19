---
task_id: OTC-20260819-track-a-secret-vault-bootstrap
status: implementing
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

Design:

- persistent encrypted CMS envelope under the self-hosted runner `/work` volume;
- RSA private key generated only on Synology and stored mode `0600`;
- repository Secrets consumed only by a bounded self-hosted seeding step with shell tracing disabled;
- plaintext credential frame exists only in process memory during sealing/use;
- later consumers decrypt directly to memory and create a sealed memfd for the existing native-auth transport;
- this task does not perform login and does not expand PR #528 runtime admission.

Acceptance:

1. runner path and OpenSSL availability verified;
2. workflow seeds vault without printing secret values;
3. dummy local round-trip validates encryption/decryption and exact credential frame format;
4. final workflow is manual `workflow_dispatch` only after initial seeding;
5. no plaintext credential file is created.
