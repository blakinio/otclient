//! Deterministic offline compiler for the bounded synthetic asset format.

use cap_fs_ext::{DirExt, FollowSymlinks, OpenOptionsFollowExt};
use cap_std::ambient_authority;
use cap_std::fs::{Dir, File as CapabilityFile, OpenOptions as CapabilityOpenOptions};
use oteryn_asset_types::{
    AssetError, AssetId, AssetKind, AssetMetadata, AssetPack, AssetRecord, MAX_ASSET_BYTES,
    MAX_RECORDS,
};
use serde_json::{Map, Value};
use std::error::Error;
use std::ffi::OsStr;
use std::fmt::{self, Display, Formatter};
use std::fs::{self, OpenOptions};
use std::io::{self, Read, Write};
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
/// Source entries are resolved under the opened manifest-directory capability.
/// Every path component is opened without following links, and source type,
/// size and bytes are obtained from the same accepted file handle. The final
/// output must not already exist. A same-directory temporary file is committed
/// with a final rename only after all parsing, validation and encoding succeeds.
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
    let (manifest_bytes, source_root) = read_bounded_manifest(manifest_path)?;
    let manifest: Value =
        serde_json::from_slice(&manifest_bytes).map_err(|_| CompilerError::InvalidJson)?;
    let records = parse_manifest(&manifest, &source_root)?;
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

fn read_bounded_manifest(path: &Path) -> Result<(Vec<u8>, Dir), CompilerError> {
    let file_name = path
        .file_name()
        .filter(|value| !value.is_empty())
        .ok_or(CompilerError::ManifestUnavailable)?;
    let parent = path
        .parent()
        .filter(|value| !value.as_os_str().is_empty())
        .unwrap_or_else(|| Path::new("."));
    let root = Dir::open_ambient_dir(parent, ambient_authority())
        .map_err(|_| CompilerError::ManifestUnavailable)?;
    let file =
        open_file_nofollow(&root, file_name).map_err(|_| CompilerError::ManifestUnavailable)?;
    let bytes = read_bounded_open_file(
        file,
        MAX_MANIFEST_BYTES,
        CompilerError::ManifestUnavailable,
        CompilerError::ManifestTooLarge,
    )?;
    Ok((bytes, root))
}

fn read_bounded_open_file(
    file: CapabilityFile,
    limit: usize,
    unavailable: CompilerError,
    too_large: CompilerError,
) -> Result<Vec<u8>, CompilerError> {
    let metadata = file.metadata().map_err(|_| unavailable)?;
    if !metadata.is_file() {
        return Err(unavailable);
    }
    if metadata.len() > usize_to_u64(limit) {
        return Err(too_large);
    }

    let mut bytes = Vec::with_capacity(usize::try_from(metadata.len()).map_err(|_| too_large)?);
    file.take(usize_to_u64(limit + 1))
        .read_to_end(&mut bytes)
        .map_err(|_| unavailable)?;
    if bytes.len() > limit {
        return Err(too_large);
    }
    Ok(bytes)
}

