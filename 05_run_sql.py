import sqlite3
import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 60)

conn = sqlite3.connect(r"superstore.db")

with open(r"analysis.sql", encoding="utf-8") as f:
    queries = [q.strip() for q in f.read().split(";") if q.strip()]

for i, q in enumerate(queries, start=1):
    print(f"=== QUERY {i} ===")
    print(pd.read_sql(q, conn), "\n")

conn.close()