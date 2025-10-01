# MoMo Transactions API Documentation

This document describes the REST API built for managing MoMo transactions
The server runs locally at http://localhost:8000

-Authentication

All requestws must include valid Basic Authentication credentials.
- Credentials are loaded from environment variables: `API_USER` and `API_PASS`
- Withoud valid credentials 401 unauthorized is returned

- Endpoints
1. GET /transactions

Description: Returns all transactions

Example Request:
curl -u admin:password http://localhost:8000/transactions

Example Response:
{ 
    "1": {"date": "2025-01-01", "amount": "5000", "type": "deposit"},
    "2": {"date": "2025-01-03", "amount": "2000", "type": "withdrawal"}
}

- Possible Errors
401 Unatgorized- Invalid or missing credentials 

2. GET transactions(id)
Description: Returns a specific transactiod by ID

Example Request
curl -u admin:password http://localhost:8000/transactions/1

Example Response

{
    "date": "2025-01-01",
    "amount": "5000",
    "type": "deposit"
}

- Possible Errors:
400 Bad Request - Invalid transcation ID format
401 Unauthorized - Invalid or missing credentials
404 Not Found - Transactions does not exist

3. POST/transactions
Description: Creates a new transaction
Example Request:

curl -u admin:password -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{"date":"2025-02-01","amount":"3000","type":"deposit"}'

  Example Response

  {
    "message": "Transaction 3 added",
    "id": 3
}

- Possible Errors:

400 Bad Request - Invalid JSON format
401 Unauthorized - Invalid or missing credentials
404 Not Found - Invalid endpoint path

4.  PUT/transactions(id)

Description: Updates an existing transaction by ID.

Example Request:

curl -u admin:password -X PUT http://localhost:8000/transactions/1 \
  -H "Content-Type: application/json" \
  -d '{"date":"2025-01-01","amount":"7000","type":"deposit"}'

Example Response:

{
    "message": "Transaction 1 updated"
}

- Possible Errors:

400 Bad Request - Invalid transaction ID or JSON format
401 Unauthorized - Invalid or missing credentials
404 Not Found - Transaction does not exist

5. DELETE /transactions(id)
Description: Deletes a transaction by ID.

Example Request:

curl -u admin:password -X DELETE http://localhost:8000/transactions/1

Example Response:

json{
    "message": "Transaction 1 deleted"
}

- Possible Errors:

400 Bad Request - Invalid transaction ID format
401 Unauthorized - Invalid or missing credentials
404 Not Found - Transaction does not exist

- Error Responses:

401 Unauthorized(Authentication Failed)
{
    "error": "Authentication required",
    "message": "Please provide valid credentials"
}

400 Bad Request(Invalid Data)
{
    "error": "Invalid JSON"
}

404 Not Found( Resource Not Found)
{
    "error": "Transaction not found"
}

Testing with Postman

1.Create a new request
2.Select the appropriate HTTP method (GET, POST, PUT, DELETE)
3.Enter the URL: http://localhost:8000/transactions or http://localhost:8000/transactions/{id}
4.Go to Authorization tab → Select Basic Auth → Enter username and password
5.For POST/PUT requests: Go to Body tab → Select raw → Choose JSON → Enter request body
6.Click Send