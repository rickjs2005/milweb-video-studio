#!/usr/bin/env python3
"""Local reference-video workspace. Python stdlib + FFmpeg; no model/API calls."""
import argparse
from array import array
from fractions import Fraction
import hashlib
import html
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import wave

SKILL = Path(__file__).resolve().parents[1]
HF_VERSION = "0.8.162"


def run(args, *, cwd=None, timeout=120):
    result = subprocess.run([str(a) for a in args], cwd=cwd, capture_output=True,
                            stdin=subprocess.DEVNULL, timeout=timeout)
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", "replace")[-5000:]
                           or result.stdout.decode("utf-8", "replace")[-5000:])
    return result


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                    encoding="utf-8")
    temp.replace(path)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def number(value):
    value = float(value)
    if not math.isfinite(value) or value <= 0:
        raise argparse.ArgumentTypeError("Use a finite positive number")
    return value


def frame_rate(value):
    try:
        return number(float(Fraction(value)))
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        raise argparse.ArgumentTypeError("Use a positive fps or fraction such as 30000/1001") from exc


def binary(name):
    found = shutil.which(name)
    if not found:
        raise RuntimeError(f"Missing {name}; install it and add it to PATH")
    return found


def media(path):
    path = Path(path).resolve(strict=True)
    if not path.is_file():
        raise ValueError("Input must be a local file")
    data = json.loads(run([binary("ffprobe"), "-v", "error", "-protocol_whitelist",
                          "file,pipe", "-show_format", "-show_streams", "-of", "json", path]).stdout)
    videos = [s for s in data.get("streams", []) if s.get("codec_type") == "video"
              and not s.get("disposition", {}).get("attached_pic")]
    if not videos:
        raise ValueError("Input has no video stream")
    duration = float(data.get("format", {}).get("duration", 0))
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError("Input has no finite positive duration")
    stream = videos[0]
    rate = stream.get("avg_frame_rate", "0/1")
    try:
        fps = float(Fraction(rate))
    except (ValueError, ZeroDivisionError):
        fps = None
    return {"path": str(path), "duration": duration, "width": stream["width"],
            "height": stream["height"], "fps": fps, "video_index": stream["index"],
            "audio": any(s.get("codec_type") == "audio" for s in data.get("streams", [])),
            "codec": stream.get("codec_name")}


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fresh_output(path, source=None):
    path = Path(path).resolve()
    if source and path == Path(source).resolve():
        raise ValueError("Output must not overwrite the input")
    if path.exists():
        raise FileExistsError(f"Output exists; choose a new path: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def frame(path, at, output, width=480, fit_height=None, video_index=None):
    scale = f"scale={width}:-2"
    if fit_height:
        scale = (f"scale={width}:{fit_height}:force_original_aspect_ratio=decrease,"
                 f"pad={width}:{fit_height}:(ow-iw)/2:(oh-ih)/2:color=0x12151c")
    run([binary("ffmpeg"), "-nostdin", "-v", "error", "-protocol_whitelist", "file,pipe",
         "-ss", f"{at:.6f}", "-i", path, "-map", f"0:{video_index}" if video_index is not None else "0:V:0", "-frames:v", "1",
         "-vf", scale, "-threads", "1", output])


def sheet(directory, prefix, count, output):
    cols = min(4, count)
    run([binary("ffmpeg"), "-nostdin", "-v", "error", "-i", directory / f"{prefix}%03d.jpg",
         "-vf", f"tile={cols}x{math.ceil(count / cols)}:padding=8:margin=8:color=0x12151c",
         "-frames:v", "1", "-threads", "1", output])


def review_page(path, source, samples, title="Reference review"):
    figures = "".join(f'<figure><img src="{html.escape(s["file"])}"><figcaption>{s["time"]:.3f}s</figcaption></figure>'
                      for s in samples)
    path.write_text("<!doctype html><meta charset='utf-8'><title>" + html.escape(title)
                    + "</title><style>body{background:#11151d;color:#eee;font:16px system-ui;margin:32px}"
                    "video{max-height:65vh;max-width:100%}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}"
                    "figure{margin:0}img{width:100%}figcaption{padding:6px}button{margin:8px;padding:8px}</style>"
                    + "<h1>" + html.escape(title) + "</h1><p>Playback and listening require review. Event scores are candidates, not verified cuts.</p>"
                    + f'<video id="v" controls src="{html.escape(Path(source).as_uri())}"></video>'
                    + '<div><button onclick="v.playbackRate=.25">0.25×</button><button onclick="v.playbackRate=.5">0.5×</button>'
                    + '<button onclick="v.playbackRate=1">1×</button></div><div class="grid">'
                    + figures + "</div>", encoding="utf-8")


def analyze(args):
    source = Path(args.video).resolve(strict=True)
    out = Path(args.out).resolve()
    if out.exists() and any(out.iterdir()):
        raise FileExistsError("Analysis output must be an empty or new directory; preserve prior annotations")
    out.mkdir(parents=True, exist_ok=True)
    meta = media(source)
    start = args.start
    end = min(args.end if args.end is not None else meta["duration"], meta["duration"])
    if not (math.isfinite(start) and math.isfinite(end) and 0 <= start < end):
        raise ValueError("Require 0 <= start < end <= duration")
    # Stream tiny gray frames; memory is bounded independently of video duration.
    width, height = 96, 54
    command = [binary("ffmpeg"), "-nostdin", "-v", "error", "-protocol_whitelist", "file,pipe",
               "-ss", str(start), "-i", str(source), "-t", str(end - start),
               "-map", f"0:{meta['video_index']}", "-an", "-vf", f"fps={args.sample_fps},scale={width}:{height},format=gray",
               "-threads", "1", "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1"]
    candidates = []
    previous = None
    index = 0
    # Avoid filling a stderr pipe while streaming frames.
    log_path = out / "frame-scan.log"
    with log_path.open("wb") as log:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=log, stdin=subprocess.DEVNULL)
        try:
            while True:
                raw = process.stdout.read(width * height)
                if len(raw) < width * height:
                    break
                if previous is not None:
                    score = sum(abs(a - b) for a, b in zip(raw, previous)) / (len(raw) * 255)
                    if score >= args.threshold:
                        candidates.append({"time": round(start + index / args.sample_fps, 6),
                                           "difference": round(score, 6)})
                previous = raw
                index += 1
            process.wait(timeout=30)
        finally:
            process.stdout.close()
            if process.poll() is None:
                process.kill()
                process.wait()
    if process.returncode:
        raise RuntimeError(log_path.read_text(encoding="utf-8", errors="replace")[-3000:])
    events = []
    for event in sorted(candidates, key=lambda e: e["difference"], reverse=True):
        if all(abs(event["time"] - e["time"]) >= 0.3 for e in events):
            events.append(event)
        if len(events) >= args.max_events:
            break
    events.sort(key=lambda e: e["time"])
    # A base grid preserves gradual motion; bursts show both sides of candidate events.
    tail = max(start, end - max(1 / (meta["fps"] or 30), 0.05))
    times = {round(start + (tail - start) * i / 7, 6) for i in range(8)}
    for event in events:
        times.update(round(max(start, min(tail, event["time"] + d / args.sample_fps)), 6)
                     for d in (-2, -1, 0, 1, 2))
    samples = []
    for i, at in enumerate(sorted(times)):
        name = f"frame{i:03d}.jpg"
        frame(source, at, out / name, video_index=meta["video_index"])
        samples.append({"time": at, "file": name})
    sheet(out, "frame", len(samples), out / "contact-sheet.jpg")
    if meta["audio"]:
        run([binary("ffmpeg"), "-nostdin", "-v", "error", "-protocol_whitelist", "file,pipe",
             "-ss", str(start), "-i", source, "-t", str(end - start), "-vn", "-ac", "1",
             "-ar", "16000", out / "speech.wav"])
    report = {"schema": "milweb.reference/1", "measured": meta,
              "source_sha256": digest(source), "range": [start, end],
              "sampling": {"fps": args.sample_fps, "threshold": args.threshold,
                           "events_are": "visual change candidates; not verified shot boundaries",
                           "frames_scanned": index},
              "events": events, "samples": samples, "observed": [], "hypotheses": [],
              "review": {"motion_playback": "pending", "listening": "pending" if meta["audio"] else "not_applicable"}}
    write_json(out / "analysis.json", report)
    (out / "timeline.md").write_text("# Reference evidence\n\n"
        "Measured candidate times below. Fill observed movement and sound after inspecting the media.\n\n"
        "| Time | Difference | Observed movement / sound | Hypothesis |\n|---|---|---|---|\n"
        + "".join(f'| {e["time"]:.3f}s | {e["difference"]:.4f} | pending | pending |\n' for e in events),
        encoding="utf-8")
    review_page(out / "review.html", source, samples)
    return {"status": "analyzed", "analysis": str(out / "analysis.json"), "frames": len(samples),
            "review": str(out / "review.html"), "visual_and_audio_review": "pending"}


