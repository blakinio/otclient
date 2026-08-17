# Track A canonical Xvfb DRI-path repair — hosted validation

## Scope

GitHub-hosted implementation validation only. No Synology runner, official client, X11/VNC, network/login/gameplay or canonical lease/registration/session state was observed or mutated by this implementation PR.

## Repair basis

The physical research chain ended with Draft #421 proving the minimal causal input under the exact current canonical Xvfb argument surface:

```text
without contained LIBGL_DRIVERS_PATH: extension_count=22, GLX=false
with contained LIBGL_DRIVERS_PATH only: extension_count=23, GLX=true, GLX opcode=150
```

No explicit `+extension GLX` server argument is required.

## Implementation

The canonical session worker now:

1. derives `usr/lib/x86_64-linux-gnu/dri` from the selected trusted toolroot only;
2. requires that DRI directory to be a real non-symlink directory contained below the selected root;
3. requires `swrast_dri.so` to exist and resolve to a regular file below the contained DRI directory/toolroot;
4. makes `toolroot_complete()` fail closed when that provider contract is missing or escapes containment;
5. derives the validated DRI directory again for bootstrap and exports only:

```text
LIBGL_DRIVERS_PATH="$dri"
```

into the Xvfb process environment;
6. leaves the Xvfb argument list unchanged;
7. leaves the official client environment unchanged.

Regression fixtures mirror the real provider layout by allowing `swrast_dri.so` to be a symlink whose resolved regular-file target remains inside the DRI directory.

## Dedicated hosted validator

Temporary workflow:
`.github/workflows/tibia-official-client-re-xvfb-dri-path-validation.yml`

Validation run:
- run: `31966128631`
- job: `95211462614`
- result: `SUCCESS`
- runner: `ubuntu-24.04` GitHub-hosted
- checked PR merge candidate containing implementation head `cf9f361389972dcfe3f8c29db2ecd1c4c147c3ab`

Results:

```text
bash -n canonical session worker: PASS
canonical session tests: 14/14 PASS
canonical transition tests: 9/9 PASS
canonical guard tests: 3/3 PASS
canonical lease tests: 14/14 PASS
minimal Xvfb DRI-path source contract: PASS
```

The source contract directly rejected accidental introduction of:

- `+extension GLX` in the Xvfb launch;
- `LIBGL_ALWAYS_SOFTWARE`;
- `GALLIUM_DRIVER`;
- `MESA_LOADER_DRIVER_OVERRIDE`;
- `LIBGL_DRIVERS_PATH` leakage into the client launch environment.

The temporary validator workflow was removed immediately after successful proof and is not part of the candidate delivery.

## Governance checkpoint

Initial implementation head `a57d7671f23335f43fd189991ac138dee9064315` passed both Track A admission audits in run `31966079573` before the dedicated validator was added.

The final candidate head after validator removal/evidence/task closeout must obtain fresh normal governance and repository CI; those final run IDs belong in the terminal PR handoff, not inferred from the validator result.

## Classification

`HOSTED_REPAIR_VALIDATED_PHYSICAL_REVALIDATION_REQUIRED_AFTER_PROMOTION`

The repository implementation is validated against deterministic contracts. It does not claim that a canonical physical runtime now exists or that the official client window is fixed in production. A fresh RUNTIME redispatch from trusted `main` is required only after coordinator promotion of this repair.
