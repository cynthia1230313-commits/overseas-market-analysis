-- ============================================================
-- Olist 巴西电商 — SQL 分析查询集
-- 数据源：Brazilian E-Commerce Public Dataset (Kaggle)
-- 数据库：MySQL / PostgreSQL 兼容
-- 难度覆盖：基础 → 进阶（窗口函数 / CTE / 留存分析 / 漏斗）
-- ============================================================

-- ============================================================
-- PART 1: 整体经营指标
-- ============================================================

-- Q1: 月度 GMV、订单量、客单价趋势
SELECT
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS gmv,
    ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2) AS aov,
    COUNT(DISTINCT c.customer_unique_id) AS unique_customers
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')
ORDER BY month;

-- Q2: YoY 增长率（使用 LAG 窗口函数）
WITH monthly_revenue AS (
    SELECT
        DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
        SUM(oi.price) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')
)
SELECT
    month,
    ROUND(revenue, 2) AS revenue,
    ROUND(LAG(revenue) OVER (ORDER BY month), 2) AS prev_month_revenue,
    ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) / LAG(revenue) OVER (ORDER BY month) * 100, 1) AS mom_growth_pct
FROM monthly_revenue
ORDER BY month;


-- ============================================================
-- PART 2: 用户留存队列分析
-- ============================================================

-- Q3: 按月 Cohort 计算用户留存率
WITH first_purchase AS (
    SELECT
        c.customer_unique_id,
        DATE_FORMAT(MIN(o.order_purchase_timestamp), '%Y-%m') AS cohort_month
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),
user_orders AS (
    SELECT
        c.customer_unique_id,
        DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS purchase_month
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id, DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')
),
cohort_data AS (
    SELECT
        fp.cohort_month,
        TIMESTAMPDIFF(MONTH, STR_TO_DATE(CONCAT(fp.cohort_month, '-01'), '%Y-%m-%d'),
                      STR_TO_DATE(CONCAT(uo.purchase_month, '-01'), '%Y-%m-%d')) AS month_offset,
        COUNT(DISTINCT uo.customer_unique_id) AS active_users
    FROM first_purchase fp
    JOIN user_orders uo ON fp.customer_unique_id = uo.customer_unique_id
    GROUP BY fp.cohort_month, month_offset
),
cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT customer_unique_id) AS total_users
    FROM first_purchase
    GROUP BY cohort_month
)
SELECT
    cd.cohort_month,
    cd.month_offset,
    cd.active_users,
    cs.total_users,
    ROUND(cd.active_users * 100.0 / cs.total_users, 1) AS retention_pct
FROM cohort_data cd
JOIN cohort_size cs ON cd.cohort_month = cs.cohort_month
ORDER BY cd.cohort_month, cd.month_offset;


-- ============================================================
-- PART 3: 复购与用户生命周期
-- ============================================================

-- Q4: 复购率 & 用户购买频次分布
WITH user_order_count AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS n_orders,
        SUM(oi.price) AS total_spend
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)
SELECT
    n_orders,
    COUNT(*) AS user_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct,
    ROUND(AVG(total_spend), 2) AS avg_total_spend
FROM user_order_count
GROUP BY n_orders
ORDER BY n_orders;

-- Q5: 平均复购间隔（天）
WITH order_sequence AS (
    SELECT
        c.customer_unique_id,
        o.order_purchase_timestamp,
        ROW_NUMBER() OVER (PARTITION BY c.customer_unique_id ORDER BY o.order_purchase_timestamp) AS order_seq
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
),
repurchase_gap AS (
    SELECT
        a.customer_unique_id,
        DATEDIFF(b.order_purchase_timestamp, a.order_purchase_timestamp) AS days_to_next
    FROM order_sequence a
    JOIN order_sequence b
        ON a.customer_unique_id = b.customer_unique_id
        AND a.order_seq = b.order_seq - 1
)
SELECT
    ROUND(AVG(days_to_next), 1) AS avg_repurchase_days,
    ROUND(MIN(days_to_next), 0) AS min_days,
    ROUND(MAX(days_to_next), 0) AS max_days,
    -- 使用 PERCENTILE_CONT (PostgreSQL) 或子查询计算中位数
    ROUND(AVG(CASE WHEN row_num * 2 >= total_rows - 1 AND row_num * 2 <= total_rows + 1 THEN days_to_next END), 0) AS median_days
FROM (
    SELECT
        days_to_next,
        ROW_NUMBER() OVER (ORDER BY days_to_next) AS row_num,
        COUNT(*) OVER () AS total_rows
    FROM repurchase_gap
    WHERE days_to_next > 0
) t;


-- ============================================================
-- PART 4: 品类绩效与 ABC 分类
-- ============================================================

