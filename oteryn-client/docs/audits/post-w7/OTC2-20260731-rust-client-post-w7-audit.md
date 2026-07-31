# Audyt klienta Oteryn w Rust po W1-W7

Task: `OTC2-20260731-rust-client-post-w7-audit`  
Evidence cut: `main@227958e3fb33a3cf1a18b0b6da011290c2877cd2`  
Zakres: `oteryn-client/**`  
Zmiany implementacji: **brak**  
Niezależna walidacja: **oczekuje na świeżą sesję**

## 1. Executive summary

Repozytorium zawiera spójny workspace Rust z 19 członkami. Zaimplementowano fundamenty typów i lifecycle, diagnostykę i test support, Windows application shell, deterministyczną własność powierzchni renderera, syntetyczny format/kompilator assetów, kontrakty wejścia W7, natywne granice Identity/Gateway, ograniczony transport i parsery protokołu, produkcyjny adapter Canary działający fail-closed oraz syntetyczne złożenie technical-login.

Bieżący graf manifestów zachowuje udokumentowany kierunek zależności i nie zależy runtime'owo od legacy C++/Lua. Exact W7 CI potwierdza locked metadata, formatowanie, strict Clippy, 139 zwykłych testów, obecny architecture checker i cargo-deny. PR #119 zmienił wyłącznie governance i archiwizację tasku, dlatego bieżąca implementacja i lockfile odpowiadają przetestowanemu stanowi W7.

Nie znaleziono `CRITICAL` ani `HIGH`. Pozostają cztery `MEDIUM`: niepełne end-to-end czyszczenie kopii sekretów, blokujący `join` na ścieżce zamknięcia event loop, TOCTOU w odczycie źródeł asset compilera oraz architecture checker egzekwujący tylko częściowy denylist. Dwa `LOW` dotyczą rozjazdu governance/evidence oraz deklarowanych, lecz niewykonanych doctestów.

**Wniosek readiness:** workspace jest gotowy jako ograniczony fundament i syntetyczny technical-login slice. Nie jest klientem gry i nie jest gotowy produkcyjnie.

## 2. Exact evidence cut

- exact `main`: `227958e3fb33a3cf1a18b0b6da011290c2877cd2`;
- PR #118 feature merge: `946063cd9c19ae1ae17726649bb4a0b9f21e6e32`;
- PR #119 archive merge: `227958e3fb33a3cf1a18b0b6da011290c2877cd2`;
- tested PR Actions merge ref: `38b656add027f8aa21bdc5bde51424347137256c`;
- otwarte PR-y: #97, #48, #23; brak zmian w `oteryn-client/**`;
- brak nierozwiązanych review threads i pokrywającego tasku/lease;
- PR #119 zmienił tylko `MODULE_CATALOG` i przeniósł task W7 do archiwum;
- `Cargo.toml`, `Cargo.lock` i `apps/client/src/technical_login.rs` mają identyczne blob SHA w przetestowanym merge-refie i obecnym `main`.

Lokalny checkout był niedostępny: `git ls-remote` zakończył się kodem `128` z `Could not resolve host: github.com`. Lokalnie nie było poleceń `cargo` ani `cargo-deny`. Wyniki lokalne są `NOT RUN`, a wykonanie potwierdza exact repository CI.

## 3. Audited scope i exclusions

Sprawdzono live GitHub/task/PR state, wymagane dokumenty agentów i architektury, ADR-y, foundation audit, evidence W1-W7, wszystkie workspace manifests, reprezentatywne źródła i testy każdego członka, lockfile/policy/workflow, historię finalnych PR headów, logi W7 CI, granice lifecycle/concurrency/security oraz claims-versus-evidence.

Nie były dostępne i nie są uznane za poprawne: deployed Identity/Gateway/Canary, prawdziwe konta i credentials, prywatne capture'y, interactive Windows, real GPU/driver/hardware, produkcyjne assety i podpisy, legal approval, fuzz/soak/performance oraz gameplay.

