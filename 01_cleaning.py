import pandas as pd

path = r"Sample - Superstore.csv"
df = pd.read_csv(path, encoding="latin-1")

# 1. Ubah tipe data
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%m/%d/%Y")
df["Postal Code"] = df["Postal Code"].astype(str).str.zfill(5)

# 2. Kolom tambahan
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)
df["Ship Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
df["Profit Margin %"] = (df["Profit"] / df["Sales"] * 100).round(2)
df["Is Loss"] = df["Profit"] < 0
df["Discount Group"] = pd.cut(
    df["Discount"],
    bins=[-0.01, 0, 0.2, 0.4, 1],
    labels=["0%", "1-20%", "21-40%", ">40%"],
)

# 3. Cek hasilnya
print(df[["Order Date", "Ship Date"]].dtypes)
print(df["Order Date"].min(), df["Order Date"].max())
print(df["Ship Days"].describe())
print(df["Discount Group"].value_counts())
print("Jumlah transaksi rugi:", df["Is Loss"].sum())

# 4. Simpan data bersih
df.to_csv(r"\superstore-analysis\superstore_clean.csv", index=False)
print("Selesai, file bersih tersimpan")