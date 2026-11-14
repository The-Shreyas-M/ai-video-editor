"""Assemble v2: trimmed voice, SCRIPT-based captions (aligned), a different music track per video, whooshes, example frames."""
import json, os, subprocess, sys, wave, glob
sys.path.insert(0, r"C:\Users\shrey_itz95ac\Projects\ai-video-editor\skills\shorts-from-main-video\scripts")
from align_script import align_script
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
WS = r"C:\Users\shrey_itz95ac\Projects\AI Video Editor"
MUS = WS + r"\work\music"
SFX = r"C:\Users\shrey_itz95ac\Projects\ai-video-editor\skills\shorts-from-main-video\assets\sfx"
EX = WS + r"\work\examples\frames"
script = json.load(open("script.json", encoding="utf-8"))["clips"]
os.makedirs("trim", exist_ok=True)


def dur(p):
    w = wave.open(p)
    return w.getnframes() / w.getframerate()


def trim(cid):
    out = f"trim/{cid}.wav"
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", f"voice/{cid}.wav", "-ac", "1", "-ar", "24000",
                    "-af", "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.1,areverse",
                    out], check=True)
    return out


def seqinfo():
    m = {"ex1": "example-short-1", "ex2": "example-short-2", "ex3": "example-short-3", "raw": "example-raw", "clip": "example-clipvideo"}
    out = {}
    for k, d in m.items():
        n = len(glob.glob(f"{EX}\\{d}\\*.jpg"))
        out[k] = {"base": "file:///" + (EX + "\\" + d).replace("\\", "/").replace(" ", "%20") + "/", "fps": 15, "n": n}
    return out


SEQ = seqinfo()


def make(name, clips, fmt, pad, track, music_ss, vol, whoosh_each=True):
    t, scenes, words, parts, cues = 0.0, [], [], [], []
    for cid in clips:
        p = trim(cid)
        ws, rep = align_script(script[cid], p)
        print(f"  {cid}: match {rep['match']}  heard-differently: {rep['mismatch'][:6]}", flush=True)
        for w in ws:
            words.append({"w": w["w"], "s": t + w["s"], "e": t + w["e"]})
        d = dur(p)
        pp = pad[clips.index(cid)] if isinstance(pad, list) else pad
        scenes.append({"id": cid, "dur": round(d + pp, 3)})
        parts.append((p, d + pp))
        cues.append(t)
        t += d + pp
    lst = []
    for i, (p, d) in enumerate(parts):
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", p, "-ac", "2", "-ar", "48000", "-af", f"apad=whole_dur={d:.3f}", f"tmp_{name}_{i}.wav"], check=True)
        lst.append(f"tmp_{name}_{i}.wav")
    total = t
    inputs = sum([["-i", x] for x in lst], [])
    fc = "".join(f"[{i}:a]" for i in range(len(lst))) + f"concat=n={len(lst)}:v=0:a=1,highpass=f=70,acompressor=threshold=-18dB:ratio=3:attack=5:release=80[v]"
    subprocess.run([FF, "-y", "-loglevel", "error"] + inputs + ["-filter_complex", fc, "-map", "[v]", f"voice_{name}.wav"], check=True)
    # mix: voice + ducked music + whooshes at scene starts
    sfx_in, sfx_fc, labels = [], "", []
    for k, c in enumerate(cues if whoosh_each else cues[:1]):
        sfx_in += ["-i", SFX + (r"\whoosh-soft.wav" if k == 0 else r"\whoosh-short.wav")]
        ms = int(max(0, c - 0.04) * 1000)
        sfx_fc += f"[{k + 2}:a]aresample=48000,aformat=channel_layouts=stereo,volume=-17dB,adelay={ms}|{ms}[x{k}];"
        labels.append(f"[x{k}]")
    mix = (f"[0:a]asplit=2[vs][vk];[1:a]atrim=start={music_ss},asetpts=PTS-STARTPTS,volume={vol},afade=t=in:st=0:d=1,afade=t=out:st={total - 2.0:.2f}:d=2[m];"
           f"[m][vk]sidechaincompress=threshold=0.02:ratio=6:attack=20:release=350[md];{sfx_fc}"
           f"[vs][md]{''.join(labels)}amix=inputs={2 + len(labels)}:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[o]")
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", f"voice_{name}.wav", "-i", f"{MUS}\\{track}.mp3"] + sfx_in +
                   ["-filter_complex", mix, "-map", "[o]", "-t", f"{total:.2f}", f"audio_{name}.wav"], check=True)
    W, H = (1920, 1080) if fmt == "l" else (1080, 1920)
    cfg = {"fmt": fmt, "width": W, "height": H, "fps": 30, "scenes": scenes, "words": words, "total": round(total, 3),
           "frames": f"frames_{name}", "seq": SEQ}
    json.dump(cfg, open(f"cfg_{name}.json", "w"), indent=1)
    print(name, f"{total:.1f}s", [s["dur"] for s in scenes], flush=True)
    for x in lst:
        os.remove(x)


make("main", [f"m{i}" for i in range(1, 9)], "l", [5.5, 14.5, 18.5, 8.5, 5.5, 5.5, 7.5, 5.5], "track2", 8, 0.28)
make("h1", ["h1"], "v", 2.5, "track1", 20, 0.30)
make("h2", ["h2"], "v", 2.5, "track3", 10, 0.30)
make("h3", ["h3"], "v", 2.5, "track4", 30, 0.30)
