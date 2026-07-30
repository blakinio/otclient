//! Strict bounded Oteryn Platform and Game Gateway protocol-v1 boundary.
//!
//! Raw OAuth, ticket and Gateway DTOs terminate in this crate. Successful
//! Gateway data is converted immediately into the merged W7 entry contracts.

use oteryn_account_session::AccountSessionId;
use oteryn_foundation::{Deadline, MonotonicClock};
use oteryn_game_session::GameEntryCredential;
use oteryn_world_directory::{
    AccountDirectorySnapshot, Availability, CharacterId, CharacterSummary, Compatibility,
    DirectoryRevision, WorldId, WorldRoute, WorldSummary,
};
use serde::Deserialize;
use serde::de::DeserializeOwned;
use std::error::Error;
use std::fmt::{self, Debug, Display, Formatter};
use std::net::IpAddr;
use std::time::Duration;
use time::OffsetDateTime;
use time::format_description::well_known::Rfc3339;
use url::Url;

/// Maximum accepted response body for every sensitive native-auth request.
pub const MAX_RESPONSE_BODY_BYTES: usize = 64 * 1024;
/// Maximum accepted response-header block configured on the production adapter.
pub const MAX_RESPONSE_HEADER_BYTES: usize = 16 * 1024;
/// Maximum opaque OAuth, ticket or session value accepted from a producer.
pub const MAX_SECRET_BYTES: usize = 4 * 1024;
/// Maximum configured public OAuth client identifier length.
pub const MAX_CLIENT_ID_BYTES: usize = 256;
/// Maximum accepted future lifetime of a Gateway game-session credential.
pub const MAX_GAME_SESSION_TTL: Duration = Duration::from_secs(120);

/// Exact configured native-auth endpoints.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PlatformEndpoints {
    identity_base: Url,
    gateway_base: Url,
}

impl PlatformEndpoints {
    /// Validate two explicit service base URLs.
    ///
    /// Non-loopback endpoints must use HTTPS. Base URLs may not contain
    /// credentials, query strings, fragments or a non-root path.
    pub fn new(identity_base: &str, gateway_base: &str) -> Result<Self, PlatformError> {
        Ok(Self {
            identity_base: validate_base_url(identity_base)?,
            gateway_base: validate_base_url(gateway_base)?,
        })
    }

    fn identity_url(&self, path: &str) -> Result<Url, PlatformError> {
        self.identity_base
            .join(path)
            .map_err(|_| PlatformError::new(PlatformErrorKind::InvalidConfiguration))
    }

    fn gateway_url(&self, path: &str) -> Result<Url, PlatformError> {
        self.gateway_base
            .join(path)
            .map_err(|_| PlatformError::new(PlatformErrorKind::InvalidConfiguration))
    }
}

fn validate_base_url(value: &str) -> Result<Url, PlatformError> {
    let url = Url::parse(value)
        .map_err(|_| PlatformError::new(PlatformErrorKind::InvalidConfiguration))?;
    if url.username() != ""
        || url.password().is_some()
        || url.query().is_some()
        || url.fragment().is_some()
        || url.path() != "/"
    {
        return Err(PlatformError::new(
            PlatformErrorKind::InvalidConfiguration,
        ));
    }
    let host = url
        .host_str()
        .ok_or_else(|| PlatformError::new(PlatformErrorKind::InvalidConfiguration))?;
    let is_loopback = host.eq_ignore_ascii_case("localhost")
        || host
            .parse::<IpAddr>()
            .is_ok_and(|address| address.is_loopback());
    match url.scheme() {
        "https" => Ok(url),
        "http" if is_loopback => Ok(url),
        _ => Err(PlatformError::new(
            PlatformErrorKind::InvalidConfiguration,
        )),
    }
}

/// Non-cloneable secret UTF-8 material with redacted formatting and best-effort clearing.
pub struct SecretString(Box<[u8]>);

impl SecretString {
    /// Own one non-empty bounded secret string.
    pub fn new(value: String) -> Result<Self, PlatformError> {
        let bytes = value.into_bytes();
        if bytes.is_empty() || bytes.len() > MAX_SECRET_BYTES {
            return Err(PlatformError::new(PlatformErrorKind::InvalidSecret));
        }
        Ok(Self(bytes.into_boxed_slice()))
    }

