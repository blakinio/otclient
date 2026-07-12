# OTS / OTClient — dokument przekazania pracy między agentami

> **Status dokumentu:** aktywny  
> **Ostatnia aktualizacja:** 2026-07-12, Europe/Warsaw  
> **Główne repozytorium robocze:** `blakinio/otclient`  
> **Główna gałąź:** `main`  
> **Właściciel repozytorium:** `blakinio`  
> **Lokalna ścieżka użytkownika:** `C:\Users\barte\Documents\New project`

---

## 1. Po co istnieje ten plik

Ten plik jest trwałym handoffem dla kolejnych agentów pracujących nad projektem OTS. Ma umożliwić bezpieczne przejęcie pracy, gdy:

- bieżące okno rozmowy stanie się zbyt długie lub wolne,
- zostanie osiągnięty limit tokenów,
- pracę przejmie inny agent,
- trzeba wrócić do projektu po przerwie,
- lokalny agent utraci część kontekstu rozmowy.

Każdy agent powinien:

1. przeczytać ten dokument przed zmianami,
2. zweryfikować dynamiczny stan GitHub i lokalnego repozytorium,
3. nie zakładać, że stan opisany w sekcji „snapshot” nadal jest aktualny,
4. aktualizować ten plik po każdym większym etapie, merge’u, zmianie polityki lub wykryciu istotnego problemu,
5. nie usuwać historii decyzji bez wyraźnego powodu.

---

## 2. Cel projektu

Budujemy i utrzymujemy własny, stabilny fork OTClient Redemption przeznaczony do współpracy z Canary.

Najważniejsze cele:

- stabilny i przewidywalny klient dla serwera Canary,
- zgodność protokołu klient–serwer,
- bezpieczny i powtarzalny proces CI,
- testy jednostkowe, integracyjne, kontraktowe i regresyjne,
- ograniczenie regresji przy aktualizacjach z upstreamu,
- możliwość dalszej rozbudowy funkcji klienta i mechanik serwerowych,
- czytelne zasady pracy dla ludzi i agentów AI,
- automatyzacja bez osłabiania bezpieczeństwa repozytorium.

Długofalowo projekt może obejmować także:

- rozwój mechanik OTS po stronie Canary,
- edycję i generowanie map,
- narzędzia do questów, NPC, potworów i zawartości,
- integrację Remere’s Map Editor i client-editor,
- testy kompatybilności klient–serwer,
- regresje dla mechanik takich jak Forge, Wheel, Gem Atelier, Prey, Market i login.

---

## 3. Repozytoria i ich role

### 3.1 Repozytorium robocze

- `https://github.com/blakinio/otclient`
- To jest repozytorium, w którym wykonujemy bieżące prace.
- Wszystkie zwykłe branche i Pull Requesty mają trafiać tutaj.
- Domyślny target PR: `blakinio/otclient:main`.

### 3.2 Upstream OTClient

- `https://github.com/opentibiabr/otclient`
- Źródło aktualizacji upstream.
- Nie należy otwierać PR-ów do upstreamu bez wyraźnej zgody użytkownika.
- Nie należy przypadkowo używać upstreamu jako repozytorium docelowego PR.

### 3.3 Canary

- `https://github.com/opentibiabr/canary`
- Serwer, z którym klient ma być kompatybilny.
- Zmiany protokołu i mechanik trzeba analizować po obu stronach.

### 3.4 Remere’s Map Editor

- `https://github.com/opentibiabr/remeres-map-editor`
- Narzędzie do map OTBM.
- Potencjalny element przyszłego workflow generowania i walidacji map.

### 3.5 Client Editor

- `https://github.com/opentibiabr/client-editor`
- Narzędzie pomocnicze dla danych i zasobów klienta.

### 3.6 Zasada krytyczna

Nigdy nie otwieraj PR-a do `opentibiabr/otclient`, jeśli użytkownik nie poprosił o wkład do upstreamu wprost.

Wcześniej doszło do przypadkowego otwarcia PR-a do upstreamu. PR został zamknięty i nie został zmergowany. Nie wolno powtórzyć tego błędu.

---

## 4. Aktualny zweryfikowany stan repozytorium

### 4.1 `main`

Snapshot z 2026-07-12:

- aktualny commit `main`:
  - `bdd83db12292bb646280372dfdf8ae5cd50e3072`
  - `fix(ci): restore runtime-scoped Lua syntax checks`
