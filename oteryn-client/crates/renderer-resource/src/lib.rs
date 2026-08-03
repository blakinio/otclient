//! Bounded generation-fenced renderer resource lifecycle for synthetic-v1 RGBA8 images.
//!
//! This crate owns immutable upload plans and logical resource-cache state only.
//! It performs no filesystem access, media decode, world mutation, draw ordering,
//! protocol work, input mapping or application composition.

use oteryn_asset_decode::{DecodedRgba8, MAX_DECODED_RGBA8_BYTES, RGBA8_BYTES_PER_PIXEL};
use oteryn_asset_runtime::{AssetHandle, PackGeneration};
use oteryn_foundation::ProcessGeneration;
use std::error::Error;
use std::fmt::{self, Debug, Display, Formatter};
use std::num::{NonZeroU64, NonZeroUsize};

/// Required byte alignment for one staged texture-copy row.
pub const COPY_BYTES_PER_ROW_ALIGNMENT: usize = 256;
/// Maximum number of live synthetic renderer resources.
pub const MAX_CACHE_ENTRIES: usize = 256;
/// Maximum accounted logical device bytes for this bounded producer.
pub const MAX_CACHE_DEVICE_BYTES: usize = 64 * 1024 * 1024;
/// Maximum immutable upload-plan allocation.
pub const MAX_UPLOAD_PLAN_BYTES: usize = MAX_DECODED_RGBA8_BYTES;

/// Non-zero generation identifying one renderer device lifetime.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct DeviceGeneration(NonZeroU64);

impl DeviceGeneration {
    /// Construct a renderer device generation.
    ///
    /// # Errors
    ///
    /// Returns [`ResourceError::InvalidGeneration`] for zero.
    pub fn new(value: u64) -> Result<Self, ResourceError> {
        NonZeroU64::new(value)
            .map(Self)
            .ok_or(ResourceError::InvalidGeneration)
    }

    /// Return the numeric generation.
    #[must_use]
    pub const fn get(self) -> u64 {
        self.0.get()
    }
}

/// Backend-neutral texture format supported by the P2 synthetic producer.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum TextureFormat {
    /// Four normalized color channels in red, green, blue and alpha order.
    Rgba8UnormSrgb,
}

impl TextureFormat {
    const fn bytes_per_pixel(self) -> usize {
        match self {
            Self::Rgba8UnormSrgb => RGBA8_BYTES_PER_PIXEL,
        }
    }
}

impl Display for TextureFormat {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str(match self {
            Self::Rgba8UnormSrgb => "rgba8-unorm-srgb",
        })
    }
}

/// Runtime bounds for one renderer-resource cache.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ResourceLimits {
    max_entries: NonZeroUsize,
    max_total_device_bytes: NonZeroUsize,
    max_single_texture_bytes: NonZeroUsize,
    max_upload_plan_bytes: NonZeroUsize,
}

impl ResourceLimits {
    /// Return the accepted bounded synthetic-v1 limits.
    #[must_use]
    pub const fn synthetic_v1() -> Self {
        Self {
            max_entries: NonZeroUsize::new(MAX_CACHE_ENTRIES).expect("non-zero constant"),
            max_total_device_bytes: NonZeroUsize::new(MAX_CACHE_DEVICE_BYTES)
                .expect("non-zero constant"),
            max_single_texture_bytes: NonZeroUsize::new(MAX_DECODED_RGBA8_BYTES)
                .expect("non-zero constant"),
            max_upload_plan_bytes: NonZeroUsize::new(MAX_UPLOAD_PLAN_BYTES)
                .expect("non-zero constant"),
        }
    }

    /// Construct narrower renderer-resource limits.
    ///
    /// # Errors
    ///
    /// Returns [`ResourceError::InvalidLimits`] when a value is zero, exceeds
    /// the accepted absolute bound, or permits one texture larger than the
    /// total cache budget.
    pub fn new(
        max_entries: usize,
        max_total_device_bytes: usize,
        max_single_texture_bytes: usize,
        max_upload_plan_bytes: usize,
    ) -> Result<Self, ResourceError> {
        let max_entries = NonZeroUsize::new(max_entries).ok_or(ResourceError::InvalidLimits)?;
        let max_total_device_bytes =
            NonZeroUsize::new(max_total_device_bytes).ok_or(ResourceError::InvalidLimits)?;
        let max_single_texture_bytes =
            NonZeroUsize::new(max_single_texture_bytes).ok_or(ResourceError::InvalidLimits)?;
        let max_upload_plan_bytes =
            NonZeroUsize::new(max_upload_plan_bytes).ok_or(ResourceError::InvalidLimits)?;

        if max_entries.get() > MAX_CACHE_ENTRIES
            || max_total_device_bytes.get() > MAX_CACHE_DEVICE_BYTES
            || max_single_texture_bytes.get() > MAX_DECODED_RGBA8_BYTES
            || max_upload_plan_bytes.get() > MAX_UPLOAD_PLAN_BYTES
            || max_single_texture_bytes.get() > max_total_device_bytes.get()
        {
            return Err(ResourceError::InvalidLimits);
        }

        Ok(Self {
            max_entries,
            max_total_device_bytes,
            max_single_texture_bytes,
            max_upload_plan_bytes,
        })
    }

