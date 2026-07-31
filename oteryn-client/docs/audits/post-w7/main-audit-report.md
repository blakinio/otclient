# Audyt klienta Oteryn w Rust po W1-W7

Task: `OTC2-20260731-rust-client-post-w7-audit`  
Evidence cut: `main@227958e3fb33a3cf1a18b0b6da011290c2877cd2`  
Zakres: `oteryn-client/**`  
Zmiany implementacji: **brak**  
Niezależna walidacja: **VALIDATED_WITH_CORRECTIONS**

## 1. Executive summary

Repozytorium zawiera spójny workspace Rust z 19 członkami. Zaimplementowano fundamenty typów i lifecycle, diagnostykę i test support, Windows application shell, deterministyczną własność powierzchni renderera, syntetyczny format/kompilator assetów, kontrakty wejścia W7, natywne granice Identity/Gateway, ograniczony transport i parsery protokołu, produkcyjny adapter Canary działający fail-closed oraz syntetyczne złożenie technical-login.

Exact W7 CI potwierdza locked metadata, formatowanie, strict Clippy, 139 zwykłych testów, bieżący architecture checker i cargo-deny. PR #119 zmienił wyłącznie dokumentację governance/tasku, dlatego bieżące manifesty, lockfile i implementacja odpowiadają przetestowanemu stanowi W7.

Nie znaleziono `CRITICAL` ani `HIGH`. Niezależna walidacja ponownie potwierdziła wszystkie cztery `MEDIUM` oraz oba reprezentatywne `LOW`. Próba obalenia wniosku readiness nie powiodła się: syntetyczny slice jest gotowy tylko w zadeklarowanym, ograniczonym zakresie, natomiast real technical login, minimum playable slice i production release pozostają niegotowe.

Korekty walidatora dotyczą wyłącznie dokumentacji audytu i checkpointu: ustanowienia kanonicznego pliku `main-audit-report.md`, aktualizacji live listy PR-ów oraz zastąpienia nieaktualnego headu gałęzi dokładnym headem wejściowym walidacji.

## 2. Exact evidence cut i validator state

- exact `main`: `227958e3fb33a3cf1a18b0b6da011290c2877cd2`;
- W7 feature merge / PR #118: `946063cd9c19ae1ae17726649bb4a0b9f21e6e32`;
- W7 archive merge / PR #119: `227958e3fb33a3cf1a18b0b6da011290c2877cd2`;
- tested PR Actions merge ref: `38b656add027f8aa21bdc5bde51424347137256c`;
- audit branch input head zweryfikowany przez walidatora: `7c74c8b1801296a4f4788f0d69cb27c353476fe4`;
- live open PRs podczas walidacji: #120, #97, #48 i #23;
- #120 dotyka wyłącznie dozwolonych dokumentów audytu/checkpointu;
- #97, #48 i #23 nie zmieniają `oteryn-client/**`;
- wszystkie cztery otwarte PR-y miały zero nierozwiązanych review threads;
- nie wykryto nakładającego się aktywnego Rust-client ownership/lease.

PR #119 zmienił wyłącznie:

- `docs/agents/MODULE_CATALOG.md`;
- `docs/agents/tasks/active/OTC2-20260731-w7-login-e2e.md`;
- `docs/agents/tasks/archive/OTC2-20260731-w7-login-e2e.md`.

Nie zmienił implementation, manifests, lockfile ani workflows. Blob identity pomiędzy tested merge ref i bieżącym `main`:

- `oteryn-client/Cargo.toml`: `3014a23b30766d4b5e63809f7339486315590913`;
- `oteryn-client/Cargo.lock`: `0f2e91094260c9ea5990d2d8713be1a680de062f`;
- `oteryn-client/apps/client/src/technical_login.rs`: `42bc41c6939876bc204a78d3a31875974914dce7`.

Lokalny checkout/Cargo pozostawał niedostępny dla sesji głównego audytu. Walidator nie zamienia repository CI PASS w local PASS.

