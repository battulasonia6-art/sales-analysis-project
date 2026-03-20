import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from streamlit_lottie import st_lottie
import time

st.set_page_config(page_title="AI Dashboard", layout="wide")

df = pd.read_csv("cleaned_data.csv")

def load_lottie(url):
    return requests.get(url).json()

lottie = load_lottie("https://assets10.lottiefiles.com/packages/lf20_qp1q7mct.json")

# -------------------------
# CSS (ONLY insight color changed)
# -------------------------
st.markdown("""
<style>

.block-container {
    padding-top: 0rem !important;
}

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #1e293b) !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

header {visibility: hidden;}

h1, h2, h3, h4, p, label {
    color: white !important;
}

span[data-baseweb="tag"] {
    background-color: #2563eb !important;
    color: white !important;
}

.glass {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
    border-radius: 16px;
    padding: 18px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 6px 20px rgba(0,0,0,0.5);
    transition: 0.3s;
}
.glass:hover {
    transform: translateY(-6px);
}

.kpi-title {color:#cbd5e1;}
.kpi-value {
    font-size: 28px;
    font-weight: bold;
    color: white;
}

/* NEW INSIGHT COLOR (NOT BLUE) */
.insight {
    background: linear-gradient(135deg, #14532d, #22c55e);
    padding: 25px;
    border-radius: 18px;
    color: white;
    box-shadow: 0 10px 30px rgba(0,0,0,0.6);
}

.center-btn {
    display: flex;
    justify-content: center;
    margin-top: 30px;
}

.stDownloadButton button {
    background-color: #22c55e !important;
    color: white !important;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("🔍 Filters")

city = st.sidebar.multiselect("City", df["City"].unique(), default=df["City"].unique())
product = st.sidebar.multiselect("Product Line", df["Product line"].unique(), default=df["Product line"].unique())

filtered_df = df[(df["City"].isin(city)) & (df["Product line"].isin(product))]

# -------------------------
# HEADER
# -------------------------
col1, col2 = st.columns([4,1])

with col1:
    st.markdown("<h1>✨ AI-Powered Sales Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h4>Smart Insights for Business Growth</h4>", unsafe_allow_html=True)

with col2:
    st_lottie(lottie, height=140)

with st.spinner("Loading..."):
    time.sleep(1)

# -------------------------
# KPIs
# -------------------------
total_revenue = filtered_df["Revenue"].sum()
orders = filtered_df.shape[0]
rating = filtered_df["Rating"].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'<div class="glass"><div class="kpi-title">💰 Total Revenue</div><div class="kpi-value">₹ {total_revenue:,.0f}</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="glass"><div class="kpi-title">🧾 Total Orders</div><div class="kpi-value">{orders}</div></div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div class="glass"><div class="kpi-title">⭐ Avg Rating</div><div class="kpi-value">{rating:.2f}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------
# HEADINGS INSIDE EMPTY BARS (FIXED)
# -------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="glass"><h3>🏆 Top Products</h3></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass"><h3>📈 Sales Trend</h3></div>', unsafe_allow_html=True)

# -------------------------
# CHARTS
# -------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    top_products = filtered_df.groupby("Product line")["Revenue"].sum().reset_index()
    fig1 = px.bar(top_products, x="Product line", y="Revenue", color="Revenue")
    fig1.update_layout(template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    monthly = filtered_df.groupby("Month")["Revenue"].sum().reset_index()
    fig2 = px.line(monthly, x="Month", y="Revenue", markers=True)
    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# SECOND HEADINGS (FIXED)
# -------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="glass"><h3>🌍 City Sales</h3></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass"><h3>👥 Customer Types</h3></div>', unsafe_allow_html=True)

# -------------------------
# SECOND CHARTS
# -------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    city_sales = filtered_df.groupby("City")["Revenue"].sum().reset_index()
    fig3 = px.bar(city_sales, x="City", y="Revenue", color="Revenue")
    fig3.update_layout(template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    cust = filtered_df.groupby("Customer type")["Revenue"].sum().reset_index()
    fig4 = px.pie(cust, names="Customer type", values="Revenue", hole=0.5)
    fig4.update_layout(template="plotly_dark")
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# IMPROVED INSIGHTS
# -------------------------
top_cat = top_products.sort_values(by="Revenue", ascending=False).iloc[0]["Product line"]
top_city = city_sales.sort_values(by="Revenue", ascending=False).iloc[0]["City"]

st.markdown(f"""
<div class="insight">

<h3>📌 Smart Business Insights</h3>

✅ <b>Top Revenue Driver:</b> {top_cat}  
→ Increase inventory & run targeted promotions  

🌍 <b>Top Performing City:</b> {top_city}  
→ Expand operations & consider new outlets  

📊 <b>Sales Trend Insight:</b>  
→ Identify peak months & align marketing campaigns  

👥 <b>Customer Strategy:</b>  
→ Strengthen loyalty programs for repeat customers  

📉 <b>Improvement Areas:</b>  
→ Boost low-performing categories with offers  

💡 <b>Growth Opportunities:</b>  
→ Bundle products, cross-sell, and upsell  

🚀 <b>Business Recommendation:</b>  
→ Focus on high-margin + high-demand products for faster growth  

</div>
""", unsafe_allow_html=True)

# -------------------------
# DOWNLOAD BUTTON
# -------------------------
csv = filtered_df.to_csv(index=False).encode('utf-8')

st.markdown('<div class="center-btn">', unsafe_allow_html=True)
st.download_button("📥 Download Report", data=csv, file_name="sales_report.csv", mime="text/csv")
st.markdown('</div>', unsafe_allow_html=True)