//! Focused fake-service security evidence for the W7 Identity lane.

#[cfg(test)]
mod tests {
    use oteryn_account_session::AccountSessionId;
    use oteryn_foundation::{CancellationSource, ManualClock, Moment};
    use oteryn_identity::{
        ActiveAccountSession, AuthorizationTransaction, BrowserLauncher, CallbackAttempt,
        CallbackBinder, CallbackReceiver, EntropySource, FixedAccountSession, IdentityClient,
        IdentityConfig, IdentityError, IdentityErrorKind,
    };
    use oteryn_platform::{
        HttpRequest, HttpResponse, HttpTransport, HttpTransportError, PlatformClient,
        PlatformEndpoints, SecretString, TokenExchange,
    };
    use oteryn_world_directory::DirectoryRevision;
    use std::error::Error;
    use std::net::{IpAddr, Ipv4Addr};
    use std::sync::atomic::{AtomicU8, AtomicUsize, Ordering};
    use std::sync::{Arc, Mutex};
    use std::time::Duration;
    use time::format_description::well_known::Rfc3339;
    use time::OffsetDateTime;
    use url::Url;

    const JSON: &str = "application/json";
    const CACHE: &str = "no-store, no-cache, must-revalidate, private";

    struct CounterEntropy {
        next: AtomicU8,
    }

    impl CounterEntropy {
        fn new() -> Self {
            Self {
                next: AtomicU8::new(1),
            }
        }
    }

    impl EntropySource for CounterEntropy {
        fn fill(&self, destination: &mut [u8]) -> Result<(), IdentityError> {
            let byte = self.next.fetch_add(1, Ordering::AcqRel);
            destination.fill(byte);
            Ok(())
        }
    }

    #[derive(Default)]
    struct BrowserState {
        opened_url: Mutex<Option<Url>>,
        order: AtomicUsize,
    }

    struct FakeBrowser {
        state: Arc<BrowserState>,
    }

    impl BrowserLauncher for FakeBrowser {
        fn open(&self, authorization_url: &Url) -> Result<(), IdentityError> {
            assert_eq!(self.state.order.load(Ordering::Acquire), 1);
            let mut opened = lock(&self.state.opened_url);
            *opened = Some(authorization_url.clone());
            self.state.order.store(2, Ordering::Release);
            Ok(())
        }
    }

    struct FakeBinder {
        state: Arc<BrowserState>,
        port: u16,
    }

    impl CallbackBinder for FakeBinder {
        fn bind(&self, callback_path: &str) -> Result<Box<dyn CallbackReceiver>, IdentityError> {
            assert_eq!(callback_path, "/callback");
            assert_eq!(self.state.order.swap(1, Ordering::AcqRel), 0);
            let redirect_uri = Url::parse(&format!(
                "http://127.0.0.1:{}{}",
                self.port, callback_path
            ))
            .map_err(|_| synthetic_identity_error())?;
            Ok(Box::new(FakeReceiver {
                state: Arc::clone(&self.state),
                redirect_uri,
            }))
        }
    }

    struct FakeReceiver {
        state: Arc<BrowserState>,
        redirect_uri: Url,
    }

    impl CallbackReceiver for FakeReceiver {
        fn redirect_uri(&self) -> &Url {
            &self.redirect_uri
        }

        fn receive(
            &mut self,
            _clock: &dyn oteryn_foundation::MonotonicClock,
            _deadline: oteryn_foundation::Deadline,
            cancellation: &oteryn_foundation::CancellationToken,
        ) -> Result<CallbackAttempt, IdentityError> {
            if cancellation.is_cancelled() {
                return Err(synthetic_identity_error());
            }
            assert_eq!(self.state.order.load(Ordering::Acquire), 2);
            let opened = lock(&self.state.opened_url);
            let url = opened.as_ref().ok_or_else(synthetic_identity_error)?;
            assert_eq!(
                url.query_pairs()
                    .find(|(key, _)| key == "redirect_uri")
                    .map(|(_, value)| value.into_owned()),
                Some(self.redirect_uri.as_str().to_owned())
            );
            let state = url
                .query_pairs()
                .find(|(key, _)| key == "state")
                .map(|(_, value)| value.into_owned())
                .ok_or_else(synthetic_identity_error)?;
            self.state.order.store(3, Ordering::Release);
            Ok(CallbackAttempt {
                peer: IpAddr::V4(Ipv4Addr::LOCALHOST),
                target: format!("/callback?code=synthetic-code&state={state}"),
            })
        }
    }