    /// Expose secret text only at the exact protocol boundary.
    pub fn expose_secret(&self) -> Result<&str, PlatformError> {
        std::str::from_utf8(&self.0)
            .map_err(|_| PlatformError::new(PlatformErrorKind::InvariantViolation))
    }
}

impl Debug for SecretString {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str("SecretString([REDACTED])")
    }
}

impl Display for SecretString {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str("[REDACTED SECRET]")
    }
}

impl Drop for SecretString {
    fn drop(&mut self) {
        self.0.fill(0);
    }
}

struct SecretBytes(Box<[u8]>);

impl SecretBytes {
    fn new(value: Vec<u8>) -> Result<Self, PlatformError> {
        if value.len() > MAX_RESPONSE_BODY_BYTES {
            return Err(PlatformError::new(PlatformErrorKind::ResponseTooLarge));
        }
        Ok(Self(value.into_boxed_slice()))
    }

    fn from_secret_string(value: String) -> Result<Self, PlatformError> {
        let bytes = value.into_bytes();
        if bytes.is_empty() || bytes.len() > MAX_RESPONSE_BODY_BYTES {
            return Err(PlatformError::new(PlatformErrorKind::InvalidSecret));
        }
        Ok(Self(bytes.into_boxed_slice()))
    }

    fn expose_secret(&self) -> &[u8] {
        &self.0
    }
}

impl Debug for SecretBytes {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str("SecretBytes([REDACTED])")
    }
}

impl Drop for SecretBytes {
    fn drop(&mut self) {
        self.0.fill(0);
    }
}

/// One sensitive HTTP POST request. Debug output never exposes body or bearer data.
pub struct HttpRequest {
    url: Url,
    content_type: &'static str,
    bearer: Option<SecretString>,
    body: SecretBytes,
}

impl HttpRequest {
    fn new(
        url: Url,
        content_type: &'static str,
        bearer: Option<SecretString>,
        body: SecretBytes,
    ) -> Self {
        Self {
            url,
            content_type,
            bearer,
            body,
        }
    }

    /// Return the non-secret destination URL.
    #[must_use]
    pub const fn url(&self) -> &Url {
        &self.url
    }

    /// Return the explicit request content type.
    #[must_use]
    pub const fn content_type(&self) -> &'static str {
        self.content_type
    }

    /// Expose the bearer only to an HTTP adapter or deterministic fake.
    pub fn bearer(&self) -> Result<Option<&str>, PlatformError> {
        self.bearer
            .as_ref()
            .map(SecretString::expose_secret)
            .transpose()
    }

    /// Expose body bytes only to an HTTP adapter or deterministic fake.
    #[must_use]
    pub fn body(&self) -> &[u8] {
        self.body.expose_secret()
    }
}

impl Debug for HttpRequest {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("HttpRequest")
            .field("url", &self.url)
            .field("content_type", &self.content_type)
            .field("bearer", &self.bearer.as_ref().map(|_| "[REDACTED]"))
            .field("body", &"[REDACTED]")
            .finish()
    }
}

/// Bounded HTTP response returned by a real adapter or fake service.
pub struct HttpResponse {
    status: u16,
    content_type: Option<String>,
    cache_control: Option<String>,
    pragma: Option<String>,
    location: Option<String>,
    body: SecretBytes,
}

impl HttpResponse {
    /// Construct one response for an adapter or fake service.
    pub fn new(
        status: u16,
        content_type: Option<String>,
        cache_control: Option<String>,
        pragma: Option<String>,
        location: Option<String>,
        body: Vec<u8>,
    ) -> Result<Self, PlatformError> {
        Ok(Self {
            status,
            content_type,
            cache_control,
            pragma,
            location,
            body: SecretBytes::new(body)?,
        })
    }
}

impl Debug for HttpResponse {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("HttpResponse")
            .field("status", &self.status)
            .field("content_type", &self.content_type)
            .field("cache_control", &self.cache_control)
            .field("pragma", &self.pragma)
            .field("location", &self.location.as_ref().map(|_| "[REDACTED]"))
            .field("body", &"[REDACTED]")
            .finish()
    }
}

