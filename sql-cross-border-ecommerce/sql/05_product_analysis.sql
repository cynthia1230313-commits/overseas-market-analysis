-- ============================================================
-- 商品分析（4 题）
-- 难度：基础 → 进阶
-- ============================================================

-- ----------------------------------------
-- Q13: 各市场 Top 5 畅销商品
-- 场景：了解不同市场的爆品差异
-- 难度：★★☆☆☆
-- ----------------------------------------
WITH product_sales AS (
    SELECT
        c.region,
        p.product_name,
        p.category,
        SUM(oi.quantity) AS units_sold,
        SUM(oi.total_price) AS revenue,
        ROW_NUMBER() OVER (PARTITION BY c.region ORDER BY SUM(oi.quantity) DESC) AS rn
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.order_status != 'cancelled'
    GROUP BY c.region, p.product_name, p.category
)
SELECT region, product_name, category, units_sold, ROUND(revenue, 2) AS revenue
FROM product_sales
WHERE rn <= 5
ORDER BY region, rn;

-- ----------------------------------------
-- Q14: 商品毛利率排名
-- 场景：评估商品盈利能力
-- 难度：★★☆☆☆
-- ----------------------------------------
SELECT
    p.product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.total_price), 2) AS total_revenue,
    ROUND(SUM(oi.quantity * p.cost_price), 2) AS total_cost,
    ROUND(SUM(oi.total_price) - SUM(oi.quantity * p.cost_price), 2) AS gross_profit,
    ROUND(
        (SUM(oi.total_price) - SUM(oi.quantity * p.cost_price))
        / SUM(oi.total_price) * 100,
        1
    ) AS margin_pct
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_status != 'cancelled'
GROUP BY p.product_id, p.product_name, p.category
ORDER BY margin_pct DESC;

-- ----------------------------------------
-- Q15: 关联购买分析（购物篮分析）
-- 场景：发现「经常一起购买」的商品组合
-- 难度：★★★★☆
-- ----------------------------------------
WITH order_pairs AS (
    SELECT
        a.product_id AS product_a,
        b.product_id AS product_b,
        COUNT(DISTINCT a.order_id) AS times_bought_together
    FROM order_items a
    JOIN order_items b ON a.order_id = b.order_id AND a.product_id < b.product_id
    JOIN orders o ON a.order_id = o.order_id
    WHERE o.order_status != 'cancelled'
    GROUP BY a.product_id, b.product_id
),
product_counts AS (
    SELECT product_id, COUNT(DISTINCT order_id) AS order_count
    FROM order_items
    GROUP BY product_id
)
SELECT
    p1.product_name AS product_1,
    p2.product_name AS product_2,
    op.times_bought_together,
    ROUND(op.times_bought_together * 100.0 / pc1.order_count, 1) AS pct_of_product1_orders
FROM order_pairs op
JOIN products p1 ON op.product_a = p1.product_id
JOIN products p2 ON op.product_b = p2.product_id
JOIN product_counts pc1 ON op.product_a = pc1.product_id
WHERE op.times_bought_together >= 2
ORDER BY op.times_bought_together DESC
LIMIT 10;

-- ----------------------------------------
-- Q16: 库存周转预警
-- 场景：识别需要补货或清仓的商品
-- 难度：★★☆☆☆
-- ----------------------------------------
WITH sales_velocity AS (
    SELECT
        oi.product_id,
        SUM(oi.quantity) AS total_sold_6m
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_date >= '2024-01-01'
      AND o.order_date < '2024-07-01'
      AND o.order_status != 'cancelled'
    GROUP BY oi.product_id
)
SELECT
    p.product_name,
    p.category,
    i.warehouse_location,
    i.quantity AS current_stock,
    i.safety_stock,
    COALESCE(sv.total_sold_6m, 0) AS sold_last_6m,
    ROUND(COALESCE(sv.total_sold_6m, 0) / 6.0, 1) AS monthly_velocity,
    ROUND(i.quantity / NULLIF(COALESCE(sv.total_sold_6m, 0) / 6.0, 0), 1) AS months_of_stock,
    CASE
        WHEN i.quantity <= i.safety_stock THEN 'URGENT: Reorder'
        WHEN i.quantity < i.safety_stock * 2 THEN 'WARNING: Low Stock'
        WHEN i.quantity > i.safety_stock * 5
             AND COALESCE(sv.total_sold_6m, 0) / 6.0 < 1 THEN 'SLOW: Consider Discount'
        ELSE 'Healthy'
    END AS stock_status
FROM inventory i
JOIN products p ON i.product_id = p.product_id
LEFT JOIN sales_velocity sv ON i.product_id = sv.product_id
ORDER BY months_of_stock ASC;
