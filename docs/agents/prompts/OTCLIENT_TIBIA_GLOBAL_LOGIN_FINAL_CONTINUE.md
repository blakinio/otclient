# OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous Track B coordinator with optional local Vision post-processing in the same invocation.

## Owner-facing behavior

This alias is deliberately single-window. Resolve and continue Track B yourself; if accepted secret-safe visual evidence becomes available, run the local Vision/Qwen post-processing yourself in the same invocation. **do not ask the owner to open a second chat/window** and do not ask the owner to start `TIBIA-RE-VISION-BENCHMARK` separately.

Vision is a merged helper capability, not a second owner-operated programme. Use `tools/tibia-re-vision-benchmark` from fresh trusted `main` as the canonical local harness implementation.

## Fresh-state recovery

1. Re-read `docs/agents/TIBIA_RESEARCH_TRACKS.md` from current trusted `main`.
2. Resolve live PR #284. While it remains active, read `docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md` from its exact live head branch; if PR #284 is terminal or superseded, follow the replacement state recorded in the repository.
3. Revalidate current `main`, Track B head, changed paths, checks, evidence, runtime ownership and exact `next_action`; do not trust stale SHA/run values from this prompt or chat.
4. At the time this coordinator was introduced, the Track B stop was `BLOCKED_REQUIRED_CURRENT_NATIVE_PRE_LOGIN_OUTBOUND_SEQUENCE_EVIDENCE`. Treat that token as historical orientation only: live repository state wins if it has advanced.
5. Continue structural Track B work first. Do not spend a service E2E until the live Track B contract independently permits a materially evidence-derived attempt.

## Non-negotiable Track B authority boundary

- Track B structural/runtime evidence remains the only authority for protocol mutation, login acceptance and `IN_GAME` conclusions.
- Vision output is always `visual_only` and `structural_authority:false`.
- Vision cannot prove native `GameclientMessage*` ordering, the queue/TCP serializer, packet field order/types/widths, server acceptance, `GAME_START`, or authoritative world state.
- A visual observation may rank or annotate hypotheses only after those hypotheses are already legal under Track B evidence.
- Never trigger or repeat an official-service E2E merely to obtain screenshots.
- Never convert absence of screenshots, local-model-host downtime, or Vision failure into authority for another E2E.

## Single-window Vision policy

Evaluate this policy after every independently legal, materially changed Track B E2E and also when resuming from an already-existing accepted visual handoff.

### Case A — no accepted keyframes

If no accepted secret-safe keyframes exist, record:

`VISION_POST_E2E=SKIPPED_NO_ACCEPTED_KEYFRAMES`

Then continue structural Track B work. Vision absence is not a Track B blocker and must not cause an E2E retry.

### Case B — accepted keyframes exist

Accepted input is a bounded set from the same Track B experiment, preferably:

1. pre-attempt frame after credential/session material is no longer rendered or exposed;
2. first post-attempt visible-state-change frame, if one exists;
3. terminal error/success frame.

Every frame must have a non-secret order/timestamp marker and a content SHA-256. Reject/quarantine frames that may contain account credentials, 2FA values, auth/session tokens, cookies, secret-bearing debug overlays or other protected secret material. Do not commit or upload plaintext rejected frames.

When the accepted set exists, record:

`VISION_POST_E2E=RUN_QWEN`

and execute the Vision pass yourself before asking the owner for any separate action.

### Local Vision execution

1. Use the fresh trusted-main implementation under `tools/tibia-re-vision-benchmark`; do not copy an old harness from a stale Track B branch.
2. Use the bounded local Qwen leading profile first: `qwen3-vl:4b-instruct-q4_K_M`, `num_ctx=4096`, `num_predict=256`, `temperature=0`.
3. Revalidate the installed model digest against the current durable benchmark report/evidence before inference; do not silently accept a different model or quantization.
4. Use loopback-only local inference and one-model residency. No cloud/API/provider fallback.
5. Bind every frame manifest hash to actual image bytes before inference and preserve the trusted capture/model/authority metadata outside model-authored output.
6. Require strict VisualEvidence schema. Do not repair malformed model JSON into a pass.
7. Explicitly unload/release the owned model after the bounded pass and verify the local model slot is empty.
8. Do not persist chain-of-thought or secret-bearing raw visual content in GitHub evidence.