    /// Return the live-entry bound.
    #[must_use]
    pub const fn max_entries(self) -> usize {
        self.max_entries.get()
    }

    /// Return the total accounted device-byte bound.
    #[must_use]
    pub const fn max_total_device_bytes(self) -> usize {
        self.max_total_device_bytes.get()
    }

    /// Return the per-texture device-byte bound.
    #[must_use]
    pub const fn max_single_texture_bytes(self) -> usize {
        self.max_single_texture_bytes.get()
    }

    /// Return the immutable upload-plan allocation bound.
    #[must_use]
    pub const fn max_upload_plan_bytes(self) -> usize {
        self.max_upload_plan_bytes.get()
    }
}

impl Default for ResourceLimits {
    fn default() -> Self {
        Self::synthetic_v1()
    }
}

/// Fully checked backend-neutral RGBA8 texture layout.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TextureDescriptor {
    width: u32,
    height: u32,
    format: TextureFormat,
    source_row_pitch_bytes: usize,
    upload_row_pitch_bytes: usize,
    source_byte_len: usize,
    upload_byte_len: usize,
    device_byte_len: usize,
}

impl TextureDescriptor {
    /// Return the width in pixels.
    #[must_use]
    pub const fn width(self) -> u32 {
        self.width
    }

    /// Return the height in pixels.
    #[must_use]
    pub const fn height(self) -> u32 {
        self.height
    }

    /// Return the logical texture format.
    #[must_use]
    pub const fn format(self) -> TextureFormat {
        self.format
    }

    /// Return the tightly packed source-row byte count.
    #[must_use]
    pub const fn source_row_pitch_bytes(self) -> usize {
        self.source_row_pitch_bytes
    }

    /// Return the 256-byte-aligned upload-row byte count.
    #[must_use]
    pub const fn upload_row_pitch_bytes(self) -> usize {
        self.upload_row_pitch_bytes
    }

    /// Return the exact decoded source byte count.
    #[must_use]
    pub const fn source_byte_len(self) -> usize {
        self.source_byte_len
    }

    /// Return the padded upload-plan byte count.
    #[must_use]
    pub const fn upload_byte_len(self) -> usize {
        self.upload_byte_len
    }

    /// Return the accounted logical device byte count.
    #[must_use]
    pub const fn device_byte_len(self) -> usize {
        self.device_byte_len
    }
}

/// Immutable checked upload plan created away from the frame lookup path.
#[derive(Clone, PartialEq, Eq)]
pub struct TextureUploadPlan {
    asset: AssetHandle,
    descriptor: TextureDescriptor,
    bytes: Box<[u8]>,
}

impl TextureUploadPlan {
    /// Create a checked padded upload plan from an already decoded image.
    ///
    /// The source image is validated again at the GPU-resource boundary. The
    /// returned plan owns its bytes and contains zero-filled row padding.
    ///
    /// # Errors
    ///
    /// Returns a stable error for invalid layout, arithmetic overflow or an
    /// upload/device memory limit violation.
    pub fn new(
        asset: AssetHandle,
        decoded: &DecodedRgba8,
        limits: ResourceLimits,
    ) -> Result<Self, ResourceError> {
        let format = TextureFormat::Rgba8UnormSrgb;
        let width =
            usize::try_from(decoded.width()).map_err(|_| ResourceError::ArithmeticOverflow)?;
        let height =
            usize::try_from(decoded.height()).map_err(|_| ResourceError::ArithmeticOverflow)?;
        if width == 0 || height == 0 {
            return Err(ResourceError::InvalidImageLayout);
        }

        let source_row_pitch_bytes = width
            .checked_mul(format.bytes_per_pixel())
            .ok_or(ResourceError::ArithmeticOverflow)?;
        let source_byte_len = source_row_pitch_bytes
            .checked_mul(height)
            .ok_or(ResourceError::ArithmeticOverflow)?;
        let pixel_count = width
            .checked_mul(height)
            .ok_or(ResourceError::ArithmeticOverflow)?;

        if decoded.row_pitch_bytes() != source_row_pitch_bytes
            || decoded.pixel_count() != pixel_count
            || decoded.byte_len() != source_byte_len
            || decoded.pixels().len() != source_byte_len
        {
            return Err(ResourceError::InvalidImageLayout);
        }
        if source_byte_len > limits.max_single_texture_bytes() {
            return Err(ResourceError::TextureBytesLimitExceeded);
        }

        let upload_row_pitch_bytes =
            align_up(source_row_pitch_bytes, COPY_BYTES_PER_ROW_ALIGNMENT)?;
        let upload_byte_len = upload_row_pitch_bytes
            .checked_mul(height)
            .ok_or(ResourceError::ArithmeticOverflow)?;
        if upload_byte_len > limits.max_upload_plan_bytes() {
            return Err(ResourceError::UploadBytesLimitExceeded);
        }

        let bytes = if upload_row_pitch_bytes == source_row_pitch_bytes {
            decoded.pixels().to_vec().into_boxed_slice()
        } else {
            let mut padded = vec![0_u8; upload_byte_len];
            for row in 0..height {
                let source_start = row
                    .checked_mul(source_row_pitch_bytes)
                    .ok_or(ResourceError::ArithmeticOverflow)?;
                let source_end = source_start
                    .checked_add(source_row_pitch_bytes)
                    .ok_or(ResourceError::ArithmeticOverflow)?;
                let upload_start = row
                    .checked_mul(upload_row_pitch_bytes)
                    .ok_or(ResourceError::ArithmeticOverflow)?;
                let upload_end = upload_start
                    .checked_add(source_row_pitch_bytes)
                    .ok_or(ResourceError::ArithmeticOverflow)?;
                padded[upload_start..upload_end]
                    .copy_from_slice(&decoded.pixels()[source_start..source_end]);
            }
            padded.into_boxed_slice()
        };

        Ok(Self {
            asset,
            descriptor: TextureDescriptor {
                width: decoded.width(),
                height: decoded.height(),
                format,
                source_row_pitch_bytes,
                upload_row_pitch_bytes,
                source_byte_len,
                upload_byte_len,
                device_byte_len: source_byte_len,
            },
            bytes,
        })
    }

