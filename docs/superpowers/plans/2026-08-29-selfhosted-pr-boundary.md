# Track A self-hosted PR boundary repair v2

1. Preserve the original causal RED and reproduce the fresh review findings against the carried-forward #788 implementation.
2. Fix mixed-event predicate analysis and require `refs/heads/main` before the canonical workflow-dispatch physical job can be scheduled.
3. Make the repository checker defense in depth only; define the offline-by-default fresh one-job runner as the separate primary secret boundary.
4. Run focused tests, repo-wide boundary scan, exact-head hosted CI, and fresh independent code/security review; restack if main moves.
5. Squash-merge the successor and close #788 as superseded.
6. In a separate trusted-main field6 admission repair, reject `GITHUB_RUN_ATTEMPT != 1`, then create the clean one-job runner and execute at most one V4 login submit.
