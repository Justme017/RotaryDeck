# v2.2 baseline provenance and current integration

The source-download blocker is resolved. The owner committed RotaryDeck_v2.2/ to feature/v2.3-control-centre and copilot/featurev23-control-centre. The initial uploaded folder tree was ab8ca146ac07a7e79db98d128709041521f7c781. The owner confirms RotaryDeck_v2.2.2.zip is a renamed v2.2 archive, not a separate firmware version.

The release API previously reported archive SHA-256 8a3a91e63beab5fae2049169cb5c350525c76d3cbf3e703d9804ca939508d228. This is archive metadata, not a checksum independently verified by downloading the ZIP here.

RotaryDeck_v2.2/SOURCE_MANIFEST.json records original reconstructed-package provenance and baseline fingerprints. Subsequent v2.3 modifications do not inherit those original checksum guarantees. At reviewed commit 20b93d5eb82a8cd6bc570b077056d51002cdc946 the firmware headers have been modified, but the baseline manifest, SHA256SUMS and fingerprint test still describe original headers. Reconcile this before packaging; do not silently replace historical provenance with claims that new artifacts were historically verified. The package manifest also lists a package-local .gitignore whose presence must be reconciled with the imported tree.

The companion runtime log is absent from the reviewed current tree; root .gitignore contains its scoped ignore rule. The manifest does not list that log. This does not remove historical copies or certify the entire repository contains no secrets.
