from pathlib import Path


path = Path("docs/agents/tasks/active/OTC2-20260801-full-playability-program-plan.md")
text = path.read_text(encoding="utf-8")
replacements = [
    (
        "updated_at: 2026-08-01T15:38:00+02:00\nhead: 67a6c9d726f7e70977803b028270475570210db0\nbranch: docs/OTC2-20260801-full-playability-program-plan\npr: none\nstatus: active\nphase: design",
        "updated_at: 2026-08-01T16:42:00+02:00\nhead: 16a3e70bc9238cda6bd2489e2469f6ed70753dc2\nbranch: docs/OTC2-20260801-full-playability-program-plan\npr: 135\nstatus: validating\nphase: validation",
        "checkpoint live state",
    ),
    (
        "  - Current main is 67a6c9d726f7e70977803b028270475570210db0.",
        "  - Current main is 02c7ac4b1d5bf1d37c20694bad45e830e430e822.",
        "checkpoint main",
    ),
    (
        "  - PR #133 independently audits remediation closure and owns only its audit task/report paths.",
        "  - Audit PR #133, audit archive PR #134, secret-owner completion PR #136 and archive PR #137 are merged.",
        "checkpoint closure state",
    ),
    (
        "  marker: none\n  evidence: planning package not yet written",
        "  marker: resolved-stale-status\n  evidence: programme documents and prompts are written; stale audit/residual status is normalized to current main.",
        "checkpoint first failure",
    ),
    (
        "changed_paths:\n  - docs/agents/tasks/active/OTC2-20260801-full-playability-program-plan.md\nvalidation: []\nblockers:\n  - P0 worker launch waits for PR #133 and its archive plus this plan/archive.\nnext_action: Write the normative programme charter, architecture handoff, capability matrix, parallelism plan and bounded P0 prompts.",
        "changed_paths:\n  - docs/agents/tasks/active/OTC2-20260801-full-playability-program-plan.md\n  - oteryn-client/docs/agents/playability/PROGRAM_CHARTER.md\n  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md\n  - oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md\n  - oteryn-client/docs/agents/playability/DEPENDENCY_AND_PARALLELISM.md\n  - oteryn-client/docs/agents/playability/WAVE_P0_DISCOVERY.md\n  - oteryn-client/docs/agents/prompts/PLAYABILITY_COORDINATOR_AGENT.md\n  - oteryn-client/docs/agents/prompts/P0_CANARY_CAPABILITY_AGENT.md\n  - oteryn-client/docs/agents/prompts/P0_LEGACY_PARITY_AGENT.md\n  - oteryn-client/docs/agents/prompts/P0_ASSET_PIPELINE_AGENT.md\n  - oteryn-client/docs/agents/prompts/P0_UX_INPUT_AUDIO_AGENT.md\n  - oteryn-client/docs/agents/prompts/P0_RELEASE_E2E_AGENT.md\nvalidation:\n  - command: programme document and Prompting Standard review\n    result: PASS\n    evidence: twelve declared documentation paths; implementation remains unauthorized and each worker prompt contains required bounded sections.\nblockers:\n  - P0 worker launch waits for this planning PR and its separate lifecycle archive.\nnext_action: Validate, review and merge PR #135, archive the plan, then run a fresh P0 coordinator launch preflight.",
        "checkpoint final state",
    ),
]
for old, new, label in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one anchor, found {count}")
    text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
