//! Structured, bounded and secret-safe diagnostic contracts.
//!
//! This crate defines values that future sinks may consume. It does not install
//! a logger or subscriber, start background work, write files, send telemetry,
//! create crash reports or participate in application correctness.
//!
//! Callers must classify every textual value before constructing a field:
//!
//! - reviewed non-sensitive literals use [`SafeText::trusted_static`];
//! - secret or private runtime text uses [`DiagnosticValue::redacted`];
//! - bounded technical numbers, durations, monotonic time and generations use
//!   their dedicated variants.
//!
//! Arbitrary runtime text has no implicit safe conversion:
//!
//! ```compile_fail
//! use oteryn_diagnostics::DiagnosticValue;
//!
//! let untrusted = String::from("external input");
//! let value: DiagnosticValue = untrusted.into();
//! ```

use oteryn_foundation::{
    Moment, ProcessGeneration, SessionGeneration, TaskGeneration,
};
use std::fmt::{self, Debug, Display, Formatter};
use std::time::Duration;

/// Maximum UTF-8 byte length accepted for reviewed safe diagnostic text.
pub const MAX_SAFE_TEXT_BYTES: usize = 160;
/// Maximum UTF-8 byte length accepted for a structured field key.
pub const MAX_FIELD_KEY_BYTES: usize = 32;
/// Maximum number of fields held by one diagnostic event.
pub const MAX_EVENT_FIELDS: usize = 16;

/// Stable diagnostic severity independent of any future sink implementation.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Severity {
    /// Detailed information intended for focused developer diagnosis.
    Debug,
    /// Normal lifecycle or operational information.
    Info,
    /// Recoverable degradation or unexpected state.
    Warning,
    /// Failed operation requiring attention.
    Error,
    /// Safety or integrity failure requiring immediate containment.
    Critical,
}

impl Display for Severity {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str(match self {
            Self::Debug => "debug",
            Self::Info => "info",
            Self::Warning => "warning",
            Self::Error => "error",
            Self::Critical => "critical",
        })
    }
}

/// Broad stable category used for filtering without encoding product behavior.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum DiagnosticCategory {
    /// Process, session, task or component lifetime activity.
    Lifecycle,
    /// Trust-boundary, redaction or security-policy activity.
    Security,
    /// Rejection of malformed or unsupported input.
    Validation,
    /// Bounded resource pressure or availability.
    Resource,
    /// Measured technical timing or capacity information.
    Performance,
    /// Internal invariant or implementation activity.
    Internal,
}

impl Display for DiagnosticCategory {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str(match self {
            Self::Lifecycle => "lifecycle",
            Self::Security => "security",
            Self::Validation => "validation",
            Self::Resource => "resource",
            Self::Performance => "performance",
            Self::Internal => "internal",
        })
    }
}

/// Stable numeric diagnostic code allocated by the owning component.
///
/// Numeric codes cannot contain external text or secrets. Allocation policy is
/// intentionally left to later owning workstreams and catalogues.
#[derive(Debug, Default, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct DiagnosticCode(u32);

impl DiagnosticCode {
    /// Construct a code from an explicit stable numeric value.
    #[must_use]
    pub const fn new(value: u32) -> Self {
        Self(value)
    }

    /// Return the numeric code.
    #[must_use]
    pub const fn get(self) -> u32 {
        self.0
    }
}

impl Display for DiagnosticCode {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        write!(formatter, "D{:08}", self.0)
    }
}

/// Failure while validating reviewed safe text.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SafeTextError {
    /// Empty diagnostic text is not useful.
    Empty,
    /// Text exceeds the fixed byte limit.
    TooLong {
        /// Maximum accepted UTF-8 byte length.
        max_bytes: usize,
    },
    /// Text contains an ASCII control character.
    ControlCharacter,
}

impl Display for SafeTextError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::Empty => formatter.write_str("safe diagnostic text cannot be empty"),
            Self::TooLong { max_bytes } => {
                write!(formatter, "safe diagnostic text exceeds {max_bytes} bytes")
            }
            Self::ControlCharacter => {
                formatter.write_str("safe diagnostic text contains a control character")
            }
        }
    }
}

impl std::error::Error for SafeTextError {}

/// Reviewed static diagnostic text that is explicitly classified non-sensitive.
///
/// This type accepts only a `'static` literal or another `'static` string. It
/// deliberately provides no `From<String>` or `From<&str>` implementation.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct SafeText(&'static str);

