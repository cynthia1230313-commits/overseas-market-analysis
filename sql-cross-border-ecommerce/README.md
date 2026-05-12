# SQL 作品集：跨境电商业务分析

> 模拟一个面向北美和东南亚市场的 DTC 品牌独立站数据库，覆盖 20+ 业务分析场景的 SQL 查询。

## 业务场景

```
一个中国美妆品牌出海，在北美和东南亚运营独立站。
数据库记录用户、订单、商品、库存、营销活动等核心数据。
```

## 数据库设计

| 表 | 说明 | 核心字段 |
|---|------|---------|
| `customers` | 用户信息 | 国家、注册时间、渠道来源 |
| `products` | 商品信息 | 品类、价格、成本 |
| `orders` | 订单主表 | 用户、金额、状态、时间 |
| `order_items` | 订单明细 | 商品、数量、单价 |
| `inventory` | 库存 | 商品、仓库、数量 |
| `marketing_campaigns` | 营销活动 | 类型、渠道、预算、ROI |

## 查询分类

| 文件 | 场景 | 查询数 |
|------|------|--------|
| `sql/03_order_analysis.sql` | 订单分析 | 6 题 |
| `sql/04_customer_analysis.sql` | 用户分析 | 6 题 |
| `sql/05_product_analysis.sql` | 商品分析 | 4 题 |
| `sql/06_marketing_operations.sql` | 营销与运营 | 5 题 |

## 技术栈

- **SQL 标准：** MySQL / PostgreSQL 兼容
- **难度覆盖：** 基础 → 进阶（窗口函数、CTE、子查询）

## 使用方法

```sql
-- 1. 创建表结构
source sql/01_schema.sql;

-- 2. 导入示例数据
source sql/02_seed_data.sql;

-- 3. 执行业务查询
source sql/03_order_analysis.sql;
```
