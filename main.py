#!/usr/bin/env python3
"""Entry point for the news-image-20261124 bounty.

Copies the pre-rendered front page (entry.png, beside this file) to
the grader's output directory and prints its SHA-256 so the run can
be verified. Standard library only, no network, deterministic: the
same file is written on every run.
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    os.chmod(DST, 0o644)
    with open(DST, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print(f"entry.png sha256: {digest}")
    return digest


if __name__ == "__main__":
    main()
