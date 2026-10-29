import json
import os
import re
import urllib.request

repo = os.environ['GH_REPO']
token = os.environ['GH_TOKEN']
base = 'https://api.github.com/repos/' + repo

def request(path, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(base + path, data=data, method='GET' if payload is None else 'PATCH', headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)

versions = {
 'v1.0': 'Initial archived RotaryDeck_v1 sketch, DeckFirmware.h and optional WindowsApps.ahk helper.',
 'v1.2': 'Modular archived RotaryDeck_v1_2 sketch with DeckCore.h and DisplayUI.h.',
 'v2.0': 'Historical RotaryDeck_v2_0 sketch/header snapshot. Feature deltas and test coverage are not inferred from the version label.',
 'v2.1': 'Historical RotaryDeck_v2_1 firmware snapshot. The PC time/media companion was packaged separately.',
 'v2.2': 'Development line with animated carousel, centred dots, improved Media layout, Windows volume telemetry, named WinRT overload fixes, saved 12/24-hour clock and dashboard date. The local BLE reconnect patch was reported working by the owner; the complete uploaded package still needs review.'
}

for release in request('/releases?per_page=100'):
    tag = release['tag_name']
    if tag not in versions:
        continue
    if not release.get('draft'):
        print('Leaving published release unchanged:', tag)
        continue
    old = release.get('body') or ''
    links = re.findall(r'\[[^\]\r\n]+\]\(https://github\.com/user-attachments/files/[^\s)]+\)', old)
    links = list(dict.fromkeys(links))
    assets = release.get('assets') or []
    for asset in assets:
        url = asset.get('browser_download_url')
        if url:
            links.append('[' + asset['name'].replace('[', '').replace(']', '') + '](' + url + ')')
    body = '# RotaryDeck ' + tag + ' — XIAO ESP32-S3\n\n' + versions[tag]
    body += '\n\n## Platform\nSeeed Studio XIAO ESP32-S3. The final nRF52840 version is planned; this archive is not an nRF52840 build.'
    body += '\n\n## Downloads\n' + ('\n'.join(dict.fromkeys(links)) if links else 'No completed download link or release asset was detected. Finish uploading the correct ZIP before publishing.')
    body += '\n\n## Before use\nReview the archive README and required dependencies. Use manually attached firmware ZIPs, not automatic Source code archives: these archive tags do not reconstruct historical firmware commits. Incremental header/library patches are not standalone firmware.'
    body += '\n\n## Status and licensing\nDraft; not a blanket hardware-validation claim. Preserve third-party notices. The project MIT licence covers original maintainer-owned work only, not upstream library code.'
    request('/releases/' + str(release['id']), {'name': 'RotaryDeck ' + tag + ' — XIAO ESP32-S3', 'body': body})
    print('Updated draft notes without publishing or changing assets:', tag)
