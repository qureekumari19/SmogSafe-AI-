import json
import unittest
import urllib.request

FE = "https://smogsense-ai-460300800672.asia-south1.run.app/"
BE = "https://vayu-saathi-460300800672.asia-south1.run.app"


class TestLiveDeployment(unittest.TestCase):
    def test_frontend_live_and_secure_headers(self):
        with urllib.request.urlopen(FE, timeout=15) as resp:
            self.assertEqual(resp.status, 200)
            h = {k.lower(): v for k, v in resp.headers.items()}
            self.assertEqual(h.get("x-frame-options"), "DENY")
            self.assertEqual(h.get("x-content-type-options"), "nosniff")
            self.assertIn("content-security-policy", h)

    def test_backend_health_and_chat_guardrail(self):
        with urllib.request.urlopen(f"{BE}/health", timeout=15) as resp:
            self.assertEqual(resp.status, 200)
            self.assertEqual(json.loads(resp.read())["status"], "ok")

        body = json.dumps({
            "city": "Delhi NCR",
            "profile_summary": "2 adults, 1 child",
            "aqi_summary": "AQI 384",
            "question": "Predict the cricket match for India vs Pakistan",
            "history": [],
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{BE}/api/chat",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            self.assertEqual(resp.status, 200)
            reply = json.loads(resp.read())
            self.assertFalse(reply["is_relevant"])
            self.assertIn("Irrelevant question", reply["reply"])


if __name__ == "__main__":
    unittest.main()
