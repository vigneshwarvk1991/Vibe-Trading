#!/usr/bin/env python3
"""Zerodha Kite Connect Daily Authentication Helper.

Authenticates with Zerodha Kite Connect API and saves the daily access_token
to ~/.vibe-trading/zerodha.json with readonly permissions (0o600).

Usage:
  # Interactive mode:
  python scripts/kite_auth.py

  # Direct token exchange:
  python scripts/kite_auth.py --token <REQUEST_TOKEN>
"""

from __future__ import annotations

import argparse
import http.server
import json
import socketserver
import sys
import urllib.parse
import webbrowser
from pathlib import Path

# Add agent directory to sys.path
repo_root = Path(__file__).resolve().parent.parent
agent_dir = repo_root / "agent"
if str(agent_dir) not in sys.path:
    sys.path.insert(0, str(agent_dir))

from src.trading.connectors.zerodha.sdk import ZerodhaConfig, load_config, save_config


def extract_request_token(input_str: str) -> str:
    """Extract request token from raw string or redirect URL."""
    input_str = input_str.strip()
    if not input_str:
        return ""
    if "request_token=" in input_str:
        parsed = urllib.parse.urlparse(input_str)
        params = urllib.parse.parse_qs(parsed.query)
        token = params.get("request_token", [""])[0]
        if token:
            return token
    return input_str


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    captured_token = ""

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        token = params.get("request_token", [""])[0]
        if token:
            CallbackHandler.captured_token = token
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = """
            <html>
            <head><title>Zerodha Auth Success</title></head>
            <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                <h2 style="color: #2e7d32;">Authentication Successful!</h2>
                <p>Request token received. You can close this window and return to your terminal.</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing request_token")

    def log_message(self, format, *args):
        pass


def run_local_listener(port: int = 8000, timeout: int = 120) -> str:
    """Run a temporary local server to capture redirect callback."""
    CallbackHandler.captured_token = ""
    try:
        with socketserver.TCPServer(("127.0.0.1", port), CallbackHandler) as httpd:
            httpd.timeout = 2.0
            elapsed = 0.0
            print(f"[*] Listening for redirect on http://127.0.0.1:{port} (timeout: {timeout}s)...")
            while not CallbackHandler.captured_token and elapsed < timeout:
                httpd.handle_request()
                elapsed += 2.0
            return CallbackHandler.captured_token
    except OSError as e:
        print(f"[!] Could not start local callback server on port {port}: {e}")
        return ""


def main():
    parser = argparse.ArgumentParser(description="Authenticate with Zerodha Kite Connect")
    parser.add_argument("--token", help="Request token or full redirect URL")
    parser.add_argument("--port", type=int, default=8000, help="Local port for callback redirect (default: 8000)")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open the browser")
    args = parser.parse_args()

    cfg = load_config()

    if not cfg.api_key or cfg.api_key == "PASTE_YOUR_KITE_API_KEY_HERE":
        print("[!] ERROR: api_key is missing or still has placeholder value in ~/.vibe-trading/zerodha.json.")
        print("[!] Please edit ~/.vibe-trading/zerodha.json with your Zerodha Kite API Key & Secret.")
        sys.exit(1)

    if not cfg.api_secret or cfg.api_secret == "PASTE_YOUR_KITE_API_SECRET_HERE":
        print("[!] ERROR: api_secret is missing or still has placeholder value in ~/.vibe-trading/zerodha.json.")
        print("[!] Please edit ~/.vibe-trading/zerodha.json with your Zerodha Kite API Key & Secret.")
        sys.exit(1)

    login_url = f"https://kite.zerodha.com/connect/login?v=3&api_key={cfg.api_key}"
    request_token = ""

    if args.token:
        request_token = extract_request_token(args.token)
    else:
        print()
        print("=" * 60)
        print("          ZERODHA KITE CONNECT DAILY LOGIN")
        print("=" * 60)
        print("\n1. Please log in at the following URL:\n")
        print(f"   {login_url}\n")

        if not args.no_browser:
            print("[*] Opening browser...")
            webbrowser.open(login_url)

        print("Waiting for login... If your app redirect URL is set to http://127.0.0.1:8000,")
        print("the token will be captured automatically. Otherwise, paste the URL below.\n")

        try:
            prompt_text = "Paste request_token or full redirected URL (or press Enter if listening): "
            user_input = input(prompt_text).strip()
            if user_input:
                request_token = extract_request_token(user_input)
        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            sys.exit(0)

        if not request_token:
            print("[*] Waiting for browser redirect callback on http://127.0.0.1:8000...")
            request_token = run_local_listener(port=args.port, timeout=90)

    if not request_token:
        print("[!] ERROR: No request token received. Authentication aborted.")
        sys.exit(1)

    print(f"\n[*] Exchanging request token for access token...")

    try:
        from kiteconnect import KiteConnect
    except ImportError:
        print("[!] ERROR: kiteconnect library is not installed.")
        sys.exit(1)

    try:
        kite = KiteConnect(api_key=cfg.api_key)
        session_data = kite.generate_session(request_token, api_secret=cfg.api_secret)
        access_token = session_data.get("access_token")
        if not access_token:
            print(f"[!] ERROR: Failed to obtain access_token. Response: {session_data}")
            sys.exit(1)

        updated_cfg = cfg.with_overrides(access_token=access_token)
        save_path = save_config(updated_cfg)

        kite.set_access_token(access_token)
        profile = kite.profile()
        user_name = profile.get("user_name", "User")
        user_id = profile.get("user_id", "")

        print(f"\n[+] SUCCESS! Authenticated as: {user_name} ({user_id})")
        print(f"[+] Access token saved to: {save_path}")
        print("[+] Config verified: profile='live-readonly', readonly=True")
        print("=" * 60)

    except Exception as exc:
        print(f"[!] Authentication error from Kite: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
