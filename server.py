import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from sync_service import fetch_result


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/api/orders":
            self.send_error(404)
            return
        try:
            payload = fetch_result()
            body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except Exception:
            self.send_error(502, "upstream unavailable")

    def log_message(self, *_):
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
