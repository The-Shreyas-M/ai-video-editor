"""Generate narration clips with the local Voicebox server using the owner's own cloned voice profile.
usage: python vo.py script.json outdir [engine]      script.json = {"clips": {"name": "text", ...}}
The /generate call blocks until the audio exists, then /audio/<id> serves the wav.
"""
import json, os, sys, time, urllib.request
BASE = "http://127.0.0.1:17493"
PROFILE = "b6460f7d-e8e6-487b-bf83-317c603cacf8"  # the owner's own voice profile
engine = sys.argv[3] if len(sys.argv) > 3 else None


def post(path, data):
    req = urllib.request.Request(BASE + path, data=json.dumps(data).encode(), headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=3600).read())


script = json.load(open(sys.argv[1], encoding="utf-8"))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
for name, text in script["clips"].items():
    f = os.path.join(out, name + ".wav")
    if os.path.exists(f):
        continue
    t0 = time.time()
    body = {"profile_id": PROFILE, "text": text, "language": "en", "normalize": True}
    if engine:
        body["engine"] = engine
    g = post("/generate", body)
    gid = g["id"]
    for _ in range(600):
        try:
            b = urllib.request.urlopen(f"{BASE}/audio/{gid}", timeout=60).read()
            if len(b) > 2000:
                break
        except Exception:
            pass
        time.sleep(3)
    else:
        sys.exit(f"{name}: no audio")
    open(f, "wb").write(b)
    print(f"{name}: {time.time() - t0:.0f}s, {len(text.split())} words, engine={engine or 'default'}", flush=True)
