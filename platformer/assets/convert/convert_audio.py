#!/usr/bin/env python3
"""
Audio Converter Script
Converts all audio files in music/ and sounds/ folders to OGG format
"""

import os
import subprocess
from pathlib import Path

# Define the base directory (parent of this script's location)
BASE_DIR = Path(__file__).parent.parent
MUSIC_DIR = BASE_DIR / "music"
SOUNDS_DIR = BASE_DIR / "sounds"

# Supported input formats
AUDIO_FORMATS = [".mp3", ".wav", ".flac", ".m4a", ".aac", ".wma", ".aiff"]


def check_ffmpeg():
    """Check if ffmpeg is installed"""
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def convert_to_ogg(input_file, output_file, quality=5):
    """
    Convert an audio file to OGG format using ffmpeg

    Args:
        input_file: Path to the input audio file
        output_file: Path to the output OGG file
        quality: Quality level (0-10, where 10 is best quality)
    """
    try:
        # Use ffmpeg to convert with quality setting
        # -q:a 5 is a good balance between quality and file size (range 0-10)
        cmd = [
            "ffmpeg",
            "-i",
            str(input_file),
            "-c:a",
            "libvorbis",
            "-q:a",
            str(quality),
            "-y",  # Overwrite output file if it exists
            str(output_file),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_file}: {e.stderr}")
        return False


def process_directory(directory):
    """Process all audio files in a directory"""
    if not directory.exists():
        print(f"Directory not found: {directory}")
        return

    print(f"\nProcessing directory: {directory}")
    converted_count = 0
    skipped_count = 0

    # Get all files in the directory
    for file_path in directory.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in AUDIO_FORMATS:
            # Create output filename with .ogg extension
            output_path = file_path.with_suffix(".ogg")

            # Skip if already OGG or if output already exists
            if file_path.suffix.lower() == ".ogg":
                print(f"  Skipping (already OGG): {file_path.name}")
                skipped_count += 1
                continue

            if output_path.exists():
                print(
                    f"  Skipping (OGG exists): {file_path.name} -> {output_path.name}"
                )
                skipped_count += 1
                continue

            # Convert the file
            print(f"  Converting: {file_path.name} -> {output_path.name}")
            if convert_to_ogg(file_path, output_path):
                converted_count += 1
                print(f"    ✓ Success")
            else:
                print(f"    ✗ Failed")

    print(f"  Converted: {converted_count}, Skipped: {skipped_count}")


def main():
    """Main function to convert all audio files"""
    print("=" * 60)
    print("Audio Format Converter - Converting to OGG")
    print("=" * 60)

    # Check if ffmpeg is installed
    if not check_ffmpeg():
        print("\n❌ Error: ffmpeg is not installed!")
        print("\nPlease install ffmpeg:")
        print("  macOS:   brew install ffmpeg")
        print("  Ubuntu:  sudo apt-get install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        return

    print("✓ ffmpeg is installed\n")

    # Process both directories
    process_directory(MUSIC_DIR)
    process_directory(SOUNDS_DIR)

    print("\n" + "=" * 60)
    print("Conversion complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
