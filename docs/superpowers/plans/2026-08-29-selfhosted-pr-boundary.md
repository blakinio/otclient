# Track A self-hosted PR boundary repair

1. Run the hosted repository-wide regression in RED and capture every PR-triggered self-hosted job lacking an explicit non-PR event gate.
2. For each RED path, keep PR validation on GitHub-hosted runners and gate the Synology job to owner-only non-PR execution with trusted-main checkout.
3. Re-run the repository-wide boundary, Track A governance, and CI to GREEN.
4. Obtain independent exact-head code/security review, restack on fresh main, squash-merge.
5. Only after this security boundary is trusted may the field6 V4 admission continue to clean-runner attestation and credential access.
