# AI Video Editor for Claude Code

**Drop a video in a folder. Say what you want. Claude edits it, you approve it, Claude schedules it.**
Shorts, Reels, long videos, faceless animated reels, launch videos: one command, `/ai-video`.

> This repository, its documentation and its demo video were **made completely by Claude** (Anthropic's AI) at the request of its owner. Read the code before you run it.

## Install (pick one)

**One command** (needs Python 3.10+ and git; `--yes` lets it install the rest with winget / brew / apt):
```bash
git clone https://github.com/The-Shreyas-M/ai-video-editor
cd ai-video-editor
python install.py --yes
```
**One paste into Claude Code:** open [INSTALL-PROMPT.md](INSTALL-PROMPT.md), copy the box, paste it into a Claude Code chat. Claude installs and verifies everything and tells you what is left.

Then restart Claude Code once and type `/ai-video`.

## What you get
| Piece | What it does |
|---|---|
| `/ai-video` | The single entry point. Asks what you have and what you want, picks the right tool, runs the whole pipeline. |
| **Workspace folder** (`~/AI Video Editor`) | `Raw Footage/` (never touched), `Exports/`, `References/brand-sheet.md`, `posting/`, rules in `CLAUDE.md`. Any Claude chat can use it. |
| `shorts-from-main-video` | Your talking-head video to vertical Shorts: b-roll on top, face below, word-by-word captions, hook title, zooms, quiet whooshes, music that ducks under your voice, face auto-framing, boundary check. Includes a filming guide. |
| `clip-video` | A long video or YouTube URL to Shorts: the AI picks the best moments, face-tracked 9:16 reframing, captions (third-party, MIT). |
| `ai-video-studio` | The workflow: delegate edits to a subagent (cheap in tokens), you approve, then post. |
| **Posting module** | Safe scheduler: YouTube (official API), Instagram (optional), many accounts, bulk CSV (40 clips at once), approve-first, duplicate-proof ledger, dry-run by default. |
| **Faceless + promo modules** | claude-animation-skills (stick-figure / 3D cartoon / graph / map reels from a script or voiceover) and `brag-slim` (a launch video of any project or website). Installed into `~/.claude/tools`. |
| `youtube` skill | Titles, descriptions, tags, thumbnails (third-party). |

## Daily use
1. Put videos in `Raw Footage/`.
2. In any Claude chat: `/ai-video` (or say: "use the AI Video Editor, make 3 Shorts from `Raw Footage/talk.mp4`").
3. Claude delegates the edit and shows files in `Exports/`. Watch them, give notes one at a time, say **approved**.
4. Claude asks **which accounts** and **when**, shows a dry run, and posts or schedules only after you say go.

Details: [docs/USAGE.md](docs/USAGE.md) · architecture and token design: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) · posting setup (YouTube login, accounts, CSV): [docs/POSTING.md](docs/POSTING.md) · skill cheat sheet: [SKILL-LIST.txt](SKILL-LIST.txt) · for AI agents: [AGENTS.md](AGENTS.md).

## Requirements
Python 3.10+, git, Node.js 22+, ffmpeg (full build with libass; Windows `winget install Gyan.FFmpeg`, macOS `brew install ffmpeg-full`), Claude Code. About 3 GB of disk (Whisper model, Chromium, npm packages). No paid API keys. A Google Cloud OAuth client (free) is needed only for YouTube posting.

## Safety by design
Raw footage is never modified. Nothing is posted without your approval after you saw the final files. Credentials (`.env`, tokens, `accounts.json`) stay on your machine and are git-ignored. A per-account channel check stops posting to the wrong channel. Synthetic content should be disclosed as such. You are responsible for the content you post and for the licences of music and footage.

## Credits and licences
MIT for this repo. Third-party pieces keep their licences: see [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md) (Devini Community Edition of Claude Video Clipper / Plextrang, claude-animation-skills by Artem Novitckii, brag by latent-spaces, HyperFrames by HeyGen, claude-youtube by agricidaniel, YuNet, Montserrat).
