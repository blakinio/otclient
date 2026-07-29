//! Deterministic offline compiler for the bounded synthetic asset format.

use oteryn_asset_types::{
    AssetError, AssetId, AssetKind, AssetMetadata, AssetPack, AssetRecord, MAX_ASSET_BYTES,
    MAX_RECORDS,
};
use serde_json::{Map, Value};
use std::error::Error;
use std::fmt::{self, Display, Formatter};
use std::fs::{self, File, OpenOptions};
use std::io::{Read, Write};
use std::path::{Component, Path, PathBuf};

/// Current constrained JSON manifest schema version.
pub const MANIFEST_SCHEMA_VERSION: u64 = 1;
/// Maximum JSON manifest size accepted before parsing.
pub const MAX_MANIFEST_BYTES: usize = 1024 * 1024;

/// Result summary that contains no source-machine paths.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CompileReport {
    record_count: usize,
    encoded_bytes: usize,
}

impl CompileReport {
    /// Return the number of compiled records.
    #[must_use]
    pub const fn record_count(self) -> usize {
        self.record_count
    }

    /// Return the final encoded byte count.
    #[must_use]
    pub const fn encoded_bytes(self) -> usize {
        self.encoded_bytes
    }
}

/// Compile one constrained JSON manifest into one immutable synthetic pack.
///
/// Source entries are resolved under the manifest directory. The final output
/// must not already exist. A same-directory temporary file is committed with a
/// final rename only after all parsing, validation and encoding succeeds.
///
/// # Errors
///
/// Returns a stable [`CompilerError`] for invalid manifests, unsafe paths,
/// bounded I/O failures or asset contract violations.
pub fn compile_manifest(
    manifest_path: &Path,
    output_path: &Path,
) -> Result<CompileReport, CompilerError> {
    let output = OutputTarget::new(output_path)?;
    let manifest_bytes = read_bounded_manifest(manifest_path)?;
    let manifest: Value = serde_json::from_slice(&manifest_bytes)
        .map_err(|_| CompilerError::InvalidJson)?;
    let root = canonical_manifest_root(manifest_path)?;
    let records = parse_manifest(&manifest, &root)?;
    let pack = AssetPack::new(records).map_err(CompilerError::Asset)?;
    let encoded = pack.encode().map_err(CompilerError::Asset)?;
    output.commit(&encoded)?;
    Ok(CompileReport {
        record_count: pack.records().len(),
        encoded_bytes: encoded.len(),
    })
}

/// Stable non-secret compiler failures.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CompilerError {
    ManifestUnavailable,
    ManifestTooLarge,
    InvalidJson,
    InvalidManifest,
    UnsupportedManifestVersion,
    TooManyAssets,
    UnknownAssetKind,
    InvalidSourcePath,
    SourceUnavailable,
    SourceSymlink,
    SourceOutsideRoot,
    SourceNotFile,
    SourceTooLarge,
    InvalidOutputPath,
    OutputExists,
    TemporaryOutputExists,
    OutputWriteFailed,
    OutputCommitFailed,
    Asset(AssetError),
}

impl Display for CompilerError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        let message = match self {
            Self::ManifestUnavailable => "asset manifest is unavailable",
            Self::ManifestTooLarge => "asset manifest exceeds the compiler limit",
            Self::InvalidJson => "asset manifest is not valid JSON",
            Self::InvalidManifest => "asset manifest does not match schema version 1",
            Self::UnsupportedManifestVersion => "asset manifest schema version is unsupported",
            Self::TooManyAssets => "asset manifest record count exceeds the compiler limit",
            Self::UnknownAssetKind => "asset manifest kind is unknown",
            Self::InvalidSourcePath => "asset source path is invalid",
            Self::SourceUnavailable => "asset source is unavailable",
            Self::SourceSymlink => "asset source path contains a symbolic link",
            Self::SourceOutsideRoot => "asset source resolves outside the manifest root",
            Self::SourceNotFile => "asset source is not a regular file",
            Self::SourceTooLarge => "asset source exceeds the compiler limit",
            Self::InvalidOutputPath => "asset output path is invalid",
            Self::OutputExists => "asset output already exists",
            Self::TemporaryOutputExists => "asset temporary output already exists",
            Self::OutputWriteFailed => "asset output could not be written",
            Self::OutputCommitFailed => "asset output could not be committed",
            Self::Asset(error) => return Display::fmt(error, formatter),
        };
        formatter.write_str(message)
    }
}

impl Error for CompilerError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::Asset(error) => Some(error),
            _ => None,
        }
    }
}

