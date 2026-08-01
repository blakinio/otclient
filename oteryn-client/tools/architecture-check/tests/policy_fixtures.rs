use oteryn_architecture_check::{
    DependencyKind, FIXTURE_SCHEMA_VERSION, check_fixture, check_fixture_json, dependency_allowed,
    known_categories,
};
use serde_json::json;
use std::path::{Path, PathBuf};

fn fixture_path(name: &str) -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../tests/architecture-fixtures")
        .join(name)
}

fn edge_fixture(source: &str, target: &str, kind: DependencyKind) -> String {
    json!({
        "schema_version": FIXTURE_SCHEMA_VERSION,
        "workspace_root": "/workspace/oteryn-client",
        "packages": [
            {
                "name": "oteryn-source",
                "category": source,
                "manifest_path": "/workspace/oteryn-client/source/Cargo.toml",
                "dependencies": [
                    {
                        "name": "oteryn-target",
                        "path": "/workspace/oteryn-client/target",
                        "source": null,
                        "kind": kind.as_str()
                    }
                ]
            },
            {
                "name": "oteryn-target",
                "category": target,
                "manifest_path": "/workspace/oteryn-client/target/Cargo.toml",
                "dependencies": []
            }
        ]
    })
    .to_string()
}

#[test]
fn valid_minimal_workspace_passes() -> Result<(), String> {
    let violations = check_fixture(&fixture_path("valid_minimal_workspace.json"))?;
    assert!(
        violations.is_empty(),
        "unexpected violations: {violations:?}"
    );
    Ok(())
}

#[test]
fn valid_foundation_dependency_passes() -> Result<(), String> {
    let violations = check_fixture(&fixture_path("valid_foundation_dependency.json"))?;
    assert!(
        violations.is_empty(),
        "unexpected violations: {violations:?}"
    );
    Ok(())
}

#[test]
fn invalid_fixtures_report_expected_rules() -> Result<(), String> {
    let cases = [
        (
            "invalid_legacy_path_dependency.json",
            "E003_OUTSIDE_WORKSPACE",
        ),
        (
            "invalid_domain_to_canary_edge.json",
            "E005_FORBIDDEN_EDGE",
        ),
        (
            "invalid_renderer_to_feature_edge.json",
            "E005_FORBIDDEN_EDGE",
        ),
        (
            "invalid_ui_core_to_feature_edge.json",
            "E005_FORBIDDEN_EDGE",
        ),
        (
            "invalid_foundation_upward_edge.json",
            "E005_FORBIDDEN_EDGE",
        ),
        ("invalid_feature_cycle.json", "E006_DEPENDENCY_CYCLE"),
        (
            "invalid_unapproved_source_dependency.json",
            "E004_UNAPPROVED_SOURCE",
        ),
    ];

    for (fixture, expected_code) in cases {
        let violations = check_fixture(&fixture_path(fixture))?;
        assert!(
            violations
                .iter()
                .any(|violation| violation.code == expected_code),
            "fixture {fixture} did not report {expected_code}: {violations:?}"
        );
    }
    Ok(())
}

#[test]
fn every_category_pair_and_dependency_kind_matches_the_complete_policy() -> Result<(), String> {
    let kinds = [
        DependencyKind::Normal,
        DependencyKind::Build,
        DependencyKind::Dev,
    ];

    for kind in kinds {
        let mut allowed_count = 0_usize;
        let mut denied_count = 0_usize;
        for source in known_categories() {
            for target in known_categories() {
                let expected_allowed = dependency_allowed(source, target, kind);
                let violations = check_fixture_json(&edge_fixture(source, target, kind))?;
                let forbidden_count = violations
                    .iter()
                    .filter(|violation| violation.code == "E005_FORBIDDEN_EDGE")
                    .count();
                assert_eq!(
                    forbidden_count,
                    usize::from(!expected_allowed),
                    "policy mismatch for {kind} edge {source} -> {target}: {violations:?}"
                );
                assert!(
                    violations
                        .iter()
                        .all(|violation| violation.code == "E005_FORBIDDEN_EDGE"),
                    "unexpected non-policy violation for {kind} edge {source} -> {target}: {violations:?}"
                );
                if expected_allowed {
                    allowed_count += 1;
                } else {
                    denied_count += 1;
                }
            }
        }
        assert!(allowed_count > 0, "{kind} policy has no allowed edge");
        assert!(denied_count > 0, "{kind} policy has no denied edge");
    }
    Ok(())
}

#[test]
fn product_to_tool_is_dev_only() -> Result<(), String> {
    let normal = check_fixture_json(&edge_fixture("app", "tool", DependencyKind::Normal))?;
    assert!(
        normal
            .iter()
            .any(|violation| violation.code == "E005_FORBIDDEN_EDGE")
    );

    let dev = check_fixture_json(&edge_fixture("app", "tool", DependencyKind::Dev))?;
    assert!(dev.is_empty(), "unexpected dev-edge violations: {dev:?}");
    Ok(())
}

#[test]
fn build_dependencies_require_an_explicit_pair() -> Result<(), String> {
    let listed = check_fixture_json(&edge_fixture(
        "tool",
        "foundation",
        DependencyKind::Build,
    ))?;
    assert!(
        listed.is_empty(),
        "unexpected listed build violation: {listed:?}"
    );

    let unlisted = check_fixture_json(&edge_fixture(
        "app",
        "foundation",
        DependencyKind::Build,
    ))?;
    assert!(
        unlisted
            .iter()
            .any(|violation| violation.code == "E005_FORBIDDEN_EDGE")
    );
    Ok(())
}

#[test]
fn schema_v2_requires_dependency_kind() {
    let fixture = json!({
        "schema_version": FIXTURE_SCHEMA_VERSION,
        "workspace_root": "/workspace/oteryn-client",
        "packages": [
            {
                "name": "oteryn-source",
                "category": "app",
                "manifest_path": "/workspace/oteryn-client/source/Cargo.toml",
                "dependencies": [
                    {
                        "name": "oteryn-target",
                        "path": "/workspace/oteryn-client/target",
                        "source": null
                    }
                ]
            },
            {
                "name": "oteryn-target",
                "category": "foundation",
                "manifest_path": "/workspace/oteryn-client/target/Cargo.toml",
                "dependencies": []
            }
        ]
    })
    .to_string();

    let error = check_fixture_json(&fixture).expect_err("schema v2 must require dependency.kind");
    assert!(error.contains("dependency.kind"), "unexpected error: {error}");
}

#[test]
fn legacy_schema_v1_defaults_missing_kind_to_normal() -> Result<(), String> {
    let fixture = json!({
        "schema_version": 1,
        "workspace_root": "/workspace/oteryn-client",
        "packages": [
            {
                "name": "oteryn-source",
                "category": "game-domain",
                "manifest_path": "/workspace/oteryn-client/source/Cargo.toml",
                "dependencies": [
                    {
                        "name": "oteryn-target",
                        "path": "/workspace/oteryn-client/target",
                        "source": null
                    }
                ]
            },
            {
                "name": "oteryn-target",
                "category": "protocol-canary",
                "manifest_path": "/workspace/oteryn-client/target/Cargo.toml",
                "dependencies": []
            }
        ]
    })
    .to_string();

    let violations = check_fixture_json(&fixture)?;
    assert!(
        violations
            .iter()
            .any(|violation| violation.code == "E005_FORBIDDEN_EDGE")
    );
    Ok(())
}
