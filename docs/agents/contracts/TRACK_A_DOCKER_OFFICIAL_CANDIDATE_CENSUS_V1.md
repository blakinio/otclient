# Track A Docker official-client candidate census v1

Status: **REVIEWED IMPLEMENTATION CONTRACT CANDIDATE**  
Track: `official-client-re`

## Purpose

Define a fail-closed all-running-Docker candidate census that does not assume every unrelated container provides Python, POSIX shell, coreutils or any other executable in its userspace.

This contract supplements `TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1`. It does not relax that contract's requirement to cover all official native Linux client candidates before create-new/adoption/recovery decisions.

## Two-stage census

For every running Docker container returned by the Docker daemon:

1. obtain daemon-side process metadata with `docker top` using `comm` and full command/argv columns;
2. if the daemon-side census fails, is empty when a running container should have a process, or cannot be parsed safely, inventory completeness is **not proven** and the operation fails closed;
3. classify the container as requiring deep proof when any process has at least one current official-client hint:
   - `comm == client`;
   - `comm` begins with `Tibia`;
   - argv contains the CipSoft/Tibia package layout;
   - argv contains a Tibia path ending in `/bin/client`;
4. a container with no such daemon-visible official-client process hint contributes zero official-client candidates without executing a command inside that container;
5. every hinted container must run the existing deep candidate proof and retain all existing exact/mismatched/unverifiable semantics: executable path/readability, size, SHA-256 and process start identity as applicable;
6. if the deep proof cannot execute or cannot verify a hinted process, fail closed. Never reinterpret an unverifiable hinted process as absence.

`docker top` is a discovery/prefilter boundary only. It can exclude a container from expensive/in-container deep proof; it can never by itself establish an exact-current candidate or authorize bootstrap.

## Current process-signature boundary

This contract is fenced to the current official native Linux client family represented by the current-client fence. The accepted official-client launch/process evidence in this repository uses executable basename/comm `client` and Tibia package/client paths. If a future current-client fence establishes that the official Linux client no longer exposes any of the signatures above, this census contract must be revalidated before that future client can be admitted.

The rule is intentionally conservative: generic processes named `client` are treated as candidate hints and therefore force deep proof rather than being ignored.

## Security invariants

The census MUST NOT:

- narrow inventory to the canonical Kasm container only;
- skip a running Docker container because its userspace is distroless/minimal;
- treat `docker exec` exit `126`, missing Python/shell or permission failure as harmless when a daemon-visible official-client hint exists;
- persist process argv, container names or other incidental process data in public evidence when counts/stage codes suffice;
- inspect credentials, process environment, packet payloads or account/session secrets.

A PASS means only that the all-running-Docker process census is complete for this current official-client signature and every hinted candidate was deeply resolved. Bootstrap/recovery/adoption still require their own registration, lease, boot, display/window and exact-fence proofs.
