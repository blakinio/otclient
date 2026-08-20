# Surveyor player-state current-build static resolver evidence

Date: 2026-08-20
Task: `OTC-20260820-surveyor-player-state-reader`
Exact client fence: `15.32 / 52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`

## FACT — current-build rediscovery

A fresh read-only static pass over the exact current ELF on the owner-controlled Synology runtime reproduced the player-state candidate without importing historical #302 addresses:

```text
STATIC_RESOLVER=PASS
VPTR=0x30c1810
METACAST=0xd40470
POSITION_XREF=0x82d101
OFFSETS=0x78,0x7c,0x80
MATCH_CURRENT=True
```

The resolver correlates the exact `tibia::game::TPlayerData` / mangled RTTI strings, `qt_metacast` xref, ELF `R_X86_64_RELATIVE` vtable/typeinfo relationships, the exact `playerPosition` xref, and the three adjacent signed `movslq` loads. Ambiguous or missing relationships fail closed.

## FACT — deterministic validation

```text
python3 -m compileall -q tools/tibia_re_surveyor tests/tools/tibia_re_surveyor
PYTHONPATH=. python3 -m unittest discover -s tests/tools/tibia_re_surveyor -p "test_*.py" -q
Ran 30 tests
OK
git diff --check = PASS
```

A real repository-only collect-all after integration emitted:

```text
ROWS=169
ALIASES=12
MISSING_TYPED_READERS=10
PLAYER_STATE_GAP_PRESENT=false
PLAYER_STATE_READER_STATE=UNAVAILABLE
PRIVACY=PASS
```

`UNAVAILABLE` is expected without runtime input; implementation presence is distinct from semantic proof.

## Promotion boundary

The current fields remain `CANDIDATE_PENDING_CAUSAL_E2E`. This static evidence does not establish authoritative local-player XYZ. Post-merge physical read-only differential E2E must show that the reader changes exactly when the owner moves the already-logged-in character. No agent-generated input, login/logout, restart, process control, process-memory write, injection, credentials, transactions or local model use occurred.
