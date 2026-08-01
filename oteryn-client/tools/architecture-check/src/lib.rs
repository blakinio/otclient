//! Architecture policy validation for the greenfield Oteryn Rust workspace.

use serde_json::Value;
use std::collections::{BTreeMap, BTreeSet};
use std::fmt::{self, Display, Formatter};
use std::fs;
use std::path::Path;
use std::process::Command;

/// Current synthetic fixture schema.
pub const FIXTURE_SCHEMA_VERSION: u64 = 2;
const LEGACY_FIXTURE_SCHEMA_VERSION: u64 = 1;
const PACKAGE_PREFIX: &str = "oteryn-";
const ALLOWED_REGISTRY: &str = "registry+https://github.com/rust-lang/crates.io-index";
const ALLOWED_SPARSE_REGISTRY: &str = "sparse+https://index.crates.io/";

const KNOWN_CATEGORIES: &[&str] = &[
    "tool",
    "app",
    "foundation",
    "platform",
    "runtime",
    "identity",
    "account-session",
    "world-directory",
    "game-session",
    "transport",
    "protocol-core",
    "protocol-canary",
    "protocol-oteryn",
    "game-domain",
    "game-simulation",
    "world-storage",
    "render-types",
    "renderer",
    "ui-core",
    "ui-runtime",
    "input",
    "audio",
    "asset-types",
    "asset-runtime",
    "settings",
    "diagnostics",
    "extension-api",
    "extension-host",
    "feature",
];

const PRODUCT_CATEGORIES: &[&str] = &[
    "foundation",
    "platform",
    "runtime",
    "identity",
    "account-session",
    "world-directory",
    "game-session",
    "transport",
    "protocol-core",
    "protocol-canary",
    "protocol-oteryn",
    "game-domain",
    "game-simulation",
    "world-storage",
    "render-types",
    "renderer",
    "ui-core",
    "ui-runtime",
    "input",
    "audio",
    "asset-types",
    "asset-runtime",
    "settings",
    "diagnostics",
    "extension-api",
    "extension-host",
    "feature",
];

const ALLOWED_BUILD_EDGES: &[(&str, &str)] = &[("tool", "foundation"), ("tool", "asset-types")];

/// Cargo dependency kinds covered by the architecture policy.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum DependencyKind {
    /// Runtime/production dependency.
    Normal,
    /// Build-script dependency.
    Build,
    /// Test/example/benchmark-only dependency.
    Dev,
}

impl DependencyKind {
    /// Stable fixture and diagnostic spelling.
    #[must_use]
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Normal => "normal",
            Self::Build => "build",
            Self::Dev => "dev",
        }
    }
}

impl Display for DependencyKind {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str(self.as_str())
    }
}

/// Return the closed category catalogue used by the policy matrix.
#[must_use]
pub const fn known_categories() -> &'static [&'static str] {
    KNOWN_CATEGORIES
}

/// Return the explicit allow-policy result for one category edge and dependency kind.
#[must_use]
pub fn dependency_allowed(source: &str, target: &str, kind: DependencyKind) -> bool {
    if !is_known_category(source) || !is_known_category(target) {
        return false;
    }
    match kind {
        DependencyKind::Normal => allowed_normal_edge(source, target),
        DependencyKind::Build => ALLOWED_BUILD_EDGES.contains(&(source, target)),
        DependencyKind::Dev => target == "tool" || allowed_normal_edge(source, target),
    }
}

