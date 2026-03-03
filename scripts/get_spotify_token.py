"""One-off helper to obtain a Spotify refresh token via OAuth.

Run once locally:
    venv\\Scripts\\python scripts\\get_spotify_token.py

Then copy the printed refresh token into .env as SPOTIFY_REFRESH_TOKEN
and add it as a GitHub Actions secret.
"""

import http.server
import os
import threading
import time
import urllib.parse
import webbrowser
from pathlib import Path

import requests
from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")

CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
REDIRECT_URI = os.environ["SPOTIFY_REDIRECT_URI"]
SCOPES = "user-top-read user-read-recently-played"

_auth_code: str | None = None


class _CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global _auth_code
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        _auth_code = params.get("code", [None])[0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"<h2>Authorised. You can close this tab.</h2>")

    def log_message(self, *_):
        pass


def main() -> None:
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={urllib.parse.quote(REDIRECT_URI, safe='')}"
        f"&scope={urllib.parse.quote(SCOPES, safe='')}"
    )

    port = urllib.parse.urlparse(REDIRECT_URI).port or 8888
    server = http.server.HTTPServer(("", port), _CallbackHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    print("Opening browser for Spotify authorisation...")
    print(f"If it does not open automatically, visit:\n  {auth_url}\n")
    webbrowser.open(auth_url)

    print("Waiting for callback on port", port, "...")
    while _auth_code is None:
        time.sleep(0.5)
    server.shutdown()

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": _auth_code,
            "redirect_uri": REDIRECT_URI,
        },
        auth=(CLIENT_ID, CLIENT_SECRET),
        timeout=10,
    )
    response.raise_for_status()
    refresh_token = response.json()["refresh_token"]

    print("\nSuccess!")
    print(f"\nRefresh token:\n  {refresh_token}")
    print("\nNext steps:")
    print("  1. Add to .env:              SPOTIFY_REFRESH_TOKEN=<token>")
    print("  2. Add GitHub Actions secret: SPOTIFY_REFRESH_TOKEN")


if __name__ == "__main__":
    main()
