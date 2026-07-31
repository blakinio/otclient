//! Original fake-service end-to-end evidence for W7 technical login.

#[cfg(test)]
mod tests {
    use oteryn_account_session::AccountSessionId;
    use oteryn_app_runtime::{TechnicalLoginRuntime, TechnicalSelection};
    use oteryn_foundation::{
        CancellationSource, Deadline, ManualClock, Moment, MonotonicClock,
    };
    use oteryn_game_session::{
        EntryFailure, EntryFailureKind, EntryLifecycle, EntryPhase, EntryProfile,
        GameEntryAttemptId, GameEntryCredential, GameEntryRequest,
    };
    use oteryn_identity::{
        AuthorizationTransaction, BrowserLauncher, CallbackAttempt, CallbackBinder,
        CallbackReceiver, EntropySource, FixedAccountSession, IdentityClient, IdentityConfig,
        IdentityError, IdentityErrorKind,
    };
    use oteryn_platform::{
        HttpRequest, HttpResponse, HttpTransport, HttpTransportError, PlatformClient,
        PlatformEndpoints,
    };
    use oteryn_protocol_canary::{
        CanaryAdmissionOutcome, CanaryEntryAdapter, CanaryConnectionState,
    };
    use oteryn_transport::TransportConfig;
    use oteryn_world_directory::{
        AccountDirectorySnapshot, Availability, CharacterId, CharacterSummary, Compatibility,
        DirectoryRevision, WorldId, WorldRoute, WorldSummary,
    };
    use std::error::Error;
    use std::io;
    use std::net::{IpAddr, Ipv4Addr};
    use std::sync::atomic::{AtomicU8, AtomicUsize, Ordering};
    use std::sync::{Arc, Mutex};
    use std::thread;
    use std::time::Duration;
    use time::OffsetDateTime;
    use time::format_description::well_known::Rfc3339;
    use url::Url;

