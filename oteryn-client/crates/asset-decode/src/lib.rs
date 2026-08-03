//! Bounded CPU normalization for verified synthetic-v1 RGBA8 assets.
//!
//! The public API accepts only an immutable [`AssetRuntime`] and a
//! generation-fenced [`AssetHandle`]. It performs no filesystem, network, GPU,
//! renderer-cache or application work.

use oteryn_asset_runtime::{AssetHandle, AssetRuntime, RuntimeError};
use oteryn_asset_types::{AssetKind, MAX_ASSET_BYTES, MAX_IMAGE_DIMENSION};
use std::error::Error;
use std::fmt::{self, Debug, Display, Formatter};

/// Byte count of one tightly packed RGBA8 pixel.
pub const RGBA8_BYTES_PER_PIXEL: usize = 4;
/// Maximum decoded byte count accepted by the synthetic-v1 decoder.
pub const MAX_DECODED_RGBA8_BYTES: usize = MAX_ASSET_BYTES;
/// Maximum decoded pixel count accepted by the synthetic-v1 decoder.
pub const MAX_DECODED_RGBA8_PIXELS: usize = MAX_DECODED_RGBA8_BYTES / RGBA8_BYTES_PER_PIXEL;

/// Runtime decode bounds that may only narrow the synthetic-v1 schema limits.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct DecodeLimits {
    max_width: u32,
    max_height: u32,
    max_pixels: usize,
    max_decoded_bytes: usize,
}

impl DecodeLimits {
    /// Return the complete bounded synthetic-v1 RGBA8 decode limits.
    #[must_use]
    pub const fn synthetic_v1() -> Self {
        Self {
            max_width: MAX_IMAGE_DIMENSION,
            max_height: MAX_IMAGE_DIMENSION,
            max_pixels: MAX_DECODED_RGBA8_PIXELS,
            max_decoded_bytes: MAX_DECODED_RGBA8_BYTES,
        }
    }

    /// Construct narrower decode limits.
    ///
    /// # Errors
    ///
    /// Returns [`DecodeError::InvalidLimits`] when any value is zero or exceeds
    /// the accepted synthetic-v1 bounds.
    pub fn new(
        max_width: u32,
        max_height: u32,
        max_pixels: usize,
        max_decoded_bytes: usize,
    ) -> Result<Self, DecodeError> {
        if max_width == 0
            || max_height == 0
            || max_pixels == 0
            || max_decoded_bytes == 0
            || max_width > MAX_IMAGE_DIMENSION
            || max_height > MAX_IMAGE_DIMENSION
            || max_pixels > MAX_DECODED_RGBA8_PIXELS
            || max_decoded_bytes > MAX_DECODED_RGBA8_BYTES
        {
            return Err(DecodeError::InvalidLimits);
        }

        Ok(Self {
            max_width,
            max_height,
            max_pixels,
            max_decoded_bytes,
        })
    }

    /// Return the maximum accepted image width.
    #[must_use]
    pub const fn max_width(self) -> u32 {
        self.max_width
    }

    /// Return the maximum accepted image height.
    #[must_use]
    pub const fn max_height(self) -> u32 {
        self.max_height
    }

    /// Return the maximum accepted pixel count.
    #[must_use]
    pub const fn max_pixels(self) -> usize {
        self.max_pixels
    }

    /// Return the maximum accepted decoded allocation size.
    #[must_use]
    pub const fn max_decoded_bytes(self) -> usize {
        self.max_decoded_bytes
    }
}

impl Default for DecodeLimits {
    fn default() -> Self {
        Self::synthetic_v1()
    }
}

/// Immutable owned tightly packed RGBA8 image data.
#[derive(Clone, PartialEq, Eq)]
pub struct DecodedRgba8 {
    width: u32,
    height: u32,
    pixel_count: usize,
    row_pitch_bytes: usize,
    pixels: Box<[u8]>,
}

impl DecodedRgba8 {
    /// Return the image width in pixels.
    #[must_use]
    pub const fn width(&self) -> u32 {
        self.width
    }

