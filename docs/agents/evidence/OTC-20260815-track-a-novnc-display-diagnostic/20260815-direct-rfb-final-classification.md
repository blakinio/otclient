# Track A noVNC/direct-RFB final classification — 2026-08-15

Task: `OTC-20260815-track-a-novnc-display-diagnostic`  
PR: `#309`  
Semantic run: `31904709435`  
Job: `95060619492`  
Conclusion: `SUCCESS`

## FACT

The read-only discriminator observed:

```text
DOCKER_GATEWAY_WEBSOCKIFY_UPGRADE_STATUS=101
DOCKER_GATEWAY_WEBSOCKIFY_RFB_COMPLETE=true
DOCKER_GATEWAY_RFB_PROTOCOL_VERSION=003.008
DOCKER_GATEWAY_RFB_FRAMEBUFFER=1920x1080
DIRECT_RFB_DISPLAY_88_REACHABLE=false
DIRECT_RFB_DISPLAY_98_REACHABLE=false
DIRECT_RFB_DISPLAY_115_REACHABLE=false
X11_SOCKET_DISPLAY_COUNT=1
X11_SOCKET_DISPLAYS=:98
TRACK_A_NOVNC_DIRECT_RFB_FINGERPRINT_PROBE_COMPLETE=true
```

The three conventional direct RFB ports corresponding to displays `:88`, `:98` and `:115` all returned connection refused. Therefore no direct-RFB ServerInit fingerprint could be compared with the RFB stream exposed by host-facing `6082`.

## Conservative interpretation

This result does **not** disprove `6082 -> :98`. Websockify can target a host-local endpoint that is not published on the conventional `5900 + DISPLAY` TCP port, including a Unix socket or internal-only port.

Independent facts still make `:98` the strongest persistent candidate:

- it is the only persistent X11 Unix socket visible to the runner;
- historical successful Track A login/world evidence used `:98`;
- the historical screen profile was `1920x1080`, matching the RFB framebuffer exposed through `6082`.

These facts are insufficient to promote the exact backend mapping from inference to fact.

## Final classification

```yaml
gateway_6082_novnc_websockify_rfb: FACT
rfb_framebuffer_1920x1080: FACT
persistent_x11_socket_set: [":98"]
historical_working_track_a_display: ":98"
direct_rfb_5988: CONNECTION_REFUSED
direct_rfb_5998: CONNECTION_REFUSED
direct_rfb_6015: CONNECTION_REFUSED
exact_websockify_backend_display: UNKNOWN
display_98_strongest_candidate: INFERENCE_HIGH_CONFIDENCE
display_98_canonical: NOT_PROVEN
```

## Next discriminator

Do not repeat the same direct-port probe. A future read-only canonical-runtime registration should either obtain authoritative host-side websockify target metadata or compare a privacy-preserving framebuffer identity from `6082` against the persistent X11 display without exporting framebuffer contents. Controller lease authority does not substitute for this runtime-identity proof.
