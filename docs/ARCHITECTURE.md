# Architecture and token design

```
you  ->  /ai-video (router, always listed, small)
              |  reads ONLY the module needed (SKILL.md)         <- progressive disclosure
              v
         subagent / session in the workspace  (does the heavy work; main chat stays small)
              |  engines: shorts-from-main-video | clip-video | claude-animation-skills | brag-slim | ffmpeg
              v
         Exports/<project>/  ->  you watch and approve  ->  posting/post.py (accounts, CSV, ledger)
```

## Why it is cheap in tokens
- The main chat sends a brief of <= 10 lines and gets a report of <= 150 words. Transcripts, logs and frames stay in the worker.
- Heavy lifting is local code (ffmpeg, Whisper, OpenCV), not model output. The model decides (which moments, which titles), the scripts render.
- One router skill instead of many instructions in context: it names the module file to read; unused modules cost nothing.
- Edits after review are single follow-up notes to the same worker, never a full re-run.

## Components
- `skills/ai-video`: router + `references/faceless.md` + `scripts/install_modules.py`.
- `skills/ai-video-studio`: workflow + `assets/workspace/` template (rules `CLAUDE.md`, `START-HERE.md`, `run-edit.ps1`, `References/brand-sheet.md`, `posting/`).
- `skills/shorts-from-main-video`: `make_short.py` (config JSON: parts of transcript lines + b-roll + titles; flags `--check`), `transcribe.py`, `find_phrase.py`. Layout 1080x1920: b-roll 1080x608 at y=110, face 1080x1000 at y=740, captions centred, progress bar.
- `skills/clip-video`: third-party long-video clipper with its own venv.
- Modules in `~/.claude/tools`: claude-animation-skills (HyperFrames/three.js/Playwright), brag-slim.
- Posting: `post.py`; ledger (SQLite) states CLAIMED -> DONE, AMBIGUOUS halts the run; accounts in `accounts.json`; queue in `queue.json`; bulk via `schedule.csv`.

## Extending
Add a skill folder under `skills/`, list it in `SKILL-LIST.txt`, add a row to the router table in `skills/ai-video/SKILL.md`, re-run `python install.py`.

## Known limitation
`claude-animation-skills` was written for macOS/Linux. On Windows the installer adds a `python3` shim and uses Git Bash; its Playwright-Chromium download can stall on slow networks (the installer now times out after 25 min and can simply be re-run). The faceless engines (`stick-figure`, `zach-d-films`, `graph`, ...) were installed but NOT render-tested on Windows by the author of this repo; the demo video was rendered with the pipeline in `examples/promo` (system Chrome + ffmpeg) instead. `brag-slim` needs no extra install.
