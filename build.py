#!/usr/bin/env python3
"""Build links/index.html from links.config.json."""

import json
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "links.config.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "index.html")

# ── Icons ─────────────────────────────────────────────────────────────────────

ICONS = {
    "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>',
    "youtube": '<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M23.495 6.205a3.007 3.007 0 00-2.088-2.088c-1.87-.501-9.396-.501-9.396-.501s-7.507-.01-9.396.501A3.007 3.007 0 00.527 6.205a31.247 31.247 0 00-.522 5.805 31.247 31.247 0 00.522 5.783 3.007 3.007 0 002.088 2.088c1.868.502 9.396.502 9.396.502s7.506 0 9.396-.502a3.007 3.007 0 002.088-2.088 31.247 31.247 0 00.5-5.783 31.247 31.247 0 00-.5-5.805zM9.609 15.601V8.408l6.264 3.602z"/></svg>',
    "microphone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>',
    "sessionize": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><path d="M8 21h8M12 17v4"/><circle cx="9" cy="9" r="2"/><path d="M15 8h2M15 11h2M9 14h8"/></svg>',
    "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    "twitter": '<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.744l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>',
    "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    "email": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    "link": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
}

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'

# ── Helpers ───────────────────────────────────────────────────────────────────

def esc(s):
    return (str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))

def get_icon(name):
    return ICONS.get(name, ICONS["link"])

def initials(name):
    return "".join(w[0] for w in name.split())[:2].upper()

def render_avatar(profile):
    photo = profile.get("photo", "")
    if photo:
        return f'<img class="avatar" src="{esc(photo)}" alt="{esc(profile["name"])}">'
    return f'<div class="avatar">{initials(profile["name"])}</div>'

def render_card(link):
    desc_html = ""
    if link.get("description"):
        desc_html = f'\n        <span class="card-desc">{esc(link["description"])}</span>'
    return (
        f'    <a class="card" href="{esc(link["url"])}" target="_blank" rel="noopener noreferrer">\n'
        f'      <span class="card-icon">{get_icon(link.get("icon", "link"))}</span>\n'
        f'      <span class="card-body">\n'
        f'        <span class="card-label">{esc(link["label"])}</span>{desc_html}\n'
        f'      </span>\n'
        f'      <span class="card-arrow">{ARROW}</span>\n'
        f'    </a>'
    )

# ── CSS ───────────────────────────────────────────────────────────────────────