impl SafeText {
    /// Validate reviewed static non-sensitive text.
    ///
    /// # Errors
    ///
    /// Returns a closed [`SafeTextError`] for empty, oversized or control-bearing
    /// input. The rejected text is never copied into the error.
    pub fn trusted_static(value: &'static str) -> Result<Self, SafeTextError> {
        if value.is_empty() {
            return Err(SafeTextError::Empty);
        }
        if value.len() > MAX_SAFE_TEXT_BYTES {
            return Err(SafeTextError::TooLong {
                max_bytes: MAX_SAFE_TEXT_BYTES,
            });
        }
        if value.bytes().any(|byte| byte.is_ascii_control()) {
            return Err(SafeTextError::ControlCharacter);
        }
        Ok(Self(value))
    }

    /// Return the reviewed static text.
    #[must_use]
    pub const fn as_str(self) -> &'static str {
        self.0
    }
}

impl Display for SafeText {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str(self.0)
    }
}

/// Failure while validating a structured field key.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FieldKeyError {
    /// A field key must contain at least one character.
    Empty,
    /// The field key exceeds the fixed byte limit.
    TooLong {
        /// Maximum accepted byte length.
        max_bytes: usize,
    },
    /// The field key is not lower snake case ASCII.
    InvalidSyntax,
}

impl Display for FieldKeyError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::Empty => formatter.write_str("diagnostic field key cannot be empty"),
            Self::TooLong { max_bytes } => {
                write!(formatter, "diagnostic field key exceeds {max_bytes} bytes")
            }
            Self::InvalidSyntax => {
                formatter.write_str("diagnostic field key must use lower snake case ASCII")
            }
        }
    }
}

impl std::error::Error for FieldKeyError {}

/// Reviewed static lower-snake-case field key.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct FieldKey(&'static str);

impl FieldKey {
    /// Validate a reviewed static field key.
    ///
    /// # Errors
    ///
    /// Returns a closed [`FieldKeyError`] without retaining rejected text.
    pub fn trusted_static(value: &'static str) -> Result<Self, FieldKeyError> {
        if value.is_empty() {
            return Err(FieldKeyError::Empty);
        }
        if value.len() > MAX_FIELD_KEY_BYTES {
            return Err(FieldKeyError::TooLong {
                max_bytes: MAX_FIELD_KEY_BYTES,
            });
        }

        let mut bytes = value.bytes();
        let valid_first = bytes.next().is_some_and(|byte| byte.is_ascii_lowercase());
        let valid_rest = bytes.all(|byte| {
            byte.is_ascii_lowercase() || byte.is_ascii_digit() || byte == b'_'
        });
        if !valid_first || !valid_rest {
            return Err(FieldKeyError::InvalidSyntax);
        }

        Ok(Self(value))
    }

    /// Return the reviewed field key.
    #[must_use]
    pub const fn as_str(self) -> &'static str {
        self.0
    }
}

impl Display for FieldKey {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str(self.0)
    }
}

/// Explicit classification for sensitive or private runtime text.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum SensitiveKind {
    /// OAuth or equivalent access credential.
    AccessToken,
    /// OAuth or equivalent refresh credential.
    RefreshToken,
    /// Authorization transaction code.
    AuthorizationCode,
    /// PKCE verifier.
    PkceVerifier,
    /// One-shot game-entry ticket.
    GameTicket,
    /// Active session secret or resume credential.
    SessionSecret,
    /// HTTP or application cookie.
    Cookie,
    /// Private chat or private user-authored content.
    PrivateChat,
    /// Personal or user-specific filesystem path.
    PersonalPath,
    /// Other explicitly confidential text.
    Confidential,
}

impl Display for SensitiveKind {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str(match self {
            Self::AccessToken => "access-token",
            Self::RefreshToken => "refresh-token",
            Self::AuthorizationCode => "authorization-code",
            Self::PkceVerifier => "pkce-verifier",
            Self::GameTicket => "game-ticket",
            Self::SessionSecret => "session-secret",
            Self::Cookie => "cookie",
            Self::PrivateChat => "private-chat",
            Self::PersonalPath => "personal-path",
            Self::Confidential => "confidential",
        })
    }
}

/// Irreversibly redacted sensitive diagnostic value.
///
/// The constructor accepts sensitive text only to make classification explicit;
/// the value is neither copied nor retained. Formatting exposes only the
/// classification.
#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct SensitiveValue {
    kind: SensitiveKind,
}

