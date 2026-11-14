"""Assemble: durations -> timelines, word timings (whisper), mixed audio (voice + ducked phonk), render configs."""
import json, os, subprocess, sys, wave
import numpy as np
from faster_whisper import WhisperModel
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
MUSIC = os.path.abspath(os.environ.get("MUSIC", "music.mp3"))  # a track licensed for commercial use (e.g. Pixabay Content License)
model = WhisperModel("base.en", device="cpu", compute_type="int8")


def dur(path):
    w = wave.open(path)
    return w.getnframes() / w.getframerate()


def words_of(path):
    w = wave.open(path)
    sr, ch = w.getframerate(), w.getnchannels()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    if ch > 1:
        a = a.reshape(-1, ch).mean(1)
    if sr != 16000:
        a = np.interp(np.linspace(0, len(a) - 1, int(len(a) * 16000 / sr)), np.arange(len(a)), a).astype(np.float32)
    segs, _ = model.transcribe(a, language="en", word_timestamps=True)
    return [{"w": x.word.strip(), "s": x.start, "e": x.end} for s in segs for x in s.words]


def make(name, clips, scene_ids, fmt, pad, music_ss, vol):
    t, scenes, words, parts = 0.0, [], [], []
    for cid, sid in zip(clips, scene_ids):
        p = f"voice/{cid}.wav"
        d = dur(p)
        for w in words_of(p):
            words.append({"w": w["w"], "s": t + w["s"], "e": t + w["e"]})
        scenes.append({"id": sid, "dur": round(d + pad, 3)})
        parts.append((p, d + pad))
        t += d + pad
    # voice track with padding silence between clips
    lst = []
    for i, (p, d) in enumerate(parts):
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", p, "-ac", "2", "-ar", "48000", "-af", f"apad=whole_dur={d:.3f}", f"tmp_{name}_{i}.wav"], check=True)
        lst.append(f"tmp_{name}_{i}.wav")
    inputs = sum([["-i", x] for x in lst], [])
    fc = "".join(f"[{i}:a]" for i in range(len(lst))) + f"concat=n={len(lst)}:v=0:a=1,highpass=f=70,acompressor=threshold=-18dB:ratio=3:attack=5:release=80[v]"
    subprocess.run([FF, "-y", "-loglevel", "error"] + inputs + ["-filter_complex", fc, "-map", "[v]", f"voice_{name}.wav"], check=True)
    total = t
    mix = (f"[0:a]asplit=2[vs][vk];[1:a]atrim=start={music_ss},asetpts=PTS-STARTPTS,volume={vol},afade=t=in:st=0:d=1,afade=t=out:st={total - 2.0:.2f}:d=2[m];"
           f"[m][vk]sidechaincompress=threshold=0.02:ratio=6:attack=20:release=350[md];[vs][md]amix=inputs=2:duration=first:normalize=0:weights=1 0.9,loudnorm=I=-14:TP=-1.5:LRA=11[o]")
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", f"voice_{name}.wav", "-i", MUSIC, "-filter_complex", mix, "-map", "[o]", "-t", f"{total:.2f}", f"audio_{name}.wav"], check=True)
    W, H = (1920, 1080) if fmt == "l" else (1080, 1920)
    cfg = {"fmt": fmt, "width": W, "height": H, "fps": 30, "scenes": scenes, "words": words, "total": round(total, 3), "frames": f"frames_{name}"}
    json.dump(cfg, open(f"cfg_{name}.json", "w"), indent=1)
    print(name, f"{total:.1f}s", [s["dur"] for s in scenes], flush=True)
    for x in lst:
        os.remove(x)


make("main", [f"s{i}" for i in range(1, 9)], [f"s{i}" for i in range(1, 9)], "l", 0.6, 12, 0.30)
make("a", ["a"], ["s3"], "v", 0.5, 40, 0.32)
make("b", ["b"], ["s5"], "v", 0.5, 75, 0.32)
make("c", ["c"], ["s6"], "v", 0.5, 120, 0.32)
