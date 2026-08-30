# OTCLIENT-TIBIA-GLOBAL-LOGIN final continuation alias

```yaml
alias_prompt_contract_version: 1.1.0
alias: OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
repository: blakinio/otclient
entry_task: OTC-20260828-current-login-field6-runtime
canonical_prompt: docs/agents/prompts/OTCLIENT_TIBIA_GLOBAL_LOGIN_FINAL_CONTINUE.md
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
codex_spark_allowed: true
```

## Owner invocation

```text
Kontynuuj autonomicznie OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
```

## Resolution

Resolve the canonical prompt above from **fresh trusted main/live branch state**. Do not use the old Track-B-first interpretation.

The current dependency order is:

```text
Track A official-launcher seed repair
→ trusted-main V5 field6 observation
→ sanitized field6 promotion
→ Track B PR #284 reconstruction/E2E
→ final closeout
```

At the 2026-08-30 checkpoint V4 was terminal pre-login and `FIELD6_VALUE=UNKNOWN`, `physical_action_count=0`. Never rerun V4 or reuse trigger comment `5467500633`.
Repair branch checkpoint:
`fix/OTC-20260830-field6-official-launcher-seed`

Causal RED:
`FIELD6_SEED_RED: materialize_seed missing`

Sanitized checkpoint evidence:
`docs/agents/evidence/OTC-20260828-current-login-field6-runtime/20260830-v4-preauth-failure-official-launcher-seed.md`

Local proprietary seed remains only on Molehill-PC and must never be committed:
`C:\OTClientV4\tibia-15.32.75d4a0-official-launcher-seed.tar.gz`
SHA256 `64031ba091884c5b1be71416394b8ada6dac9529cfed60e7b4856c04b7e5b016`.

The canonical prompt contains the full safety, TDD, V5, Track B, Vision and closeout contract. Live GitHub state always overrides checkpoint SHA values.