impl SensitiveValue {
    /// Classify sensitive text and discard it at the diagnostic boundary.
    #[must_use]
    pub const fn redacted(kind: SensitiveKind, _value: &str) -> Self {
        Self { kind }
    }

    /// Return the non-secret classification.
    #[must_use]
    pub const fn kind(self) -> SensitiveKind {
        self.kind
    }
}

impl Debug for SensitiveValue {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        write!(formatter, "SensitiveValue(<redacted:{}>)", self.kind)
    }
}

impl Display for SensitiveValue {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        write!(formatter, "<redacted:{}>", self.kind)
    }
}

/// Bounded diagnostic value with no arbitrary owned text variant.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DiagnosticValue {
    /// Reviewed static non-sensitive text.
    SafeText(SafeText),
    /// Unsigned technical value.
    Unsigned(u64),
    /// Signed technical value.
    Signed(i64),
    /// Boolean technical value.
    Boolean(bool),
    /// Bounded standard duration.
    Duration(Duration),
    /// Monotonic time from the owning clock origin.
    Moment(Moment),
    /// Process lifetime generation.
    ProcessGeneration(ProcessGeneration),
    /// Replaceable session generation.
    SessionGeneration(SessionGeneration),
    /// Replaceable task generation.
    TaskGeneration(TaskGeneration),
    /// Sensitive input discarded at construction.
    Redacted(SensitiveValue),
}

impl DiagnosticValue {
    /// Classify sensitive runtime text and immediately replace it with a marker.
    #[must_use]
    pub const fn redacted(kind: SensitiveKind, value: &str) -> Self {
        Self::Redacted(SensitiveValue::redacted(kind, value))
    }
}

impl From<SafeText> for DiagnosticValue {
    fn from(value: SafeText) -> Self {
        Self::SafeText(value)
    }
}

impl From<u64> for DiagnosticValue {
    fn from(value: u64) -> Self {
        Self::Unsigned(value)
    }
}

impl From<i64> for DiagnosticValue {
    fn from(value: i64) -> Self {
        Self::Signed(value)
    }
}

impl From<bool> for DiagnosticValue {
    fn from(value: bool) -> Self {
        Self::Boolean(value)
    }
}

impl From<Duration> for DiagnosticValue {
    fn from(value: Duration) -> Self {
        Self::Duration(value)
    }
}

impl From<Moment> for DiagnosticValue {
    fn from(value: Moment) -> Self {
        Self::Moment(value)
    }
}

impl From<ProcessGeneration> for DiagnosticValue {
    fn from(value: ProcessGeneration) -> Self {
        Self::ProcessGeneration(value)
    }
}

impl From<SessionGeneration> for DiagnosticValue {
    fn from(value: SessionGeneration) -> Self {
        Self::SessionGeneration(value)
    }
}

impl From<TaskGeneration> for DiagnosticValue {
    fn from(value: TaskGeneration) -> Self {
        Self::TaskGeneration(value)
    }
}

impl Display for DiagnosticValue {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::SafeText(value) => Display::fmt(value, formatter),
            Self::Unsigned(value) => Display::fmt(value, formatter),
            Self::Signed(value) => Display::fmt(value, formatter),
            Self::Boolean(value) => Display::fmt(value, formatter),
            Self::Duration(value) => write_duration(formatter, *value),
            Self::Moment(value) => Display::fmt(value, formatter),
            Self::ProcessGeneration(value) => Display::fmt(value, formatter),
            Self::SessionGeneration(value) => Display::fmt(value, formatter),
            Self::TaskGeneration(value) => Display::fmt(value, formatter),
            Self::Redacted(value) => Display::fmt(value, formatter),
        }
    }
}

/// Non-secret technical correlation identifier local to diagnostics ownership.
#[derive(Debug, Default, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct CorrelationId(u64);

impl CorrelationId {
    /// Construct an identifier from an explicit technical value.
    #[must_use]
    pub const fn new(value: u64) -> Self {
        Self(value)
    }

    /// Return the stored value.
    #[must_use]
    pub const fn get(self) -> u64 {
        self.0
    }
}

impl Display for CorrelationId {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        write!(formatter, "C{:016x}", self.0)
    }
}

