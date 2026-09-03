# Vision P2 Wave 3 fresh read-only admission preflight

Observed on the authorized Remote Desktop Commander `Synology` device immediately before persisting `runtime_access:read_only`.

- container: `otclient-track-a-kasmvnc`, ID prefix `1af4af4d67f5`, running; host container PID `18473`; started `2026-08-29T06:26:42.111997309Z`
- display: `:1` connect PASS; current root dimensions `3440x1229`
- exact client candidate count across **all running Docker containers**: `1`
- candidate container: `otclient-track-a-kasmvnc`
- client PID: `28379`; start ticks: `36180734`; display: `:1.0`
- executable: `/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client`
- cwd: `/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin`
- package version: `15.32.be4f48`; package executable: `bin/client`
- executable size: `52105824`
- executable SHA-256: `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`
- top-level `Tibia` window is bound to PID `28379` at `1020x650`
- canonical runtime registration: `ABSENT`
- host boot-id SHA-256: `a6b053cc7bf4d6fffa302419b4a1d6fe5ae336c6de92abefeae27e8aa61c624a`

Admission result: **PASS for `read_only` observation** under task `OTC-20260902-vision-p2-e2e-audit`, namespace `Synology/otclient-track-a-kasmvnc/display-1/client-28379/start-36180734`, `target_uniqueness:PROVEN`, canonical control gates `NOT_APPLICABLE`, `mutation_authorized:false`.

No screenshot, model inference, GUI input, login, credentials, character selection, gameplay, process control, process-memory access, packet capture or mutation occurred during this preflight. Physical action count remains `0`. Any target identity/currentness change invalidates this admission.