fn read_bounded_manifest(path: &Path) -> Result<Vec<u8>, CompilerError> {
    let metadata = fs::metadata(path).map_err(|_| CompilerError::ManifestUnavailable)?;
    if !metadata.is_file() {
        return Err(CompilerError::ManifestUnavailable);
    }
    if metadata.len() > usize_to_u64(MAX_MANIFEST_BYTES) {
        return Err(CompilerError::ManifestTooLarge);
    }

    let file = File::open(path).map_err(|_| CompilerError::ManifestUnavailable)?;
    let mut bytes = Vec::with_capacity(
        usize::try_from(metadata.len()).map_err(|_| CompilerError::ManifestTooLarge)?,
    );
    file.take(usize_to_u64(MAX_MANIFEST_BYTES + 1))
        .read_to_end(&mut bytes)
        .map_err(|_| CompilerError::ManifestUnavailable)?;
    if bytes.len() > MAX_MANIFEST_BYTES {
        return Err(CompilerError::ManifestTooLarge);
    }
    Ok(bytes)
}

fn canonical_manifest_root(path: &Path) -> Result<PathBuf, CompilerError> {
    let root = path.parent().unwrap_or_else(|| Path::new("."));
    let canonical = fs::canonicalize(root).map_err(|_| CompilerError::ManifestUnavailable)?;
    if !canonical.is_dir() {
        return Err(CompilerError::ManifestUnavailable);
    }
    Ok(canonical)
}

fn parse_manifest(value: &Value, root: &Path) -> Result<Vec<AssetRecord>, CompilerError> {
    let object = value.as_object().ok_or(CompilerError::InvalidManifest)?;
    require_exact_keys(object, &["schema_version", "assets"])?;
    let schema_version = object
        .get("schema_version")
        .and_then(Value::as_u64)
        .ok_or(CompilerError::InvalidManifest)?;
    if schema_version != MANIFEST_SCHEMA_VERSION {
        return Err(CompilerError::UnsupportedManifestVersion);
    }
    let assets = object
        .get("assets")
        .and_then(Value::as_array)
        .ok_or(CompilerError::InvalidManifest)?;
    if assets.len() > MAX_RECORDS {
        return Err(CompilerError::TooManyAssets);
    }

    let mut records = Vec::with_capacity(assets.len());
    for asset in assets {
        records.push(parse_asset(asset, root)?);
    }
    Ok(records)
}

fn parse_asset(value: &Value, root: &Path) -> Result<AssetRecord, CompilerError> {
    let object = value.as_object().ok_or(CompilerError::InvalidManifest)?;
    let kind_name = required_string(object, "kind")?;
    match kind_name {
        "blob" => require_exact_keys(
            object,
            &["id", "kind", "name", "source", "license", "provenance"],
        )?,
        "rgba8" => require_exact_keys(
            object,
            &[
                "id",
                "kind",
                "name",
                "source",
                "license",
                "provenance",
                "width",
                "height",
            ],
        )?,
        _ => return Err(CompilerError::UnknownAssetKind),
    }

    let id_value = required_u64(object, "id")?;
    let id = AssetId::new(
        u32::try_from(id_value).map_err(|_| CompilerError::InvalidManifest)?,
    )
    .map_err(CompilerError::Asset)?;
    let logical_name = required_string(object, "name")?.to_owned();
    let license = required_string(object, "license")?.to_owned();
    let provenance = required_string(object, "provenance")?.to_owned();
    let source = validated_relative_path(required_string(object, "source")?)?;
    let payload = read_source(root, &source)?;
    let kind = match kind_name {
        "blob" => AssetKind::Blob,
        "rgba8" => AssetKind::Rgba8 {
            width: u32::try_from(required_u64(object, "width")?)
                .map_err(|_| CompilerError::InvalidManifest)?,
            height: u32::try_from(required_u64(object, "height")?)
                .map_err(|_| CompilerError::InvalidManifest)?,
        },
        _ => return Err(CompilerError::UnknownAssetKind),
    };
    let metadata = AssetMetadata::new(id, kind, logical_name, license, provenance)
        .map_err(CompilerError::Asset)?;
    AssetRecord::new(metadata, payload).map_err(CompilerError::Asset)
}

fn require_exact_keys(
    object: &Map<String, Value>,
    allowed: &[&str],
) -> Result<(), CompilerError> {
    if object.len() != allowed.len()
        || object
            .keys()
            .any(|key| !allowed.contains(&key.as_str()))
    {
        return Err(CompilerError::InvalidManifest);
    }
    Ok(())
}

fn required_string<'a>(
    object: &'a Map<String, Value>,
    key: &str,
) -> Result<&'a str, CompilerError> {
    object
        .get(key)
        .and_then(Value::as_str)
        .ok_or(CompilerError::InvalidManifest)
}

