"""Basic WebGuard app smoke tests."""
import unittest
from app import app


class WebGuardSmokeTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_homepage_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"WebGuard", response.data)

    def test_scan_requires_consent(self):
        response = self.client.post("/api/scan", json={"url": "https://example.com", "mode": "public", "consent": False})
        self.assertEqual(response.status_code, 400)

    def test_report_requires_findings(self):
        response = self.client.post("/api/report", json={})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