If the authorized local model host is unavailable, record:

`VISION_POST_E2E=BLOCKED_LOCAL_MODEL_HOST_UNAVAILABLE`

Do **not** ask for another login/E2E and do not ask the owner to switch windows. Persist the visual-postprocessing blocker if useful, then continue structural Track B work wherever independent progress remains possible.

## Visual correlation output

For each accepted frame, preserve only non-authoritative VisualEvidence such as:

- screen class: `LOGIN_SCREEN`, `CHARACTER_SELECT`, `IN_GAME_VISUAL`, `WORLD_EXIT`, `OTHER`, or `UNKNOWN`;
- clearly visible non-secret text;
- visible UI objects;
- appeared/disappeared/changed UI descriptions;
- capture order/timestamp/hash and exact model profile identity supplied by the trusted harness.

Correlate those observations with existing non-secret Track B markers from the *same* experiment. Examples of useful correlation are "no visible transition despite outbound send", "terminal compatibility popup appeared after server response", or "visual world-entry transition followed a structurally proven login-success boundary". These are diagnostic correlations, not wire truth.

## Research-value measurement

When representative real keyframes finally exist, compare structural-only analysis with structural-plus-VisualEvidence for the same evidence set. Measure where possible:

- hypotheses considered before the next valid structural discriminator;
- false hypotheses rejected;
- additional E2Es avoided;
- analysis steps or elapsed time reduced.

If those measurements are unavailable, report `VISION_RESEARCH_VALUE=INCONCLUSIVE` rather than inventing a percentage benefit.

## Current benchmark facts to preserve unless superseded

The merged benchmark concluded `PARTIAL`, with no formal primary/fallback promotion because representative Track B screenshots were unavailable. Qwen was the leading tested profile; OvisOCR2 reproduced false text on a black no-text control; Ovis2.5-2B was unsupported on the tested Windows AMD exact-profile path. Always re-read the current benchmark report on trusted `main` before relying on these facts.

## Autonomous continuation order

1. Recover exact live Track B state and current blocker.
2. Continue the structural/native outbound-sequence investigation without waiting for Vision.
3. If a material protocol delta is promoted and the existing Track B contract permits one bounded E2E, execute only that legal E2E under its existing authority/safety budget.
4. In that same E2E, accept visual keyframes only if they can be obtained without expanding credential/login/gameplay authority or creating a second attempt.
5. In the same invocation, apply the Vision policy above automatically.
6. Feed only diagnostic VisualEvidence back into hypothesis ranking; never let it authorize protocol mutation.
7. Continue until Track B reaches its genuine terminal success/blocker boundary. Persist exact evidence and `next_action` before stopping.

## Required final status fields

Every invocation using this alias should report at least:

```text
TRACK_B_STATUS=<live result>
TRACK_B_BLOCKER=<live blocker or none>
VISION_POST_E2E=SKIPPED_NO_ACCEPTED_KEYFRAMES|RUN_QWEN|BLOCKED_LOCAL_MODEL_HOST_UNAVAILABLE|SKIPPED_REJECTED_SECRET_RISK|NOT_APPLICABLE
VISION_RESEARCH_VALUE=POSITIVE|NEGATIVE|INCONCLUSIVE|NOT_MEASURED
VISION_AUTHORITY=visual_only/structural_authority:false
NEXT_ACTION=<one concrete repository-owned continuation step or none>
```

Evidence before claims. Do not stop for routine recoverable failures; debug autonomously within the current Track B authority until success or a genuine safety/authority/external blocker.
