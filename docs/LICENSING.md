# Licensing and third-party code

The root MIT License applies to original work owned by Shubham Mehta. It does not grant rights to code owned by other contributors or third parties, does not override their notices, and does not silently relicense archived upstream code.

## BLE Keyboard patch

The reconnect package modifies T-vK ESP32 BLE Keyboard 0.3.0. Its upstream licensing discussion is unresolved enough that a blanket MIT claim for the entire patched library would be inappropriate:
https://github.com/T-vK/ESP32-BLE-Keyboard/issues/60

Preserve any upstream notices and verify the applicable permissions for the exact source before distributing combined third-party code. Do not represent the patch as an official upstream version. The root MIT file is not a substitute for upstream licensing.

## Other dependencies

Arduino cores, U8g2, Python/WinRT, Pycaw and other dependencies retain their own licences. Install them from their upstream sources and retain applicable notices when redistributing them.

## Existing ZIPs

Release attachments have not been rewritten to inject a licence. When preparing future archives, include the project licence for original work and the applicable third-party notices. A historical archive lacking a licence file is not proof that all its contents are MIT-licensed.
