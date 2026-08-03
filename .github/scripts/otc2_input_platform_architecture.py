from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, found {count}")
    return text.replace(old, new)


manifest = Path("oteryn-client/crates/input-platform/Cargo.toml")
manifest_text = manifest.read_text(encoding="utf-8")
manifest_text = replace_once(
    manifest_text,
    'category = "input"',
    'category = "input-platform"',
    "input-platform category",
)
manifest.write_text(manifest_text, encoding="utf-8", newline="\n")

policy_path = Path("oteryn-client/tools/architecture-check/src/lib.rs")
policy = policy_path.read_text(encoding="utf-8")

known_start = policy.index("const KNOWN_CATEGORIES")
product_start = policy.index("const PRODUCT_CATEGORIES")
known = policy[known_start:product_start]
known = replace_once(
    known,
    '    "input",\n    "audio",',
    '    "input",\n    "input-platform",\n    "audio",',
    "known category",
)
policy = policy[:known_start] + known + policy[product_start:]

product_start = policy.index("const PRODUCT_CATEGORIES")
build_start = policy.index("const ALLOWED_BUILD_EDGES")
product = policy[product_start:build_start]
product = replace_once(
    product,
    '    "input",\n    "audio",',
    '    "input",\n    "input-platform",\n    "audio",',
    "product category",
)
policy = policy[:product_start] + product + policy[build_start:]

policy = replace_once(
    policy,
    '        "input" => matches!(target, "foundation" | "input" | "settings" | "diagnostics"),',
    '        "input" => matches!(target, "foundation" | "settings" | "diagnostics"),\n        "input-platform" => target == "input",',
    "narrow category edge",
)

old_tests = '''#[cfg(test)]
mod input_platform_policy_tests {
    use super::*;

    #[test]
    fn input_platform_dependency_edges_are_narrow() {
        assert!(dependency_allowed("input", "input", DependencyKind::Normal));
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
}'''
new_tests = '''#[cfg(test)]
mod input_platform_policy_tests {
    use super::*;

    #[test]
    fn input_platform_dependency_edges_are_narrow() {
        assert!(dependency_allowed(
            "input-platform",
            "input",
            DependencyKind::Normal
        ));
        assert!(!dependency_allowed(
            "input",
            "input-platform",
            DependencyKind::Normal
        ));
        assert!(!dependency_allowed(
            "input-platform",
            "foundation",
            DependencyKind::Normal
        ));
        assert!(!dependency_allowed(
            "input-platform",
            "platform",
            DependencyKind::Normal
        ));
        assert!(!dependency_allowed(
            "input-platform",
            "runtime",
            DependencyKind::Normal
        ));
        assert!(!dependency_allowed(
            "input-platform",
            "renderer",
            DependencyKind::Normal
        ));
    }
}'''
policy = replace_once(policy, old_tests, new_tests, "policy tests")
policy_path.write_text(policy, encoding="utf-8", newline="\n")

layout = Path("oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md")
layout_text = layout.read_text(encoding="utf-8")
layout_text = replace_once(
    layout_text,
    "`input-platform` is an input-category producer over the merged framework-neutral `input` contract",
    "`input-platform` is a dedicated platform-input category producer over the merged framework-neutral `input` contract",
    "category prose",
)
layout.write_text(layout_text, encoding="utf-8", newline="\n")
