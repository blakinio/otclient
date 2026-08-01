from pathlib import Path


path = Path("oteryn-client/tests/integration/technical-login/src/lib.rs")
source = path.read_text(encoding="utf-8")

replacements = [
    (
        '''            Ok(CallbackAttempt {
                peer: IpAddr::V4(Ipv4Addr::LOCALHOST),
                target: format!("/callback?code=synthetic-code&state={state}"),
            })
''',
        '''            CallbackAttempt::new(
                IpAddr::V4(Ipv4Addr::LOCALHOST),
                format!("/callback?code=synthetic-code&state={state}"),
            )
''',
    ),
    (
        '''        let first = CallbackAttempt {
            peer: IpAddr::V4(Ipv4Addr::LOCALHOST),
            target: target.clone(),
        };
''',
        '''        let first = CallbackAttempt::new(
            IpAddr::V4(Ipv4Addr::LOCALHOST),
            target.clone(),
        )?;
''',
    ),
    (
        '''                CallbackAttempt {
                    peer: IpAddr::V4(Ipv4Addr::LOCALHOST),
                    target: target.clone(),
                },
''',
        '''                CallbackAttempt::new(
                    IpAddr::V4(Ipv4Addr::LOCALHOST),
                    target.clone(),
                )?,
''',
    ),
    (
        '''                CallbackAttempt {
                    peer: IpAddr::V4(Ipv4Addr::LOCALHOST),
                    target: format!("/callback?code=synthetic-code&state={stale_state}"),
                },
''',
        '''                CallbackAttempt::new(
                    IpAddr::V4(Ipv4Addr::LOCALHOST),
                    format!("/callback?code=synthetic-code&state={stale_state}"),
                )?,
''',
    ),
]

for old, new in replacements:
    if source.count(old) != 1:
        raise SystemExit("technical-login callback fixture anchor mismatch")
    source = source.replace(old, new, 1)

path.write_text(source, encoding="utf-8")
