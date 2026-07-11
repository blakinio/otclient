# Description

<!-- Summarize the change, its purpose, and the user-visible impact. -->

## Problem and root cause

<!-- What problem does this solve? What caused it? For non-bug changes, describe the motivation. -->

## Behavior before the change

<!-- Describe the previous behavior. Use "Not applicable" with a reason when appropriate. -->

## Behavior after the change

<!-- Describe the expected behavior after this PR. -->

## Related issue

<!-- Use "Fixes #123", "Relates to #123", or explain why there is no issue. -->

## Type of change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Refactoring or performance improvement
- [ ] Build, CI, or dependency change
- [ ] Documentation or repository maintenance

## Changed components

- [ ] C++ source (`src/`)
- [ ] Lua modules or mods (`modules/`, `mods/`)
- [ ] UI, styles, or images
- [ ] Protocol or Canary integration
- [ ] Client assets or runtime data (`data/`, `bin/`)
- [ ] Build, packaging, Docker, or dependencies
- [ ] CI or repository configuration (`.github/`)
- [ ] Documentation
- [ ] Other: <!-- describe -->

## Compatibility and test environment

- Canary version/tag/commit:
- Client protocol version:
- Operating system and version:
- OTClient commit/build configuration:
- Assets and source (original/customized):
- Relevant feature flags or server changes:

## Reproduction steps

<!-- Required for bug fixes. Provide a minimal, numbered reproduction. Otherwise explain why this is not applicable. -->

1.
2.
3.

## Tests performed

<!-- List exact commands and manual scenarios, with results. Explain any missing coverage. -->

- [ ] Reproduction verified before the change
- [ ] Windows build/test
- [ ] Linux build/test
- [ ] Lua/format/static checks relevant to the change
- [ ] Protocol behavior tested with the Canary and protocol versions above
- [ ] Documentation-only or governance-only change; native build not required

### Client-assets verification, if applicable

<!-- Required when client-assets installation is touched. State exact versions and observed runtime load behavior. -->

- Tested final install paths:
  - `data/things/<version>/`:
  - `data/sounds/<version>/`:
  - runtime extras (for example `bin/*`):
- Expected runtime load behavior from the OTC-standard paths:
- [ ] Secure defaults remain `strictManifestSha256 = true` and `allowRawFallbackHashMismatch = false`, or the exception is justified above
- [ ] Windows/Linux extraction remains functional and Android does not require unsupported `libarchive` linkage

## Regression risk

<!-- Rate the risk (low/medium/high), identify affected flows, and describe rollback or mitigation. -->

## Screenshots and logs

<!-- Add screenshots, recordings, sanitized logs, or crash traces when relevant. Do not include credentials or private server data. -->

## Checklist

- [ ] This PR contains one logical change
- [ ] I have performed a self-review and removed unrelated changes
- [ ] I have included a reproducible bug case or explained why it is unavailable
- [ ] I have documented the Canary version, client protocol, OS, and assets, or marked them not applicable with a reason
- [ ] I have added or updated tests where practical and reported all test results
- [ ] I have updated relevant documentation
- [ ] I have not added secrets, credentials, private data, or local environment files
- [ ] I have reviewed the CI results and have not bypassed required checks
