import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

df = pd.read_csv(
    r"superstore_clean.csv",
    parse_dates=["Order Date", "Ship Date"],
)

def margin(g):
    return (g["Profit"].sum() / g["Sales"].sum() * 100).round(2)

# 1. Tren per tahun
yearly = df.groupby("Year").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).round(0)
yearly["Sales Growth %"] = (yearly["Sales"].pct_change() * 100).round(1)
yearly["Margin %"] = (yearly["Profit"] / yearly["Sales"] * 100).round(2)
print("=== 1. PER TAHUN ===")
print(yearly, "\n")

# 2. Per kategori
cat = df.groupby("Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).round(0)
cat["Margin %"] = (cat["Profit"] / cat["Sales"] * 100).round(2)
print("=== 2. PER KATEGORI ===")
print(cat.sort_values("Profit", ascending=False), "\n")

# 3. Per sub-kategori (urut dari profit terkecil)
sub = df.groupby("Sub-Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).round(0)
sub["Margin %"] = (sub["Profit"] / sub["Sales"] * 100).round(2)
print("=== 3. PER SUB-KATEGORI (profit terendah di atas) ===")
print(sub.sort_values("Profit"), "\n")

# 4. Per region
reg = df.groupby("Region").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).round(0)
reg["Margin %"] = (reg["Profit"] / reg["Sales"] * 100).round(2)
print("=== 4. PER REGION ===")
print(reg.sort_values("Profit", ascending=False), "\n")

# 5. Dampak diskon
order = ["0%", "1-20%", "21-40%", ">40%"]
disc = df.groupby("Discount Group").agg(
    Transaksi=("Sales", "count"), Sales=("Sales", "sum"), Profit=("Profit", "sum")
).round(0).reindex(order)
disc["Margin %"] = (disc["Profit"] / disc["Sales"] * 100).round(2)
print("=== 5. DAMPAK DISKON ===")
print(disc, "\n")

# 6. Pareto produk
prod = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False)
cum_share = prod.cumsum() / prod.sum()
n80 = (cum_share <= 0.8).sum() + 1
print("=== 6. PARETO ===")
print(f"Total produk: {len(prod)}")
print(f"Produk yang menyumbang 80% omzet: {n80} ({n80 / len(prod) * 100:.1f}% dari total produk)")