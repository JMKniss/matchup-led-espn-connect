// Matchup LED - ESPN Connect
// The whole extension is this file plus popup.html. There is no background script and
// no content script: nothing runs unless this popup is open.
//
// What it does, in order:
//   1. Ask the browser for two cookies ESPN set when you signed in: "SWID" and "espn_s2".
//      (The cookies permission + the *.espn.com host permission in manifest.json allow exactly this.)
//   2. Show them to you, masked, and ask for your scoreboard's address on your home Wi-Fi.
//   3. When you click Send, open  http://<your address>/setup#espn=1&swid=...&s2=...  in a new tab.
//      The part after "#" is never sent over the network by a browser; the scoreboard's own
//      setup page reads it, asks you to confirm, saves it, and clears it from the address bar.
// Nothing is sent to any server. There is no analytics, no telemetry, no update check.

'use strict';

const ESPN_URL = 'https://www.espn.com/';          // which site's cookies to read
const COOKIE_NAMES = { swid: 'SWID', s2: 'espn_s2' };
const ADDR_KEY = 'matchupled.addr';                    // remembers the address you typed (in this extension's own storage only)
const SOURCE_URL = 'https://github.com/JMKniss/matchup-led-espn-connect';   // public source for this extension

const $ = (id) => document.getElementById(id);
const api = (typeof browser !== 'undefined' && browser.cookies) ? browser : chrome; // Firefox uses `browser`, Chrome/Edge use `chrome`

function show(stateId) {
  document.querySelectorAll('.state').forEach((s) => { s.hidden = (s.id !== stateId); });
}

function mask(value, keep) {
  if (!value) return '';
  if (value.length <= keep) return value;
  return '•'.repeat(Math.min(10, value.length - keep)) + value.slice(-keep);
}

// Promise wrapper that works with both callback-style (Chrome) and promise-style (Firefox) APIs.
const PROMISES = (api !== chrome);   // Firefox's `browser.*` returns promises; Chrome/Edge's `chrome.*` takes callbacks
function getCookie(name) {
  return new Promise((resolve) => {
    try {
      if (PROMISES) api.cookies.get({ url: ESPN_URL, name }).then((c) => resolve(c || null), () => resolve(null));
      else api.cookies.get({ url: ESPN_URL, name }, (c) => resolve(c || null));
    } catch (e) {
      resolve(null);
    }
  });
}

function openTab(url) {
  // tabs.create does not need the "tabs" permission; it only opens a page.
  try {
    if (PROMISES) api.tabs.create({ url }).catch(() => window.open(url));
    else api.tabs.create({ url });
  } catch (e) {
    window.open(url);
  }
}

// Turn whatever the buyer typed into "host[:port]" with no scheme, path or spaces.
function cleanAddress(text) {
  let a = (text || '').trim();
  a = a.replace(/^https?:\/\//i, '');     // drop http:// or https://
  a = a.replace(/\/.*$/, '');             // drop any path such as /setup
  a = a.replace(/\s+/g, '');
  return a;
}

function validAddress(a) {
  // letters, digits, dots, dashes, optional :port  (covers matchupled.local, 192.168.1.42:8765, localhost:8765)
  return /^[A-Za-z0-9.-]+(:\d{1,5})?$/.test(a);
}

let found = { swid: '', s2: '' };

async function init() {
  $('v_ver').textContent = 'v' + (api.runtime && api.runtime.getManifest ? api.runtime.getManifest().version : '');
  $('l_source').href = SOURCE_URL;

  const [swidC, s2C] = await Promise.all([getCookie(COOKIE_NAMES.swid), getCookie(COOKIE_NAMES.s2)]);
  found.swid = swidC ? swidC.value : '';
  found.s2 = s2C ? s2C.value : '';

  if (!found.swid || !found.s2) {
    show('s_nologin');
    return;
  }

  $('v_swid').textContent = mask(found.swid, 6);
  $('v_s2').textContent = mask(found.s2, 4) + '  (' + found.s2.length + ' characters)';
  try { $('addr').value = localStorage.getItem(ADDR_KEY) || ''; } catch (e) { /* storage blocked: fine */ }
  show('s_ready');
  $('addr').focus();
}

function send() {
  const addr = cleanAddress($('addr').value);
  const msg = $('msg');
  if (!addr) { msg.textContent = 'Type your scoreboard\'s address first.'; return; }
  if (!validAddress(addr)) { msg.textContent = 'That does not look like an address. Example: matchupled.local or 192.168.1.42'; return; }
  try { localStorage.setItem(ADDR_KEY, addr); } catch (e) { /* ignore */ }

  const frag = new URLSearchParams({ espn: '1', swid: found.swid, s2: found.s2 }).toString();
  const url = 'http://' + addr + '/setup#' + frag;
  msg.textContent = 'Opening your scoreboard\'s setup page...';
  openTab(url);
  setTimeout(() => window.close(), 400);
}

document.addEventListener('DOMContentLoaded', () => {
  $('b_openespn').addEventListener('click', () => openTab('https://www.espn.com/login/'));
  $('b_send').addEventListener('click', send);
  $('addr').addEventListener('keydown', (e) => { if (e.key === 'Enter') send(); });
  if (window.PIX) window.PIX.all();
  init();
});
