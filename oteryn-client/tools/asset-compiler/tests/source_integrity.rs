use oteryn_asset_compiler::{CompilerError, compile_manifest};
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
            "oteryn-asset-source-integrity-{}-{sequence}",
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

fn manifest(source: &str) -> String {
    json!({
        "schema_version": 1,
        "assets": [{
            "id": 1,
            "kind": "blob",
            "name": "nested-source",
            "source": source,
            "license": "CC0-1.0",
            "provenance": "original synthetic source-integrity fixture"
        }]
    })
    .to_string()
}

#[test]
fn regular_intermediate_directories_are_opened_successfully() -> Result<(), Box<dyn Error>> {
    let directory = TestDirectory::new()?;
    directory.write("real/nested/payload.bin", b"accepted nested payload")?;
    let manifest_path = directory.write(
        "manifest.json",
        manifest("real/nested/payload.bin").as_bytes(),
    )?;
    let output = directory.path().join("output.pack");

    let report = compile_manifest(&manifest_path, &output)?;
    assert_eq!(report.record_count(), 1);
    assert!(output.is_file());
    Ok(())
}

#[test]
fn symlinked_intermediate_directories_are_rejected_when_supported() -> Result<(), Box<dyn Error>> {
    let directory = TestDirectory::new()?;
    directory.write("real/payload.bin", b"must not be reached through a link")?;
    let linked = directory.path().join("linked");

    match create_directory_symlink(Path::new("real"), &linked) {
        Ok(()) => {}
        Err(error) if symlink_creation_is_unavailable(&error) => return Ok(()),
        Err(error) => return Err(Box::new(error)),
    }

    let manifest_path =
        directory.write("manifest.json", manifest("linked/payload.bin").as_bytes())?;
    let output = directory.path().join("output.pack");
    assert_eq!(
        compile_manifest(&manifest_path, &output),
        Err(CompilerError::SourceSymlink)
    );
    assert!(!output.exists());
    Ok(())
}

#[cfg(unix)]
fn create_directory_symlink(target: &Path, link: &Path) -> io::Result<()> {
    std::os::unix::fs::symlink(target, link)
}

#[cfg(windows)]
fn create_directory_symlink(target: &Path, link: &Path) -> io::Result<()> {
    std::os::windows::fs::symlink_dir(target, link)
}

fn symlink_creation_is_unavailable(error: &io::Error) -> bool {
    error.kind() == io::ErrorKind::PermissionDenied || error.kind() == io::ErrorKind::Unsupported
}
