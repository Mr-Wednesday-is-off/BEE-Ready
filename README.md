# Bee Ready

A spelling bee study app for the 2026–2027 Scripps School Spelling Bee study lists (5th and 6th grade). Hear a word, spell it, and fill the honeycomb. There are also two-player games: Spell-off, Letter relay, and Beat the clock.

It's a Progressive Web App, so you can install it on a phone or tablet and it works with no internet.

## Install it

Open the site, then:

- **Android (Chrome):** tap ⋮ and choose **Install app** (or **Add to Home screen**).
- **iPhone / iPad (Safari):** tap the Share button and choose **Add to Home Screen**.

## Saving

Everything is saved on the device itself: the hive, honey, focus words, settings, the two-player series, and recent game scores. Nothing is sent anywhere.

Each device, and each browser on it, keeps its own copy. To move progress (for example, out of the Claude version into the installed app), go to **Back up or move progress** at the bottom of the home screen, copy the code, and paste it on the other device.

## Files

| File | What it is |
|---|---|
| `index.html` | The whole app |
| `sw.js` | Offline support. Always fetches the newest page when online, and falls back to the saved copy when offline |
| `manifest.webmanifest` | Name, colors, and icons for installing |
| `icons/` | App icons |
| `fonts/` | Baloo 2 and Atkinson Hyperlegible, bundled so they work offline (SIL Open Font License) |
| `tools/` | Scripts used to build `index.html` from the Claude artifact version and to draw the icons |

## Updating

Edit `index.html` and push. The installed app picks up the new version the next time it's opened with a connection. If you change icons or fonts, bump `ASSET_CACHE` in `sw.js`.

To rebuild `index.html` from the Claude artifact's HTML:

```
python3 tools/build_pwa.py path/to/artifact.html .
```
