import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("Sales Dashboard")

# Database connection
conn = sqlite3.connect("sales.db")

# Create table and sample data (runs only once)
conn.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        product TEXT,
        region TEXT,
        sales_amount INTEGER,
        units INTEGER,
        sale_date TEXT
    )
""")

count = conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
if count == 0:
    sample_data = [
        ("Laptop", "North", 45000, 15, "2025-04-01"),
        ("Phone", "South", 32000, 40, "2025-04-02"),
        ("Tablet", "East", 28000, 25, "2025-04-03"),
        ("Monitor", "West", 15000, 30, "2025-04-04")
    ]
    conn.executemany("""
        INSERT INTO sales (product, region, sales_amount, units, sale_date)
        VALUES (?, ?, ?, ?, ?)
    """, sample_data)
    conn.commit()

# Load data
df = pd.read_sql_query("SELECT * FROM sales", conn)
conn.close()

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    regions = ["All"] + sorted(df["region"].unique().tolist())
    selected_region = st.selectbox("Filter by Region", regions)

# Filter data
if selected_region != "All":
    filtered = df[df["region"] == selected_region]
else:
    filtered = df

# Metrics (NOW UPDATE when you filter!)
with col2:
    st.metric("Total Sales", f"${filtered['sales_amount'].sum():,}")
with col3:
    st.metric("Total Units Sold", filtered["units"].sum())

# Charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Sales by Product")
    st.bar_chart(filtered.groupby("product")["sales_amount"].sum())

with col_chart2:
    st.subheader("Sales Distribution by Region")
    region_sales = df.groupby("region")["sales_amount"].sum()   # overall for comparison
    fig = px.pie(region_sales, values=region_sales.values, names=region_sales.index)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Detailed Sales Data")
st.dataframe(filtered, use_container_width=True)