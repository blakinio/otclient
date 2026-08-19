# Track A current-client fence regression inventory

```yaml
current_version_token: '15.32'
current_size: 52109920
current_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
historical_size: 51965216
historical_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

| Case | Expected result |
|---|---|
| exact current size + exact current SHA | PASS identity fence only |
| historical size + historical SHA as current runtime | REFUSE current identity; preserve historical evidence |
| current size + wrong SHA | REFUSE |
| current SHA + wrong size | REFUSE |
| unknown/unverifiable executable | REFUSE |
| old offsets/helpers/profile on current SHA | REFUSE until exact-build re-proof |
| current identity but no effect authority | REFUSE login/input/mutation/transactions |

Deterministic validation is enforced by `.github/scripts/test_track_a_agent_runtime_governance.py` plus syntax/YAML workflow checks.