-- Q6: 品类 ABC 分类（累计营收贡献）
WITH cat_revenue AS (
    SELECT
        t.product_category_name_english AS category,
        SUM(oi.price) AS revenue,
        COUNT(DISTINCT o.order_id) AS orders,
        COUNT(DISTINCT c.customer_unique_id) AS customers
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
    WHERE o.order_status = 'delivered'
    GROUP BY t.product_category_name_english
),
ranked AS (
    SELECT
        category,
        revenue,
        orders,
        customers,
        ROUND(revenue * 100.0 / SUM(revenue) OVER (), 2) AS revenue_pct,
        ROUND(SUM(revenue) OVER (ORDER BY revenue DESC) * 100.0 / SUM(revenue) OVER (), 1) AS cum_pct
    FROM cat_revenue
)
SELECT
    category,
    ROUND(revenue, 2) AS revenue,
    revenue_pct,
    cum_pct,
    CASE
        WHEN cum_pct <= 50 THEN 'A'
        WHEN cum_pct <= 80 THEN 'B'
        ELSE 'C'
    END AS abc_class
FROM ranked
ORDER BY revenue DESC;


-- ============================================================
-- PART 5: 评分驱动因素分析
-- ============================================================

-- Q7: 配送时效对评分的影响
SELECT
    CASE
        WHEN DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp) <= 5 THEN '0-5 days'
        WHEN DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp) <= 10 THEN '6-10 days'
        WHEN DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp) <= 15 THEN '11-15 days'
        WHEN DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp) <= 20 THEN '16-20 days'
        WHEN DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp) <= 30 THEN '21-30 days'
        ELSE '30+ days'
    END AS delivery_bucket,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(AVG(r.review_score), 2) AS avg_score,
    ROUND(SUM(CASE WHEN r.review_score >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_positive
FROM orders o
JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY delivery_bucket
ORDER BY AVG(DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp));

-- Q8: 价格区间与评分关系
SELECT
    CASE
        WHEN oi.price < 50 THEN '< 50 BRL'
        WHEN oi.price < 100 THEN '50-100 BRL'
        WHEN oi.price < 200 THEN '100-200 BRL'
        WHEN oi.price < 500 THEN '200-500 BRL'
        ELSE '500+ BRL'
    END AS price_range,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(AVG(r.review_score), 2) AS avg_score,
    ROUND(AVG(oi.freight_value), 2) AS avg_freight
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY price_range
ORDER BY AVG(oi.price);


-- ============================================================
-- PART 6: 卖家与地理分析
-- ============================================================

-- Q9: 卖家集中度（头部卖家贡献）
WITH seller_revenue AS (
    SELECT
        s.seller_id,
        s.seller_state,
        SUM(oi.price) AS revenue,
        COUNT(DISTINCT o.order_id) AS orders
    FROM sellers s
    JOIN order_items oi ON s.seller_id = oi.seller_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY s.seller_id, s.seller_state
),
ranked AS (
    SELECT
        seller_id,
        seller_state,
        revenue,
        orders,
        ROUND(revenue * 100.0 / SUM(revenue) OVER (), 2) AS revenue_pct,
        ROUND(SUM(revenue) OVER (ORDER BY revenue DESC) * 100.0 / SUM(revenue) OVER (), 1) AS cum_pct,
        NTILE(5) OVER (ORDER BY revenue DESC) AS quintile
    FROM seller_revenue
)
SELECT
    quintile,
    COUNT(*) AS seller_count,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(revenue_pct), 1) AS revenue_share_pct
FROM ranked
GROUP BY quintile
ORDER BY quintile;

-- Q10: 各州客单价与评分
SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS orders,
    COUNT(DISTINCT c.customer_unique_id) AS customers,
    ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value,
    ROUND(AVG(r.review_score), 2) AS avg_score,
    ROUND(SUM(oi.price) / COUNT(DISTINCT c.customer_unique_id), 2) AS revenue_per_customer
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
HAVING COUNT(DISTINCT o.order_id) > 100
ORDER BY revenue_per_customer DESC;


-- ============================================================
-- PART 7: 支付行为分析
-- ============================================================

-- Q11: 支付方式与客单价/分期偏好
SELECT
    p.payment_type,
    COUNT(DISTINCT p.order_id) AS orders,
    ROUND(AVG(p.payment_value), 2) AS avg_payment,
    ROUND(AVG(p.payment_installments), 1) AS avg_installments,
    ROUND(SUM(CASE WHEN p.payment_installments > 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_installment
FROM order_payments p
JOIN orders o ON p.order_id = o.order_id
WHERE o.order_status = 'delivered'
  AND p.payment_sequential = 1  -- 只看首笔支付，避免重复计算
GROUP BY p.payment_type
ORDER BY orders DESC;
