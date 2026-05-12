"""
DTC 品牌用户分群分析

基于 RFM 模型对用户进行分群，并针对每个群体
输出差异化的 EDM 营销策略建议。

使用方法：
    1. 先运行 generate_data.py 生成数据
    2. 再运行本脚本进行分析
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # 非交互式后端
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os
import sys

# ============================================================
# 配置
# ============================================================
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
DATA_PATH = os.path.join(OUTPUT_DIR, "ecommerce_data.csv")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# 1. 加载数据
# ============================================================
print("=" * 60)
print("DTC 品牌用户分群分析")
print("=" * 60)

df = pd.read_csv(DATA_PATH)
df["order_date"] = pd.to_datetime(df["order_date"])
print(f"\n数据加载: {len(df)} 笔订单, {df['user_id'].nunique()} 个用户")
print(f"时间范围: {df['order_date'].min().date()} ~ {df['order_date'].max().date()}")

# ============================================================
# 2. 计算 RFM
# ============================================================
REFERENCE_DATE = df["order_date"].max() + pd.Timedelta(days=1)

rfm = df.groupby("user_id").agg(
    recency=("order_date", lambda x: (REFERENCE_DATE - x.max()).days),
    frequency=("order_id", "nunique"),
    monetary=("order_amount", "sum"),
    last_purchase=("order_date", "max"),
    first_purchase=("order_date", "min"),
    avg_order_value=("order_amount", "mean"),
).reset_index()

print(f"\nRFM 描述统计:")
print(f"  Recency:  均值={rfm['recency'].mean():.0f}天, 中位数={rfm['recency'].median():.0f}天")
print(f"  Frequency: 均值={rfm['frequency'].mean():.1f}次, 中位数={rfm['frequency'].median():.0f}次")
print(f"  Monetary:  均值=${rfm['monetary'].mean():.0f}, 中位数=${rfm['monetary'].median():.0f}")

# ============================================================
# 3. RFM 评分（1-5）
# ============================================================
rfm["r_score"] = pd.cut(
    rfm["recency"],
    bins=[0, 30, 60, 120, 240, float("inf")],
    labels=[5, 4, 3, 2, 1],
).astype(int)

rfm["f_score"] = pd.cut(
    rfm["frequency"],
    bins=[0, 1, 2, 4, 7, float("inf")],
    labels=[1, 2, 3, 4, 5],
).astype(int)

rfm["m_score"] = pd.cut(
    rfm["monetary"],
    bins=[0, 50, 100, 200, 400, float("inf")],
    labels=[1, 2, 3, 4, 5],
).astype(int)

rfm["rfm_total"] = rfm["r_score"] + rfm["f_score"] + rfm["m_score"]
rfm["rfm_cell"] = (
    rfm["r_score"].astype(str) + rfm["f_score"].astype(str) + rfm["m_score"].astype(str)
)

# ============================================================
# 4. 用户分群
# ============================================================
def assign_segment(row):
    r, f, m = row["r_score"], row["f_score"], row["m_score"]
    if r >= 4 and f >= 4 and m >= 4:
        return "Champion"
    elif r <= 2 and f >= 4 and m >= 3:
        return "At Risk"
    elif r >= 4 and f <= 2 and m >= 2:
        return "New/Potential"
    elif r <= 2 and f >= 3 and m >= 3:
        return "Hibernating"
    elif r <= 2 and f <= 2 and m <= 2:
        return "Lost"
    elif f >= 4 and m <= 2:
        return "Price Sensitive"
    elif f <= 1 and m >= 3:
        return "Big Spender (Once)"
    else:
        return "Average"

rfm["segment"] = rfm.apply(assign_segment, axis=1)

# ============================================================
# 5. 分群汇总
# ============================================================
print("\n" + "=" * 60)
print("用户分群结果")
print("=" * 60)

seg_summary = (
    rfm.groupby("segment")
    .agg(
        user_count=("user_id", "nunique"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean"),
        total_revenue=("monetary", "sum"),
        avg_order_value=("avg_order_value", "mean"),
    )
    .round(1)
)

seg_summary["pct"] = (seg_summary["user_count"] / seg_summary["user_count"].sum() * 100).round(1)
seg_summary["revenue_pct"] = (seg_summary["total_revenue"] / seg_summary["total_revenue"].sum() * 100).round(1)
seg_summary = seg_summary.sort_values("user_count", ascending=False)

for idx, row in seg_summary.iterrows():
    print(f"\n  [{idx}]")
    print(f"    用户数: {int(row['user_count'])} ({row['pct']}%)")
    print(f"    收入贡献: ${row['total_revenue']:,.0f} ({row['revenue_pct']}%)")
    print(f"    平均最近购买: {row['avg_recency']:.0f} 天前")
    print(f"    平均购买次数: {row['avg_frequency']:.1f}")
    print(f"    平均客单价: ${row['avg_order_value']:.1f}")

# ============================================================
# 6. 可视化
# ============================================================

# Fig 1: 分群分布
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 6a. 用户数量饼图
seg_colors = {
    "Champion": "#2ecc71",
    "At Risk": "#e74c3c",
    "New/Potential": "#3498db",
    "Hibernating": "#f39c12",
    "Lost": "#95a5a6",
    "Price Sensitive": "#9b59b6",
    "Big Spender (Once)": "#1abc9c",
    "Average": "#bdc3c7",
}
colors_pie = [seg_colors.get(s, "#7f8c8d") for s in seg_summary.index]
wedges, texts, autotexts = axes[0].pie(
    seg_summary["user_count"],
    labels=seg_summary.index,
    autopct="%1.1f%%",
    colors=colors_pie,
    startangle=140,
)
for t in autotexts:
    t.set_fontsize(7)
for t in texts:
    t.set_fontsize(8)
axes[0].set_title("User Distribution by Segment", fontweight="bold")

# 6b. 收入贡献 vs 用户占比
x = np.arange(len(seg_summary))
width = 0.35
bars1 = axes[1].bar(x - width/2, seg_summary["pct"], width, label="User %", color="#3498db")
bars2 = axes[1].bar(x + width/2, seg_summary["revenue_pct"], width, label="Revenue %", color="#e74c3c")
axes[1].set_xticks(x)
axes[1].set_xticklabels(seg_summary.index, rotation=45, ha="right", fontsize=8)
axes[1].set_ylabel("Percentage (%)")
axes[1].set_title("User % vs Revenue % by Segment", fontweight="bold")
axes[1].legend(fontsize=8)
axes[1].axhline(y=0, color="black", linewidth=0.5)

# 6c. 平均客单价
avg_aov = seg_summary["avg_order_value"].sort_values(ascending=True)
bars3 = axes[2].barh(avg_aov.index, avg_aov.values, color=[seg_colors.get(s, "#7f8c8d") for s in avg_aov.index])
axes[2].set_xlabel("Avg Order Value ($)")
axes[2].set_title("Average Order Value by Segment", fontweight="bold")
for bar, val in zip(bars3, avg_aov.values):
    axes[2].text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, f"${val:.1f}", va="center", fontsize=8)

plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "segment_analysis.png"), dpi=150, bbox_inches="tight")
plt.close()
print(f"\n图表已保存: output/segment_analysis.png")

# Fig 2: RFM 散点矩阵
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

segment_order = ["Champion", "At Risk", "New/Potential", "Hibernating", "Price Sensitive", "Big Spender (Once)", "Average", "Lost"]
for ax, (x_col, y_col, xlabel, ylabel) in zip(
    axes,
    [("recency", "frequency", "Recency (days)", "Frequency"),
     ("recency", "monetary", "Recency (days)", "Monetary ($)"),
     ("frequency", "monetary", "Frequency", "Monetary ($)")],
):
    for seg in segment_order:
        subset = rfm[rfm["segment"] == seg]
        if len(subset) > 0:
            ax.scatter(
                subset[x_col], subset[y_col],
                c=seg_colors.get(seg, "#7f8c8d"),
                label=seg, alpha=0.6, s=20,
            )
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(fontsize=6, loc="upper right", ncol=4)

plt.suptitle("RFM Scatter Matrix by Segment", fontweight="bold", fontsize=14)
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "rfm_scatter.png"), dpi=150, bbox_inches="tight")
plt.close()
print("图表已保存: output/rfm_scatter.png")

# ============================================================
# 7. 保存分析结果
# ============================================================
seg_summary.to_csv(os.path.join(OUTPUT_DIR, "segment_summary.csv"))
rfm.to_csv(os.path.join(OUTPUT_DIR, "user_rfm_detail.csv"), index=False)

print("\n数据已保存: output/segment_summary.csv")
print("数据已保存: output/user_rfm_detail.csv")
print("\n分析完成！")
