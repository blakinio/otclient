# Track A XRes client-support fixed-path inventory

## Execution

Task: `OTC-20260816-track-a-xres-support-inventory`  
Source Draft: `#443`  
Trusted base: `845adabba5f6d2bfecb6d54bc13834c47cc61c94`  
Workflow run: `31973740033`  
Job: `95230007324 = SUCCESS`  
Runner: `synology-otclient-01`

Same-job deterministic Track A admission passed before the support read. The job was `runtime_access: read_only`, started no X server or official client, and did not inspect canonical state or process inventory.

The one-shot workflow was removed immediately after capture.

## Fixed library paths — FACT

Neither convenience XRes client library exists in the bounded contained/system roots checked:

- `libxcb-res.so.0`: absent
- `libxcb-res.so`: absent
- `libXRes.so.1`: absent
- `libXRes.so`: absent

Core libraries were observed at both contained and system paths. Raw job evidence recorded:

- contained `/work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/libxcb.so.1` resolving to contained `libxcb.so.1.1.0`, size `162392`, SHA-256 `7958a0136b121bdc4c708968569ad152a9ed208ab026e2537b1005dde64ca440`;
- contained `/work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/libX11.so.6` resolving to contained `libX11.so.6.4.0`, size `1298088`, SHA-256 `c5b5d782bd9cab3420a62df88f5c991507edf3331a89f98464ddbc538c37b879`;
- `/usr/lib/x86_64-linux-gnu/libxcb.so.1` resolving inside the system root with the same observed size/hash as the contained libxcb copy;
- `/usr/lib/x86_64-linux-gnu/libX11.so.6` resolving inside the system root with the same observed size/hash as the contained libX11 copy.

No claim is made that the system paths resolve into the contained toolroot; the raw log shows distinct real paths with matching observed hashes.

## Fixed headers and metadata — FACT

Contained protocol header exists at:

`/work/_otclient_tibia_re_state/toolroot/usr/include/X11/extensions/XResproto.h`

The inventory did **not** emit a SHA-256 for this header, so no header digest is promoted.

The bounded relevant header lines directly recorded XRes v1.2 wire constants and structures, including:

- `X_XResQueryClientIds = 4`
- `X_XResLocalClientPIDMask = 0x02`
- `xXResQueryClientIdsReq`
- request size `8`
- `xXResQueryClientIdsReply`
- reply size `32`

The checked generated XCB-RES header path `xcb/res.h` was absent. The checked public libXRes header path `XRes.h` was absent. No xcb-res/XRes pkgconfig file was present in the fixed roots.

## Classification

`HEADERS_PROTOCOL_BASIS_PRESENT_NO_HELPER_LIBRARY`

Result flags from the raw job:

```text
XRES_SUPPORT_LIBXCB_RES_PRESENT=false
XRES_SUPPORT_LIBXRES_PRESENT=false
XRES_SUPPORT_HEADER_BASIS_PRESENT=true
XRES_SUPPORT_PKGCONFIG_PRESENT=false
XRES_SUPPORT_RESULT=PASS_READ_ONLY_INVENTORY
```

## Coordinator correction

Source Draft #443 carried two library SHA-256 values that do not match the physical job log and additionally asserted a header digest that the job did not emit. The coordinator therefore classified the source `ACCEPT_WITH_EDITS` and corrected the durable evidence to the values directly printed by job `95230007324`, while removing the unsupported header digest claim.

The underlying presence/absence and protocol-basis classification is unchanged.

## Protocol consequence

The missing convenience libraries explain the prior helper failure, but they do **not** block XRes identity in principle. The contained XRes protocol header supplies the observed minor opcode, LocalClientPid mask and fixed request/reply sizes needed to design a fail-closed raw XRes v1.2 helper over a task-owned local X11 socket.

A future helper must first prove its packet encoder and bounded reply parser host-side. It must then use a separately admitted physical run to query server version and resource identity; this support inventory itself does not authorize that run.

## Boundaries

This inventory does not prove the viewable XID belongs to the official client. It does not authorize another client launch or any canonical window-identity change. It only establishes that the convenience libraries are absent while a contained protocol-definition basis is present.
