import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "fitness-coach-r2"
WEEK_PLAN = ROOT / "tests" / "fixtures" / "week-plan" / "complete.json"
GENERATOR = ROOT / "scripts" / "generate_week_plan.py"
REQUIRED_SECTIONS = ("purpose", "load", "scope", "deny", "procedure", "done")
SKILLS = {
    "dispatcher": ROOT / "SKILL.md",
    "profile": ROOT / ".agents" / "skills" / "fitness-coach-profile" / "SKILL.md",
    "planning": ROOT / ".agents" / "skills" / "fitness-coach-planning" / "SKILL.md",
    "analyze": ROOT / ".agents" / "skills" / "fitness-coach-analyze" / "SKILL.md",
    "plan": ROOT / ".agents" / "skills" / "fitness-coach-plan" / "SKILL.md",
}


def parse_frontmatter(text):
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if line and not line.startswith(" "):
            key, separator, value = line.partition(":")
            if separator:
                fields[key] = value.strip()
    return fields


class FitnessCoachR2ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skills = {name: path.read_text(encoding="utf-8") for name, path in SKILLS.items()}

    def assert_contains_all(self, document, fragments):
        document = re.sub(r"\s+", " ", document)
        for fragment in fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(re.sub(r"\s+", " ", fragment), document)

    def test_all_skill_contracts_have_valid_frontmatter_and_required_sections(self):
        for key, document in self.skills.items():
            with self.subTest(skill=key):
                frontmatter = parse_frontmatter(document)
                self.assertEqual(frontmatter["name"], "fitness-coach" if key == "dispatcher" else f"fitness-coach-{key}")
                self.assertTrue(frontmatter["description"])
                headings = re.findall(r"^## ([a-z]+)$", document, re.MULTILINE)
                self.assertEqual(headings, list(REQUIRED_SECTIONS))

    def test_dispatcher_validates_skill_and_athlete_before_any_profile_read(self):
        document = self.skills["dispatcher"]
        self.assert_contains_all(document, (
            "Validate `<skill>` before inspecting `Profiles/` or reading any athlete file.",
            "Missing or invalid skill: output only",
            "Do not inspect `Profiles/`.",
            "Missing athlete name after a valid skill: list only basenames of immediate",
            "directories under `Profiles/`, without reading their files.",
            "If `Profiles/` is missing or has no immediate directories",
        ))

        with tempfile.TemporaryDirectory() as directory:
            profiles = Path(directory) / "Profiles"
            self.assertFalse(profiles.exists())
            profiles.mkdir()
            self.assertEqual([path.name for path in profiles.iterdir() if path.is_dir()], [])
            (profiles / "Atleta Uno").mkdir()
            self.assertEqual([path.name for path in profiles.iterdir() if path.is_dir()], ["Atleta Uno"])
            (profiles / "Atleta Due").mkdir()
            self.assertEqual(
                sorted(path.name for path in profiles.iterdir() if path.is_dir()),
                ["Atleta Due", "Atleta Uno"],
            )

    def test_dispatcher_rejects_unsafe_or_ambiguous_names_and_routes_exactly_once(self):
        document = self.skills["dispatcher"]
        self.assert_contains_all(document, (
            "Accept complete, case-sensitive athlete directory basenames, including",
            "Reject absolute paths; names containing `/` or `\\`; names equal to `.` or",
            "partial or fuzzy matches; case-insensitive matches; and any",
            "Match `<Nome>` exactly to one real, immediate directory under `Profiles/`.",
            "Exactly one internal skill received the request",
        ))
        for public, internal in (
            ("profile", "fitness-coach-profile"),
            ("planning", "fitness-coach-planning"),
            ("analyze", "fitness-coach-analyze"),
            ("plan", "fitness-coach-plan"),
        ):
            self.assertIn(f"`{public}` | `.agents/skills/{internal}/SKILL.md`", document)

    def test_profile_contract_requires_full_interview_two_confirmations_and_atomic_publish(self):
        document = self.skills["profile"]
        self.assert_contains_all(document, (
            "Blocks A-I, in exact order",
            "at most 4-5 per message",
            "This first confirmation never authorizes writes.",
            "Ask a second explicit confirmation",
            "Missing/negative answer causes no writes.",
            "one unique temporary directory inside",
            "atomic no-replace rename",
            "Never overwrite or merge an existing destination.",
            "Plan week: W0",
            "fitness-coach-planning",
        ))

    def test_planning_contract_covers_initial_revision_expiry_duration_and_rollback(self):
        document = self.skills["planning"]
        self.assert_contains_all(document, (
            "Initial mode requires a complete canonical `profile.md`, `Plan week: W0`",
            "current date later than the inclusive `Plan end`",
            "Select exactly `3`, `6`, `9` or `12` months",
            "athlete may express a preference but",
            "including `Plan week: W1`",
            "history/plans/<old-cycle-start>-<old-duration>m.md",
            "atomic no-replace rename",
            "rollback-protected transaction",
            "Failure or refusal left pre-request athlete state unchanged",
        ))

    def test_analyze_contract_covers_complete_reports_w1_w2_archives_and_plan_protection(self):
        document = self.skills["analyze"]
        self.assert_contains_all(document, (
            "Require every session prescribed for that week",
            "Preserve every original report datum.",
            "W1 requires no existing `history/last-week.md`",
            "W2 and later require one valid previous `last-week.md`",
            "history/weeks/W<N-1>-<previous-final-date>.md",
            "Never overwrite an existing weekly archive.",
            "Do not modify `plan.md`",
            "field-by-field round trip",
            "Plan week` from W<N> to exactly W<N+1>",
            "byte-exact `plan.md`",
            "rollback-protected logical transaction",
        ))

    def test_plan_contract_covers_week_source_canonical_paths_json_html_and_rollback(self):
        document = self.skills["plan"]
        self.assert_contains_all(document, (
            "Derive N exclusively from the one exact `Plan week: W<N>` field",
            "Profiles/<Nome>/artifacts/week-W<N>.json",
            "Profiles/<Nome>/artifacts/week-W<N>.html",
            "JSON as canonical",
            "HTML only when explicitly requested",
            "python3 scripts/generate_week_plan.py <temp-json>",
            "python3 scripts/generate_week_plan.py <temp-json> --output <temp-html>",
            "rollback-protected logical transaction",
            "restore every pre-existing canonical artifact",
            "leave no transaction temporary",
        ))

    def test_anonymous_fixtures_cover_canonical_w0_w1_w2_states(self):
        profiles = {
            week: (FIXTURES / f"profile-{week.lower()}.md").read_text(encoding="utf-8")
            for week in ("W0", "W1", "W2")
        }
        for week, profile in profiles.items():
            with self.subTest(week=week):
                self.assertEqual(parse_frontmatter(profile)["updated"], "2026-07-01")
                self.assertIn("# Profilo — Atleta Test", profile)
                self.assertIn(f"- Plan week: {week}", profile)
                for heading in (
                    "Dati fisici", "Livello e contesto", "Obiettivi", "Benchmarks",
                    "Infortuni e limitazioni", "Preferenze", "Stato piano", "Flags",
                ):
                    self.assertIn(f"## {heading}", profile)
        self.assertIn("- Plan start: non impostato", profiles["W0"])
        self.assertIn("- Last log: mai", profiles["W1"])
        self.assertIn("- Last log: 2026-07-07", profiles["W2"])

    def test_anonymous_plan_and_reports_match_cycle_and_history_contracts(self):
        plan = (FIXTURES / "plan.md").read_text(encoding="utf-8")
        self.assertEqual(parse_frontmatter(plan)["duration_months"], "6")
        for heading in ("Ciclo", "Obiettivo", "Struttura", "Sessioni", "Progressione", "Note coach"):
            self.assertIn(f"## {heading}", plan)

        for filename, week, final_date in (
            ("last-week-w1.md", "W1", "2026-07-07"),
            ("report-w2.md", "W2", "2026-07-14"),
        ):
            report = (FIXTURES / filename).read_text(encoding="utf-8")
            self.assertIn(f"# Report settimana {week} — Atleta Test", report)
            self.assertIn(f"- Data report: {final_date}", report)
            for heading in ("Dati giornalieri", "Metriche", "Dolore e mobilità", "Note atleta", "Analisi coach"):
                self.assertIn(f"## {heading}", report)

    def test_real_pipeline_round_trips_same_payload_at_canonical_paths(self):
        expected = json.loads(WEEK_PLAN.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            artifacts = Path(directory) / "Profiles" / "Atleta Test" / "artifacts"
            artifacts.mkdir(parents=True)
            source = artifacts / "week-W1.json"
            output = artifacts / "week-W1.html"
            shutil.copyfile(WEEK_PLAN, source)

            validate = subprocess.run(
                [sys.executable, str(GENERATOR), str(source)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(validate.returncode, 0, validate.stderr)
            generate = subprocess.run(
                [sys.executable, str(GENERATOR), str(source), "--output", str(output)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(generate.returncode, 0, generate.stderr)

            html = output.read_text(encoding="utf-8")
            match = re.search(
                r'<script id="week-plan-data" type="application/json">(.*?)</script>',
                html,
                re.DOTALL,
            )
            self.assertIsNotNone(match)
            self.assertEqual(json.loads(source.read_text(encoding="utf-8")), expected)
            self.assertEqual(json.loads(match.group(1)), expected)
            self.assertNotIn("__WEEK_PLAN_JSON__", html)
            self.assertEqual(list(artifacts.glob("*.tmp")), [])
            self.assertEqual(source.relative_to(Path(directory)).as_posix(), "Profiles/Atleta Test/artifacts/week-W1.json")
            self.assertEqual(output.relative_to(Path(directory)).as_posix(), "Profiles/Atleta Test/artifacts/week-W1.html")

    def test_pipeline_error_preserves_previous_html_and_leaves_no_temporary(self):
        with tempfile.TemporaryDirectory() as directory:
            artifacts = Path(directory) / "Profiles" / "Atleta Test" / "artifacts"
            artifacts.mkdir(parents=True)
            source = artifacts / "week-W1.json"
            output = artifacts / "week-W1.html"
            source.write_text('{"schemaVersion":"invalid"}', encoding="utf-8")
            output.write_bytes(b"previous-html")

            result = subprocess.run(
                [sys.executable, str(GENERATOR), str(source), "--output", str(output)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_bytes(), b"previous-html")
            self.assertEqual(list(artifacts.glob("*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
