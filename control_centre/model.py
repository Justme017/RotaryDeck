import hashlib
import json
import os
import re
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

TYPES = ('open_app', 'open_url', 'open_folder', 'run_shortcut', 'builtin')
BUILTINS = ('toggle_mute', 'play_pause', 'next_track', 'previous_track', 'screenshot', 'volume_up', 'volume_down', 'open_settings')

class ProfileError(ValueError):
    pass

def text(value, limit, field):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ProfileError(f'{field}: enter 1-{limit} characters.')
    if any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise ProfileError(f'{field}: control characters are not allowed.')
    return value

def valid_url(value):
    text(value, 512, 'URL')
    try:
        parts = urlsplit(value)
        parts.port
        if parts.scheme.lower() not in ('http', 'https') or not parts.hostname:
            raise ValueError()
        if parts.username is not None or parts.password is not None:
            raise ValueError()
        if any(c.isspace() for c in value) or chr(92) in value:
            raise ValueError()
        parts.hostname.encode('idna')
    except (ValueError, UnicodeError):
        raise ProfileError('Use an absolute HTTP/HTTPS URL without credentials or whitespace.') from None
    return value

def validate(profile):
    if not isinstance(profile, dict) or set(profile) != {'schema_version', 'profile_name', 'apps', 'actions'}:
        raise ProfileError('Expected only schema_version, profile_name, apps and actions.')
    if type(profile['schema_version']) is not int or profile['schema_version'] != 1:
        raise ProfileError('schema_version must be integer 1.')
    text(profile['profile_name'], 40, 'Profile name')
    for group in ('apps', 'actions'):
        entries = profile[group]
        if not isinstance(entries, list) or len(entries) != 6:
            raise ProfileError(f'{group}: exactly six slots are required.')
        seen = set()
        for entry in entries:
            if not isinstance(entry, dict):
                raise ProfileError(f'{group}: slots must be objects.')
            slot = entry.get('slot')
            if type(slot) is not int or slot not in range(1, 7) or slot in seen:
                raise ProfileError(f'{group}: use each integer slot 1-6 exactly once.')
            seen.add(slot)
            text(entry.get('label'), 16, f'{group} {slot} label')
            kind = entry.get('type')
            if kind not in TYPES:
                raise ProfileError(f'{group} {slot}: unsupported action type.')
            field = 'builtin_action' if kind == 'builtin' else 'target'
            if set(entry) != {'slot', 'label', 'type', field}:
                raise ProfileError(f'{group} {slot}: missing or unexpected fields.')
            if kind == 'builtin':
                if entry[field] not in BUILTINS:
                    raise ProfileError(f'{group} {slot}: unknown built-in action.')
            else:
                value = text(entry[field], 512, f'{group} {slot} target')
                if kind == 'open_url':
                    valid_url(value)
                if kind == 'run_shortcut' and not value.lower().endswith('.lnk'):
                    raise ProfileError('Shortcut targets must end in .lnk.')
    return profile

def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ProfileError('Duplicate JSON key: ' + key)
        result[key] = value
    return result

def load_profile(path):
    with Path(path).open('rb') as handle:
        raw = handle.read(1048577)
    if len(raw) > 1048576:
        raise ProfileError('Profile exceeds the 1 MB limit.')
    try:
        profile = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=unique_keys)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ProfileError('Invalid UTF-8 JSON: ' + str(exc)) from exc
    return validate(profile)

def profile_folder():
    path = Path(os.environ.get('APPDATA', str(Path.home() / '.config'))) / 'RotaryDeck' / 'profiles'
    path.mkdir(parents=True, exist_ok=True)
    return path

def safe_stem(name):
    value = re.sub(r'[^A-Za-z0-9_-]+', '-', name).strip('-')[:60] or 'profile'
    reserved = {'CON', 'PRN', 'AUX', 'NUL'} | {f'COM{i}' for i in range(1, 10)} | {f'LPT{i}' for i in range(1, 10)}
    return 'profile-' + value if value.upper() in reserved else value

def warnings(profile):
    validate(profile)
    result = []
    for group in ('apps', 'actions'):
        for entry in profile[group]:
            if len(entry['label']) > 12 or not entry['label'].isascii():
                result.append(f'{group} {entry["slot"]}: label font/width needs hardware verification; original text is preserved.')
            if entry['type'] in ('open_app', 'open_folder', 'run_shortcut') and not Path(entry['target']).exists():
                result.append(f'{group} {entry["slot"]}: target path is not present here or is an unverified application URI.')
    return result

def save_profile(profile, path):
    validate(profile)
    path = Path(path)
    if path.suffix.lower() != '.json':
        raise ProfileError('Use a .json filename.')
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(profile, ensure_ascii=False, indent=2) + '\n'
    backup = None
    digest = hashlib.sha256(path.name.encode('utf-8')).hexdigest()[:12]
    suffix = '-' + safe_stem(path.stem) + '-' + digest + '.json'
    backups = path.parent / 'backups'
    if path.exists():
        backups.mkdir(exist_ok=True)
        backup = backups / (datetime.now().strftime('%Y-%m-%d-%H%M%S-%f') + suffix)
        shutil.copy2(path, backup)
    descriptor, temporary = tempfile.mkstemp(prefix='.rotarydeck-', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8', newline='\n') as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    if backup:
        old = sorted(item for item in backups.glob('*.json') if item.name.endswith(suffix))
        for item in old[:-10]:
            item.unlink()
    return backup

def test_action(entry, confirmed=False):
    if not confirmed:
        raise ProfileError('Explicit user confirmation is required.')
    kind = entry.get('type')
    if kind == 'open_url':
        target = valid_url(entry.get('target'))
    elif kind == 'open_folder':
        path = Path(text(entry.get('target'), 512, 'Folder')).expanduser()
        if not path.is_absolute() or not path.is_dir():
            raise ProfileError('Select an existing absolute folder path.')
        target = str(path.resolve())
    else:
        raise ProfileError('Only URL and folder tests are implemented in this milestone.')
    if os.name != 'nt':
        raise ProfileError('PC action tests require Windows.')
    os.startfile(target)
