import os
import tempfile
import unittest
from pathlib import Path

os.environ["OUTPUT_DIR"] = tempfile.mkdtemp(prefix="automatedreels-tests-")

from app import (  # noqa: E402
    GENERATE_RATE_LIMIT,
    OUTPUT_RETENTION_SECONDS,
    GenerateRequest,
    cleanup_expired_outputs,
    generation_retry_after,
    is_allowed_pexels_video_url,
    _rate_buckets,
    _rate_lock,
)


class GenerationGuardTests(unittest.TestCase):
    def setUp(self):
        with _rate_lock:
            _rate_buckets.clear()

    def test_rate_limit_blocks_and_expires(self):
        key = "test-client"
        for tick in range(GENERATE_RATE_LIMIT):
            self.assertEqual(generation_retry_after(key, now=float(tick)), 0)
        self.assertGreater(generation_retry_after(key, now=10.0), 0)
        self.assertEqual(generation_retry_after(key, now=901.0), 0)

    def test_request_rejects_unsupported_duration(self):
        with self.assertRaises(Exception):
            GenerateRequest(topic="valid topic", duration=999)

    def test_only_https_pexels_hosts_are_accepted(self):
        self.assertTrue(is_allowed_pexels_video_url("https://videos.pexels.com/video-files/1.mp4"))
        for url in ("http://videos.pexels.com/a.mp4", "https://127.0.0.1/a.mp4",
                    "https://pexels.com.attacker.example/a.mp4", "file:///etc/passwd"):
            self.assertFalse(is_allowed_pexels_video_url(url))

    def test_expired_outputs_are_removed_but_recent_ones_remain(self):
        with tempfile.TemporaryDirectory() as folder:
            old = Path(folder) / "old.mp4"
            recent = Path(folder) / "recent.mp4"
            old.write_bytes(b"old")
            recent.write_bytes(b"recent")
            now = OUTPUT_RETENTION_SECONDS + 200.0
            os.utime(old, (100.0, 100.0))
            os.utime(recent, (now - 100.0, now - 100.0))
            removed = cleanup_expired_outputs(Path(folder), now=now)
            self.assertEqual(removed, 1)
            self.assertFalse(old.exists())
            self.assertTrue(recent.exists())


if __name__ == "__main__":
    unittest.main()
