import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

st.set_page_config(page_title="DataFlow · Sales", layout="wide", page_icon="📊")

# ═══════════════════════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --bg:       #EDF2FF;
    --surf:     #FFFFFF;
    --surf2:    #F0F4FF;
    --b1:       #C5D5FF;
    --b2:       #A3BAFF;
    --t1:       #0F2167;
    --t2:       #1E40AF;
    --t3:       #3B82F6;
    --t4:       #93C5FD;
    --blue:     #2563EB;
    --blue-dk:  #1D4ED8;
    --blue-lt:  #DBEAFE;
    --green:    #059669;
    --green-lt: #D1FAE5;
    --amber:    #D97706;
    --amber-lt: #FEF3C7;
    --red:      #DC2626;
    --red-lt:   #FEE2E2;
    --r:        10px;
    --sh: 0 1px 3px rgba(37,99,235,.08), 0 4px 16px rgba(37,99,235,.06);
    --sh2: 0 2px 6px rgba(37,99,235,.12), 0 8px 32px rgba(37,99,235,.1);
}

*, html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif !important;
    box-sizing: border-box;
}
.stApp { background: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 4rem 2rem !important; max-width: 1440px !important; }

/* ══ TOPBAR ══════════════════════════════════════════ */
.topbar {
    background: var(--t1);
    margin: 0 -2rem 2rem -2rem;
    padding: 0 2rem;
    display: flex; align-items: center; justify-content: space-between;
    height: 52px;
    position: sticky; top: 0; z-index: 999;
}
.brand { display: flex; align-items: center; gap: 10px; }
.brand-mark {
    width: 28px; height: 28px; background: var(--blue);
    border-radius: 6px; display: flex; align-items: center; justify-content: center;
    font-size: 12px; color: #fff; font-weight: 800;
    border: 1px solid rgba(255,255,255,.2);
}
.brand-name { font-size: 0.9rem; font-weight: 700; color: #fff; letter-spacing: -0.01em; }
.brand-sep  { color: rgba(255,255,255,.3); margin: 0 4px; }
.brand-sub  { font-size: 0.75rem; color: rgba(255,255,255,.55); }
.topbar-stats { display: flex; gap: 0; }
.tstat {
    padding: 0 1.2rem; border-left: 1px solid rgba(255,255,255,.12);
    display: flex; flex-direction: column; align-items: flex-end;
}
.tstat-label { font-size: 0.6rem; color: rgba(255,255,255,.45); text-transform: uppercase; letter-spacing: .08em; }
.tstat-val   { font-size: 0.88rem; font-weight: 700; color: #fff; letter-spacing: -0.02em; }

/* ══ TABS ══════════════════════════════════════════════ */
[data-testid="stSidebar"] { display: none !important; }
.main > div:first-child   { margin-left: 0 !important; }

.stTabs [data-baseweb="tab-list"] {
    gap: 0 !important; background: var(--surf) !important;
    border: 1px solid var(--b1) !important; border-radius: var(--r) !important;
    padding: 3px !important; box-shadow: var(--sh) !important; margin-bottom: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px !important; padding: 0.42rem 1rem !important;
    font-size: 0.77rem !important; font-weight: 500 !important;
    color: var(--t2) !important; background: transparent !important;
    border: none !important; transition: all 0.12s !important;
    white-space: nowrap !important;
}
.stTabs [data-baseweb="tab"]:hover { background: var(--blue-lt) !important; color: var(--t1) !important; }
.stTabs [aria-selected="true"] { background: var(--blue) !important; color: #fff !important; font-weight: 700 !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding: 1.6rem 0 0 0 !important; }

/* ══ SHARED COMPONENTS ══════════════════════════════════ */
.pill {
    display: inline-flex; align-items: center; gap: 3px;
    padding: 2px 8px; border-radius: 99px;
    font-size: 0.67rem; font-weight: 600; letter-spacing: 0.02em;
}
.p-blue  { background: var(--blue-lt);  color: var(--blue);  border: 1px solid #BFDBFE; }
.p-green { background: var(--green-lt); color: var(--green); border: 1px solid #6EE7B7; }
.p-amber { background: var(--amber-lt); color: var(--amber); border: 1px solid #FCD34D; }
.p-red   { background: var(--red-lt);   color: var(--red);   border: 1px solid #FCA5A5; }

/* ══ TAB 0 — Grid card layout ══════════════════════════ */
.t0-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; margin-bottom: 1.5rem; }
.t0-card {
    background: var(--surf); border: 1px solid var(--b1);
    border-radius: 14px; padding: 1.4rem 1.6rem;
    box-shadow: var(--sh);
}
.t0-card-title {
    font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .08em; color: var(--t3); margin-bottom: 1rem;
    padding-bottom: .65rem; border-bottom: 1px solid var(--b1);
    display: flex; align-items: center; gap: 6px;
}
.t0-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--blue); flex-shrink:0; }

/* ══ TAB 1 — Full-width stacked layout ═════════════════ */
.t1-banner {
    background: linear-gradient(135deg, var(--t1) 0%, #1E40AF 100%);
    border-radius: 14px; padding: 1.8rem 2rem;
    margin-bottom: 1.4rem; color: #fff;
    display: flex; justify-content: space-between; align-items: center;
}
.t1-banner-title { font-size: 1.1rem; font-weight: 700; letter-spacing: -0.02em; }
.t1-banner-desc  { font-size: 0.78rem; opacity: 0.65; margin-top: 3px; }
.t1-score-ring {
    width: 80px; height: 80px; border-radius: 50%;
    border: 4px solid rgba(255,255,255,.25);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.t1-score-num  { font-size: 1.4rem; font-weight: 800; line-height: 1; }
.t1-score-text { font-size: 0.58rem; opacity: .6; text-transform: uppercase; letter-spacing: .06em; }

.t1-check-row {
    display: flex; align-items: center; gap: 14px;
    padding: 1rem 1.2rem; background: var(--surf);
    border: 1px solid var(--b1); border-radius: var(--r);
    box-shadow: var(--sh); margin-bottom: .7rem;
}
.t1-check-icon {
    width: 38px; height: 38px; border-radius: 10px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; font-size: 16px;
}
.t1-check-title { font-size: 0.85rem; font-weight: 600; color: var(--t1); }
.t1-check-desc  { font-size: 0.74rem; color: var(--t3); margin-top: 2px; }

/* ══ TAB 2 — Left sidebar + main layout ══════════════════ */
.t2-wrap  { display: flex; gap: 1.4rem; }
.t2-side  {
    width: 260px; flex-shrink: 0;
    background: var(--t1); border-radius: 14px;
    padding: 1.4rem 1.2rem; color: #fff; align-self: flex-start;
}
.t2-main  { flex: 1; min-width: 0; }
.t2-step  {
    display: flex; align-items: flex-start; gap: 12px;
    padding: .9rem .8rem; border-radius: 8px;
    margin-bottom: .4rem;
    transition: background .12s;
    cursor: default;
}
.t2-step:hover { background: rgba(255,255,255,.08); }
.t2-num {
    width: 24px; height: 24px; border-radius: 50%; flex-shrink: 0;
    background: rgba(255,255,255,.15); color: #fff;
    font-size: 0.67rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    border: 1px solid rgba(255,255,255,.2);
}
.t2-step-title { font-size: 0.8rem; font-weight: 600; color: #fff; }
.t2-step-desc  { font-size: 0.7rem; color: rgba(255,255,255,.55); margin-top: 2px; line-height: 1.4; }
.t2-side-title { font-size: 0.65rem; text-transform: uppercase; letter-spacing: .1em; color: rgba(255,255,255,.4); font-weight: 700; margin-bottom: .8rem; padding-bottom: .5rem; border-bottom: 1px solid rgba(255,255,255,.1); }

/* ══ TAB 3 — Magazine editorial layout ═══════════════════ */
.t3-hero {
    background: var(--surf); border: 1px solid var(--b1);
    border-radius: 14px; padding: 0; overflow: hidden;
    box-shadow: var(--sh2); margin-bottom: 1.2rem;
    display: flex; min-height: 110px;
}
.t3-hero-bar {
    width: 6px; flex-shrink: 0;
    background: linear-gradient(to bottom, var(--blue), #60A5FA);
}
.t3-hero-body { padding: 1.4rem 1.6rem; flex: 1; }
.t3-hero-kpis { display: grid; grid-template-columns: repeat(4,1fr); gap: .8rem; }
.t3-kpi {
    padding: .9rem 1rem; background: var(--surf);
    border: 1px solid var(--b1); border-radius: var(--r);
    box-shadow: var(--sh);
}
.t3-kpi-label { font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: .07em; color: var(--t4); margin-bottom: 4px; }
.t3-kpi-val   { font-size: 1.45rem; font-weight: 800; letter-spacing: -0.04em; color: var(--t1); line-height: 1; }
.t3-kpi-sub   { font-size: 0.7rem; color: var(--t3); margin-top: 4px; }

.t3-tables { display: grid; grid-template-columns: 2fr 1.5fr 1.5fr; gap: 1rem; }
.t3-tbl {
    background: var(--surf); border: 1px solid var(--b1);
    border-radius: var(--r); overflow: hidden;
    box-shadow: var(--sh);
}
.t3-tbl-head {
    background: var(--t1); padding: .6rem .9rem;
    font-size: 0.68rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .08em; color: rgba(255,255,255,.7);
}
.t3-tbl-head span { color: #fff; }

/* ══ TAB 4 — Full-bleed alternating layout ═══════════════ */
.t4-rbac {
    background: var(--surf); border: 1px solid var(--b1);
    border-radius: 14px; overflow: hidden; box-shadow: var(--sh);
}
.t4-rbac-header {
    background: var(--t1); padding: .8rem 1.4rem;
    display: flex; align-items: center; gap: 8px;
}
.t4-rbac-header-txt { font-size: 0.8rem; font-weight: 700; color: #fff; }
.t4-role {
    display: flex; align-items: center; gap: 12px;
    padding: .9rem 1.4rem; border-bottom: 1px solid var(--b1);
    transition: background .1s;
}
.t4-role:last-child { border-bottom: none; }
.t4-role:hover { background: var(--blue-lt); }
.t4-role-av {
    width: 36px; height: 36px; border-radius: 10px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; font-size: 15px;
}
.t4-role-name { font-size: 0.84rem; font-weight: 600; color: var(--t1); line-height: 1.2; }
.t4-role-perm { font-size: 0.72rem; color: var(--t3); }

.t4-sec-row {
    display: flex; align-items: stretch; gap: .8rem;
    margin-top: 1.2rem;
}
.t4-sec-panel {
    flex: 1; background: var(--surf); border: 1px solid var(--b1);
    border-radius: 12px; overflow: hidden; box-shadow: var(--sh);
}
.t4-sec-panel-head {
    padding: .65rem 1rem;
    font-size: 0.67rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .08em;
}
.t4-sec-panel-head.tech { background: #1E3A8A; color: rgba(255,255,255,.7); }
.t4-sec-panel-head.mgmt { background: #065F46; color: rgba(255,255,255,.7); }
.t4-sec-item {
    display: flex; align-items: flex-start; gap: 9px;
    padding: .65rem 1rem; border-bottom: 1px solid var(--b1);
}
.t4-sec-item:last-child { border-bottom: none; }
.t4-ic {
    width: 26px; height: 26px; border-radius: 7px; flex-shrink: 0;
    background: var(--blue-lt); color: var(--blue);
    display: flex; align-items: center; justify-content: center; font-size: 12px;
}
.t4-ic.g { background: var(--green-lt); color: var(--green); }
.sl { font-size: 0.8rem; font-weight: 600; color: var(--t1); }
.sd { font-size: 0.71rem; color: var(--t3); margin-top: 1px; line-height: 1.4; }

/* ══ TAB 5 — Asymmetric viz layout ═══════════════════════ */
.t5-main { display: grid; grid-template-columns: 3fr 2fr; gap: 1.2rem; margin-bottom: 1.2rem; }
.t5-card {
    background: var(--surf); border: 1px solid var(--b1);
    border-radius: 14px; padding: 1.3rem 1.5rem;
    box-shadow: var(--sh);
}
.t5-card-label {
    font-size: 0.68rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .08em; color: var(--t3); margin-bottom: .9rem;
    display: flex; align-items: center; gap: 6px;
}
.t5-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--blue); }

/* ══ STREAMLIT OVERRIDES ════════════════════════════════ */
[data-testid="stMetric"] {
    background: var(--surf) !important; border: 1px solid var(--b1) !important;
    border-radius: var(--r) !important; padding: .9rem 1.1rem !important;
    box-shadow: var(--sh) !important;
}
[data-testid="stMetricLabel"] { font-size: 0.65rem !important; text-transform: uppercase !important; letter-spacing: .08em !important; font-weight: 700 !important; color: var(--t3) !important; }
[data-testid="stMetricValue"] { font-size: 1.55rem !important; font-weight: 800 !important; letter-spacing: -0.04em !important; color: var(--t1) !important; }

.stButton > button {
    background: var(--blue) !important; color: #fff !important; border: none !important;
    border-radius: 7px !important; padding: .45rem 1.1rem !important;
    font-size: 0.8rem !important; font-weight: 600 !important;
    box-shadow: 0 1px 4px rgba(37,99,235,.3) !important; transition: all .15s !important;
}
.stButton > button:hover { background: var(--blue-dk) !important; transform: translateY(-1px) !important; box-shadow: 0 3px 12px rgba(37,99,235,.35) !important; }

.stSuccess { background: var(--green-lt) !important; border: 1px solid #6EE7B7 !important; border-left: 3px solid var(--green) !important; border-radius: var(--r) !important; font-size: .82rem !important; }
.stInfo    { background: var(--blue-lt)  !important; border: 1px solid #BFDBFE !important; border-left: 3px solid var(--blue)  !important; border-radius: var(--r) !important; font-size: .82rem !important; }
.stWarning { background: var(--amber-lt) !important; border: 1px solid #FCD34D !important; border-left: 3px solid var(--amber) !important; border-radius: var(--r) !important; font-size: .82rem !important; }
.stError   { background: var(--red-lt)   !important; border: 1px solid #FCA5A5 !important; border-left: 3px solid var(--red)   !important; border-radius: var(--r) !important; font-size: .82rem !important; }

details { background: var(--surf) !important; border: 1px solid var(--b1) !important; border-radius: var(--r) !important; box-shadow: var(--sh) !important; }
summary  { font-size: .81rem !important; font-weight: 600 !important; color: var(--t2) !important; }
hr { border-color: var(--b1) !important; margin: 1.2rem 0 !important; }

.stTextInput input, .stNumberInput input {
    background: var(--surf2) !important; border: 1px solid var(--b2) !important;
    border-radius: 7px !important; font-size: .83rem !important; color: var(--t1) !important;
}
.stTextInput input:focus, .stNumberInput input:focus { border-color: var(--blue) !important; box-shadow: 0 0 0 3px rgba(37,99,235,.1) !important; }
.stSelectbox > div > div, .stDateInput > div > div {
    background: var(--surf2) !important; border: 1px solid var(--b2) !important; border-radius: 7px !important;
}
[data-testid="stDataFrame"] { border: 1px solid var(--b1) !important; border-radius: var(--r) !important; overflow: hidden !important; }
[data-testid="stTable"] table, .stDataFrame table { font-size: .79rem; border-collapse: collapse; width: 100%; }
[data-testid="stTable"] thead th, .stDataFrame thead th {
    background: var(--surf2) !important; color: var(--t3) !important;
    font-size: .66rem !important; font-weight: 700 !important; text-transform: uppercase !important;
    letter-spacing: .08em !important; padding: .6rem .9rem !important; border-bottom: 1px solid var(--b2) !important;
}
[data-testid="stTable"] tbody td, .stDataFrame tbody td {
    padding: .5rem .9rem !important; border-bottom: 1px solid var(--b1) !important;
    font-family: 'IBM Plex Mono', monospace !important; font-size: .75rem !important; color: var(--t1) !important;
}
[data-testid="stTable"] tbody tr:hover td, .stDataFrame tbody tr:hover td { background: var(--blue-lt) !important; }

.empty-state {
    text-align: center; padding: 3.5rem 2rem;
    background: var(--surf); border: 1.5px dashed var(--b2);
    border-radius: 16px; margin: 1rem 0;
}
.empty-icon  { font-size: 2.6rem; margin-bottom: .6rem; }
.empty-title { font-size: .88rem; font-weight: 600; color: var(--t2); }
.empty-desc  { font-size: .74rem; color: var(--t3); margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Matplotlib ─────────────────────────────────────────────────────────────────
PALETTE = ["#2563EB", "#059669", "#D97706", "#DC2626", "#7C3AED", "#0891B2"]
BG_C = "#FFFFFF"
mpl.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["IBM Plex Sans", "Helvetica Neue", "Arial"],
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False, "axes.spines.bottom": False,
    "axes.grid": True, "grid.color": "#DBEAFE", "grid.linewidth": 0.8,
    "axes.facecolor": BG_C, "figure.facecolor": BG_C,
    "axes.labelcolor": "#3B82F6", "xtick.color": "#3B82F6", "ytick.color": "#3B82F6",
    "xtick.labelsize": 9, "ytick.labelsize": 9,
    "axes.titlesize": 11, "axes.titleweight": "700", "axes.titlepad": 14, "figure.dpi": 140,
})

# ── Data ───────────────────────────────────────────────────────────────────────
def load_data():
    fp = 'sales_data.csv'
    if not os.path.exists(fp):
        pd.DataFrame({
            "Date":         ["2023-01-15","2023-02-20","2023-03-10","2023-03-25",
                             "2023-04-05","2023-05-18","2023-06-22","2023-07-08"],
            "Product_ID":   ["P001","P002","P003","P001","P004","P002","P005","P003"],
            "Product Name": ["Laptop","Mouse","Keyboard","Laptop","Monitor","Mouse","Headset","Keyboard"],
            "Category":     ["IT","IT","IT","IT","IT","IT","IT","IT"],
            "Quantity":     [10, 50, 30, 8, 5, 40, 20, 25],
            "Unit Price":   [25000, 500, 800, 25000, 8000, 500, 1500, 800],
            "Region":       ["North","South","Central","East","North","West","South","Central"],
        }).to_csv(fp, index=False)
    return pd.read_csv(fp)

df = load_data()

total_sales = (pd.to_numeric(df['Quantity'], errors='coerce').fillna(0) *
               pd.to_numeric(df['Unit Price'], errors='coerce').fillna(0)).sum()
n_products  = df['Product Name'].nunique() if 'Product Name' in df.columns else 0

# ── TOPBAR ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
  <div class="brand">
    <div class="brand-mark">DF</div>
    <div>
      <span class="brand-name">DataFlow</span>
      <span class="brand-sep"> · </span>
      <span class="brand-sub">Sales Analytics</span>
    </div>
  </div>
  <div class="topbar-stats">
    <div class="tstat">
      <span class="tstat-label">รายการ</span>
      <span class="tstat-val">{len(df):,}</span>
    </div>
    <div class="tstat">
      <span class="tstat-label">ยอดรวม</span>
      <span class="tstat-val">฿{total_sales:,.0f}</span>
    </div>
    <div class="tstat">
      <span class="tstat-label">สินค้า</span>
      <span class="tstat-val">{n_products}</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⊞  จัดการข้อมูล",
    "⊙  ตรวจสอบคุณภาพ",
    "⊘  ทำความสะอาด",
    "⊛  วิเคราะห์",
    "⊜  ความปลอดภัย",
    "⊝  Visualization",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 0 — จัดการข้อมูล
# layout: 2-column card grid (ฟอร์มซ้าย + delete panel ขวา)
#         + full-width table ด้านล่างพร้อม accent left border
# ══════════════════════════════════════════════════════════════════════════════
with tab0:
    st.markdown("""
    <div style="margin-bottom:1.4rem;">
      <div style="font-size:1.2rem;font-weight:800;letter-spacing:-.025em;color:var(--t1);">จัดการฐานข้อมูล</div>
      <div style="font-size:.76rem;color:var(--t3);margin-top:2px;">เพิ่มรายการยอดขาย · ลบข้อมูลที่ไม่ต้องการ</div>
    </div>
    <div class="t0-grid">
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2], gap="large")

    with col_a:
        st.markdown('<div class="t0-card"><div class="t0-card-title"><span class="t0-dot"></span>เพิ่มรายการยอดขายใหม่</div>', unsafe_allow_html=True)
        with st.form("add_form", clear_on_submit=True):
            ra1, ra2, ra3 = st.columns(3)
            new_date  = ra1.date_input("วันที่ขาย")
            new_id    = ra2.text_input("รหัสสินค้า", placeholder="P001")
            new_name  = ra3.text_input("ชื่อสินค้า",  placeholder="Laptop")
            rb1, rb2, rb3 = st.columns(3)
            new_cat   = rb1.selectbox("หมวดหมู่",    ["IT","Furniture","Electronics"])
            new_qty   = rb2.number_input("จำนวน",     min_value=1, value=1)
            new_price = rb3.number_input("ราคา/หน่วย", min_value=1, value=100)
            new_reg   = st.selectbox("ภูมิภาค", ["North","South","Central","East","West"])
            if st.form_submit_button("＋  บันทึกข้อมูล", use_container_width=True):
                new_row = pd.DataFrame([[str(new_date), new_id, new_name, new_cat, new_qty, new_price, new_reg]], columns=df.columns)
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv('sales_data.csv', index=False)
                st.success(f"✓ เพิ่ม **{new_name}** สำเร็จ")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="t0-card"><div class="t0-card-title"><span class="t0-dot" style="background:var(--red)"></span>ลบรายการ</div>', unsafe_allow_html=True)
        preview_df = df[['Product Name','Quantity','Unit Price','Region']].reset_index().rename(columns={"index":"#"})
        st.dataframe(preview_df, use_container_width=True, height=190)
        del_idx = st.number_input("เลขลำดับ (#) ที่ต้องการลบ", min_value=0, max_value=max(len(df)-1,0), step=1)
        preview_name = df.iloc[del_idx]['Product Name'] if len(df) > 0 else "—"
        st.markdown(f'<div style="background:var(--red-lt);border:1px solid #FCA5A5;border-radius:7px;padding:7px 11px;font-size:.76rem;color:#991B1B;margin:5px 0 8px;">⚠ จะลบ: <strong>{preview_name}</strong> (แถว #{del_idx})</div>', unsafe_allow_html=True)
        if st.button("🗑  ยืนยันการลบ", use_container_width=True):
            df = df.drop(df.index[del_idx]).reset_index(drop=True)
            df.to_csv('sales_data.csv', index=False)
            st.warning("ลบแล้ว")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Full-width table with left accent
    st.markdown("""
    <div style="border-left:4px solid var(--blue);padding-left:1rem;margin:.5rem 0 .7rem;">
      <div style="font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--t3);">ข้อมูลทั้งหมดในระบบ</div>
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — ตรวจสอบคุณภาพ
# layout: Hero banner สีน้ำเงินเข้ม + check-row list แนวตั้ง
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    null_rows = df[df.isnull().any(axis=1)]
    dup_rows  = df[df.duplicated(keep=False)]
    n_null    = len(null_rows)
    n_dup     = len(df[df.duplicated()])
    score     = max(0, min(100, 100 - (n_null + n_dup) * 5))
    score_color = "#34D399" if score >= 90 else "#FBBF24" if score >= 70 else "#F87171"

    st.markdown(f"""
    <div class="t1-banner">
      <div>
        <div class="t1-banner-title">ตรวจสอบคุณภาพข้อมูล</div>
        <div class="t1-banner-desc">สแกนหา Missing Values · Duplicates · ชนิดข้อมูล</div>
        <div style="display:flex;gap:8px;margin-top:10px;">
          <span style="background:rgba(255,255,255,.12);color:#fff;border-radius:99px;padding:2px 10px;font-size:.68rem;font-weight:600;border:1px solid rgba(255,255,255,.2);">📁 {len(df)} แถว</span>
          <span style="background:rgba(255,255,255,.12);color:#fff;border-radius:99px;padding:2px 10px;font-size:.68rem;font-weight:600;border:1px solid rgba(255,255,255,.2);">⚠ Missing: {n_null}</span>
          <span style="background:rgba(255,255,255,.12);color:#fff;border-radius:99px;padding:2px 10px;font-size:.68rem;font-weight:600;border:1px solid rgba(255,255,255,.2);">⊕ Dup: {n_dup}</span>
        </div>
      </div>
      <div class="t1-score-ring" style="border-color:{score_color}55;">
        <span class="t1-score-num" style="color:{score_color};">{score}</span>
        <span class="t1-score-text">SCORE</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # check rows before button press (always visible)
    null_ok = null_rows.empty
    dup_ok  = dup_rows.empty
    st.markdown(f"""
    <div class="t1-check-row">
      <div class="t1-check-icon" style="background:{'#D1FAE5' if null_ok else '#FEE2E2'};">
        {'✅' if null_ok else '❌'}
      </div>
      <div style="flex:1">
        <div class="t1-check-title">Missing Values</div>
        <div class="t1-check-desc">{'ข้อมูลครบถ้วนทุกแถว' if null_ok else f'พบ {n_null} แถวที่ขาดข้อมูล'}</div>
      </div>
      <span class="pill {'p-green' if null_ok else 'p-red'}">{'ผ่าน' if null_ok else 'ไม่ผ่าน'}</span>
    </div>
    <div class="t1-check-row">
      <div class="t1-check-icon" style="background:{'#D1FAE5' if dup_ok else '#FEF3C7'};">
        {'✅' if dup_ok else '⚠️'}
      </div>
      <div style="flex:1">
        <div class="t1-check-title">Duplicates</div>
        <div class="t1-check-desc">{'ไม่พบข้อมูลซ้ำ' if dup_ok else f'พบ {n_dup} รายการซ้ำ'}</div>
      </div>
      <span class="pill {'p-green' if dup_ok else 'p-amber'}">{'ผ่าน' if dup_ok else 'ตรวจสอบ'}</span>
    </div>
    <div class="t1-check-row">
      <div class="t1-check-icon" style="background:#DBEAFE;">🔍</div>
      <div style="flex:1">
        <div class="t1-check-title">ชนิดข้อมูล (Data Types)</div>
        <div class="t1-check-desc">กดปุ่มด้านล่างเพื่อสแกนชนิดข้อมูลรายคอลัมน์</div>
      </div>
      <span class="pill p-blue">รอสแกน</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

    if st.button("▶  เริ่มตรวจสอบเต็มรูปแบบ"):
        if not null_rows.empty:
            st.error(f"พบ {n_null} แถวที่ขาดข้อมูล")
            st.dataframe(null_rows, use_container_width=True)
        if not dup_rows.empty:
            st.warning(f"พบ {n_dup} รายการซ้ำ")
            st.dataframe(dup_rows.sort_values(by=list(df.columns)), use_container_width=True)
        st.markdown("**ชนิดข้อมูลรายคอลัมน์**")
        def check_type(v): return type(v).__name__
        st.dataframe(df.applymap(check_type), use_container_width=True)
        st.info("คอลัมน์ตัวเลขที่แสดงเป็น `str` = ชนิดข้อมูลผิดพลาด")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ทำความสะอาด
# layout: Sidebar เข้มซ้าย + content area ขวา
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="t2-wrap">', unsafe_allow_html=True)

    left_col, right_col = st.columns([1, 3], gap="large")

    with left_col:
        st.markdown("""
        <div class="t2-side">
          <div class="t2-side-title">Pipeline Steps</div>
          <div class="t2-step">
            <div class="t2-num">1</div>
            <div>
              <div class="t2-step-title">Deduplication</div>
              <div class="t2-step-desc">ลบแถวซ้ำทุกฟิลด์</div>
            </div>
          </div>
          <div class="t2-step">
            <div class="t2-num">2</div>
            <div>
              <div class="t2-step-title">Outlier Filter</div>
              <div class="t2-step-desc">กรอง Qty ≤ 0, Price ≤ 0</div>
            </div>
          </div>
          <div class="t2-step">
            <div class="t2-num">3</div>
            <div>
              <div class="t2-step-title">Date Parsing</div>
              <div class="t2-step-desc">แปลง Date → datetime64</div>
            </div>
          </div>
          <div style="margin-top:1.2rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,.1);">
            <div class="t2-side-title">เกณฑ์</div>
            <div style="font-size:.72rem;color:rgba(255,255,255,.5);line-height:1.6;">
              ข้อมูลที่ผ่านทุกขั้นตอน<br>จะถูกบันทึกใน session<br>เพื่อใช้ในขั้นตอนถัดไป
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown(f"""
        <div style="background:var(--surf);border:1px solid var(--b1);border-radius:12px;padding:1.3rem 1.5rem;box-shadow:var(--sh);margin-bottom:1rem;">
          <div style="font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--t3);margin-bottom:.8rem;padding-bottom:.65rem;border-bottom:1px solid var(--b1);">ภาพรวมก่อนทำความสะอาด</div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.8rem;">
            <div style="text-align:center;padding:.7rem;background:var(--surf2);border-radius:8px;border:1px solid var(--b1);">
              <div style="font-size:1.4rem;font-weight:800;color:var(--t1);">{len(df):,}</div>
              <div style="font-size:.65rem;color:var(--t3);text-transform:uppercase;letter-spacing:.06em;margin-top:2px;">แถวทั้งหมด</div>
            </div>
            <div style="text-align:center;padding:.7rem;background:var(--surf2);border-radius:8px;border:1px solid var(--b1);">
              <div style="font-size:1.4rem;font-weight:800;color:var(--t1);">{len(df[df.duplicated()]):,}</div>
              <div style="font-size:.65rem;color:var(--t3);text-transform:uppercase;letter-spacing:.06em;margin-top:2px;">ซ้ำ</div>
            </div>
            <div style="text-align:center;padding:.7rem;background:var(--surf2);border-radius:8px;border:1px solid var(--b1);">
              <div style="font-size:1.4rem;font-weight:800;color:var(--t1);">{len(df[df.isnull().any(axis=1)]):,}</div>
              <div style="font-size:.65rem;color:var(--t3);text-transform:uppercase;letter-spacing:.06em;margin-top:2px;">Missing</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("▶  เริ่มทำความสะอาด"):
            df_b    = df.copy()
            dup_r   = df_b[df_b.duplicated()]
            df_c    = df_b.drop_duplicates()
            wrong_r = df_c[(pd.to_numeric(df_c['Quantity'],  errors='coerce') <= 0) |
                           (pd.to_numeric(df_c['Unit Price'], errors='coerce') <= 0)]
            df_c    = df_c[(pd.to_numeric(df_c['Quantity'],  errors='coerce') > 0) &
                           (pd.to_numeric(df_c['Unit Price'], errors='coerce') > 0)]
            inv_d   = df_c[pd.to_datetime(df_c['Date'], errors='coerce').isna()]
            df_c['Date'] = pd.to_datetime(df_c['Date'], errors='coerce')
            df_c    = df_c.dropna(subset=['Date'])
            st.session_state['df_clean'] = df_c

            st.success(f"✓ เสร็จสิ้น — ข้อมูลพร้อมใช้งาน **{len(df_c):,}** แถว")
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("เริ่มต้น",       f"{len(df_b):,}")
            r2.metric("ลบซ้ำ",         f"−{len(dup_r)}")
            r3.metric("ลบผิดพลาด",     f"−{len(wrong_r)}")
            r4.metric("พร้อมใช้งาน",   f"{len(df_c):,}")
            with st.expander("รายละเอียดที่ถูกลบ"):
                if not dup_r.empty:   st.markdown("**ซ้ำ:**");     st.dataframe(dup_r,   use_container_width=True)
                if not wrong_r.empty: st.markdown("**ผิดพลาด:**"); st.dataframe(wrong_r, use_container_width=True)
                if not inv_d.empty:   st.markdown("**วันที่:**");   st.dataframe(inv_d,   use_container_width=True)
            st.markdown("**ข้อมูลพร้อมใช้งาน**")
            st.dataframe(df_c, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — วิเคราะห์
# layout: Hero KPI strip + 3-column table grid (ขนาดไม่เท่ากัน)
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    if 'df_clean' not in st.session_state:
        st.markdown('<div class="empty-state"><div class="empty-icon">⊛</div><div class="empty-title">ยังไม่มีข้อมูลที่ผ่านการทำความสะอาด</div><div class="empty-desc">ไปที่แท็บ "ทำความสะอาด" แล้วกดเริ่มก่อน</div></div>', unsafe_allow_html=True)
    else:
        data = st.session_state['df_clean'].copy()
        data['Total_Sales'] = pd.to_numeric(data['Quantity'], errors='coerce') * pd.to_numeric(data['Unit Price'], errors='coerce')
        data['Month'] = data['Date'].dt.to_period('M').astype(str)
        monthly  = data.groupby('Month')['Total_Sales'].sum().reset_index()
        top5     = data.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False).head(5).reset_index()
        region   = data.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False).reset_index()
        best_r   = region.iloc[0]['Region']
        best_p   = top5.iloc[0]['Product Name']
        total_s  = data['Total_Sales'].sum()
        avg_mo   = monthly['Total_Sales'].mean()

        # Hero strip
        st.markdown(f"""
        <div class="t3-hero">
          <div class="t3-hero-bar"></div>
          <div class="t3-hero-body">
            <div style="font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--t3);margin-bottom:.8rem;">ผลลัพธ์การวิเคราะห์</div>
            <div class="t3-hero-kpis">
              <div class="t3-kpi">
                <div class="t3-kpi-label">ยอดขายรวม</div>
                <div class="t3-kpi-val">฿{total_s:,.0f}</div>
                <div class="t3-kpi-sub">จากข้อมูลทั้งหมด</div>
              </div>
              <div class="t3-kpi">
                <div class="t3-kpi-label">เฉลี่ย/เดือน</div>
                <div class="t3-kpi-val">฿{avg_mo:,.0f}</div>
                <div class="t3-kpi-sub">ค่าเฉลี่ย</div>
              </div>
              <div class="t3-kpi">
                <div class="t3-kpi-label">ภูมิภาคนำ</div>
                <div class="t3-kpi-val" style="font-size:1.1rem;">{best_r}</div>
                <div class="t3-kpi-sub">ยอดขายสูงสุด</div>
              </div>
              <div class="t3-kpi">
                <div class="t3-kpi-label">สินค้าอันดับ 1</div>
                <div class="t3-kpi-val" style="font-size:1rem;">{best_p}</div>
                <div class="t3-kpi-sub">ขายดีที่สุด</div>
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # 3-column tables ขนาดไม่เท่ากัน
        tc1, tc2, tc3 = st.columns([2.2, 1.4, 1.4], gap="medium")
        with tc1:
            st.markdown('<div class="t3-tbl"><div class="t3-tbl-head"><span>ยอดขายรายเดือน</span></div>', unsafe_allow_html=True)
            st.table(monthly.rename(columns={"Month":"เดือน","Total_Sales":"ยอดขาย (฿)"}))
            st.markdown('</div>', unsafe_allow_html=True)
        with tc2:
            st.markdown('<div class="t3-tbl"><div class="t3-tbl-head"><span>Top 5 สินค้า</span></div>', unsafe_allow_html=True)
            st.table(top5.rename(columns={"Product Name":"สินค้า","Quantity":"จำนวน"}))
            st.markdown('</div>', unsafe_allow_html=True)
        with tc3:
            st.markdown('<div class="t3-tbl"><div class="t3-tbl-head"><span>ตามภูมิภาค</span></div>', unsafe_allow_html=True)
            st.table(region.rename(columns={"Region":"ภูมิภาค","Total_Sales":"ยอดขาย (฿)"}))
            st.markdown('</div>', unsafe_allow_html=True)

        st.success(f"**ข้อเสนอแนะ** — ทำโปรโมชั่น **{best_p}** · เพิ่มงบในภูมิภาค **{best_r}** · เตรียมสต็อกล่วงหน้า 1 เดือน")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — ความปลอดภัย
# layout: Full-bleed RBAC header + 2-panel security grid ด้านล่าง
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div style="font-size:1.2rem;font-weight:800;letter-spacing:-.025em;color:var(--t1);margin-bottom:.3rem;">ออกแบบความปลอดภัยข้อมูล</div>
    <div style="font-size:.76rem;color:var(--t3);margin-bottom:1.4rem;">RBAC · Technical Controls · PDPA Compliance</div>

    <div class="t4-rbac">
      <div class="t4-rbac-header">
        <span style="font-size:14px;">🔐</span>
        <span class="t4-rbac-header-txt">Role-Based Access Control (RBAC)</span>
        <span class="pill p-blue" style="margin-left:auto">3 Roles</span>
      </div>
      <div class="t4-role">
        <div class="t4-role-av" style="background:#FEE2E2;">🔐</div>
        <div style="flex:1">
          <div class="t4-role-name">Admin <span style="font-size:.7rem;font-weight:400;color:var(--t3)">(ไอที)</span></div>
          <div class="t4-role-perm">ดู · เพิ่ม · แก้ไข · ลบ · จัดการผู้ใช้</div>
        </div>
        <span class="pill p-red">สูงสุด</span>
      </div>
      <div class="t4-role">
        <div class="t4-role-av" style="background:#DBEAFE;">📊</div>
        <div style="flex:1">
          <div class="t4-role-name">Analyst <span style="font-size:.7rem;font-weight:400;color:var(--t3)">(นักวิเคราะห์)</span></div>
          <div class="t4-role-perm">ดู · ทำความสะอาด · วิเคราะห์</div>
        </div>
        <span class="pill p-blue">กลาง</span>
      </div>
      <div class="t4-role">
        <div class="t4-role-av" style="background:#D1FAE5;">👁</div>
        <div style="flex:1">
          <div class="t4-role-name">Viewer <span style="font-size:.7rem;font-weight:400;color:var(--t3)">(ผู้บริหาร)</span></div>
          <div class="t4-role-perm">ดูรายงานและ Dashboard เท่านั้น</div>
        </div>
        <span class="pill p-green">ต่ำ</span>
      </div>
    </div>

    <div class="t4-sec-row">
      <div class="t4-sec-panel">
        <div class="t4-sec-panel-head tech">🔧 &nbsp;มาตรการเชิงเทคนิค</div>
        <div class="t4-sec-item">
          <div class="t4-ic">🔒</div>
          <div><div class="sl">Encryption AES-256</div><div class="sd">เข้ารหัสข้อมูลขณะจัดเก็บและส่ง</div></div>
        </div>
        <div class="t4-sec-item">
          <div class="t4-ic">📱</div>
          <div><div class="sl">MFA (TOTP/SMS)</div><div class="sd">ยืนยันตัวตน 2 ชั้นทุก session</div></div>
        </div>
        <div class="t4-sec-item">
          <div class="t4-ic">📋</div>
          <div><div class="sl">Audit Logs</div><div class="sd">บันทึกทุก action + timestamp + IP</div></div>
        </div>
      </div>
      <div class="t4-sec-panel">
        <div class="t4-sec-panel-head mgmt">📋 &nbsp;มาตรการเชิงบริหาร</div>
        <div class="t4-sec-item">
          <div class="t4-ic g">📝</div>
          <div><div class="sl">NDA Agreement</div><div class="sd">สัญญาไม่เปิดเผยข้อมูลพนักงานทุกคน</div></div>
        </div>
        <div class="t4-sec-item">
          <div class="t4-ic g">🏛</div>
          <div><div class="sl">PDPA Compliance</div><div class="sd">สอดคล้อง พ.ร.บ. คุ้มครองข้อมูลฯ</div></div>
        </div>
        <div class="t4-sec-item">
          <div class="t4-ic g">🎓</div>
          <div><div class="sl">Security Training</div><div class="sd">อบรม Cyber Awareness รายปี</div></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.success("✓ สอดคล้องกับ ISO/IEC 27001 · PDPA · NIST Cybersecurity Framework")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — Visualization
# layout: Asymmetric grid — กราฟใหญ่ซ้าย (2/3) + กราฟย่อยขวา (1/3)
#         + กราฟ horizontal bar เต็มความกว้าง
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    if 'df_clean' not in st.session_state:
        st.markdown('<div class="empty-state"><div class="empty-icon">📊</div><div class="empty-title">ยังไม่มีข้อมูลที่พร้อมแสดงผล</div><div class="empty-desc">ไปที่แท็บ "ทำความสะอาด" แล้วกดเริ่มก่อน</div></div>', unsafe_allow_html=True)
    else:
        data = st.session_state['df_clean'].copy()
        data['Total_Sales'] = pd.to_numeric(data['Quantity'], errors='coerce') * pd.to_numeric(data['Unit Price'], errors='coerce')
        data['Month'] = data['Date'].dt.to_period('M').astype(str)
        monthly_trend = data.groupby('Month')['Total_Sales'].sum().reset_index()
        region_comp   = data.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False).reset_index()
        top5_prod     = data.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False).head(5).reset_index()

        # Asymmetric: 3 : 2
        vc1, vc2 = st.columns([3, 2], gap="large")

        with vc1:
            st.markdown('<div class="t5-card"><div class="t5-card-label"><span class="t5-dot"></span>แนวโน้มยอดขายรายเดือน</div>', unsafe_allow_html=True)
            fig1, ax1 = plt.subplots(figsize=(7, 3.6))
            x = range(len(monthly_trend))
            ax1.plot(x, monthly_trend['Total_Sales'],
                     color=PALETTE[0], linewidth=2.5, marker='o',
                     markersize=6, markerfacecolor=BG_C,
                     markeredgewidth=2.5, markeredgecolor=PALETTE[0], zorder=5)
            ax1.fill_between(x, monthly_trend['Total_Sales'], alpha=0.1, color=PALETTE[0])
            ax1.set_xticks(x)
            ax1.set_xticklabels(monthly_trend['Month'], rotation=30, ha='right', fontsize=8)
            ax1.set_title("Monthly Sales Trend", loc='left', color='#0F2167')
            ax1.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"฿{v/1000:.0f}K"))
            plt.tight_layout(pad=1.2)
            st.pyplot(fig1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with vc2:
            st.markdown('<div class="t5-card"><div class="t5-card-label"><span class="t5-dot" style="background:var(--green)"></span>ยอดขายตามภูมิภาค</div>', unsafe_allow_html=True)
            fig2, ax2 = plt.subplots(figsize=(4.5, 3.6))
            colors = [PALETTE[1]] + [PALETTE[0]] * (len(region_comp)-1)
            bars = ax2.bar(region_comp['Region'], region_comp['Total_Sales'],
                           color=colors, width=0.5, zorder=3, edgecolor=BG_C, linewidth=1)
            ax2.set_title("By Region", loc='left', color='#0F2167')
            ax2.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"฿{v/1000:.0f}K"))
            for b in bars:
                ax2.text(b.get_x() + b.get_width()/2, b.get_height()*1.03,
                         f"฿{b.get_height()/1000:.0f}K", ha='center', va='bottom',
                         fontsize=8, color='#1E40AF', fontweight='700')
            plt.tight_layout(pad=1.2)
            st.pyplot(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Full-width horizontal bar
        st.markdown('<div class="t5-card" style="margin-top:.8rem;"><div class="t5-card-label"><span class="t5-dot" style="background:var(--amber)"></span>สินค้าขายดี Top 5</div>', unsafe_allow_html=True)
        fig3, ax3 = plt.subplots(figsize=(12, 2.6))
        c3 = [PALETTE[2]] + [PALETTE[0]] * (len(top5_prod)-1)
        bars3 = ax3.barh(top5_prod['Product Name'][::-1], top5_prod['Quantity'][::-1],
                         color=c3[::-1], height=0.44, zorder=3, edgecolor=BG_C)
        ax3.set_title("Top 5 Products by Quantity Sold", loc='left', color='#0F2167')
        for b in bars3:
            ax3.text(b.get_width() + 0.25, b.get_y() + b.get_height()/2,
                     f"{b.get_width():.0f} ชิ้น", va='center', fontsize=9, color='#1E40AF', fontweight='700')
        plt.tight_layout(pad=1.2)
        st.pyplot(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        best_r = region_comp.iloc[0]['Region']
        best_p = top5_prod.iloc[0]['Product Name']
        st.success(f"**Executive Summary** — ภูมิภาคหลัก: **{best_r}** · สินค้าอันดับ 1: **{best_p}** · เตรียมสต็อกล่วงหน้าตาม Peak Month")