## 3. Audited scope i exclusions

Sprawdzono live GitHub/task/PR state, dokumenty agentów i architektury, evidence W1-W7, wszystkie workspace manifests, reprezentatywne źródła i testy każdego obszaru, lockfile/policy/workflow, logi exact W7 CI, lifecycle/concurrency/security oraz claims-versus-evidence.

Nie zostały udowodnione: deployed Identity/Gateway/Canary, prawdziwe konta i credentials, prywatne capture'y, interactive Windows, real GPU/driver/hardware, produkcyjne assety i podpisy, legal approval, fuzz/soak/performance oraz gameplay.

## 4. Workspace inventory i direct dependency graph

Workspace ma dokładnie 19 członków:

| Członek | Bezpośrednie zależności lokalne |
|---|---|
| `apps/client` | diagnostics, foundation; Windows: account-session, app-runtime, game-session, identity, platform, protocol-canary, renderer, transport, world-directory; dev: test-support |
| `crates/account-session` | brak |
| `crates/app-runtime` | account-session, foundation, game-session, world-directory |
| `crates/asset-types` | brak lokalnych |
| `crates/diagnostics` | foundation |
| `crates/foundation` | brak |
| `crates/game-session` | account-session, foundation, world-directory |
| `crates/identity` | account-session, foundation, game-session, platform, world-directory |
| `crates/platform` | account-session, foundation, game-session, world-directory |
| `crates/protocol-canary` | foundation, game-session, protocol-core, transport, world-directory; dev: account-session |
| `crates/protocol-core` | brak |
| `crates/renderer` | foundation |
| `crates/test-support` | diagnostics, foundation |
| `crates/transport` | foundation |
| `crates/world-directory` | account-session |
| `tests/integration/technical-login` | account-session, app-runtime, foundation, game-session, identity, platform, protocol-canary, transport, world-directory |
| `tests/security/auth` | account-session, foundation, identity, platform, world-directory |
| `tools/architecture-check` | brak lokalnych |
| `tools/asset-compiler` | asset-types |

Bezpośredni przegląd potwierdza brak manifest dependency na legacy `src/**`, `modules/**` lub `mods/**`. Bieżący graf jest zgodny z deklarowanym kierunkiem. Zielony architecture-check nie dowodzi jednak kompletnej polityki krawędzi z powodu `OTC2-AUD-004`.

## 5. Dependency and supply-chain assessment

Wersje i feature flags są dokładne, m.in. Rust `1.94`, `winit 0.30.13`, `wgpu 30.0.0` (`default-features=false`, `std`, `dx12`), `ureq 3.3.0` z native TLS bez defaults, `serde 1.0.229`, `serde_json 1.0.145`, `time 0.3.54`, `url 2.5.8`, `sha2 0.11.0`, `base64 0.22.1`, `getrandom 0.3.4` i `pollster 1.0.1`.

Exact Supply Chain job `91213890169` zbudował cargo-deny `0.20.2` i zakończył wynikiem `advisories ok, bans ok, licenses ok, sources ok`. Audyt ani walidacja nie zmieniały manifestów, lockfile, workflow lub wyjątków.

## 6. Security and lifecycle assessment

Potwierdzone zabezpieczenia obejmują CSPRNG dla state/verifier, PKCE S256, bind callbacku przed browser launch, dynamiczny IPv4 loopback, walidację path/peer/state/generation/stale/duplicate/timeout/cancellation, HTTPS poza loopback, wyłączone redirects/proxy/retries, ograniczenia parserów i ramek, one-shot credential ownership, redacted formatting, partial-I/O handling, terminalny transport state, produkcyjny Canary fail-closed przed network/credential handoff oraz workspace `unsafe_code = forbid`.

Materialne ograniczenia opisują findings 001-004.

## 7. Test/CI/tool coverage

Exact Rust Client run `30647931191`:

