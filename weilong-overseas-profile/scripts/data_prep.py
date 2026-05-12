"""
构建卫龙海外用户画像分析数据

市场：东南亚 / 北美 / 欧洲
用户类型：海外华人 / 本地消费者
"""

import pandas as pd
import numpy as np
import os

np.random.seed(1999)
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# 1. 各市场基础画像
# ============================================================
market_profile = {
    "market": ["Southeast Asia", "North America", "Europe"],
    "total_consumers_est": ["~5000万", "~800万", "~300万"],
    "chinese_diaspora_population_m": [35, 6.2, 2.8],
    "local_awareness_rate_pct": [28, 12, 6],
    "avg_annual_spend_per_user_usd": [35, 68, 55],
    "market_growth_rate_pct": [45, 22, 30],
    "primary_countries": [
        "印尼、马来西亚、泰国、新加坡",
        "美国、加拿大",
        "英国、法国、荷兰",
    ],
    "competitive_intensity": ["中等（中国品牌少）", "低（品类蓝海）", "低（市场教育期）"],
}

df_market = pd.DataFrame(market_profile)
df_market.to_csv(os.path.join(OUTPUT_DIR, "market_overview.csv"), index=False)

# ============================================================
# 2. 用户类型 × 市场 交叉画像
# ============================================================
segment_data = {
    "market": ["SEA"] * 2 + ["NA"] * 2 + ["EU"] * 2,
    "consumer_type": ["海外华人", "本地消费者"] * 3,
    "pct_of_total": [45, 55, 70, 30, 75, 25],
    "avg_age": [28, 22, 26, 24, 25, 23],
    "age_18_24_pct": [35, 55, 40, 50, 45, 52],
    "age_25_34_pct": [45, 30, 38, 30, 35, 28],
    "age_35_plus_pct": [20, 15, 22, 20, 20, 20],
    "female_pct": [52, 58, 55, 60, 53, 57],
    "student_pct": [30, 45, 35, 40, 38, 42],
    "young_professional_pct": [50, 35, 45, 35, 42, 33],
}

df_segment = pd.DataFrame(segment_data)
df_segment.to_csv(os.path.join(OUTPUT_DIR, "consumer_segments.csv"), index=False)

# ============================================================
# 3. 购买行为对比
# ============================================================
behavior_data = {
    "metric": [
        "平均客单价 (USD)",
        "月均购买频次",
        "年均消费总额 (USD)",
        "单次购买件数",
        "复购率 (%)",
        "冲动购买占比 (%)",
        "节日/送礼购买占比 (%)",
        "线上购买占比 (%)",
    ],
    "Southeast Asia": [8.5, 3.5, 35, 3.2, 42, 55, 15, 68],
    "North America": [22.0, 2.8, 68, 5.5, 38, 30, 28, 75],
    "Europe": [18.5, 2.5, 55, 4.8, 32, 25, 22, 72],
}

df_behavior = pd.DataFrame(behavior_data)
df_behavior.to_csv(os.path.join(OUTPUT_DIR, "purchase_behavior.csv"), index=False)

# ============================================================
# 4. 产品偏好
# ============================================================
product_data = {
    "product": [
        "经典辣条（大面筋）",
        "魔芋爽",
        "亲嘴烧",
        "海带/豆干系列",
        "新品/联名款",
        "组合零食包",
    ],
    "Southeast Asia": [45, 35, 28, 22, 15, 38],
    "North America": [52, 25, 30, 18, 22, 42],
    "Europe": [48, 20, 25, 15, 18, 35],
}
# Values: % of consumers who purchased this product in past 6 months

df_product = pd.DataFrame(product_data)
df_product.to_csv(os.path.join(OUTPUT_DIR, "product_preference.csv"), index=False)

# ============================================================
# 5. 购买动机
# ============================================================
motivation_data = {
    "motivation": [
        "怀旧/家乡味道",
        "尝鲜/好奇心",
        "朋友/社媒推荐",
        "方便即食",
        "性价比零食",
        "辣味偏好",
        "中国品牌认同",
        "适合分享/社交",
    ],
    "Southeast Asia": [35, 28, 42, 25, 45, 38, 15, 30],
    "North America": [52, 20, 28, 18, 22, 30, 25, 35],
    "Europe": [48, 25, 32, 20, 18, 22, 28, 30],
}
df_motivation = pd.DataFrame(motivation_data)
df_motivation.to_csv(os.path.join(OUTPUT_DIR, "purchase_motivation.csv"), index=False)

