# Independent exact packaged Qt source qualification

Scientific head 98ff5e7760673ad2e98b7c95c0faaff2f4c73669, source PR911. Repository-only RED 8052fd76210e9ab6fc0678e33f2bf4cee70f6155, seven missing-module tests before acquisition. Final41tests PASS, including observed regression RED/GREEN for ELF/SONAME/function identity, unresolved target rejection, stack widths/overlap, exact external-vs-internal decode boundaries and finite must-identity loop convergence. Independent Codex reviewer /root/queue_evidence_review: PASS,0remaining material findings over full source diff.

Exact primary client15.32.be4f48 /52105824 /552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1. Exactly one public package QtCore member bin/lib/libQt6Core.so.6, size7354472, SHA25603ac3e4e7356399897ec58d42c81ae5c257072d45d539de1def528a8a04911fa. Freshly pinned before analysis; ELF64/EM_X86_64, SONAME libQt6Core.so.6, selected defined STT_FUNC. Primary executable DT_NEEDED/import relationship proven. Package identity is not runtime-loaded identity.

FACT: exact selected QObject::connectImpl address0x1d3570, FDE0x1d3570..0x1d376a, symbolsize506. Finite must-identity dataflow reaches fixedpoint137updates,131reachableinstructions. Only two explicit FDE-scope exits: conditional jne0x1d36fb ->0xc6c16; unconditional jmp0x1d375c ->0xc6c5c. These may be cold partitions; no distinct-callee ownership inferred. One conditional in-FDE carrier observation: call0x1d36e8 ->0x1cd220 carries entryreceiver inrcx. Empty receiver-register sets at exits mean no register identity proven by this abstraction, not absence of the actual value. Earlier path-unrolling observations at0x1d36a4 are not promoted.

INFERENCE: bounded continuation semantics can discriminate the exact exits without repeating an executable-wide or larger scan.

UNKNOWN: continuation ownership/semantics, complete Qt registration/storage/delivery binding, actual loaded QtCore, actual receiver/class, finalwriter,Field6,ordering and safe TrackB delta. receiver_delegation_proven=false; external_qt_receiver_binding=NOT_PROVEN.

terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=EXACT_QT_CONNECTIMPL_OUT_OF_FDE_CONTINUATION_SEMANTICS_NOT_PROVEN

Focused33929562867/job101205219720; CI33929563003; governance33929562888; boundary33929562884, allSUCCESS. Artifact9958050430, sha256:1546d9b2ac143903c352f26d39741fe3f1c31cfa9283cb14bb67105d7e614f24. Raw client/core and all acquisition state deleted before sanitized artifact. Initial incomplete results were never scientific blockers; single overwritten stop_reason was replaced by explicit per-exit evidence, then loops closed by conservative fixedpoint.

runtime_access=none; official_client_executed=false; login_performed=false; credentials_used=false; process_memory_access=false; packet_capture=false; ocr_vision_used=false; official_service_e2e_count=0; track_b_pr_284_modified=false. Source staysDraft, never self-merges, pending clean consumption and separatearchive.
