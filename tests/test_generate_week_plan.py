import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "week-plan" / "complete.json"
sys.path.insert(0, str(ROOT / "scripts"))

import generate_week_plan as generator


class GenerateWeekPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.schema = json.loads(generator.SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.template = generator.TEMPLATE_PATH.read_text(encoding="utf-8")

    def render(self, plan=None, template=None):
        return generator.render(
            copy.deepcopy(self.plan if plan is None else plan),
            self.schema,
            self.template if template is None else template,
        )

    def assert_rejected(self, plan):
        with self.assertRaises(generator.GenerationError):
            self.render(plan)

    def test_complete_fixture_is_valid_and_covers_all_exercise_types(self):
        html = self.render()
        types = {
            exercise["type"]
            for session in self.plan["sessions"]
            for exercise in session["exercises"]
        }
        self.assertEqual(types, {"reps", "time", "dist", "mobility"})
        self.assertNotIn(generator.MARKER, html)

    def test_missing_required_field_is_rejected(self):
        plan = copy.deepcopy(self.plan)
        del plan["athlete"]
        self.assert_rejected(plan)

    def test_wrong_type_is_rejected(self):
        plan = copy.deepcopy(self.plan)
        plan["week"]["number"] = "1"
        self.assert_rejected(plan)

    def test_wrong_schema_version_is_rejected(self):
        plan = copy.deepcopy(self.plan)
        plan["schemaVersion"] = "2.0"
        self.assert_rejected(plan)

    def test_invalid_exercise_variants_are_rejected(self):
        for invalid_type in ("weight", 1, None):
            with self.subTest(invalid_type=invalid_type):
                plan = copy.deepcopy(self.plan)
                plan["sessions"][0]["exercises"][0]["type"] = invalid_type
                self.assert_rejected(plan)

    def test_template_marker_must_occur_exactly_once(self):
        for template in ("<html></html>", generator.MARKER * 2):
            with self.subTest(template=template):
                with self.assertRaises(generator.GenerationError):
                    self.render(template=template)

    def test_script_closing_payload_is_safe_and_round_trips_exactly(self):
        plan = copy.deepcopy(self.plan)
        plan["goal"] = "Test </script><script>alert('x')</script>"
        html = self.render(plan)
        self.assertNotIn(generator.MARKER, html)
        self.assertNotIn("</script><script>alert", html)
        match = re.search(
            r'<script id="week-plan-data" type="application/json">(.*?)</script>',
            html,
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        self.assertEqual(json.loads(match.group(1)), plan)

    def test_generation_error_creates_no_partial_output_or_temporary(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            output = directory / "week-W1.html"
            with mock.patch.object(generator, "TEMPLATE_PATH", directory / "missing.html"):
                with self.assertRaises(generator.GenerationError):
                    generator.generate(FIXTURE, output)
            self.assertFalse(output.exists())
            self.assertEqual(list(directory.glob("*.tmp")), [])

    def test_replace_error_preserves_existing_output_and_cleans_temporary(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            output = directory / "week-W1.html"
            output.write_text("previous", encoding="utf-8")
            with mock.patch.object(generator.os, "replace", side_effect=OSError("forced")):
                with self.assertRaises(generator.GenerationError):
                    generator.generate(FIXTURE, output)
            self.assertEqual(output.read_text(encoding="utf-8"), "previous")
            self.assertEqual(list(directory.glob("*.tmp")), [])

    def test_real_cli_writes_standalone_html_to_expected_temporary_path(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / "week-W1.json"
            output = directory / "week-W1.html"
            source.write_bytes(FIXTURE.read_bytes())
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "generate_week_plan.py"), str(source), "--output", str(output)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(source.read_text(encoding="utf-8")), self.plan)
            html = output.read_text(encoding="utf-8")
            self.assertIn("<!DOCTYPE html>", html)
            self.assertIn('id="week-plan-data"', html)
            self.assertNotIn(generator.MARKER, html)

    def test_real_cli_without_output_only_validates(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / "week-W1.json"
            source.write_bytes(FIXTURE.read_bytes())
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "generate_week_plan.py"), str(source)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(list(directory.iterdir()), [source])

    def test_validation_does_not_read_template(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.html"
            with mock.patch.object(generator, "TEMPLATE_PATH", missing):
                generator.generate(FIXTURE)

    def test_generic_app_has_import_and_week_scoped_storage(self):
        self.assertIn('accept=".json,application/json"', self.template)
        self.assertIn("plan.plan.id+'_W'+plan.week.number", self.template)
        self.assertIn("fitness_log_v4_last_plan", self.template)
        self.assertIn("I log della settimana attiva saranno cancellati", self.template)

    def test_generic_app_separates_functions_from_ordered_page_bar(self):
        self.assertIn('id="functionsButton"', self.template)
        self.assertIn('id="page-functions"', self.template)
        self.assertIn("tabBar.appendChild(tab)", self.template)
        self.assertIn("showPage('functions')", self.template)
        self.assertIn("grid-template-columns:minmax(0,30fr) minmax(0,20fr) minmax(0,45fr)", self.template)
        self.assertNotIn('id="tab-functions"', self.template)
        self.assertNotIn('class="bottom-nav"', self.template)
        self.assertNotIn('id="nav-train"', self.template)
        self.assertNotIn('id="nav-report"', self.template)
        self.assertNotIn('class="plan-actions"', self.template)

    def test_generic_app_uses_cozy_typewriter_dark_palette(self):
        colors = ("#372d29", "#2b2723", "#413632", "#2e2420", "#504431", "#645743",
                  "#ccc2b7", "#b2a699", "#868074", "#ba945f", "#e0ba86", "#e77a59",
                  "#c72626", "#6154508f")
        for color in colors:
            self.assertIn(color, self.template)
        self.assertIn('<meta name="theme-color" content="#372d29">', self.template)

    def test_generic_app_has_single_download_flow(self):
        self.assertEqual(self.template.count(generator.MARKER), 1)
        self.assertIn("function importPlanFile", self.template)
        self.assertIn("function downloadReport", self.template)
        for removed in ("navigator.clipboard", "copyReport", "saveConfig", "reportOutput", "week-config", "lastReport"):
            self.assertNotIn(removed, self.template)

    def test_git_ignore_rules_protect_artifacts_only(self):
        ignored = subprocess.run(
            [
                "git",
                "check-ignore",
                "Profiles/Example/profile.md",
                "Profiles/Example/artifacts/week-W1.json",
                "Profiles/Example/artifacts/week-W1.html",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(ignored.returncode, 0, ignored.stderr)
        self.assertEqual(len(ignored.stdout.splitlines()), 3)

        sources = [
            ".ai-project/local/project/roadmap/plans/R1/R1.5.md",
            "assets/week-plan.schema.json",
            "scripts/generate_week_plan.py",
            "assets/fitness-coach-log.html",
            "tests/test_generate_week_plan.py",
        ]
        visible = subprocess.run(
            ["git", "check-ignore", *sources],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(visible.returncode, 1, visible.stdout)

    def test_week_plan_documentation_enforces_json_to_html_contract(self):
        dispatcher = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        skill = (ROOT / ".agents" / "skills" / "fitness-coach-plan" / "SKILL.md").read_text(encoding="utf-8")
        validate_command = "python3 scripts/generate_week_plan.py <temp-json>"
        html_command = f"{validate_command} --output <temp-html>"

        self.assertIn("`plan` | `.agents/skills/fitness-coach-plan/SKILL.md`", dispatcher)
        self.assertIn("Derive N exclusively", skill)
        self.assertIn("JSON as canonical", skill)
        self.assertIn("JSON-only publication removes an existing HTML", skill)
        self.assertIn(validate_command, skill)
        self.assertIn(html_command, skill)
        self.assertIn("Require exit status zero", skill)


if __name__ == "__main__":
    unittest.main()
