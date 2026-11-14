#!/usr/bin/env python3
"""AI Video Editor: one-click installer (Windows, macOS, Linux).

    python install.py               install everything (asks nothing; prints what is missing)
    python install.py --yes         also install missing system tools (winget / brew / apt)
    python install.py --doctor      only check the installation
    python install.py --dry-run     show what would happen
    options: --workspace PATH   --voice (free local TTS models ~1 GB)   --no-modules   --no-youtube-skill

What it does (safe to re-run):
  1. checks Python 3.10+, git, Node 22+, ffmpeg (with libass), and the optional Claude Code CLI
  2. pip-installs the Python packages (faster-whisper, opencv, ...)
  3. copies the skills in ./skills into ~/.claude/skills  (ai-video, ai-video-studio, shorts-from-main-video, clip-video)
  4. sets up clip-video's private venv, the `youtube` skill, and the faceless/promo modules (claude-animation-skills, brag-slim)
  5. creates the workspace folder (default ~/AI Video Editor) with the posting module and its own venv
"""
import json, os, platform, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOME = Path.home()
SKILLS = HOME / ".claude" / "skills"
TOOLS = HOME / ".claude" / "tools"
A = set(sys.argv[1:])
DRY, YES, DOCTOR = "--dry-run" in A, "--yes" in A, "--doctor" in A
WS = None
if "--workspace" in sys.argv:
    WS = sys.argv[sys.argv.index("--workspace") + 1]
OS = "windows" if os.name == "nt" else ("mac" if sys.platform == "darwin" else "linux")
PIP = ["faster-whisper", "imageio-ffmpeg", "numpy", "pillow", "opencv-python<5", "google-api-python-client", "google-auth-oauthlib", "python-dotenv"]
problems = []


def say(m):
    print(m, flush=True)


def run(cmd, cwd=None, check=False):
    say("  $ " + " ".join(map(str, cmd)))
    if DRY:
        return 0
    r = subprocess.run([str(c) for c in cmd], cwd=cwd)
    if check and r.returncode:
        problems.append(f"command failed: {' '.join(map(str, cmd[:4]))}")
    return r.returncode


def have(tool):
    return shutil.which(tool) is not None


