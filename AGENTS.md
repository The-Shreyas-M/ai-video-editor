# AGENTS.md: guide for AI agents (Claude Code and others)

You are in the **ai-video-editor** repository: a one-click installer plus skills for editing and posting videos with Claude Code.

## If the user asks you to install it
1. `python install.py --yes` (Windows: `py` if `python` is missing). Read `install.py` first; it is short.
2. `python install.py --doctor`. Fix every `[MISS]` you can. If a system tool cannot be installed automatically, give the exact command and wait.
3. Never ask for or type passwords/tokens. The YouTube login is a one-time browser OAuth the human does (`docs/POSTING.md`).
4. Report in <= 6 lines. Do not post, upload or publish anything during installation.

## If the user asks you to make or post a video
Run the skill `ai-video` (`~/.claude/skills/ai-video/SKILL.md`): ask what they have and want, read only the module you need, delegate the heavy work to a subagent or a session in the workspace (path in `~/.claude/ai-video-editor.json`), and keep your own context small (brief in <= 10 lines, report <= 150 words). Workspace rules are in `<workspace>/CLAUDE.md`.

## Repository map
```
install.py                     one-click installer + --doctor
INSTALL-PROMPT.md              paste-to-install prompt for humans
skills/ai-video/               the router (/ai-video) + references/faceless.md + scripts/install_modules.py
skills/ai-video-studio/        the workflow skill + assets/workspace/ (the workspace template incl. posting/post.py)
skills/shorts-from-main-video/ talking head -> Shorts (scripts/make_short.py, transcribe.py, find_phrase.py, check_setup.py)
skills/clip-video/             third-party long-video clipper (MIT), has its own install.py/venv
docs/                          USAGE, ARCHITECTURE, POSTING
SKILL-LIST.txt                 one-line description of every skill
```
Installed into the user's machine: `~/.claude/skills/<skill>`, `~/.claude/tools/{claude-animation-skills,brag,claude-youtube}`, the workspace folder, and `~/.claude/ai-video-editor.json`.

## Invariants (do not weaken)
- Never modify `Raw Footage/`. Never post without explicit approval AFTER the human saw the final files and chose the accounts. Always dry-run first.
- Posting safety: approved-only, SQLite ledger with unique key and claim-before-upload, adopt-existing-by-title, halt on ambiguous errors, per-account `expected_channel`, lock file.
- Creative minimums: hook in the first 1-3 s, lead with real examples, captions from the script for synthetic audio (`align_script.py`), a different music track per video, captions out of platform UI zones. Details: `skills/ai-video/SKILL.md`.
- Credentials never enter git or chat. Check `.gitignore` before any commit in a workspace.
- Do not invent facts, testimonials or statistics in generated videos; disclose AI-generated/synthetic content; use only music that is free for commercial use and note the source.
- Third-party code keeps its licence notices (`THIRD-PARTY-NOTICES.md`).

## Testing changes
`python install.py --dry-run`, `python install.py --doctor`, `python skills/shorts-from-main-video/scripts/check_setup.py`, and for posting a throwaway workspace with `post.py import schedule.csv --start DATE` then `plan` and a dry `run` (no network needed up to the YouTube token check). Render a real Short and look at frames before claiming it works.
