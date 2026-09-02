# 2026-09-02 exact current client proof

The owner-authorized official Linux Tibia launcher updated the KasmVNC package to `15.32.be4f48` and marked it installed/usable.

Exact current tuple observed from the launcher-managed package manifest and independently re-hashed live ELF:

- version: `15.32.be4f48`
- unpacked size: `52105824`
- unpacked SHA-256: `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`
- packed size: `10205435`
- packed SHA-256 from official launcher manifest: `7a036fb52621badb8b53f34359c49220451940164962ea08fce674c97abbc114`
- manifest SHA-256: `e6dc81180a618624287076cf7d739902239b82174f08389cdc4d24ca6f740c12`

Fresh runtime recheck found exactly one `client` process, PID `28379`, on display `:1.0`, with a top-level `Tibia` window and the exact ELF size/SHA above.

Raw CDN refetch was attempted from direct Synology, Molehill-PC, and the Synology runner/WARP path but Cloudflare returned challenge/HTTP 403. Those failed refetches are explicitly not used as authority. The promoted identity is limited to official-launcher manifest + installed ELF agreement; historical offsets, serializers, QMeta addresses and semantic runtime assumptions remain build-fenced to their original evidence.

No login, credential access, character selection, gameplay input, process-memory access, or packet capture was performed for this proof.
