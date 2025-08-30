from fastapi import FastAPI
import os
import psycopg2
from pymongo import MongoClient

app = FastAPI(title="DE Demo API")

# ---- ENV ----
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
MONGO_DB = os.getenv("MONGO_DB", "etl")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "items")

WH_HOST = os.getenv("WAREHOUSE_HOST", "warehouse-db")
WH_PORT = int(os.getenv("WAREHOUSE_PORT", "5432"))
WH_DB = os.getenv("WAREHOUSE_DB", "warehouse")
WH_USER = os.getenv("WAREHOUSE_USER", "warehouse")
WH_PASS = os.getenv("WAREHOUSE_PASSWORD", "warehouse")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/mongo/items")
def mongo_items():
    client = MongoClient(MONGO_URI)
    col = client[MONGO_DB][MONGO_COLLECTION]
    # не возвращаем _id для простоты
    return list(col.find({}, {"_id": 0}))

@app.get("/warehouse/items")
def warehouse_items():
    conn = psycopg2.connect(
        host=WH_HOST, port=WH_PORT, dbname=WH_DB, user=WH_USER, password=WH_PASS
    )
    cur = conn.cursor()
    cur.execute("SELECT id, name, value, loaded_at FROM public.items ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id": r[0],
            "name": r[1],
            "value": float(r[2]) if r[2] is not None else None,
            "loaded_at": r[3].isoformat()
        }
        for r in rows
    ]
