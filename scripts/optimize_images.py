#!/usr/bin/env python3
"""
One-shot PNG optimizer for platformer/assets.

Strategy:
- All PNGs: strip metadata + max zlib compression (lossless).
- Backgrounds (assets/backgrounds): downscale to fit within MAX_BG (width x height).
- Other sprites/images: downscale longest side to MAX_SPRITE.

Skips files smaller than MIN_TARGET_BYTES (no point optimizing tiny icons).
Requires ImageMagick `convert` on PATH.
"""

import shutil
import subprocess
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "platformer" / "assets"
BACKGROUNDS = ASSETS / "backgrounds"

MAX_BG = (4500, 540)        # backgrounds tile at native size; viewport is 900x270
MAX_SPRITE_SIDE = 512        # rendered sprites top out around 60px on a 900x270 surface
MIN_TARGET_BYTES = 200 * 1024  # 200 KB — below this, savings are marginal


def identify(path: Path) -> tuple[int, int]:
    out = subprocess.check_output(
        ["identify", "-format", "%w %h", str(path)], stderr=subprocess.DEVNULL
    )
    w, h = map(int, out.decode().split())
    return w, h


def fit(w: int, h: int, mw: int, mh: int) -> tuple[int, int]:
    scale = min(mw / w, mh / h, 1.0)
    return (max(1, int(w * scale)), max(1, int(h * scale)))


def fit_side(w: int, h: int, max_side: int) -> tuple[int, int]:
    longest = max(w, h)
    if longest <= max_side:
        return (w, h)
    scale = max_side / longest
    return (max(1, int(w * scale)), max(1, int(h * scale)))


def convert_png(src: Path, target_w: int, target_h: int) -> None:
    args = [
        "convert", str(src),
        "-resize", f"{target_w}x{target_h}",
        "-strip",
        "-define", "png:compression-level=9",
        "-define", "png:compression-filter=5",
        "-define", "png:compression-strategy=1",
        str(src),
    ]
    subprocess.run(args, check=True, stderr=subprocess.PIPE)


def main():
    if shutil.which("convert") is None:
        print("ImageMagick `convert` not found on PATH", file=sys.stderr)
        sys.exit(1)

    total_before = 0
    total_after = 0
    changed = 0

    for path in sorted(ASSETS.rglob("*.png")):
        size_before = path.stat().st_size
        if size_before < MIN_TARGET_BYTES:
            continue

        try:
            w, h = identify(path)
        except subprocess.CalledProcessError:
            print(f"skip (identify failed): {path}")
            continue

        if BACKGROUNDS in path.parents:
            target = fit(w, h, *MAX_BG)
        else:
            target = fit_side(w, h, MAX_SPRITE_SIDE)

        try:
            convert_png(path, *target)
        except subprocess.CalledProcessError as e:
            print(f"FAIL {path}: {e.stderr.decode()[:200]}")
            continue

        size_after = path.stat().st_size
        total_before += size_before
        total_after += size_after
        changed += 1
        rel = path.relative_to(ASSETS.parent)
        print(
            f"{rel}\n"
            f"  {w}x{h} -> {target[0]}x{target[1]} | "
            f"{size_before/1024:.0f} KB -> {size_after/1024:.0f} KB "
            f"({(1 - size_after/size_before)*100:.0f}% smaller)"
        )

    print()
    print(
        f"Processed {changed} files. "
        f"Total: {total_before/1024/1024:.1f} MB -> {total_after/1024/1024:.1f} MB "
        f"({(1 - total_after/total_before)*100:.0f}% reduction)"
    )


if __name__ == "__main__":
    main()
