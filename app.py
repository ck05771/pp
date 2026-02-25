import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DataFlow Builder",
    layout="wide",
    page_icon="🧩"
)

# ─────────────────────────────────────────────
# BUILDER + DARK SAAS UI
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp {
    background: radial-gradient(circle at 10% 10%, #0f172a, #0b1220 60%);
    color: #e5e7eb;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid rgba(255,255,255,0.05);
}

.sidebar-title {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #64748b;
    margin-top: 1rem;
    margin-bottom: .5rem;
}

/* Topbar */
.topbar-dark {
    background: #0b1220;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding: .7rem 1.5rem;
    margin: -2rem -2rem 1.5rem -2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Canvas */
.canvas-card {
    background: #111827;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 1.5rem;
    box-shadow: 0 15px 40px rgba(0,0,0,0.4);
}

/* KPI */
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

.stButton > button {
    background: linear-gradient(90deg,#6366f1,#8b5cf6);
    border: none;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TOP CONTROL BAR
# ─────────────────────────────────────────────
st.markdown("""
<div class="topbar-dark">
    <div style="font-weight:600;">🧩 DataFlow Builder</div>
    <div style="font-size:0.8rem;color:#94a3b8;">
        Desktop · 1200px · Production Mode
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SAFE DATA LOADER
# ─────────────────────────────────────────────
def load_data():
    fp = "sales_data.csv"

    if not os.path.exists(fp):
        pd.DataFrame({
            "Date": ["2023-01-15","2023-02-20","2023-03-10"],
            "Product_ID": ["P001","P002","P003"],
            "Product Name": ["Laptop","Mouse","Keyboard"],
            "Category": ["IT","IT","IT"],
            "Quantity": [10,50,30],
            "Unit Price": [25000,500,800],
            "Region": ["North","South","Central"]
        }).to_csv(fp, index=False)

    df = pd.read_csv(fp)

    column_map = {
        "Product": "Product Name",
        "Price": "Unit Price",
        "product": "Product Name",
        "price": "Unit Price"
    }

    df = df.rename(columns=column_map)

    if "Unit Price" not in df.columns and "Price" in df.columns:
        df["Unit Price"] = df["Price"]

    if "Product Name" not in df.columns and "Product" in df.columns:
        df["Product Name"] = df["Product"]

    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)
    df["Unit Price"] = pd.to_numeric(df["Unit Price"], errors="coerce").fillna(0)
    df["Total"] = df["Quantity"] * df["Unit Price"]

    return df

df = load_data()

# ─────────────────────────────────────────────
# SIDEBAR (BUILDER STYLE)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🗂 Pages")
    page = st.radio("", [
        "Overview",
        "Data Management",
        "Quality",
        "Cleaning",
        "Analytics",
        "Visualization",
        "Security"
    ])

    st.markdown('<div class="sidebar-title">Layers</div>', unsafe_allow_html=True)
    st.checkbox("Navigation")
    st.checkbox("Header")
    st.checkbox("Charts")
    st.checkbox("Tables")

    st.markdown('<div class="sidebar-title">Assets</div>', unsafe_allow_html=True)
    st.button("Upload Image")
    st.button("Import Data")

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
# PAGES
# ─────────────────────────────────────────────
st.markdown('<div class="canvas-card">', unsafe_allow_html=True)

if page == "Overview":
    st.title("Overview")

    c1,c2,c3,c4 = st.columns(4)
    with c1: show_kpi("Revenue",f"฿{df['Total'].sum():,.0f}")
    with c2: show_kpi("Orders",len(df))
    with c3: show_kpi("Products",df["Product Name"].nunique())
    with c4: show_kpi("Regions",df["Region"].nunique())

    monthly = df.groupby("Date")["Total"].sum()
    fig,ax = plt.subplots()
    ax.plot(monthly.index,monthly.values)
    ax.set_title("Sales Trend")
    ax.tick_params(axis='x',rotation=45)
    st.pyplot(fig,use_container_width=True)

elif page == "Data Management":
    st.title("Data Management")
    st.dataframe(df,use_container_width=True)

elif page == "Quality":
    st.title("Data Quality")
    st.write("Missing Values:", df.isnull().sum().sum())
    st.write("Duplicates:", df.duplicated().sum())

elif page == "Cleaning":
    st.title("Cleaning")
    if st.button("Remove Duplicates"):
        df.drop_duplicates().to_csv("sales_data.csv",index=False)
        st.success("Duplicates Removed")
        st.rerun()

elif page == "Analytics":
    st.title("Analytics")
    region = df.groupby("Region")["Total"].sum()
    fig,ax = plt.subplots()
    ax.bar(region.index,region.values)
    ax.set_title("Revenue by Region")
    st.pyplot(fig,use_container_width=True)

elif page == "Visualization":
    st.title("Visualization")
    top = df.groupby("Product Name")["Quantity"].sum().sort_values()
    fig,ax = plt.subplots()
    ax.barh(top.index,top.values)
    ax.set_title("Top Products")
    st.pyplot(fig,use_container_width=True)

elif page == "Security":
    st.title("Security")
    st.markdown("""
    <ul>
        <li><b>Admin</b> – Full Access</li>
        <li><b>Analyst</b> – Data & Analytics</li>
        <li><b>Viewer</b> – Read Only</li>
    </ul>
    """,unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)