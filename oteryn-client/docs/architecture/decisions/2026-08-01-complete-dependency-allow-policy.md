# Complete Rust dependency allow policy

Status: accepted  
Date: 2026-08-01  
Finding: `OTC2-AUD-004`  
Task: `OTC2-20260801-complete-architecture-policy`

## Context

The architecture checker already recognized a closed catalogue of 29 package categories, but its edge enforcement was a partial denylist and discarded Cargo dependency kind. Any category pair not named by the denylist was implicitly accepted, and normal, build and dev dependencies were treated identically.

The workspace requires one auditable answer for every source category, target category and Cargo dependency kind without changing the current 19 package manifests.

## Decision

1. The category catalogue remains closed at the existing 29 categories.
2. `DependencyKind` is part of every parsed edge and is one of `normal`, `build` or `dev`.
3. Normal dependencies use a source-category allowlist. An edge is rejected unless its exact target category is allowed for that source.
4. `tool` may normally depend on any known category because tools and test harnesses consume product contracts. Product categories may not normally depend on `tool`.
5. Dev dependencies use the normal allowlist plus one explicit exception: any known category may target `tool`. This permits product tests and examples to consume test-support tooling without adding a production edge.
6. Build dependencies are denied by default. The only explicit build pairs are `tool -> foundation` and `tool -> asset-types`; adding another build edge requires a policy change reviewed with the manifest change.
7. All workspace edges, regardless of dependency kind, remain part of cycle detection and path/source validation.
8. The stable violation code for a disallowed category edge remains `E005_FORBIDDEN_EDGE`; its message now includes dependency kind.
9. Synthetic fixture schema version 2 requires `dependency.kind`. Version 1 remains readable for archived fixtures and interprets an absent kind as `normal`.
10. The policy is verified exhaustively for all `29 x 29 x 3 = 2523` category/kind combinations. Each public policy decision is compared with the actual fixture parser and `E005` result.

## Consequences

- No unlisted category edge is silently accepted.
- Normal product-to-tool dependencies fail, while dev product-to-tool dependencies remain possible.
- Build-script dependencies cannot appear accidentally.
- Archived schema-v1 fixtures remain valid, while new fixtures must state dependency kind explicitly.
- The current 19-member workspace passes without manifest, lockfile or dependency changes.
- Future category or dependency-kind changes require an explicit policy and test update rather than extending a partial denylist.

## Validation

The implementation is required to pass locked metadata, rustfmt, strict Clippy, complete workspace tests including the exhaustive matrix, architecture validation against the unchanged real workspace, Supply Chain and repository `CI / Required`.