- Windows job `91213890051`: PASS;
- Supply Chain job `91213890169`: PASS;
- checkout: `38b656add027f8aa21bdc5bde51424347137256c`;
- toolchain: Rust/Cargo `1.94.0`;
- `cargo metadata --locked --format-version 1`: PASS;
- `cargo fmt --all --check`: PASS;
- `cargo clippy --workspace --all-targets --locked -- -D warnings`: PASS;
- `cargo test --workspace --all-targets --locked`: PASS, 139 zwykłych testów;
- `cargo run --locked -p oteryn-architecture-check -- workspace .`: PASS;
- cargo-deny advisories/bans/licenses/sources: PASS;
- brak osobnego `cargo test --workspace --doc --locked` oraz brak `Doc-tests` w logu.

Suma 139 została odtworzona z wyników poszczególnych binaries/test targets, a nie przyjęta wyłącznie z raportu.

## 8. Claims-versus-evidence matrix

| Claim | Status | Ocena po walidacji |
|---|---|---|
| workspace/tooling readiness | PROVEN | READY do dalszej ograniczonej pracy |
| architecture compliance bieżącego grafu | DERIVED | graf zgodny; gate niekompletny |
| security foundation | DERIVED | częściowa; findings 001/002 |
| synthetic technical-login readiness | PROVEN | READY jako syntetyczny slice |
| real Canary wire compatibility | UNKNOWN | produkcyjny adapter fail-closed przed I/O |
| deployed Identity/Gateway compatibility | UNKNOWN | brak deployed evidence |
| interactive Windows runtime | UNKNOWN | tylko hosted compile/test |
| GPU/driver compatibility | UNKNOWN | brak real presentation/hardware |
| production asset pipeline | UNKNOWN | wyłącznie syntetyczny format/compiler |
| legal provenance | UNKNOWN | brak production approval |
| performance | UNKNOWN | brak budżetów i benchmarków |
| minimum playable slice | PROVEN | nie istnieje |
| production readiness | DERIVED | NOT READY |

## 9. Findings

### OTC2-AUD-001

ID: OTC2-AUD-001  
TITLE: Deklaracja pełnego terminal cleanup sekretów przekracza rzeczywistą implementację  
STATUS: CONFLICT  
SEVERITY: MEDIUM  
CONFIDENCE: HIGH  
AFFECTED_PATHS: `crates/identity/src/lib.rs`; `crates/platform/src/lib.rs`; `crates/game-session/src/lib.rs`; `W7_IDENTITY_EVIDENCE.md`; `MODULE_CATALOG.md`  
EVIDENCE: authorization URL, callback target, state/code i verifier copies są zwykłymi `String`/`Url`; platform transport buduje zwykły `String` przez `format!("Bearer {bearer}")`; dokumentacja formułuje szerszy terminal-cleanup claim.  
IMPACT: kopie sekretów mogą pozostać w pamięci alokatora mimo poprawnej redakcji formatowania i zeroizacji wybranych kontenerów.  
RECOMMENDATION: utrzymywać sekrety w zeroizing containers przez parsing/request/error paths, usunąć formatted bearer copy albo zawęzić claim.  
REMEDIATION_PERFORMED: NO  
VALIDATOR: CONFIRMED

### OTC2-AUD-002

ID: OTC2-AUD-002  
TITLE: Zamknięcie okna może blokować główny wątek event loop podczas synchronicznego join  
STATUS: DERIVED  
SEVERITY: MEDIUM  
CONFIDENCE: HIGH  
AFFECTED_PATHS: `apps/client/src/main.rs`; `crates/app-runtime/src/runtime.rs`; `crates/identity/src/lib.rs`; `crates/platform/src/lib.rs`; `apps/client/src/technical_login.rs`; `crates/transport/src/lib.rs`  
EVIDENCE: close/destroy wywołuje shutdown na event-loop thread; shutdown anuluje i wykonuje blokujący `JoinHandle::join`; cancellation nie przerywa trwającego synchronous HTTP send; konfiguracja transportu wymaga timeoutów niezerowych, lecz nie narzuca twardej górnej granicy.  
IMPACT: close/fatal path może przestać odpowiadać do zakończenia I/O.  
RECOMMENDATION: nonblocking shutdown state machine, join tylko finished workers i hard timeout caps.  
REMEDIATION_PERFORMED: NO  
VALIDATOR: CONFIRMED

