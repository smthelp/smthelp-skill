"""Offline unit tests (no network, no browser):  python3 -m unittest discover -s tests"""
import json, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from p3cv.config import Config                       # noqa: E402
from p3cv.errors import P3VError                     # noqa: E402
from p3cv.stages.download import classify, text_dump  # noqa: E402
from p3cv.stages.subtitles import build_cues, to_srt  # noqa: E402
from p3cv.stages.mix import build_timeline            # noqa: E402
from p3cv.stages.docs import chapters                 # noqa: E402
from p3cv.brand import rgba, lighten                  # noqa: E402
from p3cv.stages import load_all, ORDER, REGISTRY     # noqa: E402


class T(unittest.TestCase):
    def test_example_config_valid(self):
        for p in (ROOT / "examples").glob("*/product.json"):
            cfg = Config(p)
            self.assertTrue(cfg.slug)
        Config(ROOT / "config" / "product.example.json")

    def test_missing_keys(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "product.json"; f.write_text(json.dumps({"slug": "x"}))
            with self.assertRaises(P3VError) as e:
                Config(f)
            self.assertEqual(e.exception.code, "E_CONFIG")

    def test_classify(self):
        self.assertEqual(classify("<html>eDrawings modelContents</html>"), "edrawings")
        self.assertEqual(classify("x THREE.WebGLRenderer y"), "threejs")
        self.assertEqual(classify("<nav></nav><section>"), "landing")
        self.assertEqual(classify("%PDF-1.7"), "pdf")
        self.assertEqual(classify("PK\x03\x04", "a/b.pptx"), "office")
        from p3cv.stages.download import ext_for
        self.assertEqual(ext_for("https://x/y/Deck%20A.pptx"), ".pptx")
        self.assertEqual(ext_for("https://x/y/page.html"), ".html")
        self.assertNotIn("script", text_dump("<p>a</p><script>bad()</script>"))

    def test_cues(self):
        words = [[0.0, 0.3, "Hello"], [0.3, 0.6, "world."], [0.7, 1.0, "Email"], [1.0, 1.2, "info"]]
        cues = build_cues([{"start": 1.0, "text": "Hello world. Email info", "words": words}], 42)
        self.assertEqual(cues[0][2], "Hello world.")
        self.assertAlmostEqual(cues[0][0], 1.0)
        self.assertIn("00:00:01,000 -->", to_srt(cues))

    def test_timeline_and_chapters(self):
        segs, total = build_timeline([2.0, 3.0], 1.0, 0.5, 2.0)
        self.assertEqual(segs[1]["start"], 3.5); self.assertEqual(total, 8.5)
        tl = {"segments": [{"start": 1.2, "chapter": "Intro"}, {"start": 65, "chapter": "Specs"}]}
        self.assertEqual(chapters(tl), ["0:00 Intro", "1:05 Specs"])

    def test_brand(self):
        self.assertEqual(rgba("#00A896", .5), "rgba(0,168,150,0.5)")
        self.assertTrue(lighten("#000000", .5).startswith("#7f"))

    def test_stage_graph(self):
        load_all()
        self.assertEqual(ORDER[0], "download")
        for name, spec in REGISTRY.items():
            for d in spec["deps"]:
                self.assertLess(ORDER.index(d), ORDER.index(name), f"{name} depends on later stage {d}")


if __name__ == "__main__":
    unittest.main()
