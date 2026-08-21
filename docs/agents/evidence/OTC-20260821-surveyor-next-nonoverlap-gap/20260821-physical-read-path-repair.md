# Surveyor UI/settings physical read-path repair

Date: 2026-08-21 Europe/Warsaw
Task: `OTC-20260821-surveyor-next-nonoverlap-gap`
Repair PR: `#659`
Implementation merge: `1cb56f652784ca1baeaf59a777e4c0b5b8ab312e`

## First trusted-main physical result

Trusted-main `Track A Surveyor v2 read-only` run `32523208150`, job `96899728966`, re-proved the exact runtime before collection:

- client PID/start: `19590 / 76611792`;
- client size/SHA: `52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`;
- display `:1`, exactly one matching visible Tibia window;
- canonical registration generation `2`, canonical and registration lease generation `19`;
- `runtime_access=read_only`, target uniqueness `PROVEN`, `mutation_authorized=false`;
- collect-all `169` rows / `12` aliases / `7` missing reader implementations / privacy `PASS`;
- sanitized artifact `9461336737`, digest `sha256:e10a836244c454056e09202f5f179c16852b743db9016e30c004b1fa3d19690f`.

The run is not task-level E2E PASS because `ui_settings_typed_reader` returned `UNAVAILABLE / LIVE_SETTINGS_READ_FAILED:CLIENTOPTIONS_PARENT_OPEN_FAILED`. Static `TClientOptions` evidence remained `AVAILABLE`.

## Read-only metadata discriminator

A temporary same-task read-only admission was persisted for two bounded metadata-only probes, then released before the repair returned to pre-merge audit. The probes read no settings JSON and no process memory.

The process user home was `/home/kasm-user`. `.local/share` existed, but the historical isolated-runtime component `CipSoft GmbH` did not exist there. A bounded name-only census found four retained `clientoptions.json` files under old package roots, proving that a home search would be ambiguous and is not an acceptable selector.

The exact-fenced live executable itself resolves to:

```text
/home/kasm-user/otclient-track-a/Tibia-32177065988-1/bin/client
```

Its own package root is therefore:

```text
/home/kasm-user/otclient-track-a/Tibia-32177065988-1
```

Within that exact package root, `conf/clientoptions.json` exists, is a regular non-symlink file, and is owned by UID `1000`, matching the target process UID. This supplies a candidate identity anchor without scanning or selecting among historical package directories.

## Repair boundary

The first #659 repair derived `exe.parent.parent` after the PID/start/size/SHA fence, opened the package root with `O_NOFOLLOW`, and used directory descriptors for `conf/clientoptions.json`. Codex audit `4997251226` correctly found a remaining rename/replacement TOCTOU: pathname-derived `root_fd` could point to a replacement tree after the executable had been hashed.

The remediated reader therefore holds an open `/proc/<pid>/exe` descriptor for the entire live read. It verifies exact size/SHA on that descriptor, opens `root/bin/client` through the held package-root directory descriptor, and requires the package executable's `(st_dev, st_ino)` to equal the held live-executable descriptor before it opens `conf/clientoptions.json` through that same root descriptor. It rechecks process start ticks and current `/proc/<pid>/exe` descriptor identity before publication. A root pathname replacement cannot redirect the config read to an unrelated tree without failing the executable-inode binding.

`O_DIRECTORY` and `O_NOFOLLOW` remain mandatory and fail closed if unavailable. The opened config must be a regular file owned by the target UID. The reader never derives settings from passwd HOME and never searches historical package roots. The output path remains `conf/clientoptions.json`, relative to the descriptor-bound exact executable package root. The exact static/live key allowlists and rebuilt dictionaries from `AUD-658-001` remain unchanged.

No gameplay input, login/relogin, client restart, process signal/control, process-memory write, credential access, network mutation, transaction, or economy action occurred during diagnosis.
