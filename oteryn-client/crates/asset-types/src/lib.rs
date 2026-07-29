//! Bounded synthetic asset identifiers, metadata and deterministic pack encoding.

use sha2::{Digest, Sha256};
use std::error::Error;
use std::fmt::{self, Display, Formatter};
use std::num::NonZeroU32;

/// Current original Oteryn synthetic pack schema version.
pub const PACK_SCHEMA_VERSION: u16 = 1;
/// Maximum number of records accepted by schema version 1.
pub const MAX_RECORDS: usize = 4_096;
/// Maximum payload size for one synthetic record.
pub const MAX_ASSET_BYTES: usize = 16 * 1024 * 1024;
/// Maximum encoded pack size.
pub const MAX_PACK_BYTES: usize = 64 * 1024 * 1024;
/// Maximum RGBA8 image width or height.
pub const MAX_IMAGE_DIMENSION: u32 = 16_384;
/// Maximum UTF-8 byte length of a logical asset name.
pub const MAX_LOGICAL_NAME_BYTES: usize = 128;
/// Maximum UTF-8 byte length of a license identifier.
pub const MAX_LICENSE_BYTES: usize = 64;
/// Maximum UTF-8 byte length of provenance text.
pub const MAX_PROVENANCE_BYTES: usize = 512;

const PACK_MAGIC: [u8; 8] = *b"OTASSET1";
const SHA256_BYTES: usize = 32;

/// Stable non-zero identifier for one normalized asset record.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct AssetId(NonZeroU32);

impl AssetId {
    /// Construct an asset identifier.
    ///
    /// # Errors
    ///
    /// Returns [`AssetError::InvalidId`] for zero.
    pub fn new(value: u32) -> Result<Self, AssetError> {
        NonZeroU32::new(value)
            .map(Self)
            .ok_or(AssetError::InvalidId)
    }

    /// Return the numeric identifier.
    #[must_use]
    pub const fn get(self) -> u32 {
        self.0.get()
    }
}

/// Closed set of synthetic asset kinds supported by schema version 1.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AssetKind {
    /// An opaque bounded binary payload.
    Blob,
    /// Raw tightly packed RGBA8 pixels.
    Rgba8 { width: u32, height: u32 },
}

impl AssetKind {
    const fn code(self) -> u8 {
        match self {
            Self::Blob => 1,
            Self::Rgba8 { .. } => 2,
        }
    }

    fn dimensions(self) -> (u32, u32) {
        match self {
            Self::Blob => (0, 0),
            Self::Rgba8 { width, height } => (width, height),
        }
    }

    fn validate_payload(self, payload_len: usize) -> Result<(), AssetError> {
        if payload_len > MAX_ASSET_BYTES {
            return Err(AssetError::PayloadTooLarge);
        }

        match self {
            Self::Blob => Ok(()),
            Self::Rgba8 { width, height } => {
                if width == 0
                    || height == 0
                    || width > MAX_IMAGE_DIMENSION
                    || height > MAX_IMAGE_DIMENSION
                {
                    return Err(AssetError::InvalidDimensions);
                }

                let pixels = u64::from(width)
                    .checked_mul(u64::from(height))
                    .and_then(|value| value.checked_mul(4))
                    .ok_or(AssetError::ArithmeticOverflow)?;
                let expected = usize::try_from(pixels)
                    .map_err(|_| AssetError::ArithmeticOverflow)?;
                if expected != payload_len {
                    return Err(AssetError::PayloadLengthMismatch);
                }
                Ok(())
            }
        }
    }
}

/// Validated metadata stored with one asset payload.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AssetMetadata {
    id: AssetId,
    kind: AssetKind,
    logical_name: String,
    license: String,
    provenance: String,
}

