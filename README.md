# REBORN 40K

AI-powered character card generator for dark sci-fi universes. Built with the [MegaNova API](https://meganova.ai).

**Live flow:** Choose a faction → Describe or photograph yourself → AI generates a personality, collectible card, and animated video.

## What It Does

1. **Choose Faction** — Pick from 6 factions (Void Corsairs, Iron Covenant, Hive Collective, Astral Wardens, Ember Legion, Null Syndicate)
2. **Describe or Camera** — Type a character description or take a selfie/upload a photo
3. **AI Pipeline** — LLM generates personality → Image model creates faction-styled portrait → Card renders with name, faction, backstory
4. **Animate** — Generate a cinematic video from the card
5. **Share** — QR code or email to get your creations on your phone

## Tech Stack

| Model | API | Purpose |
|-------|-----|---------|
| Qwen 3.5 Plus | `/v1/chat/completions` | Character personality + vision (photo → description) |
| Seedream 4.5 | `/v1/images/generations` | Character portrait with faction-specific style |
| Wan 2.6 Flash | `/v1/videos/generations` | Image-to-video animation |

All models accessed through the unified [MegaNova API](https://meganova.ai) (OpenAI-compatible).

## Quick Start

1. Get a MegaNova API key at [meganova.ai](https://meganova.ai)
2. Open `index.html` in your browser
3. Click **API** in the top-right corner and paste your key
4. Choose a faction and describe your character

That's it — no build step, no dependencies, single HTML file.

## Camera Mode (HTTPS Required)

Camera/selfie mode requires HTTPS. For local development:

```bash
python3 serve_https.py
# Open https://localhost:8443/index.html
# Accept the self-signed certificate warning
```

## File Structure

```
index.html          — Full demo (single-file, no build step)
nova_hero_bg.png    — Hero background image
factions/           — Faction avatar thumbnails (128px JPEG)
serve_https.py      — HTTPS dev server for camera mode
cert.pem / key.pem  — Self-signed SSL cert
```

## Features

- **Faction system** — 6 factions with distinct visual styles, armor, colors, and backgrounds
- **Camera input** — Take a selfie or upload a photo, AI vision describes you as a character
- **Image regeneration** — Regenerate portraits without re-running the LLM
- **Community gallery** — All generated cards saved locally, viewable in a lightbox
- **QR sharing** — Scan to save your card/video to your phone (designed for events)
- **Email delivery** — Send assets to your inbox (requires backend endpoint)

## For Events

This demo is designed for live events and conferences. Attendees:
1. Walk up to a kiosk/laptop
2. Pick a faction, optionally take a selfie
3. Get a collectible card + video in under 60 seconds
4. Scan QR code to save to their phone

## Built With

- [MegaNova API](https://meganova.ai) — Unified AI model gateway
- [html2canvas](https://html2canvas.hertzen.com/) — Card screenshot capture
- [QRious](https://github.com/neocotic/qrious) — QR code generation
- [Google model-viewer](https://modelviewer.dev/) — 3D model display (unused, reserved for future)

## License

MIT