    /// Return the generation-fenced source asset.
    #[must_use]
    pub const fn asset(&self) -> AssetHandle {
        self.asset
    }

    /// Return the checked texture descriptor.
    #[must_use]
    pub const fn descriptor(&self) -> TextureDescriptor {
        self.descriptor
    }

    /// Return immutable padded upload bytes.
    #[must_use]
    pub fn bytes(&self) -> &[u8] {
        &self.bytes
    }
}

impl Debug for TextureUploadPlan {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("TextureUploadPlan")
            .field("asset", &self.asset)
            .field("descriptor", &self.descriptor)
            .field("upload_byte_len", &self.bytes.len())
            .finish_non_exhaustive()
    }
}

/// Logical generation-fenced reference to one uploaded texture.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct TextureHandle {
    process_generation: ProcessGeneration,
    device_generation: DeviceGeneration,
    pack_generation: PackGeneration,
    slot: u32,
    serial: NonZeroU64,
}

impl TextureHandle {
    /// Return the process generation carried by this handle.
    #[must_use]
    pub const fn process_generation(self) -> ProcessGeneration {
        self.process_generation
    }

    /// Return the device generation carried by this handle.
    #[must_use]
    pub const fn device_generation(self) -> DeviceGeneration {
        self.device_generation
    }

    /// Return the source asset-pack generation carried by this handle.
    #[must_use]
    pub const fn pack_generation(self) -> PackGeneration {
        self.pack_generation
    }

    /// Return the opaque cache slot.
    #[must_use]
    pub const fn slot(self) -> u32 {
        self.slot
    }

    /// Return the opaque allocation serial.
    #[must_use]
    pub const fn serial(self) -> u64 {
        self.serial.get()
    }
}

/// Result classification for one logical resource request.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AcquireStatus {
    /// A new sink resource was uploaded.
    Uploaded,
    /// An existing resource for the same generation-fenced asset was reused.
    Reused,
}

/// Stable result of acquiring one logical texture.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct AcquireResult {
    handle: TextureHandle,
    status: AcquireStatus,
    evicted_entries: usize,
}

impl AcquireResult {
    /// Return the acquired logical handle.
    #[must_use]
    pub const fn handle(self) -> TextureHandle {
        self.handle
    }

    /// Return whether the request uploaded or reused a resource.
    #[must_use]
    pub const fn status(self) -> AcquireStatus {
        self.status
    }

    /// Return the number of deterministic evictions performed first.
    #[must_use]
    pub const fn evicted_entries(self) -> usize {
        self.evicted_entries
    }
}

/// Read-only resolved resource view used by a later renderer consumer.
#[derive(Debug)]
pub struct ResourceView<'a, T> {
    texture: &'a T,
    descriptor: TextureDescriptor,
}

impl<'a, T> ResourceView<'a, T> {
    /// Return the sink-owned backend resource.
    #[must_use]
    pub const fn texture(&self) -> &'a T {
        self.texture
    }

    /// Return the checked descriptor associated with the resource.
    #[must_use]
    pub const fn descriptor(&self) -> TextureDescriptor {
        self.descriptor
    }
}

