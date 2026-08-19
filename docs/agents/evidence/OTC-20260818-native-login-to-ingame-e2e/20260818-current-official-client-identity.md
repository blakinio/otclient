# Track A native-login E2E — current official Linux client identity

Task: `OTC-20260818-native-login-to-ingame-e2e`  
PR: `#528`  
Date: `2026-08-18`

## Trigger

After noVNC observability was restored, the live official client displayed the version gate:

```text
Your client version is too old.
Restart Tibia to update your client.
```

No account identifier or other credential visible in the UI is reproduced in this evidence.

## Read-only current-client probe

The current official package was resolved from CipSoft's current Linux package manifest without modifying the running client, its package, authentication state, or Secrets.

Workflow:

```text
run: 32140385842
job: 95721374178
head: b0bbb35d0c4c814285e140c4d25b3532783d2fb8
```

Preconditions and authority:

```text
TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true
TRACK_A_CANONICAL_LEASE_GENERATION=16
TRACK_A_CANONICAL_GATE_B=PASS
CURRENT_PROBE_OLD_CLIENT_PID=30067
CURRENT_PROBE_OLD_CLIENT_DISPLAY=:99
```

The currently running old exact client remains:

```text
version=15.32.df7b29
size=51965216
sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

The official current `client.lzma` manifest entry was downloaded through the already-admitted task-owned WARP/SOCKS path, its packed hash was verified, and the CipSoft LZMA envelope was decoded only in a temporary runner directory.

Exact current official binary identity:

```text
packed_client_lzma_sha256=1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked_client_sha256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
unpacked_client_size=52109920
CURRENT_PROBE_DIFFERS_FROM_GEN16=true
CURRENT_PROBE_VERSION_STRINGS=15.32,11.25
```

The public version strings alone are not promoted into a new exact build suffix. The new SHA-256 and size are the authoritative binary identity until a stronger build-identifier provenance is recovered.

Post-probe authority remained intact:

```text
TRACK_A_CANONICAL_GATE_B=PASS
TRACK_A_CANONICAL_LEASE_GENERATION=16
CURRENT_PROBE_SECRET_ACCESS=false
CURRENT_PROBE_CLIENT_MUTATION=false
CURRENT_PROBE_RUNTIME_RESTART=false
CURRENT_PROBE_RESULT=PASS
```

## Causal conclusion

### FACT

The current official Linux client binary differs from the live gen16 binary by both SHA-256 and size. The live client itself reports that its version is too old.

### CONSEQUENCE

The previous secret-bearing native-auth attempt is not evidence that the credentials were rejected. The live version gate is a concrete precondition failure before a successful current-service login can be expected.

Do not retry account credentials against the old exact binary.

Do not reuse old exact-client addresses, QMeta fences, vptr offsets, character-controller offsets, or the old native-auth helper against the new binary without fresh proof.

## Required migration sequence

```text
1. Preserve gen16 evidence and current authority.
2. Perform a reviewed canonical teardown/unregister of the old exact runtime.
3. Update the official package through the legitimate CipSoft update/launcher path.
4. Fence the installed binary to:
     size=52109920
     sha256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
5. Re-prove the native authentication and character-login boundaries for that exact binary.
6. Rebuild/revalidate the experimental native-auth helper against the new exact binary.
7. Bootstrap/re-register a fresh canonical runtime and re-prove Gate B.
8. Restore noVNC presentation to the new active DISPLAY.
9. Only then perform another bounded GitHub-Secrets authentication attempt.
```

## Terminal checkpoint

```text
CURRENT_OFFICIAL_CLIENT_RESOLVED=true
OLD_CLIENT_TOO_OLD=true
OLD_CLIENT_SHA256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
CURRENT_OFFICIAL_CLIENT_SHA256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
CURRENT_OFFICIAL_CLIENT_SIZE=52109920
CURRENT_OFFICIAL_PACKED_SHA256=1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
SECRET_RETRY_BEFORE_UPDATE=false
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=NO
CAUSAL_PROOF=INCOMPLETE
```
