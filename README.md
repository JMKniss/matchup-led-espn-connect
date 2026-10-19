# Matchup LED - ESPN Connect

A small browser extension that connects your ESPN fantasy football leagues to your **Matchup LED** scoreboard.

Matchup LED is an LED scoreboard that sits on a shelf and shows your fantasy matchup live on game days. Public ESPN leagues need nothing extra. Private ESPN leagues need your ESPN sign-in, and ESPN has no official way for a device to sign in. This extension gives the scoreboard that sign-in with one click.

## How it works

1. Sign in at espn.com the way you normally do.
2. Click the extension's icon. It finds your ESPN sign-in in this browser and shows it to you, partly hidden.
3. Type your scoreboard's address (it's shown on the scoreboard's setup page) and click **Send to my scoreboard**.
4. Your scoreboard's setup page opens in a new tab. Check it and click **Save**. The scoreboard lists your ESPN leagues and you pick the ones you want.

ESPN's sign-in lasts about a year. When the scoreboard says it has expired, sign in to espn.com again and click Send again.

## What it can and can't do

The extension reads two cookies that ESPN put in your browser when you signed in: `SWID` and `espn_s2`. Together they work as a session key to your ESPN account, the same way the ESPN website knows it's you.

- It **never sees or asks for your ESPN password.**
- It reads the two cookies **only while its window is open**, after you click it. It runs nothing in the background.
- It **sends them only to the scoreboard address you type**, on your own home network. They travel in the part of the web address after the `#` sign, which browsers never send over the internet. Your scoreboard's setup page reads them, asks you to confirm, saves them on the scoreboard, and clears them from the address bar.
- There is **no server, no account, no analytics and no tracking.** The maker of Matchup LED never receives your sign-in or your league data.
- It remembers one thing: the scoreboard address you typed, so you don't have to type it again next season.

### Permissions it asks for

| Permission | Why |
|---|---|
| `cookies` | To read the two ESPN cookies above. |
| Access to `*.espn.com` | Limits the cookie reading to ESPN only. |

That is the complete list. It has no access to your tabs, browsing history, downloads or any other website. If a future version ever asks for more than this, or adds a server, it would break the promise above, and you should not accept it.

## Checking for yourself

The whole extension is a few short files, and all of the logic is in one file of about 100 lines. You're welcome to read it before installing.

The source code will be published in this repository before the extension is released on the Chrome Web Store.

## Install

- **Chrome, Edge and Brave:** coming to the Chrome Web Store and Edge Add-ons.
- **Phones:** Chrome and Edge on phones don't run extensions. If you only have a phone, ask your league commissioner to make the league viewable to the public in ESPN's league settings, then add it on the scoreboard by its league ID. Or use any computer once a season.

## On the scoreboard

The scoreboard keeps the two cookies in its own memory and never shows them back on its setup page. It uses them only to request your league data from ESPN. Disconnecting the ESPN account on the setup page erases them. The connection from your browser to the scoreboard is a plain local web page on your home Wi-Fi, the same way printers and most smart-home devices are set up.

## Privacy policy

The full privacy policy, with the same points as above in plain words, will be published here with the source code.

---

Matchup LED is an independent product. It is not affiliated with or endorsed by ESPN or The Walt Disney Company.
