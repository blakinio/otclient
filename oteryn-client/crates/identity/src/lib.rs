//! Authorization Code + PKCE transaction and loopback callback validation for W7.
//!
//! The crate owns no passwords and defines no substitute account, directory or
//! game-entry contracts. It composes the strict `oteryn-platform` boundary with
//! the merged producer-owned types.

use base64::Engine;
use base64::engine::general_purpose::URL_SAFE_NO_PAD;
use oteryn_account_session::AccountSessionId;
use oteryn_foundation::{CancellationToken, Deadline, MonotonicClock};
use oteryn_game_session::{EntryFailure, EntryFailureKind, GameEntryCredential};
use oteryn_platform::{
    HttpTransport, PlatformClient, PlatformErrorKind, SecretString, TokenExchange,
};
use oteryn_world_directory::{AccountDirectorySnapshot, DirectoryRevision};
use sha2::{Digest, Sha256};
use std::error::Error;
use std::fmt::{self, Debug, Display, Formatter};
use std::io::{Read, Write};
use std::net::{IpAddr, Ipv4Addr, TcpListener, TcpStream};
use std::process::Command;
use std::thread;
use std::time::Duration;
use url::Url;

/// Maximum accepted browser callback request header bytes.
pub const MAX_CALLBACK_REQUEST_BYTES: usize = 8 * 1024;
/// Maximum accepted callback request target bytes.
pub const MAX_CALLBACK_TARGET_BYTES: usize = 4 * 1024;
/// Minimum PKCE verifier length required by RFC 7636.
pub const MIN_PKCE_VERIFIER_BYTES: usize = 43;
/// Maximum PKCE verifier length required by RFC 7636.
pub const MAX_PKCE_VERIFIER_BYTES: usize = 128;
/// CSPRNG bytes encoded into one state value.
pub const STATE_RANDOM_BYTES: usize = 32;
/// CSPRNG bytes encoded into one verifier value.
pub const VERIFIER_RANDOM_BYTES: usize = 64;

/// Explicit immutable native OAuth configuration.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IdentityConfig {
    authorization_base: Url,
    client_id: String,
    callback_path: String,
    callback_timeout: Duration,
}

impl IdentityConfig {
    /// Validate the authorization service, public client identifier, exact
    /// callback path and one bounded callback timeout.
    pub fn new(
        authorization_base: &str,
        client_id: String,
        callback_path: String,
        callback_timeout: Duration,
    ) -> Result<Self, IdentityError> {
        let authorization_base = validate_authorization_base(authorization_base)?;
        if client_id.is_empty() || client_id.len() > 256 {
            return Err(IdentityError::new(IdentityErrorKind::InvalidConfiguration));
        }
        if callback_path != "/callback" {
            return Err(IdentityError::new(IdentityErrorKind::InvalidConfiguration));
        }
        if callback_timeout.is_zero() || callback_timeout > Duration::from_secs(300) {
            return Err(IdentityError::new(IdentityErrorKind::InvalidConfiguration));
        }
        Ok(Self {
            authorization_base,
            client_id,
            callback_path,
            callback_timeout,
        })
    }

    /// Return the exact callback path.
    #[must_use]
    pub fn callback_path(&self) -> &str {
        &self.callback_path
    }

    /// Return the callback deadline duration.
    #[must_use]
    pub const fn callback_timeout(&self) -> Duration {
        self.callback_timeout
    }
}

fn validate_authorization_base(value: &str) -> Result<Url, IdentityError> {
    let url = Url::parse(value)
        .map_err(|_| IdentityError::new(IdentityErrorKind::InvalidConfiguration))?;
    if url.username() != ""
        || url.password().is_some()
        || url.query().is_some()
        || url.fragment().is_some()
        || url.path() != "/"
    {
        return Err(IdentityError::new(IdentityErrorKind::InvalidConfiguration));
    }
    let host = url
        .host_str()
        .ok_or_else(|| IdentityError::new(IdentityErrorKind::InvalidConfiguration))?;
    let loopback = host.eq_ignore_ascii_case("localhost")
        || host
            .parse::<IpAddr>()
            .is_ok_and(|address| address.is_loopback());
    match url.scheme() {
        "https" => Ok(url),
        "http" if loopback => Ok(url),
        _ => Err(IdentityError::new(IdentityErrorKind::InvalidConfiguration)),
    }
}

/// Injectable CSPRNG boundary.
pub trait EntropySource: Send + Sync {
    /// Fill the complete destination with cryptographically secure random bytes.
    fn fill(&self, destination: &mut [u8]) -> Result<(), IdentityError>;
}

/// Operating-system entropy source backed by `getrandom`.
#[derive(Debug, Default, Clone, Copy)]
pub struct OsEntropy;

