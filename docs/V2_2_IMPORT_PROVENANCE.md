# v2.2.2 baseline import provenance

## Required asset

- Release: `v2.2`
- Asset name: `RotaryDeck_v2.2.2.zip`
- Expected SHA-256: `8a3a91e63beab5fae2049169cb5c350525c76d3cbf3e703d9804ca939508d228`
- Release metadata source: GitHub release API via `get_release_by_tag`.

## Retrieval attempts in this environment

1. `get_release_by_tag` for `v2.2.2` returned 404 (tag not present).
2. `get_release_by_tag` for `v2.2` returned the `RotaryDeck_v2.2.2.zip` asset metadata including matching digest.
3. Direct download attempt from `https://github.com/Justme017/RotaryDeck/releases/download/v2.2/RotaryDeck_v2.2.2.zip` returned HTTP 404.
4. GitHub API asset download attempt (`/releases/assets/692177411` with octet-stream accept header) returned HTTP 403 in this sandbox.

## Current status

Firmware/companion baseline import is currently blocked in this environment because the release asset cannot be downloaded here, so extraction and in-repo source import cannot be completed without fabricating content.

Until the archive is downloadable, host-only v2.3 sync logic and tests are implemented, but firmware-side integration, on-device storage staging, and hardware compile/validation remain pending.
