import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from studia import HTML, app


class StudiaWebTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_homepage_references_separate_local_assets(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn('href="static/studia.css?v=7"', page)
        self.assertIn('src="static/studia.js?v=7"', page)
        self.assertNotIn("<style>", page)
        self.assertNotIn("<script>\n", page)

    def test_first_visit_onboarding_and_permanent_tutorial_are_present(self):
        self.assertIn('id="introOverlay"', HTML)
        self.assertIn('id="startJourneyBtn"', HTML)
        self.assertIn('id="skipIntroBtn"', HTML)
        self.assertIn('id="onboardingChecklist"', HTML)
        self.assertIn('data-view="tutorial"', HTML)
        self.assertIn('id="view-tutorial"', HTML)

        javascript = (PROJECT_ROOT / "static" / "studia.js").read_text(
            encoding="utf-8"
        )
        self.assertIn('const ONBOARDING_KEY="studia_onboarding_v1"', javascript)
        self.assertIn("function startGuidedTour", javascript)
        self.assertIn("function renderOnboarding()", javascript)
        self.assertIn("onboardingState.scheduleVisited=true", javascript)
        self.assertIn("onboardingState.tourCompleted=true", javascript)

    def test_standalone_sound_control_is_removed(self):
        self.assertNotIn('id="soundToggle"', HTML)
        javascript = (PROJECT_ROOT / "static" / "studia.js").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("function playSound(", javascript)
        self.assertNotIn("studia_sound_enabled_v1", javascript)

    def test_classroom_is_removed_but_deadline_reminders_remain(self):
        self.assertNotIn("Classroom", HTML)
        self.assertNotIn('data-view="classroom"', HTML)
        self.assertIn('data-view="messages"', HTML)
        self.assertIn('id="view-messages"', HTML)

    def test_demo_data_is_separate_and_preserves_personal_tasks(self):
        javascript = (PROJECT_ROOT / "static" / "studia.js").read_text(
            encoding="utf-8"
        )

        self.assertIn('const DEMO_KEY="studia_demo_tasks_v1"', javascript)
        self.assertIn('JSON.stringify(personalTasks)', javascript)
        self.assertIn('JSON.stringify(savedDemoTasks)', javascript)
        self.assertIn("function loadDemoData()", javascript)
        self.assertIn("function removeDemoData()", javascript)
        self.assertIn("demoTasks=[...legacyDemo,...normalized]", javascript)
        self.assertIn("tasks=[...tasks,...demo]", javascript)
        self.assertIn("tasks:tasks.filter(task=>!task.isSample)", javascript)

    def test_calendar_is_local_and_starts_on_monday(self):
        self.assertIn(
            '<div class="weekdays"><div>Sen</div><div>Sel</div><div>Rab</div>',
            HTML,
        )
        javascript = (PROJECT_ROOT / "static" / "studia.js").read_text(
            encoding="utf-8"
        )

        self.assertIn("function taskDayKey(task){return dayKey(new Date(task.deadline))}", javascript)
        self.assertIn("return (date.getDay()+6)%7", javascript)
        self.assertIn("function formatFullDate(date)", javascript)
        self.assertIn('function changeCalendarMonth(delta)', javascript)

    def test_frontend_assets_are_served(self):
        for asset in ("studia.css", "studia.js"):
            with self.subTest(asset=asset):
                response = self.client.get(f"/static/{asset}")
                self.assertEqual(response.status_code, 200)
                self.assertGreater(len(response.data), 0)
                response.close()

    def test_pages_build_has_every_local_asset(self):
        page = HTML
        references = re.findall(r'(?:href|src)="(static/[^"]+)"', page)

        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory)
            (output / "index.html").write_text(page, encoding="utf-8")
            shutil.copytree(PROJECT_ROOT / "static", output / "static")

            self.assertTrue(references)
            for reference in references:
                with self.subTest(reference=reference):
                    self.assertTrue((output / reference.split("?", 1)[0]).is_file())

    def test_browser_source_uses_local_storage_and_real_history(self):
        javascript = (PROJECT_ROOT / "static" / "studia.js").read_text(
            encoding="utf-8"
        )

        self.assertIn('const KEY="studia_tasks_v1"', javascript)
        self.assertIn("function renderCompletionHistory()", javascript)
        self.assertIn('recordActivity(task.done?"completed":"reopened",task)', javascript)
        self.assertNotIn("const vals=[Math.max(0,rate-35)", javascript)

    def test_backup_fixture_has_versioned_restore_payload(self):
        backup = json.loads(
            (PROJECT_ROOT / "tests" / "fixtures" / "backup.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual((backup["format"], backup["version"]), ("studia-backup", 1))
        for key in ("tasks", "activityEvents", "focusSessions", "focusTimer"):
            with self.subTest(key=key):
                self.assertIn(key, backup)


if __name__ == "__main__":
    unittest.main()