    /// Return the image height in pixels.
    #[must_use]
    pub const fn height(&self) -> u32 {
        self.height
    }

    /// Return the total pixel count.
    #[must_use]
    pub const fn pixel_count(&self) -> usize {
        self.pixel_count
    }

    /// Return the tightly packed row pitch in bytes.
    #[must_use]
    pub const fn row_pitch_bytes(&self) -> usize {
        self.row_pitch_bytes
    }

    /// Return the owned immutable RGBA8 bytes.
    #[must_use]
    pub fn pixels(&self) -> &[u8] {
        &self.pixels
    }

    /// Return the decoded allocation size in bytes.
    #[must_use]
    pub fn byte_len(&self) -> usize {
        self.pixels.len()
    }
}

impl Debug for DecodedRgba8 {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("DecodedRgba8")
            .field("width", &self.width)
            .field("height", &self.height)
            .field("pixel_count", &self.pixel_count)
            .field("row_pitch_bytes", &self.row_pitch_bytes)
            .field("byte_len", &self.byte_len())
            .finish_non_exhaustive()
    }
}

/// Stable payload-redacted failures produced by RGBA8 normalization.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DecodeError {
    /// Configured decode limits are zero or exceed synthetic-v1 bounds.
    InvalidLimits,
    /// Runtime lookup rejected the generation-fenced handle.
    Runtime(RuntimeError),
    /// The verified record is not an RGBA8 image.
    UnsupportedAssetKind,
    /// Width or height is zero.
    InvalidDimensions,
    /// Checked layout arithmetic could not be represented.
    ArithmeticOverflow,
    /// Width or height exceeds configured decode limits.
    DimensionLimitExceeded,
    /// Pixel count exceeds the configured decode limit.
    PixelLimitExceeded,
    /// Decoded bytes exceed the configured allocation limit.
    DecodedBytesLimitExceeded,
    /// Payload length is not exactly the checked RGBA8 layout length.
    PayloadLengthMismatch,
}

impl Display for DecodeError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        let message = match self {
            Self::InvalidLimits => "asset decode limits are invalid",
            Self::Runtime(error) => return Display::fmt(error, formatter),
            Self::UnsupportedAssetKind => "asset is not a supported RGBA8 image",
            Self::InvalidDimensions => "RGBA8 dimensions must be non-zero",
            Self::ArithmeticOverflow => "RGBA8 layout arithmetic overflowed",
            Self::DimensionLimitExceeded => "RGBA8 dimensions exceed the decode limit",
            Self::PixelLimitExceeded => "RGBA8 pixel count exceeds the decode limit",
            Self::DecodedBytesLimitExceeded => "RGBA8 decoded bytes exceed the allocation limit",
            Self::PayloadLengthMismatch => "RGBA8 payload length does not match its layout",
        };
        formatter.write_str(message)
    }
}

impl Error for DecodeError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::Runtime(error) => Some(error),
            _ => None,
        }
    }
}

impl From<RuntimeError> for DecodeError {
    fn from(value: RuntimeError) -> Self {
        Self::Runtime(value)
    }
}

