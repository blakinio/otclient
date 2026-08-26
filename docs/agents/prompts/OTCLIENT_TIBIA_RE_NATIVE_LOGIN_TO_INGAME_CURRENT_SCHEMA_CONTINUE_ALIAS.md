# OTCLIENT-TIBIA-RE native login-to-ingame current-schema continuation alias

```yaml
alias_prompt_contract_version: 1.0.0
prompting_standard_version: 2.1
execution_policy_version: 2
alias: OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME-CURRENT-SCHEMA-CONTINUE
repository: blakinio/otclient
track_id: official-client-re
lane: P2-NETWORK
risk: high
run_scope: existing_current_login_schema_task_then_track_b_consumer
continuation_policy: continue_until_real_stop
task_completion_policy: promote_archive_then_consume_if_evidence_complete
user_communication: low_noise
direct_codex_spark_authorized_if_current_root_governance_still_allows_native_login_family: true
direct_codex_spark_model: gpt-5.3-codex-spark
owner_funded_ai_api_authorized: false
```

Owner invocation:

```text
Kontynuuj OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME-CURRENT-SCHEMA-CONTINUE autonomicznie.
```

or simply:

```text
OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME-CURRENT-SCHEMA-CONTINUE
```

## Role and source of truth

You are the fresh continuation agent for the existing native-login programme. Do not reconstruct state from chat history and do not restart discovery that already has durable evidence.

Live GitHub/repository state always wins. Historical SHAs below are only anchors for locating the correct work.

At startup read current versions of:

```text
AGENTS.md
docs/agents/README.md
docs/agents/PROMPTING_STANDARD.md
docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
docs/agents/TASK_CLOSEOUT_AUDIT_E2E.md
docs/agents/TRUST_AND_CONTEXT_BOUNDARIES.md
docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME.md
docs/agents/tasks/active/OTC-20260826-current-game-login-schema.md
docs/agents/evidence/OTC-20260826-current-game-login-schema/20260826-current-game-login-schema.md
```

Also resolve from live GitHub:

- protected `main` and its exact SHA;
- PR #711, its exact head, state, changed files, CI/governance and reviews;
- merged Track A current wire-writer promotion/closeout #706/#707;
- Track B PR #284 and its current task/checkpoint/canonical prompt;
- any newer task/PR that supersedes #711 or owns overlapping prompt/evidence paths.

If live state differs from the anchors below, live state wins.

## Continuation anchors at prompt creation

```text
main observed: 8c7bc507aa5c1118aca0b8252dc422675add1be0
source task: OTC-20260826-current-game-login-schema
source PR: #711
source branch: research/OTC-20260826-current-game-login-schema
source evidence-producing head: d24b6e61d1086094112020db6e7d959c24bdb34a
final static producer run: 33017207072 = SUCCESS
job: 98338388458
artifact: 9625060590
artifact digest: sha256:be50b5baf632095f3eccc90aad6b0b9ff409d3dac626c8580b35deb36b245a74
result.json sha256: 1940d58a7fcb2615da7f9d47179e6dbdf41397f89b8b522af52da75b076154dc
```

Exact current client fence proven by that producer:

```text
version: 15.32.75d4a0
packed sha256: 075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
unpacked sha256: d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
unpacked size: 52105824
```

Safety markers: `runtime_access:none`, no official-client execution, no login, no credential/session read, no process-memory access and no raw proprietary client upload.

## Current proven schema

For the exact build above, current generated protobuf ABI is behaviorally identified as:

```text
+0x10 Clear-equivalent
+0x18 ByteSizeLong-equivalent
+0x28 _InternalSerialize-equivalent
+0x30 zero / end of current class vtable
```

`GameclientMessageLogin` current wire shape:

```text
field 1: varint           storage +0x30  tag 0x08
field 2: varint           storage +0x34  tag 0x10
field 3: varint           storage +0x38  tag 0x18
field 4: length-delimited storage +0x18  tag 0x22
field 5: length-delimited storage +0x20  tag 0x2a
field 6: varint           storage +0x3c  tag 0x30
field 7: embedded message storage +0x28  field number 7
```

Current field 7 is directly proven as `LoginRSAEncryptedBlock`: `GameclientMessageLogin::ByteSizeLong` at `0x17728a0` calls current `LoginRSAEncryptedBlock::ByteSizeLong` at `0x1772740` on `[this+0x28]`.

`LoginRSAEncryptedBlock` current wire shape:

```text
field 1: length-delimited storage +0x18 tag 0x0a
field 2: length-delimited storage +0x20 tag 0x12
field 3: varint           storage +0x40 tag 0x18
field 4: varint           storage +0x44 tag 0x20
field 5: length-delimited storage +0x28 tag 0x2a
field 6: length-delimited storage +0x30 tag 0x32
field 7: length-delimited storage +0x38 tag 0x3a
```

Current producer identity is also proven:

```text
TLoginProtocolMessageHandler
  RTTI 0x30b4ed0
  vtable AP 0x30b6700
  slot +0x60 -> 0xe25620
  producer FDE 0xe25620..0xe2656d

TAuthenticationAndEncryptionInfo
  RTTI 0x30adc40
  vtable AP 0x2f82f98
```

