"""Highscore management system for tracking and persisting player scores."""

import os
import sys
import json
from datetime import datetime
from ..config.constants import (
    SCORE_PER_SECOND_REMAINING,
    SCORE_PER_TROPHY,
    SCORE_PER_DAMAGE,
    SCORE_PER_LIFE,
)

# Detect if running in web/pygbag environment
IS_WEB_BUILD = sys.platform == "emscripten"

# Import appropriate backend
if IS_WEB_BUILD:
    # Web builds use HTTP API client
    from .http_highscore_client import HTTPHighscoreClient

    POSTGRES_AVAILABLE = False
    HTTP_CLIENT_AVAILABLE = True
    print("🌐 Running in web environment - using HTTP API for highscores")
else:
    # Desktop builds can use direct PostgreSQL connection
    HTTP_CLIENT_AVAILABLE = False
    try:
        from .database import DatabaseConnection, is_postgres_available

        POSTGRES_AVAILABLE = True
    except ImportError:
        POSTGRES_AVAILABLE = False
        print("⚠️ PostgreSQL support not available. Using JSON file storage.")


class HighscoreManager:
    """Manages highscores including calculation, storage, and retrieval."""

    def __init__(self, highscore_file=None, use_postgres=True, api_base_url=None):
        """
        Initialize the highscore manager.

        Args:
            highscore_file: Path to the highscore file. If None, uses default location.
            use_postgres: Whether to use PostgreSQL if available (default: True).
            api_base_url: Base URL for HTTP API (used in web builds).
        """
        # Determine storage backend based on environment
        if IS_WEB_BUILD:
            # Web builds can use HTTP API or localStorage fallback
            self.use_postgres = False

            # Debug output to browser console
            try:
                import platform

                platform.window.console.log(
                    "[HIGHSCORE] Initializing in web environment"
                )
                platform.window.console.log(
                    f"[HIGHSCORE] api_base_url = {api_base_url}"
                )
            except:
                pass

            self.http_client = HTTPHighscoreClient(api_base_url)

            # Check if API is available (None means localhost without config)
            api_url = self.http_client._get_api_url()

            try:
                import platform

                platform.window.console.log(f"[HIGHSCORE] Detected API URL: {api_url}")
            except:
                pass

            if api_url is not None:
                self.use_http = True
                print(f"✅ Using HTTP API for highscore storage: {api_url}")
                try:
                    import platform

                    platform.window.console.log("[HIGHSCORE] Using HTTP API")
                except:
                    pass
            else:
                # Fallback to localStorage (only for localhost)
                self.use_http = False
                try:
                    import platform

                    platform.window.console.log(
                        "[HIGHSCORE] Falling back to localStorage"
                    )
                except:
                    pass
                from .http_highscore_client import LocalStorageHighscoreClient

                self.http_client = LocalStorageHighscoreClient()
                print(
                    "✅ Using localStorage for highscore storage (API not configured)"
                )
        else:
            # Desktop builds can use PostgreSQL or JSON
            self.use_http = False
            self.use_postgres = (
                use_postgres and POSTGRES_AVAILABLE and is_postgres_available()
            )

            if self.use_postgres:
                print("✅ Using PostgreSQL for highscore storage")
                # Initialize connection pool
                try:
                    DatabaseConnection.initialize_pool()
                except Exception as e:
                    print(f"⚠️ Failed to initialize PostgreSQL: {e}")
                    print("⚠️ Falling back to JSON file storage")
                    self.use_postgres = False

        # Setup JSON fallback for non-web, non-postgres scenarios
        if not self.use_http and not self.use_postgres:
            print("📝 Using JSON file for highscore storage")
            if highscore_file is None:
                # Default to assets/highscores.json
                assets_dir = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "assets",
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
        if self.use_http:
            # Web builds use async HTTP - return coroutine
            return self._add_highscore_http(level_name, player_name, score_breakdown)
        elif self.use_postgres:
            self._add_highscore_postgres(level_name, player_name, score_breakdown)
        else:
            self._add_highscore_json(level_name, player_name, score_breakdown)

    async def _add_highscore_http(self, level_name, player_name, score_breakdown):
        """Add highscore via HTTP API (async)."""
        return await self.http_client.add_highscore(
            level_name, player_name, score_breakdown
        )

    def _add_highscore_json(self, level_name, player_name, score_breakdown):
        """Add highscore to JSON file."""
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

    def _add_highscore_postgres(self, level_name, player_name, score_breakdown):
        """Add highscore to PostgreSQL database."""
        connection = None
        try:
            connection = DatabaseConnection.get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO highscores 
                (level_name, player_name, total_score, time_score, trophy_score, 
                 damage_score, life_score, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    level_name,
                    player_name,
                    score_breakdown["total_score"],
                    score_breakdown["time_score"],
                    score_breakdown["trophy_score"],
                    score_breakdown["damage_score"],
                    score_breakdown["life_score"],
                    datetime.now(),
                ),
            )

            connection.commit()
            cursor.close()

        except Exception as e:
            print(f"⚠️ Error adding highscore to database: {e}")
            if connection:
                try:
                    connection.rollback()
                except Exception as rollback_error:
                    print(
                        f"⚠️ Error during rollback (connection may be closed): {rollback_error}"
                    )

        finally:
            if connection:
                try:
                    DatabaseConnection.return_connection(connection)
                except Exception as cleanup_error:
                    print(f"⚠️ Error returning connection: {cleanup_error}")

    def get_top_scores(self, level_name, limit=5):
        """
        Get top scores for a level.

        Args:
            level_name: Name of the level
            limit: Maximum number of scores to return (default: 5)

        Returns:
            List of score entries (dictionaries) or coroutine for web builds
        """
        if self.use_http:
            # Web builds use async HTTP - return coroutine
            return self._get_top_scores_http(level_name, limit)
        elif self.use_postgres:
            return self._get_top_scores_postgres(level_name, limit)
        else:
            return self._get_top_scores_json(level_name, limit)

    async def _get_top_scores_http(self, level_name, limit=5):
        """Get top scores via HTTP API (async)."""
        return await self.http_client.get_top_scores(level_name, limit)

    def _get_top_scores_json(self, level_name, limit=5):
        """Get top scores from JSON file."""
        if level_name not in self.highscores:
            return []
        return self.highscores[level_name][:limit]

    def _get_top_scores_postgres(self, level_name, limit=5):
        """Get top scores from PostgreSQL database."""
        connection = None
        try:
            connection = DatabaseConnection.get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT player_name, total_score, time_score, trophy_score,
                       damage_score, life_score, timestamp
                FROM highscores
                WHERE level_name = %s
                ORDER BY total_score DESC
                LIMIT %s
                """,
                (level_name, limit),
            )

            results = []
            for row in cursor.fetchall():
                results.append(
                    {
                        "player_name": row[0],
                        "score": row[1],
                        "breakdown": {
                            "total_score": row[1],
                            "time_score": row[2],
                            "trophy_score": row[3],
                            "damage_score": row[4],
                            "life_score": row[5],
                        },
                        "timestamp": row[6].isoformat() if row[6] else None,
                    }
                )

            cursor.close()
            return results

        except Exception as e:
            print(f"⚠️ Error retrieving highscores from database: {e}")
            return []

        finally:
            if connection:
                try:
                    DatabaseConnection.return_connection(connection)
                except Exception as cleanup_error:
                    print(f"⚠️ Error returning connection: {cleanup_error}")

    def is_highscore(self, level_name, score):
        """
        Check if a score qualifies as a highscore (top 10).

        Args:
            level_name: Name of the level
            score: The score to check

        Returns:
            Boolean indicating if this is a top 10 score, or coroutine for web builds
        """
        if self.use_http:
            # Web builds use async HTTP - return coroutine
            return self._is_highscore_http(level_name, score)
        elif self.use_postgres:
            return self._is_highscore_postgres(level_name, score)
        else:
            return self._is_highscore_json(level_name, score)

    async def _is_highscore_http(self, level_name, score):
        """Check if score is a highscore via HTTP API (async)."""
        return await self.http_client.is_highscore(level_name, score)

    def _is_highscore_json(self, level_name, score):
        """Check if score is a highscore using JSON data."""
        if level_name not in self.highscores:
            return True  # First score for this level

        scores = [entry["score"] for entry in self.highscores[level_name]]
        if len(scores) < 10:
            return True  # Less than 10 scores, so it qualifies

        # Check if score is higher than the lowest top 10 score
        return score > min(scores)

    def _is_highscore_postgres(self, level_name, score):
        """Check if score is a highscore using PostgreSQL."""
        connection = None
        try:
            connection = DatabaseConnection.get_connection()
            cursor = connection.cursor()

            # Count scores higher than or equal to the given score
            cursor.execute(
                """
                SELECT COUNT(*) FROM highscores
                WHERE level_name = %s
                """,
                (level_name,),
            )
            total_count = cursor.fetchone()[0]

            if total_count < 10:
                cursor.close()
                return True  # Less than 10 scores, so it qualifies

            # Get the 10th highest score
            cursor.execute(
                """
                SELECT total_score FROM highscores
                WHERE level_name = %s
                ORDER BY total_score DESC
                LIMIT 1 OFFSET 9
                """,
                (level_name,),
            )

            result = cursor.fetchone()
            cursor.close()

            if result:
                return score > result[0]
            return True

        except Exception as e:
            print(f"⚠️ Error checking highscore in database: {e}")
            return True  # Default to True on error

        finally:
            if connection:
                try:
                    DatabaseConnection.return_connection(connection)
                except Exception as cleanup_error:
                    print(f"⚠️ Error returning connection: {cleanup_error}")
