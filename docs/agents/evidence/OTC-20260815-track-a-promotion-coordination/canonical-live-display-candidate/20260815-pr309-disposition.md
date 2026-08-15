# PR #309 noVNC/display diagnostic — coordinator disposition

Coordinator task: `OTC-20260815-track-a-promotion-coordination`  
Source PR: `#309`  
Source final head: `717a23092e0cb43c04fd71b3471bf3eaee81b6f1`  
Semantic run: `31904709435`  
Semantic job: `95060619492`  
Source CI: `31909081449`  
`CI / Required`: `95071474364` SUCCESS  
Review threads: `0`

## Disposition

`ACCEPT_WITH_EDITS`

The source correctly preserves a bounded read-only diagnostic result. Coordinator promotion accepts only the exact FACT / INFERENCE / UNKNOWN classification below; it does not merge the research branch or promote `:98` to canonical runtime status.

## FACT

```yaml
gateway_6082_novnc_websockify_rfb: true
rfb_protocol_version: "003.008"
rfb_framebuffer: "1920x1080"
persistent_x11_socket_count: 1
persistent_x11_socket_set:
  - ":98"
direct_rfb_5988: CONNECTION_REFUSED
direct_rfb_5998: CONNECTION_REFUSED
direct_rfb_6015: CONNECTION_REFUSED
historical_working_track_a_display: ":98"
```

Historical accepted Track A evidence used display `:98` and created a visible Tibia window / probable world view on the exact fenced official client.

## INFERENCE

```yaml
display_98_is_strongest_persistent_backend_candidate: HIGH_CONFIDENCE
```

This inference is supported by the combination of the only persistent X11 socket being `:98`, historical successful Track A use of `:98`, and the historical `1920x1080` screen profile matching the RFB framebuffer exposed by `6082`.

## UNKNOWN / NOT PROVEN

```yaml
exact_websockify_6082_backend_display: UNKNOWN
exact_websockify_backend_transport: UNKNOWN
current_canonical_live_pid: UNKNOWN
current_canonical_live_session_state: UNKNOWN
display_98_is_canonical: NOT_PROVEN
```

Connection refusal on conventional `5900 + DISPLAY` ports does not disprove an internal/Unix-socket websockify mapping. The direct-port probe is therefore complete and must not be repeated unchanged.

## Promotion boundary

Future canonical-runtime registration must use a different read-only discriminator or authoritative host-side service metadata to prove concrete runtime identity. A controller lease from the merged #312 manager grants mutation authority only and does not substitute for runtime identity/provenance.

Track B remains isolated. No runtime mutation is authorized by this disposition.
