import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

st.set_page_config(
    page_title="DataFlow · Sales",
    layout="centered",
    page_icon="📊",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════════════════════
# CSS — Mobile-First Premium Dark App
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:         #07090F;
    --surface:    #0C1018;
    --surface-2:  #111827;
    --surface-3:  #162030;
    --border:     #1C2A3E;
    --border-2:   #253650;
    --border-hi:  #334870;

    --txt1:  #EDF2FF;
    --txt2:  #6B80A6;
    --txt3:  #384E6E;

    --blue:      #4B76FF;
    --blue-lt:   #0D1B40;
    --blue-dk:   #3660EE;
    --blue-glow: rgba(75,118,255,.4);
    --blue-sel:  #102040;

    --green:     #0FD584;
    --green-lt:  #061A10;

    --amber:     #FFA820;
    --amber-lt:  #1E1504;

    --red:       #FF4B68;
    --red-lt:    #1E0610;

    --purple:    #9860FF;
    --purple-lt: #110B24;

    --cyan:      #08C8D2;

    --nav-h: 68px;

    --r8:  8px; --r12: 12px; --r16: 16px; --r20: 20px; --r99: 99px;
    --sh: 0 2px 8px rgba(0,0,0,.55), 0 1px 2px rgba(0,0,0,.4);
    --sh2: 0 8px 32px rgba(0,0,0,.7);
}

/* ── Reset & Base ── */
*, html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    box-sizing: border-box;
    color-scheme: dark;
    -webkit-tap-highlight-color: transparent;
}

.stApp {
    background: var(--bg) !important;
    color: var(--txt1) !important;
    max-width: 480px;
    margin: 0 auto;
}

/* Ambient background */
.stApp::before {
    content: '';
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
        radial-gradient(ellipse 600px 400px at 80% 0%, rgba(75,118,255,.07) 0%, transparent 65%),
        radial-gradient(ellipse 400px 300px at 0% 100%, rgba(15,213,132,.04) 0%, transparent 60%);
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* ── Main container ── */
.block-container {
    padding: 0 16px calc(var(--nav-h) + 20px) 16px !important;
    max-width: 480px !important;
    margin: 0 auto !important;
    position: relative; z-index: 1;
}

/* ══════════════════════════════════════
   TOP APP BAR
══════════════════════════════════════ */
.topbar {
    position: sticky; top: 0; z-index: 100;
    background: rgba(7,9,15,0.92);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
    margin: 0 -16px 20px -16px;
    padding: 14px 16px;
    display: flex; align-items: center; gap: 10px;
}
.topbar-mark {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, var(--blue) 0%, var(--blue-dk) 100%);
    border-radius: 10px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Syne', sans-serif !important;
    font-size: 12px; font-weight: 800; color: #fff;
    box-shadow: 0 0 16px var(--blue-glow);
}
.topbar-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem; font-weight: 700; color: var(--txt1); letter-spacing: -0.02em;
}
.topbar-sub { font-size: 0.65rem; color: var(--txt3); margin-top: 1px; }
.topbar-badge {
    margin-left: auto; flex-shrink: 0;
    display: flex; align-items: center; gap: 5px;
    background: var(--surface-2); border: 1px solid var(--border-2);
    border-radius: var(--r99); padding: 5px 10px;
    font-size: 0.65rem; font-weight: 600; color: var(--txt2);
}
.online-dot {
    width: 6px; height: 6px; border-radius: 50%; background: var(--green);
    box-shadow: 0 0 6px var(--green); flex-shrink: 0;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}

/* ══════════════════════════════════════
   BOTTOM NAVIGATION BAR
══════════════════════════════════════ */
.bottom-nav {
    position: fixed; bottom: 0; left: 50%;
    transform: translateX(-50%);
    width: 100%; max-width: 480px;
    height: var(--nav-h);
    background: rgba(7,9,15,0.96);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border-top: 1px solid var(--border);
    display: grid; grid-template-columns: repeat(6, 1fr);
    z-index: 200;
    padding: 0 4px;
    box-shadow: 0 -8px 32px rgba(0,0,0,.6);
}
.nav-item {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    gap: 3px; cursor: pointer; padding: 6px 2px;
    border-radius: var(--r8);
    transition: background 0.15s;
    min-height: 48px;
    position: relative;
}
.nav-item:hover  { background: var(--surface-2); }
.nav-item.active { background: var(--blue-sel); }
.nav-item.active::before {
    content: '';
    position: absolute; top: 0; left: 20%; right: 20%; height: 2px;
    background: var(--blue);
    border-radius: 0 0 4px 4px;
    box-shadow: 0 0 8px var(--blue-glow);
}
.nav-ic {
    font-size: 18px; line-height: 1;
    filter: grayscale(0.6) opacity(0.5);
    transition: filter 0.15s;
}
.nav-item.active .nav-ic { filter: none; }
.nav-lbl {
    font-size: 0.55rem; font-weight: 600; letter-spacing: 0.02em;
    color: var(--txt3); text-align: center;
    transition: color 0.15s;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    max-width: 56px;
}
.nav-item.active .nav-lbl { color: #7AACFF; }

/* ══════════════════════════════════════
   PAGE HEADER
══════════════════════════════════════ */
.ph {
    display: flex; align-items: center; gap: 12px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
}
.ph-icon {
    width: 46px; height: 46px; border-radius: 14px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; font-size: 20px;
    border: 1px solid var(--border);
    background: var(--surface-2);
}
.ph-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.2rem; font-weight: 700; letter-spacing: -0.03em;
    color: var(--txt1); margin: 0; line-height: 1.2;
}
.ph-desc { font-size: 0.71rem; color: var(--txt3); margin: 3px 0 0 0; }