impl EntropySource for OsEntropy {
    fn fill(&self, destination: &mut [u8]) -> Result<(), IdentityError> {
        getrandom::fill(destination)
            .map_err(|_| IdentityError::new(IdentityErrorKind::EntropyUnavailable))
    }
}

/// Non-cloneable state/verifier bytes with redacted formatting and clearing.
struct SecretBytes(Box<[u8]>);

impl SecretBytes {
    fn new(value: Vec<u8>) -> Result<Self, IdentityError> {
        if value.is_empty() || value.len() > MAX_PKCE_VERIFIER_BYTES {
            return Err(IdentityError::new(IdentityErrorKind::InvalidSecret));
        }
        Ok(Self(value.into_boxed_slice()))
    }

    fn expose_secret(&self) -> Result<&str, IdentityError> {
        std::str::from_utf8(&self.0)
            .map_err(|_| IdentityError::new(IdentityErrorKind::InvariantViolation))
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

/// Browser launch adapter. Implementations must not use shell interpolation.
pub trait BrowserLauncher: Send + Sync {
    /// Open the complete authorization URL in the system browser.
    fn open(&self, authorization_url: &Url) -> Result<(), IdentityError>;
}

/// Platform-native browser launcher using a direct process argument.
#[derive(Debug, Default, Clone, Copy)]
pub struct SystemBrowser;

impl BrowserLauncher for SystemBrowser {
    fn open(&self, authorization_url: &Url) -> Result<(), IdentityError> {
        launch_system_browser(authorization_url)
    }
}

#[cfg(target_os = "windows")]
fn launch_system_browser(authorization_url: &Url) -> Result<(), IdentityError> {
    Command::new("explorer.exe")
        .arg(authorization_url.as_str())
        .spawn()
        .map(|_| ())
        .map_err(|_| IdentityError::new(IdentityErrorKind::BrowserLaunchFailed))
}

#[cfg(target_os = "macos")]
fn launch_system_browser(authorization_url: &Url) -> Result<(), IdentityError> {
    Command::new("open")
        .arg(authorization_url.as_str())
        .spawn()
        .map(|_| ())
        .map_err(|_| IdentityError::new(IdentityErrorKind::BrowserLaunchFailed))
}

#[cfg(all(unix, not(target_os = "macos")))]
fn launch_system_browser(authorization_url: &Url) -> Result<(), IdentityError> {
    Command::new("xdg-open")
        .arg(authorization_url.as_str())
        .spawn()
        .map(|_| ())
        .map_err(|_| IdentityError::new(IdentityErrorKind::BrowserLaunchFailed))
}

#[cfg(not(any(target_os = "windows", target_os = "macos", unix)))]
fn launch_system_browser(_authorization_url: &Url) -> Result<(), IdentityError> {
    Err(IdentityError::new(IdentityErrorKind::BrowserLaunchFailed))
}

/// One accepted TCP callback request reduced to the security-relevant facts.
///
/// The request target contains OAuth code/state material and therefore has no
/// ordinary clone or revealing debug surface.
pub struct CallbackAttempt {
    /// Remote peer observed by the bound listener.
    pub peer: IpAddr,
    /// Exact HTTP request target including query.
    pub target: String,
}

impl Debug for CallbackAttempt {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("CallbackAttempt")
            .field("peer", &self.peer)
            .field("target", &"[REDACTED]")
            .finish()
    }
}

/// One pre-bound loopback callback receiver.
pub trait CallbackReceiver: Send {
    /// Return the exact redirect URI containing the OS-assigned port.
    fn redirect_uri(&self) -> &Url;

    /// Receive one bounded request or a stable timeout/cancellation failure.
    fn receive(
        &mut self,
        clock: &dyn MonotonicClock,
        deadline: Deadline,
        cancellation: &CancellationToken,
    ) -> Result<CallbackAttempt, IdentityError>;
}

/// Factory that binds the listener before the browser is launched.
pub trait CallbackBinder: Send + Sync {
    /// Bind IPv4 `127.0.0.1:0` for the exact callback path.
    fn bind(&self, callback_path: &str) -> Result<Box<dyn CallbackReceiver>, IdentityError>;
}

/// Production IPv4 loopback listener binder.
#[derive(Debug, Default, Clone, Copy)]
pub struct TcpLoopbackBinder;

impl CallbackBinder for TcpLoopbackBinder {
    fn bind(&self, callback_path: &str) -> Result<Box<dyn CallbackReceiver>, IdentityError> {
        if callback_path != "/callback" {
            return Err(IdentityError::new(IdentityErrorKind::InvalidConfiguration));
        }
        let listener = TcpListener::bind((Ipv4Addr::LOCALHOST, 0))
            .map_err(|_| IdentityError::new(IdentityErrorKind::ListenerUnavailable))?;
        listener
            .set_nonblocking(true)
            .map_err(|_| IdentityError::new(IdentityErrorKind::ListenerUnavailable))?;
        let port = listener
            .local_addr()
            .map_err(|_| IdentityError::new(IdentityErrorKind::ListenerUnavailable))?
            .port();
        let redirect_uri = Url::parse(&format!("http://127.0.0.1:{port}{callback_path}"))
            .map_err(|_| IdentityError::new(IdentityErrorKind::InvariantViolation))?;
        Ok(Box::new(TcpCallbackReceiver {
            listener,
            redirect_uri,
        }))
    }
}

struct TcpCallbackReceiver {
    listener: TcpListener,
    redirect_uri: Url,
}

impl CallbackReceiver for TcpCallbackReceiver {
    fn redirect_uri(&self) -> &Url {
        &self.redirect_uri
    }

