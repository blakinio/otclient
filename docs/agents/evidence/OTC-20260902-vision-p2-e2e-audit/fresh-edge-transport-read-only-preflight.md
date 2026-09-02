# Fresh edge-transport read-only preflight

- observed at: 2026-09-02T16:14:44+02:00
- Molehill-PC endpoint: online; LAN `192.168.1.154/24`.
- Synology container: `otclient-track-a-kasmvnc`, running; display `:1` reachable.
- exactly one official `client` exists across all running containers.
- PID/start: `28379 / 36180734`; DISPLAY `:1.0`.
- package: `15.32.be4f48`; size `52105824`.
- SHA-256: `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`.
- PID-bound X11 window: `0x01e00017`, geometry `810,263,1020,650`, title `Tibia`.
- canonical registration: `ABSENT`; target uniqueness: `PROVEN`.
- exact current-client fence: `PASS`.
- admission: `read_only` for `OTC-20260902-vision-p2-e2e-audit` only.
- mutation/login/input/process-memory/network-payload authorities remain false; physical action count `0`.

This admission authorizes only the remaining real authenticated Synology-to-Molehill edge observation window. Pairing keys are ephemeral and must not enter repository evidence/logs. No observation frame is sent before the admission commit is pushed.
