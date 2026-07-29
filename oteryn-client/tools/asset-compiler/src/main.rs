use oteryn_asset_compiler::{CompilerError, compile_manifest};
use std::env;
use std::ffi::OsString;
use std::path::Path;
use std::process::ExitCode;

fn main() -> ExitCode {
    match run(env::args_os().skip(1).collect()) {
        Ok((record_count, encoded_bytes)) => {
            println!("compiled {record_count} synthetic asset record(s) into {encoded_bytes} byte(s)");
            ExitCode::SUCCESS
        }
        Err(message) => {
            eprintln!("{message}");
            ExitCode::from(2)
        }
    }
}

fn run(arguments: Vec<OsString>) -> Result<(usize, usize), String> {
    let [manifest, output] = arguments.as_slice() else {
        return Err("usage: oteryn-asset-compiler <manifest.json> <output.pack>".to_owned());
    };
    let report = compile_manifest(Path::new(manifest), Path::new(output)).map_err(stable_error)?;
    Ok((report.record_count(), report.encoded_bytes()))
}

fn stable_error(error: CompilerError) -> String {
    format!("asset compilation failed: {error}")
}
