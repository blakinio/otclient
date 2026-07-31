# Independent validator packet

Task: `OTC2-20260731-rust-client-post-w7-audit`  
Evidence cut: `227958e3fb33a3cf1a18b0b6da011290c2877cd2`  
Audit branch: `docs/OTC2-20260731-rust-client-post-w7-audit`  
Main report: `OTC2-20260731-rust-client-post-w7-audit.md`

## Required fresh checks

1. Ponownie sprawdź live `main`. Musi nadal wynosić `227958e3fb33a3cf1a18b0b6da011290c2877cd2`; w przeciwnym razie zwróć `REJECTED` albo wymagaj nowego evidence cut.
2. Sprawdź wszystkie otwarte PR-y, aktywne taski, leases, ownership i review threads pod kątem `oteryn-client/**`.
3. Ponownie zweryfikuj wszystkie `MEDIUM`:
   - `OTC2-AUD-001` — ordinary secret copies kontra terminal cleanup claim;
   - `OTC2-AUD-002` — blocking join na event-loop close path;
   - `OTC2-AUD-003` — asset source-open TOCTOU;
   - `OTC2-AUD-004` — niekompletny architecture edge policy.
4. Sprawdź reprezentatywną próbkę `LOW`: `OTC2-AUD-005` i `OTC2-AUD-006`.
5. Zweryfikuj Rust Client run `30647931191`, Windows job `91213890051`, Supply Chain job `91213890169`, checkout `38b656add027f8aa21bdc5bde51424347137256c`, 139 zwykłych testów i brak doc-test step.
6. Zweryfikuj kompletność 19 członków workspace'u oraz direct dependency graph.
7. Zweryfikuj, że PR #119 nie zmienił implementation/manifests/lockfile/workflows.
8. Zweryfikuj, że audit branch zawiera wyłącznie:
   - `docs/agents/tasks/active/OTC2-20260731-rust-client-post-w7-audit.md`;
   - `oteryn-client/docs/audits/post-w7/**`.
9. Spróbuj obalić wniosek: synthetic slice READY, real/production NOT READY.
10. Zapisz wynik `VALIDATED`, `VALIDATED_WITH_CORRECTIONS` albo `REJECTED`. Korekty mogą zmieniać wyłącznie raporty audytu i task checkpoint.

## Evidence map

- repository/live/CI index: `EVIDENCE_INDEX.md`;
- findings and readiness: `OTC2-20260731-rust-client-post-w7-audit.md`;
- local limitation: GitHub DNS i Cargo były niedostępne; nie zamieniaj CI PASS w local PASS.

## Validator output contract

Walidator musi zapisać:

- exact main i audit branch head;
- sprawdzone findings i korekty;
- wynik command/CI evidence verification;
- wynik unauthorized-change check;
- końcowy status walidacji;
- końcowy checkpoint tego samego tasku.
