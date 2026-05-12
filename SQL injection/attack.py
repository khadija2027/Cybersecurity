#!/usr/bin/env python3
"""Complete SQL Injection Attack Suite"""

import subprocess
import sys
import os
import time


def run_phase(phase_number, script_name):
    print(f"\n{'='*70}")
    print(f"RUNNING PHASE {phase_number}: {script_name}")
    print(f"{'='*70}\n")

    result = subprocess.run(
        [sys.executable, script_name, "--target", "http://localhost:5001"])
    return result.returncode == 0


def main():
    print("\n" + "="*70)
    print("COMPLETE SQL INJECTION TESTING SUITE")
    print("="*70)
    print("\nTarget: http://localhost:5001")
    print("Make sure the vulnerable backend is running!\n")

    phases = [
        ("01_error_based.py", "Error-Based SQL Injection"),
        ("02_auth_bypass.py", "Authentication Bypass"),
        ("03_union_based.py", "Union-Based SQL Injection"),
        ("04_blind_injection.py", "Blind SQL Injection"),
        ("05_advanced_extraction.py", "Advanced Data Extraction"),
        ("06_out_of_band.py", "Out-of-Band SQL Injection"),
        ("07_second_order.py", "Second-Order SQL Injection"),
        ("08_stacked_queries.py", "Stacked Queries"),
        ("09_waf_bypass.py", "WAF Bypass Techniques"),
    ]

    results = []

    for script, name in phases:
        print(f"\n{'='*70}")
        print(f"PHASE: {name}")
        print(f"{'='*70}")

        input("Press Enter to continue (or Ctrl+C to stop)...")

        success = run_phase(phases.index((script, name)) + 1, script)
        results.append((name, success))
        time.sleep(2)

    print("\n" + "="*70)
    print("FINAL RESULTS")
    print("="*70)

    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")


if __name__ == "__main__":
    main()
