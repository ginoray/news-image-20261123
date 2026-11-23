#!/usr/bin/env python3
"""news-image-20261123 entry: "The World Today — 23 November 2026".

Writes a pre-rendered 1024x1024 news poster (seven verified stories of
Monday 23 November 2026) to entry.png in the output directory.

The poster bytes are sealed as base64 in poster_data.py, so this program
needs only the Python standard library and no network. Output directory
resolution follows the kit convention: an explicit argv path wins, then
the MAKEFUN_OUTPUT_DIR environment variable, then /output.
"""

import base64
import os
import sys

from poster_data import POSTER_B64

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024  # the competition gate: at most 1 MiB


def output_dir():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def poster_bytes():
    """Decode the sealed poster and sanity-check it before writing."""
    data = base64.b64decode(POSTER_B64, validate=True)
    if not data.startswith(PNG_SIGNATURE):
        raise SystemExit("sealed payload is not a PNG image")
    if len(data) > MAX_BYTES:
        raise SystemExit("sealed poster exceeds the 1 MiB gate")
    return data


def main():
    target = os.path.join(output_dir(), "entry.png")
    with open(target, "wb") as fh:
        fh.write(poster_bytes())


if __name__ == "__main__":
    main()