- poprzedni commit governance:
  - `208c64d336eef7c199fa022daf08d1ee95295575`
  - `Chore/repository governance (#1)`

Przed rozpoczęciem pracy zawsze wykonaj:

```powershell
git fetch --all --prune
git status -sb
git branch -vv
git log --oneline --decorate -10 origin/main
```

Nie zakładaj, że powyższy SHA nadal jest najnowszy.

### 4.2 Otwarty Pull Request test foundation

Snapshot z 2026-07-12:

- PR: `#3`
- URL: `https://github.com/blakinio/otclient/pull/3`
- tytuł: `test: establish client unit and integration test foundation`
- stan: otwarty
- draft: nie
- base: `main`
- base SHA: `bdd83db12292bb646280372dfdf8ae5cd50e3072`
- head branch: `test/client-test-foundation`
- head SHA: `92d29382e6a87cefb6453ac3b3d7b5224423fd3e`
- liczba commitów w chwili snapshotu: 9
- zmienione pliki: 43
- additions: 1936
- deletions: 14
- mergeable: tak
- CI przy ostatniej weryfikacji: `in_progress`
- workflow: `CI`
- run number: `7`
- run ID: `29186723650`

Ostatni commit na branchu testowym:

```text
92d29382e6a87cefb6453ac3b3d7b5224423fd3e
test: include client compile context in new tests
```

Commit dodał wymagany kontekst kompilacyjny, m.in. `#include <framework/pch.h>`, do nowych testów i brakujące include’y dla typów klienta.

Dynamiczny stan sprawdzaj poleceniami:

```powershell
gh pr view 3 --repo blakinio/otclient
gh pr checks 3 --repo blakinio/otclient
gh run list --repo blakinio/otclient --branch test/client-test-foundation
```

---

## 5. Zakończone etapy i pełny changelog projektu

## 5.1 Uporządkowanie forka

- Fork `blakinio/otclient` został przeanalizowany względem upstreamu.
- Na początku był zsynchronizowany z upstreamem.
- Ustalono, że właściwą bazą klienta dla Canary jest OTClient Redemption.
- Ustalono, że zmiany produkcyjne powinny być osobne od zmian governance i test infrastructure.

## 5.2 Governance foundation — PR #1

Gałąź:

```text
chore/repository-governance
```

Merge commit po squash:

```text
208c64d336eef7c199fa022daf08d1ee95295575
Chore/repository governance (#1)
```

Zakres obejmował m.in.:

- stabilny wymagany status CI,
- minimalne uprawnienia GitHub Actions,
- ograniczenie ryzyka workflowów uprzywilejowanych,
- przypinęcie akcji do konkretnych SHA,
- Dependabot,
- bezpieczny workflow dla Dependabot,
- retry tylko dla awarii infrastrukturalnych,
- CODEOWNERS,
- szablony issue,
- szablon Pull Requesta,
- dokumentację contribution/governance,
- helper do konfiguracji ustawień repozytorium.

Ważne pliki:

```text
.github/CODEOWNERS
.github/ISSUE_TEMPLATE/
.github/PULL_REQUEST_TEMPLATE.md
.github/dependabot.yml
.github/workflows/ci.yml
.github/workflows/reusable-tests-lua.yml
scripts/configure-github-repository.sh
```

W governance dodano łącznie około 30 plików lub zmian organizacyjnych.

### Problem podczas publikacji governance

Lokalna gałąź: będnie śledziła `origin/main`.

Naprawiono to przez:

```powershell
git branch --unset-upstream
git push -u origin chore/repository-governance
```

Wniosek dla kolejnych agentów:

- po utworzeniu brancha zawsze sprawdź `git branch -vv`,
- branch roboczy powinien śledzić odpowiadający mu branch na `origin`,
- nie zakładaj, że `git push` ustawi poprawny upstream.

## 5.3 Naprawa Lua CI — PR #2

Po merge governance CI początkowo nie przechodziło.

Pierwotny problem:

- workflow Lua skanował wszystkie śledzone pliki `*.lua`,
- część plików nie była runtime’owym kodem OTClient,
- wymagany check `Lua Syntax / Check Lua Syntax` padał,
- agregat `CI / Required` także padał,
- buildy były pomijane zgodnie z wykrytym zakresem zmian.

Naprawa:

- branch: `fix/ci-lua-syntax`
- PR #2: `fix(ci): restore runtime-scoped Lua syntax checks`
- commit po squash:
  - `bdd83db12292bb646280372dfdf8ae5cd50e3072`

Nowy zakres blokującego sprawdzania Lua:

```text
data/
modules/
mods/
```

Pliki są wyszukiwane deterministycznie:

```bash
find data modules mods -type f -name '*.lua' -print0 | sort -z
```

Prawdziwe błędy składni nadal są fatalne.

Po naprawie przeszły:

- Detect Build Scope,
- Fast Checks,
- syntax/workflow checks,
- Lua Syntax,
- informacyjna analiza statyczna,
- `CI / Required`.

Buildy platformowe mogły być pominięte, ponieważ zmiana dotyczyła tylko workflow CI. To było oczekiwane.

## 5.4 Ustawienia Pull Requestów

Zweryfikowane ustawienia repozytorium:

- default branch: `main`
- Allow auto-merge: ON
- Always suggest updating pull request branches / allow update branch: ON
- Allow squash merging: ON
- Allow merge commits: OFF
- Allow rebase merging: OFF
- Automatically delete head branches: ON
- Require contributors to sign off web-based commits: OFF
- Allow comments on commits: ON

Efektywny sposób merge:

```text
squash only
```

## 5.5 Ochrona `main`

Ustalono, że używamy:

```text
jednego Branch Ruleset
```

Nie używamy równolegle klasycznej:

```text
Branch protection rule
```

Stara branch protection rule została usunięta.

Weryfikacja klasycznego mechanizmu zwraca:

```json
{
  "message": "Branch not protected",
  "status": "404"
}
```

To jest prawidłowe, ponieważ `main` jest chroniony przez Ruleset, nie przez legacy branch protection.

### Aktywny Ruleset

Nazwa:

```text
Protect main
```

Parametry:

- target: `branch`
- enforcement: `active`
- branch target:
  - `~DEFAULT_BRANCH`
- blokada usuwania:
  - `deletion`
- blokada force push:
  - `non_fast_forward`
- liniowa historia:
  - `required_linear_history`
- wymagany Pull Request:
  - approvals: `0`
  - dismiss stale reviews: `false`
  - Code Owner review: `false`
  - last push approval: `false`
  - review thread resolution: `true`
  - allowed merge methods: tylko `squash`
- wymagane checki:
  - `CI / Required`
- branch musi być aktualny względem `main`:
  - `strict_required_status_checks_policy: true`
- `do_not_enforce_on_create: false`
- brak wymaganego CodeQL/code scanning w rulesecie
- bypass:
  - administrator repozytorium
  - `RepositoryRole`
  - actor ID `5`
  - mode `always`

Zweryfikowany efektywny wynik:

```json
{
  "rules": [
    "deletion",
    "non_fast_forward",
    "required_linear_history",
    "pull_request",
    "required_status_checks"
  ],
  "merge_methods": [
    "squash"
  ],
  "checks": [
    "CI / Required"
  ]
}
```

### Ważny kompromis

`strict_required_status_checks_policy: true` oznacza, że branch PR musi być aktualny względem `main`.

Może to czasem powodować ponowne uruchomienie CI lub potrzebę użycia `Update branch`, gdy `main` zmieni się w trakcie pracy.

Jest to świadoma aktualna decyzja. Nie wyłączaj tego bez wyraźnej decyzji użytkownika.

## 5.6 GitHub CLI na komputerze użytkownika

Na Windows zainstalowano:

```text
gh version 2.96.0
```

Użytkownik zalogował się jako:

```text
blakinio
```

Protokół Git:

```text
HTTPS
```

Na lokalnym komputerze użytkownika `gh` działa.

Nie zakładaj jednak, że `gh` jest dostępne w każdym kontenerze agenta. Brak `gh` w kontenerze nie może blokować implementacji, lokalnych commitów ani zwykłego `git push`.

---

## 6. Architektura CI, której nie wolno przypadkowo zepsuć

## 6.1 Jeden stabilny wymagany check

Ruleset wymaga dokładnie:

```text
CI / Required
```

Nie dodawaj do Rulesetu nazw dynamicznych jobów matrix, warunkowych buildów ani checków, które nie występują przy każdym PR.

`CI / Required` ma być agregatem uruchamianym zawsze i oceniać wyniki poprzednich jobów.

To pozwala:

- wymagać jednego stabilnego statusu,
- pomijać niepotrzebne buildy przy zmianach dokumentacji,
- nie blokować merge przez brak warunkowego checka,
- zachować czytelną ochronę `main`.

## 6.2 Scope detection

Workflow wykrywa zakres zmian i może pominąć kosztowne buildy, gdy nie są potrzebne.

Ważne:

- dokumentacyjny PR nadal musi otrzymać `CI / Required`,
- nie stosować workflow-level `paths` w sposób, który całkowicie uniemożliwi pojawienie się wymaganego checka,
- warunkowe joby mogą być `skipped`, ale agregat musi poprawnie je interpretować.

## 6.3 Uprawnienia i bezpieczeństwo

Zasady:

- minimalne `permissions`,
- nie zwiększać globalnie uprawnień workflow,
- akcje zewnętrzne przypinać do SHA,
- nie wykonywać kodu z niezaufanego PR w kontekście sekretów,
- `pull_request_target` tylko przy jasno udowodnionym bezpiecznym modelu,
- nie checkoutować kodu PR w uprzywilejowanym workflow.

Bezpieczny workflow Dependabot:

- read-only,
- sprawdza, że aktorem jest Dependabot,
- sprawdza, że PR pochodzi z tego samego repo,
- nie checkoutuje kodu PR,
- automatyzacja tylko w bezpiecznym zakresie.

## 6.4 Retry infrastrukturalny

Retry nie może ukrywać błędów testów.

Dopuszczony retry tylko dla przypadków infrastrukturalnych, np.:

- cancelled,
- timed out,
- startup failure.

Maksymalnie jeden kontrolowany retry.

## 6.5 Lua syntax

Blokujący Lua syntax job ma skanować runtime roots:

```text
data
modules
mods
```

Nie wracaj do:

```bash
git ls-files '*.lua'
```

bez analizy wpływu, ponieważ to wcześniej zepsuło CI.

---

## 7. Test foundation — zakres PR #3

## 7.1 Cel

Utworzyć pierwszą deterministyczną bazę testów klienta:

- unit,
- integration,
- contract,
- Lua,
- regression support.

PR nie powinien zmieniać produkcyjnego zachowania klienta.

## 7.2 Stan przed PR

Przed zmianami:

- około 23 wykrywane testy GoogleTest,
- 3 istniejące targety,
- coverage głównie dla:
  - map spectators,
  - string encoding,
  - OTML aliases,
- CTest wykonywany głównie w Linux Debug,
- Lua CI sprawdzało głównie składnię,
- brak wspólnych message builders,
- brak testu protocol loopback,
- brak cross-language resource contracts,
- brak uporządkowanego backlogu regresji.

## 7.3 Nowa struktura

Nowe lub rozbudowane katalogi:

```text
tests/unit/
tests/integration/
tests/lua/
tests/fixtures/
tests/support/
```

Nowe targety CMake:

```text
otclient_message_tests
otclient_test_support_tests
otclient_tile_order_tests
otclient_protocol_contract_tests
otclient_protocol_loopback_tests
```

Nowe rejestracje CTest dla Lua:

```text
otclient_lua_unit_tests
otclient_lua_contract_tests
otclient_lua_runner_failure_contract
```

Oczekiwany zakres po konfiguracji:

- 58 przypadków GoogleTest,
- 3 rejestracje Lua CTest,
- 7 pozytywnych przypadków Lua,
- 1 celowo negatywny kontrakt failure runnera.

## 7.4 Pokryte obszary

### InputMessage

- U8,
- U16,
- U32,
- U64,
- strings,
- positions,
- cursor,
- unread bytes,
- EOF,
- skipping,
- empty bodies,
- bounds,
- reserved-header offset semantics.

### OutputMessage

- kodowanie liczb,
- kodowanie stringów,
- byte order,
- positions,
- size,
- append preservation,
- reset.

### TestEnvironment

- lifecycle,
- deterministic fake resources,
- fake game state,
- fake local player,
- callback ordering.

### Tile / Thing builders

- syntetyczne Tile,
- ThingType,
- Item,
- Creature,
- ordering,
- selection,
- overlap,
- add/remove,
- reguły pustego tile.

### Protocol contracts

- wybrane zakresy opcode,
- unikalność opcode,
- kontrakty C++ ↔ Lua,
- ResourceTypes,
- feature names,
- singular fragment identifiers `84/85`,
- ochrona przed błędnymi aliasami `BANK_BALANCE`.