impl AssetMetadata {
    /// Construct validated metadata.
    ///
    /// # Errors
    ///
    /// Returns a bounded metadata error when a string is empty, contains a
    /// control character or exceeds its schema-v1 limit.
    pub fn new(
        id: AssetId,
        kind: AssetKind,
        logical_name: String,
        license: String,
        provenance: String,
    ) -> Result<Self, AssetError> {
        validate_text(&logical_name, MAX_LOGICAL_NAME_BYTES)?;
        validate_text(&license, MAX_LICENSE_BYTES)?;
        validate_text(&provenance, MAX_PROVENANCE_BYTES)?;
        Ok(Self {
            id,
            kind,
            logical_name,
            license,
            provenance,
        })
    }

    /// Return the stable identifier.
    #[must_use]
    pub const fn id(&self) -> AssetId {
        self.id
    }

    /// Return the normalized kind.
    #[must_use]
    pub const fn kind(&self) -> AssetKind {
        self.kind
    }

    /// Return the logical name.
    #[must_use]
    pub fn logical_name(&self) -> &str {
        &self.logical_name
    }

    /// Return the license identifier.
    #[must_use]
    pub fn license(&self) -> &str {
        &self.license
    }

    /// Return the provenance statement.
    #[must_use]
    pub fn provenance(&self) -> &str {
        &self.provenance
    }
}

/// One validated metadata and payload record.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AssetRecord {
    metadata: AssetMetadata,
    digest: [u8; SHA256_BYTES],
    payload: Vec<u8>,
}

impl AssetRecord {
    /// Validate one payload and calculate its SHA-256 digest.
    ///
    /// # Errors
    ///
    /// Returns an asset error for an oversized payload or invalid RGBA8 shape.
    pub fn new(metadata: AssetMetadata, payload: Vec<u8>) -> Result<Self, AssetError> {
        metadata.kind.validate_payload(payload.len())?;
        let digest: [u8; SHA256_BYTES] = Sha256::digest(&payload).into();
        Ok(Self {
            metadata,
            digest,
            payload,
        })
    }

    /// Return validated metadata.
    #[must_use]
    pub const fn metadata(&self) -> &AssetMetadata {
        &self.metadata
    }

    /// Return the SHA-256 digest.
    #[must_use]
    pub const fn digest(&self) -> &[u8; SHA256_BYTES] {
        &self.digest
    }

    /// Return the payload.
    #[must_use]
    pub fn payload(&self) -> &[u8] {
        &self.payload
    }
}

/// Canonically ordered collection of validated asset records.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AssetPack {
    records: Vec<AssetRecord>,
}

impl AssetPack {
    /// Sort records by identifier and reject duplicate identifiers.
    ///
    /// # Errors
    ///
    /// Returns an asset error when the record count is too large or an ID is
    /// duplicated.
    pub fn new(mut records: Vec<AssetRecord>) -> Result<Self, AssetError> {
        if records.len() > MAX_RECORDS {
            return Err(AssetError::TooManyRecords);
        }

        records.sort_by_key(|record| record.metadata.id);
        for pair in records.windows(2) {
            if let [left, right] = pair
                && left.metadata.id == right.metadata.id
            {
                return Err(AssetError::DuplicateId);
            }
        }

        Ok(Self { records })
    }

    /// Return canonically ordered records.
    #[must_use]
    pub fn records(&self) -> &[AssetRecord] {
        &self.records
    }

    /// Encode the original deterministic schema-v1 pack format.
    ///
    /// # Errors
    ///
    /// Returns an asset error when a length conversion or pack-size bound is
    /// exceeded.
    pub fn encode(&self) -> Result<Vec<u8>, AssetError> {
        let mut encoded = Vec::new();
        append_bytes(&mut encoded, &PACK_MAGIC)?;
        append_bytes(&mut encoded, &PACK_SCHEMA_VERSION.to_le_bytes())?;
        let record_count = u32::try_from(self.records.len())
            .map_err(|_| AssetError::TooManyRecords)?;
        append_bytes(&mut encoded, &record_count.to_le_bytes())?;

        for record in &self.records {
            append_bytes(&mut encoded, &record.metadata.id.get().to_le_bytes())?;
            append_bytes(&mut encoded, &[record.metadata.kind.code()])?;
            let (width, height) = record.metadata.kind.dimensions();
            append_bytes(&mut encoded, &width.to_le_bytes())?;
            append_bytes(&mut encoded, &height.to_le_bytes())?;
            append_text(&mut encoded, &record.metadata.logical_name)?;
            append_text(&mut encoded, &record.metadata.license)?;
            append_text(&mut encoded, &record.metadata.provenance)?;
            append_bytes(&mut encoded, &record.digest)?;
            let payload_len = u32::try_from(record.payload.len())
                .map_err(|_| AssetError::PayloadTooLarge)?;
            append_bytes(&mut encoded, &payload_len.to_le_bytes())?;
            append_bytes(&mut encoded, &record.payload)?;
        }

        Ok(encoded)
    }

