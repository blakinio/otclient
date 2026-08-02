//! Immutable bounded runtime for project-original synthetic-v1 asset packs.
//!
//! The public boundary accepts bytes or an already-opened reader. It never
//! accepts paths, resolves loose files, decodes media, uploads resources or
//! claims compatibility with production asset formats.

mod error;
mod handle;

pub use error::RuntimeError;
pub use handle::{AssetHandle, PackGeneration};

use oteryn_asset_types::{
    AssetId, AssetKind, AssetMetadata, AssetPack, AssetRecord, MAX_ASSET_BYTES, MAX_PACK_BYTES,
    MAX_RECORDS,
};
use std::fmt::{self, Debug, Formatter};
use std::io::Read;

/// Runtime bounds that may only narrow the synthetic-v1 schema limits.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RuntimeLimits {
    max_pack_bytes: usize,
    max_records: usize,
    max_asset_bytes: usize,
}

impl RuntimeLimits {
    /// Return the complete schema-v1 limits.
    #[must_use]
    pub const fn schema_v1() -> Self {
        Self {
            max_pack_bytes: MAX_PACK_BYTES,
            max_records: MAX_RECORDS,
            max_asset_bytes: MAX_ASSET_BYTES,
        }
    }

    /// Construct narrower runtime limits.
    ///
    /// # Errors
    ///
    /// Returns [`RuntimeError::InvalidLimits`] when a value exceeds the
    /// synthetic-v1 schema bounds or the pack-byte bound is zero.
    pub fn new(
        max_pack_bytes: usize,
        max_records: usize,
        max_asset_bytes: usize,
    ) -> Result<Self, RuntimeError> {
        if max_pack_bytes == 0
            || max_pack_bytes > MAX_PACK_BYTES
            || max_records > MAX_RECORDS
            || max_asset_bytes > MAX_ASSET_BYTES
        {
            return Err(RuntimeError::InvalidLimits);
        }
        Ok(Self {
            max_pack_bytes,
            max_records,
            max_asset_bytes,
        })
    }

    /// Return the maximum accepted encoded object size.
    #[must_use]
    pub const fn max_pack_bytes(self) -> usize {
        self.max_pack_bytes
    }

    /// Return the maximum accepted record count.
    #[must_use]
    pub const fn max_records(self) -> usize {
        self.max_records
    }

    /// Return the maximum accepted payload size per record.
    #[must_use]
    pub const fn max_asset_bytes(self) -> usize {
        self.max_asset_bytes
    }
}

