use oteryn_account_session::AccountSessionId;
use oteryn_foundation::{CancellationSource, Deadline, ManualClock, Moment, MonotonicClock};
use oteryn_identity::{
    BrowserLauncher, CallbackAttempt, CallbackBinder, CallbackReceiver, EntropySource,
    FixedAccountSession, IdentityClient, IdentityConfig, IdentityError, IdentityErrorKind,
};
use oteryn_platform::{
    HttpRequest, HttpResponse, HttpTransport, HttpTransportError, PlatformClient,
    PlatformEndpoints, PlatformErrorKind, SecretString, MAX_RESPONSE_BODY_BYTES,
};
use oteryn_world_directory::DirectoryRevision;
use std::error::Error;
use std::sync::Mutex;
use std::time::Duration;
use time::OffsetDateTime;
use url::Url;

const JSON: &str = "application/json";
const CACHE: &str = "no-store, no-cache, must-revalidate, private";

struct FixedEntropy;

impl EntropySource for FixedEntropy {
    fn fill(&self, destination: &mut [u8]) -> Result<(), IdentityError> {
        destination.fill(7);
        Ok(())
    }
}

struct AcceptingBrowser;

impl BrowserLauncher for AcceptingBrowser {
    fn open(&self, _authorization_url: &Url) -> Result<(), IdentityError> {
        Ok(())
    }
}

struct TimeoutBinder;

impl CallbackBinder for TimeoutBinder {
    fn bind(&self, callback_path: &str) -> Result<Box<dyn CallbackReceiver>, IdentityError> {
        let redirect_uri = Url::parse(&format!("http://127.0.0.1:49153{callback_path}"))
            .map_err(|_| IdentityError::for_kind(IdentityErrorKind::InvariantViolation))?;
        Ok(Box::new(TimeoutReceiver { redirect_uri }))
    }
}

struct TimeoutReceiver {
    redirect_uri: Url,
}

impl CallbackReceiver for TimeoutReceiver {
    fn redirect_uri(&self) -> &Url {
        &self.redirect_uri
    }

    fn receive(
        &mut self,
        _clock: &dyn MonotonicClock,
        _deadline: Deadline,
        _cancellation: &oteryn_foundation::CancellationToken,
    ) -> Result<CallbackAttempt, IdentityError> {
        Err(IdentityError::for_kind(
            IdentityErrorKind::CallbackTimeout,
        ))
    }
}

struct NoHttp;

impl HttpTransport for NoHttp {
    fn post(&self, _request: HttpRequest) -> Result<HttpResponse, HttpTransportError> {
        Err(HttpTransportError::InvalidRequest)
    }
}

fn session() -> Result<AccountSessionId, Box<dyn Error>> {
    Ok(AccountSessionId::new(41)?)
}

fn revision() -> Result<DirectoryRevision, Box<dyn Error>> {
    Ok(DirectoryRevision::new(3)?)
}

#[test]
fn callback_timeout_is_typed_and_stops_before_http() -> Result<(), Box<dyn Error>> {
    let endpoints =
        PlatformEndpoints::new("http://127.0.0.1:18080/", "http://127.0.0.1:18081/")?;
    let client = IdentityClient::new(
        PlatformClient::new(endpoints, NoHttp),
        Box::new(TimeoutBinder),
        Box::new(AcceptingBrowser),
        Box::new(FixedEntropy),
        Box::new(ManualClock::new(Moment::ZERO)),
    );
    let config = IdentityConfig::new(
        "http://127.0.0.1:18080/",
        "synthetic-public-client".to_owned(),
        "/callback".to_owned(),
        Duration::from_secs(10),
    )?;
    let cancellation = CancellationSource::new();
    let error = client
        .authenticate(
            &config,
            &FixedAccountSession(session()?),
            session()?,
            revision()?,
            &cancellation.token(),
        )
        .err()
        .ok_or("expected callback timeout")?;
    assert_eq!(error.kind(), IdentityErrorKind::CallbackTimeout);
    Ok(())
}

