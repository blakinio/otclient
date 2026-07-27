use oteryn_architecture_check::check_fixture;
use std::path::{Path, PathBuf};

fn fixture_path(name: &str) -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../tests/architecture-fixtures")
        .join(name)
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
        ("invalid_domain_to_canary_edge.json", "E005_FORBIDDEN_EDGE"),
        (
            "invalid_renderer_to_feature_edge.json",
            "E005_FORBIDDEN_EDGE",
        ),
        (
            "invalid_ui_core_to_feature_edge.json",
            "E005_FORBIDDEN_EDGE",
        ),
        ("invalid_foundation_upward_edge.json", "E005_FORBIDDEN_EDGE"),
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