/// Resource destruction summary for device/pack replacement or explicit clear.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ResetReport {
    destroyed_entries: usize,
    released_device_bytes: usize,
}

impl ResetReport {
    /// Return the number of destroyed resources.
    #[must_use]
    pub const fn destroyed_entries(self) -> usize {
        self.destroyed_entries
    }

    /// Return the released accounted device bytes.
    #[must_use]
    pub const fn released_device_bytes(self) -> usize {
        self.released_device_bytes
    }
}

/// Backend upload boundary used by the real renderer owner or deterministic tests.
pub trait TextureUploadSink {
    /// Sink-owned texture resource type.
    type Texture;
    /// Sink-specific error type; details do not escape this crate's stable API.
    type Error: Error;

    /// Upload one fully checked immutable plan.
    fn upload(&mut self, plan: &TextureUploadPlan) -> Result<Self::Texture, Self::Error>;

    /// Destroy one previously uploaded texture.
    fn destroy(&mut self, texture: Self::Texture);
}

/// Stable payload-redacted renderer-resource failures.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ResourceError {
    /// A process/device generation constructor received zero.
    InvalidGeneration,
    /// Configured resource limits are invalid.
    InvalidLimits,
    /// Decoded image fields are internally inconsistent.
    InvalidImageLayout,
    /// Checked layout, counter or accounting arithmetic overflowed.
    ArithmeticOverflow,
    /// One texture exceeds the configured logical device-byte bound.
    TextureBytesLimitExceeded,
    /// One padded upload plan exceeds its configured allocation bound.
    UploadBytesLimitExceeded,
    /// The source asset belongs to a different pack generation.
    StaleAssetGeneration,
    /// A handle belongs to a different process generation.
    StaleProcessGeneration,
    /// A handle belongs to a different device generation.
    StaleDeviceGeneration,
    /// A handle belongs to a different asset-pack generation.
    StaleHandleAssetGeneration,
    /// A device reset attempted to reuse the current generation.
    DeviceGenerationNotAdvanced,
    /// A pack reset attempted to reuse the current generation.
    PackGenerationNotAdvanced,
    /// The backend upload sink rejected the checked plan.
    UploadFailed,
    /// The requested resource was evicted, cleared or never existed.
    MissingResource,
}

impl Display for ResourceError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str(match self {
            Self::InvalidGeneration => "renderer resource generation must be non-zero",
            Self::InvalidLimits => "renderer resource limits are invalid",
            Self::InvalidImageLayout => "decoded RGBA8 image layout is inconsistent",
            Self::ArithmeticOverflow => "renderer resource arithmetic overflowed",
            Self::TextureBytesLimitExceeded => "texture exceeds the device-memory limit",
            Self::UploadBytesLimitExceeded => "texture upload plan exceeds the allocation limit",
            Self::StaleAssetGeneration => "asset belongs to a stale pack generation",
            Self::StaleProcessGeneration => "texture handle belongs to a stale process generation",
            Self::StaleDeviceGeneration => "texture handle belongs to a stale device generation",
            Self::StaleHandleAssetGeneration => {
                "texture handle belongs to a stale asset-pack generation"
            }
            Self::DeviceGenerationNotAdvanced => {
                "replacement device generation must differ from the current generation"
            }
            Self::PackGenerationNotAdvanced => {
                "replacement asset-pack generation must differ from the current generation"
            }
            Self::UploadFailed => "renderer upload sink rejected the texture plan",
            Self::MissingResource => "renderer resource is unavailable",
        })
    }
}

impl Error for ResourceError {}

struct CacheEntry<T> {
    asset: AssetHandle,
    handle: TextureHandle,
    descriptor: TextureDescriptor,
    texture: T,
    last_used: u64,
}

/// Bounded deterministic logical texture cache owning one upload sink.
pub struct ResourceCache<S: TextureUploadSink> {
    process_generation: ProcessGeneration,
    device_generation: DeviceGeneration,
    pack_generation: PackGeneration,
    limits: ResourceLimits,
    sink: S,
    entries: Vec<CacheEntry<S::Texture>>,
    accounted_device_bytes: usize,
    access_tick: u64,
    next_slot: u32,
    next_serial: u64,
}

impl<S: TextureUploadSink> ResourceCache<S> {
    /// Create an empty bounded cache for one process/device/asset generation set.
    #[must_use]
    pub fn new(
        process_generation: ProcessGeneration,
        device_generation: DeviceGeneration,
        pack_generation: PackGeneration,
        limits: ResourceLimits,
        sink: S,
    ) -> Self {
        Self {
            process_generation,
            device_generation,
            pack_generation,
            limits,
            sink,
            entries: Vec::new(),
            accounted_device_bytes: 0,
            access_tick: 1,
            next_slot: 1,
            next_serial: 1,
        }
    }