### Integration

- bounded loopback,
- ephemeral local port,
- limit około 3 sekund,
- jeden world-light packet.

### OTML

- nesting,
- comments,
- aliases,
- empty values,
- deterministic reload,
- invalid indentation.

### Lua runner

- assertions,
- named reporting,
- nonzero exit on failure,
- minimal client-global stubs,
- pure gamelib formatting tests,
- ResourceTypes contracts.

## 7.5 Presety lokalne

Linux:

```bash
cmake --preset linux-tests
cmake --build --preset linux-tests
ctest --preset linux-tests
ctest --test-dir build/linux-tests -L unit --output-on-failure
ctest --test-dir build/linux-tests -L lua --output-on-failure
ctest --test-dir build/linux-tests -L integration --output-on-failure
```

Odpowiedniki:

```text
windows-tests
macos-tests
```

Opcjonalna analiza ręczna:

```text
linux-asan-tests
linux-coverage-tests
```

## 7.6 Lokalna walidacja wykonana przed PR

Według opisu PR:

- CMake preset JSON parsuje się,
- nowe Lua unit: 4/4,
- nowe Lua resource contracts: 3/3,
- Lua runner failure contract: passed,
- nowe źródła Lua kompilują się do bytecode LuaJIT,
- zmodyfikowane workflowy przeszły yamllint,
- `git diff --check` przeszedł,
- pełne C++/CTest przekazane do CI, ponieważ lokalny Windows nie miał toolchainu vcpkg repozytorium.

Nie wolno przedstawiać pełnych testów C++ jako zaliczonych lokalnie, jeśli nie zostały faktycznie uruchomione.

## 7.7 CI w PR #3

Zmiany przewidują:

- wymagany Linux test configuration,
- osobne etykiety:
  - unit,
  - lua,
  - integration,
- dedykowany Windows test build/CTest,
- docs-only nadal korzysta z path scope,
- coverage i ASAN jako opcjonalne manual jobs,
- brak progu coverage,
- brak zewnętrznego tokenu do raportowania coverage.

## 7.8 Rzeczy celowo poza zakresem PR #3

Nie dodawać do tego PR bez bardzo dobrego powodu:

- kompletnego Forge,
- kompletnego Wheel,
- kompletnego Gem Atelier,
- Prey,
- Market,
- pełnego login flow,
- headless startup,
- wszystkich parser opcode dispatch seams,
- pełnych mocków globali klienta,
- Canary E2E,
- zmian zachowania produkcyjnego,
- zmian branch protection,
- zmian Rulesetu,
- zmian ustawień repozytorium.

Wheel używający plural fragment names został zapisany jako przyszła regresja/fix, nie jako zmiana zachowania w PR foundation.

## 7.9 Client assets

PR #3 nie powinien zmieniać instalacji ani ładowania client-assets.

Oczekiwane ścieżki runtime pozostają w stylu OTClient:

```text
data/things/<version>/
data/sounds/<version>/
bin/*
```

Nie osłabiać:

- strict manifest SHA-256,
- bezpiecznych ustawień raw fallback,
- walidacji źródła assetów.

Nie commitować:

- sekretów,
- tokenów,
- prywatnych danych serwera,
- nielegalnie pozyskanych lub prawnie zastrzeżonych assetów CipSoft.

---

## 8. Natychmiastowy plan dla kolejnego agenta

### Priorytet 1 — dokończyć PR #3

1. Zweryfikować aktualny stan:
   ```powershell
   gh pr view 3 --repo blakinio/otclient
   gh pr checks 3 --repo blakinio/otclient
   ```

2. Sprawdzić, czy branch nadal jest:
   ```text
   test/client-test-foundation
   ```

3. Upewnić się, że target to:
   ```text
   blakinio/otclient:main
   ```

4. Jeśli CI pada:
   - odczytać konkretny job i log,
   - naprawić przyczynę,
   - nie wyłączać testu,
   - nie zmieniać wymaganych checków,
   - nie dodawać `continue-on-error` tylko po to, aby uzyskać zielony status,
   - nie osłabiać kompilacji warningów bez analizy,
   - commitować poprawkę na tym samym branchu.

5. Po poprawkach:
   ```powershell
   git status -sb
   git diff --check
   git push
   gh pr checks 3 --repo blakinio/otclient --watch
   ```

