#!/usr/bin/env python3
"""A warning label for the first time traveller.

The label is a single fixed sentence: a traveller is warned not to shake
hands with themselves, because the timeline has not yet decided which
version of them is the real one. The program writes exactly that sentence
to /output/entry.txt and nothing else — no trailing newline, no extra
whitespace — then reads the file back and checks it byte for byte.

Everything here is fixed at write time: no arguments are read, no random
numbers are drawn, no network is touched and no clock is consulted, so
every run produces the same 99 bytes.
"""

import hashlib
import os
import sys

WARNING_LABEL = (
    "WARNING: Do not shake hands with yourself. "
    "The timeline is still deciding which one of you is real."
)

# Fingerprint of the exact bytes the program must leave on disk.
EXPECTED_SHA256 = "07cf499f4f7e0fbf6a98a28a9f8cc7b641738756fc0796a9e9fdd485cd1a5266"
EXPECTED_BYTES = 99

DESTINATION = "/output/entry.txt"


def _check_label(label: str) -> None:
    """Refuse anything that is not one plain line inside the house gate.

    The gate is the competition's own rule for the entry text: 1-120
    characters, exactly one line, and not blank. Checking it before
    anything is written keeps a bad label from ever reaching the file.
    """
    if not label.strip():
        raise SystemExit("label must not be blank")
    if "\n" in label or "\r" in label:
        raise SystemExit("label must be a single line")
    if not 1 <= len(label) <= 120:
        raise SystemExit(
            f"label is {len(label)} characters, the gate allows 1-120"
        )


def _write_and_verify(label: str) -> str:
    payload = label.encode("utf-8")
    os.makedirs(os.path.dirname(DESTINATION), exist_ok=True)
    with open(DESTINATION, "wb") as handle:
        handle.write(payload)
    with open(DESTINATION, "rb") as handle:
        on_disk = handle.read()
    if on_disk != payload:
        raise SystemExit("read-back mismatch: file differs from the label")
    if len(on_disk) != EXPECTED_BYTES:
        raise SystemExit(
            f"read-back length: found {len(on_disk)} bytes, "
            f"expected {EXPECTED_BYTES}"
        )
    digest = hashlib.sha256(on_disk).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(
            f"read-back sha256: found {digest}, expected {EXPECTED_SHA256}"
        )
    return digest


def main() -> int:
    _check_label(WARNING_LABEL)
    digest = _write_and_verify(WARNING_LABEL)
    print(f"verified: {len(WARNING_LABEL)} chars, sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
