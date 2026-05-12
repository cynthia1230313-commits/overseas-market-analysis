# DTC 品牌用户分群与 EDM 策略优化

> 基于 RFM 模型的用户分群分析，输出差异化 EDM 营销策略

## 项目背景

模拟一个面向北美市场的 DTC 美妆品牌独立站，基于一年内的用户购买行为数据，使用 RFM 模型进行用户分群，并针对不同群体设计差异化的 EDM 营销策略。

## 技术栈

- **Python** (pandas, matplotlib, seaborn) — 数据生成、清洗、可视化
- **SQL** — RFM 分群查询
- **RFM 模型** — Recency / Frequency / Monetary 三位分群

## 项目结构

```
├── README.md
├── scripts/
│   ├── generate_data.py      # 生成模拟电商数据
│   └── user_analysis.py      # 用户分群分析与可视化
├── sql/
│   └── rfm_analysis.sql      # RFM 分群 SQL 查询
└── output/
    └── (生成的图表和报告)
```

## 使用方法

```bash
# 1. 生成模拟数据
python scripts/generate_data.py

# 2. 运行分析
python scripts/user_analysis.py

# 3. SQL 分析（可选，导入数据库执行）
# sql/rfm_analysis.sql
```
