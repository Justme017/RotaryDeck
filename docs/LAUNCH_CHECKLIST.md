# Public-launch checklist

Policy: remain private until the owner confirms readiness. Documentation, draft releases and an MIT file do not authorise a public launch.

## Required work

- [ ] Reviewed current source is available in a reproducible layout.
- [ ] Windows companion has a usable configuration interface.
- [ ] Apps and Actions are editable, tested and acknowledged by the deck.
- [ ] Exact nRF52840 board selected and final firmware/device testing completed.
- [ ] S3 and nRF52840 wiring diagrams independently verified.
- [ ] Case CAD, printable files, test print and assembly instructions completed.
- [ ] Real screen photos and feature GIFs captured; no mock-ups presented as working features.
- [ ] README remains concise with a clear supported-platform table and detailed documentation links.
- [ ] Linux and macOS implementation/testing completed, or explicitly deferred by the owner with unsupported status clearly documented.

## Validation

- [ ] Clean firmware build/install and clean companion installation tested.
- [ ] Slot editing, target validation, profile persistence and device-label sync tested.
- [ ] Interrupted sync retains the previous valid configuration.
- [ ] Power cycles and reconnects tested with companion stopped and running.
- [ ] No queued launch actions replay after reconnection.
- [ ] Current functionality and proposed functionality are clearly distinguished.

## Packaging and permissions

- [ ] Archives contain the intended source, companion and required patch instructions.
- [ ] No .venv, caches, credentials, private logs or unnecessary personal paths.
- [ ] Release tags, attachments and descriptions match the intended versions.
- [ ] Third-party redistribution permissions/notices reviewed; root MIT is not used to relicense upstream code.
- [ ] Open-source download provides the actual editable project source, not documentation-only automatic archives.
- [ ] Owner explicitly approves publication and repository visibility change.

No existing workflow should be interpreted as approval to publish. Hardware validation and OS support must be reported as actually tested, not assumed.
