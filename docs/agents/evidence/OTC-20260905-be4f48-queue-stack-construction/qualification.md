# Exact-current private-stack construction qualification

## Authority and scope

Source PR935, registered by PR934 merge1f8501614e6a3efa275451f2f9c8c1a6dd86d09b. Independent private-stack construction/pointer-escape proof class. Inspect only exact primary-client FDE[0xdd8df0,0xdd8e1a),42bytes, and the promoted direct JMP at0xde823a. No callee, import/PLT metadata, branch, global census, runtime or TrackB changes.

Primary15.32.be4f48,52105824bytes,SHA256552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1. PackagedQtCore7354472bytes,SHA25603ac3e4e7356399897ec58d42c81ae5c257072d45d539de1def528a8a04911fa; packaged identity does not prove runtime-loaded identity. Exact fence values also recorded in result.json.

## TDD and falsification

Repository-only RED8853b691b53d7c9973a970af9325fae248146cbb:21explicitunimplementedtest errors. Minimal GREEN adds21construction/tail cases;9existing package guards pass. S935-01 independently found reused Image imported relocation/symbol metadata outside scope, so scientific d049b49ef73278751fc645523b32a63e814100ed is disqualified. Regression REDc64b1ffd284a3ea12293a08242d40b71db6a62ea raised FORBIDDEN_IMPORT_METADATA_TRAVERSAL. Repair removes relocation/symbol lookup and disables DWARF relocation processing. Repaired head e85fce0a9b370bde294e7347954374398e8497de:31testsPASS,gitdiffcheckPASS, independent whole-diff and completed-result review PASS,0materialfindings. Repaircycle1,retries0.

## Exact qualification

Scientifichead e85fce0a9b370bde294e7347954374398e8497de. Focused run33961765839/job101294753595; CI33961765973; governance33961765904; self-hosted boundary33961765868: allSUCCESS. Artifact9968160929,digest761058680cdcf7cd63cda906cd34920d010c373735885f9ef685bed2bdde9a36. Root and independent reviewer verified checkout, exact fences,31tests, deterministic sanitized JSON, and raw/helper-state cleanup before sanitized artifact upload. No proprietary bytes retained in artifacts. This documentation commit must receive its own exact-head qualification and checks before consumption.

## FACT

Terminal result POSITIVE_EXACT_STACK_CONSTRUCTION_ESCAPE. Seven instructions in the linear normal prefix reach first direct call0xdd8e10->0x4d7dc0. Allocated private frame is ENTRY_RSP[-24,0). Two known8bytecells:offset-16=symbolic entry rsi, written0xdd8df9;offset-24=constant0,written0xdd8e08. At first call,rcx is a pointer to frameoffset-24 and these cells have relative offsets[0,8]. The promoted predecessor remains direct JMP0xde823a->0xdd8df0. This is a conditional static prefix proof; exceptional control is not modeled.

## INFERENCE

None promoted. No inference that the frame is fully initialized, a logical object/vector, or a Qt argument array.

## UNKNOWN

FIRST_MISSING_BOUNDARY=ESCAPED_STACK_REGION_CALLEE_USE_NOT_PROVEN. Target identity, callee use, logical parameter names, activation/index, actual receiver identity, complete sendLogin causal binding, successful registration/delivery, final queue/TCPwriter and writer contract, Field6 value, pre-success ordering remainUNKNOWN. TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN. Source result does not authorize following the callee in this task.

## Safety and lifecycle

runtime_access=none; official_client_executed=false; login_performed=false; credentials_used=false; process_memory_access=false; packet_capture=false; ocr_vision_used=false; official_service_e2e_count=0; track_b_pr_284_modified=false. Source remainsDraft and is never self-merged. Only a clean docs-only coordinator promotion from fresh trusted main may consume this result; close source unmerged, then separate ownership-releasing archive before successor registration.
