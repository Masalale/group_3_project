# Import required libraries
# Built-in HTTP server in Python
from http.server import BaseHTTPRequestHandler, HTTPServer
import json  # To send/receive data in JSON format

# Load parsed transactions from parsed_sms.json
with open("../parsed_sms.json", "r") as file:
    transactions = json.load(file)

# Dictionary to store transactions with id as key
transactions_dic = {}

# store transactions in a dictionary with id as key
for i, t in enumerate(transactions, start=1):
    transactions_dic[i] = t

# --------------------------
# Request Handler Class
# --------------------------
class TransactionHandler(BaseHTTPRequestHandler):
    """
    Handles incoming HTTP requests to access the MoMo transactions.
    Every time a client calls our server, this class decides how to respond.
    """

    # Utility method to set headers for JSON responses
    def _set_headers(self, status=200):
        # HTTP status code (200 OK, 404 Not Found, etc.)
        self.send_response(status)
        # Tell client we're sending JSON
        self.send_header("Content-Type", "application/json")
        self.end_headers()  # End headers section

    # Handle GET requests
    def do_GET(self):
        # If the client is asking for /transactions, send the list of transactions
        if self.path == "/transactions":
            self._set_headers()
            # Send list of transactions in JSON format
            self.wfile.write(json.dumps(transactions_dic, indent=4).encode())
        # If the client is asking for /transactions/<id>, send that specific transaction
        elif self.path.startswith("/transactions/"):
            # Extract the transaction ID from the URL
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
            # If the client is asking for something else, respond with 404
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    # Handle DELETE requests
    def do_DELETE(self):
        # to delete a transaction by id
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
                # If the client is asking to delete something else other than transactions, respond with 404
                self._set_headers(404)
                self.wfile.write(json.dumps({"Error": "Not Found the requested resource"}).encode())

    def do_POST(self):
        # to add a new transaction
        if self.path == "/transactions":
            data_length = int(self.headers['Content-Length'])  # Get the size of data
            post_data = self.rfile.read(data_length).decode("utf-8")  # Read the data
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

    # Handle PUT requests
    def do_PUT(self):
        # to update an existing transaction by id
        if self.path.startswith("/transactions/"):
            try:
                transaction_id = int(self.path.split("/")[-1])
                if transaction_id in transactions_dic:
                    data_length = int(self.headers.get('Content-Length', 0))  # Get the size of data
                    put_data = self.rfile.read(data_length).decode("utf-8")  # Read the data
                    try:
                        updated_transaction = json.loads(put_data)  # Parse JSON data
                        transactions_dic[transaction_id] = updated_transaction  # Update dictionary
                        self._set_headers(200)  # 200 OK
                        self.wfile.write(json.dumps({"message": f"Transaction {transaction_id} updated"}, indent=4).encode())
                    except json.JSONDecodeError:
                        self._set_headers(400)  # Bad Request
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
        
# --------------------------
# Run the Server
# --------------------------
def run(port=8080):
    """
    Start the server on the given port (default = 8080).
    """
    server = HTTPServer(
        ("", port), TransactionHandler)  # Bind server to port + handler class
    # Info message in console
    print(f"Server running at http://localhost:{port}")
    print("Use CTRL+C to stop the server")
    server.serve_forever()  # Keep the server running forever (until stopped)


# --------------------------
# Entry Point
# --------------------------
if __name__ == "__main__":
    run()

