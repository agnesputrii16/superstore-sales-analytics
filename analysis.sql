-- 1. Omzet dan profit bulanan + growth month-over-month (LAG)
WITH monthly AS (
    SELECT yearmonth,
           ROUND(SUM(sales), 0)  AS sales,
           ROUND(SUM(profit), 0) AS profit
    FROM sales
    GROUP BY yearmonth
)
SELECT yearmonth, sales, profit,
       ROUND((sales - LAG(sales) OVER (ORDER BY yearmonth)) * 100.0
             / LAG(sales) OVER (ORDER BY yearmonth), 1) AS mom_growth_pct
FROM monthly
ORDER BY yearmonth;

-- 2. Ranking sub-kategori berdasarkan profit di dalam tiap kategori (RANK)
SELECT category, sub_category,
       ROUND(SUM(sales), 0)  AS sales,
       ROUND(SUM(profit), 0) AS profit,
       RANK() OVER (PARTITION BY category ORDER BY SUM(profit) DESC) AS rank_in_category
FROM sales
GROUP BY category, sub_category
ORDER BY category, rank_in_category;

-- 3. Pareto: berapa produk yang menyumbang 80% omzet (CTE + cumulative sum)
WITH prod AS (
    SELECT product_name, SUM(sales) AS sales
    FROM sales
    GROUP BY product_name
),
cum AS (
    SELECT product_name, sales,
           SUM(sales) OVER (ORDER BY sales DESC
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum_sales,
           SUM(sales) OVER () AS total_sales
    FROM prod
)
SELECT COUNT(*) AS produk_penyumbang_80pct,
       (SELECT COUNT(*) FROM prod) AS total_produk
FROM cum
WHERE cum_sales - sales < 0.8 * total_sales;

-- 4. Margin per kelompok diskon
SELECT discount_group,
       COUNT(*) AS transaksi,
       ROUND(SUM(sales), 0)  AS sales,
       ROUND(SUM(profit), 0) AS profit,
       ROUND(SUM(profit) * 100.0 / SUM(sales), 2) AS margin_pct
FROM sales
GROUP BY discount_group
ORDER BY MIN(discount);

-- 5. Performa region: diskon rata-rata, profit, dan persen transaksi rugi
SELECT region,
       ROUND(AVG(discount), 3) AS avg_discount,
       ROUND(SUM(profit), 0)   AS profit,
       ROUND(100.0 * SUM(is_loss) / COUNT(*), 1) AS pct_transaksi_rugi
FROM sales
GROUP BY region
ORDER BY avg_discount DESC;