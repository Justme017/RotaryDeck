import json
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

PLAN = {
    'v1.0': (428128222, 'RotaryDeck_v1_complete.zip', '### Included\n- Initial archived RotaryDeck_v1 sketch and DeckFirmware.h.\n- Optional WindowsApps.ahk helper.\n\nHistorical snapshot; no unverified feature delta or test coverage is inferred.'),
    'v1.2': (428128244, 'RotaryDeck_v1_2_modular.zip', '### Changed\n- Modular sketch layout with DeckCore.h and DisplayUI.h.\n\nHistorical snapshot. Exact behavioural differences and hardware coverage are not asserted.'),
    'v2.0': (428128260, 'RotaryDeck_v2_0.zip', '### Included\n- Archived RotaryDeck_v2_0 sketch and matching headers.\n\nPreserve the matching Arduino folder/sketch name. A detailed feature delta from v1.2 has not been verified.'),
    'v2.1': (428128278, 'RotaryDeck_v2_1_firmware.zip', '### Included\n- Archived RotaryDeck_v2_1 sketch, DeckCore.h and DisplayUI.h.\n- Firmware generation associated with the separate PC time/media companion.\n\nThe companion is not assumed to be bundled. Do not use backup headers as active source.'),
    'v2.2': (428128298, 'RotaryDeck_v2.2.zip', '### Added\n- Animated carousel, category animations and centred position dots.\n- Windows output-volume/mute telemetry and matching receiver.\n- Saved 12/24-hour clock setting and dashboard date.\n\n### Improved\n- Menu and Media layout; solid speaker icons.\n\n### Fixed\n- WinRT enumeration and named GATT overload calls.\n- Local BLE Keyboard reconnect handling; success reported by the owner on their device.\n\nThese describe the development line, not a fresh audit of this uploaded ZIP. Confirm the firmware, corrected companion and required library patch are included or documented. Custom Apps/Actions editor, companion GUI, enclosure, wiring diagrams, Linux/macOS and nRF52840 remain future work.')
}
INDEX_SHA = '5d54262e57aad66d3d57ffb3211abecd4363c792'

def api(repo, token, path, payload=None, method=None):
    data = None if payload is None else json.dumps(payload).encode()
    headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28', 'Content-Type': 'application/json'}
    req = Request('https://api.github.com/repos/' + repo + path, data=data, method=method or ('GET' if payload is None else 'PATCH'), headers=headers)
    with urlopen(req, timeout=30) as response:
        return json.load(response)

def upload_notice(repo, token, release, filename, content):
    if any(a['name'] == filename for a in release['assets']):
        return
    root = release['upload_url'].split('{', 1)[0]
    parsed = urlsplit(root)
    if parsed.scheme != 'https' or parsed.netloc != 'uploads.github.com' or not parsed.path.startswith('/repos/' + repo + '/releases/'):
        raise RuntimeError('Unexpected upload endpoint; refusing to send credentials')
    req = Request(root + '?name=' + quote(filename, safe=''), data=content, method='POST', headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/octet-stream'})
    with urlopen(req, timeout=30) as response:
        json.load(response)

def release_body(repo, version, changes, assets):
    lines = ['# RotaryDeck ' + version + ' — XIAO ESP32-S3', '', 'Repurposing an Ender 3 display as a Bluetooth desktop controller.', '', '## Changelog', changes, '', '## Downloads']
    for asset in assets:
        name = asset['name']
        if name.lower().endswith('.zip'):
            lines.append('- [' + name.replace('[', '').replace(']', '') + '](https://github.com/' + repo + '/releases/download/' + version + '/' + quote(name, safe='') + ')')
    lines += ['', 'Download the attached version ZIP, not the automatic Source code ZIP/tar. These archive-index tags do not reconstruct the historical firmware commits.', '', '## Platform and installation', 'Current archives target Seeed Studio XIAO ESP32-S3. nRF52840 is planned, not supported by this build. Follow the archive README and [installation guide](https://github.com/' + repo + '/blob/main/docs/INSTALLATION.md). Review required library patches and companion dependencies before flashing.', '', '## Licence', 'Original maintainer-owned work is MIT-licensed. Attached RotaryDeck-LICENSE.txt and RotaryDeck-THIRD-PARTY-NOTICES.md explain the scope. Third-party code is not relicensed; verify applicable upstream permissions before redistributing a combined library archive.', '', '## Validation and release status', 'Draft prepared for owner review; no new firmware build or archive-content audit was performed by this metadata update. No cross-platform or nRF52840 validation is claimed. [Full changelog](https://github.com/' + repo + '/blob/main/CHANGELOG.md).']
    return '\n'.join(lines)

def main():
    repo, token = os.environ['GH_REPO'], os.environ['GH_TOKEN']
    if repo != 'Justme017/RotaryDeck':
        raise RuntimeError('This one-time finalizer is restricted to Justme017/RotaryDeck')
    notices = {'RotaryDeck-LICENSE.txt': Path('LICENSE').read_bytes(), 'RotaryDeck-THIRD-PARTY-NOTICES.md': Path('docs/LICENSING.md').read_bytes()}
    all_releases = api(repo, token, '/releases?per_page=100')
    pending = []
    # Check every draft and required ZIP before any writes.
    for version, (rid, expected_zip, changes) in PLAN.items():
        release = api(repo, token, '/releases/' + str(rid))
        if not release.get('draft'):
            raise RuntimeError(version + ' is no longer a draft; no changes made by this run')
        if release['name'].split(' — ')[0] != 'RotaryDeck ' + version:
            raise RuntimeError('Release identity mismatch: ' + version)
        if any(r['id'] != rid and r['tag_name'] == version for r in all_releases):
            raise RuntimeError('Version assigned to a different release: ' + version)
        if not any(a['name'] == expected_zip and a.get('size', 0) > 0 for a in release.get('assets', [])):
            raise RuntimeError('Missing nonempty release ZIP asset for ' + version + '; no changes made by this run')
        pending.append((version, changes, release))
    for version, changes, release in pending:
        try:
            api(repo, token, '/git/ref/tags/' + version)
        except HTTPError as error:
            if error.code != 404:
                raise
            api(repo, token, '/git/refs', {'ref': 'refs/tags/' + version, 'sha': INDEX_SHA}, 'POST')
        # Existing tag refs are never force-moved.
        for filename, content in notices.items():
            upload_notice(repo, token, release, filename, content)
        updated = api(repo, token, '/releases/' + str(release['id']), {'tag_name': version, 'name': 'RotaryDeck ' + version + ' — XIAO ESP32-S3', 'body': release_body(repo, version, changes, release['assets']), 'draft': True})
        if updated.get('tag_name') != version or not updated.get('draft'):
            raise RuntimeError('Unexpected post-update state for ' + version + '; inspect drafts')
        print('Finalized draft notes/tag/notices, ZIP unchanged:', version)

if __name__ == '__main__':
    main()