/* ══════════════════════════════════════
   KPI STAT CARDS — 2x2 grid on mobile
══════════════════════════════════════ */
.kpi-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 20px;
}
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r16);
    padding: 14px 14px 12px 14px;
    position: relative; overflow: hidden;
    box-shadow: var(--sh);
}
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    border-radius: 16px 16px 0 0;
}
.kpi-card.blue::before   { background: linear-gradient(90deg, var(--blue), var(--cyan)); }
.kpi-card.green::before  { background: linear-gradient(90deg, var(--green), #06C8D8); }
.kpi-card.amber::before  { background: linear-gradient(90deg, var(--amber), #FF8C20); }
.kpi-card.red::before    { background: linear-gradient(90deg, var(--red), var(--purple)); }
.kpi-card.purple::before { background: linear-gradient(90deg, var(--purple), var(--blue)); }
.kpi-card.cyan::before   { background: linear-gradient(90deg, var(--cyan), var(--green)); }
.kpi-label {
    font-size: 0.6rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: var(--txt3); margin-bottom: 6px;
}
.kpi-value {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.65rem; font-weight: 700; letter-spacing: -0.04em;
    color: var(--txt1); line-height: 1;
}
.kpi-value.sm { font-size: 1.1rem; }
.kpi-sub  { font-size: 0.65rem; color: var(--txt2); margin-top: 5px; }
.kpi-icon { position: absolute; right: 12px; top: 14px; font-size: 22px; opacity: 0.12; }

/* ══════════════════════════════════════
   CARDS
══════════════════════════════════════ */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r16);
    padding: 16px;
    box-shadow: var(--sh);
    margin-bottom: 12px;
    position: relative; overflow: hidden;
}
.ct {
    font-size: 0.62rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--txt3);
    margin-bottom: 12px; padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; gap: 7px;
}
.ct-dot {
    width: 5px; height: 5px; border-radius: 50%;
    background: var(--blue); flex-shrink: 0;
    box-shadow: 0 0 6px var(--blue-glow);
}

/* ══════════════════════════════════════
   SECTION LABEL
══════════════════════════════════════ */
.section-label {
    font-size: 0.6rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.12em; color: var(--txt3); margin: 18px 0 8px 2px;
    display: flex; align-items: center; gap: 8px;
}
.section-label::after {
    content: ''; flex: 1; height: 1px; background: var(--border);
}

/* ══════════════════════════════════════
   LIST ROWS (role / security items)
══════════════════════════════════════ */
.list-row {
    display: flex; align-items: center; gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid var(--border);
    transition: background 0.1s;
}
.list-row:last-child { border-bottom: none; }
.list-av {
    width: 40px; height: 40px; border-radius: 12px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; font-size: 18px;
    border: 1px solid var(--border); background: var(--surface-2);
}
.list-title { font-size: 0.85rem; font-weight: 600; color: var(--txt1); }
.list-sub   { font-size: 0.7rem; color: var(--txt3); margin-top: 2px; }

/* Pill tags */
.pill {
    display: inline-flex; align-items: center;
    padding: 4px 10px; border-radius: var(--r99);
    font-size: 0.64rem; font-weight: 700; letter-spacing: 0.04em;
    border: 1px solid transparent; flex-shrink: 0;
}
.p-blue   { background: var(--blue-lt);   color: #7AACFF; border-color: #1E3364; }
.p-green  { background: var(--green-lt);  color: #2EE89A; border-color: #0E3C24; }
.p-amber  { background: var(--amber-lt);  color: #FFCA50; border-color: #3D2E0A; }
.p-red    { background: var(--red-lt);    color: #FF8098; border-color: #3D1020; }
.p-purple { background: var(--purple-lt); color: #B899FF; border-color: #241448; }

/* ══════════════════════════════════════
   WORKFLOW STEPS
══════════════════════════════════════ */
.wf-step {
    display: flex; align-items: flex-start; gap: 14px;
    padding: 12px 0; border-bottom: 1px solid var(--border);
}
.wf-step:last-child { border-bottom: none; }
.wf-num {
    width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0;
    background: linear-gradient(135deg, var(--blue), var(--blue-dk));
    color: #fff; font-size: 0.7rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 0 12px var(--blue-glow);
    font-family: 'JetBrains Mono', monospace !important;
    border: 1px solid rgba(75,118,255,.35);
    flex-shrink: 0;
}
.wf-title { font-size: 0.88rem; font-weight: 600; color: var(--txt1); }
.wf-desc  { font-size: 0.73rem; color: var(--txt2); margin-top: 4px; line-height: 1.6; }

/* ══════════════════════════════════════
   SECURITY ITEMS
══════════════════════════════════════ */
.sec-item {
    display: flex; align-items: center; gap: 12px;
    padding: 11px 0; border-bottom: 1px solid var(--border);
}
.sec-item:last-child { border-bottom: none; }
.sec-ic {
    width: 36px; height: 36px; border-radius: 10px; flex-shrink: 0;
    background: var(--blue-lt); color: #7AACFF;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; border: 1px solid #1E3364;
}
.sec-title { font-size: 0.84rem; font-weight: 600; color: var(--txt1); }
.sec-desc  { font-size: 0.7rem; color: var(--txt3); margin-top: 2px; }

/* ══════════════════════════════════════
   EMPTY STATE
══════════════════════════════════════ */
.empty-state {
    text-align: center; padding: 56px 24px;
    background: var(--surface);
    border: 1px dashed var(--border-2);
    border-radius: var(--r20); margin: 8px 0;
}
.empty-icon  { font-size: 3.5rem; display: block; margin-bottom: 12px; opacity: 0.3; }
.empty-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem; font-weight: 700; color: var(--txt2);
}
.empty-desc { font-size: 0.74rem; color: var(--txt3); margin-top: 6px; line-height: 1.5; }
.empty-hint {
    display: inline-flex; align-items: center; gap: 6px;
    margin-top: 16px; background: var(--blue-lt);
    border: 1px solid #1E3364; border-radius: var(--r99);
    padding: 7px 14px; font-size: 0.72rem; color: #7AACFF; font-weight: 500;
}

/* ══════════════════════════════════════
   DELETE WARNING
══════════════════════════════════════ */
.del-warn {
    background: var(--red-lt); border: 1px solid #3D1020;
    border-left: 3px solid var(--red); border-radius: var(--r8);
    padding: 10px 14px; font-size: 0.78rem; color: #FF8098;
    margin: 8px 0 12px 0; display: flex; align-items: center; gap: 8px;
}

/* ══════════════════════════════════════
   STREAMLIT OVERRIDES — Mobile sizing
══════════════════════════════════════ */

/* Metrics */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r12) !important;
    padding: 14px 16px !important;
    box-shadow: var(--sh) !important;
    position: relative; overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--blue), var(--cyan));
    border-radius: 12px 12px 0 0;
}
[data-testid="stMetricLabel"] {
    font-size: 0.6rem !important; text-transform: uppercase !important;
    letter-spacing: 0.1em !important; font-weight: 700 !important; color: var(--txt3) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.5rem !important; font-weight: 700 !important;
    letter-spacing: -0.04em !important; color: var(--txt1) !important;
}

/* Buttons — large touch targets */
.stButton > button {
    background: linear-gradient(135deg, var(--blue) 0%, var(--blue-dk) 100%) !important;
    color: #fff !important; border: none !important;
    border-radius: var(--r12) !important;
    padding: 14px 20px !important; font-size: 0.9rem !important;
    font-weight: 600 !important; min-height: 52px !important;
    box-shadow: 0 4px 16px rgba(75,118,255,.4) !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    box-shadow: 0 6px 24px rgba(75,118,255,.6) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(1px) !important; box-shadow: none !important; }

/* Alerts */
.stSuccess {
    background: linear-gradient(135deg, var(--green-lt), rgba(6,26,16,.3)) !important;
    border: 1px solid #0E3C24 !important; border-left: 3px solid var(--green) !important;
    border-radius: var(--r12) !important; font-size: 0.82rem !important; color: #2EE89A !important;
}
.stInfo {
    background: linear-gradient(135deg, var(--blue-lt), rgba(13,27,64,.3)) !important;
    border: 1px solid #1E3364 !important; border-left: 3px solid var(--blue) !important;
    border-radius: var(--r12) !important; font-size: 0.82rem !important; color: #7AACFF !important;
}
.stWarning {
    background: linear-gradient(135deg, var(--amber-lt), rgba(30,21,4,.3)) !important;
    border: 1px solid #3D2E0A !important; border-left: 3px solid var(--amber) !important;
    border-radius: var(--r12) !important; font-size: 0.82rem !important; color: #FFCA50 !important;
}
.stError {
    background: linear-gradient(135deg, var(--red-lt), rgba(30,6,16,.3)) !important;
    border: 1px solid #3D1020 !important; border-left: 3px solid var(--red) !important;
    border-radius: var(--r12) !important; font-size: 0.82rem !important; color: #FF8098 !important;
}

/* Form inputs — large touch */
.stTextInput input, .stNumberInput input {
    background: var(--surface-2) !important; border: 1px solid var(--border-2) !important;
    border-radius: var(--r12) !important; font-size: 0.88rem !important; color: var(--txt1) !important;
    padding: 12px 14px !important; min-height: 48px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--blue) !important; box-shadow: 0 0 0 3px rgba(75,118,255,.14) !important;
}
.stSelectbox > div > div {
    background: var(--surface-2) !important; border: 1px solid var(--border-2) !important;
    border-radius: var(--r12) !important; color: var(--txt1) !important;
    min-height: 48px !important;
}
.stDateInput > div > div {
    background: var(--surface-2) !important; border: 1px solid var(--border-2) !important;
    border-radius: var(--r12) !important; min-height: 48px !important;
}
label {
    color: var(--txt2) !important; font-size: 0.78rem !important;
    font-weight: 500 !important; margin-bottom: 4px !important;
}