    /// Return the current process generation.
    #[must_use]
    pub const fn process_generation(&self) -> ProcessGeneration {
        self.process_generation
    }

    /// Return the current device generation.
    #[must_use]
    pub const fn device_generation(&self) -> DeviceGeneration {
        self.device_generation
    }

    /// Return the current asset-pack generation.
    #[must_use]
    pub const fn pack_generation(&self) -> PackGeneration {
        self.pack_generation
    }

    /// Return the configured limits.
    #[must_use]
    pub const fn limits(&self) -> ResourceLimits {
        self.limits
    }

    /// Return the live resource count.
    #[must_use]
    pub fn entry_count(&self) -> usize {
        self.entries.len()
    }

    /// Return the currently accounted logical device bytes.
    #[must_use]
    pub const fn accounted_device_bytes(&self) -> usize {
        self.accounted_device_bytes
    }

    /// Acquire one texture, reusing an existing asset request when possible.
    ///
    /// The frame-critical [`Self::resolve`] path is allocation-free and performs
    /// no decode or I/O. Upload-plan allocation and sink submission occur only
    /// on this explicit acquisition path.
    ///
    /// # Errors
    ///
    /// Rejects stale asset generations, invalid images, exhausted checked
    /// counters and sink upload failures. Capacity and memory pressure evict the
    /// deterministic least-recently-used entry before upload.
    pub fn acquire(
        &mut self,
        asset: AssetHandle,
        decoded: &DecodedRgba8,
    ) -> Result<AcquireResult, ResourceError> {
        if asset.generation() != self.pack_generation {
            return Err(ResourceError::StaleAssetGeneration);
        }

        if let Some(index) = self.entries.iter().position(|entry| entry.asset == asset) {
            let tick = self.take_access_tick()?;
            self.entries[index].last_used = tick;
            return Ok(AcquireResult {
                handle: self.entries[index].handle,
                status: AcquireStatus::Reused,
                evicted_entries: 0,
            });
        }

        let plan = TextureUploadPlan::new(asset, decoded, self.limits)?;
        let required_bytes = plan.descriptor().device_byte_len();
        if required_bytes > self.limits.max_total_device_bytes() {
            return Err(ResourceError::TextureBytesLimitExceeded);
        }

        let mut evicted_entries = 0_usize;
        while self.entries.len() >= self.limits.max_entries()
            || self
                .accounted_device_bytes
                .checked_add(required_bytes)
                .ok_or(ResourceError::ArithmeticOverflow)?
                > self.limits.max_total_device_bytes()
        {
            self.evict_one()?;
            evicted_entries = evicted_entries
                .checked_add(1)
                .ok_or(ResourceError::ArithmeticOverflow)?;
        }

        let handle = self.preview_next_handle()?;
        let texture = self
            .sink
            .upload(&plan)
            .map_err(|_| ResourceError::UploadFailed)?;
        let tick = self.take_access_tick()?;
        self.next_slot = self
            .next_slot
            .checked_add(1)
            .ok_or(ResourceError::ArithmeticOverflow)?;
        self.next_serial = self
            .next_serial
            .checked_add(1)
            .ok_or(ResourceError::ArithmeticOverflow)?;
        self.accounted_device_bytes = self
            .accounted_device_bytes
            .checked_add(required_bytes)
            .ok_or(ResourceError::ArithmeticOverflow)?;
        self.entries.push(CacheEntry {
            asset,
            handle,
            descriptor: plan.descriptor(),
            texture,
            last_used: tick,
        });

        Ok(AcquireResult {
            handle,
            status: AcquireStatus::Uploaded,
            evicted_entries,
        })
    }

