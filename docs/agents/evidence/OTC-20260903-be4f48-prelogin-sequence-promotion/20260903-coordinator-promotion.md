# Coordinator promotion — be4f48 pre-login sequence / writer discriminator

Decision: **SOURCE_BLOCKER**.

This clean promotion is reconstructed from fresh trusted `main@05a0befa9670b164e5d88046584899ae3aaebb29`, frozen source Draft PR #865 and the already-existing exact-current writer evidence. The source analyzer/workflow is not promoted.

## Exact evidence

```text
source PR             #865
source head           8d6c752cd3d009a78b5deddb650c752c95156298
source workflow       33756449924 = SUCCESS
source job            100651924970 = SUCCESS
source CI             33756450210 = SUCCESS
source governance     33756449991 = SUCCESS
source boundary       33756449971 = SUCCESS
source artifact       9893838828
artifact sha256       20043e76288cf7377c480015a1c2726fb76f39fd1366e43faae445c3bfd87cee
result.json sha256    c44a1cdd3f20a84da4ca3c8ec6970a0dc86ef46c89ee8cd348db7d46729a2d37

writer run             32998976901 = SUCCESS
writer head            3d87d729b73f868aefe1662c72af666a4921b1d8
writer artifact        9886703883
writer artifact sha256 84e88080ea862d2faf82fc169dde5f908fc5fd7a856585e434523795481fc4fa
writer result sha256   296f5a915d15f9383fc3f1c7809eb5c6934a3deb24a9e2b9cd1808b660c40f14
```

Exact public Linux client is `15.32.be4f48`, SHA-256 `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`, size `52105824`. Analysis was static only; the official client was never executed and no login, credentials/session material, process-memory access, packet capture or raw-client upload occurred.

## Accepted producer facts

The exact-current primary producer constructs `tibia::protobuf::protocol::GameclientMessageLogin` with outer fields `1`, `2`, `3` and **`6`** present. Field 6 is written at `0xe25ccc` from `r14d`; the exact-current source analysis binds the defining move to producer entry `mov r14d, edx @ 0xe25624`.

This proves structural presence and producer-input provenance only. It does **not** prove the exact value passed in `edx` or a user-facing semantic name. `field6_value=UNKNOWN` remains mandatory.

The same exact-current producer structurally references nested `LoginRSAEncryptedBlock` source slots for fields `1`, `2`, `5`, `6` and `7`. These source references do not prove non-empty runtime values or semantic names.

## Accepted sendLogin binding facts

Exact-current `tibia::protocol::TProtocolMessageQueue::sendLogin` is QMeta index `196`, target `0xde82a2`, and is on the non-signal method side (`signal_count=192`). Its QMeta body has one external tail transfer:

```text
0xde82ae -> 0xbd3050
```

The adapter FDE is `0xbd3050..0xbd34dd`. The exact-current writer run independently derives the same QMeta target/edge/FDE and proves adapter indirect calls, so this binding is independently falsified.

The unique instruction-aligned RIP reference to the adapter is `0x7c6b34` in owner FDE `0x7c6700..0x7cc933`.

## Connection-block falsification

A fresh discriminator derived the current connection block without hardcoding the observed addresses. It recovered:

```text
adapter reference     0x7c6b34
adapter target        0xbd3050
peer target           0xd052a0
connection helper     0x4d8670
object-field candidate +0x88
object-field candidate +0x9c0
```

The endpoint census also found an `rsp+0x20` stack temporary, so the connection block remains fail-closed as `UNKNOWN_ENDPOINT_PAIR` rather than manufacturing a unique endpoint pair.

More importantly, the peer target has:

```text
peer_qmeta_candidates=[]
peer_qmeta_role=UNKNOWN
bounded_gameclient_root_reachability=UNKNOWN_PEER_QMETA_IDENTITY
```

Therefore the source evidence does **not** prove a `TGameClient` signal/method identity or causal sender-side event for `sendLogin`. The original direct-call bounded graph also remains:

```text
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
proved_send_methods=[]
```

## Independent final writer boundary

The separate exact-current writer evidence classifies:

```text
current_sendlogin_qmeta=PROVEN
current_sendlogin_first_direct_edges=PROVEN
current_sendlogin_adapter_fde=PROVEN
current_sendlogin_adapter_indirect_calls=PROVEN
final_writer_contract=UNKNOWN
```

It does not uniquely identify the final queue/TCP writer contract. Discovery-only TCP/QMeta candidates and generic writer-slot references are not promoted into a final wire contract.

## Track B consequence

This evidence cut proves a real structural difference: the native exact-current producer contains outer `GameclientMessageLogin.field6`, while the current Track B implementation does not have a proven exact-current value for such a field. But a structural mismatch without the value and without complete sender/writer ordering is not an implementable payload delta.

Therefore this promotion **does not authorize** a Track B payload mutation or another official-service game E2E. PR #284 remains unchanged.

```text
PRE_LOGIN_SEQUENCE_COMPLETE=false
PRE_LOGIN_MESSAGE_ORDER=UNKNOWN
PRE_LOGIN_REQUIRED_MESSAGE_MISSING_IN_OTCLIENT=UNKNOWN
FIELD6_PRESENT=true
FIELD6_SOURCE=producer input edx
FIELD6_VALUE=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=exact-current sender-side native event/peer identity and direction for the connection that binds TProtocolMessageQueue::sendLogin
SECONDARY_MISSING_BOUNDARY=sendLogin serialized queue object -> final queue/TCP writer contract
```

Do not relaunch this analyzer with broader BFS, historical literals, guessed values or new architecture. A future task is justified only by a new concrete discriminator capable of proving one of the missing boundaries above.