#[test]
fn response_construction_rejects_oversized_sensitive_body() -> Result<(), Box<dyn Error>> {
    let error = HttpResponse::new(
        200,
        Some(JSON.to_owned()),
        Some(CACHE.to_owned()),
        Some("no-cache".to_owned()),
        None,
        vec![0_u8; MAX_RESPONSE_BODY_BYTES + 1],
    )
    .err()
    .ok_or("expected oversized response rejection")?;
    assert_eq!(error.kind(), PlatformErrorKind::ResponseTooLarge);
    Ok(())
}

struct SingleResponse {
    response: Mutex<Option<HttpResponse>>,
}

impl HttpTransport for SingleResponse {
    fn post(&self, _request: HttpRequest) -> Result<HttpResponse, HttpTransportError> {
        match self.response.lock() {
            Ok(mut response) => response.take().ok_or(HttpTransportError::InvalidRequest),
            Err(poisoned) => poisoned
                .into_inner()
                .take()
                .ok_or(HttpTransportError::InvalidRequest),
        }
    }
}

fn gateway_response(body: serde_json::Value) -> Result<HttpResponse, Box<dyn Error>> {
    Ok(HttpResponse::new(
        200,
        Some(JSON.to_owned()),
        Some(CACHE.to_owned()),
        Some("no-cache".to_owned()),
        None,
        serde_json::to_vec(&body)?,
    )?)
}

fn request_gateway_case(body: serde_json::Value) -> Result<PlatformErrorKind, Box<dyn Error>> {
    let endpoints =
        PlatformEndpoints::new("http://127.0.0.1:18080/", "http://127.0.0.1:18081/")?;
    let client = PlatformClient::new(
        endpoints,
        SingleResponse {
            response: Mutex::new(Some(gateway_response(body)?)),
        },
    );
    let clock = ManualClock::new(Moment::ZERO);
    let error = client
        .request_game_entry_at(
            SecretString::new("synthetic-ticket".to_owned())?,
            session()?,
            revision()?,
            &clock,
            OffsetDateTime::UNIX_EPOCH,
        )
        .err()
        .ok_or("expected Gateway rejection")?;
    Ok(error.kind())
}

fn valid_gateway_body() -> serde_json::Value {
    serde_json::json!({
        "protocol_version": 1,
        "session": {
            "credential": "synthetic-session-credential",
            "expires_at": "1970-01-01T00:01:00Z"
        },
        "worlds": [{
            "id": 9,
            "slug": "current",
            "name": "Current",
            "region": "eu-central",
            "host": "127.0.0.1",
            "port": 7172
        }],
        "characters": [{
            "id": 17,
            "name": "Synthetic Knight",
            "level": 100,
            "vocation": 4,
            "world_id": 9
        }]
    })
}

#[test]
fn gateway_rejects_unsupported_protocol_version() -> Result<(), Box<dyn Error>> {
    let mut body = valid_gateway_body();
    body["protocol_version"] = serde_json::json!(2);
    assert_eq!(
        request_gateway_case(body)?,
        PlatformErrorKind::UnsupportedProtocolVersion
    );
    Ok(())
}

#[test]
fn gateway_rejects_duplicate_ids_invalid_port_and_unknown_world_relation()
-> Result<(), Box<dyn Error>> {
    let mut duplicate = valid_gateway_body();
    duplicate["worlds"] = serde_json::json!([
        {
            "id": 9,
            "slug": "current",
            "name": "Current",
            "region": "eu-central",
            "host": "127.0.0.1",
            "port": 7172
        },
        {
            "id": 9,
            "slug": "duplicate",
            "name": "Duplicate",
            "region": "eu-central",
            "host": "127.0.0.1",
            "port": 7173
        }
    ]);
    assert_eq!(
        request_gateway_case(duplicate)?,
        PlatformErrorKind::InvalidDirectory
    );

    let mut invalid_port = valid_gateway_body();
    invalid_port["worlds"][0]["port"] = serde_json::json!(0);
    assert_eq!(
        request_gateway_case(invalid_port)?,
        PlatformErrorKind::InvalidDirectory
    );

    let mut unknown_world = valid_gateway_body();
    unknown_world["characters"][0]["world_id"] = serde_json::json!(10);
    assert_eq!(
        request_gateway_case(unknown_world)?,
        PlatformErrorKind::InvalidDirectory
    );
    Ok(())
}
