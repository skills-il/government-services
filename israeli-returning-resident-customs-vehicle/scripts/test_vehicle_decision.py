#!/usr/bin/env python3
"""Regression tests for vehicle-decision.py. Run: python3 scripts/test_vehicle_decision.py"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "vehicle-decision.py")
BASE = ["--car-value-usd", "28000", "--shipping-usd", "3500", "--car-age-months", "40",
        "--local-price-usd", "50000", "--ils-per-usd", "3.7"]


def run(*extra):
    p = subprocess.run([sys.executable, SCRIPT, *BASE, *extra], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def check(name, cond):
    print(("ok   " if cond else "FAIL ") + name)
    return cond


def main():
    results = []
    rc, out = run("--vehicle-class", "hybrid", "--green-score", "120", "--gross-weight-kg", "2100")
    results.append(check("example 2: 117,991 NIS, 101%", rc == 0 and "117,991 NIS (101% of CIF)" in out))
    rc, out = run("--no-emissions-data", "--gross-weight-kg", "2100")
    results.append(check("example 2 without emissions letter: $71,993", rc == 0 and "$71,993" in out))
    rc, out = run("--green-score", "120", "--origin", "other", "--gross-weight-kg", "2100")
    results.append(check("example 2 non-FTA: 116%, $69,351", rc == 0 and "(116% of CIF)" in out and "$69,351" in out))
    rc, out = run("--gross-weight-kg", "0")
    results.append(check("weight 0 rejected (exit 2)", rc == 2 and "purchase tax" not in out))
    rc, out = run("--gross-weight-kg", "-5")
    results.append(check("negative weight rejected (exit 2)", rc == 2 and "purchase tax" not in out))
    rc, out = run()
    results.append(check("missing weight rejected (exit 2)", rc == 2))
    rc, out = run("--gross-weight-kg", "3500.1")
    results.append(check("above 3,500 kg not covered (exit 3)",
                         rc == 3 and "NOT COVERED" in out and "purchase tax" not in out))
    rc, out = run("--gross-weight-kg", "3500", "--green-score", "120")
    results.append(check("exactly 3,500 kg covered", rc == 0 and "purchase tax" in out))
    rc, out = run("--gross-weight-kg", "2400", "--vehicle-class", "ev", "--goods-vehicle")
    results.append(check("electric pickup not covered (exit 3)",
                         rc == 3 and "NOT COVERED" in out and "purchase tax" not in out))
    rc, out = run("--gross-weight-kg", "2400", "--goods-vehicle", "--green-score", "200")
    results.append(check("ICE pickup up to 3,500 kg covered", rc == 0 and "purchase tax" in out))
    rc, out = run("--gross-weight-kg", "2000", "--motorcycle")
    results.append(check("motorcycle not covered (exit 3)", rc == 3 and "purchase tax" not in out))
    rc, out = run("--gross-weight-kg", "2000", "--vehicle-class", "ev")
    results.append(check("EV prints both official reductions", rc == 0 and "14,523" in out and "19,498" in out))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
