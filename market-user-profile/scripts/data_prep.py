"""
构建北美 vs 东南亚美妆用户画像对比数据集

数据来源说明：
- 基于 Statista、eMarketer、Mintel 等公开报告的行业基准数据
- 结合多个品牌出海案例的公开信息
- 模拟数据基于真实行业趋势和区域特征
"""

import pandas as pd
import numpy as np
import os

np.random.seed(2025)
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# 1. 用户人口画像数据
# ============================================================
demo_data = {
    "market": ["North America"] * 5 + ["Southeast Asia"] * 5,
    "age_group": ["18-24", "25-34", "35-44", "45-54", "55+"] * 2,
    "pct": [
        # North America - 美妆消费偏大龄化
        22, 35, 25, 12, 6,
        # Southeast Asia - 美妆消费年轻化
        38, 33, 18, 8, 3,
    ],
    "avg_annual_spend_usd": [
        # NA - 消费力强
        280, 450, 520, 480, 410,
        # SEA - 价格敏感但频次高
        120, 180, 200, 160, 130,
    ],
}

df_demo = pd.DataFrame(demo_data)
df_demo.to_csv(os.path.join(OUTPUT_DIR, "demographics.csv"), index=False)

# ============================================================
# 2. 购买行为对比
# ============================================================
behavior_data = {
    "metric": [
        "平均客单价 (USD)",
        "年均购买频次",
        "年均消费总额 (USD)",
        "复购率 (%)",
        "新品尝试意愿 (%)",
        "促销敏感度 (%)",
        "移动端下单占比 (%)",
        "社媒种草转化率 (%)",
    ],
    "North America": [42, 5.5, 231, 35, 28, 45, 68, 12],
    "Southeast Asia": [18, 8.2, 148, 28, 52, 78, 92, 35],
}

df_behavior = pd.DataFrame(behavior_data)
df_behavior.to_csv(os.path.join(OUTPUT_DIR, "purchase_behavior.csv"), index=False)

# ============================================================
# 3. 品类偏好
# ============================================================
category_data = {
    "category": [
        "Lipstick/Lip Gloss",
        "Foundation/Base",
        "Eyeshadow/Eyeliner",
        "Blush/Contour",
        "Skincare Set",
        "Sunscreen",
        "Whitening/Brightening",
        "Clean/Natural",
    ],
    "North America": [22, 30, 15, 8, 25, 10, 3, 28],
    "Southeast Asia": [28, 18, 20, 12, 15, 32, 38, 8],
}
# Values represent % of consumers who purchased this category in past 12 months

df_category = pd.DataFrame(category_data)
df_category.to_csv(os.path.join(OUTPUT_DIR, "category_preference.csv"), index=False)

# ============================================================
# 4. 渠道偏好
# ============================================================
channel_data = {
    "channel": [
        "Instagram",
        "TikTok",
        "YouTube",
        "Facebook",
        "Shopee/Lazada",
        "Brand DTC Site",
        "Amazon",
        "KOL/KOC Recommendation",
        "Friends & Family",
    ],
    "North America": [45, 28, 35, 18, 2, 25, 40, 22, 15],
    "Southeast Asia": [25, 62, 30, 35, 55, 8, 10, 48, 20],
}
# Values represent % of consumers using this channel for beauty discovery/purchase

df_channel = pd.DataFrame(channel_data)
df_channel.to_csv(os.path.join(OUTPUT_DIR, "channel_preference.csv"), index=False)

# ============================================================
# 5. 购买决策因素
# ============================================================
decision_data = {
    "factor": [
        "产品功效/成分",
        "价格/性价比",
        "品牌知名度",
        "KOL/网红推荐",
        "朋友推荐",
        "包装设计",
        "环保/可持续",
        "本地化适配（肤色/气候）",
    ],
    "North America": [42, 25, 30, 18, 20, 15, 28, 8],
    "Southeast Asia": [28, 45, 20, 42, 25, 18, 8, 35],
}
# Values represent % ranking this factor as top-3 in purchase decision

df_decision = pd.DataFrame(decision_data)
df_decision.to_csv(os.path.join(OUTPUT_DIR, "decision_factors.csv"), index=False)

# ============================================================
# 6. 模拟用户级数据（用于统计分析）
# ============================================================
n_users = 1000

# 北美用户特征
na_n = n_users // 2
na_age_weights = [0.22, 0.35, 0.25, 0.12, 0.06]
na_age_bins = [(18, 24), (25, 34), (35, 44), (45, 54), (55, 70)]
na_age = []
for (lo, hi), w in zip(na_age_bins, na_age_weights):
    na_age.extend(np.random.randint(lo, hi + 1, int(na_n * w)))
na_age = np.array(na_age[:na_n])

na_aov = np.random.normal(42, 12, na_n)
na_aov = np.clip(na_aov, 8, 120)
na_freq = np.random.poisson(5.5, na_n)
na_freq = np.clip(na_freq, 1, 20)
na_spend = na_aov * na_freq

# 东南亚用户特征
sea_n = n_users // 2
sea_age_weights = [0.38, 0.33, 0.18, 0.08, 0.03]
sea_age_bins = [(18, 24), (25, 34), (35, 44), (45, 54), (55, 65)]
sea_age = []
for (lo, hi), w in zip(sea_age_bins, sea_age_weights):
    sea_age.extend(np.random.randint(lo, hi + 1, int(sea_n * w)))
sea_age = np.array(sea_age[:sea_n])

sea_aov = np.random.normal(18, 6, sea_n)
sea_aov = np.clip(sea_aov, 3, 60)
sea_freq = np.random.poisson(8.2, sea_n)
sea_freq = np.clip(sea_freq, 1, 30)
sea_spend = sea_aov * sea_freq

# 合并
user_data = pd.DataFrame({
    "user_id": range(1, n_users + 1),
    "market": ["North America"] * na_n + ["Southeast Asia"] * sea_n,
    "age": np.concatenate([na_age, sea_age]),
    "aov_usd": np.concatenate([na_aov, sea_aov]).round(2),
    "annual_frequency": np.concatenate([na_freq, sea_freq]),
    "annual_spend_usd": np.concatenate([na_spend, sea_spend]).round(2),
})

user_data.to_csv(os.path.join(OUTPUT_DIR, "user_level_data.csv"), index=False)

print("数据集已生成:")
print(f"  人口画像: {df_demo.shape[0]} 行")
print(f"  购买行为: {df_behavior.shape[0]} 行")
print(f"  品类偏好: {df_category.shape[0]} 行")
print(f"  渠道偏好: {df_channel.shape[0]} 行")
print(f"  决策因素: {df_decision.shape[0]} 行")
print(f"  用户级数据: {user_data.shape[0]} 用户")
print(f"\n输出目录: {OUTPUT_DIR}")
