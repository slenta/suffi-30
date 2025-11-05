"""
Sound Manager for Platformer Game

This module handles all sound-related functionality including:
- Background music for levels
- Sound effects for gameplay events
- Volume control and music management
"""

import pygame as pg
import os
from typing import Optional, Dict


class SoundManager:
    """Manages all sound functionality for the game."""

    def __init__(self):
        """Initialize the sound manager."""
        # Initialize pygame mixer
        pg.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pg.mixer.init()

        # Sound state
        self.music_volume = 0.7  # Default music volume (0.0 to 1.0)
        self.sfx_volume = 0.8  # Default sound effects volume
        self.music_enabled = True
        self.sfx_enabled = True

        # Current music tracking
        self.current_music_file = None
        self.is_music_playing = False

        # Sound effects cache
        self.sound_effects: Dict[str, pg.mixer.Sound] = {}

        print("🎵 Sound Manager initialized")

    def set_music_volume(self, volume: float):
        """Set the music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        pg.mixer.music.set_volume(self.music_volume)
        print(f"🎵 Music volume set to {self.music_volume:.1f}")

    def set_sfx_volume(self, volume: float):
        """Set the sound effects volume (0.0 to 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))
        # Update volume for all cached sound effects
        for sound in self.sound_effects.values():
            print(sound["name"])
            sound.set_volume(self.sfx_volume)
        print(f"🔊 SFX volume set to {self.sfx_volume:.1f}")

    def toggle_music(self):
        """Toggle music on/off."""
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            if self.current_music_file and not self.is_music_playing:
                self.play_background_music(self.current_music_file)
        else:
            self.stop_music()
        print(f"🎵 Music {'enabled' if self.music_enabled else 'disabled'}")

    def toggle_sfx(self):
        """Toggle sound effects on/off."""
        self.sfx_enabled = not self.sfx_enabled
        print(f"🔊 Sound effects {'enabled' if self.sfx_enabled else 'disabled'}")

    def play_background_music(self, music_file_path: str, loop: bool = True):
        """
        Play background music for a level.

        Args:
            music_file_path: Path to the music file (MP3, OGG, WAV supported)
            loop: Whether to loop the music (-1 for infinite loop, 0 for no loop)
        """
        if not self.music_enabled:
            print("🎵 Music is disabled, skipping playback")
            return

        # Check if file exists
        if not os.path.exists(music_file_path):
            print(f"❌ Music file not found: {music_file_path}")
            return

        # Don't restart if same music is already playing
        if self.current_music_file == music_file_path and self.is_music_playing:
            print(f"🎵 Music already playing: {os.path.basename(music_file_path)}")
            return

        try:
            # Stop current music
            self.stop_music()

            # Load and play new music
            pg.mixer.music.load(music_file_path)
            pg.mixer.music.set_volume(self.music_volume)
            pg.mixer.music.play(-1 if loop else 0)

            self.current_music_file = music_file_path
            self.is_music_playing = True

            print(f"🎵 Playing: {os.path.basename(music_file_path)}")

        except pg.error as e:
            print(f"❌ Error playing music: {e}")

    def stop_music(self):
        """Stop the currently playing background music."""
        if self.is_music_playing:
            pg.mixer.music.stop()
            self.is_music_playing = False
            print("🎵 Music stopped")

    def pause_music(self):
        """Pause the currently playing music."""
        if self.is_music_playing:
            pg.mixer.music.pause()
            print("⏸️ Music paused")

    def resume_music(self):
        """Resume paused music."""
        if self.current_music_file and not pg.mixer.music.get_busy():
            pg.mixer.music.unpause()
            print("▶️ Music resumed")

    def load_sound_effect(self, name: str, file_path: str) -> Optional[pg.mixer.Sound]:
        """
        Load a sound effect into memory.

        Args:
            name: Name to reference this sound effect
            file_path: Path to the sound file

        Returns:
            The loaded Sound object or None if failed
        """
        if not os.path.exists(file_path):
            print(f"❌ Sound effect file not found: {file_path}")
            return None

        try:
            sound = pg.mixer.Sound(file_path)
            sound.set_volume(self.sfx_volume)
            self.sound_effects[name] = sound
            print(f"🔊 Loaded sound effect: {name}")
            return sound

        except pg.error as e:
            print(f"❌ Error loading sound effect {name}: {e}")
            return None

    def play_sound_effect(self, name: str):
        """
        Play a loaded sound effect.

        Args:
            name: Name of the sound effect to play
        """
        if not self.sfx_enabled:
            return

        if name in self.sound_effects:
            self.sound_effects[name].play()
        else:
            print(f"❌ Sound effect not found: {name}")

    def cleanup(self):
        """Clean up sound resources."""
        self.stop_music()
        self.sound_effects.clear()
        pg.mixer.quit()
        print("🎵 Sound Manager cleaned up")


# Global sound manager instance
sound_manager = SoundManager()