fn parse_manifest(value: &Value, root: &Dir) -> Result<Vec<AssetRecord>, CompilerError> {
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

fn parse_asset(value: &Value, root: &Dir) -> Result<AssetRecord, CompilerError> {
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
    let id = AssetId::new(u32::try_from(id_value).map_err(|_| CompilerError::InvalidManifest)?)
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

fn require_exact_keys(object: &Map<String, Value>, allowed: &[&str]) -> Result<(), CompilerError> {
    if object.len() != allowed.len() || object.keys().any(|key| !allowed.contains(&key.as_str())) {
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
    if value.is_empty()
        || value.contains('\\')
        || value.contains(':')
        || value.chars().any(char::is_control)
        || value
            .split('/')
            .any(|segment| segment.is_empty() || segment == "." || segment == "..")
    {
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

fn read_source(root: &Dir, relative: &Path) -> Result<Vec<u8>, CompilerError> {
    read_source_with_hook(root, relative, || {})
}

fn read_source_with_hook<F>(
    root: &Dir,
    relative: &Path,
    after_open: F,
) -> Result<Vec<u8>, CompilerError>
where
    F: FnOnce(),
{
    let mut directory = root
        .try_clone()
        .map_err(|_| CompilerError::SourceUnavailable)?;
    let mut components = relative.components().peekable();
    let mut file = None;

    while let Some(component) = components.next() {
        let Component::Normal(part) = component else {
            return Err(CompilerError::InvalidSourcePath);
        };
        if components.peek().is_some() {
            directory = directory
                .open_dir_nofollow(Path::new(part))
                .map_err(|_| classify_source_open_error(&directory, part, true))?;
        } else {
            file = Some(
                open_file_nofollow(&directory, part)
                    .map_err(|_| classify_source_open_error(&directory, part, false))?,
            );
        }
    }

    let file = file.ok_or(CompilerError::InvalidSourcePath)?;
    let metadata = file
        .metadata()
        .map_err(|_| CompilerError::SourceUnavailable)?;
    if !metadata.is_file() {
        return Err(CompilerError::SourceNotFile);
    }
    if metadata.len() > usize_to_u64(MAX_ASSET_BYTES) {
        return Err(CompilerError::SourceTooLarge);
    }

    after_open();

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

fn open_file_nofollow(directory: &Dir, name: &OsStr) -> io::Result<CapabilityFile> {
    let mut options = CapabilityOpenOptions::new();
    options.read(true).follow(FollowSymlinks::No);
    directory.open_with(Path::new(name), &options)
}

fn classify_source_open_error(
    directory: &Dir,
    name: &OsStr,
    directory_required: bool,
) -> CompilerError {
    match directory.symlink_metadata(Path::new(name)) {
        Ok(metadata) if metadata.file_type().is_symlink() => CompilerError::SourceSymlink,
        Ok(metadata) if directory_required && !metadata.is_dir() => CompilerError::SourceNotFile,
        Ok(metadata) if !directory_required && !metadata.is_file() => CompilerError::SourceNotFile,
        _ => CompilerError::SourceUnavailable,
    }
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
        match fs::symlink_metadata(path) {
            Ok(_) => return Err(CompilerError::OutputExists),
            Err(error) if error.kind() == std::io::ErrorKind::NotFound => {}
            Err(_) => return Err(CompilerError::InvalidOutputPath),
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

#[cfg(test)]
mod tests {
    use super::*;
    use std::cell::RefCell;
    use std::env;
    use std::process;
    use std::sync::atomic::{AtomicU64, Ordering};

    static NEXT_DIRECTORY: AtomicU64 = AtomicU64::new(1);

    #[test]
    fn opened_source_handle_cannot_be_redirected_by_path_replacement() -> Result<(), Box<dyn Error>>
    {
        let sequence = NEXT_DIRECTORY.fetch_add(1, Ordering::Relaxed);
        let directory_path = env::temp_dir().join(format!(
            "oteryn-asset-open-handle-{}-{sequence}",
            process::id()
        ));
        drop(fs::remove_dir_all(&directory_path));
        fs::create_dir(&directory_path)?;
        let source_path = directory_path.join("source.bin");
        let moved_path = directory_path.join("accepted.bin");
        fs::write(&source_path, b"accepted object bytes")?;

        let root = Dir::open_ambient_dir(&directory_path, ambient_authority())?;
        let replacement = RefCell::new(None);
        let payload = read_source_with_hook(&root, Path::new("source.bin"), || {
            let result = fs::rename(&source_path, &moved_path)
                .and_then(|()| fs::write(&source_path, b"substituted path bytes"));
            replacement.replace(Some(result));
        })?;

        assert_eq!(payload, b"accepted object bytes");
        let replacement = replacement
            .into_inner()
            .ok_or_else(|| io::Error::other("source replacement hook did not run"))?;
        if replacement.is_ok() {
            assert_eq!(fs::read(&source_path)?, b"substituted path bytes");
        }

        drop(root);
        drop(fs::remove_dir_all(&directory_path));
        Ok(())
    }
}
