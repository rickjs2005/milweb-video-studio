"""Integration checks using synthetic media; no network or paid services."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path(os.environ.get("MILWEB_SKILL_DIR", ROOT / "skills/milweb-video-studio"))
SCRIPT = SKILL / "scripts/media_audit.py"


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "Requires FFmpeg")
class MediaAuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.directory = Path(cls.temp.name)
        cls.video = cls.directory / "vídeo com áudio.mp4"
        cls.silent = cls.directory / "silent.mp4"
        subprocess.run([
            "ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi", "-i",
            "testsrc2=size=320x180:rate=12", "-f", "lavfi", "-i",
            "sine=frequency=440:sample_rate=48000", "-t", "2", "-c:v", "mpeg4",
            "-c:a", "aac", str(cls.video)
        ], check=True, capture_output=True)
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(cls.video),
                        "-an", "-c:v", "copy", str(cls.silent)],
                       check=True, capture_output=True)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def audit(self, path, *args):
        result = subprocess.run([sys.executable, str(SCRIPT), str(path), *args],
                                capture_output=True, text=True, encoding="utf-8")
        return result.returncode, json.loads(result.stdout)

    def test_decode_unicode_path_and_preserve_original(self):
        before = hashlib.sha256(self.video.read_bytes()).hexdigest()
        code, result = self.audit(self.video, "--require-audio", "--decode",
                                  "--min-duration", "1.9", "--max-duration", "2.2")
        self.assertEqual(code, 0, result)
        self.assertEqual(result["decode"], "passed")
        self.assertEqual(before, hashlib.sha256(self.video.read_bytes()).hexdigest())

    def test_missing_required_audio(self):
        code, result = self.audit(self.silent, "--require-audio")
        self.assertEqual(code, 1)
        self.assertIn("Required audio stream is missing", result["errors"])

    def test_intentional_silence_allowed(self):
        code, result = self.audit(self.silent)
        self.assertEqual(code, 0, result)
        self.assertEqual(result["decode"], "not_checked")

    def test_duration_below_minimum(self):
        code, result = self.audit(self.video, "--min-duration", "25")
        self.assertEqual(code, 1)
        self.assertIn("Duration is below the requested minimum", result["errors"])

    def test_duration_above_maximum(self):
        code, result = self.audit(self.video, "--max-duration", "1")
        self.assertEqual(code, 1)
        self.assertIn("Duration exceeds the requested maximum", result["errors"])

    def test_missing_file(self):
        code, result = self.audit(self.directory / "missing.mp4")
        self.assertEqual(code, 1)
        self.assertTrue(result["errors"])

    def test_corrupt_file(self):
        invalid = self.directory / "corrupt.mp4"
        invalid.write_bytes(b"not a media container")
        code, result = self.audit(invalid, "--decode")
        self.assertEqual(code, 1)
        self.assertNotEqual(result["decode"], "passed")

    def test_invalid_duration_arguments(self):
        for args in [("--min-duration", "nan"), ("--min-duration", "-1"),
                     ("--min-duration", "5", "--max-duration", "2")]:
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, str(SCRIPT), str(self.video), *args],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
