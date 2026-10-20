# Matchup LED - ESPN Connect (browser extension)

One-click way for a Matchup LED owner to give their scoreboard access to private ESPN fantasy leagues.
The buyer signs in to espn.com normally, clicks the extension, types the board's address, clicks Send.

## Files

| file | what it is |
|---|---|
| `manifest.json` | Manifest V3. Permissions: `cookies` + host access to `https://*.espn.com/*`. Nothing else. No background script, no content scripts. |
| `popup.html` / `popup.css` / `popup.js` | The little window. All the logic is in `popup.js` (about 100 lines). |
| `pixfont.js` | The board's 5x5 pixel font, copied from `product/demo/web/pixfont.js`, for the headings. |
| `privacy.html` | Privacy policy in plain words. Also opened from the popup footer. The store listings need a public URL for this: put the same text on the GitHub repo (or GitHub Pages). |
| `icons/` | 16/32/48/128 px icons (LED "M"). `make_icons.py` regenerates them (`python make_icons.py`); buyers never need it. |

## How the hand-off works

1. `popup.js` asks the browser for the cookies `SWID` and `espn_s2` for `https://www.espn.com/`.
2. It shows them masked and asks for the scoreboard's address (`matchupled.local`, `192.168.1.42`, or `localhost:8765` for the PC demo). The address is remembered in the popup's own localStorage.
3. Send opens a new tab at `http://<address>/setup#espn=1&swid=<SWID>&s2=<espn_s2>`.
   The fragment (after `#`) is never sent over the network by a browser. The board's setup page reads it,
   immediately replaces the URL (so it is not left in the address bar), shows a confirm card, and on confirm
   saves the account through its normal `/api/accounts/espn` endpoint and lists the leagues.

Why not POST from the extension straight to the board? It would need either a host permission for the LAN
(makes the permission list scarier) or CORS on the board, and Chrome's local-network rules keep changing.
Opening a page needs no extra permission and works the same in every browser.

## Test on Jason's PC (no store needed)

1. Start the demo: `python board.py` in `product/demo`.
2. Chrome or Edge: open `chrome://extensions` (Edge: `edge://extensions`), turn on **Developer mode** (top right), click **Load unpacked**, pick this `extension` folder.
3. Pin the extension (puzzle-piece icon -> pin). Make sure you are signed in at espn.com in that browser.
4. Click the extension icon. It should show your SWID (masked) and espn_s2 (masked). Type `localhost:8765`, click Send.
5. A tab opens on the demo's setup page with a green "ESPN SIGN-IN RECEIVED" card. Click **Save and list my leagues**. Your ESPN leagues appear in the picker, same as the paste route.
6. After any edit to the extension files, click the reload arrow on its card in `chrome://extensions`.

If the popup says "not signed in" while you are: open espn.com in the same browser profile (not a guest/incognito window) and try again.

## Publishing (when the board is real)

- **Chrome Web Store**: one-time $5 developer registration. Zip the folder contents (not the folder itself). Fill the privacy tab: single purpose, each permission's reason (text is in `privacy.html`), "does not collect user data", and the privacy policy URL. Review takes a few days.
- **Edge Add-ons**: free Partner Center account; upload the same zip. Edge users can also install straight from the Chrome Web Store.
- **Firefox (not in v1)**: same code would need `browser_specific_settings.gecko.id` in the manifest and a listing on addons.mozilla.org. Left out so Chrome does not show an "unrecognized key" warning. Note for later: Firefox for Android installs add-ons from that store, which would give Android-phone buyers a route.
- Before uploading: bump `version` in `manifest.json`. (`SOURCE_URL` in `popup.js` already points at this repo.)
- Never ship an update that adds permissions, a background script, or any network call. That is the promise in the privacy policy.

## Phone-only buyers (as of Oct 2026)

Chrome and Edge on phones do not run extensions; Safari on iPhone needs an App Store app wrapper ($99/yr Apple account + a Mac).
Routes for them: have the commissioner set the league to "viewable to public" and add it by ID, or borrow any computer once a season (espn_s2 lasts about a year).
