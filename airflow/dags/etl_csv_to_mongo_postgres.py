from datetime import datetime
import os
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
import psycopg2
from pymongo import MongoClient

# ---- ENV ----
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
MONGO_DB = os.getenv("MONGO_DB", "etl")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "items")

WH_HOST = os.getenv("WAREHOUSE_HOST", "warehouse-db")
WH_PORT = int(os.getenv("WAREHOUSE_PORT", "5432"))
WH_DB = os.getenv("WAREHOUSE_DB", "warehouse")
WH_USER = os.getenv("WAREHOUSE_USER", "warehouse")
WH_PASS = os.getenv("WAREHOUSE_PASSWORD", "warehouse")

# Airflow-монтирует папку ./data в /opt/airflow/data
CSV_PATH = "/opt/airflow/data/sample.csv"

def load_to_mongo(**_):
    df = pd.read_csv(CSV_PATH)
    client = MongoClient(MONGO_URI)
    col = client[MONGO_DB][MONGO_COLLECTION]
    col.delete_many({})                       # чистим коллекцию для повторяемости
    col.insert_many(df.to_dict(orient="records"))

def load_to_postgres(**_):
    df = pd.read_csv(CSV_PATH)
    conn = psycopg2.connect(
        host=WH_HOST, port=WH_PORT, dbname=WH_DB, user=WH_USER, password=WH_PASS
    )
    cur = conn.cursor()
    for _, row in df.iterrows():
        cur.execute(
            "INSERT INTO public.items (name, value) VALUES (%s, %s);",
            (row["name"], row["value"])
        )
    conn.commit()
    cur.close()
    conn.close()

with DAG(
    dag_id="etl_csv_to_mongo_postgres",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={"owner": "sanat"},
    tags=["etl", "mongo", "postgres"],
) as dag:
    t1 = PythonOperator(task_id="load_to_mongo", python_callable=load_to_mongo)
    t2 = PythonOperator(task_id="load_to_postgres", python_callable=load_to_postgres)
    t1 >> t2
