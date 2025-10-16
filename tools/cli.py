# -------------------------------------------------------
# tools/cli.py
# -------------------------------------------------------
# Author: projectfong
# Copyright (c) 2025 Fong
# All Rights Reserved
# -------------------------------------------------------
# Purpose Summary:
#   - Provide a deterministic local CLI to interact with the cfo-ai-security-demo API.
#   - Implements commands for health check, mock ingestion, and evidence verification.
# Audit:
#   - Each command prints UTC timestamps at start and stop.
#   - All outputs are formatted JSON for reproducibility.
#   - No external network connections are made; localhost only.
# -------------------------------------------------------
#!/usr/bin/env python3

import argparse
import json
import sys
import os
import hashlib
from datetime import datetime
from urllib import request

BASE = "http://127.0.0.1:8080"

# -------------------------------------------------------
# Utility Functions
# -------------------------------------------------------
def ts():
    # Purpose: Return UTC timestamp string.
    # Audit: Used for CLI start/stop log lines.
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def _get(path: str):
    # Purpose: Perform local GET request to demo API.
    # Audit: Operates against localhost only; returns parsed JSON.
    with request.urlopen(f"{BASE}{path}") as r:
        return json.loads(r.read().decode())

def _post(path: str, payload: dict):
    # Purpose: Perform local POST request to demo API.
    # Audit: Encodes deterministic JSON payload; no external I/O.
    data = json.dumps(payload).encode()
    req = request.Request(f"{BASE}{path}", method="POST", data=data, headers={"Content-Type": "application/json"})
    with request.urlopen(req) as r:
        return json.loads(r.read().decode())

def verify_evidence():
    # Purpose: Validate structure and integrity of evidence JSONL files.
    # Audit:
    #   - Reads all log and vector JSONL files under ./evidence/.
    #   - Recomputes SHA256 for each record (excluding event_id field).
    #   - Reports mismatches and totals in plain text summary.
    base = "./evidence"
    verified = 0
    failed = 0
    checked = 0

    for root, _, files in os.walk(base):
        for f in files:
            if not f.endswith(".jsonl"):
                continue
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8") as fh:
                for line in fh:
                    checked += 1
                    try:
                        data = json.loads(line)
                        eid = data.get("event_id")
                        if not eid:
                            print(f"[WARN] Missing event_id in {path}")
                            failed += 1
                            continue
                        temp = dict(data)
                        temp.pop("event_id", None)
                        raw = json.dumps(temp, sort_keys=True, separators=(',', ':')).encode("utf-8")
                        digest = hashlib.sha256(raw).hexdigest()
                        if digest != eid:
                            print(f"[FAIL] Hash mismatch in {path}")
                            failed += 1
                        else:
                            verified += 1
                    except Exception as e:
                        print(f"[ERROR] Invalid JSON line in {path}: {e}")
                        failed += 1

    print("\nVerification Summary:")
    print(f"  Files checked : {checked}")
    print(f"  Verified       : {verified}")
    print(f"  Failed         : {failed}")
    if failed == 0:
        print("  Result         : VERIFIED (All entries passed)")
    else:
        print("  Result         : WARNING (Some entries failed validation)")

# -------------------------------------------------------
# Main Entry Point
# -------------------------------------------------------
def main():
    # Purpose: Define CLI command structure and dispatch execution.
    # Audit:
    #   - Prints deterministic start/stop timestamps for each command.
    #   - Outputs formatted JSON responses where applicable.
    parser = argparse.ArgumentParser(description="cfo-ai-security-demo CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # health command
    sub.add_parser("health", help="Check API health")

    # mock-ingest command
    mi = sub.add_parser("mock-ingest", help="Simulate firewall -> vessel -> embed pipeline")
    mi.add_argument("--message", required=True, help="Firewall log message content")
    mi.add_argument("--source", default="fwlogs", help="Source label for message")

    # verify-evidence command
    sub.add_parser("verify-evidence", help="Validate JSON structure and SHA256 hashes in evidence files")

    args = parser.parse_args()
    print(f"{ts()} cli=start cmd={args.cmd}")

    if args.cmd == "health":
        out = _get("/healthz")
    elif args.cmd == "mock-ingest":
        out = _post("/mock/ingest", {"message": args.message, "source": args.source})
    elif args.cmd == "verify-evidence":
        verify_evidence()
        out = {"status": "done"}
    else:
        out = {"status": "error", "message": "unknown command"}

    print(json.dumps(out, indent=2, sort_keys=True))
    print(f"{ts()} cli=done cmd={args.cmd}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
