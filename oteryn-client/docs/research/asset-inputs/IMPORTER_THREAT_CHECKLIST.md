# Importer threat checklist

Scope: future build-time asset importers and inventory tools. Runtime engine crates do not parse arbitrary legacy/development formats.

An importer consumes hostile input. “It came from a local installation” or “the archive hash matched a download manifest” does not make inner structures trusted.

## 1. Input admission

- [ ] Exact source class, rights record, source version and expected top-level format are known before parsing.
- [ ] Maximum file/archive bytes, entries, dimensions, records, string bytes, nesting and decoded output are configured before allocation.
- [ ] Empty, truncated, unsupported-version and ambiguous-format inputs fail closed.
- [ ] Format detection uses bounded magic/header parsing, not filename extension alone.
- [ ] Symlinks, devices, FIFOs, sockets and other non-regular inputs are rejected unless a later explicit policy owns them.
- [ ] Absolute source paths and user names never enter logs, errors, inventory or output packs.
- [ ] Source handles are opened read-only; the importer never modifies or executes source content.

## 2. Integer and memory safety

- [ ] Every count/offset/length/dimension conversion is checked before allocation or slicing.
- [ ] Add, multiply, align, stride, frame-size and cumulative-total arithmetic uses checked operations.
- [ ] The parser validates `offset <= input_len` and `length <= input_len - offset` before reading.
- [ ] Zero dimensions/counts are accepted only when the format contract explicitly permits them.
- [ ] Aggregate budgets are enforced across nested structures, not only per record.
- [ ] A declared compressed/decoded size does not bypass actual output and ratio limits.
- [ ] Untrusted counts do not directly become `Vec::with_capacity` or equivalent allocations.
- [ ] Recursion/nesting depth is bounded or replaced with an explicit bounded stack.

## 3. Archives and paths

- [ ] Member names are normalized once and reject absolute roots, drive/UNC prefixes, `..`, NUL and control characters.
- [ ] Normalization is performed before duplicate/collision checks.
- [ ] Case-folding/canonical-name collision policy is explicit for Windows-targeted output.
- [ ] Symlink, hardlink and reparse-point members are rejected.
- [ ] Extraction writes only beneath a newly created private staging directory.
- [ ] Existing files are not followed through links or overwritten outside the staging root.
- [ ] Member count, single-member size, total expanded size and compression ratio are bounded.
- [ ] Nested archives are rejected by default; enabling them requires separate depth/aggregate limits.
- [ ] Partial extraction is deleted or quarantined on failure/cancellation.

## 4. Image, texture and animation inputs

- [ ] Width, height, layers, frames, mip count, channels and bit depth use fixed upper bounds.
- [ ] Row stride and total decoded bytes are checked independently from header claims.
- [ ] Animation duration/count arithmetic is bounded and deterministic.
- [ ] Color-space, alpha and premultiplication policy is explicit; unknown variants are rejected rather than guessed.
- [ ] Decoder metadata and decoded output are both validated.
- [ ] Embedded color profiles/metadata cannot trigger external file/network access.
- [ ] Atlas/layout generation is deterministic and independent of directory enumeration order.

## 5. Audio inputs

- [ ] Channel count, sample rate, sample format, duration and decoded bytes are bounded.
- [ ] Duration calculation uses checked arithmetic and validates container/chunk boundaries.
- [ ] Metadata tags are ignored or normalized into closed fields; arbitrary text is not copied into diagnostics.
- [ ] Decoder work has cancellation and time/output budgets.
- [ ] No audio decoder runs in a real-time callback or frame-critical path.

## 6. Fonts and text resources

- [ ] Exact font/license record is approved before content processing or bundling.
- [ ] Container face/table counts, offsets and table lengths are bounded.
- [ ] Invalid/cyclic table references and oversized glyph/variation data fail closed.
- [ ] Font names and metadata are not treated as trusted paths, identifiers or UI strings.
- [ ] Localization keys/values have byte/count limits, valid encoding and duplicate-key policy.
- [ ] Text import cannot create filesystem/network/process actions or shader/script execution.