    /// Resolve a current logical handle without allocation, decode or I/O.
    ///
    /// # Errors
    ///
    /// Rejects every stale generation and handles that were evicted or cleared.
    pub fn resolve(
        &self,
        handle: TextureHandle,
    ) -> Result<ResourceView<'_, S::Texture>, ResourceError> {
        self.validate_handle_generations(handle)?;
        let entry = self
            .entries
            .iter()
            .find(|entry| entry.handle == handle)
            .ok_or(ResourceError::MissingResource)?;
        Ok(ResourceView {
            texture: &entry.texture,
            descriptor: entry.descriptor,
        })
    }

    /// Destroy all resources and advance the renderer device generation.
    ///
    /// # Errors
    ///
    /// Rejects an unchanged generation.
    pub fn replace_device(
        &mut self,
        new_generation: DeviceGeneration,
    ) -> Result<ResetReport, ResourceError> {
        if new_generation == self.device_generation {
            return Err(ResourceError::DeviceGenerationNotAdvanced);
        }
        let report = self.clear_entries();
        self.device_generation = new_generation;
        Ok(report)
    }

    /// Destroy all resources and advance the accepted asset-pack generation.
    ///
    /// # Errors
    ///
    /// Rejects an unchanged generation.
    pub fn replace_pack(
        &mut self,
        new_generation: PackGeneration,
    ) -> Result<ResetReport, ResourceError> {
        if new_generation == self.pack_generation {
            return Err(ResourceError::PackGenerationNotAdvanced);
        }
        let report = self.clear_entries();
        self.pack_generation = new_generation;
        Ok(report)
    }

    /// Explicitly destroy every live resource while preserving generations.
    #[must_use]
    pub fn clear(&mut self) -> ResetReport {
        self.clear_entries()
    }

    fn take_access_tick(&mut self) -> Result<u64, ResourceError> {
        let current = self.access_tick;
        self.access_tick = self
            .access_tick
            .checked_add(1)
            .ok_or(ResourceError::ArithmeticOverflow)?;
        Ok(current)
    }

    fn preview_next_handle(&self) -> Result<TextureHandle, ResourceError> {
        let serial = NonZeroU64::new(self.next_serial).ok_or(ResourceError::ArithmeticOverflow)?;
        self.next_slot
            .checked_add(1)
            .ok_or(ResourceError::ArithmeticOverflow)?;
        self.next_serial
            .checked_add(1)
            .ok_or(ResourceError::ArithmeticOverflow)?;
        Ok(TextureHandle {
            process_generation: self.process_generation,
            device_generation: self.device_generation,
            pack_generation: self.pack_generation,
            slot: self.next_slot,
            serial,
        })
    }

    fn validate_handle_generations(&self, handle: TextureHandle) -> Result<(), ResourceError> {
        if handle.process_generation != self.process_generation {
            return Err(ResourceError::StaleProcessGeneration);
        }
        if handle.device_generation != self.device_generation {
            return Err(ResourceError::StaleDeviceGeneration);
        }
        if handle.pack_generation != self.pack_generation {
            return Err(ResourceError::StaleHandleAssetGeneration);
        }
        Ok(())
    }

    fn evict_one(&mut self) -> Result<(), ResourceError> {
        let index = self
            .entries
            .iter()
            .enumerate()
            .min_by_key(|(_, entry)| (entry.last_used, entry.handle.slot))
            .map(|(index, _)| index)
            .ok_or(ResourceError::MissingResource)?;
        let entry = self.entries.remove(index);
        self.accounted_device_bytes = self
            .accounted_device_bytes
            .checked_sub(entry.descriptor.device_byte_len())
            .ok_or(ResourceError::ArithmeticOverflow)?;
        self.sink.destroy(entry.texture);
        Ok(())
    }

    fn clear_entries(&mut self) -> ResetReport {
        let destroyed_entries = self.entries.len();
        let released_device_bytes = self.accounted_device_bytes;
        while let Some(entry) = self.entries.pop() {
            self.sink.destroy(entry.texture);
        }
        self.accounted_device_bytes = 0;
        ResetReport {
            destroyed_entries,
            released_device_bytes,
        }
    }
}

impl<S: TextureUploadSink> Drop for ResourceCache<S> {
    fn drop(&mut self) {
        while let Some(entry) = self.entries.pop() {
            self.sink.destroy(entry.texture);
        }
    }
}

fn align_up(value: usize, alignment: usize) -> Result<usize, ResourceError> {
    let mask = alignment
        .checked_sub(1)
        .ok_or(ResourceError::ArithmeticOverflow)?;
    let adjusted = value
        .checked_add(mask)
        .ok_or(ResourceError::ArithmeticOverflow)?;
    Ok(adjusted & !mask)
}

#[cfg(test)]
mod tests {
    use super::*;
    use oteryn_asset_decode::{DecodeLimits, decode_rgba8};
    use oteryn_asset_runtime::{AssetRuntime, RuntimeLimits};
    use oteryn_asset_types::{AssetId, AssetKind, AssetMetadata, AssetPack, AssetRecord};
    use std::io;

    #[derive(Debug, Clone, Copy, PartialEq, Eq)]
    struct FakeSinkError;

