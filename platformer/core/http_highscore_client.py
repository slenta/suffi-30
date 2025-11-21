"""HTTP-based highscore client for web/pygbag builds."""

import json
from datetime import datetime


class LocalStorageHighscoreClient:
    """Fallback client using browser localStorage for web builds."""

    def __init__(self):
        """Initialize localStorage client."""
        self._is_web = self._detect_web_environment()
        if self._is_web:
            try:
                import platform

                self.storage = platform.window.localStorage
                print("📦 Using browser localStorage for highscores")
            except Exception as e:
                print(f"⚠️ Error accessing localStorage: {e}")
                self.storage = None
        else:
            self.storage = None

    def _detect_web_environment(self):
        """Detect if running in web/pygbag environment."""
        try:
            import sys

            return sys.platform == "emscripten"
        except:
            return False

    async def add_highscore(self, level_name, player_name, score_breakdown):
        """Add highscore to localStorage."""
        if not self.storage:
            return {"error": "localStorage not available"}

        try:
            # Get existing highscores
            key = f"highscores_{level_name}"
            existing = self.storage.getItem(key)

            if existing:
                highscores = json.loads(existing)
            else:
                highscores = []

            # Add new score
            entry = {
                "player_name": player_name,
                "score": score_breakdown["total_score"],
                "breakdown": score_breakdown,
                "timestamp": datetime.now().isoformat(),
            }

            highscores.append(entry)
            highscores.sort(key=lambda x: x["score"], reverse=True)
            highscores = highscores[:10]  # Keep top 10

            # Save back to localStorage
            self.storage.setItem(key, json.dumps(highscores))
            print(
                f"💾 Highscore saved to localStorage: {player_name} - {score_breakdown['total_score']}"
            )

            return {"success": True}

        except Exception as e:
            print(f"⚠️ Error saving to localStorage: {e}")
            return {"error": str(e)}

    async def get_top_scores(self, level_name, limit=5):
        """Get top scores from localStorage."""
        if not self.storage:
            return []

        try:
            key = f"highscores_{level_name}"
            existing = self.storage.getItem(key)

            if existing:
                highscores = json.loads(existing)
                return highscores[:limit]
            return []

        except Exception as e:
            print(f"⚠️ Error reading from localStorage: {e}")
            return []

    async def is_highscore(self, level_name, score):
        """Check if score qualifies as a highscore."""
        if not self.storage:
            return True

        try:
            key = f"highscores_{level_name}"
            existing = self.storage.getItem(key)

            if not existing:
                return True

            highscores = json.loads(existing)

            if len(highscores) < 10:
                return True

            return score > min(h["score"] for h in highscores)

        except Exception as e:
            print(f"⚠️ Error checking highscore in localStorage: {e}")
            return True