def version(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
    except Exception:
        return ""


HINT = {
    "git": {"windows": "winget install -e --id Git.Git", "mac": "brew install git", "linux": "sudo apt install git"},
    "node": {"windows": "winget install -e --id OpenJS.NodeJS.LTS", "mac": "brew install node", "linux": "install Node 22+ from nodejs.org"},
    "ffmpeg": {"windows": "winget install -e --id Gyan.FFmpeg", "mac": "brew install ffmpeg-full", "linux": "sudo apt install ffmpeg"},
}


def ffmpeg_has_libass():
    exe = shutil.which("ffmpeg")
    if not exe:
        return False
    out = subprocess.run([exe, "-hide_banner", "-filters"], capture_output=True, text=True).stdout
    return " ass " in out


def check_prereqs():
    say("== 1/5 prerequisites ==")
    ok = True
    py_ok = sys.version_info >= (3, 10)
    say(("[ok]   " if py_ok else "[MISS] ") + f"Python {sys.version.split()[0]} (need 3.10+)")
    ok &= py_ok
    for tool in ("git", "node", "ffmpeg", "ffprobe"):
        found = have(tool)
        extra = ""
        if tool == "node" and found:
            v = version(["node", "-v"]).lstrip("v").split(".")[0]
            if not v.isdigit() or int(v) < 22:
                found, extra = False, f" (found v{v}, need 22+)"
        say(("[ok]   " if found else "[MISS] ") + tool + extra)
        if not found:
            key = "ffmpeg" if tool == "ffprobe" else tool
            cmd = HINT[key][OS]
            say(f"         install: {cmd}")
            if YES and not DRY and cmd.startswith(("winget", "brew", "sudo")):
                subprocess.run(cmd, shell=True)
            ok = False
    if have("ffmpeg") and not ffmpeg_has_libass():
        say("[WARN] your ffmpeg has no libass (captions). Install a 'full' build (Windows: Gyan.FFmpeg, macOS: ffmpeg-full).")
        problems.append("ffmpeg without libass: clip-video captions will fail (the shorts skill uses imageio-ffmpeg and still works)")
    say(("[ok]   " if have("claude") else "[info] ") + "Claude Code CLI" + ("" if have("claude") else " not found (only needed for headless `run-edit` jobs): https://code.claude.com"))
    return ok


def doctor():
    say("== doctor ==")
    rows = [(n, (SKILLS / n / "SKILL.md").exists()) for n in ("ai-video", "ai-video-studio", "shorts-from-main-video", "clip-video", "youtube")]
    rows += [("module claude-animation-skills", (TOOLS / "claude-animation-skills" / "kit" / "node_modules").exists()),
             ("module brag-slim", (TOOLS / "brag" / "skills" / "brag-slim" / "SKILL.md").exists()),
             ("clip-video venv", (SKILLS / "clip-video" / ".venv").exists())]
    ptr = HOME / ".claude" / "ai-video-editor.json"
    w = Path(json.loads(ptr.read_text())["workspace"]) if ptr.exists() else None
    rows += [("workspace " + (str(w) if w else "(not created)"), bool(w and (w / "CLAUDE.md").exists())),
             ("posting venv", bool(w and (w / "Tools" / ".venv").exists()))]
    for name, ok in rows:
        say(("[ok]   " if ok else "[MISS] ") + name)
    try:
        import cv2, faster_whisper, imageio_ffmpeg  # noqa
        say("[ok]   python packages (opencv, faster-whisper, imageio-ffmpeg)")
    except Exception as e:
        say(f"[MISS] python packages: {e}")
    return all(ok for _, ok in rows)


def main():
    if DOCTOR:
        sys.exit(0 if doctor() else 1)
    say(f"AI Video Editor installer ({OS}){' [dry run]' if DRY else ''}")
    check_prereqs()
    say("\n== 2/5 python packages ==")
    run([sys.executable, "-m", "pip", "install", "-q", "--upgrade", *PIP], check=True)

    say("\n== 3/5 skills -> ~/.claude/skills ==")
    SKILLS.mkdir(parents=True, exist_ok=True)
    for d in sorted((ROOT / "skills").iterdir()):
        if d.is_dir():
            dest = SKILLS / d.name
            keep = {".venv", "output"} if d.name == "clip-video" else set()
            say(f"  {d.name}")
            if not DRY:
                if dest.exists():
                    for item in dest.iterdir():
                        if item.name in keep:
                            continue
                        shutil.rmtree(item) if item.is_dir() else item.unlink()
                shutil.copytree(d, dest, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    say("\n== 4/5 engines and modules ==")
    clip = SKILLS / "clip-video"
    run([sys.executable, "install.py"], cwd=clip, check=True)
    if "--no-youtube-skill" not in A:
        yt = TOOLS / "claude-youtube"
        TOOLS.mkdir(parents=True, exist_ok=True)
        if not yt.exists():
            run(["git", "clone", "--depth", "1", "https://github.com/agricidaniel/claude-youtube.git", yt], check=True)
        src = yt / "skills" / "claude-youtube"
        if src.exists() and not DRY:
            shutil.copytree(src, SKILLS / "youtube", dirs_exist_ok=True)
            say("  youtube skill installed (third-party, agricidaniel/claude-youtube)")
    if "--no-modules" not in A:
        run([sys.executable, str(SKILLS / "ai-video" / "scripts" / "install_modules.py")] + (["--voice"] if "--voice" in A else []), check=True)

    say("\n== 5/5 workspace ==")
    run([sys.executable, str(SKILLS / "ai-video-studio" / "scripts" / "setup_workspace.py")] + ([WS] if WS else []), check=True)

    say("\n== result ==")
    ok = True if DRY else doctor()
    for p in problems:
        say("[problem] " + p)
    say("\nDone. Open Claude Code anywhere and type /ai-video (restart Claude Code once so it sees the new skills)." if ok and not problems
        else "\nFinished with notes above. Re-run `python install.py --doctor` after fixing them. Docs: README.md, AGENTS.md")


if __name__ == "__main__":
    main()
