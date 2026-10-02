import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS (Premium Modern Slate Theme)
# =========================================================

st.markdown("""
<style>
    /* Main Background - Slate 900 */
    .stApp {
        background-color: #0F172A;
    }

    /* Sidebar Background - Slate 800 */
    section[data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155;
    }

    /* Text Colors globally for Streamlit elements */
    .stMarkdown, .stText, label {
        color: #F8FAFC !important;
    }

    /* Main title */
    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0px;
    }

    .main-title span {
        color: #3B82F6; /* Electric Blue Accent */
    }

    .subtitle {
        color: #94A3B8;
        font-size: 15px;
        margin-top: 3px;
    }

    /* KPI Cards */
    .kpi-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 22px;
        height: 145px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        transition: transform 0.2s ease-in-out;
    }

    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: #3B82F6;
    }

    .kpi-title {
        color: #94A3B8;
        font-size: 15px;
        margin-bottom: 10px;
        font-weight: 600;
    }

    .kpi-value {
        color: #F8FAFC;
        font-size: 30px;
        font-weight: 700;
    }

    .kpi-subtitle {
        color: #10B981; /* Emerald Green for positive indicators */
        font-size: 13px;
        margin-top: 8px;
        font-weight: 500;
    }

    /* Hide Streamlit menu */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    data = pd.read_csv("orders.csv")
    data["order_date"] = pd.to_datetime(data["order_date"])
    data["Year"] = data["order_date"].dt.year
    data["Month"] = data["order_date"].dt.month
    data["Month_Name"] = data["order_date"].dt.strftime("%b")
    data["Year_Month"] = data["order_date"].dt.to_period("M").astype(str)
    return data


df = load_data()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## 📊 Sales Dashboard")
st.sidebar.markdown("---")

st.sidebar.markdown("### 📅 Date Range")
min_date = df["order_date"].min()
max_date = df["order_date"].max()
date_range = st.sidebar.date_input("Select Date", value=(min_date, max_date), min_value=min_date, max_value=max_date)

st.sidebar.markdown("### 🚚 Ship Mode")
ship_modes = sorted(df["ship_mode"].dropna().unique())
selected_ship_modes = st.sidebar.multiselect("Ship Mode", ship_modes, default=ship_modes)

st.sidebar.markdown("### 👤 Customer")
customers = sorted(df["customer_id"].dropna().unique())
selected_customers = st.sidebar.multiselect("Customer", customers, default=[])

# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()

if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
    filtered_df = filtered_df[(filtered_df["order_date"] >= start_date) & (filtered_df["order_date"] <= end_date)]

if selected_ship_modes:
    filtered_df = filtered_df[filtered_df["ship_mode"].isin(selected_ship_modes)]
else:
    filtered_df = filtered_df.iloc[0:0]

if selected_customers:
    filtered_df = filtered_df[filtered_df["customer_id"].isin(selected_customers)]

# =========================================================
# HEADER
# =========================================================

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<div class="main-title">Sales <span>Dashboard</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Track performance • Discover insights • Drive growth</div>',
                unsafe_allow_html=True)

with col2:
    st.markdown(
        """
        <div style="text-align:right; color:#94A3B8; font-size:14px; padding-top:15px;">
        Better Data,<br>
        <b style="color:#F8FAFC;">Better Decisions</b>
        </div>
        """, unsafe_allow_html=True
    )

st.markdown("---")

# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = filtered_df["sales"].sum()
total_orders = filtered_df["id"].nunique() if "id" in filtered_df.columns else len(filtered_df)
total_customers = filtered_df["customer_id"].nunique()
average_order_value = total_sales / total_orders if total_orders > 0 else 0

# =========================================================
# KPI CARDS
# =========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-title">💰 Total Sales</div><div class="kpi-value">${total_sales:,.0f}</div><div class="kpi-subtitle">↗ Sales Revenue</div></div>',
        unsafe_allow_html=True)
with c2:
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-title">🛒 Total Orders</div><div class="kpi-value">{total_orders:,}</div><div class="kpi-subtitle">↗ Orders</div></div>',
        unsafe_allow_html=True)
with c3:
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-title">👥 Customers</div><div class="kpi-value">{total_customers:,}</div><div class="kpi-subtitle">Active Customers</div></div>',
        unsafe_allow_html=True)
with c4:
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-title">💵 Average Order Value</div><div class="kpi-value">${average_order_value:,.0f}</div><div class="kpi-subtitle">Average Sales / Order</div></div>',
        unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# CHART LAYOUT SETTINGS (Reusable for Premium Dark Theme)
# =========================================================
chart_layout = dict(
    paper_bgcolor="#0F172A",
    plot_bgcolor="#0F172A",
    font_color="#94A3B8",
    title_font=dict(color="#F8FAFC", size=18)
)
grid_style = dict(showgrid=True, gridcolor='#1E293B', zerolinecolor='#1E293B')

# =========================================================
# SALES TREND
# =========================================================
monthly_sales = filtered_df.groupby("Year_Month", as_index=False).agg(Sales=("sales", "sum"))

fig_trend = px.line(monthly_sales, x="Year_Month", y="Sales", markers=True)
fig_trend.update_traces(line=dict(color="#3B82F6", width=3),
                        marker=dict(size=8, color="#F8FAFC", line=dict(width=2, color="#3B82F6")))
fig_trend.update_layout(**chart_layout, title="📈 Sales Trend", xaxis_title="", yaxis_title="Sales",
                        hovermode="x unified", yaxis=grid_style)
st.plotly_chart(fig_trend, use_container_width=True)

# =========================================================
# TWO CHARTS ROW
# =========================================================
col1, col2 = st.columns(2)

# SALES BY SHIP MODE
with col1:
    ship_sales = filtered_df.groupby("ship_mode", as_index=False).agg(Sales=("sales", "sum")).sort_values("Sales",
                                                                                                          ascending=False)
    fig_ship = px.bar(ship_sales, x="ship_mode", y="Sales", title="🚚 Sales by Ship Mode", text_auto='.2s')
    fig_ship.update_traces(marker_color="#3B82F6", marker_line_color="#2563EB", marker_line_width=1.5, opacity=0.9)
    fig_ship.update_layout(**chart_layout, xaxis_title="", yaxis_title="Sales", yaxis=grid_style)
    st.plotly_chart(fig_ship, use_container_width=True)

# SALES DISTRIBUTION
with col2:
    fig_pie = px.pie(ship_sales, names="ship_mode", values="Sales", hole=0.6, title="📊 Sales Distribution")
    fig_pie.update_traces(
        marker=dict(colors=["#3B82F6", "#60A5FA", "#93C5FD", "#DBEAFE"], line=dict(color='#0F172A', width=2)))
    fig_pie.update_layout(**chart_layout)
    st.plotly_chart(fig_pie, use_container_width=True)

# =========================================================
# SECOND ROW
# =========================================================
col1, col2 = st.columns(2)

# TOP CUSTOMERS
with col1:
    top_customers = filtered_df.groupby("customer_id", as_index=False).agg(Sales=("sales", "sum")).sort_values("Sales",
                                                                                                               ascending=False).head(
        10)
    fig_customers = px.bar(top_customers, x="Sales", y="customer_id", orientation="h", title="🏆 Top 10 Customers",
                           text_auto='.2s')
    fig_customers.update_traces(marker_color="#3B82F6", marker_line_color="#2563EB", marker_line_width=1.5, opacity=0.9)
    fig_customers.update_layout(**chart_layout, xaxis_title="Sales", yaxis_title="", xaxis=grid_style)
    fig_customers.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_customers, use_container_width=True)

# SALES BY YEAR
with col2:
    yearly_sales = filtered_df.groupby("Year", as_index=False).agg(Sales=("sales", "sum"))
    fig_year = px.bar(yearly_sales, x="Year", y="Sales", title="📅 Sales by Year", text_auto='.2s')
    fig_year.update_traces(marker_color="#10B981", marker_line_color="#059669", marker_line_width=1.5,
                           opacity=0.9)  # لون أخضر مميز للسنين
    fig_year.update_layout(**chart_layout, xaxis_title="Year", yaxis_title="Sales", yaxis=grid_style)
    st.plotly_chart(fig_year, use_container_width=True)

# =========================================================
# CUSTOMER ANALYSIS
# =========================================================
customer_analysis = filtered_df.groupby("customer_id").agg(Total_Sales=("sales", "sum"),
                                                           Orders=("id", "count")).reset_index()

fig_scatter = px.scatter(customer_analysis, x="Orders", y="Total_Sales", hover_name="customer_id", size="Total_Sales",
                         title="👥 Customer Sales vs Orders")
fig_scatter.update_traces(marker_color="#8B5CF6", marker_line_color="#F8FAFC", marker_line_width=0.5,
                          opacity=0.7)  # لون بنفسجي للـ Scatter
fig_scatter.update_layout(**chart_layout, xaxis_title="Number of Orders", yaxis_title="Total Sales", yaxis=grid_style,
                          xaxis=grid_style)
st.plotly_chart(fig_scatter, use_container_width=True)

# =========================================================
# DATA TABLE
# =========================================================
st.markdown("### 📋 Orders Data")

display_df = filtered_df[["id", "order_date", "ship_mode", "customer_id",
                          "sales"]].copy() if "id" in filtered_df.columns else filtered_df.copy()
display_df["sales"] = display_df["sales"].round(2)

st.dataframe(display_df, use_container_width=True, height=350)