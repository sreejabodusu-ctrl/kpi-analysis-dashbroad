import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------------------------
# Generate Sample Sales Data
# -------------------------
np.random.seed(42)

n = 1000

dates = pd.date_range(start="2024-01-01", end="2024-12-31", periods=n)

products = ["Laptop", "Mobile", "Tablet", "Headphones", "Smart Watch"]
categories = ["Electronics", "Accessories"]
regions = ["North", "South", "East", "West"]

df = pd.DataFrame({
    "Order_ID": range(1001, 1001+n),
    "Order_Date": dates,
    "Product": np.random.choice(products, n),
    "Category": np.random.choice(categories, n),
    "Region": np.random.choice(regions, n),
    "Sales": np.random.randint(500, 50000, n),
    "Profit": np.random.randint(50, 10000, n)
})

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Sales KPI Dashboard",
    layout="wide"
)

st.title("📊 Sales KPI Dashboard")

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(selected_region)) &
    (df["Category"].isin(selected_category))
]

# -------------------------
# KPI Calculations
# -------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order_ID"].nunique()
avg_order_value = total_sales / total_orders
profit_margin = (total_profit / total_sales) * 100

# -------------------------
# KPI Cards
# -------------------------
st.subheader("Key Performance Indicators")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
c2.metric("📦 Orders", f"{total_orders:,}")
c3.metric("📈 Total Profit", f"₹{total_profit:,.0f}")
c4.metric("🛒 Avg Order Value", f"₹{avg_order_value:,.0f}")
c5.metric("📊 Profit Margin", f"{profit_margin:.2f}%")

st.markdown("---")

# -------------------------
# Monthly Sales Trend
# -------------------------
monthly_sales = (
    filtered_df
    .groupby(filtered_df["Order_Date"].dt.month)["Sales"]
    .sum()
    .reset_index()
)

monthly_sales.columns = ["Month", "Sales"]

fig1 = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------
# Category Sales
# -------------------------
col1, col2 = st.columns(2)

category_sales = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    title="Sales by Category"
)

col1.plotly_chart(fig2, use_container_width=True)

# -------------------------
# Regional Sales
# -------------------------
region_sales = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig3 = px.pie(
    region_sales,
    names="Region",
    values="Sales",
    title="Regional Sales Distribution"
)

col2.plotly_chart(fig3, use_container_width=True)

# -------------------------
# Top Products
# -------------------------
top_products = (
    filtered_df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig4 = px.bar(
    top_products,
    x="Product",
    y="Sales",
    color="Sales",
    title="Top Products by Sales"
)

st.plotly_chart(fig4, use_container_width=True)

# -------------------------
# Profit by Region
# -------------------------
profit_region = (
    filtered_df.groupby("Region")["Profit"]
    .sum()
    .reset_index()
)

fig5 = px.bar(
    profit_region,
    x="Region",
    y="Profit",
    title="Profit by Region",
    text_auto=True
)

st.plotly_chart(fig5, use_container_width=True)

# -------------------------
# Detailed Dataset
# -------------------------
st.subheader("Sales Dataset")

st.dataframe(filtered_df)

# -------------------------
# Download Dataset
# -------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Data",
    data=csv,
    file_name="sales_data.csv",
    mime="text/csv"
)