## 7. Structured metadata and compatibility maps

- [ ] Schema version and compatibility owner are explicit.
- [ ] Unknown fields/flags have reviewed reject/ignore behavior; they are not silently reinterpreted.
- [ ] Logical IDs use checked typed conversion and duplicate/reuse policy.
- [ ] Source filesystem names never become stable runtime IDs automatically.
- [ ] Cross-record references are validated after bounded parse and before output generation.
- [ ] Cycles, dangling references and conflicting definitions are deterministic errors.
- [ ] A compatibility map cannot silently repurpose an ID within one declared compatibility line.

## 8. Execution and dependency isolation

- [ ] Importers live in tools/build workflows, not runtime engine crates.
- [ ] Embedded scripts, macros, plugins, native libraries and executable members are never run.
- [ ] No shell command is constructed from source-controlled text.
- [ ] External conversion tools, if ever approved, use exact argv, pinned versions, bounded working directories and sanitized environment.
- [ ] Network access is disabled during deterministic conversion unless a separate fetch stage with hashes/rights owns it.
- [ ] Native/unsafe dependencies receive focused source, advisory, license and safety review.

## 9. Determinism and output integrity

- [ ] Identical approved inputs, configuration and tool version produce byte-identical normalized output.
- [ ] Sorting/canonicalization rules are explicit; filesystem order and timestamps do not affect output.
- [ ] Floating-point or platform-dependent transformations have defined reproducibility policy.
- [ ] Output is written to staging, fully validated, hashed and atomically finalized.
- [ ] Tool/config/input hashes and provenance references bind the output.
- [ ] Failed output is never promoted or used as a runtime source of truth.
- [ ] Compiler caches are disposable and keyed by all behavior-affecting inputs.

## 10. Cancellation and resource containment

- [ ] Long loops/decoders check explicit cancellation at bounded intervals.
- [ ] Cancellation is owned by the calling build operation and does not rely on dropping observers.
- [ ] Worker count, queue depth, memory, temporary disk and per-input CPU/time budgets are explicit.
- [ ] Cancellation/failure removes staged outputs and releases file handles.
- [ ] No hidden thread/background service survives the importing command.
- [ ] Re-running after interruption starts from verified inputs or a validated cache, never partial output.

## 11. Diagnostics and privacy

- [ ] Errors use closed categories and bounded technical values.
- [ ] No raw input bytes, arbitrary embedded text, absolute paths, signed URLs, credentials or private identifiers appear in logs.
- [ ] Sensitive source labels use redacted/opaque correlation identifiers.
- [ ] Support artifacts contain only explicitly approved inventory/provenance metadata.
- [ ] Panic/debug dumps are not treated as acceptable error reporting for hostile inputs.

## 12. Required negative tests

Every implemented parser/importer must cover applicable cases:

- [ ] truncation at each variable header/table/record boundary;
- [ ] maximum and maximum-plus-one count/size/dimension;
- [ ] offset+length overflow and overlapping/conflicting ranges;
- [ ] duplicate IDs/names and canonical path collisions;
- [ ] path traversal, absolute path, drive/UNC, NUL/control characters and link members;
- [ ] decompression bomb, false declared size, excessive ratio and nested archive;
- [ ] malformed encoding, invalid enum/flag, dangling/cyclic reference;
- [ ] cancellation before parse, during decode, during output and before activation;
- [ ] deterministic output across shuffled input enumeration;
- [ ] source/private marker absence in error, diagnostic and inventory formatting;
- [ ] fuzz-smoke target with bounded memory/time and a minimized regression corpus.

## 13. Stop conditions

Stop the importer task and record a blocker when:

- rights/provenance are missing for content intended to be committed or distributed;
- exact format evidence requires copying proprietary content or unapproved private samples;
- safe bounds cannot be established from reviewed source/sample evidence;
- a dependency requires weakening unsafe, advisory, license or source policy;
- deterministic conversion cannot be achieved for a release artifact;
- source inspection reveals executable/script behavior not covered by an accepted security design.
