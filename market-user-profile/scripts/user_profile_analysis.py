"""
出海市场用户画像对比分析：北美 vs 东南亚

分析维度：
1. 人口画像对比
2. 购买行为差异
3. 品类偏好
4. 渠道偏好
5. 购买决策因素
6. 用户级数据分布
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os
import warnings
warnings.filterwarnings("ignore")

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

NA_COLOR = "#3498db"
SEA_COLOR = "#e74c3c"
NA_LIGHT = "#d4e6f1"
SEA_LIGHT = "#fadbd8"

# ============================================================
# 1. 人口画像对比
# ============================================================
df_demo = pd.read_csv(os.path.join(OUTPUT_DIR, "demographics.csv"))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 1a. 年龄分布
na_demo = df_demo[df_demo["market"] == "North America"]
sea_demo = df_demo[df_demo["market"] == "Southeast Asia"]
age_groups = na_demo["age_group"].tolist()
x = np.arange(len(age_groups))
w = 0.35

axes[0].bar(x - w/2, na_demo["pct"], w, label="North America", color=NA_COLOR, alpha=0.85)
axes[0].bar(x + w/2, sea_demo["pct"], w, label="Southeast Asia", color=SEA_COLOR, alpha=0.85)
axes[0].set_xticks(x)
axes[0].set_xticklabels(age_groups)
axes[0].set_ylabel("Percentage (%)")
axes[0].set_title("Age Distribution of Beauty Consumers", fontweight="bold")
axes[0].legend()
axes[0].bar(x - w/2, na_demo["pct"], w, color=NA_COLOR, alpha=0.85)
axes[0].bar(x + w/2, sea_demo["pct"], w, color=SEA_COLOR, alpha=0.85)

# 1b. 各年龄段年均消费
axes[1].plot(age_groups, na_demo["avg_annual_spend_usd"], "o-", color=NA_COLOR,
             linewidth=2, markersize=8, label="North America")
axes[1].plot(age_groups, sea_demo["avg_annual_spend_usd"], "s-", color=SEA_COLOR,
             linewidth=2, markersize=8, label="Southeast Asia")
for i, (na_v, sea_v) in enumerate(zip(na_demo["avg_annual_spend_usd"], sea_demo["avg_annual_spend_usd"])):
    axes[1].annotate(f"${na_v}", (age_groups[i], na_v), textcoords="offset points",
                     xytext=(0, 10), fontsize=8, ha="center", color=NA_COLOR)
    axes[1].annotate(f"${sea_v}", (age_groups[i], sea_v), textcoords="offset points",
                     xytext=(0, -15), fontsize=8, ha="center", color=SEA_COLOR)
axes[1].set_ylabel("Annual Spend (USD)")
axes[1].set_title("Annual Beauty Spend by Age Group", fontweight="bold")
axes[1].legend()
axes[1].grid(axis="y", alpha=0.3)

plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "demographics.png"), dpi=150, bbox_inches="tight")
plt.close()
print("图表已保存: demographics.png")


# ============================================================
# 2. 购买行为雷达图
# ============================================================
df_behavior = pd.read_csv(os.path.join(OUTPUT_DIR, "purchase_behavior.csv"))

# Normalize for radar
metrics_radar = df_behavior["metric"].tolist()
na_vals = df_behavior["North America"].tolist()
sea_vals = df_behavior["Southeast Asia"].tolist()
max_vals = [max(a, b) * 1.1 for a, b in zip(na_vals, sea_vals)]
na_norm = [a / m for a, m in zip(na_vals, max_vals)]
sea_norm = [a / m for a, m in zip(sea_vals, max_vals)]

angles = np.linspace(0, 2 * np.pi, len(metrics_radar), endpoint=False).tolist()
angles += angles[:1]
na_norm += na_norm[:1]
sea_norm += sea_norm[:1]

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
ax.fill(angles, na_norm, alpha=0.25, color=NA_COLOR)
ax.plot(angles, na_norm, "o-", linewidth=2, color=NA_COLOR, label="North America")
ax.fill(angles, sea_norm, alpha=0.25, color=SEA_COLOR)
ax.plot(angles, sea_norm, "s-", linewidth=2, color=SEA_COLOR, label="Southeast Asia")

# Labels with actual values
labels = []
for m, na, sea in zip(metrics_radar, na_vals, sea_vals):
    short_m = m.replace(" (%)", "").replace(" (USD)", "")
    labels.append(f"{short_m}\n(NA: {na}, SEA: {sea})")
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontsize=7)
ax.set_ylim(0, 1)
ax.set_yticks([0.25, 0.5, 0.75])
ax.set_yticklabels(["25%", "50%", "75%"], fontsize=7)
ax.set_title("Purchase Behavior Comparison\n(Normalized Scale)", fontweight="bold", pad=30)
ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "behavior_radar.png"), dpi=150, bbox_inches="tight")
plt.close()
print("图表已保存: behavior_radar.png")


# ============================================================
# 3. 品类偏好对比
# ============================================================
df_cat = pd.read_csv(os.path.join(OUTPUT_DIR, "category_preference.csv"))

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(df_cat))
w = 0.35

ax.barh(x - w/2, df_cat["North America"], w, label="North America", color=NA_COLOR, alpha=0.85)
ax.barh(x + w/2, df_cat["Southeast Asia"], w, label="Southeast Asia", color=SEA_COLOR, alpha=0.85)
ax.set_yticks(x)
ax.set_yticklabels(df_cat["category"], fontsize=9)
ax.set_xlabel("Purchase Rate (%)")
ax.set_title("Category Preference: NA vs SEA", fontweight="bold")
ax.legend()
ax.invert_yaxis()

# Add value labels
for i, (na_v, sea_v) in enumerate(zip(df_cat["North America"], df_cat["Southeast Asia"])):
    ax.text(na_v + 0.5, i - 0.2, f"{na_v}%", fontsize=7, color=NA_COLOR)
    ax.text(sea_v + 0.5, i + 0.15, f"{sea_v}%", fontsize=7, color=SEA_COLOR)

plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "category_preference.png"), dpi=150, bbox_inches="tight")
plt.close()
print("图表已保存: category_preference.png")


# ============================================================
# 4. 渠道偏好对比
# ============================================================
df_channel = pd.read_csv(os.path.join(OUTPUT_DIR, "channel_preference.csv"))

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(df_channel))
w = 0.35

bars1 = ax.bar(x - w/2, df_channel["North America"], w, label="North America", color=NA_COLOR, alpha=0.85)
bars2 = ax.bar(x + w/2, df_channel["Southeast Asia"], w, label="Southeast Asia", color=SEA_COLOR, alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels(df_channel["channel"], rotation=45, ha="right", fontsize=9)
ax.set_ylabel("Usage Rate (%)")
ax.set_title("Channel Preference: Where Users Discover & Purchase", fontweight="bold")
ax.legend()

# Highlight key differences
for i, (na_v, sea_v) in enumerate(zip(df_channel["North America"], df_channel["Southeast Asia"])):
    diff = abs(na_v - sea_v)
    if diff >= 15:
        ax.annotate(f"Δ{diff:.0f}%", (i, max(na_v, sea_v) + 1),
                    fontsize=8, ha="center", fontweight="bold", color="#8e44ad")

plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "channel_preference.png"), dpi=150, bbox_inches="tight")
plt.close()
print("图表已保存: channel_preference.png")


# ============================================================
# 5. 用户级数据分布
# ============================================================
df_users = pd.read_csv(os.path.join(OUTPUT_DIR, "user_level_data.csv"))
na_users = df_users[df_users["market"] == "North America"]
sea_users = df_users[df_users["market"] == "Southeast Asia"]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 5a. 客单价分布
axes[0, 0].hist(na_users["aov_usd"], bins=30, alpha=0.6, color=NA_COLOR, label="North America", density=True)
axes[0, 0].hist(sea_users["aov_usd"], bins=30, alpha=0.6, color=SEA_COLOR, label="Southeast Asia", density=True)
axes[0, 0].axvline(na_users["aov_usd"].mean(), color=NA_COLOR, linestyle="--", linewidth=2)
axes[0, 0].axvline(sea_users["aov_usd"].mean(), color=SEA_COLOR, linestyle="--", linewidth=2)
axes[0, 0].set_xlabel("Average Order Value (USD)")
axes[0, 0].set_ylabel("Density")
axes[0, 0].set_title(f"AOV Distribution\nNA Mean=${na_users['aov_usd'].mean():.1f} | SEA Mean=${sea_users['aov_usd'].mean():.1f}", fontweight="bold")
axes[0, 0].legend()

# 5b. 年消费总额分布
axes[0, 1].hist(na_users["annual_spend_usd"], bins=30, alpha=0.6, color=NA_COLOR, label="North America", density=True)
axes[0, 1].hist(sea_users["annual_spend_usd"], bins=30, alpha=0.6, color=SEA_COLOR, label="Southeast Asia", density=True)
axes[0, 1].axvline(na_users["annual_spend_usd"].mean(), color=NA_COLOR, linestyle="--", linewidth=2)
axes[0, 1].axvline(sea_users["annual_spend_usd"].mean(), color=SEA_COLOR, linestyle="--", linewidth=2)
axes[0, 1].set_xlabel("Annual Spend (USD)")
axes[0, 1].set_ylabel("Density")
axes[0, 1].set_title(f"Annual Spend Distribution\nNA Mean=${na_users['annual_spend_usd'].mean():.0f} | SEA Mean=${sea_users['annual_spend_usd'].mean():.0f}", fontweight="bold")
axes[0, 1].legend()

# 5c. 年龄分布
axes[1, 0].hist(na_users["age"], bins=20, alpha=0.6, color=NA_COLOR, label="North America", density=True)
axes[1, 0].hist(sea_users["age"], bins=20, alpha=0.6, color=SEA_COLOR, label="Southeast Asia", density=True)
axes[1, 0].axvline(na_users["age"].mean(), color=NA_COLOR, linestyle="--", linewidth=2)
axes[1, 0].axvline(sea_users["age"].mean(), color=SEA_COLOR, linestyle="--", linewidth=2)
axes[1, 0].set_xlabel("Age")
axes[1, 0].set_ylabel("Density")
axes[1, 0].set_title(f"Age Distribution\nNA Mean={na_users['age'].mean():.0f} | SEA Mean={sea_users['age'].mean():.0f}", fontweight="bold")
axes[1, 0].legend()

# 5d. 年龄 vs 年消费
axes[1, 1].scatter(na_users["age"], na_users["annual_spend_usd"],
                   alpha=0.4, s=15, color=NA_COLOR, label="North America")
axes[1, 1].scatter(sea_users["age"], sea_users["annual_spend_usd"],
                   alpha=0.4, s=15, color=SEA_COLOR, label="Southeast Asia")

# Trend lines
for df_m, color, label in [(na_users, NA_COLOR, "NA"), (sea_users, SEA_COLOR, "SEA")]:
    z = np.polyfit(df_m["age"], df_m["annual_spend_usd"], 1)
    p = np.poly1d(z)
    ages_sorted = np.sort(df_m["age"].unique())
    axes[1, 1].plot(ages_sorted, p(ages_sorted), color=color, linewidth=2, label=f"{label} Trend")

axes[1, 1].set_xlabel("Age")
axes[1, 1].set_ylabel("Annual Spend (USD)")
axes[1, 1].set_title("Age vs Annual Spend by Market", fontweight="bold")
axes[1, 1].legend()

plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "user_distribution.png"), dpi=150, bbox_inches="tight")
plt.close()
print("图表已保存: user_distribution.png")


# ============================================================
# 6. 关键差异总结
# ============================================================
print("\n" + "=" * 60)
print("关键发现")
print("=" * 60)

print("\n【人口画像】")
print(f"  北美平均年龄: {na_users['age'].mean():.0f} 岁")
print(f"  东南亚平均年龄: {sea_users['age'].mean():.0f} 岁")
print(f"  差异: 东南亚用户年轻 {na_users['age'].mean() - sea_users['age'].mean():.0f} 岁")

print("\n【消费能力】")
print(f"  北美平均客单价: ${na_users['aov_usd'].mean():.1f}")
print(f"  东南亚平均客单价: ${sea_users['aov_usd'].mean():.1f}")
print(f"  北美年均消费: ${na_users['annual_spend_usd'].mean():.0f}")
print(f"  东南亚年均消费: ${sea_users['annual_spend_usd'].mean():.0f}")

print("\n【购买频次】")
print(f"  北美年均频次: {na_users['annual_frequency'].mean():.1f}")
print(f"  东南亚年均频次: {sea_users['annual_frequency'].mean():.1f}")

print("\n分析完成！")
print(f"所有图表保存在: {OUTPUT_DIR}")
