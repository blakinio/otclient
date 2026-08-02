# Canary Current Fixture Feasibility Index

Status: generated provenance/feasibility metadata only  
Producer: `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`  
No credentials, session keys, private packet captures, proprietary assets or producer implementation bodies are contained here.

## Family feasibility

| Family | Entries | Literal opcodes | Unknown opcodes | Feasibility | Allowed fixture source | Safety/claim boundary | Proposed package |
|---|---:|---:|---:|---|---|---|---|
| bootstrap | 15 | 14 | 1 | controlled-environment-required | synthetic framing/unit fixtures plus disposable controlled account/session capture | session keys, credentials and private captures must never be committed | `protocol-canary-bootstrap` |
| chat | 29 | 29 | 0 | synthetic-plus-controlled | project-original malformed/boundary fixtures now; sanitized controlled packets later | production equality remains unproven until exact staging evidence exists | `protocol-canary-chat` |
| combat | 7 | 7 | 0 | synthetic-plus-controlled | project-original malformed/boundary fixtures now; sanitized controlled packets later | production equality remains unproven until exact staging evidence exists | `protocol-canary-combat` |
| containers | 21 | 21 | 0 | synthetic-plus-controlled | project-original malformed/boundary fixtures now; sanitized controlled packets later | production equality remains unproven until exact staging evidence exists | `protocol-canary-containers` |
| economy | 34 | 34 | 0 | feature-gated-controlled | project-original negative fixtures plus controlled enabled-feature evidence | do not treat source declaration as configured release requirement | `protocol-canary-economy` |
| entity | 36 | 34 | 2 | synthetic-plus-controlled | project-original malformed/boundary fixtures now; sanitized controlled packets later | production equality remains unproven until exact staging evidence exists | `protocol-canary-entity` |
| items | 23 | 23 | 0 | synthetic-plus-controlled | project-original malformed/boundary fixtures now; sanitized controlled packets later | production equality remains unproven until exact staging evidence exists | `protocol-canary-items` |
| map | 12 | 10 | 2 | synthetic-plus-controlled | project-original malformed/boundary fixtures now; sanitized controlled packets later | production equality remains unproven until exact staging evidence exists | `protocol-canary-map` |
| modern | 24 | 21 | 3 | feature-gated-controlled | project-original negative fixtures plus controlled enabled-feature evidence | do not treat source declaration as configured release requirement | `protocol-canary-modern-features` |
| movement | 20 | 20 | 0 | synthetic-plus-controlled | project-original malformed/boundary fixtures now; sanitized controlled packets later | production equality remains unproven until exact staging evidence exists | `protocol-canary-movement` |
| operational | 7 | 7 | 0 | not-release-fixture-by-default | unit-only source-shape tests unless product/operations explicitly authorize more | avoid staff/admin data and operational credentials | `protocol-canary-operational` |
| player | 7 | 5 | 2 | synthetic-plus-controlled | project-original malformed/boundary fixtures now; sanitized controlled packets later | production equality remains unproven until exact staging evidence exists | `protocol-canary-player` |
| progression | 34 | 34 | 0 | feature-gated-controlled | project-original negative fixtures plus controlled enabled-feature evidence | do not treat source declaration as configured release requirement | `protocol-canary-progression` |
| social | 19 | 19 | 0 | feature-gated-controlled | project-original negative fixtures plus controlled enabled-feature evidence | do not treat source declaration as configured release requirement | `protocol-canary-social` |
| unclassified | 59 | 55 | 4 | manual-review-required | no fixture package until source ownership and exact layout are resolved | unclassified methods cannot be guessed from neighboring opcodes | `protocol-canary-unclassified-review` |

## Provenance rules

1. Synthetic fixtures must be project-original and describe the exact source anchor they exercise.
2. Controlled runtime fixtures require an approved staging environment, disposable identity and explicit retention/redaction policy.
3. Never commit credentials, session secrets, private captures or proprietary asset bytes.
4. A method declaration or literal opcode proves source shape only; it does not prove deployment, configuration, ordering or product requirement.
5. Re-generate this index from the pinned producer revision and require byte-identical output before accepting an update.

## Suggested fixture identifiers

- `bootstrap`: `canary-1525-bootstrap-a60b909ef1fa` — metadata key only; no packet bytes embedded.
- `chat`: `canary-1525-chat-47a439340b2f` — metadata key only; no packet bytes embedded.
- `combat`: `canary-1525-combat-cb7b267b97f9` — metadata key only; no packet bytes embedded.
- `containers`: `canary-1525-containers-b48982bf5950` — metadata key only; no packet bytes embedded.
- `economy`: `canary-1525-economy-1242abd90eb0` — metadata key only; no packet bytes embedded.
- `entity`: `canary-1525-entity-540eed13c676` — metadata key only; no packet bytes embedded.
- `items`: `canary-1525-items-260affc5fe74` — metadata key only; no packet bytes embedded.
- `map`: `canary-1525-map-5d8ceb20bd0d` — metadata key only; no packet bytes embedded.
- `modern`: `canary-1525-modern-08b9b79b6fa9` — metadata key only; no packet bytes embedded.
- `movement`: `canary-1525-movement-0e4691e23162` — metadata key only; no packet bytes embedded.
- `operational`: `canary-1525-operational-75da59244c3f` — metadata key only; no packet bytes embedded.
- `player`: `canary-1525-player-61825a1471c6` — metadata key only; no packet bytes embedded.
- `progression`: `canary-1525-progression-a0c751f25c45` — metadata key only; no packet bytes embedded.
- `social`: `canary-1525-social-9b4618b89a04` — metadata key only; no packet bytes embedded.
- `unclassified`: `canary-1525-unclassified-acc2313cc8f2` — metadata key only; no packet bytes embedded.