    fn receive(
        &mut self,
        clock: &dyn MonotonicClock,
        deadline: Deadline,
        cancellation: &CancellationToken,
    ) -> Result<CallbackAttempt, IdentityError> {
        loop {
            if cancellation.is_cancelled() {
                return Err(IdentityError::new(IdentityErrorKind::Cancelled));
            }
            if deadline.has_elapsed(clock) {
                return Err(IdentityError::new(IdentityErrorKind::CallbackTimeout));
            }
            match self.listener.accept() {
                Ok((mut stream, peer)) => {
                    let target = read_callback_target(&mut stream, clock, deadline, cancellation)?;
                    write_callback_response(&mut stream)?;
                    return Ok(CallbackAttempt {
                        peer: peer.ip(),
                        target,
                    });
                }
                Err(error) if error.kind() == std::io::ErrorKind::WouldBlock => {
                    let remaining = deadline.remaining(clock);
                    thread::sleep(remaining.min(Duration::from_millis(10)));
                }
                Err(_) => {
                    return Err(IdentityError::new(IdentityErrorKind::ListenerUnavailable));
                }
            }
        }
    }
}

fn read_callback_target(
    stream: &mut TcpStream,
    clock: &dyn MonotonicClock,
    deadline: Deadline,
    cancellation: &CancellationToken,
) -> Result<String, IdentityError> {
    let mut received = Vec::with_capacity(1024);
    let mut buffer = [0_u8; 512];
    loop {
        if cancellation.is_cancelled() {
            return Err(IdentityError::new(IdentityErrorKind::Cancelled));
        }
        if deadline.has_elapsed(clock) {
            return Err(IdentityError::new(IdentityErrorKind::CallbackTimeout));
        }
        stream
            .set_read_timeout(Some(
                deadline.remaining(clock).min(Duration::from_millis(250)),
            ))
            .map_err(|_| IdentityError::new(IdentityErrorKind::ListenerUnavailable))?;
        match stream.read(&mut buffer) {
            Ok(0) => return Err(IdentityError::new(IdentityErrorKind::MalformedCallback)),
            Ok(count) => {
                received.extend_from_slice(&buffer[..count]);
                if received.len() > MAX_CALLBACK_REQUEST_BYTES {
                    return Err(IdentityError::new(IdentityErrorKind::CallbackTooLarge));
                }
                if received.windows(4).any(|window| window == b"\r\n\r\n") {
                    break;
                }
            }
            Err(error)
                if matches!(
                    error.kind(),
                    std::io::ErrorKind::WouldBlock | std::io::ErrorKind::TimedOut
                ) => {}
            Err(_) => return Err(IdentityError::new(IdentityErrorKind::ListenerUnavailable)),
        }
    }
    let request = std::str::from_utf8(&received)
        .map_err(|_| IdentityError::new(IdentityErrorKind::MalformedCallback))?;
    let request_line = request
        .split("\r\n")
        .next()
        .ok_or_else(|| IdentityError::new(IdentityErrorKind::MalformedCallback))?;
    let mut parts = request_line.split(' ');
    let method = parts
        .next()
        .ok_or_else(|| IdentityError::new(IdentityErrorKind::MalformedCallback))?;
    let target = parts
        .next()
        .ok_or_else(|| IdentityError::new(IdentityErrorKind::MalformedCallback))?;
    let version = parts
        .next()
        .ok_or_else(|| IdentityError::new(IdentityErrorKind::MalformedCallback))?;
    if method != "GET" || version != "HTTP/1.1" || parts.next().is_some() {
        return Err(IdentityError::new(IdentityErrorKind::MalformedCallback));
    }
    if target.len() > MAX_CALLBACK_TARGET_BYTES {
        return Err(IdentityError::new(IdentityErrorKind::CallbackTooLarge));
    }
    Ok(target.to_owned())
}

fn write_callback_response(stream: &mut TcpStream) -> Result<(), IdentityError> {
    const BODY: &str = "Oteryn sign-in callback received. You may close this window.";
    let response = format!(
        "HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nCache-Control: no-store\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{BODY}",
        BODY.len()
    );
    stream
        .write_all(response.as_bytes())
        .map_err(|_| IdentityError::new(IdentityErrorKind::ListenerUnavailable))
}

/// Current active account-session generation source.
pub trait ActiveAccountSession: Send + Sync {
    /// Return the currently accepted non-secret local generation.
    fn active_account_session(&self) -> Option<AccountSessionId>;
}

/// Fixed generation source useful for one owned worker invocation.
#[derive(Debug, Clone, Copy)]
pub struct FixedAccountSession(pub AccountSessionId);

impl ActiveAccountSession for FixedAccountSession {
    fn active_account_session(&self) -> Option<AccountSessionId> {
        Some(self.0)
    }
}

/// One stateful PKCE transaction. State and verifier are never cloneable or formatted.
pub struct AuthorizationTransaction {
    session_id: AccountSessionId,
    redirect_uri: Url,
    state: SecretBytes,
    verifier: Option<SecretBytes>,
    challenge: String,
    callback_consumed: bool,
}

impl AuthorizationTransaction {
    /// Create one transaction from injected CSPRNG bytes.
    pub fn new(
        session_id: AccountSessionId,
        redirect_uri: Url,
        entropy: &dyn EntropySource,
    ) -> Result<Self, IdentityError> {
        validate_dynamic_redirect(&redirect_uri)?;
        let mut state_bytes = [0_u8; STATE_RANDOM_BYTES];
        let mut verifier_bytes = [0_u8; VERIFIER_RANDOM_BYTES];
        entropy.fill(&mut state_bytes)?;
        entropy.fill(&mut verifier_bytes)?;
        let state = URL_SAFE_NO_PAD.encode(state_bytes);
        let verifier = URL_SAFE_NO_PAD.encode(verifier_bytes);
        Self::from_encoded_values(session_id, redirect_uri, state, verifier)
    }

