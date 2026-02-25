import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

st.set_page_config(page_title="DataFlow · Sales", layout="wide", page_icon="📊",
                   initial_sidebar_state="expanded")

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — Premium Dark SaaS — Refined Noir Edition
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@500;600;700;800&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:         #080C12;
    --surface:    #0E1420;
    --surface-2:  #141C2C;
    --surface-3:  #1B2438;
    --surface-gl: rgba(14,20,32,0.7);
    --border:     #1E2D44;
    --border-2:   #2A3E5A;
    --border-hi:  #3A5278;

    --sidebar-bg: #080C12;

    --txt1:   #EBF0FA;
    --txt2:   #6E82A8;
    --txt3:   #3D506E;

    --blue:      #4D7CFF;
    --blue-lt:   #0F1E44;
    --blue-dk:   #3A67F0;
    --blue-glow: rgba(77,124,255,.35);
    --blue-sel:  #132040;
    --blue-bar:  #4D7CFF;

    --cyan:      #06C8D0;
    --cyan-lt:   #041E28;

    --green:     #10D98B;
    --green-lt:  #071E15;
    --green-glow:rgba(16,217,139,.25);

    --amber:     #FFB020;
    --amber-lt:  #221806;

    --red:       #FF4D6A;
    --red-lt:    #200810;
    --red-glow:  rgba(255,77,106,.25);

    --purple:    #9B6DFF;
    --purple-lt: #140E28;

    --r4: 4px; --r6: 6px; --r8: 8px; --r12: 12px; --r16: 16px; --r20: 20px;
    --sh:  0 1px 4px rgba(0,0,0,.6), 0 4px 16px rgba(0,0,0,.4);
    --sh2: 0 8px 32px rgba(0,0,0,.7);
    --sh-blue: 0 4px 20px rgba(77,124,255,.2);
    --sh-green: 0 4px 20px rgba(16,217,139,.15);
}

*, html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    box-sizing: border-box;
    color-scheme: dark;
}

.stApp {
    background: var(--bg) !important;
    color: var(--txt1) !important;
}
.stApp::before {
    content: '';
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
        radial-gradient(ellipse 900px 600px at 70% -10%, rgba(77,124,255,.06) 0%, transparent 70%),
        radial-gradient(ellipse 600px 400px at -5% 80%, rgba(16,217,139,.04) 0%, transparent 60%);
}
#MainMenu, footer, header { visibility: hidden; }

/* ══════════════════════════════════════
   SIDEBAR
══════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: 1px solid var(--border) !important;
    width: 240px !important; min-width: 240px !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] > div:first-child,
[data-testid="stSidebarContent"] {
    background: var(--sidebar-bg) !important;
    padding: 0 !important;
}

.sb-brand {
    display: flex; align-items: center; gap: 10px;
    padding: 18px 16px 14px 16px;
    border-bottom: 1px solid var(--border);
}
.sb-mark {
    width: 30px; height: 30px;
    background: linear-gradient(135deg, #4D7CFF 0%, #3A67F0 100%);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Syne', sans-serif !important;
    font-size: 11px; font-weight: 800; color: #fff;
    letter-spacing: -0.5px; flex-shrink: 0;
    box-shadow: 0 0 16px var(--blue-glow), 0 2px 6px rgba(0,0,0,.4);
}
.sb-brand-name {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.9rem; font-weight: 700; color: var(--txt1); letter-spacing: -0.02em;
}
.sb-brand-sub { font-size: 0.63rem; color: var(--txt3); margin-top: 1px; letter-spacing: 0.02em; }

.sb-section {
    font-size: 0.58rem; font-weight: 600;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--txt3); padding: 14px 16px 6px 16px;
}
.sb-divider { height: 1px; background: var(--border); margin: 6px 0; }

.sb-stats {
    margin: 8px 12px 0 12px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--r8); padding: 10px 12px;
}
.sb-stat-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 4px 0; border-bottom: 1px solid var(--border); font-size: 0.71rem;
}
.sb-stat-row:last-child { border-bottom: none; }
.sb-stat-label { color: var(--txt3); }
.sb-stat-val {
    color: var(--txt1); font-weight: 600;
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.69rem;
}

/* ══════════════════════════════════════
   MAIN CONTENT
══════════════════════════════════════ */
.block-container {
    padding: 0 2.4rem 3rem 2.4rem !important;
    max-width: 100% !important;
    position: relative; z-index: 1;
}

/* ── Page header ── */
.ph {
    display: flex; align-items: center; gap: 14px;
    padding: 1.8rem 0 1.4rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.8rem;
}
.ph-icon {
    width: 44px; height: 44px; border-radius: 12px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; font-size: 18px;
    border: 1px solid var(--border);
    position: relative; overflow: hidden;
}
.ph-icon::after {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,.05) 0%, transparent 60%);
}
.ph-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.15rem; font-weight: 700; letter-spacing: -0.03em;
    margin: 0; color: var(--txt1); line-height: 1.2;
}
.ph-desc { font-size: 0.72rem; color: var(--txt3); margin: 3px 0 0 0; letter-spacing: 0.01em; }
.ph-badge {
    margin-left: auto;
    font-size: 0.62rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase;
    background: var(--surface-2); border: 1px solid var(--border-2);
    border-radius: 99px; padding: 4px 12px; color: var(--txt3);
}

