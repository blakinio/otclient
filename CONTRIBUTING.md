# Contributing

Thank you for helping improve this OTClient Redemption fork. The project tracks
compatibility with Canary and multiple client protocols, so small, focused
changes with reproducible test results are the easiest to review safely.

## Before you start

- Search existing issues and pull requests before opening a duplicate.
- Use a private security advisory for a suspected vulnerability. Do not disclose
  an active vulnerability in a public issue; see [SECURITY.md](SECURITY.md).
- Keep one logical topic in each pull request. Separate refactoring, formatting,
  dependency updates, and behavior changes unless they are inseparable.
- Do not commit secrets, credentials, private server data, generated build
  output, or local environment configuration.

Bug fixes must include a minimal reproduction or a clear explanation of why one
cannot be provided. Record the exact OTClient commit, Canary version or commit,
client protocol version, operating system, and asset set involved.

## Branch workflow

Never push directly to `main`. Update your local fork, then create a topic branch
from the current `main`:

```bash
git switch main
git pull --ff-only origin main
git switch -c fix/short-description
```

Use one of these prefixes:

- `fix/...` for bug fixes
- `feat/...` for new behavior
- `chore/...` for maintenance
- `docs/...` for documentation
- `ci/...` for build and automation changes

Use a short, descriptive suffix such as `fix/login-timeout` or
`feat/protocol-compatibility-report`.

Open a pull request against `main`; direct pushes to `main` are not part of the
contribution workflow. Keep the branch up to date while it is under review and
resolve every review conversation. Accepted pull requests are squash-merged, so
write a clear pull request title suitable for the resulting commit.

## Compatibility information

Every change that can affect the client-server boundary must state:

- the exact Canary release, tag, or commit tested;
- the client protocol version selected in OTClient;
- whether the behavior was compared with the corresponding CipSoft client;
- which assets were used, including whether they are original or customized;
- any required feature flags, extended opcodes, or server-side changes.

Do not describe a change as generally compatible when it was tested against only
one protocol. If a value is not applicable, say why instead of leaving the pull
request field blank.

## Build and test expectations

Run the checks that cover the changed area before opening a pull request. Use the
build instructions in [`docs/building`](docs/building) and the repository's CMake
presets. Typical native verification includes:

```bash
cmake --preset linux-debug
cmake --build --preset linux-debug
ctest --preset linux-debug
```

On Windows, use the corresponding `windows-release`, `windows-debug`, or
`windows-tests` preset as appropriate. Changes to portable C++, protocol logic,
Lua modules, dependencies, or build configuration should be checked on both
Windows and Linux. If you cannot run one of those environments, identify the
missing coverage and explain how CI is expected to cover it.

For user-visible bugs, test the reproduction before and after the change. For
protocol changes, test connection, login, the affected packet or feature, and
disconnect behavior with the stated Canary and protocol versions.

Changes to client-assets installation must preserve and explicitly verify the
runtime contract documented in
[`docs/client-assets-auto-install.md`](docs/client-assets-auto-install.md): final
files stay under `data/things/<version>/`, `data/sounds/<version>/`, and expected
runtime locations such as `bin/`; the client continues loading from those paths.

## Keeping the fork synchronized

Keep the canonical project configured as a separate remote:

```bash
git remote add upstream https://github.com/opentibiabr/otclient.git
git fetch --prune upstream
```

If `upstream` already exists, verify it with `git remote -v` instead of adding it
again. Rebase ordinary topic branches on the current fork `main`; never rewrite
published `main`. Prepare upstream synchronization as its own maintainer-reviewed
pull request, and do not mix upstream changes with fork-specific features or
fixes. This keeps conflicts and any Canary-specific adaptations auditable.

## Pull request checklist

Before requesting review:

1. Complete every applicable section of the pull request template.
2. Link the issue and include reproduction steps for a bug fix.
3. Report Windows and Linux results, including commands and relevant failures.
4. Report the Canary version, client protocol, OS, and assets used.
5. Confirm that the pull request contains one logical change.
6. Review the diff for unrelated files, generated artifacts, and sensitive data.
7. Wait for required CI checks to pass; do not bypass or weaken a failing check.
