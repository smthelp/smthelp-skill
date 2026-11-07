"""Offline tests for 1.2.0 contract features:  python3 -m unittest discover -s tests"""
import json, re, shutil, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from p3cv import __version__                                   # noqa: E402
from p3cv.config import Config, CONFIG_SCHEMA                  # noqa: E402
from p3cv.errors import P3VError                               # noqa: E402
from p3cv.stages.landing import apply_replacements, leftovers  # noqa: E402
from p3cv.contract import envelope, migrate, manifest, kind_of  # noqa: E402
from p3cv.cli import main as cli                               # noqa: E402


class Contract(unittest.TestCase):
    def test_versions_agree(self):
        sk = json.loads((ROOT / "skill.json").read_text())
        fm = re.search(r"^version:\s*(\S+)", (ROOT / "SKILL.md").read_text(), re.M).group(1)
        self.assertEqual(sk["version"], __version__); self.assertEqual(fm, __version__)
        self.assertEqual(sk["config_schema"], CONFIG_SCHEMA)
        self.assertIn(f"## [{__version__}]", (ROOT / "CHANGELOG.md").read_text())

    def test_skill_json_outputs_and_stages(self):
        sk = json.loads((ROOT / "skill.json").read_text())
        from p3cv.stages import load_all, ORDER
        load_all(); self.assertEqual(sk["contract"]["stages"], ORDER)
        for f in sk["outputs"]["files"]:
            self.assertIn("kind", f)

    def test_replacements(self):
        page = "<title>S7020 FAB</title><h1>S7020</h1>"
        out = apply_replacements(page, [["<title>S7020 FAB</title>", "<title>S7040P</title>"],
                                        {"find": "S7020", "replace": "S7040P", "count": 1}])
        self.assertEqual(out, "<title>S7040P</title><h1>S7040P</h1>")
        with self.assertRaises(P3VError) as e:
            apply_replacements(page, [["missing", "x"]])
        self.assertEqual(e.exception.code, "E_ASSEMBLE")
        self.assertEqual(len(leftovers("a S7020 b S7020", ["S7020"])), 2)

    def test_bad_replacement_config(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "product.json"; raw = json.loads((ROOT / "config/product.example.json").read_text())
            raw["landing"]["replacements"] = ["oops"]; p.write_text(json.dumps(raw))
            with self.assertRaises(P3VError):
                Config(p)

    def test_schema_too_new(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "product.json"; raw = json.loads((ROOT / "config/product.example.json").read_text())
            raw["schema_version"] = CONFIG_SCHEMA + 1; p.write_text(json.dumps(raw))
            with self.assertRaises(P3VError) as e:
                Config(p)
            self.assertIn("upgrade", e.exception.hint)

    def test_migrate_and_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "product.json"; shutil.copy(ROOT / "config/product.example.json", p)
            raw = json.loads(p.read_text()); raw.pop("schema_version", None); p.write_text(json.dumps(raw))
            r = migrate(p); self.assertEqual(r["to"], CONFIG_SCHEMA); self.assertTrue(r["steps"])
            self.assertEqual(json.loads(p.read_text())["schema_version"], CONFIG_SCHEMA)
            self.assertFalse(migrate(p)["steps"])
            cfg = Config(p); (Path(d) / "out").mkdir()
            (Path(d) / "out" / f"youtube-thumbnail-{cfg.slug}.jpg").write_bytes(b"x")
            m = manifest(cfg)
            self.assertEqual(m["files"][0]["kind"], "thumbnail"); self.assertIn("landing_html", m["missing"])
            self.assertEqual(kind_of("a_16x9_4K.mp4"), "video_16x9")

    def test_envelope(self):
        e = envelope("/tmp/x/product.json", "pending", {}, {"code": "E_PENDING", "message": "m", "hint": None})
        self.assertEqual(e["exit_code"], 3); self.assertEqual(e["version"], __version__)
        self.assertEqual(envelope("/tmp/x/product.json", "ok")["exit_code"], 0)

    def test_cli_info(self):
        self.assertEqual(cli(["info"]), 0)

    def test_relabel(self):
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            self.skipTest("Pillow missing")
        from p3cv.tools.relabel import relabel
        with tempfile.TemporaryDirectory() as d:
            im = Image.new("RGB", (200, 80), (230, 232, 236)); ImageDraw.Draw(im).rectangle([40, 30, 140, 50], fill=(50, 70, 140))
            src = Path(d) / "a.jpg"; im.save(src)
            r = relabel(src, Path(d) / "b.jpg", (40, 30, 140, 50), "S7040P")
            self.assertTrue((Path(d) / "b.jpg").exists()); self.assertTrue(r["bg"].startswith("#e"))


if __name__ == "__main__":
    unittest.main()
