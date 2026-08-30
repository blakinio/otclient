# 2026-08-30 V5 terminal pre-action provenance readability failure

## Terminal identity

- trusted main: `d1ce0ad811cf6a4a5a3466f7e5af045f39acab31`;
- owner admission comment: `5468621219`;
- exact V5 trigger comment: `5469017445`;
- one-time label: `field6-v5-5469017445`;
- workflow run: `33314713078`, attempt `1`;
- live job: `99265883209`;
- runner: `molehill-otclient-v5-01` / Actions Runner `2.337.0`.

## First failing boundary

`Prove independent clean guest provenance` failed with:

`PermissionError: [Errno 13] Permission denied: '/etc/otclient-field6-runner-provenance'`

The file was intentionally root-owned but had mode `0600`. That satisfied non-writability but made it unreadable to the unprivileged runner account executing the workflow. The next generation must use root-owned runner-readable mode `0644` while retaining no group/world write bits.

## No physical action

The following steps were SKIPPED: trusted-main checkout, live-admission proof, package materialization, owner-authorization consumption, secret-bearing capture, scalar validation and evidence upload. Therefore the authoritative terminal state is:

```yaml
physical_action_count: 0
login_submit_count: 0
FIELD6_VALUE: UNKNOWN
owner_authorization_consumed: false
credentials_exposed_to_capture: false
official_client_started: false
```

The final cleanup step also failed because checkout never occurred, so `.github/scripts/track_a_current_client_package_acquire.sh` was absent. No package-acquisition state had been created before that step.

## Destruction proof

The ephemeral runner completed with failure, removed `.credentials` and `.runner`, deregistered from GitHub, and exited without retry. WSL registry readback uniquely mapped `OTClientV5Clean` to `C:\Users\barte\OTClientV5Clean`; that exact distro was terminated/unregistered and readback confirmed its destruction.

V5 is terminal and must never be rerun. A new V6 generation is required even though the allowed login action was not consumed.
