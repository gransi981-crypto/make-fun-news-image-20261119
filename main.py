#!/usr/bin/env python3
"""Entry program for make.fun bounty news-image-20261119 (program/v1).

Writes the entry image to /output/entry.png. The image is the finished
front page held in this repository as entry.png (drawn at build time by
render.py from the verified news of Thursday 19 November 2026); this
program only copies it to the output directory, so both graded runs
produce the same bytes. Standard library only, no network.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", output_dir / "entry.png")


if __name__ == "__main__":
    main()
