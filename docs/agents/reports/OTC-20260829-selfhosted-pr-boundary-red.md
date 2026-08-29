# OTC-20260829 self-hosted PR boundary evidence

## Scope

Hosted-only security regression for the trusted-main workflow graph. No Synology job, official Tibia client, credential, login, GUI action, process control or payload capture is authorized by this evidence package.

## Parser correction

The first scan correctly found the vulnerable canonical-lease job but also treated payload references such as `github.event.issue.pull_request` as proof of a `pull_request` event. The regression was corrected to classify explicit `github.event_name == 'issue_comment'` / other non-PR gates before interpreting payload fields.

## Causal RED

After the parser correction, hosted run `33236883246`, job `99059301992` failed on exactly one trusted-main job:

```text
TRACK_A_SELFHOSTED_PR_BOUNDARY_RED: PR-controlled self-hosted jobs: .github/workflows/tibia-official-client-re-canonical-live-lease.yml::isolated-selfhosted
```

This matches the fresh exact-head Codex security finding from PR #786.

## GREEN

The canonical lease self-hosted test now requires owner-only `workflow_dispatch`, checks out trusted `main`, disables credential persistence and proves the checkout still matches remote `main` before exercising task-owned lease state.

Exact implementation head `4a6a792f1bc2682819db08d64c24665039774b90`:

```text
Track A self-hosted PR boundary             33236911255  success
Track A canonical live controller lease     33236911337  success
  isolated-selfhosted                                      skipped
Track A agent runtime governance            33236911266  success
CI / Required                               33236911425  success
```

The repository-wide GREEN means trusted main contains no PR-triggered Synology/self-hosted job lacking an explicit event gate excluding pull requests.

## Remaining boundary

This repair prevents future PR-controlled runner contamination after merge. Historical state on the persistent runner remains a separate question. V4 field6 secret access remains forbidden until a no-secret physical clean-runner attestation/remediation proves a safe credential execution environment.
