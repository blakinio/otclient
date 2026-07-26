# Rust Client Task Extension

Use the repository root task template first. Add the following fields to the task front matter/body for work under `oteryn-client/`.

```yaml
track: greenfield-rust
workstream: WS-RXX
crates_touched: []
features_touched: []
contracts_touched: []
architecture_documents: []
performance_evidence: []
security_evidence: []
legacy_evidence_used: []
```

## Required questions

- Which audit finding or accepted gate authorizes this task?
- Which stable architecture boundary owns the behavior?
- Does the task change `GameEvent`, `GameCommand`, typed IDs, render snapshots, asset schemas, UI registries or extension APIs?
- Which other active tasks own adjacent contracts or paths?
- Does any fact require exact Canary/Oteryn producer evidence?
- Are all fixtures synthetic, sanitized and legally distributable?
- What is the smallest observable implementation/result?
- Which performance/security/lifecycle gates apply?
- What is explicitly out of scope?

## Validation record

Record exact commit SHA, command/workflow, result and evidence. Do not write `passed`, `compatible`, `faster` or `secure` without exact proof.

## Handoff

Leave:

- one concrete next action;
- exact first file/symbol/test to open;
- current blocker or first failure;
- decisions not to repeat;
- runtime/server/platform claims that remain unproven.
