# Xdotool toolroot loader closure

Task: `OTC-20260817-track-a-worldmap-server-delivery-causal-validation`  
PR: `#475`  
Boundary: pre-secret runtime repair + no-client validation

## Physical failure boundary

Physical baseline run `32033750235`, job `95399298793`, reached all of the following before the failure:

- current-main admission: PASS;
- canonical controller idle / registration absent preflight: PASS;
- exact-client bootstrap and target uniqueness: PROVEN;
- bounded GDB attach: `WORLDMAP_BASELINE_GDB_ATTACH=PASS`;
- pre-Storage observer: `WORLDMAP_BASELINE_PRE_STORAGE_OBSERVER=ARMED`;
- manifest-owned XRes UI identity: PROVEN.

The first task-local `xdotool` invocation then failed in the dynamic loader because `libxdo.so.3` was not available in the process library search path. The failure occurred before the harmless dummy editable-field probes and before any credential submission.

Terminal safety markers from that physical generation remained:

- `WORLDMAP_BASELINE_LOGIN_SUBMITTED=true`: **absent**;
- original exact source rehash: PASS;
- task cleanup: COMPLETE.

Therefore the baseline login budget remains `0/1`.

## Repair

`track-a-worldmap-causal-ui-geometry-repair.py` now routes task-local `xdotool` through one `xdo()` wrapper with:

```text
DISPLAY=<task display>
LD_LIBRARY_PATH=<task toolroot usr/lib + lib>
```

The transform also routes the three post-`world=0` xdotool call sites (character double-click fallback and Right/Left stimulus) through the same wrapper. It fails closed unless exactly those three legacy post-block call sites are present before replacement and unless no raw `DISPLAY="$DISPLAY" "$XDOTOOL"` invocation survives afterwards.

## No-client validation

Exact repair head: `4916aa072ec4a82c4e2737e86e7de474dd9ce543`.

Run `32034438400`, job `95401437908` completed `SUCCESS` on `synology-otclient-01` without launching the Tibia client and without using secrets.

Validated:

- task toolroot `xdotool` exists and is executable;
- `LD_LIBRARY_PATH=<task toolroot libs> ldd <xdotool>` contains no `not found` dependency;
- `libxdo.so.3` resolves under that task-local library path;
- the complete screen -> GDB -> behavioral UI helper composition passes;
- the composed helper contains the loader-safe `xdo` wrapper;
- no direct unbound `DISPLAY="$DISPLAY" "$XDOTOOL"` invocation survives;
- bounded GDB attach and behavioral editable-field gates remain present.

No client execution, login, gameplay, credential output, raw XWD artifact, or client-byte mutation occurred in this validation.

## Disposition

`XDOTOOL_TOOLROOT_LOADER_CLOSURE=PROVEN_NO_CLIENT`.

Next legal physical action remains exactly one hardened baseline attempt after the branch is synchronized to then-current `main` and fresh Track A admission passes. The patched `[19,14]` arm remains forbidden until baseline FullMap/map-description evidence is successfully persisted.