/// Closed transport failure without raw backend or OS text.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum HttpTransportError {
    /// DNS, connection, TLS, send or receive failed.
    Unavailable,
    /// The body exceeded the configured bound.
    ResponseTooLarge,
    /// A request invariant was violated by the adapter.
    InvalidRequest,
}

impl Display for HttpTransportError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::Unavailable => formatter.write_str("HTTP transport unavailable"),
            Self::ResponseTooLarge => formatter.write_str("HTTP response exceeds the size limit"),
            Self::InvalidRequest => formatter.write_str("HTTP request is invalid"),
        }
    }
}

impl Error for HttpTransportError {}

/// Injectable blocking HTTP transport.
pub trait HttpTransport: Send + Sync {
    /// Send exactly one POST request without automatic retries.
    fn post(&self, request: HttpRequest) -> Result<HttpResponse, HttpTransportError>;
}

/// Production blocking HTTP adapter using rustls certificate and hostname validation.
#[derive(Clone)]
pub struct UreqTransport {
    agent: ureq::Agent,
}

impl UreqTransport {
    /// Build an adapter with one bounded global timeout, no redirects and no
    /// environment-derived proxy configuration.
    pub fn new(timeout: Duration) -> Result<Self, PlatformError> {
        if timeout.is_zero() || timeout > Duration::from_secs(30) {
            return Err(PlatformError::new(
                PlatformErrorKind::InvalidConfiguration,
            ));
        }
        let config = ureq::Agent::config_builder()
            .timeout_global(Some(timeout))
            .max_redirects(0)
            .http_status_as_error(false)
            .max_response_header_size(MAX_RESPONSE_HEADER_BYTES)
            .proxy(None)
            .build();
        Ok(Self {
            agent: config.into(),
        })
    }
}

impl HttpTransport for UreqTransport {
    fn post(&self, request: HttpRequest) -> Result<HttpResponse, HttpTransportError> {
        let mut builder = self
            .agent
            .post(request.url().as_str())
            .header("Accept", "application/json")
            .header("Content-Type", request.content_type());
        if let Some(bearer) = request
            .bearer()
            .map_err(|_| HttpTransportError::InvalidRequest)?
        {
            let authorization = format!("Bearer {bearer}");
            builder = builder.header("Authorization", &authorization);
        }
        let mut response = builder
            .send(request.body())
            .map_err(|_| HttpTransportError::Unavailable)?;
        if response
            .body()
            .content_length()
            .is_some_and(|length| length > MAX_RESPONSE_BODY_BYTES as u64)
        {
            return Err(HttpTransportError::ResponseTooLarge);
        }
        let content_type = response
            .headers()
            .get("content-type")
            .and_then(|value| value.to_str().ok())
            .map(str::to_owned);
        let cache_control = response
            .headers()
            .get("cache-control")
            .and_then(|value| value.to_str().ok())
            .map(str::to_owned);
        let pragma = response
            .headers()
            .get("pragma")
            .and_then(|value| value.to_str().ok())
            .map(str::to_owned);
        let location = response
            .headers()
            .get("location")
            .and_then(|value| value.to_str().ok())
            .map(str::to_owned);
        let status = response.status().as_u16();
        let body = response
            .body_mut()
            .with_config()
            .limit((MAX_RESPONSE_BODY_BYTES + 1) as u64)
            .read_to_vec()
            .map_err(|error| match error {
                ureq::Error::BodyExceedsLimit(_) => HttpTransportError::ResponseTooLarge,
                _ => HttpTransportError::Unavailable,
            })?;
        if body.len() > MAX_RESPONSE_BODY_BYTES {
            return Err(HttpTransportError::ResponseTooLarge);
        }
        HttpResponse::new(
            status,
            content_type,
            cache_control,
            pragma,
            location,
            body,
        )
        .map_err(|error| match error.kind() {
            PlatformErrorKind::ResponseTooLarge => HttpTransportError::ResponseTooLarge,
            _ => HttpTransportError::InvalidRequest,
        })
    }
}

