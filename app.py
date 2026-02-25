import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

st.set_page_config(page_title="DataFlow · Sales", layout="wide", page_icon="📊",
                   initial_sidebar_state="expanded")

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — Linear.app Dark Sidebar Layout
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:        #0D1117;
    --surface:   #13181F;
    --surface-2: #1A2130;
    --surface-3: #222C3C;
    --border:    #263044;
    --border-2:  #334060;

    --sidebar-bg: #0D1117;
    --sidebar-w:  260px;

    --txt1:      #E2E8F5;
    --txt2:      #7F8FAD;
    --txt3:      #4D5C7A;

    --blue:      #5B7CF8;
    --blue-lt:   #1A2550;
    --blue-dk:   #4A68E8;
    --blue-glow: rgba(91,124,248,.3);
    --blue-sel:  #1E2E5A;

    --green:     #22C55E;
    --green-lt:  #0A2218;
    --amber:     #F59E0B;
    --amber-lt:  #271C05;
    --red:       #EF4444;
    --red-lt:    #260A0A;
    --purple:    #A855F7;
    --purple-lt: #1A0E2E;

    --r4: 5px; --r6: 6px; --r8: 8px; --r12: 12px; --r16: 16px;
    --sh:  0 1px 3px rgba(0,0,0,.5), 0 2px 8px rgba(0,0,0,.4);
    --sh2: 0 4px 24px rgba(0,0,0,.6);
}

*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box;
    color-scheme: dark;
}

.stApp { background: var(--bg) !important; color: var(--txt1) !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ══════════════════════════════════════
   SIDEBAR OVERRIDES — Linear style
══════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: 1px solid var(--border) !important;
    width: var(--sidebar-w) !important;
    min-width: var(--sidebar-w) !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
    background: var(--sidebar-bg) !important;
}
[data-testid="stSidebarContent"] {
    background: var(--sidebar-bg) !important;
    padding: 0 !important;
}
/* Collapse button */
[data-testid="collapsedControl"] {
    color: var(--txt2) !important;
}
button[kind="headerNoBorder"] {
    color: var(--txt2) !important;
}

/* ── Sidebar Brand ── */
.sb-brand {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 16px 14px 12px 14px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 4px;
}
.sb-mark {
    width: 28px; height: 28px;
    background: var(--blue);
    border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 800; color: #fff;
    letter-spacing: -0.5px;
    flex-shrink: 0;
    box-shadow: 0 0 12px var(--blue-glow);
}
.sb-brand-name { font-size: 0.84rem; font-weight: 700; color: var(--txt1); letter-spacing: -0.02em; }
.sb-brand-sub  { font-size: 0.66rem; color: var(--txt3); margin-top: 1px; }

/* ── Sidebar Section label ── */
.sb-section {
    font-size: 0.6rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--txt3);
    padding: 10px 14px 5px 14px;
}

/* ── Sidebar Nav Item ── */
.sb-item {
    display: flex; align-items: center; gap: 9px;
    padding: 6px 14px;
    border-radius: 0;
    cursor: pointer;
    font-size: 0.8rem;
    font-weight: 400;
    color: var(--txt2);
    transition: all 0.1s;
    position: relative;
    margin: 1px 0;
}
.sb-item:hover { background: var(--surface-2); color: var(--txt1); }
.sb-item.active {
    background: var(--blue-sel);
    color: var(--txt1);
    font-weight: 500;
}
.sb-item.active::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 2px;
    background: var(--blue);
    border-radius: 0 2px 2px 0;
}
.sb-item-ic {
    width: 18px; height: 18px;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; flex-shrink: 0;
    opacity: 0.7;
}
.sb-item.active .sb-item-ic { opacity: 1; }

/* ── Sidebar Stats ── */
.sb-stats {
    margin: 12px 10px 0 10px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--r8);
    padding: 10px 12px;
}
.sb-stat-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 4px 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.73rem;
}
.sb-stat-row:last-child { border-bottom: none; }
.sb-stat-label { color: var(--txt3); }
.sb-stat-val   { color: var(--txt1); font-weight: 600; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; }

/* ── Sidebar Divider ── */
.sb-divider {
    height: 1px; background: var(--border);
    margin: 8px 0;
}

/* ══════════════════════════════════════
   MAIN CONTENT AREA
══════════════════════════════════════ */
.block-container {
    padding: 0 2rem 3rem 2rem !important;
    max-width: 100% !important;
}

