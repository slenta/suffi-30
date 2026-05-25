#!/usr/bin/env python3
"""
One-shot OGG re-encoder for platformer/assets/music.

The original music files are encoded at very high bitrates (trancefloor.ogg is
15 MB for one track). For an in-browser pygame build, ~128 kbps Vorbis is
transparent on typical laptop/phone speakers and shaves the bundle significantly.

Strategy:
- Re-encode every *.ogg under MUSIC_DIR at TARGET_QUALITY (libvorbis -q:a).
  q=2 ~= 96 kbps; q=4 ~= 128 kbps; q=5 ~= 160 kbps.
- Leaves sound effects (assets/sounds) alone — they're already tiny.

Requires ffmpeg on PATH.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "platformer" / "assets"
MUSIC_DIR = ASSETS / "music"

TARGET_QUALITY = "4"  # libvorbis quality: 4 ≈ 128 kbps stereo


def encode(src: Path, quality: str) -> Path:
    tmp = Path(tempfile.mkstemp(suffix=".ogg", dir=src.parent)[1])
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(src),
            "-c:a", "libvorbis",
            "-q:a", quality,
            str(tmp),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    return tmp


def main():
    if shutil.which("ffmpeg") is None:
        print("ffmpeg not found on PATH", file=sys.stderr)
        sys.exit(1)

    if not MUSIC_DIR.exists():
        print(f"missing dir: {MUSIC_DIR}", file=sys.stderr)
        sys.exit(1)

    total_before = 0
    total_after = 0

    for src in sorted(MUSIC_DIR.glob("*.ogg")):
        before = src.stat().st_size
        try:
            tmp = encode(src, TARGET_QUALITY)
        except subprocess.CalledProcessError as e:
            print(f"FAIL {src.name}: {e.stderr.decode()[:200]}")
            continue
        after = tmp.stat().st_size
        # Only swap if we actually got smaller.
        if after < before:
            tmp.replace(src)
            total_before += before
            total_after += after
            print(
                f"{src.name}: {before/1024/1024:.2f} MB -> {after/1024/1024:.2f} MB "
                f"({(1 - after/before)*100:.0f}% smaller)"
            )
        else:
            tmp.unlink()
            print(f"{src.name}: skip (re-encode not smaller)")

    print()
    print(
        f"Total: {total_before/1024/1024:.1f} MB -> {total_after/1024/1024:.1f} MB "
        f"({(1 - total_after/total_before)*100:.0f}% reduction)"
        if total_before
        else "No files changed."
    )


if __name__ == "__main__":
    main()
