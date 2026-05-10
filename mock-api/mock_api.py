import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


USERS = {
    "1": {
        "id": 1,
        "name": "Ada Chen",
        "email": "ada.chen@example.test",
        "phone": "0912-000-001",
        "website": "https://ada.example.test",
        "company": {"name": "Northwind Labs"},
        "address": {"city": "Taipei", "street": "Training Road 1"}
    },
    "2": {
        "id": 2,
        "name": "Ben Lin",
        "email": "ben.lin@example.test",
        "phone": "0912-000-002",
        "website": "https://ben.example.test",
        "company": {"name": "Gateway Studio"},
        "address": {"city": "Kaohsiung", "street": "Compose Avenue 2"}
    }
}

POSTS = {
    "1": {
        "id": 1,
        "userId": 1,
        "title": "How API Gateway shapes frontend contracts",
        "body": "This post is intentionally short for KrakenD aggregation labs."
    },
    "2": {
        "id": 2,
        "userId": 2,
        "title": "Rate limiting from the backend point of view",
        "body": "This sample response helps students compare allow and deny."
    }
}

ORDERS = [
    {"id": 1001, "userId": 1, "total": 1200, "currency": "TWD", "status": "paid"},
    {"id": 1002, "userId": 1, "total": 450, "currency": "TWD", "status": "pending"},
    {"id": 2001, "userId": 2, "total": 980, "currency": "TWD", "status": "paid"}
]


class MockApiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path_parts = [part for part in parsed.path.split("/") if part]

        if parsed.path == "/health":
            self.write_json(200, {"status": "ok"})
            return

        if len(path_parts) == 2 and path_parts[0] == "users":
            self.write_item(USERS, path_parts[1], "user")
            return

        if len(path_parts) == 2 and path_parts[0] == "posts":
            self.write_item(POSTS, path_parts[1], "post")
            return

        if len(path_parts) == 1 and path_parts[0] == "orders":
            query = parse_qs(parsed.query)
            user_id = query.get("userId", [None])[0]
            orders = ORDERS
            if user_id is not None:
                orders = [order for order in ORDERS if str(order["userId"]) == user_id]
            self.write_json(200, orders)
            return

        self.write_json(404, {"error": "not_found", "path": parsed.path})

    def log_message(self, format, *args):
        return

    def write_item(self, data, item_id, resource_name):
        item = data.get(item_id)
        if item is None:
            self.write_json(404, {"error": f"{resource_name}_not_found", "id": item_id})
            return

        self.write_json(200, item)

    def write_json(self, status_code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8000), MockApiHandler)
    server.serve_forever()
