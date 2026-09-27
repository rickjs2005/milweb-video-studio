#!/usr/bin/env python3
"""Read-only technical checks for local video. Not perceptual/editorial QA."""
import argparse
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("Use a finite nonnegative number")
    return number


def positive(value):
    number = nonnegative(value)
    if number == 0:
        raise argparse.ArgumentTypeError("Use a number greater than zero")
    return number


def run(command, timeout):
    result = subprocess.run(command, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=timeout,
                            stdin=subprocess.DEVNULL, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip()[-2000:] or "Media command failed")
    return result.stdout


def duration_of(metadata):
    try:
        value = float(metadata.get("format", {}).get("duration"))
        return value if math.isfinite(value) and value > 0 else None
    except (TypeError, ValueError):
        return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Local media file; URLs are not supported")
    parser.add_argument("--min-duration", type=nonnegative)
    parser.add_argument("--max-duration", type=nonnegative)
    parser.add_argument("--require-audio", action="store_true")
    parser.add_argument("--decode", action="store_true", help="Decode primary video and all audio")
    parser.add_argument("--timeout", type=positive, default=120,
                        help="Seconds allowed per media subprocess (default: 120)")
    args = parser.parse_args(argv)
    if (args.min_duration is not None and args.max_duration is not None
            and args.min_duration > args.max_duration):
        parser.error("--min-duration must not exceed --max-duration")

    report = {
        "file": str(args.file.resolve()),
        "status": "failed",
        "duration_seconds": None,
        "video": [],
        "audio": [],
        "decode": "not_checked",
        "errors": [],
        "limitations": [
            "No visual playback or listening was performed",
            "No semantic scene durations, sync, loudness or rights were checked",
            "Duration is container metadata; stream endpoints may differ",
        ],
    }
    try:
        if not args.file.is_file():
            raise RuntimeError("Input is not an existing local file")
        probe = shutil.which("ffprobe")
        if not probe:
            raise RuntimeError("ffprobe was not found in PATH")
        metadata = json.loads(run([
            probe, "-v", "error", "-protocol_whitelist", "file,pipe",
            "-show_format", "-show_streams", "-of", "json", str(args.file.resolve())
        ], args.timeout))
        streams = metadata.get("streams", [])
        videos = [s for s in streams if s.get("codec_type") == "video"
                  and not s.get("disposition", {}).get("attached_pic")]
        audios = [s for s in streams if s.get("codec_type") == "audio"]
        for stream in videos:
            report["video"].append({k: stream.get(k) for k in (
                "index", "codec_name", "width", "height", "avg_frame_rate",
                "r_frame_rate", "pix_fmt", "color_space", "color_transfer")})
        for stream in audios:
            report["audio"].append({k: stream.get(k) for k in (
                "index", "codec_name", "sample_rate", "channels", "channel_layout")})
        duration = duration_of(metadata)
        report["duration_seconds"] = duration
        if not videos:
            report["errors"].append("No video stream (excluding cover images)")
        if args.require_audio and not audios:
            report["errors"].append("Required audio stream is missing")
        if duration is None:
            report["errors"].append("Valid container duration is unavailable")
        else:
            if args.min_duration is not None and duration < args.min_duration:
                report["errors"].append("Duration is below the requested minimum")
            if args.max_duration is not None and duration > args.max_duration:
                report["errors"].append("Duration exceeds the requested maximum")
        if args.decode:
            report["decode"] = "failed"
            decoder = shutil.which("ffmpeg")
            if not decoder:
                raise RuntimeError("ffmpeg was not found in PATH")
            if not videos:
                raise RuntimeError("Cannot decode primary video: no video stream")
            run([decoder, "-nostdin", "-v", "error", "-xerror",
                 "-protocol_whitelist", "file,pipe", "-i", str(args.file.resolve()),
                 "-map", f"0:{videos[0]['index']}", "-map", "0:a?",
                 "-f", "null", "-"], args.timeout)
            report["decode"] = "passed"
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
        report["errors"].append(str(exc))
    report["status"] = "passed" if not report["errors"] else "failed"
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