    fn from_encoded_values(
        session_id: AccountSessionId,
        redirect_uri: Url,
        state: String,
        verifier: String,
    ) -> Result<Self, IdentityError> {
        if verifier.len() < MIN_PKCE_VERIFIER_BYTES || verifier.len() > MAX_PKCE_VERIFIER_BYTES {
            return Err(IdentityError::new(IdentityErrorKind::InvalidSecret));
        }
        let challenge = pkce_challenge(&verifier);
        Ok(Self {
            session_id,
            redirect_uri,
            state: SecretBytes::new(state.into_bytes())?,
            verifier: Some(SecretBytes::new(verifier.into_bytes())?),
            challenge,
            callback_consumed: false,
        })
    }

    /// Build the exact authorization URL. Callers must treat the complete URL as
    /// sensitive because it contains state.
    pub fn authorization_url(&self, config: &IdentityConfig) -> Result<Url, IdentityError> {
        let mut url = config
            .authorization_base
            .join("oauth/authorize")
            .map_err(|_| IdentityError::new(IdentityErrorKind::InvalidConfiguration))?;
        let state = self.state.expose_secret()?;
        url.query_pairs_mut()
            .append_pair("client_id", &config.client_id)
            .append_pair("redirect_uri", self.redirect_uri.as_str())
            .append_pair("response_type", "code")
            .append_pair("scope", "game:ticket")
            .append_pair("state", state)
            .append_pair("code_challenge", &self.challenge)
            .append_pair("code_challenge_method", "S256");
        Ok(url)
    }

    /// Validate one exact callback and consume the transaction callback slot.
    pub fn accept_callback(
        &mut self,
        active_session_id: Option<AccountSessionId>,
        attempt: CallbackAttempt,
    ) -> Result<SecretString, IdentityError> {
        if self.callback_consumed {
            return Err(IdentityError::new(IdentityErrorKind::DuplicateCallback));
        }
        if active_session_id != Some(self.session_id) {
            return Err(IdentityError::new(IdentityErrorKind::StaleGeneration));
        }
        if !matches!(attempt.peer, IpAddr::V4(address) if address.is_loopback()) {
            return Err(IdentityError::new(IdentityErrorKind::InvalidCallbackPeer));
        }
        let callback = parse_callback_target(&attempt.target)?;
        if callback.path() != self.redirect_uri.path() {
            return Err(IdentityError::new(IdentityErrorKind::InvalidCallbackPath));
        }
        let mut code = None;
        let mut state = None;
        let mut oauth_error = None;
        for (key, value) in callback.query_pairs() {
            match key.as_ref() {
                "code" if code.is_none() => code = Some(value.into_owned()),
                "state" if state.is_none() => state = Some(value.into_owned()),
                "error" if oauth_error.is_none() => oauth_error = Some(value.into_owned()),
                "error_description" | "error_uri" => {}
                "code" | "state" | "error" => {
                    return Err(IdentityError::new(IdentityErrorKind::MalformedCallback));
                }
                _ => return Err(IdentityError::new(IdentityErrorKind::MalformedCallback)),
            }
        }
        if oauth_error.is_some() {
            self.callback_consumed = true;
            return Err(IdentityError::new(IdentityErrorKind::AuthorizationDenied));
        }
        let returned_state =
            state.ok_or_else(|| IdentityError::new(IdentityErrorKind::MalformedCallback))?;
        if !constant_time_equal(
            self.state.expose_secret()?.as_bytes(),
            returned_state.as_bytes(),
        ) {
            return Err(IdentityError::new(IdentityErrorKind::InvalidCallbackState));
        }
        let code = code.ok_or_else(|| IdentityError::new(IdentityErrorKind::MalformedCallback))?;
        self.callback_consumed = true;
        SecretString::new(code).map_err(|_| IdentityError::new(IdentityErrorKind::InvalidSecret))
    }

