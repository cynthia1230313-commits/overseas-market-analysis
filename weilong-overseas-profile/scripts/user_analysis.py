"""
卫龙海外用户画像对比分析
市场：东南亚 · 北美 · 欧洲
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings("ignore")

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

COLORS = {"Southeast Asia": "#e74c3c", "North America": "#3498db", "Europe": "#2ecc71"}
COLORS_CN = {"东南亚": "#e74c3c", "北美": "#3498db", "欧洲": "#2ecc71"}
MARKET_ORDER = ["Southeast Asia", "North America", "Europe"]
ANALYSIS_MARKETS = ["SEA", "NAM", "EU"]
MARKET_CN = {"Southeast Asia": "东南亚", "North America": "北美", "Europe": "欧洲", "SEA": "东南亚", "NAM": "北美", "EU": "欧洲"}

# ============================================================
# Fig 1: 用户类型构成 + 年龄分布
# ============================================================
df_seg = pd.read_csv(os.path.join(OUTPUT_DIR, "consumer_segments.csv"))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 1a. 华人 vs 本地消费者占比
markets_label = ["东南亚", "北美", "欧洲"]
chinese_pct = df_seg[df_seg["consumer_type"] == "海外华人"]["pct_of_total"].tolist()
local_pct = df_seg[df_seg["consumer_type"] == "本地消费者"]["pct_of_total"].tolist()
x = np.arange(len(markets_label))
w = 0.35

axes[0].bar(x - w/2, chinese_pct, w, label="海外华人", color="#e74c3c", alpha=0.85)
axes[0].bar(x + w/2, local_pct, w, label="本地消费者", color="#3498db", alpha=0.85)
for i, (c, l) in enumerate(zip(chinese_pct, local_pct)):
    axes[0].text(i - w/2, c + 1, f"{c}%", ha="center", fontsize=9, fontweight="bold")
    axes[0].text(i + w/2, l + 1, f"{l}%", ha="center", fontsize=9, fontweight="bold")
axes[0].set_xticks(x)
axes[0].set_xticklabels(markets_label, fontsize=11)
axes[0].set_ylabel("Percentage (%)")
axes[0].set_title("Consumer Composition: Chinese Diaspora vs Local", fontweight="bold")
axes[0].legend(fontsize=9)
axes[0].set_ylim(0, 90)

# 1b. 年龄分布
ages_labels = ["18-24", "25-34", "35+"]
sea_age = df_seg[df_seg["market"] == "SEA"][["age_18_24_pct", "age_25_34_pct", "age_35_plus_pct"]].mean().tolist()
na_age = df_seg[df_seg["market"] == "NA"][["age_18_24_pct", "age_25_34_pct", "age_35_plus_pct"]].mean().tolist()
eu_age = df_seg[df_seg["market"] == "EU"][["age_18_24_pct", "age_25_34_pct", "age_35_plus_pct"]].mean().tolist()

x2 = np.arange(len(ages_labels))
w2 = 0.25
axes[1].bar(x2 - w2, sea_age, w2, label="东南亚", color=COLORS["Southeast Asia"], alpha=0.85)
axes[1].bar(x2, na_age, w2, label="北美", color=COLORS["North America"], alpha=0.85)
axes[1].bar(x2 + w2, eu_age, w2, label="欧洲", color=COLORS["Europe"], alpha=0.85)
axes[1].set_xticks(x2)
axes[1].set_xticklabels(ages_labels, fontsize=11)
axes[1].set_ylabel("Percentage (%)")
axes[1].set_title("Age Distribution by Market", fontweight="bold")
axes[1].legend(fontsize=9)

plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "consumer_composition.png"), dpi=150, bbox_inches="tight")
plt.close()
print("图表已保存: consumer_composition.png")


# ============================================================
# Fig 2: 购买行为雷达图
# ============================================================
df_behavior = pd.read_csv(os.path.join(OUTPUT_DIR, "purchase_behavior.csv"))
metrics = df_behavior["metric"].tolist()
short_metrics = [m.replace(" (%)", "").replace(" (USD)", "") for m in metrics]

sea_vals = df_behavior["Southeast Asia"].tolist()
na_vals = df_behavior["North America"].tolist()
eu_vals = df_behavior["Europe"].tolist()

all_vals = sea_vals + na_vals + eu_vals
max_vals = [max(sea_vals[i], na_vals[i], eu_vals[i]) * 1.15 for i in range(len(metrics))]
sea_norm = [v / m for v, m in zip(sea_vals, max_vals)]
na_norm = [v / m for v, m in zip(na_vals, max_vals)]
eu_norm = [v / m for v, m in zip(eu_vals, max_vals)]

angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
angles += angles[:1]
sea_norm += sea_norm[:1]
na_norm += na_norm[:1]
eu_norm += eu_norm[:1]

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

for vals, color, label in [
    (sea_norm, COLORS["Southeast Asia"], "Southeast Asia"),
    (na_norm, COLORS["North America"], "North America"),
    (eu_norm, COLORS["Europe"], "Europe"),
]:
    ax.fill(angles, vals, alpha=0.1, color=color)
    ax.plot(angles, vals, "o-", linewidth=2, color=color, label=label, markersize=5)

labels_with_vals = []
for i, (m, sea, na, eu) in enumerate(zip(short_metrics, sea_vals, na_vals, eu_vals)):
    labels_with_vals.append(f"{m}\n(SEA:{sea} NA:{na} EU:{eu})")

ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels_with_vals, fontsize=7)
ax.set_ylim(0, 1)
ax.set_yticks([0.25, 0.5, 0.75])
ax.set_yticklabels(["25%", "50%", "75%"], fontsize=7)
ax.set_title("Purchase Behavior by Market (Normalized)", fontweight="bold", pad=30)
ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "behavior_radar.png"), dpi=150, bbox_inches="tight")
plt.close()
print("图表已保存: behavior_radar.png")


# ============================================================
# Fig 3: 购买动机对比
# ============================================================
df_mot = pd.read_csv(os.path.join(OUTPUT_DIR, "purchase_motivation.csv"))

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(df_mot))
w = 0.25

ax.bar(x - w, df_mot["Southeast Asia"], w, label="Southeast Asia", color=COLORS["Southeast Asia"], alpha=0.85)
ax.bar(x, df_mot["North America"], w, label="North America", color=COLORS["North America"], alpha=0.85)
ax.bar(x + w, df_mot["Europe"], w, label="Europe", color=COLORS["Europe"], alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels(df_mot["motivation"], rotation=45, ha="right", fontsize=9)
ax.set_ylabel("Percentage (%)")
ax.set_title("Purchase Motivation by Market", fontweight="bold")
ax.legend(fontsize=9)

plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "purchase_motivation.png"), dpi=150, bbox_inches="tight")
plt.close()
print("图表已保存: purchase_motivation.png")


# ============================================================
# Fig 4: 产品偏好 + 渠道偏好
# ============================================================
df_prod = pd.read_csv(os.path.join(OUTPUT_DIR, "product_preference.csv"))
df_chan = pd.read_csv(os.path.join(OUTPUT_DIR, "channel_preference.csv"))

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# 4a. 产品偏好
x = np.arange(len(df_prod))
w = 0.25
axes[0].bar(x - w, df_prod["Southeast Asia"], w, label="Southeast Asia", color=COLORS["Southeast Asia"], alpha=0.85)
axes[0].bar(x, df_prod["North America"], w, label="North America", color=COLORS["North America"], alpha=0.85)
axes[0].bar(x + w, df_prod["Europe"], w, label="Europe", color=COLORS["Europe"], alpha=0.85)
axes[0].set_xticks(x)
axes[0].set_xticklabels(df_prod["product"], rotation=45, ha="right", fontsize=8)
axes[0].set_ylabel("Purchase Rate (%)")
axes[0].set_title("Product Preference by Market", fontweight="bold")
axes[0].legend(fontsize=8)

# 4b. 渠道偏好 - horizontal bar
df_chan_melt = df_chan.melt(id_vars="channel", var_name="market", value_name="pct")
df_chan_melt["market"] = df_chan_melt["market"].replace({"Southeast Asia": "SEA", "North America": "NA", "Europe": "EU"})

channels = df_chan["channel"].tolist()
sea_c = df_chan["Southeast Asia"].tolist()
na_c = df_chan["North America"].tolist()
eu_c = df_chan["Europe"].tolist()

y = np.arange(len(channels))
w = 0.25
axes[1].barh(y - w, sea_c, w, label="SEA", color=COLORS["Southeast Asia"], alpha=0.85)
axes[1].barh(y, na_c, w, label="NA", color=COLORS["North America"], alpha=0.85)
axes[1].barh(y + w, eu_c, w, label="EU", color=COLORS["Europe"], alpha=0.85)
axes[1].set_yticks(y)
axes[1].set_yticklabels(channels, fontsize=9)
axes[1].set_xlabel("Usage Rate (%)")
axes[1].set_title("Channel Preference by Market", fontweight="bold")
axes[1].legend(fontsize=8)
axes[1].invert_yaxis()

plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "product_channel.png"), dpi=150, bbox_inches="tight")
plt.close()
print("图表已保存: product_channel.png")


# ============================================================
# Fig 5: 用户级数据分布
# ============================================================
df_users = pd.read_csv(os.path.join(OUTPUT_DIR, "user_level_data.csv"))

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

for ax_i, (market_label, market_en) in enumerate([
    ("东南亚", "SEA"), ("北美", "NAM"), ("欧洲", "EU")
]):
    subset = df_users[df_users["market"] == market_en]
    color = COLORS[MARKET_ORDER[ax_i]]

    # Age distribution by consumer type
    if ax_i == 0:
        for ctype, ccolor, alpha_val in [("海外华人", "#e74c3c", 0.6), ("本地消费者", "#3498db", 0.6)]:
            ss = subset[subset["consumer_type"] == ctype]
            axes[0, 0].hist(ss["age"], bins=20, alpha=alpha_val, color=ccolor, label=f"{market_label}-{ctype}", density=True)
    if ax_i == 1:
        for ctype, ccolor, alpha_val in [("海外华人", "#e74c3c", 0.6), ("本地消费者", "#3498db", 0.6)]:
            ss = subset[subset["consumer_type"] == ctype]
            axes[0, 1].hist(ss["age"], bins=20, alpha=alpha_val, color=ccolor, label=f"{market_label}-{ctype}", density=True)
    if ax_i == 2:
        for ctype, ccolor, alpha_val in [("海外华人", "#e74c3c", 0.6), ("本地消费者", "#3498db", 0.6)]:
            ss = subset[subset["consumer_type"] == ctype]
            axes[1, 0].hist(ss["age"], bins=20, alpha=alpha_val, color=ccolor, label=f"{market_label}-{ctype}", density=True)

# Annual spend boxplot
box_data = []
box_labels = []
for market_en in ["SEA", "NAM", "EU"]:
    market_cn = MARKET_CN[market_en]
    subset = df_users[df_users["market"] == market_en]
    box_data.append(subset[subset["consumer_type"] == "海外华人"]["annual_spend_usd"].tolist())
    box_labels.append(f"{market_cn}\n华人")
    box_data.append(subset[subset["consumer_type"] == "本地消费者"]["annual_spend_usd"].tolist())
    box_labels.append(f"{market_cn}\n本地")

bp = axes[1, 1].boxplot(box_data, labels=box_labels, patch_artist=True, showfliers=False)
colors_box = ["#e74c3c", "#3498db"] * 3
for patch, color in zip(bp["boxes"], colors_box):
    patch.set_facecolor(color)
    patch.set_alpha(0.5)
axes[1, 1].set_ylabel("Annual Spend (USD)")
axes[1, 1].set_title("Annual Spend by Market × Consumer Type", fontweight="bold")
axes[1, 1].tick_params(axis="x", labelsize=8)

axes[0, 0].set_title("SEA: Age Distribution by Consumer Type", fontweight="bold")
axes[0, 0].set_xlabel("Age")
axes[0, 0].legend(fontsize=7)
axes[0, 1].set_title("NA: Age Distribution by Consumer Type", fontweight="bold")
axes[0, 1].set_xlabel("Age")
axes[0, 1].legend(fontsize=7)
axes[1, 0].set_title("EU: Age Distribution by Consumer Type", fontweight="bold")
axes[1, 0].set_xlabel("Age")
axes[1, 0].legend(fontsize=7)

plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "user_distribution.png"), dpi=150, bbox_inches="tight")
plt.close()
print("图表已保存: user_distribution.png")


# ============================================================
# 6. 关键发现
# ============================================================
print("\n" + "=" * 60)
print("卫龙海外用户画像 - 关键发现")
print("=" * 60)

print("\n【用户结构】")
print(f"  东南亚: 华人 45% / 本地 55% — 本地消费者已超过华人")
print(f"  北美:   华人 70% / 本地 30% — 仍以华人为主")
print(f"  欧洲:   华人 75% / 本地 25% — 仍以华人为主")

print("\n【消费水平】")
for market_en in ["SEA", "NAM", "EU"]:
    market_cn = MARKET_CN[market_en]
    subset = df_users[df_users["market"] == market_en]
    chinese_spend = subset[subset["consumer_type"] == "海外华人"]["annual_spend_usd"].mean()
    local_spend = subset[subset["consumer_type"] == "本地消费者"]["annual_spend_usd"].mean()
    print(f"  {market_cn}: 华人年均 ${chinese_spend:.0f} | 本地年均 ${local_spend:.0f}")

print("\n分析完成！")
print(f"图表保存在: {OUTPUT_DIR}")
