---
task_id: OTC-20260827-current-game-login-authinfo-writer-provenance
status: validating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: validate
branch: research/OTC-20260827-current-game-login-authinfo-writer-provenance
related_pr: 729
base_branch: main
base_main: 96d1fadac4c25c2d2ceb679cb21722f46f7688b6
created: 2026-08-27T21:05:00+02:00
risk: high
execution_class: github_hosted
runtime_access: none
physical_e2e_required: false
promotion_authority: coordinator_only
implementation_authorized: false
owned_paths:
  - .github/workflows/tibia-official-client-re-gameserver-tcp-writer-provenance.yml
  - tools/tibia_re_login_authinfo_writer_provenance/
  - docs/agents/tasks/active/OTC-20260827-current-game-login-authinfo-writer-provenance.md
modules_touched: []
reuses:
  - PR #706 current game-login wire-writer promotion
  - PR #719 current typed game-login schema promotion
  - PR #724 current AuthInfo-to-wire structural provenance
  - PR #589 historical native auth/session provenance
---
# Objective

Resolve the final current-build write-provenance gap between retained native auth/session state and the already-proven `TAuthenticationAndEncryptionInfo -> GameclientMessageLogin/LoginRSAEncryptedBlock` destinations.

Do not remap Qt/QMeta globally. Reuse source-only probes from superseded PR #722 and narrow them to the current AuthInfo population function/caller chain. Preserve every unsupported user-facing field name and password/session mapping as `UNKNOWN`.

# Exact client fence

```text
version          15.32.75d4a0
packed sha256    075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
unpacked sha256  d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
unpacked size    52105824
```

# Acceptance

1. Re-derive AuthInfo and login-producer identities on the exact build.
2. Re-derive the AuthInfo population FDE and all direct callers without trusting old absolute addresses.
3. Trace population inputs backward to identifiable current native source types/QMeta payloads where exact evidence exists.
4. Emit only structural categories/edges, never secret values or proprietary client bytes.
5. If required Track B values cannot be mapped causally, fail closed and leave them `UNKNOWN`.
6. No Track B mutation or secret-bearing E2E occurs in this source research task.

next_action: consume the exact-head GitHub-hosted sanitized deep/owner/trace artifact from PR #729 and decide whether the causal source mapping is sufficient for Track B.