    fn take_verifier(&mut self) -> Result<SecretString, IdentityError> {
        let verifier = self
            .verifier
            .take()
            .ok_or_else(|| IdentityError::new(IdentityErrorKind::InvariantViolation))?;
        let value = verifier.expose_secret()?.to_owned();
        SecretString::new(value).map_err(|_| IdentityError::new(IdentityErrorKind::InvalidSecret))
    }
}

impl Debug for AuthorizationTransaction {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("AuthorizationTransaction")
            .field("session_id", &self.session_id)
            .field("redirect_uri", &self.redirect_uri)
            .field("state", &"[REDACTED]")
            .field("verifier", &"[REDACTED]")
            .field("challenge", &"[REDACTED]")
            .field("callback_consumed", &self.callback_consumed)
            .finish()
    }
}

fn validate_dynamic_redirect(url: &Url) -> Result<(), IdentityError> {
    if url.scheme() != "http"
        || url.host_str() != Some("127.0.0.1")
        || url.path() != "/callback"
        || url.port().is_none()
        || url.query().is_some()
        || url.fragment().is_some()
        || url.username() != ""
        || url.password().is_some()
    {
        return Err(IdentityError::new(IdentityErrorKind::InvalidConfiguration));
    }
    Ok(())
}

fn parse_callback_target(target: &str) -> Result<Url, IdentityError> {
    if !target.starts_with('/') || target.len() > MAX_CALLBACK_TARGET_BYTES {
        return Err(IdentityError::new(IdentityErrorKind::MalformedCallback));
    }
    Url::parse(&format!("http://127.0.0.1{target}"))
        .map_err(|_| IdentityError::new(IdentityErrorKind::MalformedCallback))
}

fn pkce_challenge(verifier: &str) -> String {
    URL_SAFE_NO_PAD.encode(Sha256::digest(verifier.as_bytes()))
}

fn constant_time_equal(left: &[u8], right: &[u8]) -> bool {
    let mut difference = left.len() ^ right.len();
    let compared = left.len().min(right.len());
    for index in 0..compared {
        difference |= usize::from(left[index] ^ right[index]);
    }
    difference == 0
}

/// Successful merged account/directory/credential result.
pub struct IdentityBootstrap {
    account_session_id: AccountSessionId,
    directory: AccountDirectorySnapshot,
    credential: GameEntryCredential,
}

impl IdentityBootstrap {
    /// Return the originating local generation.
    #[must_use]
    pub const fn account_session_id(&self) -> AccountSessionId {
        self.account_session_id
    }

    /// Consume into the merged producer-owned directory and credential.
    #[must_use]
    pub fn into_parts(self) -> (AccountDirectorySnapshot, GameEntryCredential) {
        (self.directory, self.credential)
    }
}

impl Debug for IdentityBootstrap {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("IdentityBootstrap")
            .field("account_session_id", &self.account_session_id)
            .field("directory", &self.directory)
            .field("credential", &"[REDACTED]")
            .finish()
    }
}

/// Complete synchronous W7 Identity client. Application composition runs this
/// object on an owned worker thread rather than on the window event loop.
pub struct IdentityClient<T> {
    platform: PlatformClient<T>,
    binder: Box<dyn CallbackBinder>,
    browser: Box<dyn BrowserLauncher>,
    entropy: Box<dyn EntropySource>,
    clock: Box<dyn MonotonicClock>,
}

