import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app import app as vercel_app
from studia import HTML, app


class StudiaWebTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_homepage_references_separate_local_assets(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn('href="static/studia.css?v=8"', page)
        self.assertIn('src="static/studia.js?v=8"', page)
        self.assertNotIn("<style>", page)
        self.assertNotIn("<script>\n", page)

    def test_vercel_flask_entrypoint_serves_the_existing_app(self):
        self.assertIs(vercel_app, app)
        response = vercel_app.test_client().get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Jadwal & Agenda", response.get_data(as_text=True))

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

    def test_calendar_distinguishes_deadline_states_and_has_selected_date_action(self):
        javascript = (PROJECT_ROOT / "static" / "studia.js").read_text(
            encoding="utf-8"
        )
        stylesheet = (PROJECT_ROOT / "static" / "studia.css").read_text(
            encoding="utf-8"
        )

        for state in (
            "upcoming-event",
            "today-event",
            "overdue-event",
            "completed-event",
        ):
            with self.subTest(state=state):
                self.assertIn(state, javascript)
                self.assertIn(state, stylesheet)
        self.assertIn('aria-pressed="${selected}"', javascript)
        self.assertIn('aria-current="date"', javascript)
        self.assertIn('statusParts.push(`${overdueCount} terlambat`)', javascript)
        self.assertIn('statusParts.push(`${todayCount} hari ini`)', javascript)
        self.assertIn('statusParts.push(`${upcomingCount} mendatang`)', javascript)
        self.assertIn('statusParts.push(`${completedCount} selesai`)', javascript)
        self.assertIn("function addTaskForSelectedDate()", javascript)
        self.assertIn("Tambah tugas pada tanggal ini", javascript)
        self.assertIn("formatFullDate(new Date(t.deadline))", javascript)
        self.assertIn("function importanceLabel(value)", javascript)
        self.assertIn("Mendatang", HTML)
        self.assertIn("Terlambat", HTML)

    def test_indonesian_labels_and_backup_scope_are_clear(self):
        self.assertIn("Tugas Saya", HTML)
        self.assertIn("Jadwal & Agenda", HTML)
        self.assertIn("Unduh Daftar Tugas", HTML)
        self.assertIn("Simpan Salinan Data", HTML)
        self.assertIn("Pulihkan dari File Cadangan", HTML)
        self.assertIn("Data Demo tetap dipertahankan.", HTML)
        self.assertIn('aria-expanded="false" aria-controls="notificationModal"', HTML)
        self.assertIn('aria-expanded="false">☰</button>', HTML)
        javascript = (PROJECT_ROOT / "static" / "studia.js").read_text(
            encoding="utf-8"
        )
        self.assertIn("Tenggat", javascript)
        self.assertIn("const activeDialog=document.querySelector", javascript)

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
