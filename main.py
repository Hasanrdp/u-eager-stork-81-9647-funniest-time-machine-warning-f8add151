#!/usr/bin/env python3
"""Funniest Time Machine Warning Label — make.fun entry.

Writes one fixed warning label (99 characters) to /output/entry.txt.
Deterministic: no input, no randomness, no network, standard library only.
"""

import hashlib
import os
import sys

LABEL = "WARNING: Do not shake hands with yourself. The timeline is still deciding which one of you is real."
EXPECTED_SHA256 = "07cf499f4f7e0fbf6a98a28a9f8cc7b641738756fc0796a9e9fdd485cd1a5266"
EXPECTED_BYTES = 99
OUTPUT_PATH = "/output/entry.txt"


def main() -> int:
    text = LABEL
    data = text.encode("utf-8")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as handle:
        handle.write(data)
    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()
    if written != data:
        print("read-back mismatch", file=sys.stderr)
        return 1
    if len(written) != EXPECTED_BYTES:
        print(f"expected {EXPECTED_BYTES} bytes, got {len(written)}",
              file=sys.stderr)
        return 1
    if hashlib.sha256(written).hexdigest() != EXPECTED_SHA256:
        print("output sha256 mismatch", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= 120:
        print("label outside the 1-120 character gate", file=sys.stderr)
        return 1
    print(f"wrote {len(data)} bytes to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