impl<T> IdentityClient<T>
where
    T: HttpTransport,
{
    /// Compose explicit injected capabilities.
    #[must_use]
    pub fn new(
        platform: PlatformClient<T>,
        binder: Box<dyn CallbackBinder>,
        browser: Box<dyn BrowserLauncher>,
        entropy: Box<dyn EntropySource>,
        clock: Box<dyn MonotonicClock>,
    ) -> Self {
        Self {
            platform,
            binder,
            browser,
            entropy,
            clock,
        }
    }

    /// Perform one bounded bootstrap attempt with no automatic retry.
    pub fn authenticate(
        &self,
        config: &IdentityConfig,
        sessions: &dyn ActiveAccountSession,
        account_session_id: AccountSessionId,
        directory_revision: DirectoryRevision,
        cancellation: &CancellationToken,
    ) -> Result<IdentityBootstrap, IdentityError> {
        ensure_active(sessions, account_session_id, cancellation)?;
        let mut receiver = self.binder.bind(config.callback_path())?;
        let mut transaction = AuthorizationTransaction::new(
            account_session_id,
            receiver.redirect_uri().clone(),
            self.entropy.as_ref(),
        )?;
        let authorization_url = transaction.authorization_url(config)?;
        self.browser.open(&authorization_url)?;
        let callback_deadline = Deadline::after(self.clock.as_ref(), config.callback_timeout())
            .map_err(|_| IdentityError::new(IdentityErrorKind::InvalidConfiguration))?;
        let attempt = receiver.receive(self.clock.as_ref(), callback_deadline, cancellation)?;
        let code = transaction.accept_callback(sessions.active_account_session(), attempt)?;
        ensure_active(sessions, account_session_id, cancellation)?;
        let verifier = transaction.take_verifier()?;
        let tokens = self
            .platform
            .exchange_authorization_code(TokenExchange {
                client_id: config.client_id.clone(),
                redirect_uri: receiver.redirect_uri().clone(),
                code,
                verifier,
            })
            .map_err(IdentityError::from_platform)?;
        ensure_active(sessions, account_session_id, cancellation)?;
        let ticket = self
            .platform
            .issue_game_login_ticket(tokens.into_access_token())
            .map_err(IdentityError::from_platform)?;
        ensure_active(sessions, account_session_id, cancellation)?;
        let gateway = self
            .platform
            .request_game_entry(
                ticket,
                account_session_id,
                directory_revision,
                self.clock.as_ref(),
            )
            .map_err(IdentityError::from_platform)?;
        ensure_active(sessions, account_session_id, cancellation)?;
        let (directory, credential) = gateway.into_parts();
        Ok(IdentityBootstrap {
            account_session_id,
            directory,
            credential,
        })
    }
}

fn ensure_active(
    sessions: &dyn ActiveAccountSession,
    expected: AccountSessionId,
    cancellation: &CancellationToken,
) -> Result<(), IdentityError> {
    if cancellation.is_cancelled() {
        return Err(IdentityError::new(IdentityErrorKind::Cancelled));
    }
    if sessions.active_account_session() != Some(expected) {
        return Err(IdentityError::new(IdentityErrorKind::StaleGeneration));
    }
    Ok(())
}

/// Stable non-secret Identity failure categories.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum IdentityErrorKind {
    /// Explicit endpoint/client/callback configuration is invalid.
    InvalidConfiguration,
    /// CSPRNG bytes could not be obtained.
    EntropyUnavailable,
    /// State, verifier or code was malformed.
    InvalidSecret,
    /// System-browser launch failed.
    BrowserLaunchFailed,
    /// Loopback listener bind, accept, read or response failed.
    ListenerUnavailable,
    /// The callback exceeded its deadline.
    CallbackTimeout,
    /// The active operation was explicitly cancelled.
    Cancelled,
    /// The request peer was not IPv4 loopback.
    InvalidCallbackPeer,
    /// The callback path did not match exactly.
    InvalidCallbackPath,
    /// Returned OAuth state did not match.
    InvalidCallbackState,
    /// Callback syntax, required parameters or uniqueness were invalid.
    MalformedCallback,
    /// Callback request exceeded a bounded input limit.
    CallbackTooLarge,
    /// The producer returned a bounded OAuth denial.
    AuthorizationDenied,
    /// The callback slot was already consumed.
    DuplicateCallback,
    /// Completion belongs to an obsolete account generation.
    StaleGeneration,
    /// Strict Platform/Gateway boundary failed.
    Platform(PlatformErrorKind),
    /// An internal invariant was violated.
    InvariantViolation,
}

/// Stable redacted Identity error.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct IdentityError {
    kind: IdentityErrorKind,
}

impl IdentityError {
    const fn new(kind: IdentityErrorKind) -> Self {
        Self::for_kind(kind)
    }

    /// Construct a stable redacted error from its closed category.
    #[must_use]
    pub const fn for_kind(kind: IdentityErrorKind) -> Self {
        Self { kind }
    }

    fn from_platform(error: oteryn_platform::PlatformError) -> Self {
        Self::new(IdentityErrorKind::Platform(error.kind()))
    }

    /// Return the stable machine-usable failure category.
    #[must_use]
    pub const fn kind(self) -> IdentityErrorKind {
        self.kind
    }

