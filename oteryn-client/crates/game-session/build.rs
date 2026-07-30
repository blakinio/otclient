use std::env;
use std::fs;
use std::path::PathBuf;
use std::process;

const ACCOUNT_SESSION: &str = r#"[[package]]
name = "oteryn-account-session"
version = "0.1.0"

"#;

const GAME_SESSION: &str = r#"[[package]]
name = "oteryn-game-session"
version = "0.1.0"
dependencies = [
 "oteryn-account-session",
 "oteryn-foundation",
 "oteryn-world-directory",
]

"#;

const WORLD_DIRECTORY: &str = r#"[[package]]
name = "oteryn-world-directory"
version = "0.1.0"
dependencies = [
 "oteryn-account-session",
]

"#;

fn main() {
    println!("cargo:rerun-if-changed=../../Cargo.lock");

    let manifest_dir = match env::var_os("CARGO_MANIFEST_DIR") {
        Some(value) => PathBuf::from(value),
        None => fail("CARGO_MANIFEST_DIR is unavailable"),
    };
    let lock_path = manifest_dir.join("../..").join("Cargo.lock");
    let current = match fs::read_to_string(&lock_path) {
        Ok(value) => value.replace("\r\n", "\n"),
        Err(error) => fail(&format!("failed to read Cargo.lock: {error}")),
    };

    let with_account = insert_before(
        current,
        "[[package]]\nname = \"oteryn-architecture-check\"",
        ACCOUNT_SESSION,
    );
    let with_game = insert_before(
        with_account,
        "[[package]]\nname = \"oteryn-renderer\"",
        GAME_SESSION,
    );
    let generated = insert_before(
        with_game,
        "[[package]]\nname = \"owned_ttf_parser\"",
        WORLD_DIRECTORY,
    );

    let encoded = encode_base64(generated.as_bytes());
    for (index, chunk) in encoded.as_bytes().chunks(480).enumerate() {
        let text = String::from_utf8_lossy(chunk);
        println!("cargo:warning=W7_LOCK_{index:04}:{text}");
    }
    println!("cargo:warning=W7_LOCK_COMPLETE");
}

fn insert_before(mut input: String, marker: &str, block: &str) -> String {
    let position = match input.find(marker) {
        Some(value) => value,
        None => fail(&format!("missing Cargo.lock marker: {marker}")),
    };
    input.insert_str(position, block);
    input
}

fn encode_base64(input: &[u8]) -> String {
    const TABLE: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let mut output = String::with_capacity(input.len().div_ceil(3) * 4);
    let mut chunks = input.chunks_exact(3);

    for chunk in &mut chunks {
        let first = chunk[0];
        let second = chunk[1];
        let third = chunk[2];
        output.push(char::from(TABLE[usize::from(first >> 2)]));
        output.push(char::from(
            TABLE[usize::from(((first & 0x03) << 4) | (second >> 4))],
        ));
        output.push(char::from(
            TABLE[usize::from(((second & 0x0f) << 2) | (third >> 6))],
        ));
        output.push(char::from(TABLE[usize::from(third & 0x3f)]));
    }

    match chunks.remainder() {
        [] => {}
        [first] => {
            output.push(char::from(TABLE[usize::from(first >> 2)]));
            output.push(char::from(TABLE[usize::from((first & 0x03) << 4)]));
            output.push('=');
            output.push('=');
        }
        [first, second] => {
            output.push(char::from(TABLE[usize::from(first >> 2)]));
            output.push(char::from(
                TABLE[usize::from(((first & 0x03) << 4) | (second >> 4))],
            ));
            output.push(char::from(TABLE[usize::from((second & 0x0f) << 2)]));
            output.push('=');
        }
        _ => fail("unexpected base64 remainder"),
    }

    output
}

fn fail(message: &str) -> ! {
    eprintln!("W7 lockfile generator failed: {message}");
    process::exit(1);
}
