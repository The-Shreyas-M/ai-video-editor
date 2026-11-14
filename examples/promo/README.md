# How the demo video was made (example pipeline)

The promo video for this repo was produced end to end by Claude with these files:
1. `script.json`: the narration, one clip per scene (plus 3 Shorts clips a, b, c).
2. `python ../../skills/ai-video/scripts/voicebox_tts.py script.json voice` : narration in the creator's own cloned voice (local Voicebox, free, no cloud).
3. `MUSIC=your-track.mp3 python build.py` : durations, word timings (Whisper), voice + ducked music, render configs.
4. `bash run_render.sh` : `promo.html` is a time-seekable HTML page; `render.mjs` screenshots it frame by frame with Chrome (Playwright) and ffmpeg encodes video + audio.
For a quicker, general-purpose launch video of any project or site use the `brag-slim` module via `/ai-video`. Disclose synthetic voices and AI-made content when you publish.
