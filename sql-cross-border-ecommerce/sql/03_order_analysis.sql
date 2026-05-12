-- ============================================================
-- 订单分析（6 题）
-- 难度：基础 → 进阶
-- ============================================================

-- ----------------------------------------
-- Q1: 按月统计各市场订单量与销售额
-- 场景：月度经营看板
-- 难度：★☆☆☆☆
-- ----------------------------------------
SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    c.region AS market,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(o.total_amount) AS total_revenue,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value,
    COUNT(DISTINCT o.customer_id) AS unique_customers
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status != 'cancelled'
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m'), c.region
ORDER BY month, market;

-- ----------------------------------------
-- Q2: 计算各国家的订单履约时效（下单到发货）
-- 场景：物流效率监控
-- 难度：★★☆☆☆
-- ----------------------------------------
SELECT
    o.shipping_country,
    COUNT(*) AS total_orders,
    ROUND(AVG(DATEDIFF(o.created_at, o.order_date)), 1) AS avg_fulfillment_days,
    SUM(CASE WHEN o.order_status = 'delivered' THEN 1 ELSE 0 END) AS delivered_count,
    ROUND(
        SUM(CASE WHEN o.order_status = 'delivered' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        1
    ) AS delivery_rate
FROM orders o
WHERE o.order_status IN ('shipped', 'delivered')
GROUP BY o.shipping_country
ORDER BY total_orders DESC;

-- ----------------------------------------
-- Q3: 计算退款率（按市场和品类）
-- 场景：品控与退款分析
-- 难度：★★☆☆☆
-- ----------------------------------------
SELECT
    c.region,
    p.category,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(CASE WHEN o.order_status = 'returned' THEN 1 ELSE 0 END) AS returned_orders,
    ROUND(
        SUM(CASE WHEN o.order_status = 'returned' THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT o.order_id),
        2
    ) AS return_rate_pct
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY c.region, p.category
HAVING COUNT(DISTINCT o.order_id) >= 3
ORDER BY return_rate_pct DESC;

-- ----------------------------------------
-- Q4: 订单金额分段统计（客单价分布）
-- 场景：了解用户消费层级
-- 难度：★★☆☆☆
-- ----------------------------------------
SELECT
    c.region,
    CASE
        WHEN o.total_amount < 20 THEN 'Under $20'
        WHEN o.total_amount < 40 THEN '$20-$39'
        WHEN o.total_amount < 60 THEN '$40-$59'
        WHEN o.total_amount < 80 THEN '$60-$79'
        ELSE '$80+'
    END AS order_range,
    COUNT(*) AS order_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY c.region), 1) AS pct
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status != 'cancelled'
GROUP BY c.region, order_range
ORDER BY c.region, MIN(o.total_amount);

-- ----------------------------------------
-- Q5: 月度环比增长率（MoM Growth）
-- 场景：CEO 月度报告
-- 难度：★★★☆☆
-- ----------------------------------------
WITH monthly_revenue AS (
    SELECT
        DATE_FORMAT(order_date, '%Y-%m') AS month,
        SUM(total_amount) AS revenue
    FROM orders
    WHERE order_status != 'cancelled'
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS prev_month_revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY month))
        / LAG(revenue) OVER (ORDER BY month) * 100,
        1
    ) AS mom_growth_pct
FROM monthly_revenue
ORDER BY month;

-- ----------------------------------------
-- Q6: 各市场 Top 3 支付方式
-- 场景：支付渠道优化
-- 难度：★★★☆☆
-- ----------------------------------------
WITH payment_rank AS (
    SELECT
        c.region,
        o.payment_method,
        COUNT(*) AS usage_count,
        ROW_NUMBER() OVER (PARTITION BY c.region ORDER BY COUNT(*) DESC) AS rn
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status != 'cancelled'
    GROUP BY c.region, o.payment_method
)
SELECT region, payment_method, usage_count
FROM payment_rank
WHERE rn <= 3
ORDER BY region, rn;
