import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="DataFlow", layout="wide", page_icon="🚀")

# ─────────────────────────────────────────────
# DARK SAAS STYLE
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ───────── Background ───────── */
.stApp {
    background: radial-gradient(circle at 10% 10%, #0f172a, #0b1220 60%);
    color: #e5e7eb;
}

/* ───────── Sidebar Builder Panel ───────── */
section[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid rgba(255,255,255,0.05);
}

/* Sidebar Section Titles */
.sidebar-title {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #64748b;
    margin-top: 1rem;
    margin-bottom: .5rem;
}

/* ───────── Top Control Bar ───────── */
.topbar-dark {
    background: #0b1220;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding: .7rem 1.5rem;
    margin: -2rem -2rem 1.5rem -2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* ───────── Canvas Card ───────── */
.canvas-card {
    background: #111827;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 1.5rem;
    box-shadow: 0 15px 40px rgba(0,0,0,0.4);
}

/* ───────── KPI ───────── */
.kpi {
    background: linear-gradient(145deg,#111827,#0f172a);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 1rem;
}

.kpi-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #94a3b8;
}

.kpi-value {
    font-size: 1.9rem;
    font-weight: 800;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg,#6366f1,#8b5cf6);
    border: none;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SAFE DATA LOADER (รองรับหลาย schema)
# ─────────────────────────────────────────────
def load_data():
    fp = "sales_data.csv"

    # ถ้าไม่มีไฟล์ สร้าง default
    if not os.path.exists(fp):
        pd.DataFrame({
            "Date":["2023-01-15","2023-02-20","2023-03-10"],
            "Product":["Laptop","Mouse","Keyboard"],
            "Quantity":[10,50,30],
            "Price":[25000,500,800],
            "Region":["North","South","Central"]
        }).to_csv(fp,index=False)

    df = pd.read_csv(fp)

    # Map ชื่อคอลัมน์เก่า → ใหม่
    column_map = {
        "Product Name": "Product",
        "Unit Price": "Price",
        "Product_ID": "ProductID"
    }

    df = df.rename(columns=column_map)

    # ตรวจสอบคอลัมน์จำเป็น
    required = ["Quantity","Price"]
    for col in required:
        if col not in df.columns:
            st.error(f"Missing required column: {col}")
            st.stop()

    # แปลงเป็นตัวเลข
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce").fillna(0)

    df["Total"] = df["Quantity"] * df["Price"]

    return df

df = load_data()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 DataFlow")
    page = st.radio("", [
        "Overview",
        "Data Management",
        "Quality",
        "Cleaning",
        "Analytics",
        "Visualization",
        "Security"
    ])

# ─────────────────────────────────────────────
# KPI HELPER
# ─────────────────────────────────────────────
def show_kpi(label,value):
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# OVERVIEW
# ─────────────────────────────────────────────
if page == "Overview":
    st.title("Overview")

    c1,c2,c3,c4 = st.columns(4)
    with c1: show_kpi("Revenue",f"฿{df['Total'].sum():,.0f}")
    with c2: show_kpi("Orders",len(df))
    with c3: show_kpi("Products",df["Product"].nunique() if "Product" in df.columns else "-")
    with c4: show_kpi("Regions",df["Region"].nunique() if "Region" in df.columns else "-")

    st.markdown("<br>",unsafe_allow_html=True)

    st.markdown('<div class="card">',unsafe_allow_html=True)
    monthly = df.groupby("Date")["Total"].sum()
    fig,ax = plt.subplots()
    ax.plot(monthly.index,monthly.values)
    ax.set_title("Sales Trend")
    ax.tick_params(axis='x',rotation=45)
    st.pyplot(fig,use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)
st.markdown("""
<div class="topbar-dark">
    <div style="font-weight:600;">🧩 DataFlow Builder</div>
    <div style="font-size:0.8rem;color:#94a3b8;">
        Desktop · 1200px · Production Mode
    </div>
</div>
""", unsafe_allow_html=True)
# ─────────────────────────────────────────────
# DATA MANAGEMENT
# ─────────────────────────────────────────────
elif page == "Data Management":
    st.title("Data Management")

    with st.form("add_form"):
        d = st.date_input("Date")
        p = st.text_input("Product")
        q = st.number_input("Quantity",1)
        pr = st.number_input("Price",1)
        r = st.text_input("Region")

        if st.form_submit_button("Add Data"):
            new = pd.DataFrame([[str(d),p,q,pr,r]],
                               columns=["Date","Product","Quantity","Price","Region"])
            new["Total"] = new["Quantity"]*new["Price"]
            df2 = pd.concat([df,new], ignore_index=True)
            df2.to_csv("sales_data.csv",index=False)
            st.success("Data Added")
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

    c1,c2 = st.columns(2)
    with c1: show_kpi("Missing Values",nulls)
    with c2: show_kpi("Duplicates",dup)

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
        st.success("Duplicates Removed")
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
    <h3>Role-Based Access Control</h3>
    <ul>
        <li><b>Admin</b> – Full Access</li>
        <li><b>Analyst</b> – Data & Analytics</li>
        <li><b>Viewer</b> – Read Only</li>
    </ul>
    </div>
    """,unsafe_allow_html=True)