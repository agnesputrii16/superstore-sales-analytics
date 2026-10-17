import sqlite3
import pandas as pd

df = pd.read_csv(
    r"superstore_clean.csv",
    parse_dates=["Order Date", "Ship Date"],
)

# Rapikan nama kolom jadi snake_case supaya query lebih mudah ditulis
df.columns = (
    df.columns.str.lower()
    .str.replace("%", "pct", regex=False)
    .str.replace("-", "_", regex=False)
    .str.replace(" ", "_", regex=False)
)

# SQLite menyimpan tanggal sebagai teks
df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")
df["ship_date"] = df["ship_date"].dt.strftime("%Y-%m-%d")

conn = sqlite3.connect(r"\superstore-analysis\superstore.db")
df.to_sql("sales", conn, if_exists="replace", index=False)

print(pd.read_sql("SELECT COUNT(*) AS jumlah_baris FROM sales", conn))
print(list(df.columns))
conn.close()