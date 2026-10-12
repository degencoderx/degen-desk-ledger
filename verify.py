"""Verify The Degen Desk call ledger: every hash must match its line and link to the line before.

Usage: python3 verify.py [calls.jsonl]
No dependencies. Exits 0 when the whole chain is intact, 1 at the first broken line.
"""

import hashlib
import json
import sys

GENESIS_HASH = "0" * 64


def digest(entry: dict, prev_hash: str) -> str:
    canonical = json.dumps({**entry, "prev_hash": prev_hash}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify(path: str) -> int:
    prev_hash = GENESIS_HASH
    count = 0
    with open(path, encoding="utf-8") as handle:
        for number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            entry = {k: v for k, v in record.items() if k not in {"hash", "prev_hash"}}
            if record.get("prev_hash") != prev_hash:
                print(f"Line {number}: prev_hash does not match the line before. The chain is broken here.")
                return 1
            if record.get("hash") != digest(entry, prev_hash):
                print(f"Line {number}: contents do not match the hash. This call was changed after it was written.")
                return 1
            prev_hash = record["hash"]
            count += 1
    print(f"OK: {count} calls verified, chain intact. Latest hash {prev_hash}")
    return 0


if __name__ == "__main__":
    sys.exit(verify(sys.argv[1] if len(sys.argv) > 1 else "calls.jsonl"))
