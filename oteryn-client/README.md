# Oteryn Client — moved to Oteryn-v2

**Status: HISTORICAL / NON-CANONICAL**

The first-party Rust Oteryn client is no longer developed from this repository.

Canonical destination:

- repository: `blakinio/Oteryn-v2`;
- client path: `apps/client`;
- atomic destination cutover: `blakinio/Oteryn-v2#50`;
- canonical destination merge: `78988f72a80cc904aa9176ae850c50d4efa0b0f0` (`feat(rust): perform atomic client cutover (#50)`);
- frozen source snapshot used by the cutover: `blakinio/otclient@c923ad8a1dff17b4933a6110931b0823cec2c590`.

## Source-marker rule

`oteryn-client/**` in `blakinio/otclient` is retained only as historical source, migration/provenance evidence and a behavioral reference for the completed cutover.

Do not start, continue or merge new Oteryn v2 Rust-client implementation here. All new Oteryn v2 client, server, shared Rust, protocol, content and tooling work belongs in `blakinio/Oteryn-v2` under that repository's current architecture and governance.

The historical code and documents in this subtree may describe earlier Canary compatibility, dual-protocol or pre-cutover plans. Those descriptions are not the canonical Oteryn v2 architecture after the migration and must not be used to revive a second product line.

## What remains in this repository

The legacy OTClient roots such as `src/`, `modules/`, `mods/`, `data/` and their separately governed tasks remain part of `blakinio/otclient` and are unaffected by this Rust-client cutover marker.

For historical inspection of the Rust client immediately before cutover, use commit `c923ad8a1dff17b4933a6110931b0823cec2c590` and the repository Git history rather than treating this subtree as an active development target.