fn required_u64(object: &Map<String, Value>, key: &str) -> Result<u64, CompilerError> {
    object
        .get(key)
        .and_then(Value::as_u64)
        .ok_or(CompilerError::InvalidManifest)
}

fn validated_relative_path(value: &str) -> Result<PathBuf, CompilerError> {
    if value.is_empty() || value.contains('\\') || value.contains(':') {
        return Err(CompilerError::InvalidSourcePath);
    }

    let path = Path::new(value);
    if path.is_absolute() {
        return Err(CompilerError::InvalidSourcePath);
    }

    let mut normalized = PathBuf::new();
    for component in path.components() {
        match component {
            Component::Normal(part) => normalized.push(part),
            Component::Prefix(_)
            | Component::RootDir
            | Component::CurDir
            | Component::ParentDir => return Err(CompilerError::InvalidSourcePath),
        }
    }
    if normalized.as_os_str().is_empty() {
        return Err(CompilerError::InvalidSourcePath);
    }
    Ok(normalized)
}

fn read_source(root: &Path, relative: &Path) -> Result<Vec<u8>, CompilerError> {
    let mut current = root.to_path_buf();
    for component in relative.components() {
        let Component::Normal(part) = component else {
            return Err(CompilerError::InvalidSourcePath);
        };
        current.push(part);
        let metadata = fs::symlink_metadata(&current)
            .map_err(|_| CompilerError::SourceUnavailable)?;
        if metadata.file_type().is_symlink() {
            return Err(CompilerError::SourceSymlink);
        }
    }

    let canonical = fs::canonicalize(&current).map_err(|_| CompilerError::SourceUnavailable)?;
    if !canonical.starts_with(root) {
        return Err(CompilerError::SourceOutsideRoot);
    }
    let metadata = fs::metadata(&canonical).map_err(|_| CompilerError::SourceUnavailable)?;
    if !metadata.is_file() {
        return Err(CompilerError::SourceNotFile);
    }
    if metadata.len() > usize_to_u64(MAX_ASSET_BYTES) {
        return Err(CompilerError::SourceTooLarge);
    }

    let file = File::open(&canonical).map_err(|_| CompilerError::SourceUnavailable)?;
    let mut payload = Vec::with_capacity(
        usize::try_from(metadata.len()).map_err(|_| CompilerError::SourceTooLarge)?,
    );
    file.take(usize_to_u64(MAX_ASSET_BYTES + 1))
        .read_to_end(&mut payload)
        .map_err(|_| CompilerError::SourceUnavailable)?;
    if payload.len() > MAX_ASSET_BYTES {
        return Err(CompilerError::SourceTooLarge);
    }
    Ok(payload)
}

fn usize_to_u64(value: usize) -> u64 {
    u64::try_from(value).unwrap_or(u64::MAX)
}

struct OutputTarget {
    final_path: PathBuf,
    temporary_path: PathBuf,
}

impl OutputTarget {
    fn new(path: &Path) -> Result<Self, CompilerError> {
        let file_name = path
            .file_name()
            .and_then(|value| value.to_str())
            .filter(|value| !value.is_empty())
            .ok_or(CompilerError::InvalidOutputPath)?;
        let parent = path.parent().unwrap_or_else(|| Path::new("."));
        let metadata = fs::metadata(parent).map_err(|_| CompilerError::InvalidOutputPath)?;
        if !metadata.is_dir() {
            return Err(CompilerError::InvalidOutputPath);
        }
        if path.exists() {
            return Err(CompilerError::OutputExists);
        }

        let temporary_path = parent.join(format!(".{file_name}.oteryn-tmp"));
        match fs::symlink_metadata(&temporary_path) {
            Ok(_) => return Err(CompilerError::TemporaryOutputExists),
            Err(error) if error.kind() == std::io::ErrorKind::NotFound => {}
            Err(_) => return Err(CompilerError::InvalidOutputPath),
        }
        Ok(Self {
            final_path: path.to_path_buf(),
            temporary_path,
        })
    }

    fn commit(self, encoded: &[u8]) -> Result<(), CompilerError> {
        let result = self.write_and_commit(encoded);
        if result.is_err() {
            drop(fs::remove_file(&self.temporary_path));
        }
        result
    }

    fn write_and_commit(&self, encoded: &[u8]) -> Result<(), CompilerError> {
        let mut file = OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&self.temporary_path)
            .map_err(|_| CompilerError::OutputWriteFailed)?;
        file.write_all(encoded)
            .map_err(|_| CompilerError::OutputWriteFailed)?;
        file.sync_all()
            .map_err(|_| CompilerError::OutputWriteFailed)?;
        drop(file);
        fs::rename(&self.temporary_path, &self.final_path)
            .map_err(|_| CompilerError::OutputCommitFailed)
    }
}
