use oteryn_asset_compiler::compile_manifest;
use oteryn_asset_runtime::{AssetRuntime, PackGeneration, RuntimeLimits};
use oteryn_asset_types::AssetId;
use std::error::Error;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicU64, Ordering};

static NEXT_DIRECTORY: AtomicU64 = AtomicU64::new(1);

struct TestDirectory(PathBuf);

impl TestDirectory {
    fn create() -> io::Result<Self> {
        for _ in 0..100 {
            let sequence = NEXT_DIRECTORY.fetch_add(1, Ordering::Relaxed);
            let path = std::env::temp_dir().join(format!(
                "oteryn-asset-runtime-compiler-{}-{sequence}",
                std::process::id()
            ));
            match fs::create_dir(&path) {
                Ok(()) => return Ok(Self(path)),
                Err(error) if error.kind() == io::ErrorKind::AlreadyExists => continue,
                Err(error) => return Err(error),
            }
        }
        Err(io::Error::new(
            io::ErrorKind::AlreadyExists,
            "could not allocate unique asset-runtime test directory",
        ))
    }

    fn join(&self, path: impl AsRef<Path>) -> PathBuf {
        self.0.join(path)
    }
}

impl Drop for TestDirectory {
    fn drop(&mut self) {
        let _cleanup_result = fs::remove_dir_all(&self.0);
    }
}

#[test]
fn compiler_output_opens_and_indexes_deterministically() -> Result<(), Box<dyn Error>> {
    let directory = TestDirectory::create()?;
    let source = directory.join("source.bin");
    let manifest = directory.join("manifest.json");
    let first_output = directory.join("first.pack");
    let second_output = directory.join("second.pack");

    fs::write(&source, b"project-original synthetic payload")?;
    fs::write(
        &manifest,
        r#"{"schema_version":1,"assets":[{"id":7,"kind":"blob","name":"fixture","source":"source.bin","license":"CC0-1.0","provenance":"project-original synthetic fixture"}]}"#,
    )?;

    let first_report = compile_manifest(&manifest, &first_output)?;
    let second_report = compile_manifest(&manifest, &second_output)?;
    let first_bytes = fs::read(&first_output)?;
    let second_bytes = fs::read(&second_output)?;

    assert_eq!(first_bytes, second_bytes);
    assert_eq!(first_report.record_count(), 1);
    assert_eq!(first_report, second_report);
    assert_eq!(first_report.encoded_bytes(), first_bytes.len());

    let runtime = AssetRuntime::open_bytes(
        PackGeneration::new(9)?,
        &first_bytes,
        RuntimeLimits::schema_v1(),
    )?;
    let handle = runtime
        .handle(AssetId::new(7)?)
        .ok_or_else(|| io::Error::other("compiled asset handle is missing"))?;
    let view = runtime.lookup(handle)?;

    assert_eq!(runtime.record_count(), 1);
    assert_eq!(view.metadata().logical_name(), "fixture");
    assert_eq!(view.payload(), b"project-original synthetic payload");
    Ok(())
}
