"""Unplugged: A Smart Toaster's Breakup Line.

Builds the toaster's one-line breakup note and writes it to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).
Writes nowhere else; the repository itself is never touched.
"""

import os
import sys

SETUP = "It's not you, it's me"
TWIST = "actually it's you: you burnt 47 bagels, blamed the firmware,"
CLOSER = "and ticket #4821 says we're done."


def build_line():
    """Assemble the breakup line from its three fragments."""
    return " ".join([SETUP, "\u2014", TWIST, CLOSER])


def validate_line(line):
    """Gate: one line, 1-280 chars, UTF-8, no control characters."""
    if not line or len(line) > 280:
        raise ValueError("entry must be 1-280 characters, got %d" % len(line))
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    for ch in line:
        if ord(ch) < 0x20 and ch not in ("\t",):
            raise ValueError("entry contains a control character")
        if ch in ("\u200b", "\ufeff", "\u00ad"):
            raise ValueError("entry contains an invisible character")
    line.encode("utf-8")
    return line


def emit(line):
    """Write the entry and read it back for a byte-level check."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    with open(path, "rb") as f:
        raw = f.read()
    if raw.decode("utf-8") != line:
        raise ValueError("round-trip check failed")
    return path


def main():
    line = validate_line(build_line())
    path = emit(line)
    print("wrote %d chars to %s" % (len(line), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
