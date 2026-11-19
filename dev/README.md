# عُمق — source and build

The repository root is the installable phone app (PWA) served by GitHub Pages. This folder holds the source.

- `umq.html` — the whole game (single file). Edit this.
- `build.py` — turns `umq.html` into the app at the repository root (index.html, sw.js, vendored three.js, Firebase and fonts).
- `icons.js` + `icon.svg` — render the app icons into `../icons/`.
- `firebase-config.js` — Firebase web config for project `umq-game` (public values; security is in `firestore.rules`).
- `firestore.rules` — Firestore rules: each player reads and writes only `users/{their uid}`.

Rebuild after changing `umq.html`:

```
npm pack three@0.128.0 @fontsource/cairo @fontsource/ibm-plex-mono firebase@10.14.1   # then untar each
node icons.js            # only if icon.svg changed
python3 build.py <three.min.js> <cairo package dir> <ibm-plex-mono package dir> <firebase package dir>
```

Notes:
- Everything is local, so the app runs offline after the first visit. `sw.js` gets a content hash, so each build replaces the old cache.
- Online save: Firebase email/password account + Firestore doc `users/{uid}` = `{v, wall, json}`. When a device with its own game in progress signs in to an account that already has a save, the player picks which game to keep.
- Inside a Claude artifact the same code uses the artifact `db` capability instead of Firebase.
- Game time is real time (1 game hour = 1 real hour). Add `#dev` to the URL to run 720× faster for testing.
