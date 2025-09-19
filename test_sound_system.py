#!/usr/bin/env python3
"""
Sound System Test Script

This script tests the sound system functionality without running the full game.
Use this to verify that pygame.mixer is working and sound files can be loaded.
"""

import sys
import os

# Add the platformer module to the path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from platformer.sound_manager import sound_manager
    print("✅ Sound system imported successfully!")
    
    # Test music loading (with dummy path)
    print("\n🎵 Testing background music functionality...")
    sound_manager.play_background_music("nonexistent.mp3")  # Should show file not found message
    
    # Test sound effect loading (with dummy path)
    print("\n🔊 Testing sound effects functionality...")
    sound_manager.load_sound_effect("test", "nonexistent.wav")  # Should show file not found message
    
    # Test volume controls
    print("\n🎛️ Testing volume controls...")
    sound_manager.set_music_volume(0.5)
    sound_manager.set_sfx_volume(0.6)
    
    # Test toggles
    print("\n⏯️ Testing toggles...")
    sound_manager.toggle_music()
    sound_manager.toggle_sfx()
    
    print("\n✅ All sound system tests completed successfully!")
    print("\n📋 To add actual music and sounds:")
    print("   1. Place MP3 files in the 'music/' directory")
    print("   2. Place WAV files in the 'sounds/' directory")
    print("   3. Run the game normally with 'python launcher.py'")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure pygame is installed: pip install pygame")
except Exception as e:
    print(f"❌ Error: {e}")