/* Expander */
details {
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-radius: var(--r12) !important;
}
summary {
    font-size: 0.85rem !important; font-weight: 600 !important;
    color: var(--txt2) !important; padding: 12px 16px !important;
}
hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }

/* Tables */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--r12) !important; overflow: hidden !important;
}
[data-testid="stTable"] table, .stDataFrame table { font-size: 0.76rem; width: 100%; border-collapse: collapse; }
[data-testid="stTable"] thead th, .stDataFrame thead th {
    background: var(--surface-2) !important; color: var(--txt3) !important;
    font-size: 0.6rem !important; font-weight: 700 !important; text-transform: uppercase !important;
    letter-spacing: 0.09em !important; padding: 10px 12px !important;
    border-bottom: 1px solid var(--border-2) !important;
}
[data-testid="stTable"] tbody td, .stDataFrame tbody td {
    padding: 10px 12px !important; border-bottom: 1px solid var(--border) !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.72rem !important;
    color: var(--txt1) !important; background: var(--surface) !important;
}
[data-testid="stTable"] tbody tr:hover td, .stDataFrame tbody tr:hover td {
    background: var(--surface-2) !important;
}

/* Remove tab UI */
.stTabs [data-baseweb="tab-list"]   { display: none !important; }
.stTabs [data-baseweb="tab-panel"]  { padding: 0 !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Matplotlib ─────────────────────────────────────────────────────────────────
PALETTE = ["#4B76FF", "#0FD584", "#FFA820", "#FF4B68", "#9860FF", "#08C8D2"]
BG_C = "#0C1018"
mpl.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["DM Sans", "Helvetica Neue", "Arial"],
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False, "axes.spines.bottom": False,
    "axes.grid": True, "grid.color": "#1C2A3E", "grid.linewidth": 0.6,
    "grid.linestyle": "--", "grid.alpha": 0.9,
    "axes.facecolor": BG_C, "figure.facecolor": BG_C,
    "axes.labelcolor": "#384E6E", "xtick.color": "#384E6E", "ytick.color": "#384E6E",
    "xtick.labelsize": 8, "ytick.labelsize": 8,
    "axes.titlesize": 10.5, "axes.titleweight": "600", "axes.titlepad": 12,
    "axes.titlecolor": "#EDF2FF",
    "figure.dpi": 160, "text.color": "#6B80A6", "patch.linewidth": 0,
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

if 'page' not in st.session_state:
    st.session_state['page'] = 0

# ══════════════════════════════════════════════════════════════════════════════
# TOP APP BAR
# ══════════════════════════════════════════════════════════════════════════════
page_names = ["จัดการข้อมูล","ตรวจสอบ","ทำความสะอาด","วิเคราะห์","ความปลอดภัย","Charts"]
page_icons_nav = ["🗂","🔍","✨","📊","🔐","📈"]

st.markdown(f"""
<div class="topbar">
  <div class="topbar-mark">DF</div>
  <div>
    <div class="topbar-title">DataFlow</div>
    <div class="topbar-sub">{page_names[st.session_state['page']]}</div>
  </div>
  <div class="topbar-badge">
    <span class="online-dot"></span>
    ฿{total_sales/1000:.0f}K
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
nav_labels = ["จัดการ","ตรวจสอบ","Clean","วิเคราะห์","Security","Charts"]
cur = st.session_state['page']
nav_items = "".join([
    f'<div class="nav-item {"active" if i == cur else ""}" onclick="void(0)">'
    f'<span class="nav-ic">{icon}</span>'
    f'<span class="nav-lbl">{label}</span>'
    f'</div>'
    for i, (icon, label) in enumerate(zip(page_icons_nav, nav_labels))
])
st.markdown(f'<div class="bottom-nav">{nav_items}</div>', unsafe_allow_html=True)

# Navigation buttons (hidden visually, functional) — use columns
nav_cols = st.columns(6)
for i, (col, label) in enumerate(zip(nav_cols, page_icons_nav)):
    with col:
        if st.button(label, key=f"nav_{i}", help=nav_labels[i]):
            st.session_state['page'] = i
            st.rerun()

# Hide nav buttons but keep them functional
st.markdown("""
<style>
/* Make the actual nav button row invisible — bottom nav HTML handles visuals */
div[data-testid="stHorizontalBlock"]:has(button[data-testid="baseButton-secondary"]) {
    position: fixed !important; bottom: 0 !important; left: 50% !important;
    transform: translateX(-50%) !important; z-index: 300 !important;
    width: 100% !important; max-width: 480px !important;
    height: var(--nav-h) !important;
    display: grid !important; grid-template-columns: repeat(6, 1fr) !important;
    gap: 0 !important; padding: 0 4px !important;
    background: transparent !important;
}
div[data-testid="stHorizontalBlock"]:has(button[data-testid="baseButton-secondary"]) .stButton > button {
    background: transparent !important;
    color: transparent !important; border: none !important;
    box-shadow: none !important; border-radius: 0 !important;
    padding: 0 !important; width: 100% !important; height: 100% !important;
    min-height: var(--nav-h) !important; font-size: 0 !important;
    transform: none !important;
}
div[data-testid="stHorizontalBlock"]:has(button[data-testid="baseButton-secondary"]) .stButton > button:hover {
    background: transparent !important; transform: none !important; box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════
page = st.session_state.get('page', 0)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 0 — จัดการข้อมูล
# ─────────────────────────────────────────────────────────────────────────────
if page == 0:
    st.markdown("""
    <div class="ph">
      <div class="ph-icon">🗂</div>
      <div>
        <div class="ph-title">จัดการข้อมูล</div>
        <div class="ph-desc">เพิ่ม · ลบ รายการยอดขาย</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Stats summary
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card blue">
        <span class="kpi-icon">📋</span>
        <div class="kpi-label">รายการ</div>
        <div class="kpi-value">{len(df)}</div>
        <div class="kpi-sub">Records</div>
      </div>
      <div class="kpi-card green">
        <span class="kpi-icon">💰</span>
        <div class="kpi-label">ยอดขาย</div>
        <div class="kpi-value" style="font-size:1.3rem;">฿{total_sales/1000:.0f}K</div>
        <div class="kpi-sub">Total sales</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ADD FORM
    st.markdown('<div class="section-label">➕ เพิ่มรายการใหม่</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("add_form", clear_on_submit=True):
        new_date  = st.date_input("📅 วันที่ขาย")
        c1, c2   = st.columns(2)
        new_id   = c1.text_input("🔖 รหัสสินค้า", placeholder="P001")
        new_name = c2.text_input("📦 ชื่อสินค้า", placeholder="Laptop")
        new_cat  = st.selectbox("🏷 หมวดหมู่", ["IT","Furniture","Electronics"])
        c3, c4   = st.columns(2)
        new_qty  = c3.number_input("📊 จำนวน", min_value=1, value=1)
        new_price= c4.number_input("💰 ราคา/หน่วย", min_value=1, value=100)
        new_reg  = st.selectbox("🌏 ภูมิภาค", ["North","South","Central","East","West"])
        if st.form_submit_button("＋  บันทึกรายการ", use_container_width=True):
            new_row = pd.DataFrame([[str(new_date), new_id, new_name, new_cat, new_qty, new_price, new_reg]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv('sales_data.csv', index=False)
            st.success(f"✓ เพิ่ม **{new_name}** เรียบร้อยแล้ว")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # DELETE
    st.markdown('<div class="section-label">🗑 ลบรายการ</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(
        df[['Product Name','Quantity','Unit Price','Region']].reset_index().rename(columns={"index":"#"}),
        use_container_width=True, height=180
    )
    del_idx = st.number_input("เลขลำดับ (#) ที่ต้องการลบ", min_value=0, max_value=max(len(df)-1,0), step=1)
    preview = df.iloc[del_idx]['Product Name'] if len(df) > 0 else "—"
    st.markdown(f'<div class="del-warn">⚠ จะลบ: <strong>{preview}</strong> (แถว #{del_idx})</div>', unsafe_allow_html=True)
    if st.button("🗑  ยืนยันการลบ", use_container_width=True):
        df = df.drop(df.index[del_idx]).reset_index(drop=True)
        df.to_csv('sales_data.csv', index=False)
        st.warning(f"ลบ **{preview}** เรียบร้อยแล้ว")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Full table
    st.markdown('<div class="section-label">📋 ข้อมูลทั้งหมด</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 — ตรวจสอบคุณภาพ
# ─────────────────────────────────────────────────────────────────────────────
elif page == 1:
    st.markdown("""
    <div class="ph">
      <div class="ph-icon">🔍</div>
      <div>
        <div class="ph-title">ตรวจสอบคุณภาพ</div>
        <div class="ph-desc">Missing · Duplicates · Type Check</div>
      </div>
    </div>""", unsafe_allow_html=True)

    null_rows = df[df.isnull().any(axis=1)]
    dup_rows  = df[df.duplicated(keep=False)]
    n_null    = len(null_rows)
    n_dup     = len(df[df.duplicated()])
    score     = max(0, min(100, 100 - (n_null + n_dup) * 5))

    sc = "green" if score >= 90 else "amber" if score >= 70 else "red"
    nc = "green" if n_null == 0 else "red"
    dc = "green" if n_dup  == 0 else "amber"

    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card blue">
        <span class="kpi-icon">📋</span>
        <div class="kpi-label">แถวทั้งหมด</div>
        <div class="kpi-value">{len(df)}</div>
        <div class="kpi-sub">Total rows</div>
      </div>
      <div class="kpi-card {sc}">
        <span class="kpi-icon">⭐</span>
        <div class="kpi-label">Quality Score</div>
        <div class="kpi-value">{score}</div>
        <div class="kpi-sub">{'Excellent ✓' if score >= 90 else 'Fair' if score >= 70 else 'Needs Work'}</div>
      </div>
      <div class="kpi-card {nc}">
        <span class="kpi-icon">🔎</span>
        <div class="kpi-label">Missing</div>
        <div class="kpi-value">{n_null}</div>
        <div class="kpi-sub">{'ครบถ้วน ✓' if n_null == 0 else f'{n_null} แถว'}</div>
      </div>
      <div class="kpi-card {dc}">
        <span class="kpi-icon">🔄</span>
        <div class="kpi-label">Duplicates</div>
        <div class="kpi-value">{n_dup}</div>
        <div class="kpi-sub">{'ไม่มีซ้ำ ✓' if n_dup == 0 else f'{n_dup} รายการ'}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔍  เริ่มสแกนข้อมูล", use_container_width=True):
        st.markdown('<div class="section-label">Missing Values</div>', unsafe_allow_html=True)
        if null_rows.empty: st.success("✓ ข้อมูลครบถ้วนทุกแถว")
        else: st.error(f"พบ {n_null} แถวที่ขาดข้อมูล"); st.dataframe(null_rows, use_container_width=True)

        st.markdown('<div class="section-label">Duplicates</div>', unsafe_allow_html=True)
        if dup_rows.empty: st.success("✓ ไม่พบข้อมูลซ้ำ")
        else: st.warning(f"พบ {n_dup} รายการซ้ำ"); st.dataframe(dup_rows, use_container_width=True)

        st.markdown('<div class="section-label">Data Types</div>', unsafe_allow_html=True)
        def check_type(v): return type(v).__name__
        st.dataframe(df.applymap(check_type), use_container_width=True)
        st.info("💡 ตัวเลขที่แสดงเป็น str = type ผิด ควรแก้ก่อนวิเคราะห์")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 — ทำความสะอาด
# ─────────────────────────────────────────────────────────────────────────────
elif page == 2:
    st.markdown("""
    <div class="ph">
      <div class="ph-icon">✨</div>
      <div>
        <div class="ph-title">ทำความสะอาดข้อมูล</div>
        <div class="ph-desc">3-Step Cleaning Pipeline</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <div class="ct"><span class="ct-dot" style="background:var(--amber)"></span>Cleaning Pipeline</div>
      <div class="wf-step">
        <div class="wf-num">01</div>
        <div>
          <div class="wf-title">Deduplication</div>
          <div class="wf-desc">ตรวจจับและลบแถวที่มีข้อมูลซ้ำกันทุกฟิลด์</div>
        </div>
      </div>
      <div class="wf-step">
        <div class="wf-num">02</div>
        <div>
          <div class="wf-title">Outlier Filter</div>
          <div class="wf-desc">ลบ Quantity ≤ 0 และ Unit Price ≤ 0</div>
        </div>
      </div>
      <div class="wf-step">
        <div class="wf-num">03</div>
        <div>
          <div class="wf-title">Date Normalization</div>
          <div class="wf-desc">แปลง Date → datetime64 ลบแถวที่ parse ไม่ได้</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✨  เริ่ม Clean Pipeline", use_container_width=True):
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

        removed = len(df_b) - len(df_c)
        st.success(f"✓ Pipeline สำเร็จ — พร้อมใช้ **{len(df_c):,}** แถว (นำออก {removed})")

        st.markdown(f"""
        <div class="kpi-grid">
          <div class="kpi-card blue">
            <span class="kpi-icon">📥</span>
            <div class="kpi-label">Input</div>
            <div class="kpi-value">{len(df_b)}</div>
            <div class="kpi-sub">แถวเริ่มต้น</div>
          </div>
          <div class="kpi-card green">
            <span class="kpi-icon">✓</span>
            <div class="kpi-label">Output</div>
            <div class="kpi-value">{len(df_c)}</div>
            <div class="kpi-sub">พร้อมใช้งาน</div>
          </div>
          <div class="kpi-card red">
            <span class="kpi-icon">🔄</span>
            <div class="kpi-label">ลบซ้ำ</div>
            <div class="kpi-value">−{len(dup_r)}</div>
            <div class="kpi-sub">Duplicates</div>
          </div>
          <div class="kpi-card amber">
            <span class="kpi-icon">⚡</span>
            <div class="kpi-label">ลบ Outlier</div>
            <div class="kpi-value">−{len(wrong_r)}</div>
            <div class="kpi-sub">Invalid rows</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("🔍 ดูรายละเอียดที่นำออก"):
            if not dup_r.empty:   st.markdown("**ซ้ำ:**");    st.dataframe(dup_r,   use_container_width=True)
            if not wrong_r.empty: st.markdown("**ผิดพลาด:**"); st.dataframe(wrong_r, use_container_width=True)
            if not inv_d.empty:   st.markdown("**วันที่:**");  st.dataframe(inv_d,   use_container_width=True)

        st.markdown('<div class="section-label">ข้อมูลหลัง Clean</div>', unsafe_allow_html=True)
        st.dataframe(df_c, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 — วิเคราะห์
# ─────────────────────────────────────────────────────────────────────────────
elif page == 3:
    st.markdown("""
    <div class="ph">
      <div class="ph-icon">📊</div>
      <div>
        <div class="ph-title">วิเคราะห์ข้อมูล</div>
        <div class="ph-desc">Business Analytics</div>
      </div>
    </div>""", unsafe_allow_html=True)

    if 'df_clean' not in st.session_state:
        st.markdown("""
        <div class="empty-state">
          <span class="empty-icon">📊</span>
          <div class="empty-title">ยังไม่มีข้อมูล Clean</div>
          <div class="empty-desc">ไปที่เมนู ✨ ทำความสะอาด<br>แล้วกด Pipeline ก่อน</div>
          <span class="empty-hint">✨ ไปหน้า Clean →</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        data = st.session_state['df_clean'].copy()
        data['Total_Sales'] = pd.to_numeric(data['Quantity'], errors='coerce') * pd.to_numeric(data['Unit Price'], errors='coerce')
        data['Month'] = data['Date'].dt.to_period('M').astype(str)
        monthly = data.groupby('Month')['Total_Sales'].sum().reset_index()
        top5    = data.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False).head(5).reset_index()
        region  = data.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False).reset_index()
        best_r  = region.iloc[0]['Region']
        best_p  = top5.iloc[0]['Product Name']
        total   = data['Total_Sales'].sum()
        avg_mo  = monthly['Total_Sales'].mean()

        st.markdown(f"""
        <div class="kpi-grid">
          <div class="kpi-card blue">
            <span class="kpi-icon">💰</span>
            <div class="kpi-label">ยอดขายรวม</div>
            <div class="kpi-value" style="font-size:1.3rem;">฿{total/1000:.0f}K</div>
            <div class="kpi-sub">Total revenue</div>
          </div>
          <div class="kpi-card cyan">
            <span class="kpi-icon">📅</span>
            <div class="kpi-label">เฉลี่ย/เดือน</div>
            <div class="kpi-value" style="font-size:1.3rem;">฿{avg_mo/1000:.0f}K</div>
            <div class="kpi-sub">Monthly avg</div>
          </div>
          <div class="kpi-card green">
            <span class="kpi-icon">🌏</span>
            <div class="kpi-label">ภูมิภาคนำ</div>
            <div class="kpi-value sm">{best_r}</div>
            <div class="kpi-sub">Top region</div>
          </div>
          <div class="kpi-card purple">
            <span class="kpi-icon">🏆</span>
            <div class="kpi-label">สินค้าขายดี</div>
            <div class="kpi-value sm">{best_p}</div>
            <div class="kpi-sub">Best seller</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-label">ยอดขายรายเดือน</div>', unsafe_allow_html=True)
        st.table(monthly.rename(columns={"Month":"เดือน","Total_Sales":"ยอดขาย (฿)"}))

        st.markdown('<div class="section-label">สินค้าขายดี Top 5</div>', unsafe_allow_html=True)
        st.table(top5.rename(columns={"Product Name":"สินค้า","Quantity":"จำนวน"}))

        st.markdown('<div class="section-label">ยอดขายตามภูมิภาค</div>', unsafe_allow_html=True)
        st.table(region.rename(columns={"Region":"ภูมิภาค","Total_Sales":"ยอดขาย (฿)"}))

        st.success(f"💡 ทำโปรโมชั่น **{best_p}** · เพิ่มงบภูมิภาค **{best_r}**")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 4 — ความปลอดภัย
# ─────────────────────────────────────────────────────────────────────────────
elif page == 4:
    st.markdown("""
    <div class="ph">
      <div class="ph-icon">🔐</div>
      <div>
        <div class="ph-title">ความปลอดภัย</div>
        <div class="ph-desc">RBAC · Controls · PDPA</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-label">Role-Based Access</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
      <div class="list-row">
        <div class="list-av">🔐</div>
        <div style="flex:1">
          <div class="list-title">Admin (ไอที)</div>
          <div class="list-sub">ดู · เพิ่ม · แก้ไข · ลบ · จัดการผู้ใช้</div>
        </div>
        <span class="pill p-red">สูงสุด</span>
      </div>
      <div class="list-row">
        <div class="list-av">📊</div>
        <div style="flex:1">
          <div class="list-title">Analyst</div>
          <div class="list-sub">ดู · ทำความสะอาด · วิเคราะห์</div>
        </div>
        <span class="pill p-blue">กลาง</span>
      </div>
      <div class="list-row">
        <div class="list-av">👁</div>
        <div style="flex:1">
          <div class="list-title">Viewer (ผู้บริหาร)</div>
          <div class="list-sub">ดูรายงานเท่านั้น</div>
        </div>
        <span class="pill p-green">ต่ำ</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">🔧 Technical Controls</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
      <div class="sec-item">
        <div class="sec-ic">🔒</div>
        <div>
          <div class="sec-title">Encryption AES-256</div>
          <div class="sec-desc">เข้ารหัสข้อมูลขณะจัดเก็บและส่ง</div>
        </div>
      </div>
      <div class="sec-item">
        <div class="sec-ic">📱</div>
        <div>
          <div class="sec-title">MFA (TOTP/SMS)</div>
          <div class="sec-desc">ยืนยันตัวตน 2 ชั้นทุก session</div>
        </div>
      </div>
      <div class="sec-item">
        <div class="sec-ic">📋</div>
        <div>
          <div class="sec-title">Audit Logs</div>
          <div class="sec-desc">บันทึก action + timestamp + IP</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">📋 Administrative</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
      <div class="sec-item">
        <div class="sec-ic" style="background:var(--green-lt);color:#2EE89A;border:1px solid #0E3C24">📝</div>
        <div>
          <div class="sec-title">NDA Agreement</div>
          <div class="sec-desc">สัญญา NDA พนักงานทุกคน</div>
        </div>
      </div>
      <div class="sec-item">
        <div class="sec-ic" style="background:var(--green-lt);color:#2EE89A;border:1px solid #0E3C24">🏛</div>
        <div>
          <div class="sec-title">PDPA Compliance</div>
          <div class="sec-desc">สอดคล้อง พ.ร.บ. คุ้มครองข้อมูลฯ</div>
        </div>
      </div>
      <div class="sec-item">
        <div class="sec-ic" style="background:var(--green-lt);color:#2EE89A;border:1px solid #0E3C24">🎓</div>
        <div>
          <div class="sec-title">Security Training</div>
          <div class="sec-desc">อบรม Cyber Awareness รายปี</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.success("✓ ISO/IEC 27001 · PDPA · NIST Cybersecurity Framework")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 5 — Charts
# ─────────────────────────────────────────────────────────────────────────────
elif page == 5:
    st.markdown("""
    <div class="ph">
      <div class="ph-icon">📈</div>
      <div>
        <div class="ph-title">Data Charts</div>
        <div class="ph-desc">Trends · Region · Products</div>
      </div>
    </div>""", unsafe_allow_html=True)

    if 'df_clean' not in st.session_state:
        st.markdown("""
        <div class="empty-state">
          <span class="empty-icon">📈</span>
          <div class="empty-title">ยังไม่มีข้อมูล</div>
          <div class="empty-desc">ไปที่ ✨ ทำความสะอาด ก่อน</div>
          <span class="empty-hint">✨ ไปหน้า Clean →</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        data = st.session_state['df_clean'].copy()
        data['Total_Sales'] = pd.to_numeric(data['Quantity'], errors='coerce') * pd.to_numeric(data['Unit Price'], errors='coerce')
        data['Month'] = data['Date'].dt.to_period('M').astype(str)
        monthly_trend = data.groupby('Month')['Total_Sales'].sum().reset_index()
        region_comp   = data.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False).reset_index()
        top5_prod     = data.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False).head(5).reset_index()

        # Chart 1 — Line
        st.markdown('<div class="section-label">แนวโน้มยอดขายรายเดือน</div>', unsafe_allow_html=True)
        fig1, ax1 = plt.subplots(figsize=(4.8, 2.8))
        x = range(len(monthly_trend))
        ax1.fill_between(x, monthly_trend['Total_Sales'], alpha=0.13, color=PALETTE[0])
        ax1.plot(x, monthly_trend['Total_Sales'],
                 color=PALETTE[0], linewidth=2.5, marker='o',
                 markersize=7, markerfacecolor=BG_C, markeredgewidth=2.5,
                 markeredgecolor=PALETTE[0], zorder=5)
        ax1.set_xticks(x)
        ax1.set_xticklabels(monthly_trend['Month'], rotation=35, ha='right', fontsize=7.5)
        ax1.set_title("Monthly Sales Trend", loc='left', color='#EDF2FF')
        ax1.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"฿{v/1000:.0f}K"))
        plt.tight_layout(pad=1.2)
        st.pyplot(fig1, use_container_width=True)

        # Chart 2 — Bar (Region)
        st.markdown('<div class="section-label">ยอดขายตามภูมิภาค</div>', unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(4.8, 2.8))
        colors = [PALETTE[0]] + [PALETTE[5]] * (len(region_comp)-1)
        bars = ax2.bar(region_comp['Region'], region_comp['Total_Sales'],
                       color=colors, width=0.52, zorder=3, edgecolor='none')
        ax2.set_title("Sales by Region", loc='left', color='#EDF2FF')
        ax2.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"฿{v/1000:.0f}K"))
        for b in bars:
            ax2.text(b.get_x() + b.get_width()/2, b.get_height()*1.04,
                     f"฿{b.get_height()/1000:.0f}K", ha='center', va='bottom',
                     fontsize=7, color='#6B80A6', fontweight='600')
        plt.tight_layout(pad=1.2)
        st.pyplot(fig2, use_container_width=True)

        # Chart 3 — Horizontal bar (Top 5)
        st.markdown('<div class="section-label">สินค้าขายดี Top 5</div>', unsafe_allow_html=True)
        fig3, ax3 = plt.subplots(figsize=(4.8, 2.6))
        bc = [PALETTE[1]] + [PALETTE[0]] * (len(top5_prod)-1)
        bars3 = ax3.barh(top5_prod['Product Name'][::-1], top5_prod['Quantity'][::-1],
                         color=bc[::-1], height=0.55, zorder=3, edgecolor='none')
        ax3.set_title("Top 5 Products", loc='left', color='#EDF2FF')
        for b in bars3:
            ax3.text(b.get_width() + 0.3, b.get_y() + b.get_height()/2,
                     f"{b.get_width():.0f}", va='center', fontsize=8, color='#6B80A6', fontweight='600')
        ax3.set_xlim(0, top5_prod['Quantity'].max() * 1.2)
        plt.tight_layout(pad=1.2)
        st.pyplot(fig3, use_container_width=True)

        best_r = region_comp.iloc[0]['Region']
        best_p = top5_prod.iloc[0]['Product Name']
        st.success(f"**📊 สรุป** — ภูมิภาค: **{best_r}** · สินค้า: **{best_p}**")