/// Exact one-time authorization-code exchange input.
pub struct TokenExchange {
    /// Explicit deployment-provided public OAuth client identifier.
    pub client_id: String,
    /// Exact dynamic loopback redirect URI used during authorization.
    pub redirect_uri: Url,
    /// One callback authorization code.
    pub code: SecretString,
    /// Matching PKCE verifier.
    pub verifier: SecretString,
}

impl Debug for TokenExchange {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("TokenExchange")
            .field("client_id", &self.client_id)
            .field("redirect_uri", &self.redirect_uri)
            .field("code", &"[REDACTED]")
            .field("verifier", &"[REDACTED]")
            .finish()
    }
}

/// OAuth token family returned for immediate ticket issuance only.
pub struct OAuthTokens {
    access_token: SecretString,
    refresh_token: SecretString,
    expires_in: Duration,
}

impl OAuthTokens {
    /// Return the bounded server-declared access-token lifetime.
    #[must_use]
    pub const fn expires_in(&self) -> Duration {
        self.expires_in
    }

    /// Consume the token family, retain only the access token and clear the
    /// unused W7 refresh token immediately.
    #[must_use]
    pub fn into_access_token(self) -> SecretString {
        let Self {
            access_token,
            refresh_token,
            expires_in: _,
        } = self;
        drop(refresh_token);
        access_token
    }
}

impl Debug for OAuthTokens {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("OAuthTokens")
            .field("access_token", &"[REDACTED]")
            .field("refresh_token", &"[REDACTED]")
            .field("expires_in", &self.expires_in)
            .finish()
    }
}

/// Validated account directory plus one fresh merged ENTRY credential.
pub struct GatewayBootstrap {
    directory: AccountDirectorySnapshot,
    credential: GameEntryCredential,
}

impl GatewayBootstrap {
    /// Consume the result into its merged producer-owned parts.
    #[must_use]
    pub fn into_parts(self) -> (AccountDirectorySnapshot, GameEntryCredential) {
        (self.directory, self.credential)
    }

    /// Inspect the validated non-secret directory.
    #[must_use]
    pub const fn directory(&self) -> &AccountDirectorySnapshot {
        &self.directory
    }
}

impl Debug for GatewayBootstrap {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("GatewayBootstrap")
            .field("directory", &self.directory)
            .field("credential", &"[REDACTED]")
            .finish()
    }
}

/// Synchronous one-attempt native-auth Platform/Gateway client.
pub struct PlatformClient<T> {
    endpoints: PlatformEndpoints,
    transport: T,
}