## 4. Architecture/dependency matrix

Workspace ma 19 członków. Bieżący graf wykazuje:

- `foundation` bez zależności ku górze;
- diagnostykę i test support konsumujące fundament;
- osobne kontrakty account/directory/game-session;
- `platform` kończący raw HTTP/DTO i zwracający typy właścicieli kontraktów;
- `identity` konsumujące platform i wspólne kontrakty;
- `protocol-canary` konsumujący transport/protocol-core i lifecycle właściciela;
- `app-runtime` bez raw HTTP/TCP public contracts;
- `renderer` zależny od foundation oraz Windows `wgpu`/`pollster`;
- asset compiler zależny wyłącznie od asset-types i serde_json;
- brak zależności manifestów od legacy `src/**`, `modules/**`, `mods/**`;
- brak substitute public contracts, globalnego service registry i global mutable state w przejrzanym kodzie produkcyjnym.

Obecny graf jest zgodny przez bezpośredni przegląd. Automatyczny gate nie dowodzi całej zgodności z powodu findingu `OTC2-AUD-004`.

## 5. Dependency and supply-chain assessment

Bezpośrednie wersje i features są dokładne, m.in. Rust `1.94`, `winit 0.30.13`, `wgpu 30.0.0` (`default-features=false`, `std`, `dx12`), `ureq 3.3.0` z native TLS bez defaults, `serde 1.0.229`, `serde_json 1.0.145`, `time 0.3.54`, `url 2.5.8`, `sha2 0.11.0`, `base64 0.22.1`, `getrandom 0.3.4`, `pollster 1.0.1`.

`deny.toml` odrzuca yanked packages, wildcardy, nieznane registry i Git sources oraz wielokrotne wersje poza trzema dokładnymi wyjątkami:

- `hashbrown 0.16.1`;
- `syn 3.0.3`;
- `windows-sys 0.61.2`.

Exact Supply Chain job `91213890169` użył cargo-deny `0.20.2` i zakończył powodzeniem advisories, bans, licenses i sources. GitHub Actions są przypięte commit SHA. Audyt nie zmieniał manifestów, lockfile ani wyjątków.

## 6. Security and lifecycle assessment

Potwierdzone zabezpieczenia:

- OS CSPRNG dla state/verifier i PKCE S256;
- callback bind przed browser launch, dynamiczny IPv4 loopback;
- walidacja exact path, peer, state, generation, stale, duplicate, timeout i cancellation;
- HTTPS poza loopback, native cert/hostname verification;
- redirects, environment proxy i automatic retries wyłączone;
- ograniczenia callback/header/body/parser/frame;
- one-shot, non-Clone credential ownership i redacted Debug/Display;
- partial-I/O handling i terminalny transport state;
- produkcyjny Canary fail-closed przed network/credential handoff;
- deterministyczny renderer lifecycle dla generation, zero-size, recovery i close;
- workspace `unsafe_code = forbid`.

Materialne ograniczenia opisują findings 001-004.

## 7. Test/CI/tool coverage

Exact W7 Rust Client run `30647931191`:

- Windows job `91213890051`: metadata PASS, fmt PASS, Clippy PASS, tests PASS, architecture PASS;
- Supply Chain job `91213890169`: advisories/bans/licenses/sources PASS;
- 139 zwykłych testów produktu, narzędzi, integracji i security;
- brak fazy documentation tests.

Finalne heady PR #50, #54, #61, #73, #79, #86, #92, #104, #110, #113 i #118 posiadają successful Rust Client workflow runs.

Brak dowodów: fuzz, soak, interactive runtime, real GPU, real-service E2E, performance, production asset/legal.

## 8. Claims-versus-evidence matrix