    /// Decode and fully validate one canonical schema-v1 pack.
    ///
    /// # Errors
    ///
    /// Returns an asset error for malformed, oversized, non-canonical or
    /// digest-mismatched input.
    pub fn decode(encoded: &[u8]) -> Result<Self, AssetError> {
        if encoded.len() > MAX_PACK_BYTES {
            return Err(AssetError::PackTooLarge);
        }

        let mut decoder = Decoder::new(encoded);
        if decoder.read_array::<8>()? != PACK_MAGIC {
            return Err(AssetError::MalformedPack);
        }
        if decoder.read_u16()? != PACK_SCHEMA_VERSION {
            return Err(AssetError::UnsupportedVersion);
        }

        let count = usize::try_from(decoder.read_u32()?)
            .map_err(|_| AssetError::ArithmeticOverflow)?;
        if count > MAX_RECORDS {
            return Err(AssetError::TooManyRecords);
        }

        let mut records = Vec::with_capacity(count);
        let mut previous_id = None;
        for _ in 0..count {
            let id = AssetId::new(decoder.read_u32()?)?;
            if let Some(previous) = previous_id {
                if id == previous {
                    return Err(AssetError::DuplicateId);
                }
                if id < previous {
                    return Err(AssetError::NonCanonicalOrder);
                }
            }
            previous_id = Some(id);

            let kind_code = decoder.read_u8()?;
            let width = decoder.read_u32()?;
            let height = decoder.read_u32()?;
            let kind = match kind_code {
                1 if width == 0 && height == 0 => AssetKind::Blob,
                2 => AssetKind::Rgba8 { width, height },
                1 => return Err(AssetError::MalformedPack),
                _ => return Err(AssetError::UnknownKind),
            };
            let logical_name = decoder.read_text(MAX_LOGICAL_NAME_BYTES)?;
            let license = decoder.read_text(MAX_LICENSE_BYTES)?;
            let provenance = decoder.read_text(MAX_PROVENANCE_BYTES)?;
            let expected_digest = decoder.read_array::<SHA256_BYTES>()?;
            let payload_len = usize::try_from(decoder.read_u32()?)
                .map_err(|_| AssetError::ArithmeticOverflow)?;
            if payload_len > MAX_ASSET_BYTES {
                return Err(AssetError::PayloadTooLarge);
            }
            let payload = decoder.read_bytes(payload_len)?.to_vec();
            let metadata = AssetMetadata::new(id, kind, logical_name, license, provenance)?;
            let record = AssetRecord::new(metadata, payload)?;
            if record.digest != expected_digest {
                return Err(AssetError::DigestMismatch);
            }
            records.push(record);
        }

        if !decoder.is_finished() {
            return Err(AssetError::TrailingBytes);
        }
        Ok(Self { records })
    }
}

/// Stable validation and decoding failures for the synthetic asset contract.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AssetError {
    InvalidId,
    EmptyText,
    TextTooLong,
    ControlCharacter,
    TooManyRecords,
    DuplicateId,
    NonCanonicalOrder,
    PayloadTooLarge,
    PackTooLarge,
    InvalidDimensions,
    PayloadLengthMismatch,
    ArithmeticOverflow,
    UnsupportedVersion,
    UnknownKind,
    MalformedPack,
    InvalidUtf8,
    DigestMismatch,
    TrailingBytes,
}

