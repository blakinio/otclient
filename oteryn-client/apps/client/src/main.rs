#[cfg(windows)]
mod technical_login;

#[cfg(windows)]
mod windows_shell;

#[cfg(windows)]
fn main() -> std::process::ExitCode {
    windows_shell::main()
}

#[cfg(not(windows))]
fn main() {
    eprintln!("the Oteryn renderer surface spike is validated only on Windows");
}