/* ── KPI Stat Cards ── */
.kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 1.6rem; }
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r12);
    padding: 1.1rem 1.3rem;
    box-shadow: var(--sh);
    position: relative; overflow: hidden;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.kpi-card:hover { border-color: var(--border-hi); }
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    border-radius: 12px 12px 0 0;
}
.kpi-card.blue::before  { background: linear-gradient(90deg, var(--blue), var(--cyan)); box-shadow: 0 0 12px var(--blue-glow); }
.kpi-card.green::before { background: linear-gradient(90deg, var(--green), #06C8D0);    box-shadow: 0 0 12px var(--green-glow); }
.kpi-card.amber::before { background: linear-gradient(90deg, var(--amber), #FF8C42); }
.kpi-card.purple::before{ background: linear-gradient(90deg, var(--purple), var(--blue)); }
.kpi-card.red::before   { background: linear-gradient(90deg, var(--red), var(--purple));  box-shadow: 0 0 12px var(--red-glow); }
.kpi-label {
    font-size: 0.62rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.1em; color: var(--txt3); margin-bottom: 6px;
}
.kpi-value {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.7rem; font-weight: 700; letter-spacing: -0.04em; color: var(--txt1); line-height: 1;
}
.kpi-sub { font-size: 0.69rem; color: var(--txt2); margin-top: 5px; }
.kpi-icon { position: absolute; right: 14px; top: 16px; font-size: 20px; opacity: 0.15; }

/* ── Glass Cards ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r12);
    padding: 1.3rem 1.5rem;
    box-shadow: var(--sh);
    margin-bottom: 1rem;
    position: relative; overflow: hidden;
    transition: border-color 0.2s;
}
.card:hover { border-color: var(--border-2); }
.card::after {
    content: '';
    position: absolute; top: 0; right: 0;
    width: 120px; height: 120px;
    background: radial-gradient(circle, rgba(77,124,255,.04) 0%, transparent 70%);
    pointer-events: none;
}

.ct {
    font-size: 0.64rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--txt3);
    margin-bottom: 0.9rem; padding-bottom: 0.65rem;
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; gap: 7px;
}
.ct-dot {
    width: 5px; height: 5px; border-radius: 50%;
    background: var(--blue); display: inline-block; flex-shrink: 0;
    box-shadow: 0 0 6px var(--blue-glow);
}

/* ── Pill tags ── */
.pill {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 3px 9px; border-radius: 99px;
    font-size: 0.64rem; font-weight: 600; letter-spacing: 0.03em;
    border: 1px solid transparent;
}
.p-blue   { background: var(--blue-lt);   color: #7AACFF; border-color: #1E3360; }
.p-green  { background: var(--green-lt);  color: #2EE89A; border-color: #0E3828; }
.p-amber  { background: var(--amber-lt);  color: #FFCA50; border-color: #3D2C0A; }
.p-red    { background: var(--red-lt);    color: #FF7088; border-color: #3D1020; }
.p-purple { background: var(--purple-lt); color: #B98AFF; border-color: #251440; }

/* ── Workflow steps ── */
.wf-wrap { position: relative; }
.wf-line {
    position: absolute; left: 20px; top: 28px; bottom: 12px;
    width: 1px; background: linear-gradient(180deg, var(--blue) 0%, transparent 100%);
    opacity: 0.3;
}
.wf-step {
    display: flex; align-items: flex-start; gap: 14px;
    padding: 0.9rem 0.7rem;
    border-radius: var(--r8);
    transition: background 0.15s;
    position: relative;
}
.wf-step:hover { background: var(--surface-2); }
.wf-num {
    width: 28px; height: 28px; border-radius: 50%; flex-shrink: 0;
    background: linear-gradient(135deg, var(--blue) 0%, var(--blue-dk) 100%);
    color: #fff; font-size: 0.65rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 0 12px var(--blue-glow);
    font-family: 'JetBrains Mono', monospace !important;
    border: 1px solid rgba(77,124,255,.3);
}
.wf-title { font-size: 0.85rem; font-weight: 600; color: var(--txt1); letter-spacing: -0.01em; }
.wf-desc  { font-size: 0.72rem; color: var(--txt2); margin-top: 3px; line-height: 1.6; }
.wf-tag {
    margin-left: auto; flex-shrink: 0; margin-top: 2px;
    font-size: 0.6rem; font-weight: 600; letter-spacing: 0.05em;
    background: var(--blue-lt); color: #7AACFF; border: 1px solid #1E3360;
    border-radius: 4px; padding: 2px 6px; text-transform: uppercase;
}

/* ── Role rows ── */
.role-row {
    display: flex; align-items: center; gap: 12px;
    padding: 0.8rem 0.6rem; border-radius: var(--r8);
    border-bottom: 1px solid var(--border);
    transition: background 0.12s;
}
.role-row:last-child { border-bottom: none; }
.role-row:hover { background: var(--surface-2); }
.role-av {
    width: 36px; height: 36px; border-radius: 10px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; font-size: 15px;
    border: 1px solid var(--border);
    position: relative; overflow: hidden;
}
.role-av::after {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,.06) 0%, transparent 60%);
}
.rn { font-size: 0.82rem; font-weight: 600; color: var(--txt1); letter-spacing: -0.01em; }
.rp { font-size: 0.7rem; color: var(--txt3); margin-top: 1px; }

/* ── Security panels ── */
.sec-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 6px; }
.sec-panel {
    background: var(--surface-2); border: 1px solid var(--border);
    border-radius: var(--r8); padding: 1rem 1.1rem;
    position: relative; overflow: hidden;
}
.sec-panel::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-hi), transparent);
}
.sec-panel-title {
    font-size: 0.62rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.09em; color: var(--txt3); margin-bottom: 10px;
}
.sec-item {
    display: flex; align-items: flex-start; gap: 9px;
    padding: 6px 0; border-bottom: 1px solid var(--border);
    transition: transform 0.1s;
}
.sec-item:last-child { border-bottom: none; }
.sec-item:hover { transform: translateX(2px); }
.sec-ic {
    width: 26px; height: 26px; border-radius: 7px;
    background: var(--blue-lt); color: #7AACFF;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; flex-shrink: 0; margin-top: 1px;
    border: 1px solid #1E3360;
}
.sl { font-size: 0.79rem; font-weight: 600; color: var(--txt1); letter-spacing: -0.01em; }
.sd { font-size: 0.69rem; color: var(--txt3); margin-top: 2px; line-height: 1.45; }

/* ── Empty state ── */
.empty-state {
    text-align: center; padding: 5rem 2rem;
    background: var(--surface);
    border: 1px dashed var(--border-2);
    border-radius: var(--r16); margin: 1.5rem 0;
    position: relative; overflow: hidden;
}
.empty-state::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 400px 300px at 50% 50%, rgba(77,124,255,.04) 0%, transparent 70%);
}
.empty-icon  { font-size: 3rem; margin-bottom: 0.8rem; opacity: 0.3; display: block; }
.empty-title { font-family: 'Syne', sans-serif !important; font-size: 0.95rem; font-weight: 700; color: var(--txt2); }
.empty-desc  { font-size: 0.72rem; color: var(--txt3); margin-top: 6px; }

/* ── Form section label ── */
.form-section {
    font-size: 0.62rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: var(--txt3); margin-bottom: 10px;
    display: flex; align-items: center; gap: 8px;
}
.form-section::after {
    content: ''; flex: 1; height: 1px; background: var(--border);
}

/* ── Delete warning box ── */
.del-warn {
    background: var(--red-lt);
    border: 1px solid #3D1020;
    border-left: 3px solid var(--red);
    border-radius: var(--r8);
    padding: 8px 12px;
    font-size: 0.75rem; color: #FF8098;
    margin: 5px 0 10px 0;
    display: flex; align-items: center; gap: 8px;
}

/* ── Info banner ── */
.info-banner {
    background: linear-gradient(135deg, var(--blue-lt) 0%, rgba(15,30,68,.3) 100%);
    border: 1px solid #1E3360;
    border-left: 3px solid var(--blue);
    border-radius: var(--r8);
    padding: 10px 14px;
    font-size: 0.78rem; color: #8ABDFF;
    margin: 10px 0;
    display: flex; align-items: flex-start; gap: 10px;
}
.info-banner-icon { font-size: 14px; flex-shrink: 0; margin-top: 1px; }

/* ── Success banner ── */
.success-banner {
    background: linear-gradient(135deg, var(--green-lt) 0%, rgba(7,30,21,.3) 100%);
    border: 1px solid #0E3828;
    border-left: 3px solid var(--green);
    border-radius: var(--r8);
    padding: 10px 14px;
    font-size: 0.78rem; color: #2EE89A;
    margin: 10px 0;
}

/* ── Data table wrapper ── */
.table-wrap {
    border: 1px solid var(--border);
    border-radius: var(--r12); overflow: hidden;
    margin-bottom: 1rem;
}

/* ── Streamlit metric overrides ── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r12) !important;
    padding: 1.1rem 1.3rem !important;
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
    font-size: 0.62rem !important; text-transform: uppercase !important;
    letter-spacing: 0.1em !important; font-weight: 700 !important; color: var(--txt3) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.6rem !important; font-weight: 700 !important;
    letter-spacing: -0.04em !important; color: var(--txt1) !important;
}
[data-testid="stMetricDelta"] { font-size: 0.7rem !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--blue) 0%, var(--blue-dk) 100%) !important;
    color: #fff !important; border: none !important;
    border-radius: var(--r8) !important;
    padding: 0.5rem 1.3rem !important; font-size: 0.8rem !important;
    font-weight: 600 !important; letter-spacing: 0.01em !important;
    box-shadow: 0 2px 8px rgba(77,124,255,.35), 0 0 0 1px rgba(77,124,255,.15) !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #5D8CFF 0%, var(--blue) 100%) !important;
    box-shadow: 0 4px 18px rgba(77,124,255,.55), 0 0 0 1px rgba(77,124,255,.3) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Alert/notification overrides ── */
[data-testid="stAlert"] {
    border-radius: var(--r8) !important;
}
.stSuccess {
    background: linear-gradient(135deg, var(--green-lt), rgba(7,30,21,.3)) !important;
    border: 1px solid #0E3828 !important; border-left: 3px solid var(--green) !important;
    border-radius: var(--r8) !important; font-size: 0.8rem !important; color: #2EE89A !important;
}
.stInfo {
    background: linear-gradient(135deg, var(--blue-lt), rgba(15,30,68,.3)) !important;
    border: 1px solid #1E3360 !important; border-left: 3px solid var(--blue) !important;
    border-radius: var(--r8) !important; font-size: 0.8rem !important; color: #7AACFF !important;
}
.stWarning {
    background: linear-gradient(135deg, var(--amber-lt), rgba(34,24,6,.3)) !important;
    border: 1px solid #3D2C0A !important; border-left: 3px solid var(--amber) !important;
    border-radius: var(--r8) !important; font-size: 0.8rem !important; color: #FFCA50 !important;
}
.stError {
    background: linear-gradient(135deg, var(--red-lt), rgba(32,8,16,.3)) !important;
    border: 1px solid #3D1020 !important; border-left: 3px solid var(--red) !important;
    border-radius: var(--r8) !important; font-size: 0.8rem !important; color: #FF8098 !important;
}

details {
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-radius: var(--r8) !important;
}
summary { font-size: 0.8rem !important; font-weight: 600 !important; color: var(--txt2) !important; }
hr { border-color: var(--border) !important; margin: 1.4rem 0 !important; }

/* ── Form inputs ── */
.stTextInput input, .stNumberInput input {
    background: var(--surface-2) !important; border: 1px solid var(--border-2) !important;
    border-radius: var(--r8) !important; font-size: 0.82rem !important; color: var(--txt1) !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(77,124,255,.12) !important;
}
.stSelectbox > div > div, .stDateInput > div > div {
    background: var(--surface-2) !important; border: 1px solid var(--border-2) !important;
    border-radius: var(--r8) !important; color: var(--txt1) !important;
}
label { color: var(--txt2) !important; font-size: 0.74rem !important; font-weight: 500 !important; }

/* ── Tables ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important; border-radius: var(--r12) !important; overflow: hidden !important;
}
[data-testid="stTable"] table, .stDataFrame table {
    font-size: 0.77rem; border-collapse: collapse; width: 100%;
}
[data-testid="stTable"] thead th, .stDataFrame thead th {
    background: var(--surface-2) !important; color: var(--txt3) !important;
    font-size: 0.62rem !important; font-weight: 700 !important; text-transform: uppercase !important;
    letter-spacing: 0.1em !important; padding: 0.6rem 1rem !important;
    border-bottom: 1px solid var(--border-2) !important;
}
[data-testid="stTable"] tbody td, .stDataFrame tbody td {
    padding: 0.55rem 1rem !important; border-bottom: 1px solid var(--border) !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.73rem !important;
    color: var(--txt1) !important; background: var(--surface) !important;
    transition: background 0.1s !important;
}
[data-testid="stTable"] tbody tr:hover td, .stDataFrame tbody tr:hover td {
    background: var(--surface-2) !important;
}

/* ── Sidebar nav buttons ── */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important; color: var(--txt2) !important;
    border: none !important; border-radius: 0 !important;
    padding: 7px 16px !important; font-size: 0.79rem !important;
    font-weight: 400 !important; text-align: left !important;
    justify-content: flex-start !important; box-shadow: none !important;
    width: 100% !important; transition: all 0.1s !important; margin: 1px 0 !important;
    letter-spacing: 0.005em !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--surface-2) !important; color: var(--txt1) !important;
    transform: none !important; box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:focus,
