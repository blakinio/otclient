# Branch hygiene note

During connector operation an empty technical branch `tmp-noop-should-not-exist` was created at `main@fa5b66b697d42c60515c5de48ea5e30135eadd0e` without commits or PR. It carries no task state or implementation content. The available GitHub connector surface in this session does not expose branch-ref deletion, so it is explicitly recorded as a cleanup-only ref rather than silently treated as programme work. It must never be selected as an authority or continuation branch.