impl<T> PlatformClient<T>
where
    T: HttpTransport,
{
    /// Construct the client from explicit validated endpoints and one adapter.
    #[must_use]
    pub const fn new(endpoints: PlatformEndpoints, transport: T) -> Self {
        Self {
            endpoints,
            transport,
        }
    }

    /// Exchange one authorization code with its exact redirect and PKCE verifier.
    pub fn exchange_authorization_code(
        &self,
        exchange: TokenExchange,
    ) -> Result<OAuthTokens, PlatformError> {
        if exchange.client_id.is_empty() || exchange.client_id.len() > MAX_CLIENT_ID_BYTES {
            return Err(PlatformError::new(
                PlatformErrorKind::InvalidConfiguration,
            ));
        }
        validate_dynamic_redirect(&exchange.redirect_uri)?;
        let code = exchange.code.expose_secret()?;
        let verifier = exchange.verifier.expose_secret()?;
        let mut serializer = url::form_urlencoded::Serializer::new(String::new());
        serializer
            .append_pair("grant_type", "authorization_code")
            .append_pair("client_id", &exchange.client_id)
            .append_pair("redirect_uri", exchange.redirect_uri.as_str())
            .append_pair("code", code)
            .append_pair("code_verifier", verifier);
        let body = SecretBytes::from_secret_string(serializer.finish())?;
        let response = self.send(HttpRequest::new(
            self.endpoints.identity_url("oauth/token")?,
            "application/x-www-form-urlencoded",
            None,
            body,
        ))?;
        validate_sensitive_success(&response)?;
        let dto: TokenResponseDto = parse_json(response.body.expose_secret())?;
        if dto.token_type != "Bearer" || dto.expires_in == 0 || dto.expires_in > 300 {
            return Err(PlatformError::new(PlatformErrorKind::InvalidResponse));
        }
        Ok(OAuthTokens {
            access_token: SecretString::new(dto.access_token)?,
            refresh_token: SecretString::new(dto.refresh_token)?,
            expires_in: Duration::from_secs(dto.expires_in),
        })
    }

    /// Issue one Game Login Ticket. This operation is never retried because the
    /// producer revokes the token family when issuance succeeds.
    pub fn issue_game_login_ticket(
        &self,
        access_token: SecretString,
    ) -> Result<SecretString, PlatformError> {
        let body = SecretBytes::new(b"{\"protocol_version\":1}".to_vec())?;
        let response = self.send(HttpRequest::new(
            self.endpoints.identity_url("api/v1/game-auth/tickets")?,
            "application/json",
            Some(access_token),
            body,
        ))?;
        validate_sensitive_success(&response)?;
        let dto: TicketResponseDto = parse_json(response.body.expose_secret())?;
        if dto.protocol_version != 1 || dto.expires_in == 0 || dto.expires_in > 60 {
            return Err(PlatformError::new(PlatformErrorKind::InvalidResponse));
        }
        SecretString::new(dto.ticket)
    }

    /// Exchange one ticket for the authoritative directory and fresh one-shot
    /// game-session credential.
    pub fn request_game_entry<C>(
        &self,
        ticket: SecretString,
        account_session_id: AccountSessionId,
        directory_revision: DirectoryRevision,
        clock: &C,
    ) -> Result<GatewayBootstrap, PlatformError>
    where
        C: MonotonicClock + ?Sized,
    {
        self.request_game_entry_at(
            ticket,
            account_session_id,
            directory_revision,
            clock,
            OffsetDateTime::now_utc(),
        )
    }

    /// Deterministic variant with an injected wall-clock instant for tests.
    pub fn request_game_entry_at<C>(
        &self,
        ticket: SecretString,
        account_session_id: AccountSessionId,
        directory_revision: DirectoryRevision,
        clock: &C,
        utc_now: OffsetDateTime,
    ) -> Result<GatewayBootstrap, PlatformError>
    where
        C: MonotonicClock + ?Sized,
    {
        let ticket_text = ticket.expose_secret()?;
        let body = serde_json::to_vec(&serde_json::json!({
            "protocol_version": 1,
            "game_login_ticket": ticket_text,
        }))
        .map_err(|_| PlatformError::new(PlatformErrorKind::InvariantViolation))?;
        let response = self.send(HttpRequest::new(
            self.endpoints.gateway_url("v1/login")?,
            "application/json",
            None,
            SecretBytes::new(body)?,
        ))?;
        validate_sensitive_success(&response)?;
        let dto: GatewayResponseDto = parse_json(response.body.expose_secret())?;
        if dto.protocol_version != 1 {
            return Err(PlatformError::new(
                PlatformErrorKind::UnsupportedProtocolVersion,
            ));
        }
        let expires_at = OffsetDateTime::parse(&dto.session.expires_at, &Rfc3339)
            .map_err(|_| PlatformError::new(PlatformErrorKind::InvalidResponse))?;
        let remaining = expires_at - utc_now;
        let remaining_seconds = remaining.whole_seconds();
        if remaining_seconds <= 0 || remaining_seconds > MAX_GAME_SESSION_TTL.as_secs() as i64 {
            return Err(PlatformError::new(PlatformErrorKind::InvalidExpiry));
        }
        let deadline = Deadline::after(clock, Duration::from_secs(remaining_seconds as u64))
            .map_err(|_| PlatformError::new(PlatformErrorKind::InvalidExpiry))?;
        let mut worlds = Vec::with_capacity(dto.worlds.len());
        for world in dto.worlds {
            let id = WorldId::new(world.id)
                .map_err(|_| PlatformError::new(PlatformErrorKind::InvalidDirectory))?;
            let port = u16::try_from(world.port)
                .ok()
                .filter(|value| *value != 0)
                .ok_or_else(|| PlatformError::new(PlatformErrorKind::InvalidDirectory))?;
            let route = WorldRoute::new(world.host, port)
                .map_err(|_| PlatformError::new(PlatformErrorKind::InvalidDirectory))?;
            worlds.push(
                WorldSummary::new(
                    id,
                    world.slug,
                    world.name,
                    world.region,
                    route,
                    Availability::Available,
                    Compatibility::Compatible,
                )
                .map_err(|_| PlatformError::new(PlatformErrorKind::InvalidDirectory))?,
            );
        }
        let mut characters = Vec::with_capacity(dto.characters.len());
        for character in dto.characters {
            let id = CharacterId::new(character.id)
                .map_err(|_| PlatformError::new(PlatformErrorKind::InvalidDirectory))?;
            let world_id = WorldId::new(character.world_id)
                .map_err(|_| PlatformError::new(PlatformErrorKind::InvalidDirectory))?;
            let level = u32::try_from(character.level)
                .ok()
                .filter(|value| *value != 0)
                .ok_or_else(|| PlatformError::new(PlatformErrorKind::InvalidDirectory))?;
            if character.vocation < 0 {
                return Err(PlatformError::new(PlatformErrorKind::InvalidDirectory));
            }
            characters.push(
                CharacterSummary::new(
                    id,
                    world_id,
                    character.name,
                    level,
                    character.vocation.to_string(),
                    Availability::Available,
                    Compatibility::Compatible,
                )
                .map_err(|_| PlatformError::new(PlatformErrorKind::InvalidDirectory))?,
            );
        }
        let directory = AccountDirectorySnapshot::new(
            account_session_id,
            directory_revision,
            worlds,
            characters,
            Vec::new(),
        )
        .map_err(|_| PlatformError::new(PlatformErrorKind::InvalidDirectory))?;
        let credential = GameEntryCredential::new(dto.session.credential.into_bytes(), deadline)
            .map_err(|_| PlatformError::new(PlatformErrorKind::InvalidSecret))?;
        Ok(GatewayBootstrap {
            directory,
            credential,
        })
    }

    fn send(&self, request: HttpRequest) -> Result<HttpResponse, PlatformError> {
        self.transport.post(request).map_err(|error| match error {
            HttpTransportError::Unavailable => {
                PlatformError::new(PlatformErrorKind::TransportUnavailable)
            }
            HttpTransportError::ResponseTooLarge => {
                PlatformError::new(PlatformErrorKind::ResponseTooLarge)
            }
            HttpTransportError::InvalidRequest => {
                PlatformError::new(PlatformErrorKind::InvariantViolation)
            }
        })
    }
}

