# OTC-VISION-P2 coordinator-managed Codex dispatch — prompt update report

## Requested behavior

A newly started `OTC-VISION-P2-COORDINATOR` must act as the supervising coordinator. For ordinary repository execution and audit work it should itself choose and invoke subordinate Codex workers when an execution bridge/tool is available. The repository owner should not need to manually choose Luna/Terra/Sol, effort, or open one worker chat per lane.

## Baseline problem

The prompt family already made the coordinator the sole promotion/integration authority, but two surfaces still encoded the older owner-operated workflow:

- the alias registry told the owner to open separate worker windows after coordinator dispatch;
- coordinator mode tables said Codex was used only for integration edits.

That wording conflicts with the current prompting v2.1 short-invocation contract and the merged empirical Codex routing calibration.

## Candidate behavior

The candidate keeps Chat/GitHub as the supervising coordination plane while making Codex a subordinate execution/audit plane. The coordinator performs live anti-duplication and ownership checks, chooses the smallest sufficient model/effort, supplies bounded verified context when supported, supervises worker execution, and independently verifies results before promotion.

Manual worker windows remain a fallback only when the execution bridge is unavailable or the owner explicitly requests manual worker operation.
## Static regression result

The candidate is prompt contract `1.1.0`. Deterministic readback confirmed:

- exactly eight aliases remain registered;
- `OTC-VISION-P2-COORDINATOR` is still the sole promotion/integration authority;
- coordinator-managed Codex execution is primary when tooling is available;
- manual worker windows are explicitly fallback-only;
- live anti-duplication/dirty-worktree checks precede dispatch;
- worker model/effort selection defers to `EXECUTION_PROTOCOL.md` and its empirical calibration;
- a Codex Sol worker is explicitly subordinate and does not inherit coordinator authority;
- verified GitHub snapshot/context-budget use is requested when the bridge supports it;
- worker `DONE`/green narrative requires independent coordinator outcome verification;
- Phase 2 runtime/input/credential/mutation prohibitions remain unchanged.

New static scenarios P2-E27 through P2-E30 cover coordinator-owned worker invocation, duplicate-worker refusal, independent verification of worker completion, and high-confidence Sol/medium + independent Luna/medium safety review before expensive xhigh escalation.

Validation command `verify_coord_prompt_v11.py` returned `COORDINATOR_CODEX_DISPATCH_STATIC_PASS=true`, `ALIASES=8`, `PROMPT_CONTRACT=1.1.0`, and `MANUAL_WORKER_WINDOWS=FALLBACK_ONLY`.