fn allowed_normal_edge(source: &str, target: &str) -> bool {
    match source {
        "tool" => KNOWN_CATEGORIES.contains(&target),
        "app" => PRODUCT_CATEGORIES.contains(&target),
        "foundation" => target == "foundation",
        "platform" => matches!(
            target,
            "foundation"
                | "account-session"
                | "world-directory"
                | "game-session"
                | "transport"
                | "settings"
                | "diagnostics"
        ),
        "runtime" => matches!(
            target,
            "foundation"
                | "platform"
                | "identity"
                | "account-session"
                | "world-directory"
                | "game-session"
                | "transport"
                | "protocol-core"
                | "game-domain"
                | "game-simulation"
                | "world-storage"
                | "render-types"
                | "renderer"
                | "ui-core"
                | "ui-runtime"
                | "input"
                | "audio"
                | "asset-types"
                | "asset-runtime"
                | "settings"
                | "diagnostics"
                | "extension-api"
                | "extension-host"
        ),
        "identity" => matches!(
            target,
            "foundation"
                | "platform"
                | "account-session"
                | "world-directory"
                | "game-session"
                | "transport"
                | "settings"
                | "diagnostics"
        ),
        "account-session" => matches!(target, "foundation" | "diagnostics"),
        "world-directory" => matches!(target, "foundation" | "account-session" | "diagnostics"),
        "game-session" => matches!(
            target,
            "foundation" | "account-session" | "world-directory" | "game-domain" | "diagnostics"
        ),
        "transport" => matches!(target, "foundation" | "settings" | "diagnostics"),
        "protocol-core" => matches!(target, "foundation" | "diagnostics"),
        "protocol-canary" | "protocol-oteryn" => matches!(
            target,
            "foundation"
                | "transport"
                | "protocol-core"
                | "account-session"
                | "world-directory"
                | "game-session"
                | "game-domain"
                | "settings"
                | "diagnostics"
        ),
        "game-domain" => matches!(
            target,
            "foundation" | "account-session" | "world-directory" | "settings" | "diagnostics"
        ),
        "game-simulation" => matches!(
            target,
            "foundation"
                | "game-domain"
                | "game-session"
                | "world-directory"
                | "settings"
                | "diagnostics"
        ),
        "world-storage" => matches!(
            target,
            "foundation" | "game-domain" | "world-directory" | "settings" | "diagnostics"
        ),
        "render-types" => matches!(target, "foundation" | "asset-types"),
        "renderer" => matches!(
            target,
            "foundation"
                | "render-types"
                | "asset-types"
                | "asset-runtime"
                | "settings"
                | "diagnostics"
        ),
        "ui-core" => matches!(
            target,
            "foundation" | "render-types" | "asset-types" | "input" | "settings" | "diagnostics"
        ),
        "ui-runtime" => matches!(
            target,
            "foundation"
                | "ui-core"
                | "renderer"
                | "render-types"
                | "input"
                | "audio"
                | "asset-runtime"
                | "settings"
                | "diagnostics"
                | "extension-api"
        ),
        "input" => matches!(target, "foundation" | "settings" | "diagnostics"),
        "audio" => matches!(
            target,
            "foundation" | "asset-types" | "asset-runtime" | "settings" | "diagnostics"
        ),
        "asset-types" => target == "foundation",
        "asset-runtime" => matches!(
            target,
            "foundation" | "asset-types" | "settings" | "diagnostics"
        ),
        "settings" => matches!(target, "foundation" | "diagnostics"),
        "diagnostics" => target == "foundation",
        "extension-api" => matches!(
            target,
            "foundation"
                | "game-domain"
                | "render-types"
                | "ui-core"
                | "asset-types"
                | "settings"
                | "diagnostics"
        ),
        "extension-host" => matches!(
            target,
            "foundation"
                | "extension-api"
                | "runtime"
                | "ui-runtime"
                | "asset-runtime"
                | "settings"
                | "diagnostics"
        ),
        "feature" => matches!(
            target,
            "foundation"
                | "runtime"
                | "identity"
                | "account-session"
                | "world-directory"
                | "game-session"
                | "transport"
                | "protocol-core"
                | "game-domain"
                | "game-simulation"
                | "world-storage"
                | "render-types"
                | "renderer"
                | "ui-core"
                | "ui-runtime"
                | "input"
                | "audio"
                | "asset-types"
                | "asset-runtime"
                | "settings"
                | "diagnostics"
                | "extension-api"
                | "extension-host"
        ),
        _ => false,
    }
}