### OTC2-AUD-003

ID: OTC2-AUD-003  
TITLE: Asset compiler ma wyścig TOCTOU między walidacją ścieżki a otwarciem pliku  
STATUS: DERIVED  
SEVERITY: MEDIUM  
CONFIDENCE: HIGH  
AFFECTED_PATHS: `tools/asset-compiler/src/lib.rs:285-330` i testy symlink  
EVIDENCE: `symlink_metadata`, `canonicalize` i metadata checks poprzedzają osobne późniejsze `File::open`; brak handle-relative no-follow open lub finalnej weryfikacji identity otwartego handle.  
IMPACT: w współdzielonym albo atakowalnym source tree sprawdzona ścieżka może zostać podmieniona przed open.  
RECOMMENDATION: trusted directory handle + no-follow/reparse protection i final identity check albo jawny exclusive-trusted-source precondition.  
REMEDIATION_PERFORMED: NO  
VALIDATOR: CONFIRMED

### OTC2-AUD-004

ID: OTC2-AUD-004  
TITLE: Architecture gate implementuje częściowy denylist zamiast kompletnej polityki krawędzi  
STATUS: PROVEN  
SEVERITY: MEDIUM  
CONFIDENCE: HIGH  
AFFECTED_PATHS: `tools/architecture-check/src/lib.rs`; `tests/architecture-fixtures/**`; `docs/architecture/ARCHITECTURE.md`; `MODULE_CATALOG.md`  
EVIDENCE: `forbidden_edge` wymienia wybrane pary; niewymieniona krawędź, np. `transport -> renderer`, przejdzie, jeśli nie naruszy innej reguły lub cyklu, mimo sprzeczności z normatywnym rozdziałem warstw. Bieżący graf takiej krawędzi nie zawiera.  
IMPACT: zielony architecture-check nie dowodzi pełnej normatywnej zgodności.  
RECOMMENDATION: explicit allow-edge matrix/layer order i exhaustive fixtures dla katalogu kategorii.  
REMEDIATION_PERFORMED: NO  
VALIDATOR: CONFIRMED

### OTC2-AUD-005

ID: OTC2-AUD-005  
TITLE: Live GitHub, governance index i część evidence files opisują różne stany  
STATUS: CONFLICT  
SEVERITY: LOW  
CONFIDENCE: HIGH  
AFFECTED_PATHS: `docs/agents/ACTIVE_WORK.md`; `docs/agents/MODULE_CATALOG.md`; W7 entry i Canary evidence  
EVIDENCE: `ACTIVE_WORK` nadal wymienia #4/#3, live state podczas walidacji to #120/#97/#48/#23; module catalog nadal opisuje #4 jako active; W7 entry/Canary evidence mają przedmerge'owe statusy.  
IMPACT: możliwa błędna detekcja ownership i duplikacja pracy.  
RECOMMENDATION: zsynchronizować governance i dodać automatyczny live-state check.  
REMEDIATION_PERFORMED: NO  
VALIDATOR: CONFIRMED

### OTC2-AUD-006

ID: OTC2-AUD-006  
TITLE: CI/evidence deklaruje doctesty, lecz workflow wybiera `--all-targets` bez `--doc`  
STATUS: CONFLICT  
SEVERITY: LOW  
CONFIDENCE: HIGH  
AFFECTED_PATHS: `.github/workflows/rust-client.yml`; `BUILD_TEST_MATRIX.md`; `W7_LOGIN_E2E_EVIDENCE.md`; `crates/game-session/src/lib.rs`  
EVIDENCE: workflow uruchamia `cargo test --workspace --all-targets --locked`; exact log ma 139 zwykłych testów i nie zawiera `Doc-tests`; publiczny kontrakt zawiera `compile_fail` doctest.  
IMPACT: evidence zawyża wykonane pokrycie, a compile-fail API barrier nie jest egzekwowany przez recorded CI.  
RECOMMENDATION: dodać osobny `cargo test --workspace --doc --locked` albo usunąć claim o wykonanych doctestach.  
REMEDIATION_PERFORMED: NO  
VALIDATOR: CONFIRMED

