## C5 TEAM 13

## Project Description
Enterprise Web App for processing Mobile Money (MoMo) SMS transaction data.
+ This project processes MoMo SMS XML data, cleans & categorizes it, stores it in a relational database, and provides a frontend dashboard for visualization and analysis.

## TEAM MEMBERS
1. Clarence Ng'ang'a Chomba 
2. Neville Ngothe Iregi
3. Fadhili Beracah Lumumba

## Project Structure

```
.
├── README.md
├── .env.example
├── requirements.txt
├── index.html
├── web/
│   ├── styles.css
│   ├── chart_handler.js
│   └── assets/
├── data/
|   ├── database
│   │   └── database_setup.sql
│   ├── raw/
│   │   └── parsed_sms.json
│   ├── examples
│   │   └── json_schemas.json
│   ├── logs/
│   │   ├── etl.log
│   └── db.sqlite3
├── etl/
│   ├── __init__.py
│   ├── config.py
│   ├── parse_xml.py
│   ├── clean_normalize.py
│   ├── categorize.py
│   ├── load_db.py
│   └── run.py
├── api/
|   ├── .env
│   ├── venv/
│   ├── app.py
│   ├── db.py
│   └── schemas.py                 
│── dsa/
|   ├── dsa_search.py
│   ├── parse_xml.py                
│── docs/
│   ├── ERD diagram
│   ├── api_docs.md
│── screenshots/
|   ├── api_testing screenshots/
│   ├── constraints/
│   ├── database rules/
│   ├── query results/
│── README.md             
├── scripts/
│   ├── run_etl.sh
│   ├── export_json.sh
│   └── serve_frontend.sh
└── tests/
    ├── test_parse_xml.py
    ├── test_clean_normalize.py
    └── test_categorize.py
```

## Database Design
**Design rationale and justification**  

Using the [MoMo sms XML data structure](data/raw/momo.xml), we designed an Entity-Relationship Diagram(ERD) for our MoMo SMS data processing system, which needs to handle various types of mobile money transactions. We created the database schema to meet business requirements and provide a model that can efficiently store, query, and analyze transaction data while maintaining data integrity and supporting future scalability.

Hence, we created five entities based on the business requirements: **Users, transactions, system logs, transaction categories, and user transaction stats**. Users could represent one of 2 people; either a sender/receiver, depending on the sms. They could have attributes such as their full name, phone number, and whether the account is a business or an individual. Transactions encompass all financial details from the MoMo's sms data, including the amount transacted, transaction charges, balance, message data(body), and processing timestamps. Transaction categories define the categories that mobile money transactions could fall under, such as deposit, withdrawal, transfer, and airtime. The categories provide for classification and filtering. System Logs track data processing and allow for error tracking within the system.

To resolve the many-to-many relationship between and transaction categories and users, we introduced a **User\_Transaction\_Stats** table. This would help us be flexible in dealing with the data and maintain the relationship between the two entities. The **User\_Transaction\_Stats** entity that combines user activity per category with attributes such as frequency, total amounts, and the last transaction date for dashboard and analysis purposes. Moreover, the model uses primary and foreign keys to ensure accurate references in tables.

The interactions of the entities establish a clean, scalable, and analytic design. It mimics a real data processing system, translating business requirements into a solid database schema and SQL execution.

## Data Dictionary

Our database schema consists of five main tables that store and manage MoMo SMS transaction data:

### USERS
| Column Name | Data Type | Key | Description |
| :---------- | :-------- | :-- | :---------- |
| user_id | INT | Primary Key | Unique identifier for each user |
| full_name | VARCHAR | | Full legal name of the user |
| phone_number | VARCHAR | | User's phone number linked to their account |
| is_business | BOOLEAN | | Indicates whether the account is an individual or business |
| created_at | TIMESTAMP | | Date and time when the user record was created |

### TRANSACTIONS
| Column Name | Data Type | Key | Description |
| :---------- | :-------- | :-- | :---------- |
| transaction_id | BIGINT | Primary Key | Unique identifier for each transaction |
| user_id | INT | Foreign Key | References `USERS.user_id` (who made the transaction) |
| category_id | INT | Foreign Key | References `TRANSACTION_CATEGORIES.category_id` (type of transaction) |
| sms_date | DATETIME | | Date and time when the transaction SMS was received |
| message_body | TEXT | | Full text of the SMS message containing transaction details |
| service_centre | VARCHAR | | Mobile service center that processed the SMS |
| amount | DECIMAL | | Amount of money transferred/paid |
| fee | DECIMAL | | Transaction fee charged |
| new_balance | DECIMAL | | Account balance after the transaction |
| direction | ENUM | | Indicates transaction flow: `INCOMING` or `OUTGOING` |
| external_tx_id | VARCHAR | | External transaction reference ID (from mobile money provider) |
| processed_at | TIMESTAMP | | Date and time when the transaction was processed in the system |

