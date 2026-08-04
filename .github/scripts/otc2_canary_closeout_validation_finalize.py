from __future__ import annotations

import re
from pathlib import Path

UPDATED = "2026-08-04T08:53:00+02:00"
VALIDATED_HEAD = "9d82234af1c23c2748984f613e8eab2fa89396da"
RUST_RUN = 30885320351
CI_RUN = 30885320455
TASK = Path("docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md")
EVIDENCE = Path("oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md")

task = TASK.read_text(encoding="utf-8")
task = re.sub(r'^updated: .*$', f'updated: {UPDATED}', task, count=1, flags=re.MULTILINE)
task = re.sub(r'^last_progress_at: .*$', f'last_progress_at: {UPDATED}', task, count=1, flags=re.MULTILINE)
task = re.sub(
    r'^ci_check_generation: .*$',
    'ci_check_generation: entity-reconciliation-closeout-restack-exact-head',
    task,
    count=1,
    flags=re.MULTILINE,
)
task = re.sub(
    r'^terminal_ci_checks_for_current_generation: \d+$',
    'terminal_ci_checks_for_current_generation: 5',
    task,
    count=1,
    flags=re.MULTILINE,
)

insert_after = """  ready_state:
    repository_ci_run: 30883947811
    repository_required_job: 91911322995
    result: PASS
"""
closeout_validation = f"""  closeout_restack_head:
    sha: {VALIDATED_HEAD}
    rust_client_run: {RUST_RUN}
    repository_ci_run: {CI_RUN}
    result: PASS
"""
if closeout_validation not in task:
    if insert_after not in task:
        raise RuntimeError("validation insertion anchor not found")
    task = task.replace(insert_after, insert_after + closeout_validation, 1)

task = task.replace(
    "  exact_head: 52942db86c6172974b4e5e80009c662f51ebb058",
    f"  exact_head: {VALIDATED_HEAD}",
    1,
)
task = re.sub(
    r"  external_run_ids:\n(?:    - \d+\n)+",
    f"  external_run_ids:\n    - {RUST_RUN}\n    - {CI_RUN}\n",
    task,
    count=1,
)
task = task.replace("  checks_used: 0", "  checks_used: 5", 1)
task = task.replace(
    "  active_operation: protected closeout restack, exact-head CI and merge reconciliation",
    "  active_operation: protected closeout merge reconciliation",
    1,
)
task = task.replace(
    "  check_generation: closeout-restack-current-main",
    "  check_generation: closeout-restack-validation-record",
    1,
)
task = task.replace(
    "  resume_condition: Reconcile PR 254 against current main; merge only after its exact-head required checks pass, otherwise preserve the precise failure.",
    "  resume_condition: Reconcile the final validation-record head of PR 254; merge only after its exact-head required checks pass, otherwise preserve the precise failure.",
    1,
)
TASK.write_text(task, encoding="utf-8", newline="\n")

evidence = EVIDENCE.read_text(encoding="utf-8")
evidence = evidence.replace(
    "final_closeout_exact_head_ci: pending",
    f"final_closeout_exact_head_ci:\n  head: {VALIDATED_HEAD}\n  rust_client_run: {RUST_RUN}\n  repository_ci_run: {CI_RUN}\n  result: PASS",
    1,
)
EVIDENCE.write_text(evidence, encoding="utf-8", newline="\n")