    #[derive(Default)]
    struct FakeHttpState {
        calls: usize,
        debug_outputs: Vec<String>,
    }

    struct FakeHttp {
        state: Arc<Mutex<FakeHttpState>>,
    }

    impl FakeHttp {
        fn new(state: Arc<Mutex<FakeHttpState>>) -> Self {
            Self { state }
        }
    }

    impl HttpTransport for FakeHttp {
        fn post(&self, request: HttpRequest) -> Result<HttpResponse, HttpTransportError> {
            let mut state = lock(&self.state);
            state.debug_outputs.push(format!("{request:?}"));
            state.calls += 1;
            match state.calls {
                1 => {
                    assert_eq!(request.url().path(), "/oauth/token");
                    assert_eq!(request.content_type(), "application/x-www-form-urlencoded");
                    assert!(request.bearer().map_err(|_| HttpTransportError::InvalidRequest)?.is_none());
                    let body = std::str::from_utf8(request.body())
                        .map_err(|_| HttpTransportError::InvalidRequest)?;
                    assert!(body.contains("grant_type=authorization_code"));
                    assert!(body.contains("code=synthetic-code"));
                    json_response(
                        br#"{"token_type":"Bearer","expires_in":300,"access_token":"synthetic-access","refresh_token":"synthetic-refresh"}"#.to_vec(),
                    )
                }
                2 => {
                    assert_eq!(request.url().path(), "/api/v1/game-auth/tickets");
                    assert_eq!(
                        request.bearer().map_err(|_| HttpTransportError::InvalidRequest)?,
                        Some("synthetic-access")
                    );
                    assert_eq!(request.body(), br#"{"protocol_version":1}"#);
                    json_response(
                        br#"{"protocol_version":1,"ticket":"synthetic-ticket","expires_in":60}"#.to_vec(),
                    )
                }
                3 => {
                    assert_eq!(request.url().path(), "/v1/login");
                    assert!(request.bearer().map_err(|_| HttpTransportError::InvalidRequest)?.is_none());
                    let body: serde_json::Value = serde_json::from_slice(request.body())
                        .map_err(|_| HttpTransportError::InvalidRequest)?;
                    assert_eq!(body["protocol_version"], 1);
                    assert_eq!(body["game_login_ticket"], "synthetic-ticket");
                    let expires_at = (OffsetDateTime::now_utc() + time::Duration::seconds(60))
                        .format(&Rfc3339)
                        .map_err(|_| HttpTransportError::InvalidRequest)?;
                    let response = serde_json::json!({
                        "protocol_version": 1,
                        "session": {
                            "credential": "synthetic-session-credential",
                            "expires_at": expires_at
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
                    });
                    json_response(
                        serde_json::to_vec(&response)
                            .map_err(|_| HttpTransportError::InvalidRequest)?,
                    )
                }
                _ => Err(HttpTransportError::InvalidRequest),
            }
        }
    }

    fn json_response(body: Vec<u8>) -> Result<HttpResponse, HttpTransportError> {
        HttpResponse::new(
            200,
            Some(JSON.to_owned()),
            Some(CACHE.to_owned()),
            Some("no-cache".to_owned()),
            None,
            body,
        )
        .map_err(|_| HttpTransportError::InvalidRequest)
    }

    fn lock<T>(mutex: &Mutex<T>) -> std::sync::MutexGuard<'_, T> {
        match mutex.lock() {
            Ok(guard) => guard,
            Err(poisoned) => poisoned.into_inner(),
        }
    }

    fn synthetic_identity_error() -> IdentityError {
        IdentityConfig::new(
            "http://remote.invalid/",
            "invalid".to_owned(),
            "/callback".to_owned(),
            Duration::from_secs(1),
        )
        .err()
        .unwrap_or_else(|| {
            let valid = IdentityConfig::new(
                "http://127.0.0.1/",
                "valid".to_owned(),
                "/wrong".to_owned(),
                Duration::from_secs(1),
            );
            match valid {
                Err(error) => error,
                Ok(_) => unreachable_identity_error(),
            }
        })
    }

    fn unreachable_identity_error() -> IdentityError {
        let result = IdentityConfig::new(
            "http://127.0.0.1/",
            String::new(),
            "/callback".to_owned(),
            Duration::from_secs(1),
        );
        match result {
            Err(error) => error,
            Ok(_) => synthetic_identity_error(),
        }
    }

    fn session() -> Result<AccountSessionId, Box<dyn Error>> {
        Ok(AccountSessionId::new(41)?)
    }

