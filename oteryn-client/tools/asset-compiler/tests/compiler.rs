use oteryn_asset_compiler::{CompilerError, MAX_MANIFEST_BYTES, compile_manifest};
use oteryn_asset_types::{AssetError, MAX_ASSET_BYTES, MAX_RECORDS};
use serde_json::json;
use std::env;
use std::error::Error;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};
use std::process;
use std::sync::atomic::{AtomicU64, Ordering};

static NEXT_DIRECTORY: AtomicU64 = AtomicU64::new(1);

struct TestDirectory {
    path: PathBuf,
}

impl TestDirectory {
    fn new() -> io::Result<Self> {
        let sequence = NEXT_DIRECTORY.fetch_add(1, Ordering::Relaxed);
        let path = env::temp_dir().join(format!(
            "oteryn-asset-compiler-{}-{sequence}",
            process::id()
        ));
        drop(fs::remove_dir_all(&path));
        fs::create_dir(&path)?;
        Ok(Self { path })
    }

    fn path(&self) -> &Path {
        &self.path
    }

    fn write(&self, relative: &str, bytes: &[u8]) -> io::Result<PathBuf> {
        let path = self.path.join(relative);
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent)?;
        }
        fs::write(&path, bytes)?;
        Ok(path)
    }
}

impl Drop for TestDirectory {
    fn drop(&mut self) {
        drop(fs::remove_dir_all(&self.path));
    }
}

fn blob_entry(id: u32, source: &str) -> String {
    json!({
        "id": id,
        "kind": "blob",
        "name": format!("blob-{id}"),
        "source": source,
        "license": "CC0-1.0",
        "provenance": "original synthetic test fixture"
    })
    .to_string()
}

fn rgba_entry(id: u32, source: &str) -> String {
    json!({
        "id": id,
        "kind": "rgba8",
        "name": format!("rgba-{id}"),
        "source": source,
        "license": "CC0-1.0",
        "provenance": "original synthetic test fixture",
        "width": 2,
        "height": 2
    })
    .to_string()
}

