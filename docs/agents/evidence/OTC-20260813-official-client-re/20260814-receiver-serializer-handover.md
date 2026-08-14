# Track A — receiver/serializer continuation handover

Date: 2026-08-14
Track: Track A / `official-client-re`
Repository: `blakinio/otclient`
Task: `OTC-20260813-official-client-re-continuation`
Branch: `ci/OTC-20260813-official-client-re-continuation`
PR: #289

## Live-state verification at handover

FACT:

- PR #289 is open and remains a draft.
- PR base is `main` and head branch is `ci/OTC-20260813-official-client-re-continuation`.
- Exact PR head observed immediately before this checkpoint: `89827b7b182654ef8a696d63bc54724f77be5162`.
- The active task record still contains older embedded recovery/context heads; those values are historical checkpoints and must not be treated as the current PR head without re-verification.
- GitHub combined-status lookup for the exact head returned no legacy commit statuses. This is not evidence that Actions checks passed or failed; workflow/check state must be inspected independently before any completion claim.

## Verified outbound GameAction facts

The following existing evidence remains authoritative for the exact pinned official Linux client binary:

- `20260814-gameaction-qmeta-dispatch-map.md`
- `20260814-high-value-outbound-signal-disassembly.md`

FACT:

- Exact QMeta method-to-executable case mappings were recovered for six high-value outbound actions:
  - `TCreaturesGameActionHandler::sendAttack`
  - `TCreaturesGameActionHandler::sendFollow`
  - `TChatGameActionHandler::sendTalkMessage`
  - `TContainerGameActionHandler::sendMoveObject`
  - `TPlayerTradeGameActionHandler::sendTradeObject`
  - `TWorldMapGameActionHandler::sendMoveObject`
- Their mapped QMeta case entries are signal-emission wrappers which call `QMetaObject::activate`; they are not direct protocol serializers.
- Exact signal indices/static metaobjects are already preserved in `20260814-high-value-outbound-signal-disassembly.md`.
- The previously suspected Player common tail at `0xd1abc0` is only an epilogue (`add rsp,0x38; ret`) and must not be labeled a serializer/network sender.

## What is not proven yet

UNKNOWN / NOT YET PROVEN:

- connected receiver/slot identity for each high-value GameAction signal;
- concrete receiver executable function for each action;
- protocol message-builder entry point downstream of each receiver;
- serializer entry point;
- wire opcode/message ID;
- field layout and serialization order;
- final socket/network-send function;
- full receiver -> builder -> serializer -> wire/runtime chain for movement, `MoveObject`, `Attack`, `Follow`, `Talk`, and `TradeObject`.

Do not promote QMeta names, signal indices, string proximity, nearby disassembly, common tails, or protocol message names into any of the unknown items above without structural evidence.

## Current acceptance implication

FACT:

The active task acceptance item:

`Outbound builder/serializer entry points are recovered for movement, MoveObject, Attack, Follow, Talk and TradeObject`

is not satisfied by the currently verified QMeta/signal evidence alone.

The Track A task and PR therefore must remain non-terminal until the required receiver/serializer evidence and any other outstanding acceptance/runtime gates are actually proven and final validation is green on the exact final head.

## Next action

Recover the Qt signal-to-receiver mapping for the already proven GameAction signal emitters, beginning with the bounded `connectImpl` candidate set already produced by prior experiments. For each candidate, structurally reconstruct sender/static-metaobject, signal index/pointer, receiver object source, slot-object/function target and connection type. Explicitly classify unresolved candidates. Once a receiver slot is proven, follow that exact executable path to message construction, serializer and network/wire convergence rather than following adjacency heuristics.

## Evidence discipline

- Preserve exact binary/version fencing from the existing Track A evidence.
- Static-only evidence must be labeled static-only.
- Runtime claims require direct runtime evidence and must not be inferred from static disassembly.
- A workflow output is not promoted as PASS unless its relevant job/run actually completed successfully.
- Before task closeout, re-read live PR head, Actions/check state, reviews, outstanding acceptance inventory and task lifecycle state.
