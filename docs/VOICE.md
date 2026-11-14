# Narration with your own voice (optional, local and free)

For faceless videos you can narrate with a voice cloned from YOUR OWN voice, running entirely on your computer.
1. Install Voicebox (https://voicebox.sh, free) and create a voice profile from a clean sample of your own voice (the app guides you).
2. Start its server (Windows): `"C:/Program Files/Voicebox/voicebox-server.exe" --host 127.0.0.1 --port 17493 --data-dir "%APPDATA%/sh.voicebox.app"` (the desktop app starts it for you too).
3. `python skills/ai-video/scripts/voicebox_tts.py script.json voice/ --engine luxtts` writes one wav per clip. Engines: `luxtts` (fast, good quality, about 0.3x real time on a laptop CPU), `qwen` (best quality, about 15x slower on CPU).
Rules: only clone a voice you own or have written permission to use; say in the video and description that the voice is synthetic; YouTube's `containsSyntheticMedia` flag is set automatically when a queue item has `"synthetic": true` (CSV column `synthetic`).
No Voicebox? Record a phone voice memo instead, or use the built-in Kokoro voice of claude-animation-skills (`install_modules.py --voice`).
