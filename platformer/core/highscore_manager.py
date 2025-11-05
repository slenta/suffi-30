"""Highscore management system for tracking and persisting player scores."""

import os
import json
from datetime import datetime
from ..config.constants import (
    SCORE_PER_SECOND_REMAINING,
    SCORE_PER_TROPHY,
    SCORE_PER_DAMAGE,
    SCORE_PER_LIFE,
)


class HighscoreManager:
    """Manages highscores including calculation, storage, and retrieval."""

    def __init__(self, highscore_file=None):
        """
        Initialize the highscore manager.

        Args:
            highscore_file: Path to the highscore file. If None, uses default location.
        """
        if highscore_file is None:
            # Default to assets/highscores.json
            assets_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets"
            )
            os.makedirs(assets_dir, exist_ok=True)
            self.highscore_file = os.path.join(assets_dir, "highscores.json")
        else:
            self.highscore_file = highscore_file

        self.highscores = self._load_highscores()

    def _load_highscores(self):
        """Load highscores from file."""
        if os.path.exists(self.highscore_file):
            try:
                with open(self.highscore_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️ Error loading highscores: {e}")
                return {}
        return {}

    def _save_highscores(self):
        """Save highscores to file."""
        try:
            with open(self.highscore_file, "w") as f:
                json.dump(self.highscores, f, indent=2)
        except IOError as e:
            print(f"⚠️ Error saving highscores: {e}")

    def calculate_score(
        self, time_remaining, trophies_collected, damage_dealt, lives_remaining
    ):
        """
        Calculate total score based on game performance.

        Args:
            time_remaining: Seconds remaining on the timer (float)
            trophies_collected: Number of trophies collected (int)
            damage_dealt: Total damage dealt to enemies (int)
            lives_remaining: Number of lives (gems) remaining (int)

        Returns:
            Dictionary with score breakdown and total
        """
        time_score = int(time_remaining * SCORE_PER_SECOND_REMAINING)
        trophy_score = trophies_collected * SCORE_PER_TROPHY
        damage_score = damage_dealt * SCORE_PER_DAMAGE
        life_score = lives_remaining * SCORE_PER_LIFE

        total_score = time_score + trophy_score + damage_score + life_score

        return {
            "time_score": time_score,
            "trophy_score": trophy_score,
            "damage_score": damage_score,
            "life_score": life_score,
            "total_score": total_score,
        }

    def add_highscore(self, level_name, player_name, score_breakdown):
        """
        Add a new highscore entry.

        Args:
            level_name: Name of the level
            player_name: Name of the player
            score_breakdown: Dictionary with score details from calculate_score()
        """
        if level_name not in self.highscores:
            self.highscores[level_name] = []

        entry = {
            "player_name": player_name,
            "score": score_breakdown["total_score"],
            "breakdown": score_breakdown,
            "timestamp": datetime.now().isoformat(),
        }

        self.highscores[level_name].append(entry)
        # Sort by score descending
        self.highscores[level_name].sort(key=lambda x: x["score"], reverse=True)
        # Keep only top 10 scores
        self.highscores[level_name] = self.highscores[level_name][:10]

        self._save_highscores()

    def get_top_scores(self, level_name, limit=5):
        """
        Get top scores for a level.

        Args:
            level_name: Name of the level
            limit: Maximum number of scores to return (default: 5)

        Returns:
            List of score entries (dictionaries)
        """
        if level_name not in self.highscores:
            return []
        return self.highscores[level_name][:limit]

    def is_highscore(self, level_name, score):
        """
        Check if a score qualifies as a highscore (top 10).

        Args:
            level_name: Name of the level
            score: The score to check

        Returns:
            Boolean indicating if this is a top 10 score
        """
        if level_name not in self.highscores:
            return True  # First score for this level

        scores = [entry["score"] for entry in self.highscores[level_name]]
        if len(scores) < 10:
            return True  # Less than 10 scores, so it qualifies

        # Check if score is higher than the lowest top 10 score
        return score > min(scores)