fn is_known_category(category: &str) -> bool {
    KNOWN_CATEGORIES.contains(&category)
}

/// One actionable architecture-policy violation.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Violation {
    /// Stable machine-readable rule code.
    pub code: &'static str,
    /// Human-readable explanation with the relevant package or edge.
    pub message: String,
}

impl Violation {
    fn new(code: &'static str, message: impl Into<String>) -> Self {
        Self {
            code,
            message: message.into(),
        }
    }
}

impl Display for Violation {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        write!(formatter, "{}: {}", self.code, self.message)
    }
}

/// Parsed workspace graph used by Cargo metadata and synthetic fixtures.
#[derive(Debug, Clone)]
pub struct WorkspaceGraph {
    root: String,
    packages: Vec<Package>,
}

#[derive(Debug, Clone)]
struct Package {
    name: String,
    category: String,
    manifest_path: String,
    dependencies: Vec<Dependency>,
}

#[derive(Debug, Clone)]
struct Dependency {
    name: String,
    path: Option<String>,
    source: Option<String>,
    kind: DependencyKind,
}

/// Load and validate a synthetic JSON fixture.
///
/// # Errors
///
/// Returns an error when the fixture cannot be read or its JSON shape is invalid.
pub fn check_fixture(path: &Path) -> Result<Vec<Violation>, String> {
    let contents = fs::read_to_string(path)
        .map_err(|error| format!("failed to read fixture {}: {error}", path.display()))?;
    check_fixture_json(&contents)
        .map_err(|error| format!("failed to validate fixture {}: {error}", path.display()))
}

/// Parse and validate one synthetic JSON fixture from memory.
///
/// # Errors
///
/// Returns an error when JSON or the fixture shape is invalid.
pub fn check_fixture_json(contents: &str) -> Result<Vec<Violation>, String> {
    let value: Value = serde_json::from_str(contents)
        .map_err(|error| format!("failed to parse fixture JSON: {error}"))?;
    let graph = graph_from_fixture(&value)?;
    Ok(validate_graph(&graph))
}

/// Run `cargo metadata` for a real workspace and validate its architecture.
///
/// # Errors
///
/// Returns an error when Cargo cannot produce metadata or the metadata shape is invalid.
pub fn check_workspace(path: &Path) -> Result<Vec<Violation>, String> {
    let output = Command::new("cargo")
        .arg("metadata")
        .arg("--locked")
        .arg("--format-version")
        .arg("1")
        .arg("--no-deps")
        .current_dir(path)
        .output()
        .map_err(|error| format!("failed to run cargo metadata: {error}"))?;

    if !output.status.success() {
        return Err(format!(
            "cargo metadata failed with status {}: {}",
            output.status,
            String::from_utf8_lossy(&output.stderr).trim()
        ));
    }

    let value: Value = serde_json::from_slice(&output.stdout)
        .map_err(|error| format!("failed to parse cargo metadata JSON: {error}"))?;
    let graph = graph_from_cargo_metadata(&value)?;
    Ok(validate_graph(&graph))
}