impl Default for RuntimeLimits {
    fn default() -> Self {
        Self::schema_v1()
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct IndexEntry {
    id: AssetId,
    record_index: usize,
}

/// One immutable, fully verified synthetic-v1 pack instance.
pub struct AssetRuntime {
    generation: PackGeneration,
    limits: RuntimeLimits,
    encoded_bytes: usize,
    pack: AssetPack,
    index: Box<[IndexEntry]>,
}

impl AssetRuntime {
    /// Open and verify one complete in-memory object.
    ///
    /// The object must already have been obtained through a caller-owned
    /// capability boundary. This method performs no path or filesystem access.
    ///
    /// # Errors
    ///
    /// Returns a stable runtime or schema error for oversized, malformed,
    /// non-canonical, truncated, trailing, digest-mismatched or unsupported
    /// input.
    pub fn open_bytes(
        generation: PackGeneration,
        encoded: &[u8],
        limits: RuntimeLimits,
    ) -> Result<Self, RuntimeError> {
        if encoded.len() > limits.max_pack_bytes {
            return Err(RuntimeError::ObjectTooLarge);
        }
        let pack = AssetPack::decode(encoded)?;
        Self::from_decoded(generation, limits, encoded.len(), pack)
    }

    /// Read, bound, open and verify one already-opened object.
    ///
    /// The caller owns acquisition and capability policy. The runtime receives
    /// only a reader and never a source path.
    ///
    /// # Errors
    ///
    /// Returns [`RuntimeError::ObjectUnavailable`] for read failure and the
    /// same verification errors as [`Self::open_bytes`].
    pub fn open_reader<R: Read>(
        generation: PackGeneration,
        reader: R,
        limits: RuntimeLimits,
    ) -> Result<Self, RuntimeError> {
        let bounded_length = limits
            .max_pack_bytes
            .checked_add(1)
            .ok_or(RuntimeError::ArithmeticOverflow)?;
        let bounded_length =
            u64::try_from(bounded_length).map_err(|_| RuntimeError::ArithmeticOverflow)?;
        let mut limited = reader.take(bounded_length);
        let mut encoded = Vec::new();
        limited
            .read_to_end(&mut encoded)
            .map_err(|_| RuntimeError::ObjectUnavailable)?;
        if encoded.len() > limits.max_pack_bytes {
            return Err(RuntimeError::ObjectTooLarge);
        }
        Self::open_bytes(generation, &encoded, limits)
    }

    fn from_decoded(
        generation: PackGeneration,
        limits: RuntimeLimits,
        encoded_bytes: usize,
        pack: AssetPack,
    ) -> Result<Self, RuntimeError> {
        if pack.records().len() > limits.max_records {
            return Err(RuntimeError::TooManyRecords);
        }

        let mut index = Vec::with_capacity(pack.records().len());
        for (record_index, record) in pack.records().iter().enumerate() {
            if record.payload().len() > limits.max_asset_bytes {
                return Err(RuntimeError::PayloadTooLarge);
            }
            index.push(IndexEntry {
                id: record.metadata().id(),
                record_index,
            });
        }

        Ok(Self {
            generation,
            limits,
            encoded_bytes,
            pack,
            index: index.into_boxed_slice(),
        })
    }

    /// Return this opened pack's generation.
    #[must_use]
    pub const fn generation(&self) -> PackGeneration {
        self.generation
    }

    /// Return the applied runtime limits.
    #[must_use]
    pub const fn limits(&self) -> RuntimeLimits {
        self.limits
    }

    /// Return the verified encoded byte count.
    #[must_use]
    pub const fn encoded_bytes(&self) -> usize {
        self.encoded_bytes
    }

    /// Return the immutable indexed record count.
    #[must_use]
    pub fn record_count(&self) -> usize {
        self.index.len()
    }

    /// Return a generation-fenced handle when the canonical ID is present.
    #[must_use]
    pub fn handle(&self, id: AssetId) -> Option<AssetHandle> {
        self.index
            .binary_search_by_key(&id, |entry| entry.id)
            .ok()
            .map(|_| AssetHandle::new(self.generation, id))
    }

    /// Enumerate canonical handles in ascending asset-ID order.
    pub fn handles(&self) -> impl ExactSizeIterator<Item = AssetHandle> + DoubleEndedIterator + '_ {
        self.index
            .iter()
            .map(|entry| AssetHandle::new(self.generation, entry.id))
    }

    /// Resolve one logical handle to bounded metadata and payload bytes.
    ///
    /// # Errors
    ///
    /// Returns [`RuntimeError::StaleHandle`] for a generation mismatch and
    /// [`RuntimeError::UnknownAsset`] when the ID is absent.
    pub fn lookup(&self, handle: AssetHandle) -> Result<AssetView<'_>, RuntimeError> {
        if handle.generation() != self.generation {
            return Err(RuntimeError::StaleHandle);
        }
        let position = self
            .index
            .binary_search_by_key(&handle.id(), |entry| entry.id)
            .map_err(|_| RuntimeError::UnknownAsset)?;
        let entry = self.index[position];
        let record = &self.pack.records()[entry.record_index];
        Ok(AssetView { record })
    }

    /// Consume the immutable runtime deterministically.
    ///
    /// No global cache, background work or external resource remains owned by
    /// this crate after the value is consumed or dropped.
    pub fn close(self) {}
}

impl Debug for AssetRuntime {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("AssetRuntime")
            .field("generation", &self.generation)
            .field("record_count", &self.record_count())
            .field("encoded_bytes", &self.encoded_bytes)
            .finish_non_exhaustive()
    }
}

/// Borrowed bounded view of one verified record.
pub struct AssetView<'a> {
    record: &'a AssetRecord,
}

