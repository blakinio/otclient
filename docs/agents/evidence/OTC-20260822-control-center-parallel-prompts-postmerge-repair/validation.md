# Pre-PR validation

Candidate branch starts from merged `main@9c54c1a4e22db974109298a23be39d9b04305e76`.

Local validation:
- `git diff --check origin/main...HEAD`: PASS before evidence-only follow-up commits.
- behavioral repair: six one-line prompt/alias completion-policy substitutions.
- no source/runtime/workflow/module changes.

Repository CI, Track A governance and fresh independent exact-head audit are mandatory before merge.
