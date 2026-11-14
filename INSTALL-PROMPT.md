# Paste-to-install prompt

Open Claude Code (desktop app or terminal) in any folder and paste everything in the box:

```text
Install the "AI Video Editor" on this computer from https://github.com/The-Shreyas-M/ai-video-editor.

1. git clone it into a folder called ai-video-editor (skip if it exists) and read its AGENTS.md first.
2. Run `python install.py --yes` (use `py` on Windows if `python` is missing). If a system tool is missing and winget/brew/apt cannot install it, tell me the exact command and wait.
3. Run `python install.py --doctor` and fix every [MISS] you can fix yourself. Do not ask me for passwords or tokens and do not enter any.
4. Tell me in 6 lines or fewer: what was installed, where my workspace folder is, what still needs me (for example the one-time YouTube login described in docs/POSTING.md), and the one thing to type next (/ai-video after restarting Claude Code).
Do not post, upload or publish anything.
```

What Claude will do: clone the repo, run the installer (skills into `~/.claude/skills`, helper modules into `~/.claude/tools`, a workspace folder in your home directory), run the doctor and report. Review `install.py` first if you like; it is short and does only what its docstring says.
