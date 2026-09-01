# Codex worker cost-control hardening report

## Incident summary

The 2026-09-01 Vision P2 coordinator burst consumed a disproportionate amount of Codex quota despite the new Luna/Terra/Sol routing policy. The primary cause was not model choice by itself. Several workers were launched through direct `codex exec` instead of the bounded local bridge, so they reloaded broad bootstrap/context, lacked verified GitHub snapshot/context budgets, and could stay alive for coordination work.

Representative owner-PC telemetry is persisted in `docs/agents/evidence/OTC-20260901-codex-worker-cost-control/observed-burn.json`. Session `total_tokens` values are cumulative context telemetry with large cached-input components and must not be treated as additive billing units; rate-limit percentages and repeated-turn behavior are the authoritative symptom signals.

## Root causes

1. Direct Codex execution bypassed the bridge that already enforced worktree locking, role context budgets and verified PR metadata.
2. An Edge Transport Terra/high worker became a CI poller, issuing repeated `Start-Sleep` cycles while carrying a very large context.
3. Workers repeatedly restacked when `main` advanced, creating new heads and new workflow generations instead of letting the coordinator own one final promotion-boundary restack.
4. The same Edge Transport exact head received two Sol/medium security reviews before a material repair changed the head.
5. Provider quota pressure was treated as a reason to spill work into Spark, exhausting a separate Spark window instead of stopping at the budget boundary.

## Local bridge hardening

The owner-PC `codex-bridge/otc_codex_dispatch.py` was hardened with TDD before this repository change:

- every real dispatch requires a fresh verified GitHub snapshot bound to alias, PR and local exact head;
- execution intent is limited to `implementation|repair` for implementers and `review|security_review` for auditors;
- coordination-only intents are rejected;
- Codex runs with JSON event output so the parent can enforce hard budgets;
- auditor ceiling: 300 seconds / 20 unique tool actions;
- implementer ceiling: 900 seconds / 60 unique tool actions;
- worker is terminated on CI-wait/watch or worker-side main-rebase/pull patterns;
- exact-head audit generation is durably deduplicated;
- a same-head second opinion requires a different model and explicit `final-confidence` stage;
- direct danger-full-access is not part of the bridge command.

Fresh local verification: `33/33 PASS`, `py_compile PASS`, CLI exposes the budget/intent/second-opinion controls.

## Repository contract hardening

Prompt contract 1.2.0 makes bridge-first execution mandatory for the five bridge-supported Wave 1 aliases when the authorized owner-PC bridge is available. A coordinator may not choose direct `codex exec` merely for convenience, and a bridge failure must be persisted before any bounded fallback.

The coordinator keeps all CI polling, status synthesis, PR metadata inspection, checkpoint-only work and final restack outside Codex. A worker that reaches external CI as its only next action exits immediately. Moving `main` does not cause an implementation worker to rebase repeatedly; the coordinator performs at most the necessary final restack at the promotion boundary and then validates that exact head.

Security re-review is generation-based. Repaired code on a new exact head may receive a fresh review. The unchanged same head cannot receive the same model/effort/prompt generation twice. A different-model second opinion on that same head is reserved for an explicit final-confidence gate, not every repair cycle.

Quota exhaustion is a real execution stop or route barrier. It is not evidence that another owner-funded provider/model should be consumed. In particular, Spark is not a quota spillover path; its use still needs an independently valid authorization and routing reason.

## Expected outcome

A normal coordinator invocation remains autonomous, but costly reasoning is spent only on implementation, repair or falsification. Coordination stays in Chat/GitHub/local deterministic tooling, worker contexts remain bounded, external waits release the worker, and repeated audit/restack generations require a material reason.
