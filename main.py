"""World in One Day, 26 November 2026.

Copies the front-page image this repository holds (entry.png) to the
grader's output directory as /output/entry.png. Standard library only.

The image itself is built by gen_image.py (run in-session, committed
alongside): a dense one-page newspaper drawn from the day's verified
stories. This entrypoint only copies bytes, so two runs of it always
write byte-identical output.
"""

import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    src = HERE / "entry.png"
    data = src.read_bytes()
    if not data.startswith(PNG_MAGIC):
        raise SystemExit("entry.png is not a PNG file")
    if len(data) > 1024 * 1024:
        raise SystemExit("entry.png is over the 1 MiB cap")
    (out_dir / "entry.png").write_bytes(data)


if __name__ == "__main__":
    main()