The producer FDE references both current primary protobuf vtables and binds `[handler+0x10]` to current `TAuthenticationAndEncryptionInfo` through matching current virtual targets. Do not rename retained fields to password/session semantics without causal proof.

## Required continuation sequence

### 1. Freeze and verify source PR #711

Treat the source researcher branch as evidence-producing only. Re-download and hash the final artifact from the exact live source head. Verify exact current package identity, unique RTTI/vtables/current generated ABI, exact wire tags/storage/nested field 7 identity, current producer/owner-slot identity, safety markers, full changed-file scope, checks, reviews and path ownership.

If source evidence changed after the anchors above, audit the new exact artifact instead of trusting these anchors.

Do not merge the research workflow/analyzer merely because its result is accepted. Follow the established #699 -> #706 -> #707 pattern unless current governance requires a newer equivalent.

### 2. Independent coordinator promotion

Use a fresh independent validator/coordinator role. Do not use the researcher summary as proof. Promote only independently verified sanitized facts to a docs/evidence PR based on current protected `main`.

Preserve as `UNKNOWN` unsupported semantic field names, password/session-token mapping, final causal explanation of Track B `0x14`, or other unproven producer semantics.

After promotion reaches trusted `main`, close #711 unmerged as superseded/consumed if that remains the repository convention, archive the task, release ownership and make all related PRs terminal.

### 3. Consume promoted result in Track B only after trusted-main promotion

Re-resolve PR #284, its exact head, current task record and canonical Track B continuation prompt. Do not assume `2d105c95...` is still current.

Promoted current wire-writer evidence already rejects changing generic outer padding/XTEA/sequence/framing as the next hypothesis. The current-schema source establishes a structural mismatch before that generic layer: official current login is a generated `GameclientMessageLogin` with nested `LoginRSAEncryptedBlock`, while Track B `ProtocolGame::sendLoginPacket()` still constructs the legacy raw pending-game/RSA body.

Do **not** implement a protobuf replacement merely from field wire types. Before mutating Track B, prove how every required current field value can be sourced from Track B's already-authorized inputs/current handoff without inventing semantic names. If one required field value remains unproven, run at most one bounded static provenance discriminator or stop with the exact first unproven boundary.

If and only if promoted evidence fully determines a concrete payload delta:

1. implement only that login-specific delta in PR #284;
2. keep generic outer framing unchanged unless newer promoted evidence disproves it;
3. add focused TDD/contract tests first;
4. update Track B durable evidence/task checkpoint;
5. permit at most one new bounded official-service E2E generation after all canonical preconditions are revalidated.

Never perform an identical retry of the already rejected packet. A new E2E is legal only after a material evidence-derived payload change.

## Safety and authority

The schema source task remains `runtime_access:none`. This alias does not itself grant Track A runtime ownership, credentials, login/session budget, process-memory access, packet capture, mutation authority or Track B secret-ingress authority.

Never print/store/commit Tibia credentials, session keys, cookies/devicecookies or play-session secrets. Never upload raw proprietary official-client binaries/assets. Never use Remote Desktop Commander as secret ingress.

For this exact native-login alias family, direct use of exactly `gpt-5.3-codex-spark` is allowed only if the **current** root `AGENTS.md` still contains the standing native-login exception. Spark may inspect repository code/diffs and sanitized evidence only. Never send Spark credentials, session material, process-memory/packet secrets or raw proprietary client binaries. Do not fall back to another model/provider or owner API key.

## Anti-loop rules

- Do not rerun Gen1/Gen2 failures; they were workflow-boundary/substring-locator defects already repaired.
- Do not rerun the same successful Gen5 producer merely to get another artifact.
- Do not translate historical `df7b29` addresses into the current build.
- Do not feature-toggle guess after structured `0x14`.
- Do not modify Track B before trusted-main promotion of the exact evidence used for that mutation.
- Keep ordinary repair cycles within current repository anti-stall budgets.

## Terminal outcomes

`DONE` requires the current-schema source to be independently promoted and archived, and either a fully evidence-derived Track B payload change is implemented/validated and the canonical task reaches its next legal terminal point, or the exact remaining payload-value provenance blocker is durably recorded with no safe work remaining under this alias.

Do not claim `GAME_START`/`IN_GAME` unless a new legally admitted E2E actually proves it.

## Final response contract

```text
STATUS=DONE|BLOCKED|WAITING|ROTATE
SOURCE_TASK=OTC-20260826-current-game-login-schema
SOURCE_PR=<live #711 disposition>
PROMOTION=<pr/merge or NONE>
FINAL_MAIN=<sha>
TRACK_B_PR=<live #284 state/head>
SCHEMA_PROMOTED=true|false
TRACK_B_PAYLOAD_DELTA=IMPLEMENTED|BLOCKED_UNPROVEN_VALUES|NOT_YET_LEGAL
NEW_E2E_ATTEMPTED=true|false
GAME_START=true|false|NOT_ATTEMPTED
IN_GAME=true|false|NOT_ATTEMPTED
BLOCKER=<exact blocker or NONE>
NEXT_ACTION=<exactly one action or NONE>
```
