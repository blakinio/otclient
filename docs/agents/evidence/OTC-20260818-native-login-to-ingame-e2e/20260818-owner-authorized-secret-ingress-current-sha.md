# Current-SHA owner authorization — bounded one-shot native auth

Task: `OTC-20260818-native-login-to-ingame-e2e`
PR: `#528`
Date: `2026-08-18`

The owner explicitly instructed the continuation agent to proceed with the already-configured `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` GitHub Secrets rather than requiring manual TTY entry.

This authorization is bounded to this task and this one-shot native-auth ingress only. Secret values must not be printed, persisted as plaintext, placed in argv, committed, uploaded as artifacts, or returned to the model. The intended transport remains: local secret source -> sealed anonymous memfd -> `SCM_RIGHTS` -> exact-SHA experimental native-auth helper -> named Qt invocation of `onRequestLoginWithCredentials(QString,QString)`.

Current live exact client fence revalidated from the persistent Track A runtime:

```text
size=52109920
sha256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
TGameClient primary vptr=0x30adce8
TGameClient local QMeta method count=44
cold-auth local ordinal=17
cold-auth target=0xd196f0
cold-auth fence32=488b5110488b71084883c4485b5de93d609cff0f1f440000488bbfa009000048
fence32_sha256=5d557de0eb8cfa4ba58d5021c7f5b66be40bf84e6deb05ebfad4dd72380c1056
```

The 32-byte fence was independently checked to occur exactly once in the live exact executable and the `qt_static_metacall` jump table entry for ordinal 17 resolves to `0xd196f0`.

Current `main` at authorization refresh: `ebbb36f50076ff4072c7218e302614c1dfea00b1`.

No GUI credential entry, OCR, coordinate automation, TLS weakening, auth bypass, fabricated callback, or server-response spoofing is authorized.