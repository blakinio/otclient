from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, found {count}")
    return text.replace(old, new)


workspace = Path("oteryn-client/Cargo.toml")
workspace_text = workspace.read_text(encoding="utf-8")
workspace_text = replace_once(
    workspace_text,
    '    "crates/input-actions",\n    "crates/game-session",',
    '    "crates/input-actions",\n    "crates/input-platform",\n    "crates/game-session",',
    "workspace member",
)
workspace.write_text(workspace_text, encoding="utf-8", newline="\n")

manifest = Path("oteryn-client/crates/input-platform/Cargo.toml")
manifest_text = manifest.read_text(encoding="utf-8")
manifest_text = replace_once(
    manifest_text,
    '''edition = "2024"
rust-version = "1.94"
license = "MIT"
repository = "https://github.com/blakinio/otclient"
''',
    '''edition.workspace = true
rust-version.workspace = true
license.workspace = true
repository.workspace = true
''',
    "workspace package inheritance",
)
manifest_text = replace_once(
    manifest_text,
    '''[lints.rust]
unsafe_code = "forbid"
unused_must_use = "deny"

[lints.clippy]
all = { level = "deny", priority = -1 }
dbg_macro = "deny"
expect_used = "deny"
panic = "deny"
todo = "deny"
unimplemented = "deny"
unwrap_used = "deny"

# Exclusive-path development is intentionally standalone until the serialized
# workspace/lockfile lease reaches Input Platform. Remove this nested workspace
# marker when the crate is integrated into the parent workspace under that lease.
[workspace]
''',
    '''[lints]
workspace = true
''',
    "workspace lint integration",
)
manifest.write_text(manifest_text, encoding="utf-8", newline="\n")

lock = Path("oteryn-client/Cargo.lock")
lock_text = lock.read_text(encoding="utf-8")
lock_text = replace_once(
    lock_text,
    '''[[package]]
name = "oteryn-input-actions"
version = "0.1.0"

[[package]]
name = "oteryn-platform"
''',
    '''[[package]]
name = "oteryn-input-actions"
version = "0.1.0"

[[package]]
name = "oteryn-input-platform"
version = "0.1.0"
dependencies = [
 "oteryn-input-actions",
 "winit",
]

[[package]]
name = "oteryn-platform"
''',
    "local lockfile package",
)
lock.write_text(lock_text, encoding="utf-8", newline="\n")

policy_path = Path("oteryn-client/tools/architecture-check/src/lib.rs")
policy = policy_path.read_text(encoding="utf-8")
policy = replace_once(
    policy,
    '        "input" => matches!(target, "foundation" | "settings" | "diagnostics"),',
    '        "input" => matches!(target, "foundation" | "input" | "settings" | "diagnostics"),',
    "input same-category edge",
)
if "fn input_platform_dependency_edges_are_narrow()" not in policy:
    policy += '''

#[cfg(test)]
mod input_platform_policy_tests {
    use super::*;

    #[test]
    fn input_platform_dependency_edges_are_narrow() {
        assert!(dependency_allowed(
            "input",
            "input",
            DependencyKind::Normal
        ));
        assert!(dependency_allowed(
            "input",
            "foundation",
            DependencyKind::Normal
        ));
        assert!(!dependency_allowed(
            "input",
            "platform",
            DependencyKind::Normal
        ));
        assert!(!dependency_allowed(
            "input",
            "runtime",
            DependencyKind::Normal
        ));
        assert!(!dependency_allowed(
            "input",
            "renderer",
            DependencyKind::Normal
        ));
    }
}
'''
policy_path.write_text(policy, encoding="utf-8", newline="\n")

layout = Path("oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md")
layout_text = layout.read_text(encoding="utf-8")
layout_text = replace_once(
    layout_text,
    "│   ├── input/\n│   ├── audio/",
    "│   ├── input/\n│   ├── input-platform/\n│   ├── audio/",
    "repository tree",
)
layout_text = replace_once(
    layout_text,
    "| `input` | devices, bindings, contexts and semantic actions | direct socket writes |\n| `audio` |",
    "| `input` | framework-neutral normalized physical events, contexts, bindings and semantic actions | native windowing types, global hooks, background capture or direct socket writes |\n| `input-platform` | bounded Windows/winit physical-event normalization into the merged `input` contract | product keymaps, gameplay commands, UI actions, native identifier retention, global hooks or application composition |\n| `audio` |",
    "responsibility table",
)
layout_text = replace_once(
    layout_text,
    "renderer-resource\n├── asset-decode\n├── asset-runtime\n└── foundation\n\ntest-support",
    "renderer-resource\n├── asset-decode\n├── asset-runtime\n└── foundation\n\ninput-platform\n└── input\n\ntest-support",
    "dependency direction",
)
layout_text = replace_once(
    layout_text,
    "`renderer-resource` is a backend-neutral renderer-category producer over `asset-decode`, `asset-runtime` and foundation; it owns no device, world or draw policy. `asset-decode` is a dedicated bounded decode category",
    "`renderer-resource` is a backend-neutral renderer-category producer over `asset-decode`, `asset-runtime` and foundation; it owns no device, world or draw policy. `input-platform` is an input-category producer over the merged framework-neutral `input` contract and owns no product keymap, command, UI action or application lifecycle. `asset-decode` is a dedicated bounded decode category",
    "dependency prose",
)
layout.write_text(layout_text, encoding="utf-8", newline="\n")
