from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, found {text.count(old)}")
    return text.replace(old, new)


source = Path("oteryn-client/crates/renderer-resource/src/lib.rs")
text = source.read_text(encoding="utf-8")
text = replace_once(
    text,
    """    /// Rejects stale asset generations, invalid images, exhausted checked
    /// counters and sink upload failures. Capacity and memory pressure evict the
    /// deterministic least-recently-used entry before upload.
""",
    """    /// Rejects stale asset generations, invalid images, exhausted checked
    /// counters and sink upload failures. Capacity and memory pressure commit
    /// deterministic least-recently-used evictions before sink upload so the
    /// configured resident-device budget is never exceeded. If that upload then
    /// fails, those already committed evictions remain in effect.
""",
    "acquire failure contract",
)
text = replace_once(
    text,
    """    /// Rejects an unchanged generation.
    pub fn replace_device(
""",
    """    /// Rejects a generation that is unchanged or lower.
    pub fn replace_device(
""",
    "device generation docs",
)
text = replace_once(
    text,
    """    /// Rejects an unchanged generation.
    pub fn replace_pack(
""",
    """    /// Rejects a generation that is unchanged or lower.
    pub fn replace_pack(
""",
    "pack generation docs",
)
text = replace_once(
    text,
    '"replacement device generation must differ from the current generation"',
    '"replacement device generation must advance beyond the current generation"',
    "device generation error",
)
text = replace_once(
    text,
    '"replacement asset-pack generation must differ from the current generation"',
    '"replacement asset-pack generation must advance beyond the current generation"',
    "pack generation error",
)

anchor = """    #[test]
    fn pre_upload_counter_failure_is_atomic() -> Result<(), Box<dyn Error>> {
"""
test = """    #[test]
    fn upload_failure_after_pressure_preserves_bounded_eviction() -> Result<(), Box<dyn Error>> {
        let (_runtime_a, asset_a, decoded_a) = fixture(10, 1, 1, 1, 1)?;
        let (_runtime_b, asset_b, decoded_b) = fixture(10, 2, 1, 1, 2)?;
        let limits = ResourceLimits::new(1, 4, 4, 256)?;
        let mut cache = cache(asset_a.generation(), limits)?;
        let first = cache.acquire(asset_a, &decoded_a)?;
        cache.sink.fail_next = true;

        assert_eq!(
            cache.acquire(asset_b, &decoded_b).err(),
            Some(ResourceError::UploadFailed)
        );
        assert_eq!(
            cache.resolve(first.handle()).err(),
            Some(ResourceError::MissingResource)
        );
        assert_eq!(cache.entry_count(), 0);
        assert_eq!(cache.accounted_device_bytes(), 0);
        assert_eq!(cache.sink.destroyed, 1);
        Ok(())
    }

"""
if "fn upload_failure_after_pressure_preserves_bounded_eviction()" not in text:
    if text.count(anchor) != 1:
        raise SystemExit("eviction failure test: expected one insertion anchor")
    text = text.replace(anchor, test + anchor)
source.write_text(text, encoding="utf-8", newline="\n")

layout = Path("oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md")
layout_text = layout.read_text(encoding="utf-8")
layout_text = replace_once(
    layout_text,
    "`asset-decode` is categorized as a bounded runtime service and depends only on the merged asset runtime and schema crates in production; its compiler dependency is test-only.",
    "`asset-decode` is a dedicated bounded decode category and depends only on the merged asset runtime and schema crates in production; its compiler dependency is test-only.",
    "asset-decode category documentation",
)
layout.write_text(layout_text, encoding="utf-8", newline="\n")
