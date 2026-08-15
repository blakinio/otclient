# Track A canonical HOME support-state metadata — 2026-08-15

Task: `OTC-20260815-track-a-loader-diagnostic`
Track: `official-client-re`
Consumer: PR #303
Classification: `FACT / metadata-only candidate`

## Evidence

Workflow run `31894272272`, job `95035023704`, exact-client SHA `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`, runner `synology-otclient-01`.

The workflow did not launch the client, read credentials, read cache/config file contents, signal processes or touch displays/ports. It enumerated only relevant immediate canonical HOME metadata and aggregate directory statistics.

Observed canonical HOME state:

```text
.config: absent
.cache: present
.cache/CipSoft GmbH: directory, 4 files, aggregate 6937 bytes, mode 0755
```

No other immediate `.config`/`.cache` entry matching `Tibia|CipSoft|QtWebEngine|QtProject|Qt6` was observed.

## Disposition

This is the first concrete canonical-HOME support-state difference not reproduced by PR #303's fresh generation HOME after the already-falsified package-path/crashdump/Xvfb-cwd hypotheses.

It is only a **candidate**, not a fix. The four cache payloads were intentionally not read or copied, so their purpose and sensitivity remain UNKNOWN. They must not be imported into a task-owned HOME unless a separate fail-closed classification proves they contain no account/session/cookie/credential material and establishes why they are required for window creation.

The safer next runtime discriminator remains sanitized Qt runtime diagnostics (`QT_DEBUG_PLUGINS=1` and all mapped/unmapped X11 windows/extensions). Cache classification should be used only if that runtime evidence points to canonical cache lookup/state as causal.
