import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
 
CSV_FILE = "superstore_clean.csv"
OUT_DIR = "images"
os.makedirs(OUT_DIR, exist_ok=True)
 
TEAL = "#2a9d8f"
RED = "#e63946"
 
# ------------------------------------------------------------------
# 1. Load dan siapkan data
# ------------------------------------------------------------------
df = pd.read_csv(CSV_FILE)
df["Order Date"] = pd.to_datetime(df["Order Date"])
 
# Kolom "Discount Group" sudah dibuat di 01_cleaning.py.
# Di sini hanya kita atur urutannya supaya grafik tampil dari 0% sampai >40%.
labels = ["0%", "1-20%", "21-40%", ">40%"]
df["Discount Group"] = pd.Categorical(df["Discount Group"], categories=labels, ordered=True)
 
 
def margin_by_group(data):
    """Jumlah transaksi dan margin (%) per kelompok diskon."""
    g = data.groupby("Discount Group", observed=True).agg(
        transactions=("Profit", "size"),
        sales=("Sales", "sum"),
        profit=("Profit", "sum"),
    )
    g["margin_pct"] = g["profit"] / g["sales"] * 100
    return g
 
 
def bar_margin(g, title, filename):
    """Bar chart margin per kelompok diskon (hijau = untung, merah = rugi)."""
    values = g["margin_pct"]
    colors = [TEAL if v >= 0 else RED for v in values]
 
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(g.index.astype(str), values, color=colors, width=0.6)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xlabel("Discount group")
    ax.set_ylabel("Profit margin (%)")
 
    low = min(0, values.min()) * 1.25 - 5
    high = max(0, values.max()) * 1.25 + 5
    ax.set_ylim(low, high)
 
    for bar, v in zip(bars, values):
        offset = 2 if v >= 0 else -2
        va = "bottom" if v >= 0 else "top"
        ax.text(bar.get_x() + bar.get_width() / 2, v + offset,
                f"{v:.1f}%", ha="center", va=va, fontsize=10)
 
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, filename), dpi=150)
    plt.close(fig)
 
 
# ------------------------------------------------------------------
# 2. Grafik 1: margin per kelompok diskon (semua transaksi)
# ------------------------------------------------------------------
overall = margin_by_group(df)
bar_margin(overall,
           "Profit margin falls as discount rises",
           "01_margin_by_discount.png")
 
print("=== Grafik 1: margin per kelompok diskon (semua transaksi) ===")
print(overall[["transactions", "margin_pct"]].round(1))
 
# ------------------------------------------------------------------
# 3. Grafik 2: omzet dan profit per bulan
# ------------------------------------------------------------------
monthly = df.groupby(df["Order Date"].dt.to_period("M"))[["Sales", "Profit"]].sum()
monthly.index = monthly.index.to_timestamp()
 
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(monthly.index, monthly["Sales"], label="Sales", color="#264653", linewidth=2)
ax.plot(monthly.index, monthly["Profit"], label="Profit", color="#e76f51", linewidth=2)
ax.set_title("Monthly sales and profit, 2014-2017", fontsize=13, fontweight="bold")
ax.set_ylabel("USD")
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: "$0" if x == 0 else f"${x/1000:.0f}K"))
ax.legend(frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, "02_monthly_sales_profit.png"), dpi=150)
plt.close(fig)
 
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
print("\n=== Grafik 2: total seluruh periode ===")
print(f"Sales : ${total_sales:,.0f}")
print(f"Profit: ${total_profit:,.0f}  (margin {total_profit / total_sales * 100:.1f}%)")
print(f"Jumlah bulan di grafik: {len(monthly)}")
 
# ------------------------------------------------------------------
# 4. Grafik 3: margin Furniture per kelompok diskon
# ------------------------------------------------------------------
furniture = margin_by_group(df[df["Category"] == "Furniture"])
bar_margin(furniture,
           "Furniture: margin by discount level",
           "03_furniture_margin_by_discount.png")

print("\n=== Grafik 3: margin Furniture per kelompok diskon ===")
print(furniture[["transactions", "margin_pct"]].round(1))
 
print(f"\nSelesai. 3 file PNG tersimpan di folder '{OUT_DIR}/'.")
