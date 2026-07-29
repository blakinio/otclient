use oteryn_asset_compiler::{CompilerError, compile_manifest};
use oteryn_asset_types::AssetError;
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
    format!(
        r#"{{"id":{id},"kind":"blob","name":"blob-{id}","source":"{source}","license":"CC0-1.0","provenance":"original synthetic test fixture"}}"#
    )
}

fn rgba_entry(id: u32, source: &str) -> String {
    format!(
        r#"{{"id":{id},"kind":"rgba8","name":"rgba-{id}","source":"{source}","license":"CC0-1.0","provenance":"original synthetic test fixture","width":2,"height":2}}"#
    )
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
fn malformed_or_extended_manifest_is_rejected() -> Result<(), Box<dyn Error>> {
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
    Ok(())
}

#[test]
fn existing_final_output_is_preserved() -> Result<(), Box<dyn Error>> {
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
    assert_eq!(fs::read(output)?, b"existing valid output");
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
fn symbolic_link_sources_are_rejected_on_unix() -> Result<(), Box<dyn Error>> {
    use std::os::unix::fs::symlink;

    let directory = TestDirectory::new()?;
    directory.write("real.bin", b"synthetic")?;
    symlink("real.bin", directory.path().join("link.bin"))?;
    let manifest_path = directory.write(
        "manifest.json",
        manifest(&blob_entry(1, "link.bin")).as_bytes(),
    )?;
    assert_eq!(
        compile_manifest(&manifest_path, &directory.path().join("output.pack")),
        Err(CompilerError::SourceSymlink)
    );
    Ok(())
}

#[cfg(windows)]
#[test]
fn symbolic_link_sources_are_rejected_when_windows_allows_creation() -> Result<(), Box<dyn Error>> {
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
    Ok(())
}
