"""Vercel serverless function for highscore operations."""

import json
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler
import psycopg2
from urllib.parse import parse_qs


def get_db_connection():
    """Get a database connection."""
    database_url = os.environ.get("POSTGRES_URL")
    if not database_url:
        raise ValueError("POSTGRES_URL environment variable not set")
    return psycopg2.connect(database_url)


def handle_add_highscore(data):
    """Add a new highscore."""
    required_fields = ["level_name", "player_name", "score_breakdown"]
    for field in required_fields:
        if field not in data:
            return {"error": f"Missing required field: {field}"}, 400

    level_name = data["level_name"]
    player_name = data["player_name"]
    score_breakdown = data["score_breakdown"]

    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO highscores 
            (level_name, player_name, total_score, time_score, trophy_score, 
             damage_score, life_score, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
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

        highscore_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()

        return {"success": True, "id": highscore_id}, 200

    except Exception as e:
        if connection:
            connection.rollback()
        return {"error": str(e)}, 500

    finally:
        if connection:
            connection.close()


def handle_get_top_scores(params):
    """Get top scores for a level."""
    level_name = params.get("level_name", [None])[0]
    if not level_name:
        return {"error": "Missing level_name parameter"}, 400

    limit = int(params.get("limit", ["5"])[0])

    connection = None
    try:
        connection = get_db_connection()
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
        return {"scores": results}, 200

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        if connection:
            connection.close()


def handle_is_highscore(params):
    """Check if a score qualifies as a highscore."""
    level_name = params.get("level_name", [None])[0]
    score = params.get("score", [None])[0]

    if not level_name or not score:
        return {"error": "Missing level_name or score parameter"}, 400

    try:
        score = int(score)
    except ValueError:
        return {"error": "Invalid score value"}, 400

    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Count total scores for this level
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
            return {"is_highscore": True}, 200

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
            is_highscore = score > result[0]
        else:
            is_highscore = True

        return {"is_highscore": is_highscore}, 200

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        if connection:
            connection.close()


class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler."""

    def _send_response(self, data, status_code=200):
        """Send JSON response."""
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        """Handle GET requests."""
        try:
            # Parse query string
            if "?" in self.path:
                path, query_string = self.path.split("?", 1)
                params = parse_qs(query_string)
            else:
                path = self.path
                params = {}

            action = params.get("action", [None])[0]

            if action == "get_top_scores":
                response, status = handle_get_top_scores(params)
            elif action == "is_highscore":
                response, status = handle_is_highscore(params)
            else:
                response, status = {"error": "Invalid action"}, 400

            self._send_response(response, status)

        except Exception as e:
            self._send_response({"error": str(e)}, 500)

    def do_POST(self):
        """Handle POST requests."""
        try:
            # Read request body
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode())

            action = data.get("action")

            if action == "add_highscore":
                response, status = handle_add_highscore(data)
            else:
                response, status = {"error": "Invalid action"}, 400

            self._send_response(response, status)

        except json.JSONDecodeError:
            self._send_response({"error": "Invalid JSON"}, 400)
        except Exception as e:
            self._send_response({"error": str(e)}, 500)
