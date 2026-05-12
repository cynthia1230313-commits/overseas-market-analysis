"""
生成模拟的 DTC 美妆品牌独立站购买数据

模拟场景：
- 面向北美市场的 DTC 美妆品牌（类似 Joocyee）
- 时间跨度：2024年7月 - 2025年6月（12个月）
- ~500 个用户，~2000 笔订单
- 包含字段：用户ID、订单日期、订单金额、产品类别、国家、渠道
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

np.random.seed(42)

# ============================================================
# 配置
# ============================================================
N_CUSTOMERS = 500
START_DATE = datetime(2024, 7, 1)
END_DATE = datetime(2025, 6, 30)
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 产品类别（类似美妆品牌）
PRODUCT_CATEGORIES = ["Lipstick", "Eyeshadow", "Blush", "Foundation", "Mascara", "Skincare Set"]
CATEGORY_WEIGHTS = [0.25, 0.20, 0.15, 0.15, 0.10, 0.15]
CATEGORY_PRICE_RANGE = {
    "Lipstick": (12, 25),
    "Eyeshadow": (15, 35),
    "Blush": (14, 28),
    "Foundation": (20, 45),
    "Mascara": (10, 22),
    "Skincare Set": (30, 80),
}

# 渠道
CHANNELS = ["Organic Search", "Social Media", "Email", "KOL Referral", "Paid Ads"]
CHANNEL_WEIGHTS = [0.25, 0.30, 0.15, 0.15, 0.15]

# 国家（北美市场）
COUNTRIES = ["United States", "Canada", "Mexico"]
COUNTRY_WEIGHTS = [0.70, 0.20, 0.10]

# ============================================================
# 生成用户档案
# ============================================================

# 用户类型分布（模拟真实场景）
# A: 高价值忠实用户 10%
# B: 活跃用户 25%
# C: 普通用户 35%
# D: 流失风险用户 20%
# E: 一次性用户 10%
user_types = np.random.choice(
    ["A", "B", "C", "D", "E"],
    size=N_CUSTOMERS,
    p=[0.10, 0.25, 0.35, 0.20, 0.10]
)

# 根据用户类型生成购买频率和客单价参数
user_params = {}
for i, utype in enumerate(user_types):
    if utype == "A":
        freq_param = np.random.randint(8, 15)  # 8-14次
        avg_order = np.random.uniform(45, 90)
    elif utype == "B":
        freq_param = np.random.randint(4, 9)   # 4-8次
        avg_order = np.random.uniform(30, 65)
    elif utype == "C":
        freq_param = np.random.randint(2, 5)   # 2-4次
        avg_order = np.random.uniform(25, 50)
    elif utype == "D":
        freq_param = np.random.randint(1, 3)   # 1-2次
        avg_order = np.random.uniform(20, 40)
    else:  # E
        freq_param = 1
        avg_order = np.random.uniform(15, 35)
    user_params[i] = {"freq": freq_param, "avg_order": avg_order, "type": utype}

# ============================================================
# 生成订单数据
# ============================================================
orders = []
order_id = 1

for user_id in range(1, N_CUSTOMERS + 1):
    params = user_params[user_id - 1]
    n_orders = params["freq"]

    # 该用户首次购买日期（越忠实越早开始）
    if params["type"] in ["A", "B"]:
        first_purchase_days = np.random.randint(0, 90)
    elif params["type"] == "C":
        first_purchase_days = np.random.randint(30, 180)
    else:
        first_purchase_days = np.random.randint(90, 300)

    first_purchase = START_DATE + timedelta(days=first_purchase_days)

    for j in range(n_orders):
        # 购买日期：均匀分布在该用户的购买周期内
        if n_orders == 1:
            order_date = first_purchase
        else:
            max_days = (END_DATE - first_purchase).days
            max_days = max(max_days, 1)
            order_days = int(j / (n_orders - 1) * max_days) + np.random.randint(-10, 10)
            order_days = max(0, min(max_days, order_days))
            order_date = first_purchase + timedelta(days=order_days)

        # 如果订单日期超出范围则跳过
        if order_date > END_DATE or order_date < START_DATE:
            continue

        # 产品类别
        category = np.random.choice(PRODUCT_CATEGORIES, p=CATEGORY_WEIGHTS)
        price_range = CATEGORY_PRICE_RANGE[category]

        # 订单金额（基于用户平均客单价 + 类别价格）
        base_price = np.random.uniform(price_range[0], price_range[1])
        quantity = np.random.choice([1, 1, 1, 1, 2, 2, 3], p=[0.4, 0.2, 0.1, 0.05, 0.1, 0.1, 0.05])
        order_amount = round(base_price * quantity + np.random.normal(0, 5), 2)
        order_amount = max(order_amount, 5.0)  # 最小5美元

        # 渠道
        channel = np.random.choice(CHANNELS, p=CHANNEL_WEIGHTS)

        # 国家
        country = np.random.choice(COUNTRIES, p=COUNTRY_WEIGHTS)

        orders.append({
            "order_id": order_id,
            "user_id": user_id,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "order_amount": round(order_amount, 2),
            "product_category": category,
            "channel": channel,
            "country": country,
        })
        order_id += 1

# ============================================================
# 保存
# ============================================================
df = pd.DataFrame(orders)
df = df.sort_values(["user_id", "order_date"]).reset_index(drop=True)

output_path = os.path.join(OUTPUT_DIR, "ecommerce_data.csv")
df.to_csv(output_path, index=False)

print(f"数据已生成: {output_path}")
print(f"用户数: {df['user_id'].nunique()}")
print(f"订单数: {len(df)}")
print(f"日期范围: {df['order_date'].min()} ~ {df['order_date'].max()}")
print(f"\n各用户类型订单数:")
user_type_map = {i+1: user_params[i]["type"] for i in range(N_CUSTOMERS)}
df["user_type"] = df["user_id"].map(user_type_map)
print(df.groupby("user_type")["order_id"].count())
print(f"\n渠道分布:")
print(df["channel"].value_counts(normalize=True))
print(f"\n国家分布:")
print(df["country"].value_counts(normalize=True))
