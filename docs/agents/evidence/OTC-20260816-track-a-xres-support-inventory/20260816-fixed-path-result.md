# Track A XRes client-support fixed-path inventory

## Execution

Task: `OTC-20260816-track-a-xres-support-inventory`  
Draft: `#443`  
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

Already-known core libraries are present:

- contained `libxcb.so.1` resolves to `libxcb.so.1.1.0`, SHA-256 `da27d986ee3028841472845406901d944c619934ca6e269b5afbc2f90bed4726`
- contained `libX11.so.6` resolves to `libX11.so.6.4.0`, SHA-256 `043514c902c6ad561661105d54894b103e67abb1dad52cfc7d3608039d000b77`

System aliases for those core libraries resolve to the same contained paths in this runner environment.

## Fixed headers and metadata — FACT

Contained protocol header exists:

`/work/_otclient_tibia_re_state/toolroot/usr/include/X11/extensions/XResproto.h`

SHA-256:

`e0663a0b6ce34af9b1f4a41e0250407078625afb09790a4d5c0fdc6c0491143d`

The bounded relevant header lines directly record XRes v1.2 wire constants and structures, including:

- `X_XResQueryClientIds = 4`
- `X_XResLocalClientPIDMask = 0x02`
- `xXResClientIdSpec`
- `xXResClientIdValue`
- `xXResQueryClientIdsReq`
- request size `8`
- `xXResQueryClientIdsReply`
- reply size `32`

No XCB-RES generated header was present at the checked contained/system `xcb/res.h` paths. No libXRes public header was present at the checked `XRes.h` paths. No xcb-res/XRes pkgconfig file was present in the fixed roots.

## Classification

`HEADERS_PROTOCOL_BASIS_PRESENT_NO_HELPER_LIBRARY`

Result flags:

```text
XRES_SUPPORT_LIBXCB_RES_PRESENT=false
XRES_SUPPORT_LIBXRES_PRESENT=false
XRES_SUPPORT_HEADER_BASIS_PRESENT=true
XRES_SUPPORT_PKGCONFIG_PRESENT=false
XRES_SUPPORT_RESULT=PASS_READ_ONLY_INVENTORY
```

## Protocol consequence

The missing convenience libraries explain the prior helper failure, but they do **not** block XRes identity in principle. The contained XRes protocol header supplies the request opcode, LocalClientPid mask, request/reply fixed sizes and client-ID record structures required to construct a fail-closed raw XRes v1.2 helper over the already-available local X11 socket.

Upstream XRes v1.2 protocol documentation independently specifies that `QueryClientIds` accepts any resource XID owned by a client and can return `LocalClientPid` to a local requester. A future helper should implement `QueryVersion` first, require server XRes >= 1.2, then send exactly one `QueryClientIds` spec for each raw XID with the LocalClientPid mask and parse only fully bounded replies.

## Boundaries

This inventory does not prove the viewable XID belongs to the official client. It does not authorize another client launch. It only proves a new helper path exists at the protocol level without installing new packages.

## Next action

In a fresh invocation, create one hosted/static raw-XRes helper task using the contained `XResproto.h` wire layout. Validate packet encoder/reply parser against protocol-sized fixtures and source contracts without Xvfb/client execution. Only after that helper is validated should a separately admitted physical identity run be considered.