/// Safe technical context attached to a diagnostic event.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TechnicalContext {
    occurred_at: Moment,
    process_generation: ProcessGeneration,
    session_generation: Option<SessionGeneration>,
    task_generation: Option<TaskGeneration>,
    correlation_id: Option<CorrelationId>,
}

impl TechnicalContext {
    /// Construct required process-scoped context.
    #[must_use]
    pub const fn new(occurred_at: Moment, process_generation: ProcessGeneration) -> Self {
        Self {
            occurred_at,
            process_generation,
            session_generation: None,
            task_generation: None,
            correlation_id: None,
        }
    }

    /// Attach a replaceable session generation.
    #[must_use]
    pub const fn with_session(mut self, generation: SessionGeneration) -> Self {
        self.session_generation = Some(generation);
        self
    }

    /// Attach a replaceable task generation.
    #[must_use]
    pub const fn with_task(mut self, generation: TaskGeneration) -> Self {
        self.task_generation = Some(generation);
        self
    }

    /// Attach a non-secret diagnostics correlation identifier.
    #[must_use]
    pub const fn with_correlation(mut self, correlation_id: CorrelationId) -> Self {
        self.correlation_id = Some(correlation_id);
        self
    }

    /// Return the monotonic event moment.
    #[must_use]
    pub const fn occurred_at(self) -> Moment {
        self.occurred_at
    }

    /// Return the process generation.
    #[must_use]
    pub const fn process_generation(self) -> ProcessGeneration {
        self.process_generation
    }

    /// Return the optional session generation.
    #[must_use]
    pub const fn session_generation(self) -> Option<SessionGeneration> {
        self.session_generation
    }

    /// Return the optional task generation.
    #[must_use]
    pub const fn task_generation(self) -> Option<TaskGeneration> {
        self.task_generation
    }

    /// Return the optional correlation identifier.
    #[must_use]
    pub const fn correlation_id(self) -> Option<CorrelationId> {
        self.correlation_id
    }
}

impl Display for TechnicalContext {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        write!(
            formatter,
            "t={} process={}",
            self.occurred_at, self.process_generation
        )?;
        if let Some(generation) = self.session_generation {
            write!(formatter, " session={generation}")?;
        }
        if let Some(generation) = self.task_generation {
            write!(formatter, " task={generation}")?;
        }
        if let Some(correlation_id) = self.correlation_id {
            write!(formatter, " correlation={correlation_id}")?;
        }
        Ok(())
    }
}

/// One structured key/value field.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct DiagnosticField {
    key: FieldKey,
    value: DiagnosticValue,
}

impl DiagnosticField {
    /// Construct a field from an already classified key and value.
    #[must_use]
    pub const fn new(key: FieldKey, value: DiagnosticValue) -> Self {
        Self { key, value }
    }

    /// Return the field key.
    #[must_use]
    pub const fn key(self) -> FieldKey {
        self.key
    }

    /// Return the classified field value.
    #[must_use]
    pub const fn value(self) -> DiagnosticValue {
        self.value
    }
}

impl Display for DiagnosticField {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        write!(formatter, "{}={}", self.key, self.value)
    }
}

/// Failure while constructing a bounded event.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DiagnosticBuildError {
    /// The event already contains the maximum field count.
    TooManyFields {
        /// Maximum accepted field count.
        max_fields: usize,
    },
    /// The event already contains the same structured key.
    DuplicateField,
}

impl Display for DiagnosticBuildError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::TooManyFields { max_fields } => {
                write!(formatter, "diagnostic event exceeds {max_fields} fields")
            }
            Self::DuplicateField => {
                formatter.write_str("diagnostic event contains a duplicate field key")
            }
        }
    }
}

impl std::error::Error for DiagnosticBuildError {}

/// One bounded structured diagnostic event.
///
/// Field order is insertion order and therefore deterministic. The event owns
/// no arbitrary runtime string and cannot contain more than
/// [`MAX_EVENT_FIELDS`] fields.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DiagnosticEvent {
    severity: Severity,
    category: DiagnosticCategory,
    code: DiagnosticCode,
    message: SafeText,
    context: TechnicalContext,
    fields: Vec<DiagnosticField>,
}

impl DiagnosticEvent {
    /// Construct an event without optional fields.
    #[must_use]
    pub fn new(
        severity: Severity,
        category: DiagnosticCategory,
        code: DiagnosticCode,
        message: SafeText,
        context: TechnicalContext,
    ) -> Self {
        Self {
            severity,
            category,
            code,
            message,
            context,
            fields: Vec::new(),
        }
    }