def demo_audio(path, duration):
    rate = 44100
    samples = array("h")
    beats = [(0.25, 220), (1.0, 329.63), (2.35, 440), (3.7, 554.37), (5.2, 440), (6.8, 329.63), (8.1, 220)]
    for i in range(round(duration * rate)):
        t = i / rate
        value = 0.025 * math.sin(2 * math.pi * 110 * t)
        for at, frequency in beats:
            dt = t - at
            if 0 <= dt < 2:
                value += 0.11 * (1 - math.exp(-dt * 60)) * math.exp(-dt * 3.5) * (
                    math.sin(2 * math.pi * frequency * dt) + 0.25 * math.sin(2 * math.pi * frequency * 2 * dt))
        envelope = min(1, t / 0.15, (duration - t) / 0.5)
        samples.append(max(-32767, min(32767, round(32767 * value * 4.5 * max(0, envelope)))))
    if sys.byteorder != "little":
        samples.byteswap()
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(samples.tobytes())


def init(args):
    if args.demo and (args.duration != 10 or args.width * 16 != args.height * 9):
        raise ValueError("The supplied demo is 10 seconds in 9:16; create it first, then author a different layout/timing")
    root = Path(args.project).resolve()
    if root.exists() and any(root.iterdir()):
        raise FileExistsError("Project directory must be new or empty")
    root.mkdir(parents=True, exist_ok=True)
    for directory in ("assets", "analysis", "renders"):
        (root / directory).mkdir()
    source = str(Path(args.reference).resolve(strict=True)) if args.reference else None
    brief = Path(args.brief).read_text(encoding="utf-8") if args.brief else ""
    content = {"brand": "STUDIO", "eyebrow": "ESTUDO DE MOVIMENTO", "headline": "Ideias que\nganham movimento.",
               "product": "Sua próxima coleção", "detail": "Seu conteúdo. Sua identidade.",
               "cta": "Uma nova forma de apresentar.", "accent": "#c9f56b"} if args.demo else {}
    job = {"schema": "milweb.video/1", "brief": brief, "reference": source,
           "canvas": {"width": args.width, "height": args.height, "fps": args.fps, "duration": args.duration},
           "audio": {"narration": None, "music": None, "captions": None},
           "client_id": None, "project_id": None, "template": "composition.html.in",
           "demo": bool(args.demo), "review": {"reference": "pending", "visual": "pending", "audio": "pending"}}
    write_json(root / "project.json", job)
    write_json(root / "content.json", content)
    write_json(root / "reference-map.json", {"schema": "milweb.reference-map/1", "scenes": []})
    template = SKILL / "assets" / "hyperframes" / ("demo.html" if args.demo else "blank.html")
    shutil.copyfile(template, root / "composition.html.in")
    shutil.copyfile(SKILL / "assets/hyperframes/package.json", root / "package.json")
    (root / ".gitignore").write_text("node_modules/\n.hyperframes/\nassets/\nanalysis/\nrenders/\nproject.json\ncontent.json\nreference-map.json\n", encoding="utf-8")
    if args.demo:
        demo_audio(root / "assets/demo.wav", args.duration)
    prepare(root)
    return {"status": "created", "project": str(root), "next": "Install project dependencies with npm install; inspect the reference before adapting the composition"}