### OTC2-AUD-007

ID: OTC2-AUD-007  
TITLE: Production readiness pozostaje nieudowodniona poza syntetycznym technical-login slice  
STATUS: UNKNOWN  
SEVERITY: INFO  
CONFIDENCE: HIGH  
EVIDENCE: produkcyjny `CanaryEntryAdapter::connect` zwraca `RealAdmissionUnavailable` przed network I/O; test integracyjny potwierdza pozostawienie lifecycle w `CredentialReady`; brak deployed, interactive, real-GPU, production-assets, legal, fuzz/soak/performance i gameplay evidence.  
REMEDIATION_PERFORMED: NO  
VALIDATOR: CONFIRMED

## 10. Próba obalenia wniosku readiness

Walidator szukał dowodu, że syntetyczny slice nie jest gotowy nawet w ograniczonym zakresie albo że real/production readiness jest większe niż raportowano.

- Nie obalono synthetic READY: exact CI kompiluje i testuje wszystkie 19 członków, trzy testy integracyjne przechodzą, fake services są jawnie syntetyczne, a production path nie jest mylony z test path.
- Nie obalono real NOT READY: `AdmissionMode::EvidenceBlocked` jest produkcyjnym trybem, `connect` zwraca `RealAdmissionUnavailable` przed I/O, a `enter_session` nie może przejąć credentialu bez implementacji admission.
- Nie znaleziono gameplay/map/runtime-assets/UI feature slice ani dowodu real-service deployment.

Wniosek audytu pozostaje prawidłowy w dokładnie zadeklarowanych granicach.

## 11. Unauthorized-change check

Na validator input head gałąź audytu była `0` commitów za `main` i `6` commitów przed `main`. Diff obejmował wyłącznie:

- `docs/agents/tasks/active/OTC2-20260731-rust-client-post-w7-audit.md`;
- `oteryn-client/docs/audits/post-w7/**`.

Walidator zmienił wyłącznie te dozwolone dokumenty. Nie zmieniono implementation, manifests, lockfile, workflows ani legacy runtime paths.

## 12. Readiness assessment

- bounded workspace development: READY;
- synthetic technical-login slice: READY;
- real technical login: NOT READY;
- minimum playable slice: ABSENT;
- production release: NOT READY.

## 13. Minimalne rekomendowane dalsze taski

1. `OTC2-RUST-LOGIN-SAFETY-HARDENING` — secret lifetime, nonblocking shutdown i hard timeout caps.
2. `OTC2-ASSET-SOURCE-HANDLE-HARDENING` — zamknięcie source-open TOCTOU.
3. `OTC2-ARCH-EVIDENCE-GATE-REPAIR` — kompletna edge policy, explicit doctest gate i synchronizacja governance.
4. `OTC2-REAL-COMPATIBILITY-DISCOVERY` — dopiero po hardeningu i przy approved exact revisions/environment/provenance.

## 14. Corrections applied by independent validator

1. Ustanowiono kanoniczny raport wymagany przez zlecenie: `oteryn-client/docs/audits/post-w7/main-audit-report.md`.
2. Zaktualizowano live state o audit PR #120, zachowując osobno pierwotny cut #97/#48/#23.
3. Zastąpiono nieaktualny checkpoint head `6ddd563e...` dokładnym validator input head `7c74c8b...`.
4. Usunięto nieaktualny blocker mówiący, że niezależna sesja walidatora nie może zostać wykonana.
5. Nie zmieniono severity, statusu ani meritum findings/readiness.

## 15. Independent validator result

`VALIDATED_WITH_CORRECTIONS`