class HTTPHighscoreClient:
    """Client for interacting with highscore API endpoints."""

    _fetch_initialized = False

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

        # Initialize the Fetch API wrapper if in web environment
        if self._is_web and not HTTPHighscoreClient._fetch_initialized:
            self._initialize_fetch()
            HTTPHighscoreClient._fetch_initialized = True

    def _detect_web_environment(self):
        """Detect if running in web/pygbag environment."""
        try:
            import sys

            return sys.platform == "emscripten"
        except:
            return False

    def _initialize_fetch(self):
        """Initialize the JavaScript Fetch API wrapper."""
        try:
            import platform

            js_code = """
window.Fetch = {}
window.Fetch.POST = function * POST (url, data)
{
    console.log('[Fetch] POST: ' + url);
    var request = new Request(url, {
        headers: {'Accept': 'application/json','Content-Type': 'application/json'},
        method: 'POST',
        body: data
    });
    var content = 'undefined';
    fetch(request)
   .then(resp => resp.text())
   .then((resp) => {
        console.log('[Fetch] POST Response:', resp);
        content = resp;
   })
   .catch(err => {
         console.error('[Fetch] POST Error:', err);
         content = JSON.stringify({error: err.toString()});
    });
    while(content == 'undefined'){
        yield;
    }
    yield content;
}
window.Fetch.GET = function * GET (url)
{
    console.log('[Fetch] GET: ' + url);
    var request = new Request(url, { method: 'GET' })
    var content = 'undefined';
    fetch(request)
   .then(resp => resp.text())
   .then((resp) => {
        console.log('[Fetch] GET Response:', resp);
        content = resp;
   })
   .catch(err => {
         console.error('[Fetch] GET Error:', err);
         content = JSON.stringify({error: err.toString()});
    });
    while(content == 'undefined'){
        yield;
    }
    yield content;
}
"""
            platform.window.eval(js_code)
            platform.window.console.log("[HTTP_CLIENT] Fetch API initialized")
        except Exception as e:
            print(f"⚠️ Failed to initialize Fetch API: {e}")

    def _get_api_url(self):
        """Get the API base URL."""
        try:
            import platform

            platform.window.console.log("[HTTP_CLIENT] _get_api_url called")
        except:
            pass

        if self.api_base_url:
            print(f"🌐 Using configured API URL: {self.api_base_url}")
            try:
                import platform

                platform.window.console.log(
                    f"[HTTP_CLIENT] Using configured URL: {self.api_base_url}"
                )
            except:
                pass
            return self.api_base_url

        # In web context, try to detect the deployment URL
        if self._is_web:
            try:
                import platform

                platform.window.console.log("[HTTP_CLIENT] Detecting web environment")

                # Check if we have window.location available
                if not hasattr(platform, "window"):
                    print("⚠️ platform.window not available yet, using relative API URL")
                    platform.window.console.log(
                        "[HTTP_CLIENT] platform.window not available, using /api"
                    )
                    # Default to relative URL - should work on deployed sites
                    return "/api"

                location = platform.window.location
                origin = str(location.origin)

                print(f"🌐 Detected origin: {origin}")
                platform.window.console.log(f"[HTTP_CLIENT] Detected origin: {origin}")

                # If running on localhost, we need to point to the deployed API
                # This should be configured in your deployment
                if "localhost" in origin or "127.0.0.1" in origin:
                    platform.window.console.log(
                        "[HTTP_CLIENT] localhost detected, returning None"
                    )
                    # For localhost, return None to trigger localStorage fallback
                    print("⚠️ Running on localhost - API URL not configured")
                    print("⚠️ Set api_base_url when initializing HighscoreManager")
                    print(
                        "⚠️ Example: HighscoreManager(api_base_url='https://your-app.vercel.app/api')"
                    )
                    return None
                else:
                    # Running on deployed site, use relative URL
                    api_url = "/api"
                    print(f"🌐 Using deployment API URL: {origin}{api_url}")
                    platform.window.console.log(
                        f"[HTTP_CLIENT] Using deployment API: {origin}{api_url}"
                    )
                    return api_url
            except Exception as e:
                print(f"⚠️ Error detecting web environment: {e}")
                try:
                    import platform

                    platform.window.console.error(f"[HTTP_CLIENT] Error: {e}")
                except:
                    pass
                import traceback

                traceback.print_exc()
                # On error, default to relative URL for deployed sites
                print("🌐 Defaulting to relative API URL: /api")
                try:
                    import platform

                    platform.window.console.log(
                        "[HTTP_CLIENT] Defaulting to /api after error"
                    )
                except:
                    pass
                return "/api"

        # For local testing with Python
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
        try:
            import platform

            platform.window.console.log(
                f"[HTTP_CLIENT] add_highscore called: {level_name}, {player_name}, {score_breakdown['total_score']}"
            )
        except:
            pass

        api_url = self._get_api_url()
        if not api_url:
            print("⚠️ API URL not configured, skipping API call")
            try:
                import platform

                platform.window.console.warn("[HTTP_CLIENT] API URL not configured")
            except:
                pass
            return {"error": "API URL not configured"}

        url = f"{api_url}/highscores"
        print(f"📤 Adding highscore to API: {url}")
        try:
            import platform

            platform.window.console.log(f"[HTTP_CLIENT] POST {url}")
        except:
            pass

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
                print(f"✅ Highscore added via API: {response}")
                try:
                    import platform

                    platform.window.console.log(f"[HTTP_CLIENT] Response: {response}")
                except:
                    pass
            else:
                # Use urllib for non-web builds (shouldn't happen, but fallback)
                response = await self._fetch_urllib(url, method="POST", data=payload)

            return response

        except Exception as e:
            print(f"⚠️ Error adding highscore via API: {e}")
            try:
                import platform

                platform.window.console.error(
                    f"[HTTP_CLIENT] Error adding highscore: {e}"
                )
            except:
                pass
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
        try:
            import platform

            platform.window.console.log(
                f"[HTTP_CLIENT] get_top_scores called: {level_name}, limit={limit}"
            )
        except:
            pass

        api_url = self._get_api_url()
        if not api_url:
            print("⚠️ API URL not configured, returning empty scores")
            try:
                import platform

                platform.window.console.warn(
                    "[HTTP_CLIENT] API URL not configured for get_top_scores"
                )
            except:
                pass
            return []

        url = f"{api_url}/highscores?action=get_top_scores&level_name={level_name}&limit={limit}"
        print(f"📥 Getting top scores from API: {url}")
        try:
            import platform

            platform.window.console.log(f"[HTTP_CLIENT] GET {url}")
        except:
            pass

        try:
            if self._is_web:
                response = await self._fetch_web(url, method="GET")
            else:
                response = await self._fetch_urllib(url, method="GET")

            if "scores" in response:
                print(f"✅ Retrieved {len(response['scores'])} scores from API")
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
        api_url = self._get_api_url()
        if not api_url:
            print("⚠️ API URL not configured, defaulting to True")
            return True

        url = f"{api_url}/highscores?action=is_highscore&level_name={level_name}&score={score}"

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

            print(f"🌐 Fetching {method} {url}")

            if method == "POST" and data:
                # Use POST with JSON data
                data_json = json.dumps(data)
                print(f"📤 Request body: {data_json[:200]}...")

                # Use the JavaScript generator pattern from pygbag
                content = await platform.jsiter(
                    platform.window.Fetch.POST(url, data_json)
                )

                print(f"📥 Response: {content[:200]}...")
                result = json.loads(content)
                return result
            else:
                # Use GET
                content = await platform.jsiter(platform.window.Fetch.GET(url))
                print(f"📥 Response: {content[:200]}...")
                result = json.loads(content)
                return result

        except Exception as e:
            print(f"❌ Web fetch failed: {e}")
            import traceback

            traceback.print_exc()
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