    fn revision() -> Result<DirectoryRevision, Box<dyn Error>> {
        Ok(DirectoryRevision::new(3)?)
    }

    #[test]
    fn fake_services_prove_dynamic_callback_and_one_shot_bootstrap() -> Result<(), Box<dyn Error>> {
        let browser_state = Arc::new(BrowserState::default());
        let http_state = Arc::new(Mutex::new(FakeHttpState::default()));
        let endpoints = PlatformEndpoints::new(
            "http://127.0.0.1:18080/",
            "http://127.0.0.1:18081/",
        )?;
        let platform = PlatformClient::new(endpoints, FakeHttp::new(Arc::clone(&http_state)));
        let client = IdentityClient::new(
            platform,
            Box::new(FakeBinder {
                state: Arc::clone(&browser_state),
                port: 49152,
            }),
            Box::new(FakeBrowser {
                state: Arc::clone(&browser_state),
            }),
            Box::new(CounterEntropy::new()),
            Box::new(ManualClock::new(Moment::ZERO)),
        );
        let config = IdentityConfig::new(
            "http://127.0.0.1:18080/",
            "synthetic-public-client".to_owned(),
            "/callback".to_owned(),
            Duration::from_secs(10),
        )?;
        let cancellation = CancellationSource::new();
        let bootstrap = client.authenticate(
            &config,
            &FixedAccountSession(session()?),
            session()?,
            revision()?,
            &cancellation.token(),
        )?;
        assert_eq!(browser_state.order.load(Ordering::Acquire), 3);
        assert_eq!(bootstrap.account_session_id(), session()?);
        let (directory, credential) = bootstrap.into_parts();
        assert_eq!(directory.worlds().len(), 1);
        assert_eq!(directory.characters().len(), 1);
        assert_eq!(directory.characters()[0].world_id().get(), 9);
        assert!(!format!("{credential:?}").contains("synthetic-session-credential"));
        let state = lock(&http_state);
        assert_eq!(state.calls, 3);
        assert!(state
            .debug_outputs
            .iter()
            .all(|output| !output.contains("synthetic-access")
                && !output.contains("synthetic-ticket")
                && !output.contains("synthetic-code")));
        Ok(())
    }

    #[test]
    fn independent_transactions_use_unique_state_and_verifier_material() -> Result<(), Box<dyn Error>> {
        let entropy = CounterEntropy::new();
        let redirect = Url::parse("http://127.0.0.1:49152/callback")?;
        let config = IdentityConfig::new(
            "http://127.0.0.1:18080/",
            "synthetic-public-client".to_owned(),
            "/callback".to_owned(),
            Duration::from_secs(10),
        )?;
        let first = AuthorizationTransaction::new(session()?, redirect.clone(), &entropy)?;
        let second = AuthorizationTransaction::new(session()?, redirect, &entropy)?;
        let first_url = first.authorization_url(&config)?;
        let second_url = second.authorization_url(&config)?;
        let first_state = first_url
            .query_pairs()
            .find(|(key, _)| key == "state")
            .map(|(_, value)| value.into_owned());
        let second_state = second_url
            .query_pairs()
            .find(|(key, _)| key == "state")
            .map(|(_, value)| value.into_owned());
        let first_challenge = first_url
            .query_pairs()
            .find(|(key, _)| key == "code_challenge")
            .map(|(_, value)| value.into_owned());
        let second_challenge = second_url
            .query_pairs()
            .find(|(key, _)| key == "code_challenge")
            .map(|(_, value)| value.into_owned());
        assert_ne!(first_state, second_state);
        assert_ne!(first_challenge, second_challenge);
        Ok(())
    }

    struct CancelledBinder;

    impl CallbackBinder for CancelledBinder {
        fn bind(&self, _callback_path: &str) -> Result<Box<dyn CallbackReceiver>, IdentityError> {
            Err(synthetic_identity_error())
        }
    }

    struct NoBrowser;

    impl BrowserLauncher for NoBrowser {
        fn open(&self, _authorization_url: &Url) -> Result<(), IdentityError> {
            Err(synthetic_identity_error())
        }
    }

    struct NoHttp;

    impl HttpTransport for NoHttp {
        fn post(&self, _request: HttpRequest) -> Result<HttpResponse, HttpTransportError> {
            Err(HttpTransportError::InvalidRequest)
        }
    }