### TRANSACTION_CATEGORIES
| Column Name | Data Type | Key | Description |
| :---------- | :-------- | :-- | :---------- |
| category_id | INT | Primary Key | Unique identifier for each transaction category |
| category_name | VARCHAR | | Human readable name of transaction category (payment, transfer, etc.) |
| description | TEXT | | Detailed description of the category |

### SYSTEM_LOGS
| Column Name | Data Type | Key | Description |
| :---------- | :-------- | :-- | :---------- |
| log_id | BIGINT | Primary Key | Unique identifier for each log entry |
| log_level | ENUM | | Severity of the log (e.g., INFO, WARNING, ERROR) |
| message | TEXT | | Log message providing details about the event |
| transaction_id | BIGINT | Foreign Key | References `TRANSACTIONS.transaction_id` (if log relates to a transaction) |
| processing_stage | VARCHAR | | Stage of processing when the log was created (e.g., ingestion, validation) |
| created_at | TIMESTAMP | | Date and time when the entry was created |

### USER_TRANSACTION_STATS
| Column Name | Data Type | Key | Description |
| :---------- | :-------- | :-- | :---------- |
| stat_id | INT | Primary Key | Unique identifier for each user transaction statistics record |
| user_id | INT | Foreign Key | References `USERS.user_id` |
| category_id | INT | Foreign Key | References `TRANSACTION_CATEGORIES.category_id` |
| frequency_count | INT | | Total number of transactions by the user in the given category |
| total_amount | DECIMAL | | Total monetary value of transactions in the category |
| last_transaction_date | TIMESTAMP | | Timestamp of the most recent transaction in the category |


## Key Folders:
- **web/**: Frontend files
- **data/**: Backend files (raw XML, processed JSON, SQLite DB, logs)
- **etl/**: Data processing pipeline
- **api/**: REST API implementation
- **dsa/**: Data parsing and DSA comparison
- **docs/**: API documentation
- **scripts/**: Automation scripts
- **screenshots/**: screenshots of test cases with curl/postman
- **tests/**: Unit tests

## Setup Instructions
1. Clone the repository
```
git clone https://github.com/masalale/group_3_project.git
cd group_3_project
```

2. Install Dependencies
This project uses Python 3.8+ and requires the following packages:
```
pip install -r requirements.txt
```

3. Run Data Parsing & DSA Comparison

Convert XML to JSON and compare search efficiency:
```
cd dsa
python parse_xml
python dsa_search.py
```

4. Run the REST API
```
cd api
python app.py
```

The API will start on:
```
http://localhost:8000
```

### Authentication

All endpoints are protected with Basic Authentication.

Example with curl:
```
curl -u admin:password http://localhost:8000/transactions
```

If invalid credentials are used, you will see:
```
401 Unauthorized
```

## API Endpoints
**GET /transactions**
Retrieve all SMS transactions.

**GET /transactions/{id}**
Retrieve a single transaction by ID.

**POST /transactions**
Add a new transaction

**PUT /transactions/{id}**
Update an existing transaction.

**DELETE /transactions/{id}**
Delete a transaction by ID.

- Full details are in **docs/api_docs.md**


## Data Structures & Algorithms

**Linear Search** → Iterates through all transactions in a list.

**Dictionary Lookup** → Uses transaction ID as a key for O(1) access.


✅ Testing
Tested using curl and Postman.
Screenshots included in the screenshots/ folder of:
    1. Successful GET with valid credentials
    2. Unauthorized GET with invalid credentials
    3. Successful POST, PUT, DELETE


## Architecture Diagram
![Architecture Diagram](/architecture_diagram.jpg)

## Project Links
- **System Architecture Diagram:** [View Architecture](https://miro.com/app/board/uXjVJKqaqkQ=/?share_link_id=412469949639)
- **Scrum Board:** [Project Management Board](https://github.com/users/Masalale/projects/4)
- **Repository:** [GitHub Repository](https://github.com/Masalale/group_3_project)

