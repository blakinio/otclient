# Vision P2 live Qwen schema finding

- audit generation before finding: `89720d634f58761849a15b3a323044c535ca1f61`
- accepted Wave 2 generation: `a746dbfaa60a129fc3fa2f91e1b1e48038837a4a`
- physical exact client: PID `28379`, start `36180734`, XID `0x01e00017`, `15.32.be4f48`, size `52105824`, SHA-256 `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`
- physical production capture: PASS, `9003 ms`, full-frame zero mask before persistence, raw frame not persisted
- masked capture SHA-256: `ebbcca421d8e9a727af1143849547450b36e120e2f540cee0262de417125d97c`
- source/acquisition monotonic ns: `369728093658595` / `369734002783431`
- model host: Ollama `0.32.14`; exact Qwen digest `ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b`; pre/post residency empty
- production sensor result: `MODEL_INFERENCE_FAILED`
- ROCm first failure: rocBLASLt could not load `TensileLibrary_lazy_gfx1201.dat` even though exact file exists and is readable
- bounded Vulkan control: model loaded and image decoded `3/3`, but production sensor still failed
- direct unchanged provider diagnostic: `ValueError` with seven strict observation schema failures (`keys`, `screen_class`, `visible_text`, `ui_objects`, `appeared`, `disappeared`, `changed`)
- post-run host state: Ollama API down; zero Ollama/llama-server processes; task PID files absent
- physical action count: `0`; forbidden inputs/actions: none
- direct Codex usage: `0`

Classification: **MATERIAL FINDING ? return to separate bounded agent-vision repair lane.**
