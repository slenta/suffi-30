"""HTTP-based highscore client for web/pygbag builds."""

import json
from datetime import datetime


class HTTPHighscoreClient:
    """Client for interacting with highscore API endpoints."""

    def __init__(self, api_base_url=None):
        """
        Initialize the HTTP client.

        Args:
            api_base_url: Base URL for the API (e.g., https://yourdomain.com/api)
                         If None, attempts to use window.location.origin in web context
        """
        self.api_base_url = api_base_url

        # In pygbag/web context, we'll use the browser's fetch API
        # This will be accessed via platform module
        self._is_web = self._detect_web_environment()

    def _detect_web_environment(self):
        """Detect if running in web/pygbag environment."""
        try:
            import sys

            return sys.platform == "emscripten"
        except:
            return False

    def _get_api_url(self):
        """Get the API base URL."""
        if self.api_base_url:
            return self.api_base_url

        # In web context, use relative URL
        if self._is_web:
            return "/api"

        # For local testing, you might want to set a default
        return "http://localhost:3000/api"

    async def add_highscore(self, level_name, player_name, score_breakdown):
        """
        Add a new highscore via API.

        Args:
            level_name: Name of the level
            player_name: Name of the player
            score_breakdown: Dictionary with score details

        Returns:
            Dictionary with response data
        """
        url = f"{self._get_api_url()}/highscores"

        payload = {
            "action": "add_highscore",
            "level_name": level_name,
            "player_name": player_name,
            "score_breakdown": score_breakdown,
        }

        try:
            if self._is_web:
                # Use platform.window.fetch for web builds
                response = await self._fetch_web(url, method="POST", data=payload)
            else:
                # Use urllib for non-web builds (shouldn't happen, but fallback)
                response = await self._fetch_urllib(url, method="POST", data=payload)

            return response

        except Exception as e:
            print(f"⚠️ Error adding highscore via API: {e}")
            return {"error": str(e)}

    async def get_top_scores(self, level_name, limit=5):
        """
        Get top scores for a level via API.

        Args:
            level_name: Name of the level
            limit: Maximum number of scores to return

        Returns:
            List of score entries
        """
        url = f"{self._get_api_url()}/highscores?action=get_top_scores&level_name={level_name}&limit={limit}"

        try:
            if self._is_web:
                response = await self._fetch_web(url, method="GET")
            else:
                response = await self._fetch_urllib(url, method="GET")

            if "scores" in response:
                return response["scores"]
            return []

        except Exception as e:
            print(f"⚠️ Error getting top scores via API: {e}")
            return []

    async def is_highscore(self, level_name, score):
        """
        Check if a score qualifies as a highscore via API.

        Args:
            level_name: Name of the level
            score: The score to check

        Returns:
            Boolean indicating if this is a top score
        """
        url = f"{self._get_api_url()}/highscores?action=is_highscore&level_name={level_name}&score={score}"

        try:
            if self._is_web:
                response = await self._fetch_web(url, method="GET")
            else:
                response = await self._fetch_urllib(url, method="GET")

            return response.get("is_highscore", True)

        except Exception as e:
            print(f"⚠️ Error checking highscore via API: {e}")
            return True  # Default to True on error

    async def _fetch_web(self, url, method="GET", data=None):
        """Fetch using browser's fetch API (for pygbag builds)."""
        try:
            import platform

            options = {"method": method}

            if data:
                options["headers"] = {"Content-Type": "application/json"}
                options["body"] = json.dumps(data)

            # Use platform.window.fetch for web builds
            response = await platform.window.fetch(url, **options)

            # Parse JSON response
            response_text = await response.text()
            return json.loads(response_text)

        except Exception as e:
            raise Exception(f"Web fetch failed: {e}")

    async def _fetch_urllib(self, url, method="GET", data=None):
        """Fetch using urllib (fallback for non-web builds)."""
        import urllib.request
        import urllib.error

        try:
            if data:
                data_bytes = json.dumps(data).encode("utf-8")
                req = urllib.request.Request(
                    url,
                    data=data_bytes,
                    headers={"Content-Type": "application/json"},
                    method=method,
                )
            else:
                req = urllib.request.Request(url, method=method)

            with urllib.request.urlopen(req) as response:
                response_text = response.read().decode("utf-8")
                return json.loads(response_text)

        except urllib.error.URLError as e:
            raise Exception(f"URL fetch failed: {e}")
