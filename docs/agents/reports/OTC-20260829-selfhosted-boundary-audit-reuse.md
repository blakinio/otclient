# OTC-20260829 reusable self-hosted boundary audit repair

Causal production-like RED: PR #796 run `33260012616`, job `99120220924`, `AUDIT-F003` rejected legitimate future V4 admission paths solely because #795 had frozen its own historical allowlist into a reusable audit.

The repair removes that historical path restriction while preserving all current-tree security assertions. Regression coverage accepts the exact future-field6 path class and still rejects an empty diff. No self-hosted/runtime/secret action is part of this repair.

Pre-restack hosted GREEN on `8068e30c...`: boundary/audit `33260190370`, governance `33260190375`, CI `33260190479` / required job `99120784888`. Final restacked evidence must supersede this for merge.
