import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DataFlow",
    layout="wide",
    page_icon="🚀"
)

# ─────────────────────────────────────────────
# DARK SAAS DESIGN SYSTEM
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at 20% 20%, #1e293b, #0f172a 60%);
    color: #e2e8f0;
}

section[data-testid="stSidebar"] {
    background: #0b1220;
    border-right: 1px solid rgba(255,255,255,0.05);
}

.card {
    background: #111827;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 18px;
    padding: 1.5rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

.kpi {
    background: linear-gradient(145deg,#111827,#0f172a);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 1.2rem;
}

.kpi-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #94a3b8;
}

.kpi-value {
    font-size: 2rem;
    font-weight: 800;
    margin-top: .3rem;
}

h1,h2,h3 {
    font-weight: 700;
}

.stButton > button {
    background: linear-gradient(90deg,#6366f1,#8b5cf6);
    border: none;
    color: white;
    border-radius: 10px;
    padding: .5rem 1.2rem;
}

.stDataFrame, .stTable {
    border-radius: 14px !important;
    overflow: hidden !important;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
def load_data():
    fp = "sales_data.csv"
    if not os.path.exists(fp):
        pd.DataFrame({
            "Date":["2023-01-15","2023-02-20","2023-03-10"],
            "Product":["Laptop","Mouse","Keyboard"],
            "Quantity":[10,50,30],
            "Price":[25000,500,800],
            "Region":["North","South","Central"]
        }).to_csv(fp,index=False)
    return pd.read_csv(fp)

df = load_data()

df["Total"] = df["Quantity"] * df["Price"]

# ─────────────────────────────────────────────
# SIDEBAR NAV
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 DataFlow")
    page = st.radio(
        "",
        ["Overview","Data","Quality","Cleaning","Analytics","Visualization","Security"]
    )

# ─────────────────────────────────────────────
# KPI FUNCTION
# ─────────────────────────────────────────────
def kpi(label,value):
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """,unsafe_allow_html=True)

# ─────────────────────────────────────────────
# OVERVIEW
# ─────────────────────────────────────────────
if page == "Overview":
    st.title("Overview")

    col1,col2,col3,col4 = st.columns(4)
    col1.markdown(kpi("Revenue",f"฿{df['Total'].sum():,.0f}"),unsafe_allow_html=True)
    col2.markdown(kpi("Orders",len(df)),unsafe_allow_html=True)
    col3.markdown(kpi("Products",df["Product"].nunique()),unsafe_allow_html=True)
    col4.markdown(kpi("Regions",df["Region"].nunique()),unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)

    st.markdown('<div class="card">',unsafe_allow_html=True)
    monthly = df.groupby("Date")["Total"].sum()
    fig,ax = plt.subplots()
    ax.plot(monthly.index,monthly.values,linewidth=2)
    ax.set_title("Sales Trend")
    ax.tick_params(axis='x',rotation=45)
    st.pyplot(fig,use_container_width=True)
    st.markdown("</div>",unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA MANAGEMENT
# ─────────────────────────────────────────────
elif page == "Data":
    st.title("Data Management")

    with st.form("add"):
        d = st.date_input("Date")
        p = st.text_input("Product")
        q = st.number_input("Quantity",1)
        pr = st.number_input("Price",1)
        r = st.text_input("Region")
        if st.form_submit_button("Add"):
            new = pd.DataFrame([[str(d),p,q,pr,r]],columns=df.columns[:-1])
            new["Total"]=new["Quantity"]*new["Price"]
            df2 = pd.concat([df,new])
            df2.to_csv("sales_data.csv",index=False)
            st.success("Added")
            st.rerun()

    st.markdown('<div class="card">',unsafe_allow_html=True)
    st.dataframe(df,use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ─────────────────────────────────────────────
# QUALITY
# ─────────────────────────────────────────────
elif page == "Quality":
    st.title("Data Quality")

    nulls = df.isnull().sum().sum()
    dup = df.duplicated().sum()

    col1,col2 = st.columns(2)
    col1.markdown(kpi("Missing",nulls),unsafe_allow_html=True)
    col2.markdown(kpi("Duplicates",dup),unsafe_allow_html=True)

    st.markdown('<div class="card">',unsafe_allow_html=True)
    st.dataframe(df.describe(),use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CLEANING
# ─────────────────────────────────────────────
elif page == "Cleaning":
    st.title("Cleaning")

    if st.button("Remove Duplicates"):
        df2 = df.drop_duplicates()
        df2.to_csv("sales_data.csv",index=False)
        st.success("Cleaned")
        st.rerun()

    st.markdown('<div class="card">',unsafe_allow_html=True)
    st.dataframe(df,use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ANALYTICS
# ─────────────────────────────────────────────
elif page == "Analytics":
    st.title("Analytics")

    region = df.groupby("Region")["Total"].sum()

    st.markdown('<div class="card">',unsafe_allow_html=True)
    fig,ax = plt.subplots()
    ax.bar(region.index,region.values)
    ax.set_title("Revenue by Region")
    st.pyplot(fig,use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ─────────────────────────────────────────────
# VISUALIZATION
# ─────────────────────────────────────────────
elif page == "Visualization":
    st.title("Visualization")

    top = df.groupby("Product")["Quantity"].sum().sort_values()

    st.markdown('<div class="card">',unsafe_allow_html=True)
    fig,ax = plt.subplots()
    ax.barh(top.index,top.values)
    ax.set_title("Top Products")
    st.pyplot(fig,use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────────
elif page == "Security":
    st.title("Security")

    st.markdown("""
    <div class="card">
    <h3>Role Based Access</h3>
    <ul>
    <li>Admin – Full Access</li>
    <li>Analyst – Data & Analytics</li>
    <li>Viewer – Read Only</li>
    </ul>
    </div>
    """,unsafe_allow_html=True)