-- ============================================================
-- 营销与运营分析（5 题）
-- 难度：进阶
-- ============================================================

-- ----------------------------------------
-- Q17: 营销活动 ROI 对比
-- 场景：评估各渠道投放效率
-- 难度：★★★☆☆
-- ----------------------------------------
SELECT
    mc.campaign_name,
    mc.campaign_type,
    mc.channel,
    mc.target_region,
    mc.budget,
    mc.actual_spend,
    mc.revenue_generated,
    ROUND(mc.revenue_generated - mc.actual_spend, 2) AS net_profit,
    ROUND((mc.revenue_generated - mc.actual_spend) / mc.actual_spend * 100, 1) AS roi_pct,
    mc.new_customers_acquired,
    ROUND(mc.actual_spend / mc.new_customers_acquired, 2) AS cac,
    ROUND(mc.revenue_generated / mc.new_customers_acquired, 2) AS revenue_per_new_customer
FROM marketing_campaigns mc
ORDER BY roi_pct DESC;

-- ----------------------------------------
-- Q18: 营销活动对客单价的提升效果
-- 场景：A/B 测试——活动期间 vs 非活动期间客单价对比
-- 难度：★★★★☆
-- ----------------------------------------
WITH campaign_orders AS (
    SELECT
        o.order_id,
        o.total_amount,
        o.customer_id,
        o.order_date,
        CASE WHEN o.campaign_id IS NOT NULL THEN 'Campaign' ELSE 'Organic' END AS order_type,
        c.region
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status != 'cancelled'
)
SELECT
    region,
    order_type,
    COUNT(DISTINCT order_id) AS order_count,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(AVG(total_amount), 2) AS avg_order_value,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM campaign_orders
GROUP BY region, order_type
ORDER BY region, order_type;

-- ----------------------------------------
-- Q19: 各渠道新用户的 30 天内复购率
-- 场景：衡量获客渠道的用户质量
-- 难度：★★★★☆
-- ----------------------------------------
WITH first_orders AS (
    SELECT
        c.customer_id,
        c.channel_source,
        c.region,
        MIN(o.order_date) AS first_order_date
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_status != 'cancelled'
    GROUP BY c.customer_id, c.channel_source, c.region
),
second_orders AS (
    SELECT DISTINCT fo.customer_id
    FROM first_orders fo
    JOIN orders o ON fo.customer_id = o.customer_id
    WHERE o.order_date > fo.first_order_date
      AND DATEDIFF(o.order_date, fo.first_order_date) <= 30
      AND o.order_status != 'cancelled'
)
SELECT
    fo.region,
    fo.channel_source,
    COUNT(DISTINCT fo.customer_id) AS new_customers,
    COUNT(DISTINCT so.customer_id) AS repurchased_within_30d,
    ROUND(
        COUNT(DISTINCT so.customer_id) * 100.0 / COUNT(DISTINCT fo.customer_id),
        1
    ) AS repurchase_rate_30d_pct
FROM first_orders fo
LEFT JOIN second_orders so ON fo.customer_id = so.customer_id
GROUP BY fo.region, fo.channel_source
ORDER BY fo.region, repurchase_rate_30d_pct DESC;

-- ----------------------------------------
-- Q20: 东南亚 vs 北美用户购买行为对比汇总
-- 场景：一篇查询看懂两市场差异
-- 难度：★★★☆☆
-- ----------------------------------------
SELECT
    c.region,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(COUNT(DISTINCT o.order_id) * 1.0 / COUNT(DISTINCT c.customer_id), 1) AS orders_per_customer,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value,
    ROUND(SUM(o.total_amount) / COUNT(DISTINCT c.customer_id), 2) AS revenue_per_customer,
    ROUND(AVG(o.discount_amount), 2) AS avg_discount_used,
    ROUND(SUM(CASE WHEN o.campaign_id IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS campaign_order_pct,
    -- 支付方式偏好
    (SELECT payment_method FROM orders o2
     JOIN customers c2 ON o2.customer_id = c2.customer_id
     WHERE c2.region = c.region AND o2.order_status != 'cancelled'
     GROUP BY payment_method ORDER BY COUNT(*) DESC LIMIT 1
    ) AS top_payment_method
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.order_status != 'cancelled'
GROUP BY c.region;

-- ----------------------------------------
-- Q21 (Bonus): 综合运营看板（CTE 组合查询）
-- 场景：一站式运营日报
-- 难度：★★★★★
-- ----------------------------------------
WITH daily_metrics AS (
    SELECT
        o.order_date,
        c.region,
        COUNT(DISTINCT o.order_id) AS orders,
        SUM(o.total_amount) AS revenue,
        COUNT(DISTINCT o.customer_id) AS active_customers
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status != 'cancelled'
    GROUP BY o.order_date, c.region
),
rolling_metrics AS (
    SELECT
        region,
        order_date,
        orders,
        revenue,
        active_customers,
        ROUND(AVG(revenue) OVER (PARTITION BY region ORDER BY order_date ROWS 6 PRECEDING), 2) AS revenue_7d_ma,
        ROUND(AVG(orders) OVER (PARTITION BY region ORDER BY order_date ROWS 6 PRECEDING), 0) AS orders_7d_ma,
        LAG(revenue, 7) OVER (PARTITION BY region ORDER BY order_date) AS revenue_7d_ago,
        ROUND(
            (revenue - LAG(revenue, 7) OVER (PARTITION BY region ORDER BY order_date))
            / NULLIF(LAG(revenue, 7) OVER (PARTITION BY region ORDER BY order_date), 0) * 100,
            1
        ) AS revenue_wow_pct
    FROM daily_metrics
)
SELECT *
FROM rolling_metrics
WHERE order_date >= '2024-03-01'
ORDER BY region, order_date DESC;