    impl Display for FakeSinkError {
        fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
            formatter.write_str("fake sink failure")
        }
    }

    impl Error for FakeSinkError {}

    #[derive(Debug, Clone, Copy, PartialEq, Eq)]
    struct FakeTexture {
        id: u64,
        byte_len: usize,
    }

    #[derive(Debug, Default)]
    struct FakeSink {
        uploads: usize,
        destroyed: usize,
        destroyed_bytes: usize,
        next_id: u64,
        fail_next: bool,
    }

    impl TextureUploadSink for FakeSink {
        type Texture = FakeTexture;
        type Error = FakeSinkError;

        fn upload(&mut self, plan: &TextureUploadPlan) -> Result<Self::Texture, Self::Error> {
            if self.fail_next {
                self.fail_next = false;
                return Err(FakeSinkError);
            }
            self.uploads += 1;
            self.next_id += 1;
            Ok(FakeTexture {
                id: self.next_id,
                byte_len: plan.descriptor().device_byte_len(),
            })
        }

        fn destroy(&mut self, texture: Self::Texture) {
            self.destroyed += 1;
            self.destroyed_bytes += texture.byte_len;
        }
    }

    fn fixture(
        generation_value: u64,
        id_value: u32,
        width: u32,
        height: u32,
        fill: u8,
    ) -> Result<(AssetRuntime, AssetHandle, DecodedRgba8), Box<dyn Error>> {
        let width_usize = usize::try_from(width)?;
        let height_usize = usize::try_from(height)?;
        let byte_len = width_usize
            .checked_mul(height_usize)
            .and_then(|pixels| pixels.checked_mul(RGBA8_BYTES_PER_PIXEL))
            .ok_or_else(|| io::Error::other("fixture layout overflow"))?;
        let id = AssetId::new(id_value)?;
        let metadata = AssetMetadata::new(
            id,
            AssetKind::Rgba8 { width, height },
            format!("fixture-{id_value}"),
            "CC0-1.0".to_owned(),
            "project-original synthetic fixture".to_owned(),
        )?;
        let encoded =
            AssetPack::new(vec![AssetRecord::new(metadata, vec![fill; byte_len])?])?.encode()?;
        let generation = PackGeneration::new(generation_value)?;
        let runtime = AssetRuntime::open_bytes(generation, &encoded, RuntimeLimits::schema_v1())?;
        let handle = runtime
            .handle(id)
            .ok_or_else(|| io::Error::other("missing fixture handle"))?;
        let decoded = decode_rgba8(&runtime, handle, DecodeLimits::synthetic_v1())?;
        Ok((runtime, handle, decoded))
    }

    fn cache(
        pack_generation: PackGeneration,
        limits: ResourceLimits,
    ) -> Result<ResourceCache<FakeSink>, ResourceError> {
        Ok(ResourceCache::new(
            ProcessGeneration::new(7),
            DeviceGeneration::new(1)?,
            pack_generation,
            limits,
            FakeSink::default(),
        ))
    }

    #[test]
    fn upload_plan_revalidates_and_zero_pads_aligned_rows() -> Result<(), Box<dyn Error>> {
        let (_runtime, handle, decoded) = fixture(1, 1, 3, 2, 9)?;
        let plan = TextureUploadPlan::new(handle, &decoded, ResourceLimits::synthetic_v1())?;
        let descriptor = plan.descriptor();

        assert_eq!(descriptor.source_row_pitch_bytes(), 12);
        assert_eq!(descriptor.upload_row_pitch_bytes(), 256);
        assert_eq!(descriptor.source_byte_len(), 24);
        assert_eq!(descriptor.upload_byte_len(), 512);
        assert_eq!(descriptor.device_byte_len(), 24);
        assert_eq!(&plan.bytes()[..12], &[9; 12]);
        assert!(plan.bytes()[12..256].iter().all(|byte| *byte == 0));
        assert_eq!(&plan.bytes()[256..268], &[9; 12]);
        assert!(plan.bytes()[268..].iter().all(|byte| *byte == 0));
        assert!(!format!("{plan:?}").contains("9, 9"));
        Ok(())
    }

    #[test]
    fn duplicate_requests_coalesce_without_second_upload() -> Result<(), Box<dyn Error>> {
        let (_runtime, asset, decoded) = fixture(2, 2, 2, 2, 3)?;
        let mut cache = cache(asset.generation(), ResourceLimits::synthetic_v1())?;

        let first = cache.acquire(asset, &decoded)?;
        let second = cache.acquire(asset, &decoded)?;
        assert_eq!(first.status(), AcquireStatus::Uploaded);
        assert_eq!(second.status(), AcquireStatus::Reused);
        assert_eq!(first.handle(), second.handle());
        assert_eq!(cache.sink.uploads, 1);
        assert_eq!(cache.entry_count(), 1);
        assert_eq!(cache.accounted_device_bytes(), 16);
        assert_eq!(cache.resolve(first.handle())?.texture().byte_len, 16);
        Ok(())
    }

    #[test]
    fn least_recently_used_entry_is_evicted_deterministically() -> Result<(), Box<dyn Error>> {
        let (_runtime_a, asset_a, decoded_a) = fixture(3, 1, 1, 1, 1)?;
        let (_runtime_b, asset_b, decoded_b) = fixture(3, 2, 1, 1, 2)?;
        let (_runtime_c, asset_c, decoded_c) = fixture(3, 3, 1, 1, 3)?;
        let limits = ResourceLimits::new(2, 8, 4, 256)?;
        let mut cache = cache(asset_a.generation(), limits)?;

        let first = cache.acquire(asset_a, &decoded_a)?;
        let second = cache.acquire(asset_b, &decoded_b)?;
        cache.acquire(asset_a, &decoded_a)?;
        let third = cache.acquire(asset_c, &decoded_c)?;

        assert_eq!(third.evicted_entries(), 1);
        assert!(cache.resolve(first.handle()).is_ok());
        assert_eq!(
            cache.resolve(second.handle()).err(),
            Some(ResourceError::MissingResource)
        );
        assert!(cache.resolve(third.handle()).is_ok());
        assert_eq!(cache.sink.destroyed, 1);
        assert_eq!(cache.entry_count(), 2);
        assert_eq!(cache.accounted_device_bytes(), 8);
        Ok(())
    }

    #[test]
    fn stale_asset_and_handle_generations_fail_closed() -> Result<(), Box<dyn Error>> {
        let (_runtime, asset, decoded) = fixture(4, 1, 1, 1, 4)?;
        let mut cache = cache(asset.generation(), ResourceLimits::synthetic_v1())?;
        let acquired = cache.acquire(asset, &decoded)?;

        let device_report = cache.replace_device(DeviceGeneration::new(2)?)?;
        assert_eq!(device_report.destroyed_entries(), 1);
        assert_eq!(device_report.released_device_bytes(), 4);
        assert_eq!(
            cache.resolve(acquired.handle()).err(),
            Some(ResourceError::StaleDeviceGeneration)
        );

        let (_new_runtime, new_asset, new_decoded) = fixture(5, 1, 1, 1, 5)?;
        assert_eq!(
            cache.acquire(new_asset, &new_decoded).err(),
            Some(ResourceError::StaleAssetGeneration)
        );
        cache.replace_pack(new_asset.generation())?;
        let new_handle = cache.acquire(new_asset, &new_decoded)?.handle();
        assert!(cache.resolve(new_handle).is_ok());
        assert_eq!(
            cache.resolve(acquired.handle()).err(),
            Some(ResourceError::StaleDeviceGeneration)
        );
        Ok(())
    }

    #[test]
    fn sink_failure_is_stable_and_does_not_create_accounting() -> Result<(), Box<dyn Error>> {
        let (_runtime, asset, decoded) = fixture(6, 1, 1, 1, 6)?;
        let mut sink = FakeSink::default();
        sink.fail_next = true;
        let mut cache = ResourceCache::new(
            ProcessGeneration::new(8),
            DeviceGeneration::new(1)?,
            asset.generation(),
            ResourceLimits::synthetic_v1(),
            sink,
        );

        assert_eq!(
            cache.acquire(asset, &decoded).err(),
            Some(ResourceError::UploadFailed)
        );
        assert_eq!(cache.entry_count(), 0);
        assert_eq!(cache.accounted_device_bytes(), 0);
        assert_eq!(cache.sink.uploads, 0);
        Ok(())
    }

    #[test]
    fn memory_pressure_evicts_before_upload_and_clear_is_exact() -> Result<(), Box<dyn Error>> {
        let (_runtime_a, asset_a, decoded_a) = fixture(7, 1, 2, 1, 1)?;
        let (_runtime_b, asset_b, decoded_b) = fixture(7, 2, 2, 1, 2)?;
        let limits = ResourceLimits::new(2, 8, 8, 256)?;
        let mut cache = cache(asset_a.generation(), limits)?;

        let first = cache.acquire(asset_a, &decoded_a)?;
        let second = cache.acquire(asset_b, &decoded_b)?;
        assert_eq!(second.evicted_entries(), 1);
        assert_eq!(
            cache.resolve(first.handle()).err(),
            Some(ResourceError::MissingResource)
        );
        assert_eq!(cache.accounted_device_bytes(), 8);

        let report = cache.clear();
        assert_eq!(report.destroyed_entries(), 1);
        assert_eq!(report.released_device_bytes(), 8);
        assert_eq!(cache.entry_count(), 0);
        assert_eq!(cache.accounted_device_bytes(), 0);
        assert_eq!(cache.sink.destroyed, 2);
        assert_eq!(cache.sink.destroyed_bytes, 16);
        Ok(())
    }

    #[test]
    fn invalid_limits_and_unchanged_generation_resets_are_rejected() -> Result<(), Box<dyn Error>> {
        assert_eq!(
            ResourceLimits::new(0, 1, 1, 1),
            Err(ResourceError::InvalidLimits)
        );
        let (_runtime, asset, _decoded) = fixture(8, 1, 1, 1, 8)?;
        let mut cache = cache(asset.generation(), ResourceLimits::synthetic_v1())?;
        assert_eq!(
            cache.replace_device(cache.device_generation()).err(),
            Some(ResourceError::DeviceGenerationNotAdvanced)
        );
        assert_eq!(
            cache.replace_pack(cache.pack_generation()).err(),
            Some(ResourceError::PackGenerationNotAdvanced)
        );
        Ok(())
    }
}
