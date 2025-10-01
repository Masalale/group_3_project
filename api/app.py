#!/usr/bin/env python3
"""
RESTful API server to access and manage Mobile Money (MoMo) transactions.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API credentials from .env file
API_USER = os.getenv("API_USER")
API_PASS = os.getenv("API_PASS")

if not API_USER or not API_PASS:
    raise ValueError("API_USER and API_PASS environment variables are required")

# Load parsed transactions from parsed_sms.json
with open("../data/parsed_sms.json", "r") as file:
    transactions = json.load(file)

# Dictionary to store transactions with id as key
transactions_dic = {}

# store transactions in a dictionary with id as key
for i, t in enumerate(transactions, start=1):
    transactions_dic[i] = t

class TransactionHandler(BaseHTTPRequestHandler):
    """
    Handles incoming HTTP requests to access the MoMo transactions.
    Every time a client calls our server, this class decides how to respond.
    """

    def _set_headers(self, status=200):
        """ Set HTTP headers for the response """
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def check_auth(self):
        """Verify basic authentication credentials"""
        auth_header = self.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Basic '):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="MoMo API"')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Authentication required",
                "message": "Invalid credentials"
            }).encode())
            return False
        
        try:
            # Extract and decode credentials
            encoded = auth_header.split(' ', 1)[1]
            decoded = base64.b64decode(encoded).decode('utf-8')
            username, password = decoded.split(':', 1)
            
            # Validate credentials
            if username == API_USER and password == API_PASS:
                return True
        except Exception:
            pass

        # Send 401 Unauthorized if authentication fails
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="MoMo API"')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "error": "Invalid credentials",
            "message": "Username or password is incorrect"
        }).encode())
        return False

    def do_GET(self):
        """ Handle GET requests to fetch transactions """
        if not self.check_auth():
            return

        if self.path == "/transactions":
            self._set_headers()
            self.wfile.write(json.dumps(transactions_dic, indent=4).encode())
        elif self.path.startswith("/transactions/"):
            try:
                transaction_id = int(self.path.split("/")[-1])
                transaction_record = transactions_dic.get(transaction_id)
                if transaction_record:
                    self._set_headers()
                    self.wfile.write(json.dumps(transaction_record, indent=4).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Transaction not found"}).encode())
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid transaction ID"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def do_DELETE(self):
        """ Handle DELETE requests to remove transactions """
        if not self.check_auth():
            return

        if self.path.startswith("/transactions/"):
            try:
                transaction_id = int(self.path.split("/")[-1])
                if transaction_id in transactions_dic:
                    del transactions_dic[transaction_id]
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"message": f"Transaction {transaction_id} deleted"}).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Transaction not found"}).encode())
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid transaction ID"}).encode())
        else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"Error": "Not Found the requested resource"}).encode())

    def do_POST(self):
        """ Handle POST requests to add new transactions """
        if not self.check_auth():
            return

        if self.path == "/transactions":
            data_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(data_length).decode("utf-8")
            try:
                new_transaction = json.loads(post_data)  # Parse JSON data
                new_id = max(transactions_dic.keys()) + 1 if transactions_dic else 1
                transactions_dic[new_id] = new_transaction  # Add to dictionary
                self._set_headers(201)  # 201 Created
                self.wfile.write(json.dumps({"message": f"Transaction {new_id} added", "id": new_id}, indent=4).encode())
            except json.JSONDecodeError:
                self._set_headers(400)  # Bad Request
                self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def do_PUT(self):
        """ Handle PUT requests to update existing transactions """
        if not self.check_auth():
            return

        if self.path.startswith("/transactions/"):
            try:
                transaction_id = int(self.path.split("/")[-1])
                if transaction_id in transactions_dic:
                    data_length = int(self.headers.get('Content-Length', 0))
                    put_data = self.rfile.read(data_length).decode("utf-8")
                    try:
                        updated_transaction = json.loads(put_data)
                        transactions_dic[transaction_id] = updated_transaction
                        self._set_headers(200)
                        self.wfile.write(json.dumps({"message": f"Transaction {transaction_id} updated"}, indent=4).encode())
                    except json.JSONDecodeError:
                        self._set_headers(400)
                        self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Transaction not found"}).encode())
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid transaction ID"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

def run(port=None):
    """ Run the HTTP server """
    if port is None:
        port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "")
    
    server = HTTPServer((host, port), TransactionHandler)
    print(f"Server running at http://{host}:{port}")
    # Print API credentials
    print(f"API Credentials: {API_USER} / {API_PASS}")
    print("Available endpoints:")
    print("  GET /transactions       - List all transactions")
    print("  GET /transactions/{id}  - Get specific transaction")
    print("  POST /transactions      - Create new transaction")
    print("  PUT /transactions/{id}  - Update transaction")
    print("  DELETE /transactions/{id} - Delete transaction")
    print("Use CTRL+C to stop the server")
    server.serve_forever()  # Keep the server running forever (until stopped)

# Main function
if __name__ == "__main__":
    run()