6. Przed merge:
   - `CI / Required` musi być zielone,
   - branch musi być aktualny względem `main`,
   - wszystkie rozmowy review muszą być rozwiązane,
   - PR nie może zawierać zmian produkcyjnego zachowania,
   - sprawdzić summary i listę testów,
   - merge tylko przez squash.

7. Po merge:
   ```powershell
   git checkout main
   git pull --ff-only origin main
   git branch -d test/client-test-foundation
   git fetch --prune
   ```

8. Zaktualizować ten dokument:
   - nowy SHA `main`,
   - numer merge,
   - wynik CI,
   - liczbę finalnych testów,
   - czas CI,
   - znane follow-upy.

### Priorytet 2 — backlog regresji

Po stabilnym merge test foundation kolejne PR-y powinny być małe i tematyczne.

Rekomendowana kolejność:

1. protocol parser contracts,
2. login/character list seams,
3. Forge contracts,
4. Wheel contracts,
5. Gem Atelier contracts,
6. Prey,
7. Market,
8. Canary client/server E2E,
9. headless client smoke test,
10. map/content tooling integration.

Każdy temat w osobnym branchu i PR.

---

## 9. Standard pracy agenta

## 9.1 Początek każdej sesji

Na Windows:

```powershell
cd "C:\Users\barte\Documents\New project"

git status -sb
git remote -v
git fetch --all --prune
git branch -vv
git log --oneline --decorate -10 origin/main

gh auth status
gh pr list --repo blakinio/otclient
```

Agent w kontenerze powinien wykonać analogiczne polecenia dostępne w jego środowisku.

## 9.2 Remote’y

Docelowo:

```text
origin   -> https://github.com/blakinio/otclient.git
upstream -> https://github.com/opentibiabr/otclient.git
```

Nie zakładaj, że `upstream` istnieje. Najpierw sprawdź.

Dodanie upstreamu, gdy brak:

```powershell
git remote add upstream https://github.com/opentibiabr/otclient.git
git fetch upstream
```

## 9.3 Tworzenie brancha

Nowy branch zawsze z aktualnego `origin/main`, chyba że użytkownik wyraźnie wskazał inną bazę.

```powershell
git fetch origin
git checkout -B <branch-name> origin/main
```

Nie twórz nowego zadania z:

```text
chore/repository-governance
```

ani z innego starego brancha.

## 9.4 Nazewnictwo branchy

Stosowane prefiksy:

```text
feat/
fix/
test/
ci/
docs/
chore/
refactor/
```

Przykłady:

```text
test/client-test-foundation
fix/ci-lua-syntax
chore/repository-governance
```

## 9.5 Commity

Preferowane Conventional Commits:

```text
feat:
fix:
test:
ci:
docs:
chore:
refactor:
build:
```

Commity powinny być:

- logiczne,
- możliwie małe,
- bez przypadkowych plików,
- bez sekretów,
- bez plików build output,
- bez niepowiązanych refaktorów.

Przed commitem:

```powershell
git status --short
git diff --check
git diff --stat
```

## 9.6 Pull Request

Każdy istotny PR powinien zawierać:

- cel,
- stan przed zmianą,
- zakres zmian,
- wpływ na produkcję,
- sposób uruchomienia testów,
- co faktycznie zweryfikowano,
- czego nie zweryfikowano,
- ryzyka,
- follow-upy,
- informację o client-assets, jeśli temat ich dotyczy.

Target:

```text
blakinio/otclient:main
```

Merge:

```text
squash
```

Nie pushuj bezpośrednio do `main`.

## 9.7 Admin bypass

Bypass administratora istnieje na wypadek awarii.

Nie używać go do:

- ominięcia czerwonego CI,
- szybkiego merge bez testów,
- ominięcia unresolved conversations,
- przepchnięcia nieaktualnego brancha.

Bypass tylko w realnej sytuacji awaryjnej, z opisem powodu.

---

## 10. Pułapki i znane błędy

### 10.1 Przypadkowy PR do upstreamu

Objaw:

- PR celuje w `opentibiabr/otclient:main`.

Działanie:

- nie merge’ować,
- zamknąć,
- utworzyć poprawny PR w `blakinio/otclient`.

### 10.2 Zły upstream lokalnego brancha

Sprawdzenie:

```powershell
git branch -vv
```

Naprawa:

```powershell
git branch --unset-upstream
git push -u origin <branch>
```