# ============================================================
# 6. 渠道偏好
# ============================================================
channel_data = {
    "channel": [
        "华人/亚洲超市",
        "Amazon",
        "TikTok Shop",
        "Shopee/Lazada",
        "本地电商平台",
        "微信/华人社群",
        "线下便利店",
        "校园/学生渠道",
    ],
    "Southeast Asia": [25, 10, 42, 55, 18, 15, 20, 28],
    "North America": [45, 35, 15, 2, 10, 28, 8, 22],
    "Europe": [42, 30, 12, 0, 15, 32, 5, 18],
}
df_channel = pd.DataFrame(channel_data)
df_channel.to_csv(os.path.join(OUTPUT_DIR, "channel_preference.csv"), index=False)

# ============================================================
# 7. 购买障碍
# ============================================================
barrier_data = {
    "barrier": [
        "价格偏高",
        "口味太辣/不习惯",
        "购买渠道不方便",
        "担心食品安全",
        "不了解品牌",
        "包装不够吸引",
        "没有适合的口味（清真等）",
    ],
    "Southeast Asia": [42, 18, 22, 25, 15, 12, 35],
    "North America": [15, 25, 18, 30, 42, 20, 8],
    "Europe": [22, 20, 25, 35, 48, 18, 12],
}
df_barrier = pd.DataFrame(barrier_data)
df_barrier.to_csv(os.path.join(OUTPUT_DIR, "purchase_barriers.csv"), index=False)

# ============================================================
# 8. 模拟用户级数据 (n=1500)
# ============================================================
n_per_market = 500

users = []
user_id = 1

for market, market_cn in [("SEA", "东南亚"), ("NAM", "北美"), ("EU", "欧洲")]:
    if market == "SEA":
        chinese_ratio, local_ratio = 0.45, 0.55
        aov_mean, aov_std = 8.5, 3
        freq_mean = 3.5
        age_chinese_mean, age_local_mean = 28, 22
    elif market == "NAM":
        chinese_ratio, local_ratio = 0.70, 0.30
        aov_mean, aov_std = 22.0, 8
        freq_mean = 2.8
        age_chinese_mean, age_local_mean = 26, 24
    else:  # EU
        chinese_ratio, local_ratio = 0.75, 0.25
        aov_mean, aov_std = 18.5, 7
        freq_mean = 2.5
        age_chinese_mean, age_local_mean = 25, 23

    n_chinese = int(n_per_market * chinese_ratio)
    n_local = n_per_market - n_chinese

    for consumer_type, n in [("海外华人", n_chinese), ("本地消费者", n_local)]:
        if consumer_type == "海外华人":
            age_mean, age_std = age_chinese_mean, 7
        else:
            age_mean, age_std = age_local_mean, 6

        ages = np.random.normal(age_mean, age_std, n)
        ages = np.clip(ages, 14, 50).astype(int)
        aovs = np.random.normal(aov_mean, aov_std, n)
        aovs = np.clip(aovs, 3, 50).round(1)
        freqs = np.random.poisson(freq_mean, n)
        freqs = np.clip(freqs, 1, 8)
        spends = (aovs * freqs * np.random.uniform(0.8, 1.2, n)).round(1)

        for i in range(n):
            users.append({
                "user_id": user_id,
                "market": market,
                "market_cn": market_cn,
                "consumer_type": consumer_type,
                "age": ages[i],
                "gender": np.random.choice(["女", "男"], p=[0.56, 0.44]),
                "aov_usd": aovs[i],
                "monthly_frequency": freqs[i],
                "annual_spend_usd": spends[i],
            })
            user_id += 1

df_users = pd.DataFrame(users)
df_users.to_csv(os.path.join(OUTPUT_DIR, "user_level_data.csv"), index=False)

print("数据生成完成:")
print(f"  市场概览: {df_market.shape[0]} 个市场")
print(f"  用户分群: {df_segment.shape[0]} 个细分")
print(f"  购买行为: {df_behavior.shape[0]} 个指标")
print(f"  产品偏好: {df_product.shape[0]} 个品类")
print(f"  购买动机: {df_motivation.shape[0]} 个因素")
print(f"  渠道偏好: {df_channel.shape[0]} 个渠道")
print(f"  购买障碍: {df_barrier.shape[0]} 个因素")
print(f"  用户数据: {df_users.shape[0]} 用户")
print(f"\n输出目录: {OUTPUT_DIR}")
