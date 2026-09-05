# Exact-current packaged QtCore dynamic definition

## FACT

Registered946 on protected main 67e6030ac3a94d3e5241749c2f8332353b3a46df. Scientific c694e8970fbd427e02e9c7c08093b621c1a183a9 verified primary15.32.be4f48/52105824/SHA256552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1 and packaged QtCore7354472/SHA25603ac3e4e7356399897ec58d42c81ae5c257072d45d539de1def528a8a04911fa.

For the name promoted by943/944, _ZN11QMetaObject8activateEP7QObjectPKS_iPPv, the selected GNU hash lookup proves one defined default-visibility GLOBAL/WEAK STT_FUNC record at symbol index3860, address0x1d3ff0,size85,extent[0x1d3ff0,0x1d4045),section14. Acceptance does not distinguish GLOBAL versus WEAK in sanitized output. GNU hash3389874950; one bloom word,one bucket,four chain entries,one candidate name. DT_GNU_HASH0x328,DT_SYMTAB0xd538,DT_SYMENT0x18,DT_STRTAB0x3a1d8. Header-only section metadata; no eager GNUHashSection construction, no function-body or FDE reads. The extent is uniquely contained in an allocated executable file-backed section after rejecting all partial allocated mapping intersections.

terminal_result=POSITIVE_EXACT_PACKAGED_DYNAMIC_DEFINITION. FIRST_MISSING_BOUNDARY=PACKAGED_DEFINITION_BODY_USE_NOT_PROVEN. This is a packaged link-time definition, not a loaded provider or version-resolution proof.

## TDD and falsification

Initial RED 1c8103a3686f5d714fd614622e49683c851b80b4:30 errors from explicit unimplemented lookup,then GREEN39 including9 package tests. Root prequalification bounds/chain-width controls RED2 failures,GREEN41 before first source qualification.

S947-01 independently found partial section overlaps ignored by full-containment-only checks. e77b565b109feb0e42b32812f4b04d502cc33a74 disqualified despite focused33968512852/CI33968512914/governance33968512851/boundary33968512877 SUCCESS. Regression RED 36451a1f947114fe8d91edd4c87dc5f9a3d4d6b1:four failures; GREEN45 counts all allocated intersections for selected metadata and function extent. Independent repair-family tests also accept adjacent non-overlapping sections.

S947-02 root then found pyelftools iter_sections constructs GNUHashSection and eagerly reads all bloom words/buckets. dae0651276fdb31a44ea5e9edd2d7e14e640a72f disqualified despite focused33968595877/CI33968596133/governance33968595969/boundary33968595983 SUCCESS and earlier PASS0 review. Reviewer independently confirmed the missed constructor side effect. Regression RED c085856330293f22a16d6e8a9cffba78abbc138f:two failures including actual analyzer entry calling forbidden iter_sections. GREEN47 reads only fixed-width section headers after table width/count/file bounds. Independent real synthetic ELF guard permits ELFFile initialization and header metadata while denying dynamic/hash/symbol/string/function payload; old get_section path trips the hash guard. Invalid header width,offset,count rejected. Final source review PASS0 material findings. Repaircycles2,retries0.

## Exact qualification

Focused33968804893/job101313538079 SUCCESS;CI33968804984/governance33968804906/boundary33968804881 SUCCESS. Exact checkout,47 tests,strict dual-file fences,raw removal and all acquisition-state removal before artifact verified. Sanitized artifact9970281348,digest5b03d25ddde9b7e49f1b437f8345a6030a54719e38ee584256394d55557656b3. result.json is the original deterministic sanitized result. Final documentation head still requires fresh qualification, equality comparison and checks before consumption.

## INFERENCE

None promoted. Matching mangled name does not prove runtime import binding, symbol-version selection, activation ABI/arguments or signal delivery.

## UNKNOWN

Packaged definition body/use,version/runtime resolution,logical argument vector,activation/index semantics,sendLogin receiver/complete causal binding,registered downstream receiver/delivery,final queue/TCP writers/contract,Field6 value andpre-success ordering remain UNKNOWN. TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN. TrackB284 head62383aded3acbeb5f405a12fe1f93849cd8e35f9 unchangedblocked. Sources939/919 remain separately blocked with released ownership.

## Lifecycle and safety

SourceDraft nevermerges. Clean docs-only coordinator consumption after exact final gates,expected-head squash,sourceclosedunmergedconsumed,separatearchiveownershiprelease before successor. No analyzer/workflow promotion. Runtime/clientexecution/login/credentials/memory/capture/OCR/serviceE2E/TrackBmutationzero. E2ENOT_APPLICABLE staticproducer. Rawofficialbytes transientonly,neverartifact. Invocation11:35:52Z/240minutes/4additionalsources,thisadditional3,repaircycles2/retries0; no budgetreset.