/// Resolve and normalize one verified synthetic-v1 RGBA8 asset.
///
/// All shape and allocation checks complete before the output copy is
/// allocated. The returned value owns its bytes and does not borrow or alias
/// mutable runtime payload storage.
///
/// # Errors
///
/// Returns a stable decode error for stale/unknown handles, opaque blobs,
/// invalid or over-limit layouts and non-exact payload lengths.
pub fn decode_rgba8(
    runtime: &AssetRuntime,
    handle: AssetHandle,
    limits: DecodeLimits,
) -> Result<DecodedRgba8, DecodeError> {
    let view = runtime.lookup(handle)?;
    normalize_rgba8(view.kind(), view.payload(), limits)
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct CheckedLayout {
    pixel_count: usize,
    row_pitch_bytes: usize,
    expected_bytes: usize,
}

fn checked_layout(width: u32, height: u32) -> Result<CheckedLayout, DecodeError> {
    if width == 0 || height == 0 {
        return Err(DecodeError::InvalidDimensions);
    }

    let width = usize::try_from(width).map_err(|_| DecodeError::ArithmeticOverflow)?;
    let height = usize::try_from(height).map_err(|_| DecodeError::ArithmeticOverflow)?;
    let pixel_count = width
        .checked_mul(height)
        .ok_or(DecodeError::ArithmeticOverflow)?;
    let row_pitch_bytes = width
        .checked_mul(RGBA8_BYTES_PER_PIXEL)
        .ok_or(DecodeError::ArithmeticOverflow)?;
    let expected_bytes = row_pitch_bytes
        .checked_mul(height)
        .ok_or(DecodeError::ArithmeticOverflow)?;

    Ok(CheckedLayout {
        pixel_count,
        row_pitch_bytes,
        expected_bytes,
    })
}

fn normalize_rgba8(
    kind: AssetKind,
    payload: &[u8],
    limits: DecodeLimits,
) -> Result<DecodedRgba8, DecodeError> {
    let AssetKind::Rgba8 { width, height } = kind else {
        return Err(DecodeError::UnsupportedAssetKind);
    };

    let layout = checked_layout(width, height)?;
    if width > limits.max_width || height > limits.max_height {
        return Err(DecodeError::DimensionLimitExceeded);
    }
    if layout.pixel_count > limits.max_pixels {
        return Err(DecodeError::PixelLimitExceeded);
    }
    if layout.expected_bytes > limits.max_decoded_bytes {
        return Err(DecodeError::DecodedBytesLimitExceeded);
    }
    if payload.len() != layout.expected_bytes {
        return Err(DecodeError::PayloadLengthMismatch);
    }

    let pixels = payload.to_vec().into_boxed_slice();
    Ok(DecodedRgba8 {
        width,
        height,
        pixel_count: layout.pixel_count,
        row_pitch_bytes: layout.row_pitch_bytes,
        pixels,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use oteryn_asset_compiler::compile_manifest;
    use oteryn_asset_runtime::{PackGeneration, RuntimeLimits};
    use oteryn_asset_types::{
        AssetError, AssetId, AssetMetadata, AssetPack, AssetRecord, MAX_ASSET_BYTES,
    };
    use std::fs;
    use std::io;
    use std::path::{Path, PathBuf};
    use std::sync::atomic::{AtomicU64, Ordering};

    static TEMP_COUNTER: AtomicU64 = AtomicU64::new(0);

    struct TestDirectory {
        path: PathBuf,
    }

    impl TestDirectory {
        fn new() -> io::Result<Self> {
            let counter = TEMP_COUNTER.fetch_add(1, Ordering::Relaxed);
            let path = std::env::temp_dir().join(format!(
                "oteryn-asset-decode-{}-{counter}",
                std::process::id()
            ));
            fs::create_dir(&path)?;
            Ok(Self { path })
        }

        fn path(&self) -> &Path {
            &self.path
        }
    }

    impl Drop for TestDirectory {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.path);
        }
    }

    fn generation(value: u64) -> Result<PackGeneration, RuntimeError> {
        PackGeneration::new(value)
    }

    fn record(
        id: u32,
        kind: AssetKind,
        name: &str,
        payload: Vec<u8>,
    ) -> Result<AssetRecord, AssetError> {
        let metadata = AssetMetadata::new(
            AssetId::new(id)?,
            kind,
            name.to_owned(),
            "CC0-1.0".to_owned(),
            "project-original synthetic fixture".to_owned(),
        )?;
        AssetRecord::new(metadata, payload)
    }

    fn runtime(
        generation_value: u64,
        records: Vec<AssetRecord>,
    ) -> Result<AssetRuntime, Box<dyn Error>> {
        let encoded = AssetPack::new(records)?.encode()?;
        Ok(AssetRuntime::open_bytes(
            generation(generation_value)?,
            &encoded,
            RuntimeLimits::schema_v1(),
        )?)
    }

    #[test]
    fn decodes_owned_byte_identical_rgba8() -> Result<(), Box<dyn Error>> {
        let payload = vec![1, 2, 3, 4, 5, 6, 7, 8];
        let runtime = runtime(
            7,
            vec![record(
                9,
                AssetKind::Rgba8 {
                    width: 2,
                    height: 1,
                },
                "two-pixels",
                payload.clone(),
            )?],
        )?;
        let handle = runtime
            .handle(AssetId::new(9)?)
            .ok_or_else(|| io::Error::other("missing expected handle"))?;

        let first = decode_rgba8(&runtime, handle, DecodeLimits::synthetic_v1())?;
        let second = decode_rgba8(&runtime, handle, DecodeLimits::synthetic_v1())?;
        assert_eq!(first, second);
        assert_eq!(first.width(), 2);
        assert_eq!(first.height(), 1);
        assert_eq!(first.pixel_count(), 2);
        assert_eq!(first.row_pitch_bytes(), 8);
        assert_eq!(first.byte_len(), 8);
        assert_eq!(first.pixels(), payload.as_slice());

        drop(runtime);
        assert_eq!(first.pixels(), payload.as_slice());
        Ok(())
    }

    #[test]
    fn opaque_blob_is_rejected_explicitly() -> Result<(), Box<dyn Error>> {
        let runtime = runtime(
            1,
            vec![record(1, AssetKind::Blob, "opaque", vec![1, 2, 3, 4])?],
        )?;
        let handle = runtime
            .handle(AssetId::new(1)?)
            .ok_or_else(|| io::Error::other("missing expected handle"))?;
        assert_eq!(
            decode_rgba8(&runtime, handle, DecodeLimits::synthetic_v1()).err(),
            Some(DecodeError::UnsupportedAssetKind)
        );
        Ok(())
    }

    #[test]
    fn stale_generation_fails_closed() -> Result<(), Box<dyn Error>> {
        let records = vec![record(
            3,
            AssetKind::Rgba8 {
                width: 1,
                height: 1,
            },
            "pixel",
            vec![1, 2, 3, 4],
        )?];
        let old = runtime(10, records.clone())?;
        let handle = old
            .handle(AssetId::new(3)?)
            .ok_or_else(|| io::Error::other("missing expected handle"))?;
        let current = runtime(11, records)?;

        assert_eq!(
            decode_rgba8(&current, handle, DecodeLimits::synthetic_v1()).err(),
            Some(DecodeError::Runtime(RuntimeError::StaleHandle))
        );
        Ok(())
    }

    #[test]
    fn unsupported_schema_fails_before_decode() -> Result<(), Box<dyn Error>> {
        let mut encoded = AssetPack::new(vec![record(
            8,
            AssetKind::Rgba8 {
                width: 1,
                height: 1,
            },
            "schema-fence",
            vec![1, 2, 3, 4],
        )?])?
        .encode()?;
        encoded[8..10].copy_from_slice(&2_u16.to_le_bytes());

        assert_eq!(
            AssetRuntime::open_bytes(generation(12)?, &encoded, RuntimeLimits::schema_v1(),).err(),
            Some(RuntimeError::Asset(AssetError::UnsupportedVersion))
        );
        Ok(())
    }

    #[test]
    fn limits_are_validated_and_applied_before_copy() -> Result<(), Box<dyn Error>> {
        assert_eq!(
            DecodeLimits::new(0, 1, 1, 4),
            Err(DecodeError::InvalidLimits)
        );
        assert_eq!(
            DecodeLimits::new(MAX_IMAGE_DIMENSION + 1, 1, 1, 4),
            Err(DecodeError::InvalidLimits)
        );

        let limits = DecodeLimits::new(2, 2, 4, 15)?;
        assert_eq!(
            normalize_rgba8(
                AssetKind::Rgba8 {
                    width: 2,
                    height: 2,
                },
                &[0; 16],
                limits,
            ),
            Err(DecodeError::DecodedBytesLimitExceeded)
        );
        Ok(())
    }

    #[test]
    fn zero_overflow_truncated_and_trailing_layouts_fail_deterministically() {
        let limits = DecodeLimits::synthetic_v1();
        assert_eq!(
            normalize_rgba8(
                AssetKind::Rgba8 {
                    width: 0,
                    height: 1,
                },
                &[],
                limits,
            ),
            Err(DecodeError::InvalidDimensions)
        );
        assert_eq!(
            checked_layout(u32::MAX, u32::MAX),
            Err(DecodeError::ArithmeticOverflow)
        );
        assert_eq!(
            normalize_rgba8(
                AssetKind::Rgba8 {
                    width: 2,
                    height: 2,
                },
                &[0; 15],
                limits,
            ),
            Err(DecodeError::PayloadLengthMismatch)
        );
        assert_eq!(
            normalize_rgba8(
                AssetKind::Rgba8 {
                    width: 2,
                    height: 2,
                },
                &[0; 17],
                limits,
            ),
            Err(DecodeError::PayloadLengthMismatch)
        );
    }

    #[test]
    fn accepts_the_exact_synthetic_v1_allocation_maximum() -> Result<(), Box<dyn Error>> {
        let width = MAX_IMAGE_DIMENSION;
        let height = u32::try_from(MAX_DECODED_RGBA8_PIXELS / usize::try_from(width)?)?;
        let payload = vec![0xA5; MAX_ASSET_BYTES];
        let runtime = runtime(
            5,
            vec![record(
                4,
                AssetKind::Rgba8 { width, height },
                "maximum",
                payload,
            )?],
        )?;
        let handle = runtime
            .handle(AssetId::new(4)?)
            .ok_or_else(|| io::Error::other("missing expected handle"))?;
        let decoded = decode_rgba8(&runtime, handle, DecodeLimits::synthetic_v1())?;

        assert_eq!(decoded.width(), MAX_IMAGE_DIMENSION);
        assert_eq!(decoded.height(), 256);
        assert_eq!(decoded.pixel_count(), MAX_DECODED_RGBA8_PIXELS);
        assert_eq!(decoded.byte_len(), MAX_DECODED_RGBA8_BYTES);
        Ok(())
    }

    #[test]
    fn debug_and_display_output_reveal_no_payload_bytes() -> Result<(), Box<dyn Error>> {
        let secret_like_payload = b"do-not-print-this".to_vec();
        let decoded = normalize_rgba8(
            AssetKind::Rgba8 {
                width: 4,
                height: 1,
            },
            &secret_like_payload[..16],
            DecodeLimits::synthetic_v1(),
        )?;
        let debug = format!("{decoded:?}");
        assert!(!debug.contains("do-not-print"));
        assert_eq!(
            DecodeError::PayloadLengthMismatch.to_string(),
            "RGBA8 payload length does not match its layout"
        );
        Ok(())
    }

    #[test]
    fn compiler_runtime_decode_component_round_trip() -> Result<(), Box<dyn Error>> {
        let directory = TestDirectory::new()?;
        let payload_path = directory.path().join("pixels.rgba");
        let manifest_path = directory.path().join("manifest.json");
        let pack_path = directory.path().join("assets.pack");
        fs::write(&payload_path, [1_u8, 2, 3, 4, 5, 6, 7, 8])?;
        fs::write(
            &manifest_path,
            r#"{
  "schema_version": 1,
  "assets": [
    {
      "id": 42,
      "kind": "rgba8",
      "name": "component-pixels",
      "source": "pixels.rgba",
      "license": "CC0-1.0",
      "provenance": "project-original synthetic fixture",
      "width": 2,
      "height": 1
    }
  ]
}"#,
        )?;

        let report = compile_manifest(&manifest_path, &pack_path)?;
        assert_eq!(report.record_count(), 1);
        let encoded = fs::read(&pack_path)?;
        assert_eq!(report.encoded_bytes(), encoded.len());
        let runtime =
            AssetRuntime::open_bytes(generation(99)?, &encoded, RuntimeLimits::schema_v1())?;
        let handle = runtime
            .handle(AssetId::new(42)?)
            .ok_or_else(|| io::Error::other("missing expected handle"))?;
        let decoded = decode_rgba8(&runtime, handle, DecodeLimits::synthetic_v1())?;
        assert_eq!(decoded.pixels(), &[1, 2, 3, 4, 5, 6, 7, 8]);
        Ok(())
    }
}