| Claim | Status | Ocena |
|---|---|---|
| workspace/tooling readiness | PROVEN | gotowy do dalszej ograniczonej pracy |
| architecture compliance bieżącego grafu | DERIVED | graf zgodny; gate niekompletny |
| security foundation | DERIVED | częściowa; finding 001/002 |
| synthetic technical-login readiness | PROVEN | gotowy jako syntetyczny slice |
| real Canary wire compatibility | UNKNOWN | adapter produkcyjny wyłączony przed I/O |
| deployed Identity/Gateway compatibility | UNKNOWN | brak deployed evidence |
| interactive Windows runtime | UNKNOWN | tylko hosted compile/test |
| GPU/driver compatibility | UNKNOWN | brak real presentation/hardware |
| production asset pipeline | UNKNOWN | syntetyczny format/compiler בלבד |
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
AFFECTED_PATHS: `crates/identity/src/lib.rs:1-220,320-545,680-705`; `crates/platform/src/lib.rs:90-205,300-390`; `crates/game-session/src/lib.rs:130-260`; `W7_IDENTITY_EVIDENCE.md`; `MODULE_CATALOG.md`  
EVIDENCE: authorization URL, callback target, returned state/code i verifier copies są zwykłymi `String`/`Url`; `UreqTransport::post` tworzy zwykły `String` przez `format!("Bearer {bearer}")`; część error paths odrzuca zwykłe `String`/`Vec`; dokumentacja twierdzi terminal cleanup wszystkich secret-bearing values.  
IMPACT: kopie state, code, access token, ticket lub credential mogą pozostać w pamięci alokatora. Redaction formatowania działa, lecz end-to-end zeroization nie jest udowodnione.  
RECOMMENDATION: utrzymywać sekrety w zeroizing containers przez parsing/request construction/error paths, usunąć formatted bearer copy i zawęzić dokumentowane twierdzenie do faktycznie egzekwowanego zakresu.  
REMEDIATION_PERFORMED: NO

### OTC2-AUD-002

ID: OTC2-AUD-002  
TITLE: Zamknięcie okna może blokować główny wątek event loop podczas synchronicznego join  
STATUS: DERIVED  
SEVERITY: MEDIUM  
CONFIDENCE: HIGH  
AFFECTED_PATHS: `apps/client/src/main.rs:105-175,185-235`; `crates/app-runtime/src/runtime.rs:180-270,390-465`; `crates/identity/src/lib.rs:680-705`; `crates/platform/src/lib.rs:300-350`; `apps/client/src/technical_login.rs:170-245`; `crates/transport/src/lib.rs:1-120`  
EVIDENCE: close/destroy wywołuje `request_exit` na event-loop thread; shutdown anuluje i natychmiast wykonuje blokujący `join`; cancellation nie przerywa trwającego Ureq send; HTTP timeout może wynosić do 30 s; TCP/env timeout nie ma twardej górnej granicy.  
IMPACT: close lub fatal renderer path może zamrozić okno do zakończenia blokującego I/O.  
RECOMMENDATION: nonblocking shutdown state machine, cancellation request, dalsze pompowanie event loop, join tylko finished workers oraz hard upper bounds timeoutów.  
REMEDIATION_PERFORMED: NO

### OTC2-AUD-003

ID: OTC2-AUD-003  
TITLE: Asset compiler ma wyścig TOCTOU między walidacją ścieżki a otwarciem pliku  
STATUS: DERIVED  
SEVERITY: MEDIUM  
CONFIDENCE: HIGH  
AFFECTED_PATHS: `tools/asset-compiler/src/lib.rs:285-330` oraz testy static symlink  
EVIDENCE: `symlink_metadata`, `canonicalize` i metadata checks poprzedzają osobne późniejsze `File::open`; brak handle-relative no-follow open lub weryfikacji finalnej tożsamości otwartego handle; testy nie obejmują concurrent replacement.  
IMPACT: przy współdzielonym niezaufanym source tree sprawdzona ścieżka może zostać podmieniona przed open, osłabiając containment i provenance.  
RECOMMENDATION: otwierać względem trusted directory handle z no-follow/reparse protection i sprawdzać final path/identity albo jawnie wymagać exclusive trusted ownership source tree.  
REMEDIATION_PERFORMED: NO

### OTC2-AUD-004