    /// Add one classified field while enforcing the fixed bound and unique key.
    ///
    /// # Errors
    ///
    /// Returns [`DiagnosticBuildError::TooManyFields`] at the fixed limit or
    /// [`DiagnosticBuildError::DuplicateField`] for a repeated key.
    pub fn try_add_field(
        &mut self,
        field: DiagnosticField,
    ) -> Result<(), DiagnosticBuildError> {
        if self.fields.len() >= MAX_EVENT_FIELDS {
            return Err(DiagnosticBuildError::TooManyFields {
                max_fields: MAX_EVENT_FIELDS,
            });
        }
        if self.fields.iter().any(|existing| existing.key == field.key) {
            return Err(DiagnosticBuildError::DuplicateField);
        }
        self.fields.push(field);
        Ok(())
    }

    /// Return the severity.
    #[must_use]
    pub const fn severity(&self) -> Severity {
        self.severity
    }

    /// Return the category.
    #[must_use]
    pub const fn category(&self) -> DiagnosticCategory {
        self.category
    }

    /// Return the stable code.
    #[must_use]
    pub const fn code(&self) -> DiagnosticCode {
        self.code
    }

    /// Return the reviewed message.
    #[must_use]
    pub const fn message(&self) -> SafeText {
        self.message
    }

    /// Return the technical context.
    #[must_use]
    pub const fn context(&self) -> TechnicalContext {
        self.context
    }

    /// Return fields in deterministic insertion order.
    #[must_use]
    pub fn fields(&self) -> &[DiagnosticField] {
        &self.fields
    }

    /// Return the current bounded field count.
    #[must_use]
    pub fn field_count(&self) -> usize {
        self.fields.len()
    }
}

impl Display for DiagnosticEvent {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        write!(
            formatter,
            "{} {}/{} [{}] {}",
            self.severity, self.category, self.code, self.context, self.message
        )?;
        for field in &self.fields {
            write!(formatter, " {field}")?;
        }
        Ok(())
    }
}