fn manifest(entries: &str) -> String {
    format!(r#"{{"schema_version":1,"assets":[{entries}]}}"#)
}

#[test]
fn repeated_and_shuffled_compilation_is_byte_identical() -> Result<(), Box<dyn Error>> {
    let directory = TestDirectory::new()?;
    directory.write("blob.txt", b"synthetic blob")?;
    directory.write("checker.rgba", b"RGBA0123456789AB")?;
    let first_manifest = directory.write(
        "first.json",
        manifest(&format!(
            "{},{}",
            blob_entry(1, "blob.txt"),
            rgba_entry(2, "checker.rgba")
        ))
        .as_bytes(),
    )?;
    let second_manifest = directory.write(
        "second.json",
        manifest(&format!(
            "{},{}",
            rgba_entry(2, "checker.rgba"),
            blob_entry(1, "blob.txt")
        ))
        .as_bytes(),
    )?;
    let first_output = directory.path().join("first.pack");
    let second_output = directory.path().join("second.pack");

    let first_report = compile_manifest(&first_manifest, &first_output)?;
    let second_report = compile_manifest(&second_manifest, &second_output)?;
    assert_eq!(first_report.record_count(), 2);
    assert_eq!(first_report, second_report);
    assert_eq!(fs::read(first_output)?, fs::read(second_output)?);
    Ok(())
}

#[test]
fn unsafe_portable_source_paths_are_rejected() -> Result<(), Box<dyn Error>> {
    let invalid_paths = [
        "../outside.bin",
        "/absolute.bin",
        "C:/windows.bin",
        "folder\\escape.bin",
        "./current.bin",
        "folder/./current.bin",
        "folder//double.bin",
        "folder/trailing/",
        "control\u{0000}.bin",
    ];

    for (index, invalid_path) in invalid_paths.iter().enumerate() {
        let directory = TestDirectory::new()?;
        let manifest_path = directory.write(
            "manifest.json",
            manifest(&blob_entry(1, invalid_path)).as_bytes(),
        )?;
        let output = directory.path().join(format!("invalid-{index}.pack"));
        assert_eq!(
            compile_manifest(&manifest_path, &output),
            Err(CompilerError::InvalidSourcePath)
        );
    }
    Ok(())
}

#[test]
fn directories_are_not_accepted_as_sources() -> Result<(), Box<dyn Error>> {
    let directory = TestDirectory::new()?;
    fs::create_dir(directory.path().join("payload"))?;
    let manifest_path = directory.write(
        "manifest.json",
        manifest(&blob_entry(1, "payload")).as_bytes(),
    )?;
    assert_eq!(
        compile_manifest(&manifest_path, &directory.path().join("output.pack")),
        Err(CompilerError::SourceNotFile)
    );
    Ok(())
}

#[test]
fn oversized_source_is_rejected_before_reading() -> Result<(), Box<dyn Error>> {
    let directory = TestDirectory::new()?;
    let source = fs::File::create(directory.path().join("oversized.bin"))?;
    source.set_len(u64::try_from(MAX_ASSET_BYTES + 1)?)?;
    let manifest_path = directory.write(
        "manifest.json",
        manifest(&blob_entry(1, "oversized.bin")).as_bytes(),
    )?;
    assert_eq!(
        compile_manifest(&manifest_path, &directory.path().join("output.pack")),
        Err(CompilerError::SourceTooLarge)
    );
    Ok(())
}

#[test]
fn invalid_rgba_dimensions_are_rejected() -> Result<(), Box<dyn Error>> {
    let directory = TestDirectory::new()?;
    directory.write("checker.rgba", b"too short")?;
    let manifest_path = directory.write(
        "manifest.json",
        manifest(&rgba_entry(1, "checker.rgba")).as_bytes(),
    )?;
    assert_eq!(
        compile_manifest(&manifest_path, &directory.path().join("output.pack")),
        Err(CompilerError::Asset(AssetError::PayloadLengthMismatch))
    );
    Ok(())
}

#[test]
fn malformed_extended_and_unsupported_manifests_are_rejected() -> Result<(), Box<dyn Error>> {
    let directory = TestDirectory::new()?;
    let invalid_json = directory.write("invalid.json", b"{")?;
    assert_eq!(
        compile_manifest(&invalid_json, &directory.path().join("invalid.pack")),
        Err(CompilerError::InvalidJson)
    );

    let extended = directory.write(
        "extended.json",
        br#"{"schema_version":1,"assets":[],"unexpected":true}"#,
    )?;
    assert_eq!(
        compile_manifest(&extended, &directory.path().join("extended.pack")),
        Err(CompilerError::InvalidManifest)
    );

    let unsupported =
        directory.write("unsupported.json", br#"{"schema_version":2,"assets":[]}"#)?;
    assert_eq!(
        compile_manifest(&unsupported, &directory.path().join("unsupported.pack")),
        Err(CompilerError::UnsupportedManifestVersion)
    );
    Ok(())
}

#[test]
fn unknown_kind_and_duplicate_ids_are_rejected() -> Result<(), Box<dyn Error>> {
    let directory = TestDirectory::new()?;
    directory.write("blob.txt", b"synthetic blob")?;
    let unknown_entry = json!({
        "id": 1,
        "kind": "audio",
        "name": "unknown",
        "source": "blob.txt",
        "license": "CC0-1.0",
        "provenance": "original synthetic test fixture"
    })
    .to_string();
    let unknown_manifest = directory.write("unknown.json", manifest(&unknown_entry).as_bytes())?;
    assert_eq!(
        compile_manifest(&unknown_manifest, &directory.path().join("unknown.pack")),
        Err(CompilerError::UnknownAssetKind)
    );

    let duplicate_manifest = directory.write(
        "duplicate.json",
        manifest(&format!(
            "{},{}",
            blob_entry(7, "blob.txt"),
            blob_entry(7, "blob.txt")
        ))
        .as_bytes(),
    )?;
    assert_eq!(
        compile_manifest(
            &duplicate_manifest,
            &directory.path().join("duplicate.pack")
        ),
        Err(CompilerError::Asset(AssetError::DuplicateId))
    );
    Ok(())
}

#[test]
fn manifest_size_and_record_count_are_bounded() -> Result<(), Box<dyn Error>> {
    let directory = TestDirectory::new()?;
    let oversized = directory.write("oversized.json", &vec![b' '; MAX_MANIFEST_BYTES + 1])?;
    assert_eq!(
        compile_manifest(&oversized, &directory.path().join("oversized.pack")),
        Err(CompilerError::ManifestTooLarge)
    );

    let entries = (0..=MAX_RECORDS)
        .map(|index| u32::try_from(index + 1).map(|id| blob_entry(id, "missing.bin")))
        .collect::<Result<Vec<_>, _>>()?
        .join(",");
    let too_many = directory.write("too-many.json", manifest(&entries).as_bytes())?;
    assert_eq!(
        compile_manifest(&too_many, &directory.path().join("too-many.pack")),
        Err(CompilerError::TooManyAssets)
    );
    Ok(())
}

#[test]
fn existing_final_and_temporary_outputs_are_preserved() -> Result<(), Box<dyn Error>> {
    let directory = TestDirectory::new()?;
    directory.write("blob.txt", b"synthetic blob")?;
    let manifest_path = directory.write(
        "manifest.json",
        manifest(&blob_entry(1, "blob.txt")).as_bytes(),
    )?;
    let output = directory.write("output.pack", b"existing valid output")?;
    assert_eq!(
        compile_manifest(&manifest_path, &output),
        Err(CompilerError::OutputExists)
    );
    assert_eq!(fs::read(&output)?, b"existing valid output");

    fs::remove_file(&output)?;
    let temporary = directory.write(".output.pack.oteryn-tmp", b"stale temporary output")?;
    assert_eq!(
        compile_manifest(&manifest_path, &output),
        Err(CompilerError::TemporaryOutputExists)
    );
    assert_eq!(fs::read(temporary)?, b"stale temporary output");
    assert!(!output.exists());
    Ok(())
}

#[test]
fn pack_does_not_embed_absolute_source_paths() -> Result<(), Box<dyn Error>> {
    let directory = TestDirectory::new()?;
    directory.write("blob.txt", b"synthetic blob")?;
    let manifest_path = directory.write(
        "manifest.json",
        manifest(&blob_entry(1, "blob.txt")).as_bytes(),
    )?;
    let output = directory.path().join("output.pack");
    compile_manifest(&manifest_path, &output)?;
    let encoded = fs::read(output)?;
    let absolute = directory.path().to_string_lossy();
    assert!(
        !encoded
            .windows(absolute.len())
            .any(|window| window == absolute.as_bytes())
    );
    Ok(())
}

#[cfg(unix)]
#[test]
fn symbolic_links_and_special_files_are_rejected_on_unix() -> Result<(), Box<dyn Error>> {
    use std::os::unix::fs::symlink;
    use std::os::unix::net::UnixListener;

    let directory = TestDirectory::new()?;
    directory.write("real.bin", b"synthetic")?;
    symlink("real.bin", directory.path().join("link.bin"))?;
    let link_manifest =
        directory.write("link.json", manifest(&blob_entry(1, "link.bin")).as_bytes())?;
    assert_eq!(
        compile_manifest(&link_manifest, &directory.path().join("link.pack")),
        Err(CompilerError::SourceSymlink)
    );

    let socket_path = directory.path().join("source.sock");
    let _listener = UnixListener::bind(&socket_path)?;
    let socket_manifest = directory.write(
        "socket.json",
        manifest(&blob_entry(2, "source.sock")).as_bytes(),
    )?;
    assert_eq!(
        compile_manifest(&socket_manifest, &directory.path().join("socket.pack")),
        Err(CompilerError::SourceNotFile)
    );

    let dangling_output = directory.path().join("dangling.pack");
    symlink("missing.pack", &dangling_output)?;
    assert_eq!(
        compile_manifest(&link_manifest, &dangling_output),
        Err(CompilerError::OutputExists)
    );
    Ok(())
}

#[cfg(windows)]
#[test]
fn symbolic_link_sources_and_outputs_are_rejected_when_windows_allows_creation()
-> Result<(), Box<dyn Error>> {
    use std::os::windows::fs::symlink_file;

    let directory = TestDirectory::new()?;
    directory.write("real.bin", b"synthetic")?;
    let link = directory.path().join("link.bin");
    match symlink_file("real.bin", &link) {
        Ok(()) => {}
        Err(error) if error.kind() == io::ErrorKind::PermissionDenied => return Ok(()),
        Err(error) => return Err(Box::new(error)),
    }
    let manifest_path = directory.write(
        "manifest.json",
        manifest(&blob_entry(1, "link.bin")).as_bytes(),
    )?;
    assert_eq!(
        compile_manifest(&manifest_path, &directory.path().join("output.pack")),
        Err(CompilerError::SourceSymlink)
    );

    let dangling_output = directory.path().join("dangling.pack");
    symlink_file("missing.pack", &dangling_output)?;
    assert_eq!(
        compile_manifest(&manifest_path, &dangling_output),
        Err(CompilerError::OutputExists)
    );
    Ok(())
}
