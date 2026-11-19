"""Generate narration line by line with Kokoro (via the HyperFrames CLI), then
assemble one WAV per scene and a timings.json with the start of every line."""
import json, subprocess, sys, wave, pathlib, hashlib

root = pathlib.Path(sys.argv[1]).resolve()
cli = root.parent.parent / ".claude/skills/hyperframes/scripts/plugin-cli.mjs"
cfg = json.loads((root / "build/script.json").read_text())
cache = root / "build/lines"; cache.mkdir(exist_ok=True)
out = root / "assets/voice"; out.mkdir(parents=True, exist_ok=True)
RATE = 24000

def tts(text):
    key = hashlib.sha1(f"{cfg['voice']}|{cfg['speed']}|{text}".encode()).hexdigest()[:12]
    p = cache / f"{key}.wav"
    if not p.exists():
        r = subprocess.run(["node", str(cli), "tts", text, "-v", cfg["voice"], "-s", str(cfg["speed"]),
                            "-o", str(p), "--json"], cwd=root, capture_output=True, text=True)
        if not p.exists():
            sys.exit(f"tts failed for: {text}\n{r.stdout[-500:]}{r.stderr[-500:]}")
    return p

def read(p):
    with wave.open(str(p)) as w:
        assert w.getframerate() == RATE and w.getnchannels() == 1, (w.getframerate(), w.getnchannels())
        return w.readframes(w.getnframes()), w.getsampwidth()

timings = {}
for sc in cfg["scenes"]:
    pcm, t, starts, ends, sw = b"", cfg["lead"], [], [], 2
    pcm += b"\x00\x00" * int(cfg["lead"] * RATE)
    for i, line in enumerate(sc["lines"]):
        extra = 0.0
        if isinstance(line, dict):  # {"text": ..., "pause": seconds of silence after it}
            extra, line = line.get("pause", 0.0), line["text"]
        data, sw = read(tts(line))
        dur = len(data) / sw / RATE
        starts.append(round(t, 3)); ends.append(round(t + dur, 3))
        pcm += data; t += dur
        gap = (cfg["gap"] if i < len(sc["lines"]) - 1 else cfg["tail"]) + extra
        pcm += b"\x00" * sw * int(gap * RATE); t += gap
    with wave.open(str(out / f"{sc['id']}.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(sw); w.setframerate(RATE); w.writeframes(pcm)
    timings[sc["id"]] = {"duration": round(t, 3), "starts": starts, "ends": ends}
    print(sc["id"], round(t, 2), "s")
(root / "build/timings.json").write_text(json.dumps(timings, indent=1))
print("total", round(sum(v["duration"] for v in timings.values()), 1), "s")