/// Validate one parsed graph and return every deterministic policy violation.
#[must_use]
pub fn validate_graph(graph: &WorkspaceGraph) -> Vec<Violation> {
    let root = normalize_path(&graph.root);
    let mut violations = Vec::new();
    let mut packages_by_name = BTreeMap::new();

    for package in &graph.packages {
        if !package.name.starts_with(PACKAGE_PREFIX) {
            violations.push(Violation::new(
                "E001_PACKAGE_NAME",
                format!(
                    "workspace package '{}' must use the '{}' prefix",
                    package.name, PACKAGE_PREFIX
                ),
            ));
        }

        if !is_known_category(&package.category) {
            violations.push(Violation::new(
                "E002_UNKNOWN_CATEGORY",
                format!(
                    "package '{}' declares unknown category '{}'",
                    package.name, package.category
                ),
            ));
        }

        if !is_within(&package.manifest_path, &root) {
            violations.push(Violation::new(
                "E003_OUTSIDE_WORKSPACE",
                format!(
                    "package '{}' manifest '{}' is outside workspace '{}'",
                    package.name, package.manifest_path, graph.root
                ),
            ));
        }

        if packages_by_name
            .insert(package.name.clone(), package)
            .is_some()
        {
            violations.push(Violation::new(
                "E009_DUPLICATE_PACKAGE",
                format!(
                    "workspace contains duplicate package name '{}'",
                    package.name
                ),
            ));
        }
    }

    let mut workspace_edges = BTreeMap::<String, Vec<String>>::new();

    for package in &graph.packages {
        let mut targets = Vec::new();
        for dependency in &package.dependencies {
            if let Some(source) = &dependency.source
                && source != ALLOWED_REGISTRY
                && source != ALLOWED_SPARSE_REGISTRY
            {
                violations.push(Violation::new(
                    "E004_UNAPPROVED_SOURCE",
                    format!(
                        "package '{}' dependency '{}' uses unapproved source '{}'",
                        package.name, dependency.name, source
                    ),
                ));
            }

            if let Some(path) = &dependency.path
                && !is_within(path, &root)
            {
                violations.push(Violation::new(
                    "E003_OUTSIDE_WORKSPACE",
                    format!(
                        "package '{}' dependency '{}' points outside the Rust workspace: '{}'",
                        package.name, dependency.name, path
                    ),
                ));
            }

            if let Some(target) = packages_by_name.get(&dependency.name) {
                targets.push(target.name.clone());
                if is_known_category(&package.category)
                    && is_known_category(&target.category)
                    && !dependency_allowed(&package.category, &target.category, dependency.kind)
                {
                    violations.push(Violation::new(
                        "E005_FORBIDDEN_EDGE",
                        format!(
                            "forbidden {} dependency edge {} ({}) -> {} ({})",
                            dependency.kind,
                            package.name,
                            package.category,
                            target.name,
                            target.category
                        ),
                    ));
                }
            } else if dependency.path.is_some() && dependency.source.is_none() {
                violations.push(Violation::new(
                    "E008_UNKNOWN_WORKSPACE_DEP",
                    format!(
                        "package '{}' has unresolved workspace path dependency '{}'",
                        package.name, dependency.name
                    ),
                ));
            }
        }
        workspace_edges.insert(package.name.clone(), targets);
    }

    if let Some(cycle) = find_cycle(&workspace_edges) {
        violations.push(Violation::new(
            "E006_DEPENDENCY_CYCLE",
            format!(
                "workspace dependency cycle detected: {}",
                cycle.join(" -> ")
            ),
        ));
    }

    violations.sort_by(|left, right| {
        left.code
            .cmp(right.code)
            .then_with(|| left.message.cmp(&right.message))
    });
    violations
}

