# Coordinator promotion of source PR #904

Trusted main: 04a4ca71b658dcc374aaf40dbb8135de43d49cb7. Protected main ruleset18840974 active; squash-only, CI / Required, resolved threads, no bypass.

Source PR904 head 191a8ff86f1b354d313a95e6901e9c7abcd389d8; analyzer/tests/workflow scientific head4d7669970b4dc54829e29887ae6d60c76b73579b. Exact fence15.32.be4f48 /52105824 /552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1 requalified on final head.

## FACT

Selected connection at0x7c6b9f constructs QSlot dispatcher0x7c4f10 with member pair{0xbd3050,0}. Given operation edi=1 and the constructed slot in rsi, entry rdx reaches adapter rdi unchanged, and [entry rcx+8] reaches adapter rsi. This is conditional invocation ABI, not evidence of external Qt's receiver argument selection.

Under the analyzer's modeled normal returning paths, adapter0xbd3050 reaches its first same-entry-receiver edge at0xbd31e4, target load64(add(load64(arg:rdi),0x68)). No concrete dynamic vptr or member implementation is identified.

The selected QObject::connectImpl symbol is an undefined dynamic import in this executable. This does not establish absence of all Qt implementation code.

## INFERENCE

Connecting this conditional invocation to the proven +0x88 registered receiver requires an exact deployed-Qt registration-to-invocation proof. A generic/historical Qt ABI description is insufficient. A resolved vptr/member also requires a distinct identity-preserving proof.

## UNKNOWN

Receiver class/identity, complete sender-receiver pair and causal binding remain unproven. Queue endpoint, final queue/TCP writer, writer contract, Field6 value and pre-success ordering remain UNKNOWN. TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN; PR284 unchanged at62383aded3acbeb5f405a12fe1f93849cd8e35f9. No implementation or E2E unlocked.

terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=CURRENT_QT_REGISTERED_RECEIVER_TO_QSLOT_ENTRY_RDX_NOT_PROVEN

## Independent coordinator falsification

Coordinator independently read the complete analyzer, result and diff; rejected equating the imported connection receiver with the conditional QSlot input, equating vptr+0x68 with a concrete writer, and treating analysis incompleteness as a scientific blocker. Independent Codex reviewer /root/adapter_review reproduced and rechecked five regressions: width/partial writes, call memory/SIMD clobbers, unsupported loops, all-path coverage, signed-immediate comparisons. All resolved;18 synthetic tests pass. Exact final evidence-head independent review PASS,0 material findings. No raw official bytes retained.

Final source qualification: focused33925815752/job101193970658; CI33925815918; governance33925815751; boundary33925815793, all SUCCESS. Persisted source JSON exactly matches the final qualification output, reviewed without JS numeric reserialization. Earlier scientific artifact9956642316 digest sha256:d3038c3a89f4490c3a9d37f0dd6109ce810cb09d81783bada18c153c83199ae3.

## Lifecycle and continuation

Source PR904 remains Draft until this clean docs-only promotion merges, then closes unmerged as consumed. Its active record lives only on its source branch; archive closeout must import an explicitly labelled historical source record, not pretend it existed on main. This coordinator active task is moved to archive in a separate PR with ownership_released:true. No source analyzer/workflow is promoted.

After archive, execute existing canonical alias OTC-BE4F48-QUEUE-SIGNAL-BF-QMETA-INDEX-CONNECTION sequentially. No duplication of consumed adapter or body/name scans. SOURCE_BLOCKER is task-local and does not exhaust static proof classes or end the login programme.

runtime_access=none; official_client_executed=false; login_performed=false; credentials_used=false; process_memory_access=false; packet_capture=false; ocr_vision_used=false; official_service_e2e_count=0; track_b_pr_284_modified=false.