    #[test]
    fn cancellation_is_observed_before_listener_or_browser_side_effects() -> Result<(), Box<dyn Error>> {
        let endpoints = PlatformEndpoints::new(
            "http://127.0.0.1:18080/",
            "http://127.0.0.1:18081/",
        )?;
        let client = IdentityClient::new(
            PlatformClient::new(endpoints, NoHttp),
            Box::new(CancelledBinder),
            Box::new(NoBrowser),
            Box::new(CounterEntropy::new()),
            Box::new(ManualClock::new(Moment::ZERO)),
        );
        let config = IdentityConfig::new(
            "http://127.0.0.1:18080/",
            "synthetic-public-client".to_owned(),
            "/callback".to_owned(),
            Duration::from_secs(10),
        )?;
        let cancellation = CancellationSource::new();
        assert!(cancellation.cancel());
        let error = client
            .authenticate(
                &config,
                &FixedAccountSession(session()?),
                session()?,
                revision()?,
                &cancellation.token(),
            )
            .err()
            .ok_or("expected cancellation")?;
        assert_eq!(error.kind(), IdentityErrorKind::Cancelled);
        Ok(())
    }

    struct SingleResponse {
        response: Mutex<Option<HttpResponse>>,
    }

    impl HttpTransport for SingleResponse {
        fn post(&self, _request: HttpRequest) -> Result<HttpResponse, HttpTransportError> {
            lock(&self.response)
                .take()
                .ok_or(HttpTransportError::InvalidRequest)
        }
    }

    fn token_exchange() -> Result<TokenExchange, Box<dyn Error>> {
        Ok(TokenExchange {
            client_id: "synthetic-public-client".to_owned(),
            redirect_uri: Url::parse("http://127.0.0.1:49152/callback")?,
            code: SecretString::new("synthetic-code".to_owned())?,
            verifier: SecretString::new(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~".to_owned(),
            )?,
        })
    }

    #[test]
    fn strict_token_boundary_rejects_unknown_trailing_redirect_and_cache_failures() -> Result<(), Box<dyn Error>> {
        let cases = [
            HttpResponse::new(
                200,
                Some(JSON.to_owned()),
                Some(CACHE.to_owned()),
                Some("no-cache".to_owned()),
                None,
                br#"{"token_type":"Bearer","expires_in":300,"access_token":"a","refresh_token":"r","unknown":true}"#.to_vec(),
            )?,
            HttpResponse::new(
                200,
                Some(JSON.to_owned()),
                Some(CACHE.to_owned()),
                Some("no-cache".to_owned()),
                None,
                br#"{"token_type":"Bearer","expires_in":300,"access_token":"a","refresh_token":"r"}{}"#.to_vec(),
            )?,
            HttpResponse::new(
                302,
                Some(JSON.to_owned()),
                Some(CACHE.to_owned()),
                Some("no-cache".to_owned()),
                Some("https://example.invalid/redirect".to_owned()),
                Vec::new(),
            )?,
            HttpResponse::new(
                200,
                Some(JSON.to_owned()),
                None,
                None,
                None,
                br#"{"token_type":"Bearer","expires_in":300,"access_token":"a","refresh_token":"r"}"#.to_vec(),
            )?,
        ];
        for response in cases {
            let endpoints = PlatformEndpoints::new(
                "http://127.0.0.1:18080/",
                "http://127.0.0.1:18081/",
            )?;
            let client = PlatformClient::new(
                endpoints,
                SingleResponse {
                    response: Mutex::new(Some(response)),
                },
            );
            assert!(client.exchange_authorization_code(token_exchange()?).is_err());
        }
        Ok(())
    }

    struct MutableSession {
        active: Mutex<Option<AccountSessionId>>,
    }

    impl ActiveAccountSession for MutableSession {
        fn active_account_session(&self) -> Option<AccountSessionId> {
            *lock(&self.active)
        }
    }

    #[test]
    fn stale_generation_is_rejected_without_network_work() -> Result<(), Box<dyn Error>> {
        let sessions = MutableSession {
            active: Mutex::new(None),
        };
        let endpoints = PlatformEndpoints::new(
            "http://127.0.0.1:18080/",
            "http://127.0.0.1:18081/",
        )?;
        let client = IdentityClient::new(
            PlatformClient::new(endpoints, NoHttp),
            Box::new(CancelledBinder),
            Box::new(NoBrowser),
            Box::new(CounterEntropy::new()),
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
                &sessions,
                session()?,
                revision()?,
                &cancellation.token(),
            )
            .err()
            .ok_or("expected stale generation")?;
        assert_eq!(error.kind(), IdentityErrorKind::StaleGeneration);
        Ok(())
    }
}