ID: OTC2-AUD-004  
TITLE: Architecture gate implementuje częściowy denylist zamiast kompletnej polityki krawędzi  
STATUS: PROVEN  
SEVERITY: MEDIUM  
CONFIDENCE: HIGH  
AFFECTED_PATHS: `tools/architecture-check/src/lib.rs:385-455`; `tests/architecture-fixtures/**`; `docs/architecture/ARCHITECTURE.md`; `MODULE_CATALOG.md`  
EVIDENCE: `forbidden_edge` zawiera wybrane pary source/target; pozostałe krawędzie przechodzą, o ile nie tworzą cyklu lub nie naruszają innej reguły; przykładowe `transport -> renderer` nie zostałoby odrzucone mimo naruszenia modelu; bieżący graf nie zawiera tej krawędzi.  
IMPACT: zielony architecture-check nie dowodzi pełnej normatywnej zgodności.  
RECOMMENDATION: explicit allow-edge matrix lub layer order, pełne fixtures dla kategorii i test exhaustive coverage katalogu kategorii.  
REMEDIATION_PERFORMED: NO

### OTC2-AUD-005

ID: OTC2-AUD-005  
TITLE: Live GitHub, governance index i część evidence files opisują różne stany  
STATUS: CONFLICT  
SEVERITY: LOW  
CONFIDENCE: HIGH  
AFFECTED_PATHS: `docs/agents/ACTIVE_WORK.md`; `docs/agents/MODULE_CATALOG.md`; W7 entry i Canary evidence  
EVIDENCE: ACTIVE_WORK wskazuje #4/#3 jako otwarte, live state wskazuje #97/#48/#23; MODULE_CATALOG nadal oznacza #4 active; entry evidence mówi validation in progress, a Canary evidence nadal nazywa #113 draftem po merge/archive.  
IMPACT: możliwa błędna detekcja ownership i duplikacja pracy.  
RECOMMENDATION: dokumentacyjna synchronizacja i automatyczna walidacja indeksów względem live GitHub/task state.  
REMEDIATION_PERFORMED: NO

### OTC2-AUD-006

ID: OTC2-AUD-006  
TITLE: CI/evidence deklaruje doctesty, lecz workflow wybiera `--all-targets` bez `--doc`  
STATUS: CONFLICT  
SEVERITY: LOW  
CONFIDENCE: HIGH  
AFFECTED_PATHS: `.github/workflows/rust-client.yml`; `BUILD_TEST_MATRIX.md`; `W7_LOGIN_E2E_EVIDENCE.md`; `crates/game-session/src/lib.rs:130-155`  
EVIDENCE: workflow uruchamia `cargo test --workspace --all-targets --locked`; log ma 139 zwykłych testów i nie ma `Doc-tests`; `GameEntryCredential` zawiera `compile_fail` doctest.  
IMPACT: evidence zawyża wykonane pokrycie, a compile-fail API barrier nie jest egzekwowany przez recorded CI.  
RECOMMENDATION: osobne `cargo test --workspace --doc --locked` albo usunięcie twierdzeń o doctestach.  
REMEDIATION_PERFORMED: NO

### OTC2-AUD-007

ID: OTC2-AUD-007  
TITLE: Production readiness pozostaje nieudowodniona poza syntetycznym technical-login slice  
STATUS: UNKNOWN  
SEVERITY: INFO  
CONFIDENCE: HIGH  
AFFECTED_PATHS: W7 E2E/Canary evidence; W4 runtime evidence; W5 renderer evidence; W6 asset evidence  
EVIDENCE: produkcyjny Canary zwraca `RealAdmissionUnavailable` przed I/O; brak deployed Identity/Gateway/Canary E2E, interactive Windows, real GPU, production assets/signing, legal approval, fuzz/soak/performance i gameplay.  
IMPACT: projekt jest zwalidowanym fundamentem/syntetycznym slice, nie playable ani production-ready clientem.  
RECOMMENDATION: utrzymać zamknięte gate'y, usunąć findings i dopiero potem wykonać controlled exact-revision compatibility discovery.  
REMEDIATION_PERFORMED: NO

