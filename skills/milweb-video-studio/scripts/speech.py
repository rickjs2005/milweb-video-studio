#!/usr/bin/env python3
"""Optional local speech and captions. No hosted speech service or API fallback."""
import argparse
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from studio import binary, fresh_output, media, number, run, write_json


def stamp(seconds):
    if not math.isfinite(seconds) or seconds < 0:
        raise ValueError("Subtitle timestamps must be finite and nonnegative")
    ms = round(seconds * 1000)
    hours, ms = divmod(ms, 3600000)
    minutes, ms = divmod(ms, 60000)
    seconds, ms = divmod(ms, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{ms:03}"


def write_srt(path, cues):
    previous = 0
    lines = []
    for i, cue in enumerate(cues, 1):
        a, b, text = cue["start"], cue["end"], cue["text"].strip()
        if not text or not all(math.isfinite(x) for x in (a, b)) or a < previous or a < 0 or b <= a:
            raise ValueError("Cues must have text and ordered, non-overlapping positive ranges")
        lines.append(f"{i}\n{stamp(a)} --> {stamp(b)}\n{text}\n")
        previous = b
    if not lines:
        raise ValueError("No speech cues; inspect the audio instead of inventing captions")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def transcribe(args):
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError("Install the optional local backend: python -m pip install faster-whisper") from exc
    source = Path(args.audio).resolve(strict=True)
    output = fresh_output(args.out, source)
    metadata = fresh_output(output.with_suffix(".json"), source)
    if metadata == output:
        raise ValueError("Subtitle output must use a different extension from its .json metadata")
    if args.offset < 0 or not math.isfinite(args.offset):
        raise ValueError("Offset must be finite and nonnegative")
    model = WhisperModel(args.model, device=args.device, compute_type="int8" if args.device == "cpu" else "float16",
                         local_files_only=not args.download_model)
    # Decode through our FFmpeg dependency, avoiding PyAV version-specific open() kwargs.
    import numpy as np
    pcm = run([binary("ffmpeg"), "-nostdin", "-v", "error", "-protocol_whitelist", "file,pipe",
               "-i", source, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "pipe:1"]).stdout
    audio = np.frombuffer(pcm, dtype="<f4").copy()
    if audio.size == 0:
        raise ValueError("Audio decoded to no samples")
    segments, info = model.transcribe(audio, language=args.language, word_timestamps=True, vad_filter=True)
    cues, words = [], []
    for segment in segments:
        cues.append({"start": segment.start + args.offset, "end": segment.end + args.offset, "text": segment.text.strip()})
        for word in segment.words or []:
            words.append({"start": word.start + args.offset, "end": word.end + args.offset, "text": word.word,
                          "probability": word.probability})
    write_srt(output, cues)
    write_json(metadata, {"language": info.language, "cues": cues, "words": words,
        "review": "pending; ASR word timestamps are not forced alignment or guaranteed exact"})
    return {"status": "transcribed", "subtitles": str(output), "language": info.language, "review": "pending"}


def narrate(args):
    try:
        from kokoro_onnx import Kokoro
        import soundfile as sf
    except ImportError as exc:
        raise RuntimeError("Install optional local TTS: python -m pip install kokoro-onnx soundfile") from exc
    source = Path(args.text).resolve(strict=True)
    text = source.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("Narration text is empty")
    model, voices = Path(args.model).resolve(strict=True), Path(args.voices).resolve(strict=True)
    output = fresh_output(args.out, source)
    metadata = fresh_output(output.with_suffix(".json"), source)
    if metadata == output:
        raise ValueError("Audio output must use a different extension from its .json metadata")
    engine = Kokoro(str(model), str(voices))
    samples, rate = engine.create(text, voice=args.voice, speed=args.speed, lang=args.language)
    if len(samples) == 0 or rate <= 0:
        raise ValueError("TTS produced no samples")
    sf.write(str(output), samples, rate)
    result = {"status": "generated", "audio": str(output), "duration": len(samples) / rate,
              "voice": args.voice, "language": args.language, "listening_review": "pending"}
    write_json(metadata, result)
    return result


def burn(args):
    source = Path(args.video).resolve(strict=True)
    subtitles = Path(args.srt).resolve(strict=True)
    output = fresh_output(args.out, source)
    if output == subtitles:
        raise ValueError("Output must not overwrite the subtitle input")
    if not re.fullmatch(r"[A-Za-z0-9 _-]{1,60}", args.font):
        raise ValueError("Font must be a plain font family name")
    canvas = media(source)
    size = args.size if args.size is not None else max(12, round(min(canvas["width"], canvas["height"]) * 0.045))
    if not 8 <= size <= 160:
        raise ValueError("Font size must be between 8 and 160")
    # Fixed relative filter filename avoids Windows drive-colon/filter injection escaping.
    with tempfile.TemporaryDirectory(prefix="milweb-captions-") as tmp:
        work = Path(tmp)
        shutil.copyfile(subtitles, work / "captions.srt")
        # Set ASS script resolution explicitly: otherwise SRT defaults can make 28 units
        # cover a portrait video. Font size and margins here are output pixels.
        side = max(8, round(canvas["width"] * 0.06))
        bottom = max(8, round(canvas["height"] / 60))
        style = (f"PlayResX={canvas['width']},PlayResY={canvas['height']},"
                 f"FontName={args.font},FontSize={size},Outline={max(1, round(size * .045))},"
                 f"Shadow=0,MarginV={bottom},MarginL={side},MarginR={side}")
        run([binary("ffmpeg"), "-nostdin", "-v", "error", "-protocol_whitelist", "file,pipe",
             "-i", source, "-vf", f"subtitles=filename=captions.srt:force_style='{style}'",
             "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac",
             "-movflags", "+faststart", output], cwd=work, timeout=args.timeout)
    return {"status": "captioned", "video": str(output), "text_and_sync_review": "pending"}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    t = sub.add_parser("transcribe"); t.add_argument("audio"); t.add_argument("--out", required=True)
    t.add_argument("--model", default="small"); t.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    t.add_argument("--language"); t.add_argument("--offset", type=float, default=0)
    t.add_argument("--download-model", action="store_true"); t.set_defaults(func=transcribe)
    t = sub.add_parser("narrate"); t.add_argument("text"); t.add_argument("--model", required=True)
    t.add_argument("--voices", required=True); t.add_argument("--voice", default="pf_dora")
    t.add_argument("--language", default="pt-br"); t.add_argument("--speed", type=number, default=1)
    t.add_argument("--out", required=True); t.set_defaults(func=narrate)
    t = sub.add_parser("captions"); t.add_argument("video"); t.add_argument("--srt", required=True)
    t.add_argument("--out", required=True); t.add_argument("--font", default="Arial")
    t.add_argument("--size", type=int, help="Font size in output pixels; defaults to a size based on the canvas")
    t.add_argument("--timeout", type=number, default=300)
    t.set_defaults(func=burn)
    args = p.parse_args(argv)
    try:
        print(json.dumps(args.func(args), ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
