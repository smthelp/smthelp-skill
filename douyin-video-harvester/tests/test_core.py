"""Offline unit tests: python3 -m unittest discover -s tests"""
import json, os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dyh import rank, naming, cookies, config, filter as flt
from dyh.errors import DyhError

def aw(i, likes, comments=0, desc="", images=None):
    return {"aweme_id": str(i), "desc": desc, "images": images,
            "statistics": {"digg_count": likes, "comment_count": comments, "share_count": 0, "collect_count": 0}}

class T(unittest.TestCase):
    def test_rank_order(self):
        r = rank.score_all([aw(1, 1), aw(2, 100, 5), aw(3, 10)], config.DEFAULTS["rank"]["weights"])
        self.assertEqual([a["aweme_id"] for a in r], ["2", "3", "1"]); self.assertEqual(r[0]["_rank"], 1)
    def test_naming(self):
        self.assertEqual(naming.check("juki-gripper-smt-nozzle.mp4"), [])
        self.assertTrue(naming.check("01-juki-nozzle.mp4")); self.assertTrue(naming.check("Juki Nozzle.mp4"))
    def test_cookie_filter(self):
        f = tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt")
        f.write(".douyin.com\tTRUE\t/\tTRUE\t0\tsid\tx\n.google.com\tTRUE\t/\tTRUE\t0\tSID\ty\n#HttpOnly_.douyin.com\tTRUE\t/\tTRUE\t0\tttwid\tz\n"); f.close()
        ck = cookies.load_douyin(f.name); self.assertEqual({c["name"] for c in ck}, {"sid", "ttwid"})
    def test_classify(self):
        self.assertEqual(flt.classify("定制吸嘴", ["吸嘴"], ["顶针"]), "keyword_hit")
        self.assertEqual(flt.classify("顶针 吸嘴", ["吸嘴"], ["顶针"]), "excluded_keyword")
    def test_config_requires_run_name(self):
        with self.assertRaises(DyhError): config.load(None, {})
        self.assertEqual(config.load(None, {"run_name": "x"})["run_dir"], "runs/x")

if __name__ == "__main__":
    unittest.main()