fn validate_dynamic_redirect(url: &Url) -> Result<(), PlatformError> {
    if url.scheme() != "http"
        || url.host_str() != Some("127.0.0.1")
        || url.path() != "/callback"
        || url.port().is_none()
        || url.query().is_some()
        || url.fragment().is_some()
        || url.username() != ""
        || url.password().is_some()
    {
        return Err(PlatformError::new(
            PlatformErrorKind::InvalidConfiguration,
        ));
    }
    Ok(())
}

fn validate_sensitive_success(response: &HttpResponse) -> Result<(), PlatformError> {
    if (300..400).contains(&response.status) || response.location.is_some() {
        return Err(PlatformError::new(PlatformErrorKind::RedirectRejected));
    }
    if response.status != 200 {
        return Err(PlatformError::new(PlatformErrorKind::RequestDenied));
    }
    if !response.content_type.as_deref().is_some_and(|value| {
        value.eq_ignore_ascii_case("application/json")
            || value
                .to_ascii_lowercase()
                .starts_with("application/json;")
    }) {
        return Err(PlatformError::new(PlatformErrorKind::InvalidResponse));
    }
    if !response.cache_control.as_deref().is_some_and(|value| {
        contains_directive(value, "no-store") && contains_directive(value, "no-cache")
    }) || !response
        .pragma
        .as_deref()
        .is_some_and(|value| contains_directive(value, "no-cache"))
    {
        return Err(PlatformError::new(PlatformErrorKind::CachePolicyMissing));
    }
    Ok(())
}

