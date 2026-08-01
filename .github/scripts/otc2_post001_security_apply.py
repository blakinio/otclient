from pathlib import Path


path = Path("oteryn-client/tests/security/auth/src/lib.rs")
source = path.read_text(encoding="utf-8")
old = '''            Ok(CallbackAttempt {
                peer: IpAddr::V4(Ipv4Addr::LOCALHOST),
                target: format!("/callback?code=synthetic-code&state={state}"),
            })
'''
new = '''            CallbackAttempt::new(
                IpAddr::V4(Ipv4Addr::LOCALHOST),
                format!("/callback?code=synthetic-code&state={state}"),
            )
'''
if source.count(old) != 1:
    raise SystemExit("security callback fixture anchor mismatch")
path.write_text(source.replace(old, new, 1), encoding="utf-8")
