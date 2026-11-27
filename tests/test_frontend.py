"""Automated WCAG accessibility, security, and functional checks for SmogSense AI."""

import unittest
from pathlib import Path

HTML_PATH = Path(__file__).resolve().parent.parent / "index.html"
DOCKERFILE_PATH = Path(__file__).resolve().parent.parent / "Dockerfile"


class TestSmogSenseFrontend(unittest.TestCase):
    def test_html_has_accessibility_landmarks_and_labels(self):
        html = HTML_PATH.read_text(encoding="utf-8")
        self.assertIn('lang="en"', html)
        self.assertIn("<h1", html)
        self.assertIn('href="#main-content"', html)
        self.assertIn('id="main-content"', html)
        self.assertIn('role="tablist"', html)
        self.assertIn('role="tabpanel"', html)
        self.assertIn('role="dialog"', html)
        self.assertIn('aria-modal="true"', html)
        self.assertIn('aria-live="polite"', html)
        self.assertIn('aria-label="Phase 1:', html)
        self.assertIn('aria-label="Close health audit modal"', html)

    def test_html_avoids_blocking_alerts_and_escapes_chat(self):
        html = HTML_PATH.read_text(encoding="utf-8")
        self.assertNotIn("alert(", html)
        self.assertIn("escapeHtml(", html)
        self.assertIn("showToast(", html)

    def test_dockerfile_sets_security_headers(self):
        dockerfile = DOCKERFILE_PATH.read_text(encoding="utf-8")
        self.assertIn("X-Frame-Options", dockerfile)
        self.assertIn("X-Content-Type-Options", dockerfile)
        self.assertIn("Content-Security-Policy", dockerfile)
        self.assertIn("Strict-Transport-Security", dockerfile)


if __name__ == "__main__":
    unittest.main()
