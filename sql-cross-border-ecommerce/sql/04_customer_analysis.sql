-- ============================================================
-- 用户分析（6 题）
-- 难度：基础 → 进阶
-- ============================================================

-- ----------------------------------------
-- Q7: RFM 用户分群
-- 场景：识别高价值用户，制定差异化运营策略
-- 难度：★★★★☆
-- ----------------------------------------
WITH rfm AS (
    SELECT
        c.customer_id,
        c.country,
        c.region,
        DATEDIFF('2024-07-01', MAX(o.order_date)) AS recency_days,
        COUNT(DISTINCT o.order_id) AS frequency,
        COALESCE(SUM(o.total_amount), 0) AS monetary
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.order_status != 'cancelled'
    GROUP BY c.customer_id, c.country, c.region
),
rfm_scored AS (
    SELECT *,
        NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,  -- 越低越好 → 分数越高
        NTILE(4) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(4) OVER (ORDER BY monetary ASC) AS m_score
    FROM rfm
)
SELECT
    region,
    CASE
        WHEN r_score = 4 AND f_score = 4 AND m_score = 4 THEN 'Champion'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
        WHEN r_score >= 3 AND f_score <= 2 THEN 'New/Potential'
        WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost'
        WHEN f_score >= 3 AND m_score <= 2 THEN 'Price Sensitive'
        WHEN m_score >= 3 AND f_score <= 1 THEN 'Big Spender'
        ELSE 'Average'
    END AS segment,
    COUNT(*) AS user_count,
    ROUND(AVG(recency_days), 0) AS avg_recency,
    ROUND(AVG(frequency), 1) AS avg_frequency,
    ROUND(AVG(monetary), 2) AS avg_spend
FROM rfm_scored
GROUP BY region, segment
ORDER BY region, user_count DESC;

-- ----------------------------------------
-- Q8: 用户生命周期价值（LTV）按渠道来源
-- 场景：评估各获客渠道 ROI
-- 难度：★★★☆☆
-- ----------------------------------------
SELECT
    c.region,
    c.channel_source,
    COUNT(DISTINCT c.customer_id) AS acquired_users,
    ROUND(COUNT(DISTINCT o.order_id) * 1.0 / COUNT(DISTINCT c.customer_id), 2) AS avg_orders_per_user,
    ROUND(COALESCE(SUM(o.total_amount), 0) / COUNT(DISTINCT c.customer_id), 2) AS ltv,
    ROUND(COALESCE(SUM(o.total_amount), 0) / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS aov
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.order_status != 'cancelled'
GROUP BY c.region, c.channel_source
ORDER BY c.region, ltv DESC;

-- ----------------------------------------
-- Q9: 用户留存分析（月度回购率）
-- 场景：衡量用户粘性
-- 难度：★★★★☆
-- ----------------------------------------
WITH first_purchase AS (
    SELECT
        customer_id,
        MIN(DATE_FORMAT(order_date, '%Y-%m')) AS cohort_month
    FROM orders
    WHERE order_status != 'cancelled'
    GROUP BY customer_id
),
cohort_orders AS (
    SELECT
        fp.cohort_month,
        DATE_FORMAT(o.order_date, '%Y-%m') AS order_month,
        COUNT(DISTINCT o.customer_id) AS customers
    FROM first_purchase fp
    JOIN orders o ON fp.customer_id = o.customer_id AND o.order_status != 'cancelled'
    GROUP BY fp.cohort_month, DATE_FORMAT(o.order_date, '%Y-%m')
),
cohort_size AS (
    SELECT cohort_month, SUM(customers) AS total_cohort
    FROM cohort_orders
    GROUP BY cohort_month
)
SELECT
    co.cohort_month,
    co.order_month,
    co.customers,
    ROUND(co.customers * 100.0 / cs.total_cohort, 1) AS retention_pct
FROM cohort_orders co
JOIN cohort_size cs ON co.cohort_month = cs.cohort_month
ORDER BY co.cohort_month, co.order_month;

-- ----------------------------------------
-- Q10: 流失预警：超过 90 天未购买的用户
-- 场景：识别需要唤醒的用户
-- 难度：★★☆☆☆
-- ----------------------------------------
SELECT
    c.customer_id,
    c.email,
    c.region,
    c.country,
    MAX(o.order_date) AS last_purchase_date,
    DATEDIFF('2024-07-01', MAX(o.order_date)) AS days_since_last_purchase,
    COUNT(DISTINCT o.order_id) AS lifetime_orders,
    COALESCE(SUM(o.total_amount), 0) AS lifetime_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_status != 'cancelled'
GROUP BY c.customer_id, c.email, c.region, c.country
HAVING DATEDIFF('2024-07-01', MAX(o.order_date)) > 90
ORDER BY lifetime_value DESC;

-- ----------------------------------------
-- Q11: 各市场新老用户贡献占比
-- 场景：区分增长来自新客还是老客
-- 难度：★★☆☆☆
-- ----------------------------------------
WITH user_type AS (
    SELECT
        c.region,
        o.order_id,
        o.total_amount,
        CASE
            WHEN o.order_date = c.first_order THEN 'New'
            ELSE 'Returning'
        END AS user_category
    FROM orders o
    JOIN (
        SELECT customer_id, region, MIN(order_date) AS first_order
        FROM orders
        JOIN customers ON orders.customer_id = customers.customer_id
        WHERE order_status != 'cancelled'
        GROUP BY customer_id, region
    ) c ON o.customer_id = c.customer_id
    WHERE o.order_status != 'cancelled'
)
SELECT
    region,
    user_category,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(SUM(total_amount), 2) AS revenue,
    ROUND(SUM(total_amount) * 100.0 / SUM(SUM(total_amount)) OVER (PARTITION BY region), 1) AS revenue_pct
FROM user_type
GROUP BY region, user_category
ORDER BY region, user_category;

-- ----------------------------------------
-- Q12: 用户平均购买间隔天数
-- 场景：预测用户下次购买时间
-- 难度：★★★☆☆
-- ----------------------------------------
WITH purchase_gaps AS (
    SELECT
        customer_id,
        order_date,
        LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order_date,
        DATEDIFF(
            order_date,
            LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)
        ) AS days_between
    FROM orders
    WHERE order_status != 'cancelled'
)
SELECT
    c.region,
    COUNT(DISTINCT pg.customer_id) AS customers_with_repurchase,
    ROUND(AVG(pg.days_between), 1) AS avg_days_between_orders,
    ROUND(STDDEV(pg.days_between), 1) AS stddev_days
FROM purchase_gaps pg
JOIN customers c ON pg.customer_id = c.customer_id
WHERE pg.days_between IS NOT NULL
GROUP BY c.region;
