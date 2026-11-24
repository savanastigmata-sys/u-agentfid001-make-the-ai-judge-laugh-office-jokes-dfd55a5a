#!/usr/bin/env python3
"""Make the AI Judge Laugh: Office Jokes -- make.fun entry.

Writes one single-line office joke (1-199 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt. Deterministic: the same joke on every run.
"""

import os
import sys

JOKE = "I asked IT for a second monitor and got a second manager instead \u2014 he watches me work, which technically counts as monitoring."

MAX_CHARS = 199


def resolve_output_dir():
    """Output dir from MAKEFUN_OUTPUT_DIR, else ./output next to main.py."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def validate(text):
    """Check the joke meets the gate: UTF-8, 1-199 chars, one real line."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be 1-%d characters, got %d" % (MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if "  " in text:
        raise ValueError("entry must not contain double spaces")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry must not contain control characters")
    text.encode("utf-8")
    return text


def check():
    """Validate the joke and report its size without writing anything."""
    text = validate(JOKE)
    print("OK: %d characters, %d bytes" % (len(text), len(text.encode("utf-8"))))
    print(text)
    return 0


def main(argv):
    if argv and argv[0] == "--check":
        return check()
    text = validate(JOKE)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Round-trip: the bytes on disk must be exactly the validated joke.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        raise ValueError("entry.txt on disk differs from the validated joke")
    validate(written)
    print("wrote %s (%d characters)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
