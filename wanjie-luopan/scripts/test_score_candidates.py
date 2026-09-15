#!/usr/bin/env python3
"""Small regression suite for score_candidates.py."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from score_candidates import evaluate, load_candidates


class ScoreCandidatesTest(unittest.TestCase):
    def test_strong_candidate_is_look_now(self) -> None:
        result = evaluate(
            {
                "name": "Useful App",
                "url": "https://github.com/example/useful-app",
                "repo_exists": True,
                "has_code": True,
                "license_status": "permissive",
                "core_dependency_available": True,
                "relevance": 5,
                "novelty": 4,
                "substance": 5,
                "activity": 4,
                "documentation": 4,
                "usage_evidence": 4,
                "legal_safety": 5,
            },
            1,
        )
        self.assertEqual(result["tier"], "look-now")
        self.assertEqual(result["gate_reasons"], [])
        self.assertGreaterEqual(result["score"], 80)

    def test_hard_gate_overrides_high_score(self) -> None:
        candidate = {
            "name": "README Only",
            "url": "https://github.com/example/readme-only",
            "repo_exists": True,
            "has_code": False,
            "license_status": "permissive",
            "core_dependency_available": True,
        }
        candidate.update({field: 5 for field in (
            "relevance", "novelty", "substance", "activity",
            "documentation", "usage_evidence", "legal_safety",
        )})
        result = evaluate(candidate, 1)
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["tier"], "excluded")
        self.assertIn("no substantive code", result["gate_reasons"])

    def test_invalid_rating_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "relevance must be between 0 and 5"):
            evaluate({"name": "Bad", "url": "https://example.com", "relevance": 6}, 1)

    def test_loads_array_and_wrapped_object(self) -> None:
        with TemporaryDirectory() as directory:
            array_path = Path(directory) / "array.json"
            object_path = Path(directory) / "object.json"
            array_path.write_text('[{"name":"A","url":"https://example.com/a"}]', encoding="utf-8")
            object_path.write_text(
                '{"candidates":[{"name":"B","url":"https://example.com/b"}]}',
                encoding="utf-8",
            )
            self.assertEqual(load_candidates(array_path)[0]["name"], "A")
            self.assertEqual(load_candidates(object_path)[0]["name"], "B")


if __name__ == "__main__":
    unittest.main()
