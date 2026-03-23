# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data, filter_data, calculate_kpis
import config

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Dashboard", layout="wide")

st.title(config.APP_TITLE)
st.markdown("### Analyze sales performance & customer trends")

# -----------------------------
# Load Data
# -----------------------------
df = load_data(config.DATA_PATH)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

# Date filter
date_range = st.sidebar.date_input("Select Date Range", [])

# State filter
states = df['state'].unique()
selected_state = st.sidebar.selectbox("Select State", [None] + list(states))

# Segment filter
segments = df['segment'].unique()
selected_segment = st.sidebar.selectbox("Select Segment", [None] + list(segments))

# Apply filters
filtered_df = filter_data(df, selected_state, selected_segment)

if len(date_range) == 2:
    start, end = date_range
    filtered_df = filtered_df[
        (filtered_df['order_date'] >= pd.to_datetime(start)) &
        (filtered_df['order_date'] <= pd.to_datetime(end))
    ]

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2 = st.tabs(["📊 Overview", "📦 Detailed Analysis"])

# =============================
# 📊 TAB 1: OVERVIEW
# =============================
with tab1:

    # KPIs
    st.subheader("📌 Key Metrics")

    col1, col2, col3 = st.columns(3)

    total_revenue, total_orders, avg_order_value = calculate_kpis(filtered_df)

    col1.metric("Total Revenue", f"{total_revenue:,.0f}")
    col2.metric("Total Orders", total_orders)
    col3.metric("Avg Order Value", f"{avg_order_value:.2f}")

    # Revenue Trend (Plotly)
    st.subheader("📈 Revenue Trend")

    trend = filtered_df.groupby('order_date')['sales'].sum().reset_index()

    fig = px.line(trend, x='order_date', y='sales', title="Revenue Over Time")
    st.plotly_chart(fig, use_container_width=True)

    # Revenue by Segment
    st.subheader("📊 Revenue by Segment")

    seg = filtered_df.groupby('segment')['sales'].sum().reset_index()

    fig2 = px.bar(seg, x='segment', y='sales', title="Segment Performance")
    st.plotly_chart(fig2, use_container_width=True)

# =============================
# 📦 TAB 2: DETAILED ANALYSIS
# =============================
with tab2:

    st.subheader("📍 State-wise Performance")

    state_data = filtered_df.groupby('state')['sales'].sum().reset_index()

    fig3 = px.bar(state_data, x='state', y='sales', title="Revenue by State")
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("📅 Monthly Trends")

    monthly = filtered_df.groupby('month')['sales'].sum().reset_index()

    fig4 = px.line(monthly, x='month', y='sales', title="Monthly Trend")
    st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# Insights Section
# -----------------------------
st.subheader("💡 Key Insights")

if not filtered_df.empty:

    top_state = filtered_df.groupby('state')['sales'].sum().idxmax()
    top_segment = filtered_df.groupby('segment')['sales'].sum().idxmax()

    st.markdown(f"""
    - 🏆 **Top Performing State:** {top_state}  
    - 📦 **Top Segment:** {top_segment}  
    - 💰 **Total Revenue:** {total_revenue:,.0f}  
    """)

else:
    st.write("No data available for selected filters.")