def prepare(root):
    root = Path(root).resolve()
    job = read_json(root / "project.json")
    content = read_json(root / "content.json")
    canvas = job["canvas"]
    for key in ("width", "height", "fps", "duration"):
        if isinstance(canvas[key], bool) or not isinstance(canvas[key], (int, float)) or not math.isfinite(canvas[key]) or canvas[key] <= 0:
            raise ValueError(f"Invalid canvas {key}")
    if canvas["width"] % 2 or canvas["height"] % 2 or not 1 <= canvas["fps"] <= 240:
        raise ValueError("Require even canvas dimensions and fps between 1 and 240")
    template = (root / job["template"]).resolve()
    if not template.is_relative_to(root):
        raise ValueError("Template must be inside the project")
    text = template.read_text(encoding="utf-8")
    payload = json.dumps(content, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    for key, value in {**{k.upper(): str(v) for k, v in canvas.items()}, "CONTENT": payload}.items():
        text = text.replace("{{" + key + "}}", value)
    if re.search(r"\{\{(?:WIDTH|HEIGHT|FPS|DURATION|CONTENT)\}\}", text):
        raise ValueError("Unresolved composition token")
    (root / "index.html").write_text(text, encoding="utf-8")
    return root


def hf_command(root):
    # Call the actual Node entrypoint, not a .cmd shim or a shell. Works with spaces on Windows.
    override = os.environ.get("MILWEB_HYPERFRAMES_JS")
    entry = Path(override).resolve() if override else root / "node_modules/hyperframes/bin/hyperframes.mjs"
    if not entry.is_file():
        raise RuntimeError(f"HyperFrames is not installed in {root}; run npm install there")
    return [binary("node"), str(entry)]


def hf(args):
    root = prepare(args.project)
    job = read_json(root / "project.json")
    if "MILWEB_UNAUTHORED_SCAFFOLD" in (root / "index.html").read_text(encoding="utf-8"):
        raise ValueError("This project is still an empty scaffold; author the reference-specific composition before rendering or checking it")
    command = hf_command(root)
    env = os.environ.copy()
    # Snapshot must never silently invoke a paid Gemini analysis when a key happens to exist.
    for key in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        env.pop(key, None)
    env["DO_NOT_TRACK"] = "1"
    if args.command == "render":
        output = fresh_output(root / "renders" / args.name)
        if not output.is_relative_to((root / "renders").resolve()):
            raise ValueError("Render name must stay inside the project's renders directory")
        rate = Fraction(str(job["canvas"]["fps"])).limit_denominator(1000000)
        command += ["render", ".", "--fps", str(rate), "--quality", args.quality,
                    "--workers", str(args.workers), "--output", str(output)]
    elif args.command == "check":
        command += ["check", ".", "--json"]
        output = None
    else:
        command += ["snapshot", ".", "--at", args.at, "--describe", "false", "--output", "renders/proof"]
        output = None
    # Stream renderer progress. No subprocess shell and no automatic installs/accounts.
    completed = subprocess.run(command, cwd=root, env=env, timeout=args.timeout)
    if completed.returncode:
        raise RuntimeError(f"HyperFrames {args.command} failed ({completed.returncode})")
    result = {"status": args.command + "_completed", "project": str(root)}
    if output:
        result["video"] = media(output)
        write_json(root / "renders/render.json", result)
    return result


def verify(args):
    path = Path(args.video).resolve(strict=True)
    if args.out:
        fresh_output(args.out, path)
    meta = media(path)
    issues = []
    if args.require_audio and not meta["audio"]:
        issues.append("Required audio stream missing")
    if args.duration is not None and abs(meta["duration"] - args.duration) > max(0.1, 1 / (meta["fps"] or 30)):
        issues.append("Duration differs from the requested duration")
    # Actual full decode, not a metadata-only approval.
    run([binary("ffmpeg"), "-nostdin", "-v", "error", "-xerror", "-protocol_whitelist", "file,pipe",
         "-i", path, "-map", f"0:{meta['video_index']}", "-map", "0:a?", "-f", "null", "-"], timeout=args.timeout)
    detections = run([binary("ffmpeg"), "-nostdin", "-hide_banner", "-protocol_whitelist", "file,pipe",
                      "-i", path, "-map", f"0:{meta['video_index']}", "-vf", "blackdetect=d=0.2:pix_th=0.10", "-an", "-f", "null", "-"],
                     timeout=args.timeout).stderr.decode("utf-8", "replace")
    black = [{"start": float(a), "end": float(b)} for a, b in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", detections)]
    loudness = None
    silence = []
    if meta["audio"]:
        measured = run([binary("ffmpeg"), "-nostdin", "-hide_banner", "-protocol_whitelist", "file,pipe", "-i", path,
                        "-vn", "-af", "silencedetect=noise=-45dB:d=0.3,loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], timeout=args.timeout).stderr.decode("utf-8", "replace")
        blocks = re.findall(r"\{\s*\"input_i\".*?\}", measured, re.S)
        if blocks:
            data = json.loads(blocks[-1])
            loudness = {name: float(data[key]) if math.isfinite(float(data[key])) else None
                        for name, key in [("integrated_lufs", "input_i"), ("true_peak_dbtp", "input_tp"), ("range_lu", "input_lra")]}
        silence = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", measured)]
    report = {"schema": "milweb.qc/1", "status": "failed" if issues else "passed", "measured": meta,
              "decode": "passed", "errors": issues, "black_intervals": black, "silence_starts": silence,
              "loudness": loudness, "review": {"visual": "pending", "listening": "pending" if meta["audio"] else "not_applicable"},
              "notes": ["Black and quiet intervals are observations, not automatic creative failures",
                        "Technical pass does not approve motion fidelity, captions, content or mix quality"]}
    if args.out:
        write_json(args.out, report)
    if issues:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        raise RuntimeError("Video failed requested technical checks")
    return report


def compare(args):
    ref, result = media(args.reference), media(args.result)
    out = Path(args.out).resolve()
    if out.exists() and any(out.iterdir()):
        raise FileExistsError("Comparison directory must be new or empty")
    out.mkdir(parents=True, exist_ok=True)
    pairs = []
    if args.map:
        for scene in read_json(args.map)["scenes"]:
            a, b = scene["reference_range"]
            c, d = scene["output_range"]
            if not (0 <= a < b <= ref["duration"] and 0 <= c < d <= result["duration"]):
                raise ValueError("Scene map ranges must fit the respective videos")
            for ratio in (0.15, 0.5, 0.85):
                pairs.append((a + (b - a) * ratio, c + (d - c) * ratio))
        alignment = "scene_map"
        if not pairs:
            raise ValueError("Scene map contains no scenes")
    else:
        pairs = [(ref["duration"] * r, result["duration"] * r) for r in (0.05, 0.2, 0.4, 0.6, 0.8, 0.95)]
        alignment = "normalized_duration; not a claim of corresponding motion"
    for i, (a, b) in enumerate(pairs):
        frame(ref["path"], a, out / f"pair{2*i:03d}.jpg", 360, 640, ref["video_index"])
        frame(result["path"], b, out / f"pair{2*i+1:03d}.jpg", 360, 640, result["video_index"])
    # Equal padding preserves each aspect ratio; no distortion between unlike canvases.
    run([binary("ffmpeg"), "-nostdin", "-v", "error", "-i", out / "pair%03d.jpg", "-vf",
         f"scale=360:640:force_original_aspect_ratio=decrease,pad=360:640:(ow-iw)/2:(oh-ih)/2,tile=2x{len(pairs)}:padding=8:margin=8",
         "-frames:v", "1", "-threads", "1", out / "comparison.jpg"])
    report = {"alignment": alignment, "pairs": [{"reference": a, "result": b} for a, b in pairs], "visual_review": "pending"}
    write_json(out / "comparison.json", report)
    return {"status": "compared", "sheet": str(out / "comparison.jpg"), **report}


def doctor(_args):
    import importlib.util
    tools = {name: shutil.which(name) for name in ("python3", "ffmpeg", "ffprobe", "node", "npm", "yt-dlp", "claude", "codex")}
    return {"core_ready": bool(tools["ffmpeg"] and tools["ffprobe"]), "tools": tools,
            "optional": {name: bool(importlib.util.find_spec(name)) for name in ("faster_whisper", "kokoro_onnx", "soundfile")},
            "renderer": {"package": f"hyperframes@{HF_VERSION}", "setup": "npm install in the created project; npx hyperframes browser ensure"},
            "paid_api_required": False}


def fetch(args):
    from urllib.parse import urlparse
    if urlparse(args.url).scheme not in ("http", "https"):
        raise ValueError("Reference URL must use http or https")
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    result = run([binary("yt-dlp"), "--no-playlist", "--no-progress", "--no-overwrites", "--restrict-filenames",
                  "--paths", out, "--print", "after_move:filepath", "--merge-output-format", "mp4", "--", args.url], timeout=args.timeout)
    return {"status": "downloaded", "paths": result.stdout.decode("utf-8", "replace").splitlines()}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("doctor"); p.set_defaults(func=doctor)
    p = sub.add_parser("new"); p.add_argument("project"); p.add_argument("--reference"); p.add_argument("--brief")
    p.add_argument("--width", type=int, default=1080); p.add_argument("--height", type=int, default=1920)
    p.add_argument("--fps", type=frame_rate, default=30); p.add_argument("--duration", type=number, default=10)
    p.add_argument("--demo", action="store_true"); p.set_defaults(func=init)
    p = sub.add_parser("fetch"); p.add_argument("url"); p.add_argument("--out", required=True)
    p.add_argument("--timeout", type=number, default=180); p.set_defaults(func=fetch)
    p = sub.add_parser("analyze"); p.add_argument("video"); p.add_argument("--out", required=True)
    p.add_argument("--start", type=float, default=0); p.add_argument("--end", type=float)
    p.add_argument("--sample-fps", type=number, default=8); p.add_argument("--threshold", type=number, default=0.035)
    p.add_argument("--max-events", type=int, default=12); p.set_defaults(func=analyze)
    for command in ("render", "check", "snapshot"):
        p = sub.add_parser(command); p.add_argument("project"); p.add_argument("--timeout", type=number, default=1800)
        p.add_argument("--name", default="final.mp4"); p.add_argument("--quality", choices=("draft", "looks", "delivery", "high"), default="high")
        p.add_argument("--workers", type=int, default=1); p.add_argument("--at", default="0.5,2,4,6,8")
        p.set_defaults(func=hf)
    p = sub.add_parser("verify"); p.add_argument("video"); p.add_argument("--out")
    p.add_argument("--require-audio", action="store_true"); p.add_argument("--duration", type=number)
    p.add_argument("--timeout", type=number, default=300); p.set_defaults(func=verify)
    p = sub.add_parser("compare"); p.add_argument("reference"); p.add_argument("result")
    p.add_argument("--out", required=True); p.add_argument("--map"); p.set_defaults(func=compare)
    args = parser.parse_args(argv)
    try:
        if getattr(args, "max_events", 1) < 1 or getattr(args, "workers", 1) < 1:
            raise ValueError("Event/worker counts must be positive")
        print(json.dumps(args.func(args), ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
