# C5 TEAM 13

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
│   ├── raw/
│   │   └── momo.xml
│   ├── processed/
│   │   └── dashboard.json
│   ├── logs/
│   │   ├── etl.log
│   │   └── dead_letter/
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
│   ├── __init__.py
│   ├── app.py
│   ├── db.py
│   └── schemas.py
├── scripts/
│   ├── run_etl.sh
│   ├── export_json.sh
│   └── serve_frontend.sh
└── tests/
    ├── test_parse_xml.py
    ├── test_clean_normalize.py
    └── test_categorize.py
```

## Key Folders:
- **web/**: Frontend files
- **data/**: Backend files (raw XML, processed JSON, SQLite DB, logs)
- **etl/**: Data processing pipeline
- **api/**: REST API
- **scripts/**: Automation scripts
- **tests/**: Unit tests

## Project Links
- **High Level System Architecture:** [View Architecture](https://miro.com/app/board/uXjVJKqaqkQ=/?share_link_id=412469949639)
- **Scrum Board:** [Project Management Board](https://github.com/users/Masalale/projects/4)
  