CSS = """
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --navy:      #0F1E35;
    --navy-mid:  #1A2E4A;
    --teal:      #00B4C6;
    --teal-dim:  rgba(0,180,198,0.12);
    --teal-glow: rgba(0,180,198,0.18);
    --gold:      #C9A84C;
    --off-white: #F2EDE6;
    --muted:     #6B8BA4;
    --border:    rgba(255,255,255,0.07);
  }

  html { scroll-behavior: smooth; }

  body {
    font-family: 'DM Sans', sans-serif;
    background: var(--navy);
    color: var(--off-white);
    min-height: 100vh;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding: 56px 16px 48px;
    -webkit-font-smoothing: antialiased;
  }

  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
      radial-gradient(ellipse 80% 50% at 50% -5%, rgba(0,180,198,0.13) 0%, transparent 60%),
      radial-gradient(ellipse 50% 40% at 85% 95%, rgba(201,168,76,0.07) 0%, transparent 55%);
    pointer-events: none;
    z-index: 0;
  }

  .page {
    position: relative;
    z-index: 1;
    width: 100%;
    max-width: 480px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 36px;
  }

  /* Profile */

  .profile {
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding-top: 8px;
  }

  .avatar {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    border: 2px solid var(--teal);
    box-shadow: 0 0 0 5px var(--teal-dim);
    object-fit: cover;
    background: var(--navy-mid);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 700;
    color: var(--teal);
    letter-spacing: 0.02em;
    text-decoration: none;
    flex-shrink: 0;
  }

  .name {
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    font-weight: 700;
    color: var(--off-white);
    letter-spacing: -0.01em;
    line-height: 1.15;
    margin-top: 4px;
  }

  .title {
    font-size: 11px;
    font-weight: 500;
    color: var(--teal);
    text-transform: uppercase;
    letter-spacing: 0.14em;
  }

  .tagline {
    font-size: 14px;
    font-weight: 300;
    color: var(--muted);
    line-height: 1.6;
    max-width: 300px;
  }

  /* Cards */

  .links {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .card {
    position: relative;
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 15px 18px;
    background: var(--navy-mid);
    border: 1px solid var(--border);
    border-radius: 14px;
    text-decoration: none;
    color: var(--off-white);
    overflow: hidden;
    transition: border-color 0.2s ease, background 0.2s ease,
                box-shadow 0.2s ease, transform 0.15s ease;
  }

  .card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(130deg, var(--teal-glow) 0%, transparent 55%);
    opacity: 0;
    transition: opacity 0.25s ease;
    pointer-events: none;
  }

  .card:hover {
    border-color: rgba(0,180,198,0.4);
    background: #1c324f;
    box-shadow: 0 0 0 1px rgba(0,180,198,0.12), 0 8px 28px rgba(0,0,0,0.35);
    transform: translateY(-1px);
  }

  .card:hover::before { opacity: 1; }
  .card:active        { transform: translateY(0); }

  .card-icon {
    position: relative;
    z-index: 1;
    flex-shrink: 0;
    width: 42px;
    height: 42px;
    background: rgba(0,180,198,0.09);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--teal);
    transition: background 0.2s ease;
  }

  .card:hover .card-icon { background: rgba(0,180,198,0.16); }
  .card-icon svg { width: 20px; height: 20px; }

  .card-body {
    position: relative;
    z-index: 1;
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .card-label {
    font-size: 15px;
    font-weight: 500;
    color: var(--off-white);
    line-height: 1.3;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .card-desc {
    display: block;
    font-size: 12px;
    font-weight: 300;
    color: var(--muted);
    line-height: 1.4;
  }

  .card-arrow {
    position: relative;
    z-index: 1;
    flex-shrink: 0;
    color: var(--muted);
    opacity: 0.45;
    transition: opacity 0.2s ease, transform 0.2s ease, color 0.2s ease;
  }

  .card-arrow svg { width: 16px; height: 16px; display: block; }

  .card:hover .card-arrow {
    opacity: 1;
    color: var(--teal);
    transform: translateX(3px);
  }

  /* Footer */

  .footer {
    font-size: 12px;
    color: var(--muted);
    opacity: 0.5;
    text-align: center;
  }

  .footer-link {
    color: inherit;
    text-decoration: none;
    transition: opacity 0.2s, color 0.2s;
  }

  .footer-link:hover {
    opacity: 1;
    color: var(--teal);
  }

  @media (max-width: 400px) {
    .name { font-size: 22px; }
    .card { padding: 13px 14px; gap: 12px; }
    .card-icon { width: 38px; height: 38px; }
    .card-label { font-size: 14px; }
  }
"""

# ── HTML generation ───────────────────────────────────────────────────────────

def generate(cfg):
    profile = cfg["profile"]
    links   = cfg["links"]
    footer  = cfg.get("footer", {})

    year     = datetime.now().year
    ft_text  = footer.get("text", f"\u00a9 {year} {profile['name']}").replace("{year}", str(year))
    ft_url   = footer.get("website", "")

    footer_inner = (
        f'<a href="{esc(ft_url)}" class="footer-link">{esc(ft_text)}</a>'
        if ft_url else f"<span>{esc(ft_text)}</span>"
    )

    title_html   = f'<p class="title">{esc(profile["title"])}</p>\n    '   if profile.get("title")   else ""
    tagline_html = f'<p class="tagline">{esc(profile["tagline"])}</p>\n    ' if profile.get("tagline") else ""

    cards = "\n".join(render_card(l) for l in links)

    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(profile['name'])} \u2014 Links</title>
<meta name="description" content="{esc(profile.get('tagline') or profile.get('title') or '')}">
<meta property="og:title" content="{esc(profile['name'])}">
<meta property="og:description" content="{esc(profile.get('tagline') or profile.get('title') or '')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="page">

  <header class="profile">
    {render_avatar(profile)}
    <h1 class="name">{esc(profile['name'])}</h1>
    {title_html}{tagline_html}
  </header>

  <main class="links">
{cards}
  </main>

  <footer class="footer">
    {footer_inner}
  </footer>

</div>
</body>
</html>"""

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        print(f"Could not read links.config.json: {e}")
        raise SystemExit(1)

    html = generate(config)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    n = len(config["links"])
    print(f"Built links/index.html \u2014 {n} link{'s' if n != 1 else ''}")
