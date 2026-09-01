# Codex coordinator simplification

## Objective

Simplify the Vision P2 coordinator prompt after the measured quota-burn hardening without weakening the technical bridge guards.

## Result

Prompt contract `1.3.0` reduces the coordinator's normal Codex workflow to six decisions:

1. reconcile live ownership/state and select one safe task;
2. choose the smallest sufficient worker model/effort;
3. dispatch a supported alias through the bounded bridge;
4. keep GitHub/CI/PR lifecycle and final restack coordinator-side;
5. independently verify the returned worker result;
6. start another worker only for materially new evidence or a required independent validation.

The dispatcher remains responsible for verified GitHub context, sandbox/context limits, hard worker budgets, wait/main-chase termination and audit deduplication.

## Measured simplification

Compared with merged prompt `1.2.0`, the coordinator-specific execution section changed from 21 lines / 618 words to 13 lines / 238 words: a 61.5% word reduction.

The alias registry also no longer carries a fixed per-alias effort table; routing remains dynamic under `EXECUTION_PROTOCOL.md`.

## Validation

- `verify_coord_prompt_v13.py`: PASS.
- owner-PC bounded dispatcher regression: `33/33 PASS`.
- dispatcher `py_compile`: PASS.
- task checkpoint validator: PASS.
- Control Room: policy-v2 task.
- Track A runtime governance: PASS.
- `git diff --check`: PASS.
- runtime E2E: NOT_APPLICABLE; prompt/documentation-only change.