fn contains_directive(value: &str, expected: &str) -> bool {
    value
        .split(',')
        .map(str::trim)
        .any(|directive| directive.eq_ignore_ascii_case(expected))
}

fn parse_json<T>(body: &[u8]) -> Result<T, PlatformError>
where
    T: DeserializeOwned,
{
    let mut deserializer = serde_json::Deserializer::from_slice(body);
    let value = T::deserialize(&mut deserializer)
        .map_err(|_| PlatformError::new(PlatformErrorKind::InvalidResponse))?;
    deserializer
        .end()
        .map_err(|_| PlatformError::new(PlatformErrorKind::TrailingResponseData))?;
    Ok(value)
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct TokenResponseDto {
    token_type: String,
    expires_in: u64,
    access_token: String,
    refresh_token: String,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct TicketResponseDto {
    protocol_version: u32,
    ticket: String,
    expires_in: u64,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct GatewayResponseDto {
    protocol_version: u32,
    session: GatewaySessionDto,
    worlds: Vec<GatewayWorldDto>,
    characters: Vec<GatewayCharacterDto>,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct GatewaySessionDto {
    credential: String,
    expires_at: String,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct GatewayWorldDto {
    id: i64,
    slug: String,
    name: String,
    region: String,
    host: String,
    port: i64,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct GatewayCharacterDto {
    id: i64,
    name: String,
    level: i64,
    vocation: i64,
    world_id: i64,
}

/// Stable non-secret Platform/Gateway failure categories.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PlatformErrorKind {
    /// Explicit service configuration is invalid.
    InvalidConfiguration,
    /// Secret input or producer output is empty, oversized or malformed.
    InvalidSecret,
    /// The blocking transport could not complete.
    TransportUnavailable,
    /// Response body exceeded the configured bound.
    ResponseTooLarge,
    /// A sensitive endpoint attempted an uncontracted redirect.
    RedirectRejected,
    /// The producer denied or could not complete the request.
    RequestDenied,
    /// Required no-store/no-cache response policy was absent.
    CachePolicyMissing,
    /// JSON or another response invariant was invalid.
    InvalidResponse,
    /// Valid JSON contained trailing data.
    TrailingResponseData,
    /// Gateway returned a protocol version other than one.
    UnsupportedProtocolVersion,
    /// World, character, port or relation validation failed.
    InvalidDirectory,
    /// Session expiry was elapsed or outside the W7 bound.
    InvalidExpiry,
    /// An internal invariant was violated without exposing raw data.
    InvariantViolation,
}

/// Stable redacted Platform/Gateway error.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct PlatformError {
    kind: PlatformErrorKind,
}

impl PlatformError {
    const fn new(kind: PlatformErrorKind) -> Self {
        Self { kind }
    }

    /// Return the stable machine-usable category.
    #[must_use]
    pub const fn kind(self) -> PlatformErrorKind {
        self.kind
    }
}

impl Display for PlatformError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        let message = match self.kind {
            PlatformErrorKind::InvalidConfiguration => "native-auth configuration is invalid",
            PlatformErrorKind::InvalidSecret => "native-auth secret value is invalid",
            PlatformErrorKind::TransportUnavailable => "native-auth transport is unavailable",
            PlatformErrorKind::ResponseTooLarge => "native-auth response exceeds the size limit",
            PlatformErrorKind::RedirectRejected => "native-auth redirect was rejected",
            PlatformErrorKind::RequestDenied => "native-auth request was denied",
            PlatformErrorKind::CachePolicyMissing => "native-auth cache policy is missing",
            PlatformErrorKind::InvalidResponse => "native-auth response is invalid",
            PlatformErrorKind::TrailingResponseData => "native-auth response has trailing data",
            PlatformErrorKind::UnsupportedProtocolVersion => {
                "native-auth protocol version is unsupported"
            }
            PlatformErrorKind::InvalidDirectory => "native-auth directory is invalid",
            PlatformErrorKind::InvalidExpiry => "native-auth credential expiry is invalid",
            PlatformErrorKind::InvariantViolation => "native-auth invariant was violated",
        };
        formatter.write_str(message)
    }
}

impl Error for PlatformError {}
