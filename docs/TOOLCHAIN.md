# Toolchain — ai-video-editor
Every tool, SDK, global package, driver, CLI, MCP server or skill this project needs. Add a row the moment something new is installed or first used.

| Tool | Version | Install command | Why this project needs it | Added |
|---|---|---|---|---|
| Python | 3.12.10 | already installed | Runs the one-click installer and the posting/video scripts | 2026-11-15 |
| git | any | `winget install Git.Git` | Clone and version control | 2026-11-15 |
| FFmpeg full build (Gyan.FFmpeg) | 9.0.2 | `winget install -e --id Gyan.FFmpeg` | encoding, libass captions, loudnorm | 2026-11-15 |
| faster-whisper (Whisper) | latest at install (2026-11) | `pip install faster-whisper` | transcription and caption timing alignment (small.en / base.en models) | 2026-11-15 |
| Claude Code (CLI) | current | see workspace registry | Runs the /ai-video skill and helper sessions | 2026-11-15 |
| Node.js | v26.5.0 | already installed | Playwright rendering scripts | 2026-11-15 |
| Google Chrome (system) | installed (system) | already installed | headless rendering target | 2026-11-15 |
| imageio-ffmpeg (bundles ffmpeg 7.1 with libass) | latest at install (2026-11) | `pip install imageio-ffmpeg` | fallback ffmpeg for the shorts skill | 2026-11-15 |
| opencv-python | <5 | `pip install "opencv-python<5"` | YuNet face detection / auto-framing | 2026-11-15 |
| numpy, pillow | latest at install (2026-11) | `pip install numpy pillow` | audio/image helpers | 2026-11-15 |
| google-api-python-client, google-auth-oauthlib, python-dotenv | latest at install (2026-11) | `pip install google-api-python-client google-auth-oauthlib python-dotenv` (in the AI Video Editor workspace Tools/.venv) | YouTube Data API uploads and scheduling | 2026-11-15 |
| Playwright | 1.49.1 (npm) | npm install (run inside ~/.claude/tools/claude-animation-skills/kit) | used with system Chrome to render HTML to frames; its own Chromium download stalled and is not needed | 2026-11-15 |
| clip-video skill, Devini Community Edition 1.0 (MIT, based on Plextrang/Claude-Video-Clipper) | 1.0 | python install.py inside ~/.claude/skills/clip-video (creates .venv: yt-dlp, faster-whisper, soundfile, numpy, opencv) | long video to Shorts | 2026-11-15 |
| claude-animation-skills (artemnovitckii, MIT) | latest at install (2026-11) | git clone into ~/.claude/tools, then kit/setup.sh (incomplete on Windows: Chromium step stalled) | faceless animation modules, installed but not render-tested | 2026-11-15 |
| brag-slim (latent-spaces/brag, MIT) | latest at install (2026-11) | sparse git clone into ~/.claude/tools/brag | launch-video module, installed, unused | 2026-11-15 |
| HyperFrames hyperframes@0.8.34 (heygen-com, Apache-2.0) | 0.8.34 | npx --yes hyperframes@0.8.34 (not warmed up) | optional renderer, not used | 2026-11-15 |
| claude-youtube skill (agricidaniel) | latest at install (2026-11) | copied to ~/.claude/skills/youtube | titles/SEO/metadata | 2026-11-15 |
| Voicebox (voicebox.sh, user-installed) with LuxTTS engine | latest at install (2026-11) | installed by the user; server: voicebox-server.exe --host 127.0.0.1 --port 17493 --data-dir %APPDATA%/sh.voicebox.app | local cloned-voice narration | 2026-11-15 |
| instagrapi | not installed | optional, not installed in the new workspace | optional Instagram posting | 2026-11-15 |
| Pixabay Content License music tracks | n/a (asset) | downloaded manually via browser | background music | 2026-11-15 |
