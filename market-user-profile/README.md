# 出海市场用户画像分析：北美 vs 东南亚

> 对比分析美妆品类在北美与东南亚两大市场的用户画像差异，为品牌出海提供数据驱动的市场策略。

## 项目背景

中国美妆品牌出海面临核心问题：同一个产品在不同市场，用户是谁？需求有何不同？本项目基于行业公开数据和市场研究报告，构建北美与东南亚两大市场的用户画像对比框架。

## 技术栈

- **Python** (pandas, matplotlib, seaborn) — 数据分析与可视化
- **公开数据源** — Statista、eMarketer、Google Trends、行业报告
- **对比框架** — 人口统计 · 购买行为 · 渠道偏好 · 消费心理

## 项目结构

```
├── README.md
├── scripts/
│   ├── data_prep.py              # 基于行业基准数据构建对比数据集
│   └── user_profile_analysis.py  # 用户画像对比分析与可视化
└── output/
    └── 出海市场用户画像分析报告.md
```

## 使用方法

```bash
# 1. 准备数据
python scripts/data_prep.py

# 2. 运行分析
python scripts/user_profile_analysis.py
```
