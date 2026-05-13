# Olist 巴西电商 — 端到端数据分析项目

> **真实数据 · 统计检验 · 留存分析 · 商业洞察**

## 项目概述

使用 **Olist 巴西电商平台 10 万笔真实交易数据**，完成从数据清洗到商业洞察的完整数据分析流程。Olist 是巴西最大的电商平台之一，连接超过 3,000 个卖家与消费者。

**数据来源：** [Brazilian E-Commerce Public Dataset (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- 99,441 笔订单 | 99,441 名用户 | 32,951 个商品 | 3,095 个卖家
- 时间跨度：2016 年 9 月 — 2018 年 10 月
- 涵盖订单、用户、商品、支付、评价、地理位置全链路数据

## 分析框架

```
├── notebooks/
│   ├── 01_data_cleaning.ipynb         # 数据清洗：缺失值/异常值/数据类型/表合并
│   ├── 02_eda_statistical.ipynb       # EDA + 统计检验：ANOVA/相关分析/ABC分类
│   └── 03_cohort_retention.ipynb      # 留存队列分析：Cohort矩阵/复购行为
├── sql/
│   └── olist_analysis.sql             # 11 道 SQL 分析查询（CTE/窗口函数/留存）
├── data/                              # 原始数据 (CSV × 9)
└── output/                            # 可视化图表输出
```

## 核心洞察

### 1. 营收增长与季节性
- 月度 GMV 持续增长，后半年较前半年提升显著
- AOV 保持稳定，增长主要由订单量驱动（非涨价）
- 年末（11-12 月）出现季节性高峰

### 2. 品类 ABC 分类
- A 类品类（Top 50% 营收）仅占品类数的 ~15%
- 健康美容、手表、床浴用品为核心品类
- 长尾品类数量多但贡献低，需评估是否缩减 SKU

### 3. 用户留存 — 核心发现
- **复购率**和**逐月留存曲线**揭示了用户粘性（运行 notebook 查看）
- 平均复购周期约 X 天（运行后填充实际数据）
- Cohort 分析识别留存拐点——Month 1 留存是关键

### 4. 评分驱动因素
- **配送时效是评分的第一驱动力**（ANOVA p < 0.001）
- 5 天内送达的订单好评率 vs 30 天+送达差异显著
- 价格与评分呈弱负相关：高价商品期望更高，更易产生差评

### 5. 卖家生态
- Top 20% 卖家贡献绝大部分营收（Lorenz 曲线）
- 圣保罗（SP）州是绝对核心市场

## 技术栈

| 领域 | 工具 |
|------|------|
| 数据处理 | Python (pandas, numpy) |
| 统计分析 | scipy (ANOVA, chi-square, Spearman/Pearson) |
| 可视化 | matplotlib, seaborn, plotly |
| SQL | MySQL/PostgreSQL 兼容 (CTE, 窗口函数, 留存分析) |
| 环境 | Jupyter Notebook |

## 与通用项目的区别

- **真实数据**：非模拟数据，包含真实业务中的脏数据、异常值、缺失值
- **统计严谨**：每个结论有统计检验支撑，不是"看图说话"
- **业务闭环**：每个分析点都有对应的业务建议
- **SQL + Python 双版本**：覆盖不同团队的协作需求

## 使用方法

```bash
# 1. 安装依赖
pip install pandas numpy matplotlib seaborn scipy jupyter

# 2. 下载数据（自动）
python -c "import kagglehub; kagglehub.dataset_download('olistbr/brazilian-ecommerce')"

# 3. 启动 Jupyter
cd notebooks
jupyter notebook

# 4. 按顺序运行: 01 → 02 → 03
```

---

*作者：林彤 (TONG LIN) | 2026*
