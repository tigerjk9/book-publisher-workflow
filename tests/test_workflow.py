from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "book-publisher" / "scripts"
INIT = SCRIPTS / "init_project.py"
VALIDATE = SCRIPTS / "validate_project.py"
STAGES = ("brief", "research", "plan", "draft", "qa", "release")


def run_script(script: Path, *args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *(str(arg) for arg in args)],
        check=False,
        capture_output=True,
        text=True,
    )


class WorkflowRegressionTests(unittest.TestCase):
    def test_init_refuses_nonempty_directory_without_partial_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "book"
            target.mkdir()
            sentinel = target / "keep.txt"
            sentinel.write_text("keep", encoding="utf-8")

            result = run_script(INIT, target)

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
            self.assertEqual([path.name for path in target.iterdir()], ["keep.txt"])

    def test_complete_stages_reject_empty_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "book"
            self.assertEqual(run_script(INIT, target).returncode, 0)
            state_path = target / "book-project.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["stages"] = {stage: "complete" for stage in STAGES}
            state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

            result = run_script(VALIDATE, target)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("complete stage requires evidence.brief", result.stderr)
            self.assertIn("complete release requires at least one file", result.stderr)

    def test_complete_project_with_evidence_and_outputs_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "book"
            self.assertEqual(run_script(INIT, target, "--title", "Example Book").returncode, 0)

            files = {
                "manuscript/chapter-01.md": "# Chapter 1\n",
                "plan/approved-plan.md": "# Approved plan\n",
                "qa/editorial-report.md": "# Editorial report\n\nPASS\n",
                "dist/release.txt": "release artifact\n",
            }
            for relative, content in files.items():
                path = target / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")

            state_path = target / "book-project.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state.update(
                {
                    "audience": "Adult learners",
                    "purpose": "Build a practical publishing workflow",
                    "writing_style": "Clear and example-led",
                    "status": "complete",
                    "stages": {stage: "complete" for stage in STAGES},
                    "evidence": {
                        "brief": ["brief.md"],
                        "research": ["research/sources.md"],
                        "plan": ["plan/approved-plan.md"],
                        "draft": ["manuscript/chapter-01.md"],
                        "qa": ["qa/editorial-report.md"],
                        "release": ["dist/release.txt"],
                    },
                }
            )
            state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

            result = run_script(VALIDATE, target)

            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
