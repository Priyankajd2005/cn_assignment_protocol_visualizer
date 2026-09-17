"""
Automated Test Suite for Dual-Panel Activity & Protocol Visualizer
Tests:
1. Browsing simulation structure & DNS/HTTP RFC accuracy
2. Mail simulation structure & SMTP state-machine handshake
3. Streaming simulation structure & HLS playlist / segment chunking
4. Flask REST API endpoints
"""

import unittest
from protocol_engine import ProtocolEngine
from app import app

class TestProtocolVisualizer(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_browsing_simulation(self):
        res = ProtocolEngine.simulate_browsing("https://wikipedia.org/wiki/Application_layer")
        self.assertEqual(res["activity"], "browsing")
        self.assertEqual(res["host"], "wikipedia.org")
        self.assertTrue(len(res["steps"]) >= 4)
        
        # Verify first step is DNS
        first_step = res["steps"][0]
        self.assertEqual(first_step["protocol"], "DNS")
        self.assertEqual(first_step["direction"], "client_to_dns")
        
        # Verify HTTP Request
        http_req = [s for s in res["steps"] if s["protocol"] == "HTTP" and s["direction"] == "client_to_server"][0]
        self.assertIn("GET /wiki/Application_layer HTTP/1.1", http_req["raw_wire"])
        
        # Verify HTTP 200 Response
        http_resp = [s for s in res["steps"] if s["protocol"] == "HTTP" and s["direction"] == "server_to_client"][0]
        self.assertIn("200 OK", http_resp["raw_wire"])

    def test_mail_simulation(self):
        res = ProtocolEngine.simulate_mail("alice@stanford.edu", "Test Subject", "Test Body")
        self.assertEqual(res["activity"], "mail")
        self.assertEqual(res["to"], "alice@stanford.edu")
        
        steps = res["steps"]
        step_titles = [s["title"] for s in steps]
        
        # Check mandatory SMTP states
        self.assertTrue(any("220 Service Ready" in t for t in step_titles))
        self.assertTrue(any("EHLO" in t for t in step_titles))
        self.assertTrue(any("MAIL FROM" in t for t in step_titles))
        self.assertTrue(any("RCPT TO" in t for t in step_titles))
        self.assertTrue(any("DATA" in t for t in step_titles))
        self.assertTrue(any("354 Start Mail Input" in t for t in step_titles))
        self.assertTrue(any("250 Queued" in t for t in step_titles))
        self.assertTrue(any("QUIT" in t for t in step_titles))
        self.assertTrue(any("221 Channel Closed" in t for t in step_titles))

    def test_streaming_simulation(self):
        res = ProtocolEngine.simulate_streaming(quality="1080p", segment_count=3)
        self.assertEqual(res["activity"], "streaming")
        self.assertEqual(res["quality"], "1080p")
        
        steps = res["steps"]
        # Verify master playlist request & response
        self.assertTrue(any("Master Playlist" in s["title"] for s in steps))
        # Verify variant playlist request & response
        self.assertTrue(any("Variant Playlist" in s["title"] for s in steps))
        # Verify segment downloads
        segments = [s for s in steps if "Chunk Delivered" in s["title"]]
        self.assertEqual(len(segments), 3)

    def test_api_endpoints(self):
        # Browse endpoint
        r = self.client.get("/api/protocols/browse?url=https://example.org")
        self.assertEqual(r.status_code, 200)
        json_data = r.get_json()
        self.assertEqual(json_data["host"], "example.org")

        # Mail endpoint
        r = self.client.post("/api/protocols/mail", json={
            "to": "test@mit.edu",
            "subject": "Greetings",
            "body": "Hello MIT!"
        })
        self.assertEqual(r.status_code, 200)
        json_data = r.get_json()
        self.assertIn("queue_id", json_data)

        # Stream endpoint
        r = self.client.get("/api/protocols/stream?quality=720p")
        self.assertEqual(r.status_code, 200)
        json_data = r.get_json()
        self.assertEqual(json_data["quality"], "720p")

        # Health endpoint
        r = self.client.get("/api/health")
        self.assertEqual(r.status_code, 200)

if __name__ == "__main__":
    unittest.main()