## 10. Documentation and governance conflicts

Live GitHub i task archives są nadrzędne. Potwierdzone konflikty: stale `ACTIVE_WORK`, stale status PR #4 w module catalog, stale nagłówki W7 entry/Canary evidence oraz doctest claim bez wykonania.

## 11. Known unknowns i blockers

- brak lokalnego checkoutu/Cargo;
- brak deployed service revisions/configuration;
- brak controlled credentials;
- brak interactive Windows/GPU;
- brak production assets/legal approval;
- brak performance/fuzz/soak;
- bieżące środowisko nie potrafi uruchomić świeżej niezależnej sesji walidatora.

## 12. Readiness assessment

- bounded workspace development: READY;
- synthetic technical-login slice: READY;
- real technical login: NOT READY;
- minimum playable slice: ABSENT;
- production release: NOT READY.

## 13. Minimalne rekomendowane dalsze taski

### OTC2-RUST-LOGIN-SAFETY-HARDENING

- cel: secret-lifetime hardening, nonblocking shutdown i hard timeout caps;
- niezależność: jedna wspólna Identity/Platform/app-runtime lifecycle boundary;
- tryb: Codex;
- zależność: zwalidowany audyt;
- minimalny zakres: identity/platform/app-runtime/apps-client i focused tests, bez real Canary wire;
- acceptance evidence: nowe error/lifetime tests, responsive-close test, locked fmt/clippy/tests/doctests/architecture/deny;
- priorytet: P0.

### OTC2-ASSET-SOURCE-HANDLE-HARDENING

- cel: zamknąć source-open TOCTOU;
- niezależność: osobny offline trust boundary;
- tryb: Codex;
- zależność: zwalidowany audyt;
- minimalny zakres: asset-compiler read/open i adversarial tests;
- acceptance evidence: handle-relative/no-follow lub verified-open design i wszystkie gate'y;
- priorytet: P1.

### OTC2-ARCH-EVIDENCE-GATE-REPAIR

- cel: kompletny architecture gate, jawny doctest gate i synchronizacja governance/evidence;
- niezależność: tooling/governance bez zmiany product behavior;
- tryb: Codex;
- zależność: zwalidowany audyt;
- minimalny zakres: checker/fixtures, workflow test command i dokumenty;
- acceptance evidence: exhaustive matrix, representative edges, explicit doctests i live-consistent indexes;
- priorytet: P1.

### OTC2-REAL-COMPATIBILITY-DISCOVERY

- cel: approved exact revisions/provenance/deployment evidence dla Identity, Gateway i Canary;
- niezależność: wymaga external owners, legal/security approval i controlled environment;
- tryb: Work;
- zależności: zamknięte P0/P1 oraz dostępne approved environment/revisions;
- minimalny zakres: read-only discovery i controlled validation plan; implementacja wymaga osobnej autoryzacji;
- acceptance evidence: approved revisions, transcript/provenance matrix, TLS/DNS/deployment evidence, named Windows/GPU environment i go/no-go;
- priorytet: P1.

## 14. Artifact index

Repozytorium:

- `EVIDENCE_INDEX.md`;
- ten raport;
- `VALIDATOR_PACKET.md`;
- task checkpoint.

Zewnętrzny pakiet zawiera pełne JSON/JSONL/CSV, dependency graph, CI inventory, command/test summaries i compact raw-log summary.

## 15. Validator handoff

Audyt główny jest kompletny, ale nie jest samodzielnie zwalidowany. Świeży walidator musi ponownie sprawdzić wszystkie `MEDIUM`, próbkę `LOW`, exact main, CI/run/job/step references, kompletność 19-member inventory, brak zmian implementacyjnych oraz spróbować obalić readiness conclusion.

Dozwolony końcowy wynik: `VALIDATED`, `VALIDATED_WITH_CORRECTIONS` albo `REJECTED`.
