# ETL with Airflow, FastAPI, MongoDB, and Postgres

## 🚀 Overview
This project demonstrates a modern **ETL pipeline** built with:

- **Apache Airflow** → orchestration of ETL tasks  
- **FastAPI** → lightweight API layer  
- **MongoDB** → semi-structured data storage  
- **Postgres** → relational data warehouse  

📊 Data from `data/sample.csv` is ingested into **MongoDB** and **Postgres** via an Airflow DAG.  
🔎 FastAPI provides REST endpoints to query the ingested data.  

This project was created as part of a portfolio for **Data Engineer / Data Analyst** roles.

---

## ⚙️ Tech Stack
- Python 3.11
- Apache Airflow 2.9
- FastAPI + Uvicorn
- MongoDB 7
- PostgreSQL 15
- Docker & Docker Compose

---

## 🏗 Project Structure
.
├── airflow/ # Airflow DAGs
│ └── dags/
│ └── etl_csv_to_mongo_postgres.py
├── fastapi/ # FastAPI app (app.py)
├── sql/ # Init scripts for Postgres warehouse
│ └── init_warehouse.sql
├── data/ # Sample CSV data
│ └── sample.csv
├── docker-compose.yml # Docker services
├── .env.example # Example environment config
├── .gitignore
└── LICENSE

yaml
Copy code

---

## ▶️ Run Locally

### 1. Clone the repository
```bash
git clone git@github.com:sanatdeveloper2003/etl-airflow-mongo-postgres-fastapi.git
cd etl-airflow-mongo-postgres-fastapi
2. Copy .env.example
bash
Copy code
cp .env.example .env
3. Start all services
bash
Copy code
docker compose up -d
4. Access services
Airflow UI → http://localhost:8080
(login: admin, password: admin)

FastAPI Swagger → http://localhost:8000/docs

📊 Example API calls
Health check:

bash
Copy code
curl http://localhost:8000/health
Get data from MongoDB:

bash
Copy code
curl http://localhost:8000/mongo/items
Get data from Postgres warehouse:

bash
Copy code
curl http://localhost:8000/warehouse/items
🧩 Airflow DAG
The DAG etl_csv_to_mongo_postgres.py:

Reads data/sample.csv

Loads rows into MongoDB

Loads rows into Postgres warehouse


📜 License
MIT License © 2025 Sanat Zhengis

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.