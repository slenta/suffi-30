"""Serve build/web on :8000, mirroring the Vercel /archives/* → pygame-web CDN rewrite."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "build" / "web"
CDN = "https://pygame-web.github.io"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def do_GET(self):
        if self.path.startswith("/archives/"):
            self.send_response(302)
            self.send_header("Location", CDN + self.path)
            self.end_headers()
            return
        super().do_GET()


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
