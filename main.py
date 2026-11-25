#!/usr/bin/env python3
"""Entry program for make.fun bounty news-image-20261125.

Writes the pre-composed poster to /output/entry.png. The poster itself
is drawn by compose_poster.py (run at build time); this program only
copies the finished image byte-for-byte, so both harness runs produce
identical bytes. Standard library only, no network.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get(
        "OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(SRC):
        print("entry.png missing next to main.py", file=sys.stderr)
        return 1
    with open(SRC, "rb") as fh:
        magic = fh.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    size = os.path.getsize(SRC)
    if size > 1048576:
        print(f"entry.png too large: {size} bytes", file=sys.stderr)
        return 1
    shutil.copyfile(SRC, dest)
    print(f"wrote {dest} ({os.path.getsize(dest)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
