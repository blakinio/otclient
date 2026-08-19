# TIBIA-RE-AUTH-SESSION — source producer log cross-check

```yaml
source_pr: 556
source_head: 411d0e287d08406c682ef063fb3f3f61341d9295
source_run: 32228900775
source_job: 95994337407
source_artifacts: 0
runtime_access: none
```

The coordinator independently fetched the complete successful producer job log instead of relying on the source Markdown summary.

## Exact build markers reproduced from the job log

```text
AUTHSESSION_CURRENT_PACKED_FENCE=PASS
AUTHSESSION_CURRENT_EXACT_CLIENT_SHA=PASS
AUTHSESSION_CURRENT_CLIENT_SIZE=52109920
AUTHSESSION_CURRENT_CLIENT_SHA256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
AUTHSESSION_CURRENT_ELF_BUILD_ID=d803d9695868713ef6ab0c3cf65f91212c9c6a62
AUTHSESSION_CURRENT_BUILD_ID_FENCE=PASS
AUTHSESSION_RAW_CLIENT_RETAINED=false
```

GitHub reports no uploaded artifact for run `32228900775`; the raw evidence is therefore the retained Actions job log plus the committed sanitized result, not a ZIP artifact.

## QMeta role cross-check

The source log directly reports:

```text
TLoginRequestUploader: METHODS=9; SIGNALS=8
loginSuccessful: INDEX=0

TGameClient: METHODS=44; SIGNALS=6
connectClientToGameserverWithExistingCredentials: INDEX=11
onRequestLoginWithCredentials: INDEX=17

TCharacterSelectionController: METHODS=26; SIGNALS=10
requestCharacterLogin: INDEX=0
```

Therefore, independently of target-address recovery:

```yaml
loginSuccessful_role: SIGNAL
requestCharacterLogin_role: SIGNAL
connectClientToGameserverWithExistingCredentials_role: METHOD
onRequestLoginWithCredentials_role: METHOD
```

This role distinction is mandatory in canonical promotion. A signal dispatch target is not promoted as a call-safe business implementation.

## Source target claims still gated

The source log reports target candidates `0xd196f0`, `0xd19500`, `0xd10200`, and `0xd52050`, but the coordinator does not promote them from this log alone. H1/H2 and the signal-target bindings remain subject to the preregistered strict control-flow discriminator.

No login, credentials, client execution, process-memory access or physical runtime observation was performed by this cross-check.
