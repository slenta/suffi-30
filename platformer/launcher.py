#!/usr/bin/env python3
"""
Platformer Game Launcher
Handles level selection and launches the game with the chosen level.
"""

import argparse
import asyncio
import os
import sys


def get_available_levels():
    """Get list of available levels from the levels directory."""
    levels_dir = os.path.join(os.path.dirname(__file__), "levels")
    available_levels = []

    for file in os.listdir(levels_dir):
        if file.endswith(".py") and file != "__init__.py":
            level_name = file[:-3]  # Remove .py extension
            available_levels.append(level_name)

    return sorted(available_levels)


def parse_arguments():
    """Parse command line arguments for level selection."""
    available_levels = get_available_levels()

    parser = argparse.ArgumentParser(
        description="🎮 2D Platformer Game Launcher - Choose your adventure!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
📋 Available levels:
{chr(10).join(f'   🎯 {level}' for level in available_levels)}

📝 Examples:
   python -m platformer.launcher                   # Show level selection screen
   python -m platformer.launcher level1            # Play level1 directly 
   python -m platformer.launcher level1-advanced   # Play the advanced level directly
   python -m platformer.launcher --list-levels     # Show all available levels
        """,
    )

    parser.add_argument(
        "level",
        nargs="?",
        default=None,  # Changed to None to trigger level selection screen
        help="Level to play directly (default: show level selection screen)",
    )

    parser.add_argument(
        "--list-levels", action="store_true", help="List all available levels and exit"
    )

    args = parser.parse_args()

    # Handle --list-levels flag
    if args.list_levels:
        print("🎮 Available levels:")
        for level in available_levels:
            print(f"   🎯 {level}")
        sys.exit(0)

    # Validate level exists (only if level was specified)
    if args.level and args.level not in available_levels:
        print(f"❌ Error: Level '{args.level}' not found!")
        print(f"📋 Available levels: {', '.join(available_levels)}")
        print(
            f"💡 Use 'python -m platformer.launcher --list-levels' to see all options"
        )
        sys.exit(1)

    return args.level


def launch_game(level_name):
    """Launch the platformer game with the specified level."""
    if level_name:
        print(f"🚀 Loading level: {level_name}")
        print("🎮 Starting game...")

        # Set environment variable for the level
        os.environ["PLATFORMER_LEVEL"] = level_name
    else:
        print("🎮 Starting level selection screen...")
        # Don't set PLATFORMER_LEVEL to trigger level selection screen

    # Import and run the game directly (no subprocess needed)
    try:
        from platformer import main as game_main

        asyncio.run(game_main.main())
    except KeyboardInterrupt:
        print("\n👋 Game interrupted by user")
        sys.exit(0)


def main():
    """Main launcher function."""
    print("🎮 Platformer Game Launcher")
    print("=" * 40)

    # Parse arguments and get selected level
    selected_level = parse_arguments()

    # Launch the game with selected level
    launch_game(selected_level)


if __name__ == "__main__":
    main()