fn graph_from_fixture(value: &Value) -> Result<WorkspaceGraph, String> {
    let object = value
        .as_object()
        .ok_or_else(|| "fixture root must be a JSON object".to_owned())?;
    let schema_version = required_u64(object.get("schema_version"), "schema_version")?;
    if !matches!(
        schema_version,
        LEGACY_FIXTURE_SCHEMA_VERSION | FIXTURE_SCHEMA_VERSION
    ) {
        return Err(format!(
            "unsupported fixture schema_version {schema_version}; supported versions are {LEGACY_FIXTURE_SCHEMA_VERSION} and {FIXTURE_SCHEMA_VERSION}"
        ));
    }

    let root = required_string(object.get("workspace_root"), "workspace_root")?;
    let package_values = object
        .get("packages")
        .and_then(Value::as_array)
        .ok_or_else(|| "fixture packages must be an array".to_owned())?;
    let mut packages = Vec::with_capacity(package_values.len());

    for package_value in package_values {
        let package_object = package_value
            .as_object()
            .ok_or_else(|| "each fixture package must be an object".to_owned())?;
        let dependency_values = package_object
            .get("dependencies")
            .and_then(Value::as_array)
            .ok_or_else(|| "fixture package dependencies must be an array".to_owned())?;
        let mut dependencies = Vec::with_capacity(dependency_values.len());

        for dependency_value in dependency_values {
            let dependency_object = dependency_value
                .as_object()
                .ok_or_else(|| "each fixture dependency must be an object".to_owned())?;
            let kind = if schema_version == LEGACY_FIXTURE_SCHEMA_VERSION {
                optional_dependency_kind(dependency_object.get("kind"), "dependency.kind")?
            } else {
                required_dependency_kind(dependency_object.get("kind"), "dependency.kind")?
            };
            dependencies.push(Dependency {
                name: required_string(dependency_object.get("name"), "dependency.name")?,
                path: optional_string(dependency_object.get("path"), "dependency.path")?,
                source: optional_string(dependency_object.get("source"), "dependency.source")?,
                kind,
            });
        }

        packages.push(Package {
            name: required_string(package_object.get("name"), "package.name")?,
            category: required_string(package_object.get("category"), "package.category")?,
            manifest_path: required_string(
                package_object.get("manifest_path"),
                "package.manifest_path",
            )?,
            dependencies,
        });
    }

    Ok(WorkspaceGraph { root, packages })
}

fn graph_from_cargo_metadata(value: &Value) -> Result<WorkspaceGraph, String> {
    let object = value
        .as_object()
        .ok_or_else(|| "cargo metadata root must be an object".to_owned())?;
    let root = required_string(object.get("workspace_root"), "workspace_root")?;
    let workspace_members = object
        .get("workspace_members")
        .and_then(Value::as_array)
        .ok_or_else(|| "cargo metadata workspace_members must be an array".to_owned())?
        .iter()
        .map(|member| {
            member
                .as_str()
                .map(str::to_owned)
                .ok_or_else(|| "workspace member id must be a string".to_owned())
        })
        .collect::<Result<BTreeSet<_>, _>>()?;

    let package_values = object
        .get("packages")
        .and_then(Value::as_array)
        .ok_or_else(|| "cargo metadata packages must be an array".to_owned())?;
    let mut packages = Vec::new();

    for package_value in package_values {
        let package_object = package_value
            .as_object()
            .ok_or_else(|| "cargo metadata package must be an object".to_owned())?;
        let id = required_string(package_object.get("id"), "package.id")?;
        if !workspace_members.contains(&id) {
            continue;
        }

        let metadata = package_object
            .get("metadata")
            .and_then(Value::as_object)
            .ok_or_else(|| format!("workspace package '{id}' metadata must be an object"))?;
        let oteryn = metadata
            .get("oteryn")
            .and_then(Value::as_object)
            .ok_or_else(|| format!("workspace package '{id}' is missing metadata.oteryn"))?;
        let category = required_string(oteryn.get("category"), "metadata.oteryn.category")?;
        let dependency_values = package_object
            .get("dependencies")
            .and_then(Value::as_array)
            .ok_or_else(|| format!("workspace package '{id}' dependencies must be an array"))?;
        let mut dependencies = Vec::with_capacity(dependency_values.len());

        for dependency_value in dependency_values {
            let dependency_object = dependency_value
                .as_object()
                .ok_or_else(|| "cargo metadata dependency must be an object".to_owned())?;
            dependencies.push(Dependency {
                name: required_string(dependency_object.get("name"), "dependency.name")?,
                path: optional_string(dependency_object.get("path"), "dependency.path")?,
                source: optional_string(dependency_object.get("source"), "dependency.source")?,
                kind: optional_dependency_kind(dependency_object.get("kind"), "dependency.kind")?,
            });
        }

        packages.push(Package {
            name: required_string(package_object.get("name"), "package.name")?,
            category,
            manifest_path: required_string(
                package_object.get("manifest_path"),
                "package.manifest_path",
            )?,
            dependencies,
        });
    }

    Ok(WorkspaceGraph { root, packages })
}

