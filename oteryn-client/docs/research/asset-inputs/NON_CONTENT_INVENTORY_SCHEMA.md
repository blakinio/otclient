# Non-content asset inventory schema

Purpose: record enough metadata to evaluate a source, importer and future pack budget without retaining asset content, decoded payloads or user-specific source paths.

This is an evidence schema, not the production asset-pack schema.

## Privacy and content boundary

An inventory record must not contain:

- raw image, sound, font, shader, localization or appearance bytes;
- thumbnails, decoded previews or screenshots;
- absolute filesystem paths, usernames, home-directory fragments or machine identifiers;
- credentials, signed URLs, cookies or private endpoints;
- free-form copied metadata from an untrusted file;
- filenames when they contain personal or secret data;
- embedded scripts or arbitrary source manifests.

Use stable source labels, bounded normalized relative labels and cryptographic digests. A path used during one local scan is process-local only and is discarded after inventory generation.

## Envelope

```yaml
schema_version: 1
inventory_id: <stable UUID/opaque non-secret identifier>
created_by_tool: <tool name>
tool_version: <immutable version/commit>
created_at_utc: <RFC 3339 timestamp>
source_class: oteryn_owned | third_party_licensed | user_local | synthetic | compatibility_metadata
source_id: <stable reviewed label>
source_version: <immutable version>
rights_record_id: <reference to approved/blocked rights record>
rights_status: approved | blocked | prohibited
compatibility:
  product: <bounded product label>
  asset_set: <version or unknown>
  protocol_profile: <profile or not_applicable>
  producer_revision: <commit/version or unknown>
scan_policy:
  content_retained: false
  absolute_paths_retained: false
  symlinks_followed: false
  archives_expanded: false
  maximum_input_bytes: <u64>
  maximum_entries: <u32>
summary: <AssetInventorySummary>
entries: [<AssetInventoryEntry>]
inventory_sha256: <hash of canonical metadata representation>
```

`archives_expanded` is false for a generic inventory-only scan. A future importer-specific inventory may inspect archive members only in a sandbox under the importer threat policy and must label that distinct mode.

## Summary

```yaml
total_entries: <u32>
total_input_bytes: <u64>
asset_family_counts:
  sprite: <u32>
  appearance_metadata: <u32>
  ui_image: <u32>
  font: <u32>
  sound: <u32>
  shader: <u32>
  localization: <u32>
  unknown: <u32>
format_counts:
  <bounded normalized format label>: <u32>
maximum_observed:
  file_bytes: <u64>
  image_width: <u32 or null>
  image_height: <u32 or null>
  image_frames: <u32 or null>
  audio_channels: <u16 or null>
  audio_sample_rate_hz: <u32 or null>
  audio_duration_ms: <u64 or null>
  font_tables: <u16 or null>
unknown_or_rejected_entries: <u32>
```

All totals use checked arithmetic. Overflow, entry-limit exhaustion or a value outside the scanner policy rejects the inventory rather than saturating silently.

## Entry

```yaml
entry_id: <stable sequential or digest-derived non-secret ID>
source_label: <bounded normalized label; not an absolute path>
family: sprite | appearance_metadata | ui_image | font | sound | shader | localization | unknown
detected_format: <closed format label or unknown>
input_bytes: <u64>
input_sha256: <digest>
metadata_status: accepted | unknown_format | malformed | policy_rejected
shape:
  image:
    width: <u32>
    height: <u32>
    frames: <u32>
    color_model: <closed label>
    alpha: none | straight | premultiplied | unknown
  audio:
    channels: <u16>
    sample_rate_hz: <u32>
    duration_ms: <u64>
    encoded_format: <closed label>
  font:
    container: <closed label>
    face_count: <u16>
    table_count: <u16>
  structured:
    record_count: <u32>
    maximum_record_bytes: <u32>
    identifier_min: <u64 or null>
    identifier_max: <u64 or null>
compatibility_tags: [<bounded reviewed static labels>]
rights_record_id: <reference>
notes_codes: [<closed machine-readable codes>]
```

Only the shape section matching the family is present. Parsed metadata is accepted only after bounded header validation; the inventory does not decode pixel/audio/glyph content merely to collect statistics.

## Canonicalization

To make inventories deterministic:

- sort entries by `(family, input_sha256, source_label)` after normalization;
- normalize labels to UTF-8, forward slash, no `.`/`..`, no drive/UNC prefix and a fixed byte limit;
- reject duplicate `entry_id` and duplicate canonical labels within one source;
- serialize maps/fields in schema-defined order;
- encode integers in decimal without locale-dependent formatting;
- omit absent family-specific sections rather than emitting arbitrary placeholders;
- hash the canonical representation excluding `inventory_sha256` itself;
- record tool revision and policy limits so changed scanners cannot silently compare as identical.

Directory enumeration order, modification timestamps, inode numbers and OS-specific path casing are not content identity.

## Rights integration

The inventory can be produced with `rights_status: blocked` to record content-free counts/statistics during a separately approved local evaluation, but:

- blocked/prohibited records cannot feed a release compiler;
- the inventory itself must still contain no protected content or private path;
- publishing aggregate statistics may require separate approval if they reveal confidential source information;
- changing rights status requires a referenced review record, not a manual field edit.

## Validation negatives

A future inventory parser/test suite must reject:

- unknown schema version;
- missing source/rights/tool identity;
- `content_retained: true`;
- absolute, parent-traversing, NUL/control-bearing or oversized labels;
- duplicate IDs/labels;
- count/byte total mismatch;
- arithmetic overflow;
- family/shape mismatch;
- unknown enum values unless explicitly represented by `unknown`;
- malformed SHA-256 values;
- unsupported compatibility tags or unbounded notes;
- canonical hash mismatch.

## Use in the first synthetic slice

The synthetic slice should generate this inventory from original, tool-generated test inputs and assert:

- deterministic canonical bytes and hash;
- exact counts/dimensions;
- no absolute source path appears in output or errors;
- changing one input changes its digest and inventory hash;
- directory enumeration order does not change output;
- malformed/oversized input produces a closed error with no copied source data.
