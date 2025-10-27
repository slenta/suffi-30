"""
Vercel Serverless Function for managing highscores
"""

from http.server import BaseHTTPRequestHandler
import json
import os

# This is a simple in-memory store for demo purposes
# In production, you'd use Vercel Postgres, KV, or another database
# Example with Vercel KV:
# from vercel_kv import kv


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Get highscores"""
        try:
            # Parse query parameters
            path = self.path.split("?")[0]

            if path == "/api/highscores":
                # TODO: Fetch from database
                # Example: highscores = kv.get('highscores') or []
                highscores = [
                    {"name": "Player1", "score": 1000, "level": "trancefloor"},
                    {"name": "Player2", "score": 850, "level": "trancefloor"},
                ]

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(highscores).encode())
            else:
                self.send_response(404)
                self.end_headers()

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_POST(self):
        """Submit a new highscore"""
        try:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            # Validate required fields
            if not all(k in data for k in ["name", "score", "level"]):
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"error": "Missing required fields"}).encode()
                )
                return

            # TODO: Save to database
            # Example:
            # highscores = kv.get('highscores') or []
            # highscores.append(data)
            # highscores.sort(key=lambda x: x['score'], reverse=True)
            # highscores = highscores[:100]  # Keep top 100
            # kv.set('highscores', highscores)

            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "data": data}).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
