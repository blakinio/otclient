# 2026-08-26 encrypted producer stayloggedin A/B result

Task: `OTC-20260813-tibia-global-login-lab`
Track: `OTCLIENT-GLOBAL-LOGIN` / Track B only
Canonical PR: #284
Repository: `blakinio/otclient`

## Fresh source-of-truth snapshot

At this checkpoint:

- live `main`: `8085b40698d409bbacba3460001e8ddca4f6c84f`;
- repair head: `6c5a0baa24241dacb5ada6684715e3aad248d515`;
- PR #284 remains the existing canonical branch/PR;
- Molehill was executable during the repair and producer observation.

Do not reuse these SHAs or runtime claims later without fresh validation.

## Material repair

Commit `6c5a0baa24241dacb5ada6684715e3aad248d515` restored the encrypted login request to the historically proven `stayloggedin: True` semantic and finished a closed redacted rejection classifier. The contract test was RED before the request change and GREEN after it.

The test also requires that the encrypted emitter never promotes a `devicecookie`, never prints raw `errorMessage`, and can emit only a closed `LAB_ENCRYPTED_HANDOFF_ERROR_CATEGORY` marker for a rejected response.

## Exact producer result

Automatic encrypted workflow run `32966019711`, job `98168611634`, executed once on exact head `6c5a0baa24241dacb5ada6684715e3aad248d515`.

Fixed non-secret markers were:

```text
LAB_ENCRYPTED_HANDOFF_WARP_READY=true
LAB_ENCRYPTED_HANDOFF_ASSET_IDENTIFIER_READY=true
LAB_ENCRYPTED_HANDOFF_HTTP_LOGIN_200=true
LAB_ENCRYPTED_HANDOFF_ERROR_CODE=7
LAB_ENCRYPTED_HANDOFF_ERROR_CATEGORY=other
```

`LAB_ENCRYPTED_HANDOFF_PLAINTEXT_VALID` and `LAB_ENCRYPTED_HANDOFF_CIPHERTEXT_READY` were not reached. The ciphertext upload step was skipped and the run has zero artifacts.

The legacy `Tibia Global Login Lab` run on this head was skipped by the canonical-branch guard. CI on this head completed successfully.

FACT: restoring `stayloggedin: True` did not eliminate the service-level rejection.

UNKNOWN: the authoritative CipSoft meaning of `errorCode=7`. The closed classifier's `other` result is not an account/auth/service diagnosis and must not be promoted into one.

## Public discriminator research

A fresh public search still found no authoritative CipSoft mapping from numeric login-service `errorCode=7` to a specific cause. Official Tibia support documents authenticator requirements and temporary login blocking after repeated incorrect password/token attempts, but does not bind those states to numeric code 7.

Therefore no further protocol/account diagnosis is justified from the numeric code alone.

## Current blocker and next action

`GAME_START=false` / `IN_GAME=false`.

Current blocker: the owner-authorized hosted login boundary returns HTTP 200 but rejects the request before session/playdata handoff with stable redacted `errorCode=7`; the only proven request-semantic delta (`stayloggedin`) has now been eliminated, and the safe classifier yields no more specific category.

Do not run a fourth unchanged or classifier-only login retry. Before any new secret-bearing producer attempt, require genuinely new evidence that can distinguish or remove the login rejection without exposing raw credentials/session/error text, for example an owner-side successful official-client login/account-state confirmation or an authoritative current login-service contract/mapping.

Once the hosted producer again reaches a valid session/playdata response, resume the existing flow only: create one encrypted `handoff.cms`, consume it on Molehill, freshly verify/stage current 15.32 assets, and perform one bounded OTClient game-login. If that game-server result is structured `0x14`, stop identical retry and require promoted current-build wire-writer evidence.