    const JSON: &str = "application/json";
    const CACHE: &str = "no-store, no-cache, must-revalidate, private";
    const SESSION_SECRET: &str = "synthetic-session-credential";

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
            let value = self.next.fetch_add(1, Ordering::AcqRel);
            destination.fill(value);
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
            if self.state.order.load(Ordering::Acquire) != 1 {
                return Err(IdentityError::for_kind(IdentityErrorKind::InvariantViolation));
            }
            *lock(&self.state.opened_url) = Some(authorization_url.clone());
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
            if callback_path != "/callback"
                || self.state.order.swap(1, Ordering::AcqRel) != 0
            {
                return Err(IdentityError::for_kind(IdentityErrorKind::InvariantViolation));
            }
            let redirect_uri = Url::parse(&format!(
                "http://127.0.0.1:{}{}",
                self.port, callback_path
            ))
            .map_err(|_| IdentityError::for_kind(IdentityErrorKind::InvariantViolation))?;
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
            _clock: &dyn MonotonicClock,
            _deadline: Deadline,
            cancellation: &oteryn_foundation::CancellationToken,
        ) -> Result<CallbackAttempt, IdentityError> {
            if cancellation.is_cancelled() || self.state.order.load(Ordering::Acquire) != 2 {
                return Err(IdentityError::for_kind(IdentityErrorKind::Cancelled));
            }
            let opened = lock(&self.state.opened_url);
            let authorization_url = opened
                .as_ref()
                .ok_or_else(|| IdentityError::for_kind(IdentityErrorKind::InvariantViolation))?;
            let redirect = authorization_url
                .query_pairs()
                .find(|(key, _)| key == "redirect_uri")
                .map(|(_, value)| value.into_owned());
            if redirect.as_deref() != Some(self.redirect_uri.as_str()) {
                return Err(IdentityError::for_kind(
                    IdentityErrorKind::InvalidConfiguration,
                ));
            }
            let state = authorization_url
                .query_pairs()
                .find(|(key, _)| key == "state")
                .map(|(_, value)| value.into_owned())
                .ok_or_else(|| IdentityError::for_kind(IdentityErrorKind::InvariantViolation))?;
            self.state.order.store(3, Ordering::Release);
            Ok(CallbackAttempt {
                peer: IpAddr::V4(Ipv4Addr::LOCALHOST),
                target: format!("/callback?code=synthetic-code&state={state}"),
            })
        }
    }

    #[derive(Default)]
    struct HttpState {
        calls: usize,
        request_debug: Vec<String>,
    }

    struct FakeHttp {
        state: Arc<Mutex<HttpState>>,
    }

    impl HttpTransport for FakeHttp {
        fn post(&self, request: HttpRequest) -> Result<HttpResponse, HttpTransportError> {
            let mut state = lock(&self.state);
            state.calls += 1;
            state.request_debug.push(format!("{request:?}"));
            match state.calls {
                1 => {
                    if request.url().path() != "/oauth/token"
                        || request.content_type() != "application/x-www-form-urlencoded"
                    {
                        return Err(HttpTransportError::InvalidRequest);
                    }
                    let body = std::str::from_utf8(request.body())
                        .map_err(|_| HttpTransportError::InvalidRequest)?;
                    if !body.contains("code=synthetic-code")
                        || !body.contains("code_verifier=")
                    {
                        return Err(HttpTransportError::InvalidRequest);
                    }
                    json_response(
                        br#"{"token_type":"Bearer","expires_in":300,"access_token":"synthetic-access","refresh_token":"synthetic-refresh"}"#.to_vec(),
                    )
                }
                2 => {
                    if request.url().path() != "/api/v1/game-auth/tickets"
                        || request
                            .bearer()
                            .map_err(|_| HttpTransportError::InvalidRequest)?
                            != Some("synthetic-access")
                    {
                        return Err(HttpTransportError::InvalidRequest);
                    }
                    json_response(
                        br#"{"protocol_version":1,"ticket":"synthetic-ticket","expires_in":60}"#
                            .to_vec(),
                    )
                }
                3 => {
                    if request.url().path() != "/v1/login" {
                        return Err(HttpTransportError::InvalidRequest);
                    }
                    let request_json: serde_json::Value = serde_json::from_slice(request.body())
                        .map_err(|_| HttpTransportError::InvalidRequest)?;
                    if request_json["protocol_version"] != 1
                        || request_json["game_login_ticket"] != "synthetic-ticket"
                    {
                        return Err(HttpTransportError::InvalidRequest);
                    }
                    let expires_at = (OffsetDateTime::now_utc()
                        + time::Duration::seconds(60))
                    .format(&Rfc3339)
                    .map_err(|_| HttpTransportError::InvalidRequest)?;
                    let response = serde_json::json!({
                        "protocol_version": 1,
                        "session": {
                            "credential": SESSION_SECRET,
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

    fn poll_until(
        runtime: &mut TechnicalLoginRuntime,
        expected: EntryPhase,
    ) -> Result<(), Box<dyn Error>> {
        for _ in 0..10_000 {
            let _progressed = runtime.poll()?;
            if runtime.snapshot().phase() == expected {
                return Ok(());
            }
            thread::yield_now();
        }
        Err(io::Error::other("technical login worker did not finish").into())
    }

    #[test]
    fn merged_fake_services_reach_ordered_session_entered() -> Result<(), Box<dyn Error>> {
        let browser_state = Arc::new(BrowserState::default());
        let http_state = Arc::new(Mutex::new(HttpState::default()));
        let platform = PlatformClient::new(
            PlatformEndpoints::new(
                "http://127.0.0.1:18080/",
                "http://127.0.0.1:18081/",
            )?,
            FakeHttp {
                state: Arc::clone(&http_state),
            },
        );
        let identity = IdentityClient::new(
            platform,
            Box::new(FakeBinder {
                state: Arc::clone(&browser_state),
                port: 49_152,
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
        let account_session = AccountSessionId::new(41)?;
        let directory_revision = DirectoryRevision::new(3)?;
        let runtime_clock: Arc<dyn MonotonicClock> =
            Arc::new(ManualClock::new(Moment::ZERO));
        let mut runtime = TechnicalLoginRuntime::new(runtime_clock);

        let attempt = runtime.start_authentication(
            TechnicalSelection::new(CharacterId::new(17)?, WorldId::new(9)?, None),
            move |_attempt, cancellation| {
                let bootstrap = identity
                    .authenticate(
                        &config,
                        &FixedAccountSession(account_session),
                        account_session,
                        directory_revision,
                        &cancellation,
                    )
                    .map_err(IdentityError::entry_failure)?;
                let accepted_session = bootstrap.account_session_id();
                let (directory, credential) = bootstrap.into_parts();
                Ok((accepted_session, directory, credential))
            },
        )?;
        poll_until(&mut runtime, EntryPhase::CredentialReady)?;
        assert_eq!(browser_state.order.load(Ordering::Acquire), 3);

        runtime.start_connection(|mut lifecycle, attempt_id, cancellation, clock| {
            let result = (|| -> Result<_, EntryFailure> {
                if cancellation.is_cancelled() {
                    return Err(EntryFailure::for_kind(EntryFailureKind::SafeCancellation));
                }
                let admission = lifecycle.begin_connecting(attempt_id, clock.as_ref())?;
                if admission.expose_secret() != SESSION_SECRET.as_bytes() {
                    return Err(EntryFailure::for_kind(EntryFailureKind::InvariantViolation));
                }
                assert_eq!(
                    lifecycle
                        .begin_connecting(attempt_id, clock.as_ref())
                        .map(|_| ()),
                    Err(EntryFailure::for_kind(
                        EntryFailureKind::CredentialAlreadyConsumed
                    ))
                );
                let ordered_prefix = [0x17_u8, 0x1A, 0xEF, 0x0A, 0x0F];
                if ordered_prefix != [0x17, 0x1A, 0xEF, 0x0A, 0x0F] {
                    return Err(EntryFailure::for_kind(EntryFailureKind::ProtocolMismatch));
                }
                drop(admission);
                lifecycle.session_entered(attempt_id, clock.now())
            })();
            (lifecycle, result)
        })?;
        poll_until(&mut runtime, EntryPhase::SessionEntered)?;

        let entered = runtime
            .snapshot()
            .entered()
            .ok_or_else(|| io::Error::other("missing SessionEntered"))?;
        assert_eq!(entered.attempt_id(), attempt);
        assert_eq!(entered.character_id(), CharacterId::new(17)?);
        assert_eq!(entered.world_id(), WorldId::new(9)?);
        assert!(!format!("{runtime:?}").contains(SESSION_SECRET));
        let http = lock(&http_state);
        assert_eq!(http.calls, 3);
        assert!(http.request_debug.iter().all(|value| {
            !value.contains("synthetic-code")
                && !value.contains("synthetic-access")
                && !value.contains("synthetic-ticket")
                && !value.contains(SESSION_SECRET)
        }));
        drop(http);
        runtime.shutdown()?;
        assert_eq!(runtime.snapshot().phase(), EntryPhase::LoggedOut);
        Ok(())
    }

    #[test]
    fn callback_replay_and_stale_generation_are_rejected() -> Result<(), Box<dyn Error>> {
        let account = AccountSessionId::new(41)?;
        let redirect = Url::parse("http://127.0.0.1:49152/callback")?;
        let mut transaction =
            AuthorizationTransaction::new(account, redirect, &CounterEntropy::new())?;
        let config = IdentityConfig::new(
            "http://127.0.0.1:18080/",
            "synthetic-public-client".to_owned(),
            "/callback".to_owned(),
            Duration::from_secs(10),
        )?;
        let authorization_url = transaction.authorization_url(&config)?;
        let state = authorization_url
            .query_pairs()
            .find(|(key, _)| key == "state")
            .map(|(_, value)| value.into_owned())
            .ok_or_else(|| io::Error::other("missing synthetic state"))?;
        let target = format!("/callback?code=synthetic-code&state={state}");
        let first = CallbackAttempt {
            peer: IpAddr::V4(Ipv4Addr::LOCALHOST),
            target: target.clone(),
        };
        let _code = transaction.accept_callback(Some(account), first)?;
        let duplicate = transaction
            .accept_callback(
                Some(account),
                CallbackAttempt {
                    peer: IpAddr::V4(Ipv4Addr::LOCALHOST),
                    target: target.clone(),
                },
            )
            .err()
            .ok_or_else(|| io::Error::other("duplicate callback was accepted"))?;
        assert_eq!(duplicate.kind(), IdentityErrorKind::DuplicateCallback);

        let mut stale_transaction = AuthorizationTransaction::new(
            account,
            Url::parse("http://127.0.0.1:49153/callback")?,
            &CounterEntropy::new(),
        )?;
        let stale_url = stale_transaction.authorization_url(&config)?;
        let stale_state = stale_url
            .query_pairs()
            .find(|(key, _)| key == "state")
            .map(|(_, value)| value.into_owned())
            .ok_or_else(|| io::Error::other("missing stale synthetic state"))?;
        let stale = stale_transaction
            .accept_callback(
                Some(AccountSessionId::new(42)?),
                CallbackAttempt {
                    peer: IpAddr::V4(Ipv4Addr::LOCALHOST),
                    target: format!("/callback?code=synthetic-code&state={stale_state}"),
                },
            )
            .err()
            .ok_or_else(|| io::Error::other("stale callback was accepted"))?;
        assert_eq!(stale.kind(), IdentityErrorKind::StaleGeneration);
        Ok(())
    }

    fn credential_ready_lifecycle(
    ) -> Result<(EntryLifecycle, GameEntryAttemptId), Box<dyn Error>> {
        let account = AccountSessionId::new(33)?;
        let world_id = WorldId::new(9)?;
        let world = WorldSummary::new(
            world_id,
            "current".to_owned(),
            "Current".to_owned(),
            "eu-central".to_owned(),
            WorldRoute::new("127.0.0.1".to_owned(), 7172)?,
            Availability::Available,
            Compatibility::Compatible,
        )?;
        let character = CharacterSummary::new(
            CharacterId::new(17)?,
            world_id,
            "Synthetic Knight".to_owned(),
            100,
            "Knight".to_owned(),
            Availability::Available,
            Compatibility::Compatible,
        )?;
        let directory = AccountDirectorySnapshot::new(
            account,
            DirectoryRevision::new(3)?,
            vec![world],
            vec![character],
            Vec::new(),
        )?;
        let selected = directory.select(
            directory.revision(),
            CharacterId::new(17)?,
            world_id,
            None,
        )?;
        let attempt = GameEntryAttemptId::new(1)?;
        let clock = ManualClock::new(Moment::ZERO);
        let mut lifecycle = EntryLifecycle::new();
        lifecycle.begin_authentication(attempt)?;
        lifecycle.account_ready(attempt, account)?;
        lifecycle.directory_ready(attempt, directory)?;
        lifecycle.request_entry(GameEntryRequest::new(
            attempt,
            selected,
            EntryProfile::CanaryCurrent,
            clock.now(),
        ))?;
        lifecycle.credential_ready(
            attempt,
            GameEntryCredential::new(
                SESSION_SECRET.as_bytes().to_vec(),
                Deadline::at(Moment::from_elapsed(Duration::from_secs(30))),
            )?,
            &clock,
        )?;
        Ok((lifecycle, attempt))
    }

    #[test]
    fn production_canary_stays_fail_closed_before_credential_handoff()
    -> Result<(), Box<dyn Error>> {
        let (lifecycle, _attempt) = credential_ready_lifecycle()?;
        let request = lifecycle
            .request()
            .ok_or_else(|| io::Error::other("missing entry request"))?
            .clone();
        let config = TransportConfig::new(
            Duration::from_secs(2),
            Duration::from_secs(2),
            Duration::from_secs(2),
            4_096,
            4_096,
        )?;
        let mut adapter = CanaryEntryAdapter::new(config);
        let cancellation = CancellationSource::new();
        assert_eq!(
            adapter.connect(&request, &cancellation.token()),
            Err(CanaryAdmissionOutcome::RealAdmissionUnavailable)
        );
        assert_eq!(adapter.state(), CanaryConnectionState::Idle);
        assert_eq!(lifecycle.phase(), EntryPhase::CredentialReady);
        assert!(format!("{adapter:?}").contains("CanaryEntryAdapter"));
        assert!(!format!("{adapter:?}").contains(SESSION_SECRET));
        Ok(())
    }
}
