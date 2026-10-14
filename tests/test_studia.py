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
        self.assertIn('href="static/studia.css?v=2"', page)
        self.assertIn('src="static/studia.js?v=2"', page)
        self.assertNotIn("<style>", page)
        self.assertNotIn("<script>\n", page)

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