fn write_duration(formatter: &mut Formatter<'_>, duration: Duration) -> fmt::Result {
    write!(
        formatter,
        "{}.{:09}s",
        duration.as_secs(),
        duration.subsec_nanos()
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    const FIELD_KEYS: [&str; MAX_EVENT_FIELDS] = [
        "field_00",
        "field_01",
        "field_02",
        "field_03",
        "field_04",
        "field_05",
        "field_06",
        "field_07",
        "field_08",
        "field_09",
        "field_10",
        "field_11",
        "field_12",
        "field_13",
        "field_14",
        "field_15",
    ];

    fn basic_event() -> Result<DiagnosticEvent, Box<dyn std::error::Error>> {
        let message = SafeText::trusted_static("operation rejected")?;
        let context = TechnicalContext::new(
            Moment::from_elapsed(Duration::from_secs(2)),
            ProcessGeneration::new(3),
        )
        .with_session(SessionGeneration::new(5))
        .with_task(TaskGeneration::new(8))
        .with_correlation(CorrelationId::new(13));

        Ok(DiagnosticEvent::new(
            Severity::Warning,
            DiagnosticCategory::Validation,
            DiagnosticCode::new(21),
            message,
            context,
        ))
    }

    #[test]
    fn reviewed_safe_text_is_bounded_and_rejects_controls() {
        assert_eq!(SafeText::trusted_static(""), Err(SafeTextError::Empty));
        assert_eq!(
            SafeText::trusted_static("line\nbreak"),
            Err(SafeTextError::ControlCharacter)
        );
        assert_eq!(
            SafeText::trusted_static(
                "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            ),
            Err(SafeTextError::TooLong {
                max_bytes: MAX_SAFE_TEXT_BYTES,
            })
        );
        assert_eq!(
            SafeText::trusted_static("bounded reviewed text").map(SafeText::as_str),
            Ok("bounded reviewed text")
        );
    }

    #[test]
    fn field_keys_are_static_lower_snake_case() {
        assert_eq!(FieldKey::trusted_static(""), Err(FieldKeyError::Empty));
        assert_eq!(
            FieldKey::trusted_static("Bad-Key"),
            Err(FieldKeyError::InvalidSyntax)
        );
        assert_eq!(
            FieldKey::trusted_static("field_key_2").map(FieldKey::as_str),
            Ok("field_key_2")
        );
    }

    #[test]
    fn every_sensitive_class_is_redacted_in_debug_and_display() {
        let markers = [
            (SensitiveKind::AccessToken, "synthetic_access_token_marker"),
            (SensitiveKind::RefreshToken, "synthetic_refresh_token_marker"),
            (
                SensitiveKind::AuthorizationCode,
                "synthetic_authorization_code_marker",
            ),
            (SensitiveKind::PkceVerifier, "synthetic_pkce_verifier_marker"),
            (SensitiveKind::GameTicket, "synthetic_game_ticket_marker"),
            (
                SensitiveKind::SessionSecret,
                "synthetic_session_secret_marker",
            ),
            (SensitiveKind::Cookie, "synthetic_cookie_marker"),
            (SensitiveKind::PrivateChat, "synthetic_private_chat_marker"),
            (SensitiveKind::PersonalPath, "synthetic_personal_path_marker"),
            (SensitiveKind::Confidential, "synthetic_confidential_marker"),
        ];

        for (kind, marker) in markers {
            let value = DiagnosticValue::redacted(kind, marker);
            let display = value.to_string();
            let debug = format!("{value:?}");

            assert!(!display.contains(marker));
            assert!(!debug.contains(marker));
            assert!(display.contains("<redacted:"));
            assert!(debug.contains("<redacted:"));
        }
    }

    #[test]
    fn event_formatting_never_reveals_sensitive_markers(
    ) -> Result<(), Box<dyn std::error::Error>> {
        let marker = "synthetic_game_ticket_marker_for_event";
        let mut event = basic_event()?;
        event.try_add_field(DiagnosticField::new(
            FieldKey::trusted_static("ticket")?,
            DiagnosticValue::redacted(SensitiveKind::GameTicket, marker),
        ))?;

        let display = event.to_string();
        let debug = format!("{event:?}");

        assert!(!display.contains(marker));
        assert!(!debug.contains(marker));
        assert!(display.contains("ticket=<redacted:game-ticket>"));
        assert!(debug.contains("SensitiveValue(<redacted:game-ticket>)"));
        Ok(())
    }

    #[test]
    fn event_fields_are_unique_and_bounded(
    ) -> Result<(), Box<dyn std::error::Error>> {
        let mut event = basic_event()?;
        for (index, key) in FIELD_KEYS.into_iter().enumerate() {
            event.try_add_field(DiagnosticField::new(
                FieldKey::trusted_static(key)?,
                DiagnosticValue::Unsigned(index as u64),
            ))?;
        }

        assert_eq!(event.field_count(), MAX_EVENT_FIELDS);
        assert_eq!(
            event.try_add_field(DiagnosticField::new(
                FieldKey::trusted_static("overflow")?,
                DiagnosticValue::Boolean(true),
            )),
            Err(DiagnosticBuildError::TooManyFields {
                max_fields: MAX_EVENT_FIELDS,
            })
        );

        let mut duplicate_event = basic_event()?;
        let duplicate_key = FieldKey::trusted_static("attempt")?;
        duplicate_event.try_add_field(DiagnosticField::new(
            duplicate_key,
            DiagnosticValue::Unsigned(1),
        ))?;
        assert_eq!(
            duplicate_event.try_add_field(DiagnosticField::new(
                duplicate_key,
                DiagnosticValue::Unsigned(2),
            )),
            Err(DiagnosticBuildError::DuplicateField)
        );
        Ok(())
    }

    #[test]
    fn technical_context_and_event_format_are_deterministic(
    ) -> Result<(), Box<dyn std::error::Error>> {
        let mut event = basic_event()?;
        event.try_add_field(DiagnosticField::new(
            FieldKey::trusted_static("retry_count")?,
            DiagnosticValue::Unsigned(2),
        ))?;
        event.try_add_field(DiagnosticField::new(
            FieldKey::trusted_static("elapsed")?,
            DiagnosticValue::Duration(Duration::new(1, 25)),
        ))?;

        assert_eq!(
            event.to_string(),
            "warning validation/D00000021 [t=2.000000000s process=3 session=5 task=8 correlation=C000000000000000d] operation rejected retry_count=2 elapsed=1.000000025s"
        );
        assert_eq!(event.code().get(), 21);
        assert_eq!(event.context().correlation_id(), Some(CorrelationId::new(13)));
        assert_eq!(event.fields()[0].key().as_str(), "retry_count");
        Ok(())
    }
}