### 10.3 Agent nie ma `gh`

Brak `gh` nie jest powodem do zatrzymania implementacji.

Można nadal:

- analizować kod,
- tworzyć branch,
- commitować,
- testować,
- wykonać `git push`.

PR można utworzyć później przez przeglądarkę, przez dostępne narzędzie GitHub albo po instalacji `gh`.

### 10.4 PowerShell i `gh --jq`

Windows PowerShell może błędnie interpretować złożone wyrażenia `--jq`.

Zamiast tego używać:

```powershell
$rules = gh api repos/blakinio/otclient/rules/branches/main | ConvertFrom-Json
```

Przykład inspekcji:

```powershell
[PSCustomObject]@{
    rules = @($rules.type)
    merge_methods = @(
        ($rules | Where-Object { $_.type -eq 'pull_request' }).parameters.allowed_merge_methods
    )
    checks = @(
        ($rules | Where-Object { $_.type -eq 'required_status_checks' }).parameters.required_status_checks.context
    )
} | ConvertTo-Json -Depth 5
```

### 10.5 `Branch not protected` 404

Polecenie:

```powershell
gh api repos/blakinio/otclient/branches/main/protection
```

zwraca 404, ponieważ klasyczna ochrona została usunięta.

To jest poprawne.

Aktywne reguły sprawdzamy przez:

```powershell
gh api repos/blakinio/otclient/rules/branches/main
```

### 10.6 Dynamiczne nazwy checków

Nie dodawaj do Rulesetu nazw takich jak konkretne platformowe joby matrix, jeżeli mogą zostać pominięte.

Jedynym wymaganym statusem ma pozostać:

```text
CI / Required
```

### 10.7 Fałszywie zielone CI

Zabronione skróty:

- `continue-on-error` na krytycznych testach,
- ignorowanie exit code,
- wyłączanie testów bez uzasadnienia,
- catch-all, który zawsze zwraca 0,
- usunięcie testu tylko dlatego, że ujawnia błąd,
- zmiana testu tak, aby akceptował nieprawidłowe zachowanie.

### 10.8 Fałszywe deklaracje walidacji

Agent ma jasno rozróżniać:

- wykonano lokalnie,
- wykonano w CI,
- nie wykonano,
- nie było możliwe z powodu brakującego toolchainu.

Nie wolno pisać „wszystkie testy przeszły”, jeśli sprawdzono tylko Lua lub parsowanie CMake JSON.

---

## 11. Zasady zmian produkcyjnych

Test foundation ma pozostać test-only.

Dalsze zmiany produkcyjne:

- osobny branch,
- osobny PR,
- test reprodukujący problem,
- opis zachowania przed i po,
- porównanie z Canary,
- w razie potrzeby porównanie z oficjalnym klientem poprzez legalną obserwację zachowania,
- brak commitowania proprietary assets lub wycieków.

Przy zmianie protokołu sprawdzić:

- wersję protokołu,
- feature flags,
- opcode po obu stronach,
- kolejność pól,
- typy i szerokości liczb,
- warunki wersji klienta,
- zgodność C++ i Lua,
- zachowanie przy nieznanym opcode,
- regresje na starszych protokołach.

---

## 12. Dokumenty, które kolejny agent powinien przeczytać

W `main` lub aktualnym branchu:

```text
.github/PULL_REQUEST_TEMPLATE.md
.github/CODEOWNERS
.github/workflows/ci.yml
.github/workflows/reusable-tests-lua.yml
.github/dependabot.yml
scripts/configure-github-repository.sh
```

Na branchu `test/client-test-foundation`:

```text
docs/testing-strategy.md
docs/regression-test-backlog.md
tests/
CMakePresets.json
```

Przed edycją workflowów należy przeczytać cały zależny workflow i sposób agregacji `CI / Required`, nie tylko pojedynczy job.

---

## 13. Protokół aktualizacji tego pliku

Po każdym większym etapie agent ma dodać wpis do changelogu i zaktualizować snapshot.

Minimalny wpis:

```markdown
### YYYY-MM-DD — krótki tytuł

- Branch:
- PR:
- Base SHA:
- Head SHA:
- Co zmieniono:
- Dlaczego:
- Testy lokalne:
- Wynik CI:
- Merge SHA:
- Znane problemy:
- Następny krok:
```

Nie nadpisywać dawnych decyzji bez śladu.

