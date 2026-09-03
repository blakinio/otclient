# Post-Qwen fresh read-only preflight

- target container: `otclient-track-a-kasmvnc` / `1af4af4d67f5`; running.
- display: `:1`; `DISPLAY_CONNECT=PASS`; dimensions `3440x1229`.
- exactly one designated client and one all-container client candidate: PID `28379`.
- process start ticks: `36180734`.
- executable: official package `.../packages/Tibia/bin/client`.
- process DISPLAY: `:1.0`; executable owner `kasm-user:kasm-user`.
- package version: `15.32.be4f48`.
- executable size: `52105824`.
- executable SHA-256: `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`.
- exactly one PID-bound X11 window: XID `0x01e00017`, geometry `810,263,1020,650`, title class `Tibia`.
- canonical runtime registration: `ABSENT`.
- boot-id SHA-256: `a6b053cc7bf4d6fffa302419b4a1d6fe5ae336c6de92abefeae27e8aa61c624a`.
- exact trusted client fence: `PASS`.
- display binding: `PASS`.
- target uniqueness: `PROVEN`.

Admission consequence: this Wave 3 task may enter `runtime_access:read_only` for one serialized observation window. This grants no canonical/mutation authority. Any change to PID/start/XID/display/fence/candidate count/boot invalidates admission. No screenshot/model/input/login/credentials/memory/network-payload/mutation occurred in this preflight; physical action count is `0`.
