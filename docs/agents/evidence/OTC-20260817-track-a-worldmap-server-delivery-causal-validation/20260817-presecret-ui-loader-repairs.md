# Worldmap causal baseline — pre-secret UI/loader repairs

Task: `OTC-20260817-track-a-worldmap-server-delivery-causal-validation`  
PR: #475  
Date: 2026-08-17

## Boundary

This record covers only deterministic failures before credential submission. None of the runs below is evidence for server-delivered map extent. No official-client bytes were mutated in these runs.

## Attempt: raw-XWD helper nounset

- run/job: `32028641905 / 95383408028`
- admitted exact-client isolated runtime reached `WORLDMAP_BASELINE_PRE_STORAGE_OBSERVER=ARMED`;
- raw-XWD classifier self-test passed;
- helper then failed before any screen capture or secret use with `stem: unbound variable` under `set -u`;
- root cause: one Bash `local` declaration referenced `$stem` on the same declaration line before assignment was visible;
- repair: split `local stem="$1"` and `local xwdfile="$ROOT/$stem.xwd"`;
- cleanup markers: `WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS`, `WORLDMAP_BASELINE_CLEANUP=COMPLETE`;
- `WORLDMAP_BASELINE_LOGIN_SUBMITTED` was not emitted.

Classification: `PRE_SECRET_INFRA_FAILURE`, baseline login not consumed.

## Attempts: toolroot XWD dynamic loader

Two exact isolated baseline generations reached the already-proven pre-Storage observer and then failed before secret submission because the task selected toolroot `xwd` without its toolroot library search path:

- `32029117879 / 95384858852`;
- `32029164295 / 95385382498`.

Both emitted:

```text
WORLDMAP_BASELINE_PRE_STORAGE_OBSERVER=ARMED
WORLDMAP_BASELINE_LOGIN_UI_TOOLING=RAW_XWD_GEOMETRY_PASS
.../toolroot/usr/bin/xwd: error while loading shared libraries: libxkbfile.so.1: cannot open shared object file
WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_BASELINE_CLEANUP=COMPLETE
```

Neither emitted `WORLDMAP_BASELINE_LOGIN_SUBMITTED=true`.

Classification: `PRE_SECRET_INFRA_FAILURE`, baseline login not consumed.

## No-client changed-hypothesis discriminator

A safety-hold workflow replaced the physical job with a no-client dynamic-link preflight before another login-capable generation was allowed.

- run/job: `32029511115 / 95386107932`;
- runner: `synology-otclient-01`;
- toolroot `xwd` dependencies were checked with `LD_LIBRARY_PATH="$TOOL/usr/lib/x86_64-linux-gnu:$TOOL/lib/x86_64-linux-gnu"`;
- `ldd` reported no unresolved dependency;
- a deliberately invalid-display loader probe reached normal XWD execution (`probe rc=1`) without a dynamic-loader error;
- markers:

```text
WORLDMAP_XWD_PREFLIGHT_PROBE_RC=1
WORLDMAP_XWD_TOOLROOT_DYNAMIC_LINK=PASS
WORLDMAP_XWD_PREFLIGHT_CLIENT_EXECUTED=false
WORLDMAP_XWD_PREFLIGHT_SECRET_USED=false
```

The runtime helper is therefore changed to bind toolroot XWD to the same isolated toolroot library roots. The next legal physical action is one baseline login/capture generation, still gated by current-main ancestry, canonical-controller idle, target uniqueness, pre-Storage observer attachment and a live `LOGIN_FORM` raw-XWD classification before credential entry.

## Safety result

```text
BASELINE_LOGIN_CONSUMED=false
CLIENT_BYTE_MUTATION_EXECUTED=false
PRE_STORAGE_OBSERVER_REGRESSION=false
ORIGINAL_SOURCE_REHASH=PASS
CLEANUP=COMPLETE
XWD_TOOLROOT_DYNAMIC_LINK=PASS
```