Gdy decyzja się zmienia:

1. zachować poprzednią decyzję w changelogu,
2. opisać nową,
3. podać powód,
4. zaktualizować sekcję „aktualny stan”.

---

## 14. Changelog handoffu

### 2026-07-12 — utworzenie dokumentu handoff

- Spisano cel projektu.
- Spisano role repozytoriów.
- Udokumentowano governance PR #1.
- Udokumentowano naprawę Lua CI PR #2.
- Udokumentowano ustawienia repozytorium.
- Udokumentowano aktywny Ruleset `Protect main`.
- Potwierdzono brak legacy branch protection.
- Spisano stan PR #3 test foundation.
- Spisano procedury dla kolejnych agentów.
- Spisano znane pułapki i wymagane polecenia weryfikacyjne.

### 2026-07-12 — PR #3 test foundation otwarty

- PR: `https://github.com/blakinio/otclient/pull/3`
- Branch: `test/client-test-foundation`
- Base: `main`
- Scope: unit, integration, contract, Lua i regression foundation.
- Produkcyjne zachowanie klienta nie powinno być zmieniane.
- CI było w toku w chwili utworzenia tego dokumentu.

### 2026-07-12 — końcowa poprawka kontekstu kompilacji nowych testów

- Commit:
  - `92d29382e6a87cefb6453ac3b3d7b5224423fd3e`
- Dodano wymagane `framework/pch.h`.
- Dodano brakujące typy klienta w testach tile.
- Cel: naprawić błędy kompilacji wynikające z kontekstu include/PCH.

### 2026-07-12 — Ruleset `Protect main`

- Włączono nowy Branch Ruleset.
- Dozwolony tylko squash.
- Wymagany `CI / Required`.
- Wymagane rozwiązanie rozmów.
- Approvals: 0.
- Wymagany aktualny branch.
- Blokada deletion i force push.
- Liniowa historia.
- Usunięto regułę CodeQL z wymagań.
- Usunięto starą branch protection rule.

### 2026-07-11 — naprawa runtime-scoped Lua CI

- PR #2 zmergowany.
- Commit:
  - `bdd83db12292bb646280372dfdf8ae5cd50e3072`
- Blokujące sprawdzanie Lua ograniczono do:
  - `data`,
  - `modules`,
  - `mods`.
- `CI / Required` wróciło do stanu zielonego.

### 2026-07-11 — repository governance

- PR #1 zmergowany.
- Commit:
  - `208c64d336eef7c199fa022daf08d1ee95295575`
- Dodano zasady repozytorium, CI, Dependabot, szablony, CODEOWNERS i dokumentację.

---

## 15. Szybki checklist dla nowego agenta

```text
[ ] Przeczytałem cały AGENT_HANDOFF.md.
[ ] Sprawdziłem git status.
[ ] Sprawdziłem remote -v.
[ ] Wykonałem fetch --all --prune.
[ ] Sprawdziłem aktualny origin/main.
[ ] Sprawdziłem otwarte PR-y.
[ ] Potwierdziłem właściwe repo docelowe: blakinio/otclient.
[ ] Potwierdziłem właściwy branch.
[ ] Nie pracuję na starej gałęzi governance.
[ ] Nie zmieniam Rulesetu ani ustawień repo bez polecenia.
[ ] Nie osłabiam CI.
[ ] Nie mieszam zmian produkcyjnych z test foundation.
[ ] Dokumentuję faktycznie wykonane testy.
[ ] Aktualizuję ten plik przed przekazaniem pracy.
```

---

## 16. Najważniejsze źródła

Repozytorium robocze:

```text
https://github.com/blakinio/otclient
```

Aktualny test foundation PR:

```text
https://github.com/blakinio/otclient/pull/3
```

Upstreamy projektu:

```text
https://github.com/opentibiabr/otclient
https://github.com/opentibiabr/canary
https://github.com/opentibiabr/remeres-map-editor
https://github.com/opentibiabr/client-editor
```

---

## 17. Jednozdaniowe podsumowanie dla kolejnego agenta

Kontynuuj rozwój `blakinio/otclient` z aktualnego `origin/main`, najpierw doprowadź PR #3 `test/client-test-foundation` do pełnego zielonego `CI / Required`, nie osłabiaj Rulesetu ani CI, nie mieszaj zmian produkcyjnych z test infrastructure i zapisuj każdy istotny etap w tym dokumencie.
