use oteryn_architecture_check::{check_fixture, check_workspace, Violation};
use std::env;
use std::path::Path;
use std::process::ExitCode;

fn main() -> ExitCode {
    match run(env::args().skip(1).collect()) {
        Ok(()) => ExitCode::SUCCESS,
        Err(message) => {
            eprintln!("{message}");
            ExitCode::from(2)
        }
    }
}

fn run(arguments: Vec<String>) -> Result<(), String> {
    match arguments.as_slice() {
        [command, path] if command == "workspace" => {
            let violations = check_workspace(Path::new(path))?;
            report("workspace", path, &violations)
        }
        [command, path] if command == "fixture" => {
            let violations = check_fixture(Path::new(path))?;
            report("fixture", path, &violations)
        }
        _ => Err("usage: oteryn-architecture-check <workspace|fixture> <path>".to_owned()),
    }
}

fn report(kind: &str, path: &str, violations: &[Violation]) -> Result<(), String> {
    if violations.is_empty() {
        println!("architecture policy passed for {kind} '{path}'");
        return Ok(());
    }

    let details = violations
        .iter()
        .map(ToString::to_string)
        .collect::<Vec<_>>()
        .join("\n");
    Err(format!(
        "architecture policy failed for {kind} '{path}' with {} violation(s):\n{details}",
        violations.len()
    ))
}
