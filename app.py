from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json
import os
from urllib.parse import urlparse, parse_qs

import api
import database

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 8000))


class StudentServer(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(data.encode())

    def serve_file(self, path, content_type):
        try:
            with open(path, "rb") as file:
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.end_headers()
                self.wfile.write(file.read())

        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"File Not Found")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):

        parsed = urlparse(self.path)

        if parsed.path == "/":
            self.serve_file(
                os.path.join("templates", "index.html"),
                "text/html"
            )
            return

        if parsed.path == "/static/css/style.css":
            self.serve_file(
                os.path.join("static", "css", "style.css"),
                "text/css"
            )
            return

        if parsed.path == "/static/js/script.js":
            self.serve_file(
                os.path.join("static", "js", "script.js"),
                "application/javascript"
            )
            return

        if parsed.path == "/api/students":
            self.send_json(api.get_students())
            return

        if parsed.path.startswith("/api/student/"):
            try:
                student_id = int(parsed.path.split("/")[-1])
                self.send_json(api.get_single_student(student_id))
            except ValueError:
                self.send_json(json.dumps({
                    "success": False,
                    "message": "Invalid Student ID"
                }), 400)
            return

        if parsed.path == "/api/search":

            query = parse_qs(parsed.query)

            keyword = query.get("q", [""])[0]

            self.send_json(api.search(keyword))
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):

        if self.path != "/api/students":
            self.send_response(404)
            self.end_headers()
            return

        try:

            length = int(self.headers.get("Content-Length", 0))

            body = self.rfile.read(length)

            data = json.loads(body.decode())

            self.send_json(api.add(data))

        except json.JSONDecodeError:

            self.send_json(json.dumps({
                "success": False,
                "message": "Invalid JSON"
            }), 400)

    def do_PUT(self):

        if not self.path.startswith("/api/student/"):
            self.send_response(404)
            self.end_headers()
            return

        try:

            student_id = int(self.path.split("/")[-1])

            length = int(self.headers.get("Content-Length", 0))

            body = self.rfile.read(length)

            data = json.loads(body.decode())

            self.send_json(api.update(student_id, data))

        except ValueError:

            self.send_json(json.dumps({
                "success": False,
                "message": "Invalid Student ID"
            }), 400)

        except json.JSONDecodeError:

            self.send_json(json.dumps({
                "success": False,
                "message": "Invalid JSON"
            }), 400)

    def do_DELETE(self):

        if not self.path.startswith("/api/student/"):
            self.send_response(404)
            self.end_headers()
            return

        try:

            student_id = int(self.path.split("/")[-1])

            self.send_json(api.remove(student_id))

        except ValueError:

            self.send_json(json.dumps({
                "success": False,
                "message": "Invalid Student ID"
            }), 400)


database.create_database()

print("=" * 50)
print("      Student Record System")
print("=" * 50)
print(f"Running at : http://{HOST}:{PORT}")
print("=" * 50)

server = ThreadingHTTPServer((HOST, PORT), StudentServer)

try:
    server.serve_forever()

except KeyboardInterrupt:
    print("\nServer Stopped")

finally:
    server.server_close()
