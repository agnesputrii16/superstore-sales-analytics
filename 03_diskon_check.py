import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

df = pd.read_csv(
    r"superstore_clean.csv",
    parse_dates=["Order Date", "Ship Date"],
)

# 1. Rata-rata diskon per sub-kategori
sub = df.groupby("Sub-Category").agg(
    Avg_Discount=("Discount", "mean"),
    Profit=("Profit", "sum"),
).round(3)
print("=== 1. RATA-RATA DISKON PER SUB-KATEGORI ===")
print(sub.sort_values("Avg_Discount", ascending=False), "\n")

# 2. Rata-rata diskon per region
reg = df.groupby("Region").agg(
    Avg_Discount=("Discount", "mean"),
    Profit=("Profit", "sum"),
).round(3)
print("=== 2. RATA-RATA DISKON PER REGION ===")
print(reg.sort_values("Avg_Discount", ascending=False), "\n")

# 3. Margin Furniture per kelompok diskon
furn = df[df["Category"] == "Furniture"]
f = furn.groupby("Discount Group", observed=True).agg(
    Transaksi=("Sales", "count"),
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
)
f["Margin %"] = (f["Profit"] / f["Sales"] * 100).round(2)
print("=== 3. FURNITURE PER KELOMPOK DISKON ===")
print(f.round(0), "\n")

# 4. Tren rata-rata diskon per tahun
print("=== 4. RATA-RATA DISKON PER TAHUN ===")
print(df.groupby("Year")["Discount"].mean().round(3))