impl AssetView<'_> {
    /// Return validated metadata.
    #[must_use]
    pub const fn metadata(&self) -> &AssetMetadata {
        self.record.metadata()
    }

    /// Return the canonical asset identifier.
    #[must_use]
    pub const fn id(&self) -> AssetId {
        self.record.metadata().id()
    }

    /// Return the normalized synthetic-v1 asset kind.
    #[must_use]
    pub const fn kind(&self) -> AssetKind {
        self.record.metadata().kind()
    }

    /// Return the verified SHA-256 payload digest declared by schema v1.
    #[must_use]
    pub const fn digest(&self) -> &[u8; 32] {
        self.record.digest()
    }

    /// Return the bounded verified payload bytes.
    #[must_use]
    pub fn payload(&self) -> &[u8] {
        self.record.payload()
    }
}

impl Debug for AssetView<'_> {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("AssetView")
            .field("id", &self.id())
            .field("kind", &self.kind())
            .field("payload_bytes", &self.payload().len())
            .finish_non_exhaustive()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use oteryn_asset_types::{AssetError, AssetMetadata, AssetRecord};
    use std::io::{self, Cursor};

    fn blob_record(id: u32, name: &str, payload: &[u8]) -> Result<AssetRecord, AssetError> {
        let metadata = AssetMetadata::new(
            AssetId::new(id)?,
            AssetKind::Blob,
            name.to_owned(),
            "CC0-1.0".to_owned(),
            "project-original synthetic fixture".to_owned(),
        )?;
        AssetRecord::new(metadata, payload.to_vec())
    }

    fn rgba_record(id: u32) -> Result<AssetRecord, AssetError> {
        let metadata = AssetMetadata::new(
            AssetId::new(id)?,
            AssetKind::Rgba8 {
                width: 1,
                height: 1,
            },
            "pixel".to_owned(),
            "CC0-1.0".to_owned(),
            "project-original synthetic fixture".to_owned(),
        )?;
        AssetRecord::new(metadata, vec![1, 2, 3, 4])
    }

    fn encoded_pack(records: Vec<AssetRecord>) -> Result<Vec<u8>, AssetError> {
        AssetPack::new(records)?.encode()
    }

    fn generation(value: u64) -> Result<PackGeneration, RuntimeError> {
        PackGeneration::new(value)
    }

    fn second_record_offset(encoded: &[u8]) -> Result<usize, io::Error> {
        let mut offset = 14usize;
        offset = skip_record(encoded, offset)?;
        Ok(offset)
    }

    fn skip_record(encoded: &[u8], mut offset: usize) -> Result<usize, io::Error> {
        offset = offset
            .checked_add(13)
            .ok_or_else(|| io::Error::other("test offset overflow"))?;
        for _ in 0..3 {
            let length_bytes = encoded
                .get(offset..offset + 2)
                .ok_or_else(|| io::Error::other("missing test text length"))?;
            let length = usize::from(u16::from_le_bytes([length_bytes[0], length_bytes[1]]));
            offset = offset
                .checked_add(2)
                .and_then(|value| value.checked_add(length))
                .ok_or_else(|| io::Error::other("test offset overflow"))?;
        }
        offset = offset
            .checked_add(32)
            .ok_or_else(|| io::Error::other("test offset overflow"))?;
        let length_bytes = encoded
            .get(offset..offset + 4)
            .ok_or_else(|| io::Error::other("missing test payload length"))?;
        let length = usize::try_from(u32::from_le_bytes([
            length_bytes[0],
            length_bytes[1],
            length_bytes[2],
            length_bytes[3],
        ]))
        .map_err(|_| io::Error::other("test payload length conversion failed"))?;
        offset = offset
            .checked_add(4)
            .and_then(|value| value.checked_add(length))
            .ok_or_else(|| io::Error::other("test offset overflow"))?;
        Ok(offset)
    }

    #[test]
    fn opens_indexes_and_looks_up_canonical_records() -> Result<(), Box<dyn std::error::Error>> {
        let encoded = encoded_pack(vec![
            blob_record(7, "second", b"beta")?,
            blob_record(2, "first", b"alpha")?,
        ])?;
        let runtime =
            AssetRuntime::open_bytes(generation(11)?, &encoded, RuntimeLimits::schema_v1())?;

        let ids: Vec<u32> = runtime.handles().map(|handle| handle.id().get()).collect();
        assert_eq!(ids, vec![2, 7]);
        let handle = runtime
            .handle(AssetId::new(7)?)
            .ok_or_else(|| io::Error::other("missing expected handle"))?;
        let view = runtime.lookup(handle)?;
        assert_eq!(view.payload(), b"beta");
        assert_eq!(view.metadata().logical_name(), "second");
        assert_eq!(runtime.record_count(), 2);
        assert_eq!(runtime.encoded_bytes(), encoded.len());
        Ok(())
    }

    #[test]
    fn already_opened_reader_is_supported() -> Result<(), Box<dyn std::error::Error>> {
        let encoded = encoded_pack(vec![blob_record(1, "reader", b"object")?])?;
        let runtime = AssetRuntime::open_reader(
            generation(1)?,
            Cursor::new(encoded),
            RuntimeLimits::schema_v1(),
        )?;
        assert_eq!(runtime.record_count(), 1);
        Ok(())
    }

    #[test]
    fn repeated_open_is_deterministic() -> Result<(), Box<dyn std::error::Error>> {
        let encoded = encoded_pack(vec![rgba_record(9)?, blob_record(3, "blob", b"same")?])?;
        let first = AssetRuntime::open_bytes(generation(4)?, &encoded, RuntimeLimits::schema_v1())?;
        let second =
            AssetRuntime::open_bytes(generation(4)?, &encoded, RuntimeLimits::schema_v1())?;
        let first_ids: Vec<_> = first.handles().collect();
        let second_ids: Vec<_> = second.handles().collect();
        assert_eq!(first_ids, second_ids);
        for handle in first_ids {
            assert_eq!(
                first.lookup(handle)?.payload(),
                second.lookup(handle)?.payload()
            );
            assert_eq!(
                first.lookup(handle)?.digest(),
                second.lookup(handle)?.digest()
            );
        }
        Ok(())
    }

    #[test]
    fn stale_and_unknown_handles_fail_closed() -> Result<(), Box<dyn std::error::Error>> {
        let encoded = encoded_pack(vec![blob_record(5, "present", b"data")?])?;
        let old = AssetRuntime::open_bytes(generation(1)?, &encoded, RuntimeLimits::schema_v1())?;
        let handle = old
            .handle(AssetId::new(5)?)
            .ok_or_else(|| io::Error::other("missing expected handle"))?;
        let current =
            AssetRuntime::open_bytes(generation(2)?, &encoded, RuntimeLimits::schema_v1())?;
        assert_eq!(
            current.lookup(handle).err(),
            Some(RuntimeError::StaleHandle)
        );
        let unknown = AssetHandle::new(generation(2)?, AssetId::new(99)?);
        assert_eq!(
            current.lookup(unknown).err(),
            Some(RuntimeError::UnknownAsset)
        );
        Ok(())
    }

    #[test]
    fn truncated_and_trailing_objects_are_rejected() -> Result<(), Box<dyn std::error::Error>> {
        let encoded = encoded_pack(vec![blob_record(1, "bounded", b"payload")?])?;
        let mut truncated = encoded.clone();
        let new_length = truncated
            .len()
            .checked_sub(1)
            .ok_or_else(|| io::Error::other("empty encoded fixture"))?;
        truncated.truncate(new_length);
        assert!(
            AssetRuntime::open_bytes(generation(1)?, &truncated, RuntimeLimits::schema_v1())
                .is_err()
        );

        let mut trailing = encoded;
        trailing.push(0);
        assert_eq!(
            AssetRuntime::open_bytes(generation(1)?, &trailing, RuntimeLimits::schema_v1()).err(),
            Some(RuntimeError::Asset(AssetError::TrailingBytes))
        );
        Ok(())
    }

    #[test]
    fn unsupported_version_and_digest_corruption_are_rejected()
    -> Result<(), Box<dyn std::error::Error>> {
        let encoded = encoded_pack(vec![blob_record(1, "versioned", b"payload")?])?;
        let mut unsupported = encoded.clone();
        unsupported[8..10].copy_from_slice(&2u16.to_le_bytes());
        assert_eq!(
            AssetRuntime::open_bytes(generation(1)?, &unsupported, RuntimeLimits::schema_v1())
                .err(),
            Some(RuntimeError::Asset(AssetError::UnsupportedVersion))
        );

        let mut corrupt = encoded;
        let final_byte = corrupt
            .last_mut()
            .ok_or_else(|| io::Error::other("empty encoded fixture"))?;
        *final_byte ^= 0xFF;
        assert_eq!(
            AssetRuntime::open_bytes(generation(1)?, &corrupt, RuntimeLimits::schema_v1()).err(),
            Some(RuntimeError::Asset(AssetError::DigestMismatch))
        );
        Ok(())
    }

    #[test]
    fn duplicate_ids_and_declared_oversize_are_rejected() -> Result<(), Box<dyn std::error::Error>>
    {
        let mut duplicate = encoded_pack(vec![
            blob_record(1, "first", b"one")?,
            blob_record(2, "second", b"two")?,
        ])?;
        let second = second_record_offset(&duplicate)?;
        duplicate[second..second + 4].copy_from_slice(&1u32.to_le_bytes());
        assert_eq!(
            AssetRuntime::open_bytes(generation(1)?, &duplicate, RuntimeLimits::schema_v1()).err(),
            Some(RuntimeError::Asset(AssetError::DuplicateId))
        );

        let mut oversized = encoded_pack(vec![blob_record(1, "large", b"one")?])?;
        let payload_length_offset = second_record_offset(&oversized)?
            .checked_sub(7)
            .ok_or_else(|| io::Error::other("invalid test payload offset"))?;
        oversized[payload_length_offset..payload_length_offset + 4]
            .copy_from_slice(&u32::MAX.to_le_bytes());
        assert_eq!(
            AssetRuntime::open_bytes(generation(1)?, &oversized, RuntimeLimits::schema_v1()).err(),
            Some(RuntimeError::Asset(AssetError::PayloadTooLarge))
        );
        Ok(())
    }

    #[test]
    fn configured_limits_narrow_schema_limits() -> Result<(), Box<dyn std::error::Error>> {
        let encoded = encoded_pack(vec![blob_record(1, "limited", b"1234")?])?;
        let record_limit = RuntimeLimits::new(MAX_PACK_BYTES, 0, MAX_ASSET_BYTES)?;
        assert_eq!(
            AssetRuntime::open_bytes(generation(1)?, &encoded, record_limit),
            Err(RuntimeError::TooManyRecords)
        );

        let payload_limit = RuntimeLimits::new(MAX_PACK_BYTES, MAX_RECORDS, 3)?;
        assert_eq!(
            AssetRuntime::open_bytes(generation(1)?, &encoded, payload_limit),
            Err(RuntimeError::PayloadTooLarge)
        );

        let byte_limit = RuntimeLimits::new(encoded.len() - 1, MAX_RECORDS, MAX_ASSET_BYTES)?;
        assert_eq!(
            AssetRuntime::open_bytes(generation(1)?, &encoded, byte_limit),
            Err(RuntimeError::ObjectTooLarge)
        );
        Ok(())
    }

    struct FailingReader;

    impl Read for FailingReader {
        fn read(&mut self, _buffer: &mut [u8]) -> io::Result<usize> {
            Err(io::Error::other("synthetic read failure"))
        }
    }

    #[test]
    fn reader_failure_and_invalid_configuration_are_stable() -> Result<(), RuntimeError> {
        assert_eq!(PackGeneration::new(0), Err(RuntimeError::InvalidGeneration));
        assert_eq!(
            RuntimeLimits::new(0, MAX_RECORDS, MAX_ASSET_BYTES),
            Err(RuntimeError::InvalidLimits)
        );
        assert_eq!(
            AssetRuntime::open_reader(generation(1)?, FailingReader, RuntimeLimits::schema_v1())
                .err(),
            Some(RuntimeError::ObjectUnavailable)
        );
        Ok(())
    }

    #[test]
    fn debug_output_does_not_expose_metadata_or_payload() -> Result<(), Box<dyn std::error::Error>>
    {
        let encoded = encoded_pack(vec![blob_record(
            1,
            "secret-logical-name",
            b"secret-payload",
        )?])?;
        let runtime =
            AssetRuntime::open_bytes(generation(1)?, &encoded, RuntimeLimits::schema_v1())?;
        let rendered = format!("{runtime:?}");
        assert!(!rendered.contains("secret-logical-name"));
        assert!(!rendered.contains("secret-payload"));
        Ok(())
    }
}