    /// Map into the merged entry failure vocabulary without backend text.
    #[must_use]
    pub const fn entry_failure(self) -> EntryFailure {
        let kind = match self.kind {
            IdentityErrorKind::DuplicateCallback => EntryFailureKind::DuplicateCallback,
            IdentityErrorKind::StaleGeneration => EntryFailureKind::StaleAuthenticationTransaction,
            IdentityErrorKind::Cancelled => EntryFailureKind::SafeCancellation,
            IdentityErrorKind::Platform(PlatformErrorKind::UnsupportedProtocolVersion) => {
                EntryFailureKind::ProtocolMismatch
            }
            IdentityErrorKind::Platform(PlatformErrorKind::InvalidDirectory) => {
                EntryFailureKind::SelectedEntryUnavailable
            }
            IdentityErrorKind::Platform(PlatformErrorKind::InvalidExpiry) => {
                EntryFailureKind::CredentialExpired
            }
            IdentityErrorKind::InvalidConfiguration
            | IdentityErrorKind::EntropyUnavailable
            | IdentityErrorKind::InvalidSecret
            | IdentityErrorKind::InvalidCallbackPeer
            | IdentityErrorKind::InvalidCallbackPath
            | IdentityErrorKind::InvalidCallbackState
            | IdentityErrorKind::MalformedCallback
            | IdentityErrorKind::CallbackTooLarge
            | IdentityErrorKind::AuthorizationDenied
            | IdentityErrorKind::InvariantViolation
            | IdentityErrorKind::Platform(PlatformErrorKind::InvalidConfiguration)
            | IdentityErrorKind::Platform(PlatformErrorKind::InvalidSecret)
            | IdentityErrorKind::Platform(PlatformErrorKind::RedirectRejected)
            | IdentityErrorKind::Platform(PlatformErrorKind::CachePolicyMissing)
            | IdentityErrorKind::Platform(PlatformErrorKind::InvalidResponse)
            | IdentityErrorKind::Platform(PlatformErrorKind::TrailingResponseData)
            | IdentityErrorKind::Platform(PlatformErrorKind::InvariantViolation) => {
                EntryFailureKind::InvariantViolation
            }
            IdentityErrorKind::BrowserLaunchFailed
            | IdentityErrorKind::ListenerUnavailable
            | IdentityErrorKind::CallbackTimeout
            | IdentityErrorKind::Platform(PlatformErrorKind::TransportUnavailable)
            | IdentityErrorKind::Platform(PlatformErrorKind::ResponseTooLarge)
            | IdentityErrorKind::Platform(PlatformErrorKind::RequestDenied) => {
                EntryFailureKind::TransportFailure
            }
        };
        EntryFailure::for_kind(kind)
    }
}

impl Display for IdentityError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        let message = match self.kind {
            IdentityErrorKind::InvalidConfiguration => "identity configuration is invalid",
            IdentityErrorKind::EntropyUnavailable => "identity entropy source is unavailable",
            IdentityErrorKind::InvalidSecret => "identity secret value is invalid",
            IdentityErrorKind::BrowserLaunchFailed => "system browser launch failed",
            IdentityErrorKind::ListenerUnavailable => "loopback callback listener is unavailable",
            IdentityErrorKind::CallbackTimeout => "loopback callback timed out",
            IdentityErrorKind::Cancelled => "identity transaction was cancelled",
            IdentityErrorKind::InvalidCallbackPeer => "callback peer is invalid",
            IdentityErrorKind::InvalidCallbackPath => "callback path is invalid",
            IdentityErrorKind::InvalidCallbackState => "callback state is invalid",
            IdentityErrorKind::MalformedCallback => "callback request is malformed",
            IdentityErrorKind::CallbackTooLarge => "callback request exceeds the size limit",
            IdentityErrorKind::AuthorizationDenied => "authorization was denied",
            IdentityErrorKind::DuplicateCallback => "callback was already consumed",
            IdentityErrorKind::StaleGeneration => "identity generation is stale",
            IdentityErrorKind::Platform(_) => "Platform or Gateway request failed",
            IdentityErrorKind::InvariantViolation => "identity invariant was violated",
        };
        formatter.write_str(message)
    }
}

impl Error for IdentityError {}

#[cfg(test)]
mod tests {
    use super::*;

    struct FixedEntropy {
        byte: u8,
    }

    impl EntropySource for FixedEntropy {
        fn fill(&self, destination: &mut [u8]) -> Result<(), IdentityError> {
            destination.fill(self.byte);
            Ok(())
        }
    }

    fn session() -> Result<AccountSessionId, Box<dyn Error>> {
        Ok(AccountSessionId::new(7)?)
    }

    #[test]
    fn pkce_s256_matches_the_rfc_7636_vector() {
        let verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk";
        assert_eq!(
            pkce_challenge(verifier),
            "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"
        );
    }