fn required_string(value: Option<&Value>, field: &str) -> Result<String, String> {
    value
        .and_then(Value::as_str)
        .map(str::to_owned)
        .ok_or_else(|| format!("{field} must be a string"))
}

fn optional_string(value: Option<&Value>, field: &str) -> Result<Option<String>, String> {
    match value {
        None | Some(Value::Null) => Ok(None),
        Some(Value::String(text)) => Ok(Some(text.clone())),
        Some(_) => Err(format!("{field} must be a string or null")),
    }
}

fn required_u64(value: Option<&Value>, field: &str) -> Result<u64, String> {
    value
        .and_then(Value::as_u64)
        .ok_or_else(|| format!("{field} must be an unsigned integer"))
}

fn required_dependency_kind(value: Option<&Value>, field: &str) -> Result<DependencyKind, String> {
    let text = value
        .and_then(Value::as_str)
        .ok_or_else(|| format!("{field} must be one of normal, build or dev"))?;
    parse_dependency_kind(text, field)
}

fn optional_dependency_kind(value: Option<&Value>, field: &str) -> Result<DependencyKind, String> {
    match value {
        None | Some(Value::Null) => Ok(DependencyKind::Normal),
        Some(Value::String(text)) => parse_dependency_kind(text, field),
        Some(_) => Err(format!(
            "{field} must be null or one of normal, build or dev"
        )),
    }
}

fn parse_dependency_kind(text: &str, field: &str) -> Result<DependencyKind, String> {
    match text {
        "normal" => Ok(DependencyKind::Normal),
        "build" => Ok(DependencyKind::Build),
        "dev" => Ok(DependencyKind::Dev),
        _ => Err(format!(
            "{field} value '{text}' must be one of normal, build or dev"
        )),
    }
}

fn normalize_path(path: &str) -> String {
    let mut normalized = path.replace('\\', "/");
    while normalized.ends_with('/') && normalized.len() > 1 {
        normalized.pop();
    }
    if cfg!(windows) {
        normalized.make_ascii_lowercase();
    }
    normalized
}

fn is_within(path: &str, normalized_root: &str) -> bool {
    let normalized_path = normalize_path(path);
    normalized_path == normalized_root
        || normalized_path
            .strip_prefix(normalized_root)
            .is_some_and(|suffix| suffix.starts_with('/'))
}

fn find_cycle(edges: &BTreeMap<String, Vec<String>>) -> Option<Vec<String>> {
    let mut permanent = BTreeSet::new();
    let mut stack = Vec::new();

    for node in edges.keys() {
        if let Some(cycle) = visit_cycle(node, edges, &mut permanent, &mut stack) {
            return Some(cycle);
        }
    }
    None
}

fn visit_cycle(
    node: &str,
    edges: &BTreeMap<String, Vec<String>>,
    permanent: &mut BTreeSet<String>,
    stack: &mut Vec<String>,
) -> Option<Vec<String>> {
    if permanent.contains(node) {
        return None;
    }
    if let Some(position) = stack.iter().position(|entry| entry == node) {
        let mut cycle = stack[position..].to_vec();
        cycle.push(node.to_owned());
        return Some(cycle);
    }

    stack.push(node.to_owned());
    if let Some(targets) = edges.get(node) {
        for target in targets {
            if let Some(cycle) = visit_cycle(target, edges, permanent, stack) {
                return Some(cycle);
            }
        }
    }
    stack.pop();
    permanent.insert(node.to_owned());
    None
}
