# Surveyor action-protocol typed reader — physical read-only acceptance

Date: 2026-08-21

Task: `OTC-20260821-surveyor-action-protocol-reader`

## Result

**PASS**

The action-protocol typed reader was accepted on the physical official-client runtime through the trusted-main, bounded read-only Surveyor `--collect-all` path. The accepted semantics prove exactly one live `tibia::game::TPlayerProtocolMessageHandler` object identity only; they do not prove action-to-protocol linkage, opcodes, packet contents, payload semantics, or `IN_GAME` state.

## Implementation and repair chain

- implementation PR: #645; merge `f80dd43f741c39ce5ee4296396cb07891d04c324`
- read-only acceptance workflow PR: #646; merge `b7fa88ef2d772c70ca7250b587e7f584327ee37b`
- pure-Python ELF resolver repair PR: #648; merge `dbc05824fb539a5dfffb0bd8cb48dbfb3a9a01e1`
- bounded live-diagnostics repair PR: #652; merge `53485c70f2532faa7588afc788f53cc67813b121`
- measured action-only RW bound repair PR: #654; merge `a28550bf5ad0880d947aa2ebc2de13f438cef6bd`
- final request-only trigger PR: #653; closed without merge after evidence capture

The final repair kept the generic typed-presence aggregate RW scan ceiling at 1536 MiB and raised only the action-protocol wrapper ceiling to 2 GiB after the exact runtime measured 468 eligible writable mappings totaling `1934311424` bytes. A pre-merge one-shot exact-fenced `O_RDONLY` scan with the 2 GiB ceiling produced `RAW_VPTR_COUNT=1` and `FILTERED_COUNT=1` without retaining addresses or memory bytes.

## Final physical run

- workflow run: `32514243771`
- authority job: PASS
- acceptance job: `96872176204`, PASS
- trusted main: `a28550bf5ad0880d947aa2ebc2de13f438cef6bd`
- artifact: `9458204826`
- artifact name: `track-a-surveyor-action-protocol-postmerge-32514243771`
- artifact size: `46135` bytes
- artifact digest: `sha256:1368e91ee2206f050d253775f0a607f3c14c5e741721337f552231ccf8c92e5e`

The self-hosted job checked out the exact pull-request base SHA and executed no PR-head code.

## Fresh exact target identity

- target container: `otclient-track-a-kasmvnc`
- display: `:1`
- exact client processes in namespace: `1`
- matching visible Tibia windows: `1`
- target uniqueness: `PROVEN`
- PID: `19590`
- process start ticks: `76611792`
- executable path: `/home/kasm-user/otclient-track-a/Tibia-32177065988-1/bin/client`
- executable size: `52109920`
- SHA-256: `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`

Canonical control-plane state during admission remained non-conflicting: lease generation `19` was released/expired, canonical registration was present and identity-matching, registration generation was `2`, and registration lease generation was `19`.

## Live reader acceptance

Physical `--collect-all` result:

- canonical rows: `169`
- aliases: `12`
- runtime admission: `READ_ONLY_ADMITTED`
- missing typed readers after: `8`
- privacy: `PASS`
- reader: `action_protocol_typed_reader=AVAILABLE`
- type: `tibia::game::TPlayerProtocolMessageHandler`
- object count: `1`
- typed object identity: `PROVEN`
- process memory access: `read_only`
- semantic state: `TYPED_ACTION_PROTOCOL_OBJECT_IDENTITY_ONLY`
- vptr offset: `0x30bf620`
- typeinfo offset: `0x30bf298`
- `action_to_protocol_connection_claimed=false`
- `serialized_message_semantics_claimed=false`
- `protocol_opcodes_claimed=false`
- `packet_payloads_retained=false`
- `in_game_claimed=false`
- `semantic_promotion_allowed=false`
- runtime mutation: `false`

Causal implementation delta: reader `NO_TYPED_READER_IMPLEMENTED -> AVAILABLE`, missing readers `9 -> 8`, privacy `PASS -> PASS`.

## Safety evidence

The final physical run declared and enforced: credential access false, GUI input false, process control false, process-memory write false, network mutation false, runtime mutation false, and PR-head code execution false. No login/logout/relogin, character selection, movement, inventory manipulation, attack, trade, economy action, client/container restart, attach/debug/injection, target-network mutation, or local-model execution was performed.

This evidence closes only the action-protocol typed-reader slice. Broader action semantics and the remaining eight Surveyor typed-reader gaps remain outside this task.