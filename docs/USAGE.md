# Usage

## 1. Film (optional but recommended)
Window light in front of you, phone at eye level, short lines with a one-second pause between them, say the hook first, tell one failure story, end with a call to action. Full guide: `skills/shorts-from-main-video/references/recording-guide.md`. No camera? Use a voiceover or the faceless tools (`skills/ai-video/references/faceless.md`).

## 2. Edit
Put files in `<workspace>/Raw Footage/`, then in Claude Code: `/ai-video`. Typical requests:
- "Make 3 Shorts from Raw Footage/talk.mp4" (uses `shorts-from-main-video`; provide b-roll such as screen recordings in `work/`).
- "Clip the best moments of this YouTube video: URL" (`clip-video`; clip only content you own or have permission to use).
- "Make a faceless explainer about X with my voiceover" (animation modules).
- "Make a launch video of my site https://..." (`brag-slim`).

## 3. Review
Watch `Exports/<project>/`. Notes one at a time ("hook louder", "cut part 2"). Say "approved" when happy. Claude checks frames and loudness itself but cannot hear audio: listen once.

## 4. Post or schedule
Claude asks which accounts and when. One-time setup in [POSTING.md](POSTING.md). Bulk: fill `posting/schedule.csv` and `post.py import`. Always dry-run, then `--execute`. YouTube schedules server-side, so your PC can be off afterwards.

## Tips
Keep `Raw Footage/` read-only. Back up the workspace's `Exports/` (git-ignored). Keep tokens low by letting the worker session do the work and asking only for the short report.
