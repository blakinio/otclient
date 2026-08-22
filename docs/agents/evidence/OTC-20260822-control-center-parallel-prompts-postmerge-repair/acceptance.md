# Acceptance matrix

| Check | Expected | Result |
|---|---|---|
| Standard enum | completion policy is declared by Prompting Standard 2.1 | PASS |
| B routing | single task + stop at task boundary | PASS |
| C routing | single task + stop at task boundary | PASS |
| D-prep routing | single task + stop at task boundary | PASS |
| Archive semantics | supported finalize/archive policy retained | PASS |
| Runtime authority | none | PASS |
| Official-client mutation | impossible from these aliases | PASS |
| Package C semantic fence | candidate/pending-causal values remain unpromoted | PASS |

Exact-head CI and independent review remain required after publication.
