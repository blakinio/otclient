from pathlib import Path


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit(f"{label}: expected one anchor, found {text.count(old)}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


program = Path("oteryn-client/docs/agents/playability/PROGRAM_CHARTER.md")
replace_once(
    program,
    "Current state: materially completed as a bounded synthetic foundation, with real deployment still unproven and focused LOW residual `OTC2-POST-001` remaining after the independent closure audit.",
    "Current state: materially completed as a bounded synthetic foundation, with real deployment still unproven. The independent closure audit residual `OTC2-POST-001` was closed by implementation PR #136 and lifecycle archive PR #137.",
    "program M0 status",
)
replace_once(
    program,
    "- the active secret flow is materially corrected and all release-required public secret-owner seams, including `OTC2-POST-001`, are closed before credential-bearing M1 validation.",
    "- the active secret flow and all audited release-required public secret-owner seams are closed within the documented best-effort project-owned-memory boundary.",
    "program M0 secret requirement",
)
replace_once(
    program,
    "M0 does not mean gameplay is visible or playable. Docs-only P0 discovery may proceed after lifecycle gates; M1 credential-bearing runtime validation may not claim complete secret-lifecycle closure while `OTC2-POST-001` remains.",
    "M0 does not mean gameplay is visible or playable. Docs-only P0 discovery may proceed after lifecycle gates. M1 remains gated by controlled staging, deployment and real credential-bearing runtime evidence rather than by an unresolved package-local secret-owner finding.",
    "program M0 boundary",
)
replace_once(
    program,
    "- `OTC2-POST-001` is closed and independently validated;",
    "- merged secret-owner completion PR #136 and archive PR #137 remain present on the exact validated base;",
    "program M1 prerequisite",
)

matrix = Path("oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md")
replace_once(
    matrix,
    "Status cut: `main@958881038ca5a5bc2f25a878a898ab5446d5e5c4` after independent post-remediation audit PR #133.  \nAudit status: `VALIDATED_WITH_ONE_RESIDUAL`; `OTC2-AUD-002/003/004` are closed and `OTC2-AUD-001` is partially closed by focused LOW `OTC2-POST-001`.  ",
    "Status cut: `main@02c7ac4b1d5bf1d37c20694bad45e830e430e822` after secret-owner completion archive PR #137.  \nRemediation status: independent audit PR #133 identified LOW `OTC2-POST-001`; implementation PR #136 and archive PR #137 closed it. `OTC2-AUD-001` through `OTC2-AUD-004` are closed within their documented boundaries.  ",
    "matrix status cut",
)
replace_once(
    matrix,
    "| Project-owned secret lifetime invariant | PARTIAL | active flow materially corrected; public mutable callback target and rejected oversized direct credential input remain as LOW `OTC2-POST-001` | one focused standard-library-only follow-up before credential-bearing M1 validation | M1 |",
    "| Project-owned secret lifetime invariant | PROVEN | callback target is externally immutable after bounded construction; rejected oversized direct credentials are cleared; claims remain limited to best-effort overwrite of project-owned initialized bytes | preserve in Identity/Platform/session changes; browser, HTTP/TLS, allocator and OS copies remain external boundaries | M1 |",
    "matrix secret invariant row",
)
replace_once(
    matrix,
    "| OAuth Authorization Code + PKCE | SYNTHETIC_ONLY | fake browser/listener/HTTP security E2E | controlled deployment validation after `OTC2-POST-001` | M1 |",
    "| OAuth Authorization Code + PKCE | SYNTHETIC_ONLY | fake browser/listener/HTTP security E2E; package-local secret-owner residual is closed | controlled deployment validation | M1 |",
    "matrix OAuth row",
)
replace_once(
    matrix,
    "| One-shot game-entry credential | PARTIAL | normal internal path is bounded/non-clone/redacted; direct oversized public constructor input is the LOW residual | focused `OTC2-POST-001` cleanup then reuse | M1 |",
    "| One-shot game-entry credential | PROVEN | bounded, non-cloneable, redacted one-shot owner; direct oversized input is cleared before rejection | preserve lifecycle contract; real Canary acceptance remains a separate staging claim | M1 |",
    "matrix credential row",
)
replace_once(
    matrix,
    "`OTC2-POST-001` does not block docs-only P0 discovery, but must be closed before credential-bearing M1 runtime validation or any broader secret-lifecycle completion claim.",
    "The package-local secret-owner follow-up is merged and archived. P0 launch now depends only on the programme lifecycle gates and fresh coordinator ownership preflight; M1 still requires controlled real staging evidence.",
    "matrix P0 note",
)

wave = Path("oteryn-client/docs/agents/playability/WAVE_P0_DISCOVERY.md")
replace_once(
    wave,
    "1. post-remediation closure audit PR #133 and its separate lifecycle archive are merged;",
    "1. post-remediation audit PR #133, audit archive PR #134, secret-owner completion PR #136 and archive PR #137 are merged;",
    "P0 launch gate",
)

task = Path("docs/agents/tasks/active/OTC2-20260801-full-playability-program-plan.md")
replace_once(
    task,
    "updated: 2026-08-01T15:38:00+02:00\nlast_verified_commit: \"67a6c9d726f7e70977803b028270475570210db0\"\nrequired_base_commit: \"67a6c9d726f7e70977803b028270475570210db0\"\nrisk: high\nrelated_pr: null",
    "updated: 2026-08-01T16:42:00+02:00\nlast_verified_commit: \"02c7ac4b1d5bf1d37c20694bad45e830e430e822\"\nrequired_base_commit: \"02c7ac4b1d5bf1d37c20694bad45e830e430e822\"\nrisk: high\nrelated_pr: 135",
    "task metadata",
)
replace_once(
    task,
    "  - closure audit task OTC2-20260801-post-remediation-closure-audit before worker launch",
    "  - closure audit PR #133 merge 958881038ca5a5bc2f25a878a898ab5446d5e5c4\n  - closure audit archive PR #134 merge 7596a792fbf747609a65e9fc35678b800b2d56e2\n  - secret-owner completion PR #136 merge 78567eaefb1f6a827ffa1bff3be6d4aa370ba858\n  - secret-owner archive PR #137 merge 02c7ac4b1d5bf1d37c20694bad45e830e430e822",
    "task dependencies",
)
replace_once(
    task,
    "The programme documents may be reviewed while PR #133 performs the independent post-remediation closure audit. No P0 worker may start until:",
    "The post-remediation audit, its archive and the audited secret-owner follow-up are merged. No P0 worker may start until:",
    "task launch introduction",
)
replace_once(
    task,
    "1. the closure audit and its lifecycle archive are merged;",
    "1. audit PR #133, audit archive PR #134, secret-owner PR #136 and archive PR #137 remain merged on the exact base;",
    "task launch first gate",
)
replace_once(
    task,
    "# Context checkpoint",
    "## Context checkpoint",
    "task checkpoint heading",
)
