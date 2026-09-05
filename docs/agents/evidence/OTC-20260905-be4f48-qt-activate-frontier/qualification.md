# Exact-current QtCore symbol control frontier

## FACT

Scientific 0533b9837f79f9001e3a5629858cb7d934c30522 requalified primary15.32.be4f48/52105824/SHA256552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1 and packagedQtCore7354472/SHA25603ac3e4e7356399897ec58d42c81ae5c257072d45d539de1def528a8a04911fa. Repaired947 identity lookup matches symbol3860,section14,address1d3ff0,size85,name _ZN11QMetaObject8activateEP7QObjectPKS_iPPv.

The selected85byte extent[0x1d3ff0,0x1d4045) has21 reachable instructions in the bounded first-transfer graph. Model graph coverage is complete with an internal cycle: edge0x1d401e->0x1d4010. First-transfer boundaries are direct TAIL_JUMP0x1d4032->0x1dcec0 and TAIL_JUMP0x1d4040->0x1dc610. Branch0x1d4030 has successors0x1d4032 and0x1d4040. No target bytes read and no target implementation/argument identity inferred. Complete graph coverage is not termination or runtime path feasibility proof; both remainfalse. Full sanitized CFG is in result.json.

terminal_result=POSITIVE_EXACT_SYMBOL_CONTROL_FRONTIER. FIRST_MISSING_BOUNDARY=SYMBOL_FRONTIER_TARGET_USE_NOT_PROVEN. The unresolved boundaries are the use/argument semantics of the two external tail targets, plus internal-cycle termination; this task proves neither.

## TDD and falsification

Original RED82df42115d6717a09fdc56c9dabc7f4684cec6a3 had20 unimplemented-stub errors,then67testsGREEN; extent guard RED1/GREEN68. S951-01 found UD0/UD1 ungrouped traps falsely falling through. Original scientific2e29d0fe58a5a91fe33064608ffcb11f2768180e remainsDISQUALIFIED despitegreen33969748852/33969748994/33969748884/33969748834. Interrupted priorinvocation endedROTATE atcheckpointd0c6444e19b539d793594c50cae537ca170fae01, which intentionally skippedCI and was never qualified.

New ownerinvocation14:37:31Z resumed same task. REDafdcc9ff5a01a718c030b1d73384003674231cf3 produced2assertionfailures before minimalUD0/UD1GREEN69. Scientific26fde7e461625aebde7692f823c71c04b6139c2e alsoDISQUALIFIED despitefocused33972569784/job101323568288SUCCESS. Independent S951-02 found ungrouped enclave/system instructions falselyfallingthrough. S951-03 found prefixedJMP andfarreturn mnemonicambiguity. RED080c396acf7feeed79049a87bba7d62bdd1859f9 produced9failures; canonical instruction identity plus explicitunmodeledsystemhandlingGREEN72. Supplemental prefixedfarreturn regression restored oldmnemonicpredicate andproduced3failures,thenrestoredidentitycheckGREEN73. Two repaircycles inthisinvocation,retries0. Independent73tests and44additionalvariant checks pass; exact-head review correspondence mustbeverified beforeconsumption.

## Qualification

Focused33972796888/job101324168813 SUCCESS;CI33972797018/governance33972796884/boundary33972796886SUCCESS. Exact checkout,73tests,strictdualfilefences,rawbytes removal and acquisition-state removal beforeartifact verified from completedlog. Sanitized artifact9971425777,SHA256d17cee26db62608c61d27acbde8936c464d7e71352041349731b6c8c2d9bec5a. This result.json preserves original scientific output. Finaldocumentationhead requiresfresh focused/CI/governance/boundary and identicalsanitizedJSON beforecleanconsumption.

## INFERENCE

None promoted. No claim that either branch executes at runtime,that cycleterminates,or that either target is a queue/TCPwriter. No activation/register/index semantics from mangledname.

## UNKNOWN

Targetuse andtailargumentsemantics,looptermination,pathfeasibility,runtime/provider/versionresolution,logicalargumentvector,activation/index,actualsendLoginreceiver/completecausalbinding,registereddownstreamreceiver/delivery,finalqueue/TCPwriter/contract,Field6value andpre-successordering remainUNKNOWN. TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN. TrackB284exact62383aded3acbeb5f405a12fe1f93849cd8e35f9 unchangedblocked; sources939/919remainseparatelyblocked.

## Safety and lifecycle

runtime_access=none;officialclientexecution/login/credentials/memory/capture/OCR/serviceE2E/TrackBmutationszero. E2ENOT_APPLICABLE staticproducer. No rawbytes uploaded/retained asartifact. SourceDraftnevermerges; clean docs-onlypromotion fromfreshmain,expectedheadsquash,sourceclosedunmergedconsumed,separatearchiveownershiprelease beforeonesuccessor. No sourceanalyzer/workflowpromotion. Newinvocation14:37:31Z/120minutes/oneadditionalafterentry951; priorinvocationhistory/counters retained, no CIwaitreset.