impl Display for AssetError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        let message = match self {
            Self::InvalidId => "asset ID must be non-zero",
            Self::EmptyText => "required asset text is empty",
            Self::TextTooLong => "asset text exceeds the schema limit",
            Self::ControlCharacter => "asset text contains a control character",
            Self::TooManyRecords => "asset record count exceeds the schema limit",
            Self::DuplicateId => "asset ID is duplicated",
            Self::NonCanonicalOrder => "asset records are not canonically ordered",
            Self::PayloadTooLarge => "asset payload exceeds the schema limit",
            Self::PackTooLarge => "asset pack exceeds the schema limit",
            Self::InvalidDimensions => "RGBA8 dimensions are invalid",
            Self::PayloadLengthMismatch => "payload length does not match the asset kind",
            Self::ArithmeticOverflow => "asset arithmetic overflow",
            Self::UnsupportedVersion => "asset pack schema version is unsupported",
            Self::UnknownKind => "asset kind is unknown",
            Self::MalformedPack => "asset pack is malformed",
            Self::InvalidUtf8 => "asset text is not valid UTF-8",
            Self::DigestMismatch => "asset payload digest does not match",
            Self::TrailingBytes => "asset pack contains trailing bytes",
        };
        formatter.write_str(message)
    }
}

impl Error for AssetError {}

fn validate_text(value: &str, limit: usize) -> Result<(), AssetError> {
    if value.is_empty() {
        return Err(AssetError::EmptyText);
    }
    if value.len() > limit {
        return Err(AssetError::TextTooLong);
    }
    if value.chars().any(char::is_control) {
        return Err(AssetError::ControlCharacter);
    }
    Ok(())
}

fn append_text(encoded: &mut Vec<u8>, value: &str) -> Result<(), AssetError> {
    let length = u16::try_from(value.len()).map_err(|_| AssetError::TextTooLong)?;
    append_bytes(encoded, &length.to_le_bytes())?;
    append_bytes(encoded, value.as_bytes())
}

fn append_bytes(encoded: &mut Vec<u8>, value: &[u8]) -> Result<(), AssetError> {
    let final_len = encoded
        .len()
        .checked_add(value.len())
        .ok_or(AssetError::ArithmeticOverflow)?;
    if final_len > MAX_PACK_BYTES {
        return Err(AssetError::PackTooLarge);
    }
    encoded.extend_from_slice(value);
    Ok(())
}

struct Decoder<'a> {
    encoded: &'a [u8],
    offset: usize,
}

impl<'a> Decoder<'a> {
    const fn new(encoded: &'a [u8]) -> Self {
        Self { encoded, offset: 0 }
    }

    fn read_u8(&mut self) -> Result<u8, AssetError> {
        Ok(self.read_array::<1>()?[0])
    }

    fn read_u16(&mut self) -> Result<u16, AssetError> {
        Ok(u16::from_le_bytes(self.read_array::<2>()?))
    }

    fn read_u32(&mut self) -> Result<u32, AssetError> {
        Ok(u32::from_le_bytes(self.read_array::<4>()?))
    }

    fn read_array<const LENGTH: usize>(&mut self) -> Result<[u8; LENGTH], AssetError> {
        let bytes = self.read_bytes(LENGTH)?;
        <[u8; LENGTH]>::try_from(bytes).map_err(|_| AssetError::MalformedPack)
    }

    fn read_text(&mut self, limit: usize) -> Result<String, AssetError> {
        let length = usize::from(self.read_u16()?);
        if length > limit {
            return Err(AssetError::TextTooLong);
        }
        String::from_utf8(self.read_bytes(length)?.to_vec())
            .map_err(|_| AssetError::InvalidUtf8)
    }

    fn read_bytes(&mut self, length: usize) -> Result<&'a [u8], AssetError> {
        let end = self
            .offset
            .checked_add(length)
            .ok_or(AssetError::ArithmeticOverflow)?;
        let bytes = self
            .encoded
            .get(self.offset..end)
            .ok_or(AssetError::MalformedPack)?;
        self.offset = end;
        Ok(bytes)
    }

    const fn is_finished(&self) -> bool {
        self.offset == self.encoded.len()
    }
}