/* ── Page header ── */
.ph {
    display: flex; align-items: center; gap: 14px;
    padding: 1.6rem 0 1.2rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.6rem;
}
.ph-icon {
    width: 40px; height: 40px; border-radius: 10px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; font-size: 17px;
    border: 1px solid var(--border);
}
.ph-title { font-size: 1.1rem; font-weight: 700; letter-spacing: -0.025em; margin: 0; color: var(--txt1); line-height: 1.2; }
.ph-desc  { font-size: 0.73rem; color: var(--txt3); margin: 3px 0 0 0; }
.ph-badge {
    margin-left: auto;
    font-size: 0.65rem; font-weight: 600; letter-spacing: 0.04em;
    background: var(--surface-2); border: 1px solid var(--border);
    border-radius: 99px; padding: 3px 10px; color: var(--txt2);
}

/* ── Cards ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r12);
    padding: 1.2rem 1.4rem;
    box-shadow: var(--sh);
    margin-bottom: 1rem;
}
.ct {
    font-size: 0.67rem; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; color: var(--txt3);
    margin-bottom: 0.8rem; padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; gap: 6px;
}
.ct-dot { width: 5px; height: 5px; border-radius: 50%; background: var(--blue); display: inline-block; flex-shrink: 0; }

/* ── Pill tags ── */
.pill {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 2px 8px; border-radius: 99px;
    font-size: 0.66rem; font-weight: 600; letter-spacing: 0.02em;
    border: 1px solid transparent;
}
.p-blue   { background: var(--blue-lt);   color: #7B9EFF;  border-color: #2A3A6A; }
.p-green  { background: var(--green-lt);  color: #4ADE80;  border-color: #153A22; }
.p-amber  { background: var(--amber-lt);  color: #FCD34D;  border-color: #3D2C0A; }
.p-red    { background: var(--red-lt);    color: #FC8181;  border-color: #3D1010; }

/* ── Workflow steps ── */
.wf-step {
    display: flex; align-items: flex-start; gap: 12px;
    padding: 0.75rem 0; border-bottom: 1px solid var(--border);
}
.wf-step:last-child { border-bottom: none; }
.wf-num {
    width: 24px; height: 24px; border-radius: 50%; flex-shrink: 0;
    background: var(--blue); color: #fff;
    font-size: 0.66rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    margin-top: 1px;
    box-shadow: 0 0 8px var(--blue-glow);
}
.wf-title { font-size: 0.82rem; font-weight: 600; color: var(--txt1); }
.wf-desc  { font-size: 0.73rem; color: var(--txt2); margin-top: 2px; line-height: 1.5; }

/* ── Role rows ── */
.role-row {
    display: flex; align-items: center; gap: 10px;
    padding: 0.7rem 0.4rem; border-radius: var(--r6);
    border-bottom: 1px solid var(--border);
    transition: background 0.1s;
}
.role-row:last-child { border-bottom: none; }
.role-row:hover { background: var(--surface-2); }
.role-av {
    width: 32px; height: 32px; border-radius: 8px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; font-size: 14px;
    border: 1px solid var(--border);
}
.rn { font-size: 0.8rem; font-weight: 600; color: var(--txt1); line-height: 1.2; }
.rp { font-size: 0.71rem; color: var(--txt2); }

/* ── Security grid ── */
.sec-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 4px; }
.sec-panel {
    background: var(--surface-2); border: 1px solid var(--border);
    border-radius: var(--r8); padding: 0.85rem 0.95rem;
}
.sec-panel-title {
    font-size: 0.62rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.08em; color: var(--txt3); margin-bottom: 8px;
}
.sec-item { display: flex; align-items: flex-start; gap: 8px; padding: 5px 0; border-bottom: 1px solid var(--border); }
.sec-item:last-child { border-bottom: none; }
.sec-ic { width: 22px; height: 22px; border-radius: 5px; background: var(--blue-lt); color: #7B9EFF; display: flex; align-items: center; justify-content: center; font-size: 10px; flex-shrink: 0; margin-top: 1px; }
.sl { font-size: 0.78rem; font-weight: 600; color: var(--txt1); }
.sd { font-size: 0.7rem; color: var(--txt2); margin-top: 1px; line-height: 1.4; }

/* ── Empty state ── */
.empty-state {
    text-align: center; padding: 4rem 2rem;
    background: var(--surface); border: 1.5px dashed var(--border-2);
    border-radius: var(--r16); margin: 1.5rem 0;
}
.empty-icon  { font-size: 2.5rem; margin-bottom: 0.6rem; opacity: 0.5; }
.empty-title { font-size: 0.88rem; font-weight: 600; color: var(--txt2); }
.empty-desc  { font-size: 0.73rem; color: var(--txt3); margin-top: 4px; }

/* ══ Streamlit component overrides ══ */
[data-testid="stMetric"] {
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-radius: var(--r12) !important; padding: 1rem 1.2rem !important;
    box-shadow: var(--sh) !important;
}
[data-testid="stMetricLabel"] { font-size: 0.64rem !important; text-transform: uppercase !important; letter-spacing: 0.09em !important; font-weight: 700 !important; color: var(--txt3) !important; }
[data-testid="stMetricValue"] { font-size: 1.55rem !important; font-weight: 700 !important; letter-spacing: -0.04em !important; color: var(--txt1) !important; }

.stButton > button {
    background: var(--blue) !important; color: #fff !important;
    border: none !important; border-radius: var(--r6) !important;
    padding: 0.44rem 1.1rem !important; font-size: 0.79rem !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 3px rgba(91,124,248,.4), 0 0 0 1px rgba(91,124,248,.15) !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover { background: var(--blue-dk) !important; box-shadow: 0 3px 14px rgba(91,124,248,.55) !important; transform: translateY(-1px) !important; }

.stSuccess { background: var(--green-lt) !important; border: 1px solid #153A22 !important; border-left: 3px solid var(--green) !important; border-radius: var(--r8) !important; font-size: 0.8rem !important; color: #4ADE80 !important; }
.stInfo    { background: var(--blue-lt)  !important; border: 1px solid #2A3A6A !important; border-left: 3px solid var(--blue)  !important; border-radius: var(--r8) !important; font-size: 0.8rem !important; color: #7B9EFF !important; }
.stWarning { background: var(--amber-lt) !important; border: 1px solid #3D2C0A !important; border-left: 3px solid var(--amber) !important; border-radius: var(--r8) !important; font-size: 0.8rem !important; color: #FCD34D !important; }
.stError   { background: var(--red-lt)   !important; border: 1px solid #3D1010 !important; border-left: 3px solid var(--red)   !important; border-radius: var(--r8) !important; font-size: 0.8rem !important; color: #FC8181 !important; }

details { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: var(--r8) !important; }
summary  { font-size: 0.8rem !important; font-weight: 600 !important; color: var(--txt2) !important; }
hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }

.stTextInput input, .stNumberInput input {
    background: var(--surface-2) !important; border: 1px solid var(--border-2) !important;
    border-radius: var(--r4) !important; font-size: 0.81rem !important; color: var(--txt1) !important;
}
.stTextInput input:focus, .stNumberInput input:focus { border-color: var(--blue) !important; box-shadow: 0 0 0 3px rgba(91,124,248,.15) !important; }
.stSelectbox > div > div, .stDateInput > div > div {
    background: var(--surface-2) !important; border: 1px solid var(--border-2) !important;
    border-radius: var(--r4) !important; color: var(--txt1) !important;
}
label { color: var(--txt2) !important; font-size: 0.76rem !important; }

[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: var(--r8) !important; overflow: hidden !important; }
[data-testid="stTable"] table, .stDataFrame table { font-size: 0.78rem; border-collapse: collapse; width: 100%; }
[data-testid="stTable"] thead th, .stDataFrame thead th {
    background: var(--surface-2) !important; color: var(--txt3) !important;
    font-size: 0.64rem !important; font-weight: 700 !important; text-transform: uppercase !important;
    letter-spacing: 0.09em !important; padding: 0.55rem 0.85rem !important;
    border-bottom: 1px solid var(--border-2) !important;
}
[data-testid="stTable"] tbody td, .stDataFrame tbody td {
    padding: 0.5rem 0.85rem !important; border-bottom: 1px solid var(--border) !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.74rem !important;
    color: var(--txt1) !important; background: var(--surface) !important;
}
[data-testid="stTable"] tbody tr:hover td, .stDataFrame tbody tr:hover td { background: var(--surface-2) !important; }

/* Remove Streamlit's default tab navigation */
.stTabs [data-baseweb="tab-list"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Matplotlib ─────────────────────────────────────────────────────────────────
PALETTE = ["#5B7CF8", "#22C55E", "#F59E0B", "#EF4444", "#A855F7", "#06B6D4"]
BG_C = "#13181F"
mpl.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Inter", "Helvetica Neue", "Arial"],
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False, "axes.spines.bottom": False,
    "axes.grid": True, "grid.color": "#263044", "grid.linewidth": 0.7,
    "axes.facecolor": BG_C, "figure.facecolor": BG_C,
    "axes.labelcolor": "#4D5C7A", "xtick.color": "#4D5C7A", "ytick.color": "#4D5C7A",
    "xtick.labelsize": 9, "ytick.labelsize": 9,
    "axes.titlesize": 11, "axes.titleweight": "700", "axes.titlepad": 14,
    "axes.titlecolor": "#E2E8F5",
    "figure.dpi": 140,
    "text.color": "#7F8FAD",
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

total_sales = (pd.to_numeric(df['Quantity'],  errors='coerce').fillna(0) *
               pd.to_numeric(df['Unit Price'], errors='coerce').fillna(0)).sum()
n_products  = df['Product Name'].nunique() if 'Product Name' in df.columns else 0

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Linear-style nav panel
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div class="sb-brand">
      <div class="sb-mark">DF</div>
      <div>
        <div class="sb-brand-name">DataFlow</div>
        <div class="sb-brand-sub">Sales Analytics</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation state
    if 'page' not in st.session_state:
        st.session_state['page'] = 0

    pages = [
        (0,  "⊞",  "จัดการข้อมูล",       "#1C2B4A"),
        (1,  "⊙",  "ตรวจสอบคุณภาพ",       "#0A2218"),
        (2,  "⊘",  "ทำความสะอาด",         "#271C05"),
        (3,  "⊛",  "วิเคราะห์",           "#1A0E2E"),
        (4,  "⊜",  "ความปลอดภัย",         "#260A0A"),
        (5,  "⊝",  "Visualization",        "#1C2B4A"),
    ]

    st.markdown('<div class="sb-section">Workspace</div>', unsafe_allow_html=True)

    for idx, icon, label, _ in pages:
        active_cls = "active" if st.session_state['page'] == idx else ""
        if st.button(f"{icon}  {label}", key=f"nav_{idx}", use_container_width=True):
            st.session_state['page'] = idx
            st.rerun()

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-section">Overview</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sb-stats">
      <div class="sb-stat-row">
        <span class="sb-stat-label">รายการทั้งหมด</span>
        <span class="sb-stat-val">{len(df):,}</span>
      </div>
      <div class="sb-stat-row">
        <span class="sb-stat-label">ยอดขายรวม</span>
        <span class="sb-stat-val">฿{total_sales/1000:.0f}K</span>
      </div>
      <div class="sb-stat-row">
        <span class="sb-stat-label">สินค้า</span>
        <span class="sb-stat-val">{n_products}</span>
      </div>
      <div class="sb-stat-row">
        <span class="sb-stat-label">สถานะ</span>
        <span class="sb-stat-val" style="color:#4ADE80;">● Live</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# Override sidebar button styles so they look like nav items, not regular buttons
st.markdown("""
<style>
/* Sidebar nav button overrides */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: var(--txt2) !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 6px 14px !important;
    font-size: 0.79rem !important;
    font-weight: 400 !important;
    text-align: left !important;
    justify-content: flex-start !important;
    box-shadow: none !important;
    width: 100% !important;
    transition: all 0.1s !important;
    margin: 1px 0 !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--surface-2) !important;
    color: var(--txt1) !important;
    transform: none !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:active,
[data-testid="stSidebar"] .stButton > button:focus {
    background: var(--blue-sel) !important;
    color: var(--txt1) !important;
    box-shadow: none !important;
    outline: none !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT — route by page
# ══════════════════════════════════════════════════════════════════════════════
page = st.session_state.get('page', 0)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 0 — จัดการข้อมูล
# ─────────────────────────────────────────────────────────────────────────────
if page == 0:
    st.markdown("""
    <div class="ph">
      <div class="ph-icon" style="background:#1A2550;border-color:#2A3F6A;">⊞</div>
      <div>
        <div class="ph-title">จัดการฐานข้อมูล</div>
        <div class="ph-desc">เพิ่ม · ลบ รายการยอดขายในระบบ</div>
      </div>
      <span class="ph-badge">Data Management</span>
    </div>""", unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2], gap="large")

    with col_a:
        st.markdown('<div class="card"><div class="ct"><span class="ct-dot"></span>เพิ่มรายการใหม่</div>', unsafe_allow_html=True)
        with st.form("add_form", clear_on_submit=True):
            r1, r2 = st.columns(3), st.columns(3)
            new_date  = r1[0].date_input("วันที่ขาย")
            new_id    = r1[1].text_input("รหัสสินค้า", placeholder="P001")
            new_name  = r1[2].text_input("ชื่อสินค้า",  placeholder="Laptop")
            new_cat   = r2[0].selectbox("หมวดหมู่",   ["IT","Furniture","Electronics"])
            new_qty   = r2[1].number_input("จำนวน",    min_value=1, value=1)
            new_price = r2[2].number_input("ราคา/หน่วย", min_value=1, value=100)
            new_reg   = st.selectbox("ภูมิภาค", ["North","South","Central","East","West"])
            if st.form_submit_button("＋  บันทึกข้อมูล", use_container_width=True):
                new_row = pd.DataFrame([[str(new_date), new_id, new_name, new_cat, new_qty, new_price, new_reg]], columns=df.columns)
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv('sales_data.csv', index=False)
                st.success(f"✓ เพิ่ม **{new_name}** สำเร็จ")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="card"><div class="ct"><span class="ct-dot" style="background:var(--red)"></span>ลบรายการ</div>', unsafe_allow_html=True)
        st.dataframe(
            df[['Product Name','Quantity','Unit Price','Region']].reset_index().rename(columns={"index":"#"}),
            use_container_width=True, height=190
        )
        del_idx = st.number_input("เลือกเลขลำดับ (#) ที่ต้องการลบ", min_value=0, max_value=max(len(df)-1,0), step=1)
        preview = df.iloc[del_idx]['Product Name'] if len(df) > 0 else "—"
        st.markdown(f'<div style="background:var(--red-lt);border:1px solid #3D1010;border-radius:7px;padding:7px 11px;font-size:0.75rem;color:#FC8181;margin:4px 0 8px 0;">⚠ จะลบ: <strong>{preview}</strong> (แถว #{del_idx})</div>', unsafe_allow_html=True)
        if st.button("🗑  ยืนยันการลบ", use_container_width=True):
            df = df.drop(df.index[del_idx]).reset_index(drop=True)
            df.to_csv('sales_data.csv', index=False)
            st.warning("ลบแล้ว")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ct"><span class="ct-dot"></span>ข้อมูลทั้งหมดในระบบ</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 — ตรวจสอบคุณภาพ
# ─────────────────────────────────────────────────────────────────────────────
elif page == 1:
    st.markdown("""
    <div class="ph">
      <div class="ph-icon" style="background:#0A2218;border-color:#153A22;">⊙</div>
      <div>
        <div class="ph-title">ตรวจสอบคุณภาพข้อมูล</div>
        <div class="ph-desc">สแกนหา Missing Values · Duplicates · ชนิดข้อมูล</div>
      </div>
      <span class="ph-badge">Quality Check</span>
    </div>""", unsafe_allow_html=True)

    null_rows = df[df.isnull().any(axis=1)]
    dup_rows  = df[df.duplicated(keep=False)]
    n_null    = len(null_rows)
    n_dup     = len(df[df.duplicated()])
    score     = max(0, min(100, 100 - (n_null + n_dup) * 5))

    kc1, kc2, kc3, kc4 = st.columns(4)
    kc1.metric("แถวทั้งหมด",        f"{len(df):,}")
    kc2.metric("Missing Values",     f"{n_null}",  delta="ปกติ" if n_null == 0 else f"⚠ {n_null} แถว")
    kc3.metric("Duplicates",         f"{n_dup}",   delta="ปกติ" if n_dup  == 0 else f"⚠ {n_dup} รายการ")
    kc4.metric("Data Quality Score", f"{score}/100")

    st.markdown("---")
    if st.button("▶  เริ่มตรวจสอบ"):
        q1, q2 = st.columns(2, gap="large")
        with q1:
            st.markdown('<div class="ct"><span class="ct-dot"></span>Missing Values</div>', unsafe_allow_html=True)
            if null_rows.empty: st.success("✓ ข้อมูลครบถ้วนทุกแถว")
            else: st.error(f"พบ {n_null} แถวที่ขาดข้อมูล"); st.dataframe(null_rows, use_container_width=True)
        with q2:
            st.markdown('<div class="ct"><span class="ct-dot" style="background:var(--amber)"></span>Duplicates</div>', unsafe_allow_html=True)
            if dup_rows.empty: st.success("✓ ไม่พบข้อมูลซ้ำ")
            else: st.warning(f"พบ {n_dup} รายการซ้ำ"); st.dataframe(dup_rows.sort_values(by=list(df.columns)), use_container_width=True)

        st.markdown('<div class="ct" style="margin-top:1rem;"><span class="ct-dot" style="background:var(--purple)"></span>ชนิดข้อมูลรายคอลัมน์</div>', unsafe_allow_html=True)
        def check_type(v): return type(v).__name__
        st.dataframe(df.applymap(check_type), use_container_width=True)
        st.info("คอลัมน์ตัวเลขที่แสดงเป็น `str` = ชนิดข้อมูลผิดพลาด ควรแก้ไขก่อนวิเคราะห์")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 — ทำความสะอาด
# ─────────────────────────────────────────────────────────────────────────────
elif page == 2:
    st.markdown("""
    <div class="ph">
      <div class="ph-icon" style="background:#271C05;border-color:#3D2C0A;">⊘</div>
      <div>
        <div class="ph-title">ทำความสะอาดข้อมูล</div>
        <div class="ph-desc">ลบซ้ำ · กรองค่าผิดพลาด · แปลงรูปแบบวันที่</div>
      </div>
      <span class="ph-badge">Data Cleaning</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <div class="ct"><span class="ct-dot"></span>ขั้นตอน (Pipeline)</div>
      <div class="wf-step">
        <div class="wf-num">1</div>
        <div><div class="wf-title">Deduplication</div><div class="wf-desc">ตรวจจับและลบแถวที่มีข้อมูลซ้ำกันทุกฟิลด์</div></div>
      </div>
      <div class="wf-step">
        <div class="wf-num">2</div>
        <div><div class="wf-title">Outlier Filter</div><div class="wf-desc">ลบแถวที่ Quantity ≤ 0 หรือ Unit Price ≤ 0</div></div>
      </div>
      <div class="wf-step">
        <div class="wf-num">3</div>
        <div><div class="wf-title">Date Parsing</div><div class="wf-desc">แปลง Date → datetime64 และลบแถวที่ไม่สามารถแปลงได้</div></div>
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

        st.success(f"✓ ทำความสะอาดเสร็จสิ้น — ข้อมูลพร้อมใช้งาน **{len(df_c):,}** แถว")
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("เริ่มต้น",      f"{len(df_b):,} แถว")
        r2.metric("ลบซ้ำ",        f"−{len(dup_r)}")
        r3.metric("ลบค่าผิดพลาด", f"−{len(wrong_r)}")
        r4.metric("พร้อมใช้งาน",   f"{len(df_c):,} แถว")
        with st.expander("ดูรายละเอียดที่ถูกลบ"):
            if not dup_r.empty:   st.markdown("**ซ้ำ:**");    st.dataframe(dup_r,   use_container_width=True)
            if not wrong_r.empty: st.markdown("**ผิดพลาด:**"); st.dataframe(wrong_r, use_container_width=True)
            if not inv_d.empty:   st.markdown("**วันที่:**");  st.dataframe(inv_d,   use_container_width=True)
        st.markdown("**ข้อมูลพร้อมใช้งาน**")
        st.dataframe(df_c, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 — วิเคราะห์
# ─────────────────────────────────────────────────────────────────────────────
elif page == 3:
    st.markdown("""
    <div class="ph">
      <div class="ph-icon" style="background:#1A0E2E;border-color:#3B1F60;">⊛</div>
      <div>
        <div class="ph-title">วิเคราะห์ข้อมูลเชิงธุรกิจ</div>
        <div class="ph-desc">Monthly Trend · Top Products · Regional Performance</div>
      </div>
      <span class="ph-badge">Analytics</span>
    </div>""", unsafe_allow_html=True)

    if 'df_clean' not in st.session_state:
        st.markdown('<div class="empty-state"><div class="empty-icon">⊛</div><div class="empty-title">ยังไม่มีข้อมูลที่ผ่านการทำความสะอาด</div><div class="empty-desc">ไปที่เมนู "ทำความสะอาด" แล้วกดเริ่มก่อนนะครับ</div></div>', unsafe_allow_html=True)
    else:
        data = st.session_state['df_clean'].copy()
        data['Total_Sales'] = pd.to_numeric(data['Quantity'], errors='coerce') * pd.to_numeric(data['Unit Price'], errors='coerce')
        data['Month'] = data['Date'].dt.to_period('M').astype(str)
        monthly  = data.groupby('Month')['Total_Sales'].sum().reset_index()
        top5     = data.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False).head(5).reset_index()
        region   = data.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False).reset_index()
        best_r   = region.iloc[0]['Region']
        best_p   = top5.iloc[0]['Product Name']
        total    = data['Total_Sales'].sum()
        avg_mo   = monthly['Total_Sales'].mean()

        kc1, kc2, kc3, kc4 = st.columns(4)
        kc1.metric("ยอดขายรวม",         f"฿{total:,.0f}")
        kc2.metric("เฉลี่ย/เดือน",      f"฿{avg_mo:,.0f}")
        kc3.metric("ภูมิภาคนำ",          best_r)
        kc4.metric("สินค้าขายดีอันดับ 1", best_p)
        st.markdown("---")

        a1, a2, a3 = st.columns([2, 2, 2], gap="medium")
        with a1:
            st.markdown('<div class="ct"><span class="ct-dot"></span>ยอดขายรายเดือน</div>', unsafe_allow_html=True)
            st.table(monthly.rename(columns={"Month":"เดือน","Total_Sales":"ยอดขาย (฿)"}))
        with a2:
            st.markdown('<div class="ct"><span class="ct-dot" style="background:var(--green)"></span>สินค้าขายดี Top 5</div>', unsafe_allow_html=True)
            st.table(top5.rename(columns={"Product Name":"สินค้า","Quantity":"จำนวน"}))
        with a3:
            st.markdown('<div class="ct"><span class="ct-dot" style="background:var(--amber)"></span>ยอดขายตามภูมิภาค</div>', unsafe_allow_html=True)
            st.table(region.rename(columns={"Region":"ภูมิภาค","Total_Sales":"ยอดขาย (฿)"}))

        st.success(f"**ข้อเสนอแนะเชิงธุรกิจ** — ทำโปรโมชั่น **{best_p}** · เพิ่มงบในภูมิภาค **{best_r}** · เตรียมสต็อกล่วงหน้า 1 เดือน")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 4 — ความปลอดภัย
# ─────────────────────────────────────────────────────────────────────────────
elif page == 4:
    st.markdown("""
    <div class="ph">
      <div class="ph-icon" style="background:#260A0A;border-color:#3D1010;">⊜</div>
      <div>
        <div class="ph-title">ออกแบบความปลอดภัยข้อมูล</div>
        <div class="ph-desc">RBAC · Technical Controls · PDPA Compliance</div>
      </div>
      <span class="ph-badge">Security</span>
    </div>""", unsafe_allow_html=True)

    s1, s2 = st.columns([5, 7], gap="large")

    with s1:
        st.markdown("""
        <div class="card">
          <div class="ct"><span class="ct-dot" style="background:var(--red)"></span>Role-Based Access Control</div>
          <div class="role-row">
            <div class="role-av" style="background:#260A0A;border-color:#3D1010;">🔐</div>
            <div style="flex:1"><div class="rn">Admin (ไอที)</div><div class="rp">ดู · เพิ่ม · แก้ไข · ลบ · จัดการผู้ใช้</div></div>
            <span class="pill p-red">สูงสุด</span>
          </div>
          <div class="role-row">
            <div class="role-av" style="background:#1A2550;border-color:#2A3F6A;">📊</div>
            <div style="flex:1"><div class="rn">Analyst (นักวิเคราะห์)</div><div class="rp">ดู · ทำความสะอาด · วิเคราะห์</div></div>
            <span class="pill p-blue">กลาง</span>
          </div>
          <div class="role-row">
            <div class="role-av" style="background:#0A2218;border-color:#153A22;">👁</div>
            <div style="flex:1"><div class="rn">Viewer (ผู้บริหาร)</div><div class="rp">ดูรายงานและ Dashboard เท่านั้น</div></div>
            <span class="pill p-green">ต่ำ</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class="card">
          <div class="ct"><span class="ct-dot" style="background:var(--purple)"></span>มาตรการป้องกัน</div>
          <div class="sec-grid">
            <div class="sec-panel">
              <div class="sec-panel-title">🔧 เชิงเทคนิค</div>
              <div class="sec-item"><div class="sec-ic">🔒</div><div><div class="sl">Encryption AES-256</div><div class="sd">เข้ารหัสข้อมูลขณะจัดเก็บและส่ง</div></div></div>
              <div class="sec-item"><div class="sec-ic">📱</div><div><div class="sl">MFA (TOTP/SMS)</div><div class="sd">ยืนยันตัวตน 2 ชั้นทุก session</div></div></div>
              <div class="sec-item"><div class="sec-ic">📋</div><div><div class="sl">Audit Logs</div><div class="sd">บันทึกทุก action + timestamp + IP</div></div></div>
            </div>
            <div class="sec-panel">
              <div class="sec-panel-title">📋 เชิงบริหาร</div>
              <div class="sec-item"><div class="sec-ic" style="background:var(--green-lt);color:#4ADE80">📝</div><div><div class="sl">NDA Agreement</div><div class="sd">สัญญาไม่เปิดเผยข้อมูลพนักงานทุกคน</div></div></div>
              <div class="sec-item"><div class="sec-ic" style="background:var(--green-lt);color:#4ADE80">🏛</div><div><div class="sl">PDPA Compliance</div><div class="sd">สอดคล้อง พ.ร.บ. คุ้มครองข้อมูลฯ</div></div></div>
              <div class="sec-item"><div class="sec-ic" style="background:var(--green-lt);color:#4ADE80">🎓</div><div><div class="sl">Security Training</div><div class="sd">อบรม Cyber Awareness รายปี</div></div></div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.success("✓ มาตรฐานนี้สอดคล้องกับ ISO/IEC 27001 · PDPA · NIST Cybersecurity Framework")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 5 — Visualization
# ─────────────────────────────────────────────────────────────────────────────
elif page == 5:
    st.markdown("""
    <div class="ph">
      <div class="ph-icon" style="background:#1A2550;border-color:#2A3F6A;">⊝</div>
      <div>
        <div class="ph-title">Data Visualization</div>
        <div class="ph-desc">Monthly Trend · Regional Comparison · Top Products</div>
      </div>
      <span class="ph-badge">Charts</span>
    </div>""", unsafe_allow_html=True)

    if 'df_clean' not in st.session_state:
        st.markdown('<div class="empty-state"><div class="empty-icon">📊</div><div class="empty-title">ยังไม่มีข้อมูลที่พร้อมแสดงผล</div><div class="empty-desc">ไปที่เมนู "ทำความสะอาด" แล้วกดเริ่มก่อน</div></div>', unsafe_allow_html=True)
    else:
        data = st.session_state['df_clean'].copy()
        data['Total_Sales'] = pd.to_numeric(data['Quantity'], errors='coerce') * pd.to_numeric(data['Unit Price'], errors='coerce')
        data['Month'] = data['Date'].dt.to_period('M').astype(str)
        monthly_trend = data.groupby('Month')['Total_Sales'].sum().reset_index()
        region_comp   = data.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False).reset_index()
        top5_prod     = data.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False).head(5).reset_index()

        vc1, vc2 = st.columns(2, gap="large")

        with vc1:
            st.markdown('<div class="ct"><span class="ct-dot"></span>แนวโน้มยอดขายรายเดือน</div>', unsafe_allow_html=True)
            fig1, ax1 = plt.subplots(figsize=(5.8, 3.4))
            x = range(len(monthly_trend))
            ax1.plot(x, monthly_trend['Total_Sales'],
                     color=PALETTE[0], linewidth=2.4, marker='o',
                     markersize=6, markerfacecolor=BG_C, markeredgewidth=2.4, markeredgecolor=PALETTE[0], zorder=5)
            ax1.fill_between(x, monthly_trend['Total_Sales'], alpha=0.1, color=PALETTE[0])
            ax1.set_xticks(x)
            ax1.set_xticklabels(monthly_trend['Month'], rotation=30, ha='right', fontsize=8)
            ax1.set_title("Monthly Sales Trend", loc='left', color='#E2E8F5')
            ax1.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"฿{v/1000:.0f}K"))
            plt.tight_layout(pad=1.2)
            st.pyplot(fig1, use_container_width=True)

        with vc2:
            st.markdown('<div class="ct"><span class="ct-dot" style="background:var(--green)"></span>ยอดขายตามภูมิภาค</div>', unsafe_allow_html=True)
            fig2, ax2 = plt.subplots(figsize=(5.8, 3.4))
            colors = [PALETTE[1]] + [PALETTE[0]] * (len(region_comp)-1)
            bars = ax2.bar(region_comp['Region'], region_comp['Total_Sales'],
                           color=colors, width=0.48, zorder=3, edgecolor=BG_C, linewidth=1)
            ax2.set_title("Sales by Region", loc='left', color='#E2E8F5')
            ax2.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"฿{v/1000:.0f}K"))
            for b in bars:
                ax2.text(b.get_x() + b.get_width()/2, b.get_height()*1.03,
                         f"฿{b.get_height():,.0f}", ha='center', va='bottom', fontsize=7.5, color='#7F8FAD', fontweight='600')
            plt.tight_layout(pad=1.2)
            st.pyplot(fig2, use_container_width=True)

        st.markdown('<div class="ct" style="margin-top:0.5rem;"><span class="ct-dot" style="background:var(--amber)"></span>สินค้าขายดี Top 5</div>', unsafe_allow_html=True)
        fig3, ax3 = plt.subplots(figsize=(10, 2.8))
        c3 = [PALETTE[2]] + [PALETTE[0]] * (len(top5_prod)-1)
        bars3 = ax3.barh(top5_prod['Product Name'][::-1], top5_prod['Quantity'][::-1],
                         color=c3[::-1], height=0.46, zorder=3, edgecolor=BG_C)
        ax3.set_title("Top 5 Products by Quantity Sold", loc='left', color='#E2E8F5')
        for b in bars3:
            ax3.text(b.get_width() + 0.3, b.get_y() + b.get_height()/2,
                     f"{b.get_width():.0f} ชิ้น", va='center', fontsize=8.5, color='#7F8FAD', fontweight='600')
        plt.tight_layout(pad=1.2)
        st.pyplot(fig3, use_container_width=True)

        best_r = region_comp.iloc[0]['Region']
        best_p = top5_prod.iloc[0]['Product Name']
        st.success(f"**Executive Summary** — ภูมิภาคหลัก: **{best_r}** · สินค้าอันดับ 1: **{best_p}** · เตรียมสต็อกล่วงหน้าตาม Peak Month")