[data-testid="stSidebar"] .stButton > button:active {
    background: var(--blue-sel) !important; color: var(--txt1) !important;
    box-shadow: inset 2px 0 0 var(--blue) !important; outline: none !important;
}

/* Remove Streamlit tabs */
.stTabs [data-baseweb="tab-list"]   { display: none !important; }
.stTabs [data-baseweb="tab-panel"]  { padding: 0 !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Matplotlib ─────────────────────────────────────────────────────────────────
PALETTE = ["#4D7CFF", "#10D98B", "#FFB020", "#FF4D6A", "#9B6DFF", "#06C8D0"]
BG_C = "#0E1420"
mpl.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["DM Sans", "Helvetica Neue", "Arial"],
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False, "axes.spines.bottom": False,
    "axes.grid": True, "grid.color": "#1E2D44", "grid.linewidth": 0.7,
    "grid.linestyle": "--", "grid.alpha": 0.8,
    "axes.facecolor": BG_C, "figure.facecolor": BG_C,
    "axes.labelcolor": "#3D506E", "xtick.color": "#3D506E", "ytick.color": "#3D506E",
    "xtick.labelsize": 8.5, "ytick.labelsize": 8.5,
    "axes.titlesize": 11, "axes.titleweight": "600", "axes.titlepad": 14,
    "axes.titlecolor": "#EBF0FA",
    "figure.dpi": 150,
    "text.color": "#6E82A8",
    "patch.linewidth": 0,
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
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
      <div class="sb-mark">DF</div>
      <div>
        <div class="sb-brand-name">DataFlow</div>
        <div class="sb-brand-sub">Sales Intelligence</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if 'page' not in st.session_state:
        st.session_state['page'] = 0

    pages = [
        (0, "⊞", "จัดการข้อมูล"),
        (1, "⊙", "ตรวจสอบคุณภาพ"),
        (2, "⊘", "ทำความสะอาด"),
        (3, "⊛", "วิเคราะห์"),
        (4, "⊜", "ความปลอดภัย"),
        (5, "⊝", "Visualization"),
    ]

    st.markdown('<div class="sb-section">Workspace</div>', unsafe_allow_html=True)
    for idx, icon, label in pages:
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
        <span class="sb-stat-label">สินค้า SKU</span>
        <span class="sb-stat-val">{n_products}</span>
      </div>
      <div class="sb-stat-row">
        <span class="sb-stat-label">สถานะ</span>
        <span class="sb-stat-val" style="color:#10D98B;">● Online</span>
      </div>
    </div>
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
      <div class="ph-icon" style="background:#0F1E44;border-color:#1E3360;">⊞</div>
      <div>
        <div class="ph-title">จัดการฐานข้อมูล</div>
        <div class="ph-desc">เพิ่ม · ลบ · ดูรายการยอดขายทั้งหมด</div>
      </div>
      <span class="ph-badge">Data Management</span>
    </div>""", unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2], gap="large")

    with col_a:
        st.markdown("""
        <div class="card">
          <div class="ct"><span class="ct-dot" style="box-shadow:0 0 6px rgba(77,124,255,.6)"></span>เพิ่มรายการใหม่</div>
          <div class="form-section">ข้อมูลสินค้า</div>
        """, unsafe_allow_html=True)
        with st.form("add_form", clear_on_submit=True):
            r1 = st.columns(3)
            new_date  = r1[0].date_input("📅 วันที่ขาย")
            new_id    = r1[1].text_input("🔖 รหัสสินค้า", placeholder="P001")
            new_name  = r1[2].text_input("📦 ชื่อสินค้า",  placeholder="Laptop")
            r2 = st.columns(3)
            new_cat   = r2[0].selectbox("🏷 หมวดหมู่",   ["IT","Furniture","Electronics"])
            new_qty   = r2[1].number_input("📊 จำนวน",    min_value=1, value=1)
            new_price = r2[2].number_input("💰 ราคา/หน่วย", min_value=1, value=100)
            new_reg   = st.selectbox("🌏 ภูมิภาค", ["North","South","Central","East","West"])
            if st.form_submit_button("＋  บันทึกรายการ", use_container_width=True):
                new_row = pd.DataFrame([[str(new_date), new_id, new_name, new_cat, new_qty, new_price, new_reg]], columns=df.columns)
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv('sales_data.csv', index=False)
                st.success(f"✓ เพิ่ม **{new_name}** เรียบร้อยแล้ว")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="card">
          <div class="ct"><span class="ct-dot" style="background:var(--red);box-shadow:0 0 6px rgba(255,77,106,.5)"></span>ลบรายการ</div>
        """, unsafe_allow_html=True)
        st.dataframe(
            df[['Product Name','Quantity','Unit Price','Region']].reset_index().rename(columns={"index":"#"}),
            use_container_width=True, height=185
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

    st.markdown('<div class="ct" style="margin-top:0.4rem;"><span class="ct-dot"></span>ข้อมูลทั้งหมดในระบบ</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 — ตรวจสอบคุณภาพ
# ─────────────────────────────────────────────────────────────────────────────
elif page == 1:
    st.markdown("""
    <div class="ph">
      <div class="ph-icon" style="background:#071E15;border-color:#0E3828;">⊙</div>
      <div>
        <div class="ph-title">ตรวจสอบคุณภาพข้อมูล</div>
        <div class="ph-desc">สแกนหา Missing Values · Duplicates · Type Errors</div>
      </div>
      <span class="ph-badge">Quality Check</span>
    </div>""", unsafe_allow_html=True)

    null_rows = df[df.isnull().any(axis=1)]
    dup_rows  = df[df.duplicated(keep=False)]
    n_null    = len(null_rows)
    n_dup     = len(df[df.duplicated()])
    score     = max(0, min(100, 100 - (n_null + n_dup) * 5))

    # Custom KPI cards
    score_color = "green" if score >= 90 else "amber" if score >= 70 else "red"
    null_color  = "green" if n_null == 0 else "red"
    dup_color   = "green" if n_dup == 0 else "amber"

    st.markdown(f"""
    <div class="kpi-row">
      <div class="kpi-card blue">
        <span class="kpi-icon">📋</span>
        <div class="kpi-label">แถวทั้งหมด</div>
        <div class="kpi-value">{len(df):,}</div>
        <div class="kpi-sub">Total records</div>
      </div>
      <div class="kpi-card {null_color}">
        <span class="kpi-icon">🔍</span>
        <div class="kpi-label">Missing Values</div>
        <div class="kpi-value">{n_null}</div>
        <div class="kpi-sub">{'ข้อมูลครบถ้วน ✓' if n_null == 0 else f'{n_null} แถวมีปัญหา'}</div>
      </div>
      <div class="kpi-card {dup_color}">
        <span class="kpi-icon">🔄</span>
        <div class="kpi-label">Duplicates</div>
        <div class="kpi-value">{n_dup}</div>
        <div class="kpi-sub">{'ไม่พบข้อมูลซ้ำ ✓' if n_dup == 0 else f'{n_dup} รายการซ้ำ'}</div>
      </div>
      <div class="kpi-card {score_color}">
        <span class="kpi-icon">⭐</span>
        <div class="kpi-label">Quality Score</div>
        <div class="kpi-value">{score}<span style="font-size:1rem;color:var(--txt3)">/100</span></div>
        <div class="kpi-sub">{'Excellent' if score >= 90 else 'Fair' if score >= 70 else 'Needs Work'}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("▶  เริ่มสแกนข้อมูล"):
        q1, q2 = st.columns(2, gap="large")
        with q1:
            st.markdown('<div class="ct"><span class="ct-dot"></span>Missing Values</div>', unsafe_allow_html=True)
            if null_rows.empty: st.success("✓ ข้อมูลครบถ้วนทุกแถว ไม่พบ null")
            else: st.error(f"พบ {n_null} แถวที่ขาดข้อมูล"); st.dataframe(null_rows, use_container_width=True)
        with q2:
            st.markdown('<div class="ct"><span class="ct-dot" style="background:var(--amber)"></span>Duplicates</div>', unsafe_allow_html=True)
            if dup_rows.empty: st.success("✓ ไม่พบข้อมูลซ้ำในระบบ")
            else: st.warning(f"พบ {n_dup} รายการซ้ำ"); st.dataframe(dup_rows.sort_values(by=list(df.columns)), use_container_width=True)

        st.markdown('<div class="ct" style="margin-top:1rem;"><span class="ct-dot" style="background:var(--purple);box-shadow:0 0 6px rgba(155,109,255,.5)"></span>ชนิดข้อมูลรายคอลัมน์</div>', unsafe_allow_html=True)
        def check_type(v): return type(v).__name__
        st.dataframe(df.applymap(check_type), use_container_width=True)
        st.info("💡 คอลัมน์ตัวเลขที่แสดงเป็น `str` = ชนิดข้อมูลผิด ควรแก้ไขก่อนวิเคราะห์")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 — ทำความสะอาด
# ─────────────────────────────────────────────────────────────────────────────
elif page == 2:
    st.markdown("""
    <div class="ph">
      <div class="ph-icon" style="background:#221806;border-color:#3D2C0A;">⊘</div>
      <div>
        <div class="ph-title">ทำความสะอาดข้อมูล</div>
        <div class="ph-desc">Deduplicate · Filter Outliers · Parse Dates</div>
      </div>
      <span class="ph-badge">Data Cleaning</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <div class="ct"><span class="ct-dot" style="background:var(--amber);box-shadow:0 0 6px rgba(255,176,32,.4)"></span>Cleaning Pipeline</div>
      <div class="wf-wrap">
        <div class="wf-line"></div>
        <div class="wf-step">
          <div class="wf-num">01</div>
          <div style="flex:1">
            <div class="wf-title">Deduplication</div>
            <div class="wf-desc">ตรวจจับและลบแถวที่มีข้อมูลซ้ำกันทุกฟิลด์ โดยเก็บแถวแรกไว้</div>
          </div>
          <span class="wf-tag">Step 1</span>
        </div>
        <div class="wf-step">
          <div class="wf-num">02</div>
          <div style="flex:1">
            <div class="wf-title">Outlier Filter</div>
            <div class="wf-desc">ลบแถวที่ Quantity ≤ 0 หรือ Unit Price ≤ 0 ออกจากชุดข้อมูล</div>
          </div>
          <span class="wf-tag">Step 2</span>
        </div>
        <div class="wf-step">
          <div class="wf-num">03</div>
          <div style="flex:1">
            <div class="wf-title">Date Normalization</div>
            <div class="wf-desc">แปลง Date → datetime64[ns] และตัดแถวที่ parse ไม่ได้ออก</div>
          </div>
          <span class="wf-tag">Step 3</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("▶  เริ่ม Clean Pipeline"):
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
        st.markdown(f"""
        <div class="success-banner">
          ✓ Pipeline สำเร็จ — <strong>ข้อมูลพร้อมใช้งาน {len(df_c):,} แถว</strong>
          (นำออก {removed} แถว)
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="kpi-row">
          <div class="kpi-card blue">
            <span class="kpi-icon">📥</span>
            <div class="kpi-label">Input</div>
            <div class="kpi-value">{len(df_b):,}</div>
            <div class="kpi-sub">แถวเริ่มต้น</div>
          </div>
          <div class="kpi-card red">
            <span class="kpi-icon">🔄</span>
            <div class="kpi-label">ลบซ้ำ</div>
            <div class="kpi-value">−{len(dup_r)}</div>
            <div class="kpi-sub">Duplicate rows</div>
          </div>
          <div class="kpi-card amber">
            <span class="kpi-icon">⚡</span>
            <div class="kpi-label">ลบ Outlier</div>
            <div class="kpi-value">−{len(wrong_r)}</div>
            <div class="kpi-sub">Invalid values</div>
          </div>
          <div class="kpi-card green">
            <span class="kpi-icon">✓</span>
            <div class="kpi-label">Output</div>
            <div class="kpi-value">{len(df_c):,}</div>
            <div class="kpi-sub">แถวพร้อมใช้</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("🔍 ดูรายละเอียดที่ถูกนำออก"):
            if not dup_r.empty:   st.markdown("**ซ้ำ:**");    st.dataframe(dup_r,   use_container_width=True)
            if not wrong_r.empty: st.markdown("**ผิดพลาด:**"); st.dataframe(wrong_r, use_container_width=True)
            if not inv_d.empty:   st.markdown("**วันที่:**");  st.dataframe(inv_d,   use_container_width=True)
        st.markdown('<div class="ct" style="margin-top:0.5rem;"><span class="ct-dot" style="background:var(--green)"></span>ข้อมูลหลัง Clean</div>', unsafe_allow_html=True)
        st.dataframe(df_c, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 — วิเคราะห์
# ─────────────────────────────────────────────────────────────────────────────
elif page == 3:
    st.markdown("""
    <div class="ph">
      <div class="ph-icon" style="background:#140E28;border-color:#251440;">⊛</div>
      <div>
        <div class="ph-title">วิเคราะห์ข้อมูลเชิงธุรกิจ</div>
        <div class="ph-desc">Monthly Trend · Top Products · Regional Performance</div>
      </div>
      <span class="ph-badge">Analytics</span>
    </div>""", unsafe_allow_html=True)

    if 'df_clean' not in st.session_state:
        st.markdown('<div class="empty-state"><span class="empty-icon">⊛</span><div class="empty-title">ยังไม่มีข้อมูลที่ผ่านการ Clean</div><div class="empty-desc">กรุณาไปที่เมนู "ทำความสะอาด" แล้วกด Pipeline ก่อน</div></div>', unsafe_allow_html=True)
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

        st.markdown(f"""
        <div class="kpi-row">
          <div class="kpi-card blue">
            <span class="kpi-icon">💰</span>
            <div class="kpi-label">ยอดขายรวม</div>
            <div class="kpi-value" style="font-size:1.35rem;">฿{total/1000:.0f}K</div>
            <div class="kpi-sub">Total revenue</div>
          </div>
          <div class="kpi-card cyan">
            <span class="kpi-icon">📅</span>
            <div class="kpi-label">เฉลี่ย/เดือน</div>
            <div class="kpi-value" style="font-size:1.35rem;">฿{avg_mo/1000:.0f}K</div>
            <div class="kpi-sub">Avg monthly</div>
          </div>
          <div class="kpi-card green">
            <span class="kpi-icon">🌏</span>
            <div class="kpi-label">ภูมิภาคนำ</div>
            <div class="kpi-value" style="font-size:1.2rem;">{best_r}</div>
            <div class="kpi-sub">Top region</div>
          </div>
          <div class="kpi-card purple">
            <span class="kpi-icon">🏆</span>
            <div class="kpi-label">สินค้าขายดีอันดับ 1</div>
            <div class="kpi-value" style="font-size:1.1rem;">{best_p}</div>
            <div class="kpi-sub">Best seller</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

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

        st.success(f"**💡 ข้อเสนอแนะ** — โปรโมชั่น **{best_p}** · เพิ่มงบภูมิภาค **{best_r}** · เตรียมสต็อกล่วงหน้า 1 เดือน")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 4 — ความปลอดภัย
# ─────────────────────────────────────────────────────────────────────────────
elif page == 4:
    st.markdown("""
    <div class="ph">
      <div class="ph-icon" style="background:#200810;border-color:#3D1020;">⊜</div>
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
          <div class="ct"><span class="ct-dot" style="background:var(--red);box-shadow:0 0 6px rgba(255,77,106,.5)"></span>Role-Based Access Control</div>
          <div class="role-row">
            <div class="role-av" style="background:#200810;border-color:#3D1020;">🔐</div>
            <div style="flex:1">
              <div class="rn">Admin</div>
              <div class="rp">ดู · เพิ่ม · แก้ไข · ลบ · จัดการผู้ใช้</div>
            </div>
            <span class="pill p-red">สูงสุด</span>
          </div>
          <div class="role-row">
            <div class="role-av" style="background:#0F1E44;border-color:#1E3360;">📊</div>
            <div style="flex:1">
              <div class="rn">Analyst</div>
              <div class="rp">ดู · ทำความสะอาด · วิเคราะห์</div>
            </div>
            <span class="pill p-blue">กลาง</span>
          </div>
          <div class="role-row">
            <div class="role-av" style="background:#071E15;border-color:#0E3828;">👁</div>
            <div style="flex:1">
              <div class="rn">Viewer</div>
              <div class="rp">ดูรายงานและ Dashboard เท่านั้น</div>
            </div>
            <span class="pill p-green">ต่ำ</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class="card">
          <div class="ct"><span class="ct-dot" style="background:var(--purple);box-shadow:0 0 6px rgba(155,109,255,.5)"></span>มาตรการป้องกัน</div>
          <div class="sec-grid">
            <div class="sec-panel">
              <div class="sec-panel-title">🔧 Technical Controls</div>
              <div class="sec-item">
                <div class="sec-ic">🔒</div>
                <div><div class="sl">Encryption AES-256</div><div class="sd">เข้ารหัสขณะจัดเก็บและส่งข้อมูล</div></div>
              </div>
              <div class="sec-item">
                <div class="sec-ic">📱</div>
                <div><div class="sl">MFA (TOTP/SMS)</div><div class="sd">ยืนยันตัวตน 2 ชั้นทุก session</div></div>
              </div>
              <div class="sec-item">
                <div class="sec-ic">📋</div>
                <div><div class="sl">Audit Logs</div><div class="sd">บันทึก action + timestamp + IP ทุกครั้ง</div></div>
              </div>
            </div>
            <div class="sec-panel">
              <div class="sec-panel-title">📋 Administrative</div>
              <div class="sec-item">
                <div class="sec-ic" style="background:var(--green-lt);color:#2EE89A;border-color:#0E3828">📝</div>
                <div><div class="sl">NDA Agreement</div><div class="sd">สัญญา NDA พนักงานทุกคน</div></div>
              </div>
              <div class="sec-item">
                <div class="sec-ic" style="background:var(--green-lt);color:#2EE89A;border-color:#0E3828">🏛</div>
                <div><div class="sl">PDPA Compliance</div><div class="sd">สอดคล้อง พ.ร.บ. คุ้มครองข้อมูลส่วนบุคคล</div></div>
              </div>
              <div class="sec-item">
                <div class="sec-ic" style="background:var(--green-lt);color:#2EE89A;border-color:#0E3828">🎓</div>
                <div><div class="sl">Security Training</div><div class="sd">อบรม Cyber Awareness ทุกปี</div></div>
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.success("✓ สอดคล้องมาตรฐาน **ISO/IEC 27001** · **PDPA** · **NIST Cybersecurity Framework**")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 5 — Visualization
# ─────────────────────────────────────────────────────────────────────────────
elif page == 5:
    st.markdown("""
    <div class="ph">
      <div class="ph-icon" style="background:#0F1E44;border-color:#1E3360;">⊝</div>
      <div>
        <div class="ph-title">Data Visualization</div>
        <div class="ph-desc">Monthly Trend · Regional Comparison · Top Products</div>
      </div>
      <span class="ph-badge">Charts</span>
    </div>""", unsafe_allow_html=True)

    if 'df_clean' not in st.session_state:
        st.markdown('<div class="empty-state"><span class="empty-icon">📊</span><div class="empty-title">ยังไม่มีข้อมูลที่พร้อมแสดงผล</div><div class="empty-desc">ไปที่เมนู "ทำความสะอาด" แล้วกด Pipeline ก่อน</div></div>', unsafe_allow_html=True)
    else:
        data = st.session_state['df_clean'].copy()
        data['Total_Sales'] = pd.to_numeric(data['Quantity'], errors='coerce') * pd.to_numeric(data['Unit Price'], errors='coerce')
        data['Month'] = data['Date'].dt.to_period('M').astype(str)
        monthly_trend = data.groupby('Month')['Total_Sales'].sum().reset_index()
        region_comp   = data.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False).reset_index()
        top5_prod     = data.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False).head(5).reset_index()

        vc1, vc2 = st.columns(2, gap="large")

        with vc1:
            st.markdown('<div class="ct"><span class="ct-dot" style="box-shadow:0 0 8px rgba(77,124,255,.6)"></span>แนวโน้มยอดขายรายเดือน</div>', unsafe_allow_html=True)
            fig1, ax1 = plt.subplots(figsize=(5.8, 3.5))
            x = range(len(monthly_trend))
            # Gradient-style fill using polygon
            ax1.fill_between(x, monthly_trend['Total_Sales'], alpha=0.12, color=PALETTE[0])
            ax1.fill_between(x, monthly_trend['Total_Sales'], alpha=0.05, color=PALETTE[1])
            ax1.plot(x, monthly_trend['Total_Sales'],
                     color=PALETTE[0], linewidth=2.5, marker='o',
                     markersize=7, markerfacecolor=BG_C, markeredgewidth=2.5,
                     markeredgecolor=PALETTE[0], zorder=5, solid_capstyle='round')
            ax1.set_xticks(x)
            ax1.set_xticklabels(monthly_trend['Month'], rotation=30, ha='right', fontsize=8)
            ax1.set_title("Monthly Sales Trend", loc='left', color='#EBF0FA', fontweight='600')
            ax1.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"฿{v/1000:.0f}K"))
            plt.tight_layout(pad=1.3)
            st.pyplot(fig1, use_container_width=True)

        with vc2:
            st.markdown('<div class="ct"><span class="ct-dot" style="background:var(--green);box-shadow:0 0 8px rgba(16,217,139,.5)"></span>ยอดขายตามภูมิภาค</div>', unsafe_allow_html=True)
            fig2, ax2 = plt.subplots(figsize=(5.8, 3.5))
            colors = [PALETTE[0]] + [PALETTE[5]] * (len(region_comp)-1)
            bars = ax2.bar(region_comp['Region'], region_comp['Total_Sales'],
                           color=colors, width=0.5, zorder=3,
                           edgecolor='none', linewidth=0)
            # Top highlight
            top_bar = bars[0]
            ax2.bar([top_bar.get_x() + top_bar.get_width()/2],
                    [top_bar.get_height()], bottom=0,
                    width=0.5, color=PALETTE[1], alpha=0.15, zorder=4)
            ax2.set_title("Sales by Region", loc='left', color='#EBF0FA', fontweight='600')
            ax2.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"฿{v/1000:.0f}K"))
            for b in bars:
                ax2.text(b.get_x() + b.get_width()/2, b.get_height()*1.04,
                         f"฿{b.get_height():,.0f}", ha='center', va='bottom',
                         fontsize=7.5, color='#6E82A8', fontweight='600')
            plt.tight_layout(pad=1.3)
            st.pyplot(fig2, use_container_width=True)

        st.markdown('<div class="ct" style="margin-top:0.5rem;"><span class="ct-dot" style="background:var(--amber);box-shadow:0 0 6px rgba(255,176,32,.4)"></span>สินค้าขายดี Top 5</div>', unsafe_allow_html=True)
        fig3, ax3 = plt.subplots(figsize=(10, 3.0))
        bar_colors = [PALETTE[1]] + [PALETTE[0]] * (len(top5_prod)-1)
        bars3 = ax3.barh(top5_prod['Product Name'][::-1], top5_prod['Quantity'][::-1],
                         color=bar_colors[::-1], height=0.5, zorder=3, edgecolor='none')
        ax3.set_title("Top 5 Products by Quantity Sold", loc='left', color='#EBF0FA', fontweight='600')
        for b in bars3:
            ax3.text(b.get_width() + 0.4, b.get_y() + b.get_height()/2,
                     f"{b.get_width():.0f} ชิ้น", va='center',
                     fontsize=9, color='#6E82A8', fontweight='600')
        ax3.set_xlim(0, top5_prod['Quantity'].max() * 1.18)
        plt.tight_layout(pad=1.3)
        st.pyplot(fig3, use_container_width=True)

        best_r = region_comp.iloc[0]['Region']
        best_p = top5_prod.iloc[0]['Product Name']
        st.success(f"**📊 Executive Summary** — ภูมิภาคหลัก: **{best_r}** · สินค้าอันดับ 1: **{best_p}** · เตรียมสต็อกตาม Peak Month")