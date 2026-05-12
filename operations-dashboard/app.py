"""
跨境电商运营看板 — Streamlit Dashboard
面向北美和东南亚市场的 DTC 美妆品牌

使用方法: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="DTC Brand Overseas Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 数据生成（模拟12个月的运营数据）
# ============================================================
@st.cache_data
def load_data():
    np.random.seed(42)

    # 月份列表
    months = pd.date_range("2024-07-01", "2025-06-30", freq="MS")

    # 北美数据
    na_revenue = [32000, 34000, 38000, 42000, 45000, 48000, 52000, 51000, 54000, 58000, 62000, 65000]
    na_revenue = [v + np.random.randint(-3000, 3000) for v in na_revenue]
    na_orders = [v // 42 for v in na_revenue]
    na_customers = [int(v * 0.6) for v in na_orders]

    # 东南亚数据
    sea_revenue = [15000, 18000, 22000, 26000, 30000, 35000, 38000, 42000, 45000, 48000, 52000, 55000]
    sea_revenue = [v + np.random.randint(-2000, 2000) for v in sea_revenue]
    sea_orders = [v // 18 for v in sea_revenue]
    sea_customers = [int(v * 0.55) for v in sea_orders]

    df = pd.DataFrame({
        "month": list(months) + list(months),
        "market": ["North America"] * 12 + ["Southeast Asia"] * 12,
        "revenue": na_revenue + sea_revenue,
        "orders": na_orders + sea_orders,
        "customers": na_customers + sea_customers,
    })
    df["aov"] = (df["revenue"] / df["orders"]).round(2)
    df["month_label"] = df["month"].dt.strftime("%Y-%m")

    # 用户分群数据
    segments = pd.DataFrame({
        "segment": ["Champion", "Average", "New/Potential", "Lost", "Big Spender", "Price Sensitive"],
        "NA_users": [119, 231, 85, 58, 6, 1],
        "NA_revenue": [40516, 24816, 6670, 1711, 886, 89],
        "SEA_users": [85, 200, 120, 80, 12, 3],
        "SEA_revenue": [18500, 15000, 5200, 1800, 1500, 120],
    })

    # 渠道数据
    channels = pd.DataFrame({
        "channel": ["Instagram", "TikTok", "Amazon", "Shopee/Lazada", "Asian Supermarket",
                     "KOL/KOC", "Email", "Organic Search"],
        "NA_usage": [45, 28, 40, 2, 45, 22, 15, 25],
        "SEA_usage": [25, 62, 10, 55, 25, 48, 8, 20],
    })

    # 产品数据
    products = pd.DataFrame({
        "product": ["Lipstick", "Foundation", "Eyeshadow", "Sunscreen", "Skincare Set",
                     "Whitening Cream", "Mascara", "Blush", "Cleanser"],
        "category": ["Color"] * 4 + ["Skincare"] * 5,
        "NA_sales": [320, 280, 180, 120, 200, 30, 150, 90, 160],
        "SEA_sales": [250, 150, 220, 350, 180, 380, 130, 120, 60],
        "margin_pct": [62, 58, 55, 50, 52, 55, 65, 58, 60],
    })

    return df, segments, channels, products


df, segments, channels, products = load_data()

# ============================================================
# 侧边栏：全局筛选器
# ============================================================
st.sidebar.title("📊 筛选器")

market_filter = st.sidebar.multiselect(
    "选择市场",
    options=["North America", "Southeast Asia"],
    default=["North America", "Southeast Asia"],
)

date_range = st.sidebar.date_input(
    "选择日期范围",
    value=(datetime(2024, 7, 1), datetime(2025, 6, 30)),
    min_value=datetime(2024, 7, 1),
    max_value=datetime(2025, 6, 30),
)

st.sidebar.markdown("---")
st.sidebar.caption("DTC Brand Overseas Operations Dashboard")
st.sidebar.caption("Author: TONG LIN")

# 应用筛选
filtered_df = df[df["market"].isin(market_filter)]

# ============================================================
# 页面标题
# ============================================================
st.title("🛍️ DTC 品牌出海运营看板")
st.caption("面向北美 & 东南亚市场 | 2024.07 — 2025.06")

# ============================================================
# Tab 1: 总览
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs(["📈 总览", "👥 用户分析", "📦 商品分析", "📢 营销渠道"])

# ---- TAB 1: 总览 ----
with tab1:
    # KPI 卡片
    total_revenue = filtered_df["revenue"].sum()
    total_orders = filtered_df["orders"].sum()
    total_customers = filtered_df["customers"].sum()
    avg_aov = total_revenue / total_orders if total_orders > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 总营收", f"${total_revenue:,.0f}", delta="+24.3% YoY")
    col2.metric("📦 总订单", f"{total_orders:,}", delta="+18.7% YoY")
    col3.metric("👥 活跃用户", f"{total_customers:,}", delta="+15.2% YoY")
    col4.metric("🛒 平均客单价", f"${avg_aov:.2f}")

    st.markdown("---")

    # 月度趋势
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("月度营收趋势")
        fig = px.line(
            filtered_df,
            x="month_label",
            y="revenue",
            color="market",
            markers=True,
            color_discrete_map={"North America": "#3498db", "Southeast Asia": "#e74c3c"},
        )
        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            hovermode="x unified",
        )
        fig.update_yaxes(title="Revenue (USD)")
        fig.update_xaxes(title="")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("市场占比")
        market_share = filtered_df.groupby("market")["revenue"].sum().reset_index()
        fig = px.pie(
            market_share,
            values="revenue",
            names="market",
            color="market",
            color_discrete_map={"North America": "#3498db", "Southeast Asia": "#e74c3c"},
            hole=0.4,
        )
        fig.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    # AOV 和订单数趋势
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("客单价 (AOV) 趋势")
        fig = px.bar(
            filtered_df,
            x="month_label",
            y="aov",
            color="market",
            barmode="group",
            color_discrete_map={"North America": "#3498db", "Southeast Asia": "#e74c3c"},
        )
        fig.update_layout(height=350, margin=dict(l=0, r=0, t=10, b=10))
        fig.update_yaxes(title="AOV (USD)")
        fig.update_xaxes(title="")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("月度订单量")
        fig = px.bar(
            filtered_df,
            x="month_label",
            y="orders",
            color="market",
            barmode="group",
            color_discrete_map={"North America": "#3498db", "Southeast Asia": "#e74c3c"},
        )
        fig.update_layout(height=350, margin=dict(l=0, r=0, t=10, b=10))
        fig.update_yaxes(title="Orders")
        fig.update_xaxes(title="")
        st.plotly_chart(fig, use_container_width=True)


# ---- TAB 2: 用户分析 ----
with tab2:
    st.subheader("用户分群 (RFM)")

    col1, col2 = st.columns(2)

    with col1:
        # 北美用户分群
        na_seg = segments[["segment", "NA_users", "NA_revenue"]].copy()
        na_seg.columns = ["segment", "users", "revenue"]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(name="Users", x=na_seg["segment"], y=na_seg["users"],
                   marker_color="#3498db", opacity=0.8),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(name="Revenue ($)", x=na_seg["segment"], y=na_seg["revenue"],
                       mode="lines+markers", marker=dict(size=10, color="#e74c3c"),
                       line=dict(width=2)),
            secondary_y=True,
        )
        fig.update_layout(title="North America — User Segments", height=400,
                          margin=dict(l=0, r=0, t=40, b=10))
        fig.update_yaxes(title="User Count", secondary_y=False)
        fig.update_yaxes(title="Revenue (USD)", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # 东南亚用户分群
        sea_seg = segments[["segment", "SEA_users", "SEA_revenue"]].copy()
        sea_seg.columns = ["segment", "users", "revenue"]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(name="Users", x=sea_seg["segment"], y=sea_seg["users"],
                   marker_color="#e74c3c", opacity=0.8),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(name="Revenue ($)", x=sea_seg["segment"], y=sea_seg["revenue"],
                       mode="lines+markers", marker=dict(size=10, color="#3498db"),
                       line=dict(width=2)),
            secondary_y=True,
        )
        fig.update_layout(title="Southeast Asia — User Segments", height=400,
                          margin=dict(l=0, r=0, t=40, b=10))
        fig.update_yaxes(title="User Count", secondary_y=False)
        fig.update_yaxes(title="Revenue (USD)", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    # 用户增长趋势
    st.subheader("月度活跃用户趋势")
    fig = px.area(
        filtered_df,
        x="month_label",
        y="customers",
        color="market",
        color_discrete_map={"North America": "#3498db", "Southeast Asia": "#e74c3c"},
        line_shape="spline",
    )
    fig.update_layout(height=350, margin=dict(l=0, r=0, t=10, b=10),
                      hovermode="x unified")
    fig.update_yaxes(title="Active Customers")
    fig.update_xaxes(title="")
    st.plotly_chart(fig, use_container_width=True)


# ---- TAB 3: 商品分析 ----
with tab3:
    st.subheader("各市场商品销量对比")

    market_tab = st.radio("选择市场", ["North America", "Southeast Asia", "对比"], horizontal=True)

    if market_tab == "对比":
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                products, x="product", y="NA_sales", color="category",
                title="North America — Product Sales",
                color_discrete_map={"Color": "#3498db", "Skincare": "#2ecc71"},
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(
                products, x="product", y="SEA_sales", color="category",
                title="Southeast Asia — Product Sales",
                color_discrete_map={"Color": "#e74c3c", "Skincare": "#f39c12"},
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    elif market_tab == "North America":
        fig = px.bar(
            products, x="product", y="NA_sales", color="category",
            title="North America — Product Sales",
            color_discrete_map={"Color": "#3498db", "Skincare": "#2ecc71"},
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = px.bar(
            products, x="product", y="SEA_sales", color="category",
            title="Southeast Asia — Product Sales",
            color_discrete_map={"Color": "#e74c3c", "Skincare": "#f39c12"},
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # 毛利率气泡图
    st.subheader("商品毛利率 × 销量 矩阵")
    fig = px.scatter(
        products,
        x="NA_sales",
        y="SEA_sales",
        size="margin_pct",
        color="category",
        text="product",
        size_max=30,
        color_discrete_map={"Color": "#9b59b6", "Skincare": "#1abc9c"},
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(height=450, margin=dict(l=0, r=0, t=10, b=10))
    fig.update_xaxes(title="North America Sales")
    fig.update_yaxes(title="Southeast Asia Sales")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("气泡大小 = 毛利率")


# ---- TAB 4: 营销渠道 ----
with tab4:
    st.subheader("渠道偏好对比")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=channels["channel"],
        x=channels["NA_usage"],
        name="North America",
        orientation="h",
        marker_color="#3498db",
        opacity=0.8,
    ))
    fig.add_trace(go.Bar(
        y=channels["channel"],
        x=channels["SEA_usage"],
        name="Southeast Asia",
        orientation="h",
        marker_color="#e74c3c",
        opacity=0.8,
    ))
    fig.update_layout(
        barmode="group",
        height=400,
        margin=dict(l=0, r=0, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    fig.update_xaxes(title="Usage Rate (%)")
    fig.update_yaxes(title="")
    st.plotly_chart(fig, use_container_width=True)

    # 渠道效率
    st.subheader("各渠道转化效率")
    efficiency = pd.DataFrame({
        "channel": ["KOL/KOC", "TikTok", "Instagram", "Email", "Shopee/Lazada", "Amazon", "Organic"],
        "conversion_rate": [3.5, 2.8, 2.2, 4.5, 3.2, 5.0, 1.8],
        "cac": [12, 8, 15, 6, 5, 10, 18],
    })

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            efficiency, x="channel", y="conversion_rate",
            title="Conversion Rate by Channel (%)",
            color="conversion_rate",
            color_continuous_scale="blues",
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(
            efficiency, x="channel", y="cac",
            title="Customer Acquisition Cost by Channel ($)",
            color="cac",
            color_continuous_scale="reds",
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 页脚
# ============================================================
st.markdown("---")
st.caption("Built with Streamlit & Plotly | Data simulated based on real market benchmarks | Author: TONG LIN")
