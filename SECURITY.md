# Security Policy

## Reporting a vulnerability

Do not open a public issue, discussion, or pull request for an active or
suspected vulnerability.

Report it privately through the repository's **Security** tab:

1. Open [Report a vulnerability](https://github.com/blakinio/otclient/security/advisories/new).
2. Create a private security advisory with the details below.
3. Keep exploit details and proposed patches inside the private advisory until
   the maintainer agrees that coordinated disclosure is safe.

Include, when available:

- the affected OTClient commit, tag, or release;
- the affected operating systems and client protocol versions;
- the Canary version or commit and relevant server configuration;
- impact, prerequisites, and a minimal proof of concept;
- reproduction steps, logs, and stack traces with credentials and personal data
  removed;
- suggested remediation or a patch, if you have one.

If the **Report a vulnerability** button is unavailable, do not fall back to a
public issue. Use a private contact method listed on the repository owner's
GitHub profile and ask the maintainer to open a draft security advisory before
sharing sensitive details.

The maintainer will validate the report, coordinate a fix, and discuss disclosure
and credit with the reporter. Please allow time for affected platforms and
protocol versions to be tested before publishing details.

## Supported versions

Security fixes target the current `main` branch and the latest published release,
when one exists. Older commits, custom builds, and unsupported protocol/server
combinations are assessed case by case. Reports are still welcome when the
affected-version status is uncertain.
