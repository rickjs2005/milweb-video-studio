"""Real local-media integration checks. No network, models or paid APIs."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

SCRIPTS = Path(__file__).resolve().parents[1] / "skills/milweb-video-studio/scripts"
sys.path.insert(0, str(SCRIPTS))
import studio
import speech


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "Requires FFmpeg")
class StudioTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.video = cls.root / "vídeo original com espaço.mp4"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi", "-i",
                        "testsrc2=size=320x180:rate=12", "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000",
                        "-t", "2", "-c:v", "mpeg4", "-c:a", "aac", str(cls.video)], check=True)
        cls.portrait = cls.root / "portrait.mp4"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(cls.video),
                        "-vf", "scale=180:320", "-c:v", "mpeg4", "-an", str(cls.portrait)], check=True)
        cls.original_hash = studio.digest(cls.video)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def cli(self, *args, script="studio.py"):
        result = subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)],
                                capture_output=True, text=True, encoding="utf-8", timeout=90)
        return result

    def test_analysis_preserves_original_and_records_unverified_review(self):
        out = self.root / "análise com espaço"
        result = self.cli("analyze", self.video, "--out", out, "--sample-fps", 6, "--max-events", 2)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = studio.read_json(out / "analysis.json")
        self.assertEqual(data["source_sha256"], self.original_hash)
        self.assertEqual(data["review"]["motion_playback"], "pending")
        self.assertEqual(data["observed"], [])
        self.assertGreater(data["sampling"]["frames_scanned"], 8)
        self.assertTrue((out / "contact-sheet.jpg").is_file())
        self.assertTrue((out / "speech.wav").is_file())
        self.assertTrue(all(0 <= sample["time"] < 2 for sample in data["samples"]))
        # Rerunning must not destroy a human's annotated analysis.
        data["observed"] = ["human annotation"]
        studio.write_json(out / "analysis.json", data)
        again = self.cli("analyze", self.video, "--out", out)
        self.assertNotEqual(again.returncode, 0)
        self.assertEqual(studio.read_json(out / "analysis.json")["observed"], ["human annotation"])
        self.assertEqual(studio.digest(self.video), self.original_hash)

    def test_project_keeps_content_as_data_and_blocks_template_escape(self):
        project = self.root / "projeto com espaço"
        result = self.cli("new", project, "--reference", self.video, "--demo")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((project / "assets/demo.wav").stat().st_size > 0)
        text = "</script><script>alert('content')</script>"
        studio.write_json(project / "content.json", {"headline": text})
        studio.prepare(project)
        rendered = (project / "index.html").read_text(encoding="utf-8")
        self.assertNotIn(text, rendered)
        self.assertIn("\\u003c/script>", rendered)
        job = studio.read_json(project / "project.json")
        job["template"] = "../outside.html"
        studio.write_json(project / "project.json", job)
        with self.assertRaises(ValueError):
            studio.prepare(project)

    def test_decode_and_actual_loudness_measurement(self):
        result = self.cli("verify", self.video, "--require-audio", "--duration", 2)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["decode"], "passed")
        self.assertIsInstance(data["loudness"]["integrated_lufs"], float)
        self.assertEqual(data["review"]["listening"], "pending")
        self.assertNotEqual(self.cli("verify", self.portrait, "--require-audio").returncode, 0)
        self.assertNotEqual(self.cli("verify", self.video, "--duration", 5).returncode, 0)
        self.assertNotEqual(self.cli("verify", self.video, "--out", self.video).returncode, 0)
        self.assertEqual(studio.digest(self.video), self.original_hash)

    def test_empty_project_cannot_be_delivered_as_a_finished_video(self):
        project = self.root / "empty project"
        result = self.cli("new", project)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.cli("render", project)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("empty scaffold", result.stderr)
        self.assertFalse((project / "renders/final.mp4").exists())

    def test_renderer_accepts_user_supplied_integer_and_fractional_fps(self):
        project = self.root / "fps project"
        result = self.cli("new", project, "--demo", "--fps", "12")
        self.assertEqual(result.returncode, 0, result.stderr)
        for fps, expected in [(12.0, "12"), (30000 / 1001, "30000/1001")]:
            job = studio.read_json(project / "project.json")
            job["canvas"]["fps"] = fps
            studio.write_json(project / "project.json", job)
            args = SimpleNamespace(project=project, command="render", name="test.mp4", quality="draft", workers=1, timeout=60)
            with patch.object(studio, "hf_command", return_value=["node", "hyperframes.mjs"]), \
                 patch.object(studio.subprocess, "run", return_value=SimpleNamespace(returncode=0)) as renderer, \
                 patch.object(studio, "media", return_value={}):
                studio.hf(args)
                argv = renderer.call_args.args[0]
                self.assertEqual(argv[argv.index("--fps") + 1], expected)

    def test_comparison_preserves_different_aspect_ratios(self):
        out = self.root / "compare"
        result = self.cli("compare", self.video, self.portrait, "--out", out)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = studio.read_json(out / "comparison.json")
        self.assertEqual(len(data["pairs"]), 6)
        self.assertEqual(data["visual_review"], "pending")
        self.assertEqual(studio.media(out / "comparison.jpg")["width"], 744)

    def test_captions_change_pixels_without_changing_original(self):
        srt = self.root / "legendas revisadas.srt"
        speech.write_srt(srt, [{"start": 0, "end": 1.8, "text": "Conteúdo de teste"}])
        output = self.root / "legendado.mp4"
        result = self.cli("captions", self.video, "--srt", srt, "--out", output, script="speech.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(studio.media(output)["audio"])
        self.assertEqual(studio.digest(self.video), self.original_hash)
        self.assertNotEqual(studio.digest(output), self.original_hash)
        self.assertNotEqual(self.cli("captions", self.video, "--srt", srt, "--out", self.video, script="speech.py").returncode, 0)

    def test_portrait_captions_remain_in_the_lower_part_of_the_frame(self):
        source = self.root / "solid portrait.mp4"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi", "-i",
                        "color=c=0x204060:s=180x320:r=12", "-t", "1", "-c:v", "mpeg4", str(source)], check=True)
        srt = self.root / "portrait captions.srt"
        speech.write_srt(srt, [{"start": 0, "end": 1, "text": "Uma legenda com escala correta."}])
        output = self.root / "captioned portrait.mp4"
        result = self.cli("captions", source, "--srt", srt, "--out", output, script="speech.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        pixels = studio.run(["ffmpeg", "-nostdin", "-v", "error", "-i", output,
                             "-frames:v", "1", "-pix_fmt", "gray", "-f", "rawvideo", "pipe:1"]).stdout
        split = 180 * 224
        self.assertFalse(any(value > 200 for value in pixels[:split]), "Subtitle unexpectedly covers the main scene")
        self.assertTrue(any(value > 200 for value in pixels[split:]), "No visible caption pixels")

    def test_invalid_ranges_and_numbers_are_rejected(self):
        for args in [("analyze", self.video, "--out", self.root / "bad-range", "--start", -1),
                     ("new", self.root / "bad-number", "--duration", "nan"),
                     ("analyze", self.video, "--out", self.root / "bad-events", "--max-events", 0)]:
            self.assertNotEqual(self.cli(*args).returncode, 0)
        with self.assertRaises(ValueError):
            speech.write_srt(self.root / "bad.srt", [{"start": 1, "end": 2, "text": "one"},
                                                    {"start": 1.5, "end": 3, "text": "overlap"}])


if __name__ == "__main__":
    unittest.main()
