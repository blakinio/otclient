# Owner-provided official Tibia Linux package — provenance checkpoint

```yaml
evidence_date: 2026-08-16
repository: blakinio/otclient
task: OTC-20260816-track-a-worldmap-extent-static-re
pr: 367
source: owner upload in ChatGPT conversation
owner_statement: downloaded today from the official Tibia website
local_filename: tibia.x64.tar.gz
archive_committed_to_repository: false
reason_archive_not_committed: preserve public-repository hygiene; record hashes/manifest rather than redistribute third-party package bytes
```

## Direct local verification

FACT:

```yaml
archive_size_bytes: 29477141
archive_sha256: 04a87c801d3855f4da1b07e201dff1f79acc8528c57c984131c3a2a88cb60ea7
contains_top_level: Tibia/
contains_executable: Tibia/Tibia
executable_size_bytes: 1460808
executable_sha256: a5fc6e8ee8246868263c438539a54ea045bd048a1bea45f968fc2f498b682ca0
executable_format: ELF 64-bit PIE x86-64
```

The archive also contains Qt6 runtime libraries/plugins and third-party licence material. String inspection of `Tibia/Tibia` contains launcher/update terminology including `Starting Launcher self update from version`, `Current Launcher Version`, `partial.package.json.version`, package configuration/version handling and update-package logic.

## Classification

FACT: the provided `Tibia/Tibia` executable does **not** satisfy the historical exact game-client fence used by this task (`size=51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`).

INFERENCE: the uploaded archive is an official Linux **launcher/bootstrap distribution**, not the already-installed full game-client payload previously reverse engineered as `15.32.df7b29`. Its small executable size and retained launcher/update strings support this interpretation.

UNKNOWN:

- current game-client build/version that this launcher would install on 2026-08-16;
- current installed game-client ELF hash/size after launcher package resolution;
- whether the current game build preserves the historical worldmap addresses/layouts;
- whether the launcher can materialize its game package non-interactively on GitHub-hosted infrastructure without authentication/runtime side effects.

## Consequence for viewport RE

Do not reject this upload as corrupt merely because it differs from the historical exact-client fence. Equally, do not relabel `Tibia/Tibia` as the game binary. Treat it as a newly supplied official launcher/bootstrap source whose package-resolution mechanism may provide a compliant route to the current official game-client payload.

Before using it for worldmap RE, recover the launcher's package metadata/update endpoints statically, identify the exact current game package and preserve a new immutable size/SHA/version fence. Do not execute GUI/login, create a Tibia session, mutate client bytes, or use Synology for static RE merely to resolve this package.
