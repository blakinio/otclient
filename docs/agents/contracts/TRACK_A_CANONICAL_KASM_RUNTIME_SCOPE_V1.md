# Track A canonical Kasm runtime scope v1

Status: **REVIEWED IMPLEMENTATION CONTRACT CANDIDATE**
Track: `official-client-re`

## Purpose

Define the runtime uniqueness boundary for the canonical native Linux Tibia client hosted in KasmVNC.

The canonical Track A runtime namespace is the single Docker container named:

`otclient-track-a-kasmvnc`

Official-client process uniqueness, zero-client recovery and create-new bootstrap decisions are evaluated inside this canonical container. Other Docker containers on the Synology host are outside the Track A runtime namespace and MUST NOT be executed into, inspected for Tibia processes, or treated as competing canonical runtime candidates.

For Kasm-backed canonical recovery/bootstrap/adoption, this scope statement supersedes earlier wording that described an all-running-Docker candidate inventory. That earlier wording was an accidental host-wide expansion of the runtime namespace, not the intended Track A isolation boundary.

## Required invariants

A recovery/bootstrap/adoption decision MUST prove all of the following:

- exactly one running Docker container has the canonical name `otclient-track-a-kasmvnc`;
- the canonical container identity is stable for the guarded transaction;
- the declared canonical display is `:1`;
- the exact current package identity is verified in the canonical container;
- official-client candidate inventory inside the canonical container is complete and fail-closed;
- a candidate with an official-client hint that cannot be deeply verified inside the canonical container is a blocker;
- zero-client recovery/create-new requires `candidate_count == 0` and `main_window_count == 0` inside the canonical container;
- adoption/post-launch verification requires exactly one exact-current candidate inside the canonical container plus the existing PID/start/fence/window proofs;
- a second official-client process inside the canonical container is forbidden.

## Explicit non-scope

The following are not Track A runtime candidates merely because they run on the same Synology host:

- unrelated Docker containers;
- services outside `otclient-track-a-kasmvnc`;
- processes belonging to Home Assistant, databases, monitoring, media, CI support or other host workloads.

No Track A recovery or bootstrap operation may require Python, shell, `docker exec`, process enumeration, executable hashing or candidate discovery inside those unrelated containers.

## Security boundary

This scope correction does not relax identity proof inside the canonical Kasm container. It only removes an accidental host-wide expansion of the runtime namespace.

The canonical container remains fail-closed for:

- unreadable official-looking processes;
- mismatched size or SHA-256;
- multiple exact candidates;
- unexpected Tibia windows;
- container identity drift;
- package/display/boot drift;
- registration/lease drift.

Credentials, login, GUI input and packet payloads are outside this scope contract.