    #[test]
    fn transaction_uses_dynamic_loopback_redirect_and_redacts_debug() -> Result<(), Box<dyn Error>>
    {
        let redirect = Url::parse("http://127.0.0.1:49152/callback")?;
        let transaction =
            AuthorizationTransaction::new(session()?, redirect, &FixedEntropy { byte: 3 })?;
        let debug = format!("{transaction:?}");
        assert!(!debug.contains("AwMDAw"));
        assert!(debug.contains("[REDACTED]"));
        let callback = CallbackAttempt {
            peer: IpAddr::V4(Ipv4Addr::LOCALHOST),
            target: "/callback?code=synthetic-code&state=synthetic-state".to_owned(),
        };
        let callback_debug = format!("{callback:?}");
        assert!(!callback_debug.contains("synthetic-code"));
        assert!(!callback_debug.contains("synthetic-state"));
        assert!(callback_debug.contains("[REDACTED]"));
        Ok(())
    }

    #[test]
    fn callback_rejects_state_mismatch_stale_peer_and_duplicate() -> Result<(), Box<dyn Error>> {
        let redirect = Url::parse("http://127.0.0.1:49152/callback")?;
        let mut transaction = AuthorizationTransaction::from_encoded_values(
            session()?,
            redirect,
            "expected-state".to_owned(),
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~".to_owned(),
        )?;
        let wrong_state = CallbackAttempt {
            peer: IpAddr::V4(Ipv4Addr::LOCALHOST),
            target: "/callback?code=synthetic-code&state=wrong".to_owned(),
        };
        assert_eq!(
            transaction
                .accept_callback(Some(session()?), wrong_state)
                .err()
                .map(|error| error.kind()),
            Some(IdentityErrorKind::InvalidCallbackState)
        );
        let remote = CallbackAttempt {
            peer: "192.0.2.10".parse()?,
            target: "/callback?code=synthetic-code&state=expected-state".to_owned(),
        };
        assert_eq!(
            transaction
                .accept_callback(Some(session()?), remote)
                .err()
                .map(|error| error.kind()),
            Some(IdentityErrorKind::InvalidCallbackPeer)
        );
        let code = transaction.accept_callback(
            Some(session()?),
            CallbackAttempt {
                peer: IpAddr::V4(Ipv4Addr::LOCALHOST),
                target: "/callback?code=synthetic-code&state=expected-state".to_owned(),
            },
        )?;
        assert_eq!(code.expose_secret()?, "synthetic-code");
        assert_eq!(
            transaction
                .accept_callback(
                    Some(session()?),
                    CallbackAttempt {
                        peer: IpAddr::V4(Ipv4Addr::LOCALHOST),
                        target: "/callback?code=synthetic-code&state=expected-state".to_owned(),
                    },
                )
                .err()
                .map(|error| error.kind()),
            Some(IdentityErrorKind::DuplicateCallback)
        );
        Ok(())
    }

    #[test]
    fn callback_rejects_stale_generation_and_wrong_path() -> Result<(), Box<dyn Error>> {
        let redirect = Url::parse("http://127.0.0.1:49152/callback")?;
        let mut transaction = AuthorizationTransaction::from_encoded_values(
            session()?,
            redirect,
            "expected-state".to_owned(),
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~".to_owned(),
        )?;
        assert_eq!(
            transaction
                .accept_callback(
                    Some(AccountSessionId::new(8)?),
                    CallbackAttempt {
                        peer: IpAddr::V4(Ipv4Addr::LOCALHOST),
                        target: "/other?code=synthetic-code&state=expected-state".to_owned(),
                    },
                )
                .err()
                .map(|error| error.kind()),
            Some(IdentityErrorKind::StaleGeneration)
        );
        assert_eq!(
            transaction
                .accept_callback(
                    Some(session()?),
                    CallbackAttempt {
                        peer: IpAddr::V4(Ipv4Addr::LOCALHOST),
                        target: "/other?code=synthetic-code&state=expected-state".to_owned(),
                    },
                )
                .err()
                .map(|error| error.kind()),
            Some(IdentityErrorKind::InvalidCallbackPath)
        );
        Ok(())
    }

    #[test]
    fn callback_parser_rejects_duplicates_and_unknown_parameters() -> Result<(), Box<dyn Error>> {
        let redirect = Url::parse("http://127.0.0.1:49152/callback")?;
        let mut transaction = AuthorizationTransaction::from_encoded_values(
            session()?,
            redirect,
            "expected-state".to_owned(),
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~".to_owned(),
        )?;
        for target in [
            "/callback?code=one&code=two&state=expected-state",
            "/callback?code=one&state=expected-state&extra=value",
        ] {
            let result = transaction.accept_callback(
                Some(session()?),
                CallbackAttempt {
                    peer: IpAddr::V4(Ipv4Addr::LOCALHOST),
                    target: target.to_owned(),
                },
            );
            assert_eq!(
                result.err().map(|error| error.kind()),
                Some(IdentityErrorKind::MalformedCallback)
            );
        }
        Ok(())
    }
}
