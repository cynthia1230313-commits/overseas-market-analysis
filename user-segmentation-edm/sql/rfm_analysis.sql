-- ============================================================
-- DTC 美妆品牌用户 RFM 分群分析
-- ============================================================
-- 使用说明：将 ecommerce_data.csv 导入数据库后执行以下查询
-- 支持 MySQL / PostgreSQL / SQLite
-- ============================================================

-- ----------------------------------------
-- 1. 计算每个用户的 RFM 指标
-- ----------------------------------------

-- 设定参考日期为数据集的最后一天 + 1
-- 如果你的数据库支持变量，可以替换 '2025-07-01'

WITH rfm_raw AS (
    SELECT
        user_id,
        -- Recency: 距离参考日期的天数（越小越好）
        julianday('2025-07-01') - julianday(MAX(order_date)) AS recency_days,
        -- Frequency: 购买次数
        COUNT(DISTINCT order_id) AS frequency,
        -- Monetary: 总消费金额
        SUM(order_amount) AS monetary,
        -- 辅助字段
        MAX(order_date) AS last_purchase_date,
        MIN(order_date) AS first_purchase_date,
        AVG(order_amount) AS avg_order_value
    FROM orders
    GROUP BY user_id
),

-- ----------------------------------------
-- 2. RFM 评分（1-5 分制，5为最优）
-- ----------------------------------------

rfm_scored AS (
    SELECT
        *,
        -- Recency: 天数越少分数越高
        CASE
            WHEN recency_days <= 30 THEN 5
            WHEN recency_days <= 60 THEN 4
            WHEN recency_days <= 120 THEN 3
            WHEN recency_days <= 240 THEN 2
            ELSE 1
        END AS r_score,
        -- Frequency: 次数越多分数越高
        CASE
            WHEN frequency >= 8 THEN 5
            WHEN frequency >= 5 THEN 4
            WHEN frequency >= 3 THEN 3
            WHEN frequency >= 2 THEN 2
            ELSE 1
        END AS f_score,
        -- Monetary: 金额越高分数越高
        CASE
            WHEN monetary >= 400 THEN 5
            WHEN monetary >= 200 THEN 4
            WHEN monetary >= 100 THEN 3
            WHEN monetary >= 50 THEN 2
            ELSE 1
        END AS m_score
    FROM rfm_raw
),

-- ----------------------------------------
-- 3. 用户分群
-- ----------------------------------------

user_segments AS (
    SELECT
        *,
        r_score || f_score || m_score AS rfm_cell,
        (r_score + f_score + m_score) AS rfm_total,
        CASE
            -- 核心用户：高价值、高忠诚度
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champion'
            -- 忠实用户：购买频繁但近期不活跃
            WHEN r_score <= 2 AND f_score >= 4 AND m_score >= 3 THEN 'At Risk'
            -- 潜力用户：近期活跃但购买频次不高
            WHEN r_score >= 4 AND f_score <= 2 AND m_score >= 2 THEN 'New/Potential'
            -- 需要唤醒：曾经活跃但沉寂已久
            WHEN r_score <= 2 AND f_score >= 3 AND m_score >= 3 THEN 'Hibernating'
            -- 流失用户：长期不活跃
            WHEN r_score <= 2 AND f_score <= 2 AND m_score <= 2 THEN 'Lost'
            -- 价格敏感：频繁但低客单价
            WHEN f_score >= 4 AND m_score <= 2 THEN 'Price Sensitive'
            -- 一次性大单：低频高客单价
            WHEN f_score <= 1 AND m_score >= 3 THEN 'Big Spender (Once)'
            -- 其余归为普通用户
            ELSE 'Average'
        END AS segment
    FROM rfm_scored
)

-- ----------------------------------------
-- 4. 各分群汇总统计
-- ----------------------------------------

SELECT
    segment,
    COUNT(*) AS user_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS pct,
    ROUND(AVG(recency_days), 1) AS avg_recency_days,
    ROUND(AVG(frequency), 1) AS avg_frequency,
    ROUND(AVG(monetary), 2) AS avg_total_spend,
    ROUND(AVG(avg_order_value), 2) AS avg_order_value,
    ROUND(SUM(monetary), 2) AS total_revenue,
    ROUND(SUM(monetary) * 100.0 / SUM(SUM(monetary)) OVER(), 1) AS revenue_pct
FROM user_segments
GROUP BY segment
ORDER BY user_count DESC;


-- ----------------------------------------
-- 5. 用户明细查询（导出用）
-- ----------------------------------------

-- SELECT
--     user_id,
--     recency_days,
--     frequency,
--     monetary,
--     r_score, f_score, m_score,
--     rfm_cell,
--     segment
-- FROM user_segments
-- ORDER BY rfm_total DESC;
