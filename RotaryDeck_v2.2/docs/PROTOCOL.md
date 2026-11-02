# Current companion protocol

Custom service: 917e0001-d588-4b6b-a9a0-a81a964ce2b1
RX characteristic: 917e0002-d588-4b6b-a9a0-a81a964ce2b1

Existing firmware requires encrypted writes. Payloads are at most 20 bytes. GATT write acknowledgement is not a HID-action execution acknowledgement.

| Type | Payload |
|---|---|
| 1 | type, sequence, UTC uint32 little-endian, UTC offset int16 minutes little-endian (8 bytes total) |
| 2 | type, sequence, chunk index, chunk count, up to 16 ASCII title bytes |
| 3 | type, sequence, playback state 0..3, session state 0..2 |
| 4 | type, sequence, percent 0..100 or 255 for unavailable, mute 0/1 |

Titles are transliterated/replaced to ASCII and limited to 128 bytes. Actual volume is displayed only while fresh; manual estimates remain labelled EST/~percent. Typical loop targets are volume ~0.5s, media ~2s and clock ~5s, but Windows/metadata queries, BLE writes and timeouts can delay them. No configuration-transfer or device-to-host custom-slot activation protocol is implemented here.
