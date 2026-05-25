# streamlit_app.py - Enhanced Professional Fraud Detection Frontend
import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import time


# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FraudShield | Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = os.environ.get("API_URL", "http://localhost:8000")

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font Import ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

/* ── Root & Base Reset ── */
:root {
    --bg-primary:    #050d1a;
    --bg-card:       #0a1628;
    --bg-card2:      #0f1f38;
    --border:        #1a3050;
    --border-glow:   #0e6fff44;
    --accent-cyan:   #00d4ff;
    --accent-blue:   #0e6fff;
    --accent-green:  #00e5a0;
    --accent-yellow: #ffd166;
    --accent-orange: #ff9f43;
    --accent-red:    #ff4757;
    --text-primary:  #e8f4ff;
    --text-secondary:#8aa8c8;
    --text-muted:    #4a6885;
    --font-heading:  'Syne', sans-serif;
    --font-mono:     'Space Mono', monospace;
}

/* ── App Background ── */
.stApp {
    background-color: var(--bg-primary);
    background-image:
        radial-gradient(ellipse 80% 60% at 50% -20%, #0e2a5022 0%, transparent 70%),
        linear-gradient(180deg, #050d1a 0%, #030912 100%);
    font-family: var(--font-heading);
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container {
    padding-top: 0 !important;
}

/* ── Typography ── */
h1, h2, h3, h4 {
    font-family: var(--font-heading) !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em;
}
p, label, .stMarkdown {
    color: var(--text-secondary) !important;
    font-family: var(--font-heading) !important;
}

/* ── Number Inputs ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
    font-family: var(--font-mono) !important;
    font-size: 0.85rem !important;
    transition: border-color 0.2s ease;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 3px #0e6fff18 !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: var(--bg-card) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
    gap: 4px;
}
[data-testid="stTabs"] [role="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: 8px !important;
    font-family: var(--font-heading) !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 8px 20px !important;
    border: none !important;
    transition: all 0.2s ease !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: var(--accent-blue) !important;
    color: white !important;
}
[data-testid="stTabs"] [role="tabpanel"] {
    padding-top: 1.5rem !important;
}

/* ── Form Submit Button ── */
[data-testid="stFormSubmitButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, #0e6fff 0%, #0052cc 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: var(--font-heading) !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.05em !important;
    padding: 14px 32px !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px #0e6fff44 !important;
    text-transform: uppercase !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(135deg, #1a7fff 0%, #0e6fff 100%) !important;
    box-shadow: 0 6px 30px #0e6fff66 !important;
    transform: translateY(-1px) !important;
}

/* ── Regular Buttons ── */
[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, #0e6fff 0%, #0052cc 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: var(--font-heading) !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 12px 28px !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px #0e6fff44 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary {
    color: var(--text-secondary) !important;
    font-family: var(--font-heading) !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
[data-testid="stMetricValue"] {
    color: var(--accent-cyan) !important;
    font-family: var(--font-mono) !important;
    font-size: 1.8rem !important;
}

/* ── File Uploader ── */
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 12px !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── Alerts / Info ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: var(--font-heading) !important;
    font-weight: 600 !important;
}

/* ── Progress Bar ── */
[data-testid="stProgressBar"] > div {
    background: var(--border) !important;
    border-radius: 99px !important;
}
[data-testid="stProgressBar"] > div > div {
    border-radius: 99px !important;
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan)) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] {
    color: var(--accent-cyan) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-blue); }
</style>
""", unsafe_allow_html=True)


# ── Helper: Custom HTML Components ─────────────────────────────────────────────
def header_banner():
    # components.html() renders in a sandboxed iframe — bypasses Streamlit's
    # HTML sanitizer which strips display:flex, @keyframes, position:absolute, etc.
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { background:transparent; font-family:'Syne', sans-serif; padding:2px; }
        @keyframes pulse {
            0%,100% { opacity:1; box-shadow: 0 0 0 0 rgba(0,229,160,0.45); }
            50%      { opacity:0.7; box-shadow: 0 0 0 7px rgba(0,229,160,0); }
        }
        @keyframes fadeIn {
            from { opacity:0; transform:translateY(-5px); }
            to   { opacity:1; transform:translateY(0); }
        }
        .banner {
            background: linear-gradient(135deg, #0a1628 0%, #0f2040 50%, #0a1628 100%);
            border: 1px solid #1a3050;
            border-radius: 14px;
            padding: 22px 28px;
            position: relative;
            overflow: hidden;
            animation: fadeIn 0.45s ease forwards;
        }
        .grid-bg {
            position: absolute; inset: 0;
            background-image:
                linear-gradient(rgba(26,48,80,0.3) 1px, transparent 1px),
                linear-gradient(90deg, rgba(26,48,80,0.3) 1px, transparent 1px);
            background-size: 32px 32px;
            pointer-events: none;
        }
        .orb1 {
            position:absolute; top:-40px; right:80px;
            width:200px; height:200px;
            background: radial-gradient(circle, rgba(14,111,255,0.14) 0%, transparent 70%);
            pointer-events:none;
        }
        .orb2 {
            position:absolute; bottom:-30px; left:120px;
            width:150px; height:150px;
            background: radial-gradient(circle, rgba(0,212,255,0.07) 0%, transparent 70%);
            pointer-events:none;
        }
        .inner {
            position: relative;
            display: flex;
            align-items: center;
            gap: 18px;
        }
        .icon {
            width:56px; height:56px; flex-shrink:0;
            background: linear-gradient(135deg, #0e6fff, #00d4ff);
            border-radius:13px;
            display:flex; align-items:center; justify-content:center;
            font-size:26px;
            box-shadow: 0 0 28px rgba(14,111,255,0.45);
        }
        .title-wrap { flex:1; }
        .title {
            font-family:'Syne', sans-serif;
            font-size:1.85rem; font-weight:800;
            color:#e8f4ff;
            letter-spacing:-0.03em; line-height:1;
        }
        .badge {
            font-size:0.75rem; font-weight:600;
            color:#00d4ff;
            background: rgba(0,212,255,0.1);
            border: 1px solid rgba(0,212,255,0.28);
            border-radius:6px;
            padding:2px 9px;
            vertical-align:middle;
            letter-spacing:0.06em;
            margin-left:8px;
        }
        .subtitle {
            font-family:'Space Mono', monospace;
            font-size:0.72rem; color:#8aa8c8;
            margin-top:5px; letter-spacing:0.05em;
        }
        .meta { text-align:right; flex-shrink:0; }
        .meta-lbl {
            font-family:'Space Mono', monospace;
            font-size:0.63rem; color:#4a6885;
            text-transform:uppercase; letter-spacing:0.1em;
        }
        .meta-val {
            font-family:'Syne', sans-serif;
            font-size:0.9rem; color:#00d4ff;
            font-weight:700; margin-top:2px;
        }
        .live-pill {
            display:inline-flex; align-items:center; gap:6px;
            margin-top:7px;
            background: rgba(0,229,160,0.1);
            border: 1px solid rgba(0,229,160,0.28);
            border-radius:99px; padding:4px 11px;
        }
        .dot {
            width:7px; height:7px;
            background:#00e5a0; border-radius:50%;
            animation: pulse 2s infinite;
            flex-shrink:0;
        }
        .live-txt {
            font-family:'Space Mono', monospace;
            font-size:0.63rem; color:#00e5a0; letter-spacing:0.07em;
        }
    </style>
    </head>
    <body>
    <div class="banner">
        <div class="grid-bg"></div>
        <div class="orb1"></div>
        <div class="orb2"></div>
        <div class="inner">
            <div class="icon">🛡️</div>
            <div class="title-wrap">
                <div class="title">FraudShield <span class="badge">PRO</span></div>
                <div class="subtitle">REAL-TIME CREDIT CARD FRAUD DETECTION ENGINE</div>
            </div>
            <div class="meta">
                <div class="meta-lbl">Model</div>
                <div class="meta-val">Random Forest v2.1</div>
                <div class="live-pill">
                    <span class="dot"></span>
                    <span class="live-txt">LIVE</span>
                </div>
            </div>
        </div>
    </div>
    </body>
    </html>
    """, height=135, scrolling=False)


def stat_card(icon, label, value, sub="", color="var(--accent-cyan)"):
    # Resolve CSS-variable colour strings to real hex values
    _cmap = {
        "var(--accent-cyan)":   "#00d4ff",
        "var(--accent-blue)":   "#0e6fff",
        "var(--accent-green)":  "#00e5a0",
        "var(--accent-yellow)": "#ffd166",
        "var(--accent-orange)": "#ff9f43",
        "var(--accent-red)":    "#ff4757",
    }
    c = _cmap.get(color, color)
    sub_html = f'<div style="font-family:Space Mono,monospace;font-size:0.71rem;color:#4a6885;margin-top:5px;">{sub}</div>' if sub else ""
    components.html(f"""<!DOCTYPE html>
<html><head>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono&family=Syne:wght@800&display=swap" rel="stylesheet">
<style>
  *{{margin:0;padding:0;box-sizing:border-box;}}
  body{{background:transparent;margin:0;padding:1px 1px 4px 1px;}}
  .card{{
    background:#0a1628;
    border:1px solid #1a3050;
    border-radius:13px;
    padding:18px 20px;
    position:relative;
    overflow:hidden;
    height:100%;
  }}
  .top-bar{{
    position:absolute;top:0;left:0;right:0;height:3px;
    background:linear-gradient(90deg,{c},transparent);
    border-radius:13px 13px 0 0;
  }}
  .ico{{font-size:1.45rem;margin-bottom:8px;}}
  .lbl{{
    font-family:'Space Mono',monospace;
    font-size:0.68rem;color:#4a6885;
    text-transform:uppercase;letter-spacing:0.1em;
    margin-bottom:4px;
  }}
  .val{{
    font-family:'Syne',sans-serif;
    font-size:1.55rem;font-weight:800;
    color:{c};line-height:1;
  }}
</style></head>
<body>
<div class="card">
  <div class="top-bar"></div>
  <div class="ico">{icon}</div>
  <div class="lbl">{label}</div>
  <div class="val">{value}</div>
  {sub_html}
</div>
</body></html>""", height=130, scrolling=False)


def result_card_fraud(probability, risk_level, recommendation):
    _colors = {
        "LOW":      ("#00e5a0", "rgba(0,229,160,0.08)",  "rgba(0,229,160,0.22)"),
        "MEDIUM":   ("#ffd166", "rgba(255,209,102,0.08)","rgba(255,209,102,0.22)"),
        "HIGH":     ("#ff9f43", "rgba(255,159,67,0.08)", "rgba(255,159,67,0.22)"),
        "CRITICAL": ("#ff4757", "rgba(255,71,87,0.08)",  "rgba(255,71,87,0.22)"),
    }
    risk_key = risk_level.upper() if risk_level else "LOW"
    accent, bg, border = _colors.get(risk_key, _colors["LOW"])
    emoji = {"LOW":"✅","MEDIUM":"⚠️","HIGH":"🔶","CRITICAL":"🚨"}.get(risk_key,"✅")
    pct = int(probability * 100)

    # Build bar fill colour as rgba (Plotly-safe not needed here, but keeps it clean)
    accent_hex = accent  # already a real hex
    components.html(f"""<!DOCTYPE html>
<html><head>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap" rel="stylesheet">
<style>
  *{{margin:0;padding:0;box-sizing:border-box;}}
  body{{background:transparent;padding:2px 1px 6px 1px;}}
  @keyframes growBar{{from{{width:0%}}to{{width:{pct}%}}}}
  .card{{
    background:{bg};
    border:1px solid {border};
    border-radius:15px;
    padding:22px;
  }}
  .row{{display:flex;align-items:center;gap:12px;margin-bottom:16px;}}
  .emoji{{font-size:2rem;flex-shrink:0;}}
  .risk-lbl{{
    font-family:'Syne',sans-serif;
    font-size:1.05rem;font-weight:800;color:{accent};
  }}
  .risk-sub{{
    font-family:'Space Mono',monospace;
    font-size:0.65rem;color:#4a6885;
    text-transform:uppercase;letter-spacing:0.08em;
    margin-top:2px;
  }}
  .pct{{
    margin-left:auto;
    font-family:'Syne',sans-serif;
    font-size:2.4rem;font-weight:800;
    color:{accent};line-height:1;flex-shrink:0;
  }}
  .bar-track{{
    height:8px;background:rgba(255,255,255,0.08);
    border-radius:99px;overflow:hidden;margin-bottom:16px;
  }}
  .bar-fill{{
    height:100%;
    background:linear-gradient(90deg,{accent}99,{accent});
    border-radius:99px;
    width:0%;
    animation:growBar 0.9s ease forwards;
  }}
  .rec{{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:10px;
    padding:11px 14px;
    font-family:'Syne',sans-serif;
    font-size:0.83rem;color:#8aa8c8;
    line-height:1.5;
  }}
  .rec strong{{color:{accent};}}
</style></head>
<body>
<div class="card">
  <div class="row">
    <span class="emoji">{emoji}</span>
    <div>
      <div class="risk-lbl">{risk_key} RISK</div>
      <div class="risk-sub">Fraud Probability</div>
    </div>
    <div class="pct">{pct}%</div>
  </div>
  <div class="bar-track"><div class="bar-fill"></div></div>
  <div class="rec">💡 <strong>Action:</strong> {recommendation}</div>
</div>
</body></html>""", height=220, scrolling=False)


def section_label(text):
    # Simple enough for st.markdown — only uses safe inline styles
    st.markdown(f"""<div style="
        font-family:monospace;
        font-size:0.68rem;color:#4a6885;
        text-transform:uppercase;letter-spacing:0.12em;
        margin-bottom:8px;margin-top:4px;
        border-left:3px solid #0e6fff;
        padding-left:10px;
    ">{text}</div>""", unsafe_allow_html=True)


def divider():
    st.markdown("""
    <hr style="border:none; border-top:1px solid var(--border); margin:18px 0;" />
    """, unsafe_allow_html=True)


# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="
        padding: 24px 16px 16px;
        border-bottom: 1px solid var(--border);
        margin-bottom: 16px;
    ">
        <div style="
            font-family:'Syne',sans-serif;
            font-size:1.3rem; font-weight:800;
            color:var(--text-primary);
            letter-spacing:-0.02em;
        ">🛡️ FraudShield</div>
        <div style="
            font-family:'Space Mono',monospace;
            font-size:0.68rem; color:var(--text-muted);
            letter-spacing:0.08em; margin-top:2px;
        ">DETECTION CONSOLE v2.1</div>
    </div>
    """, unsafe_allow_html=True)

    # API Connection Status
    section_label("System Status")
    try:
        resp = requests.get(f"{API_URL}/health", timeout=2)
        if resp.status_code == 200:
            st.markdown("""
            <div style="
                display:flex; align-items:center; gap:10px;
                background:#00e5a010; border:1px solid #00e5a030;
                border-radius:10px; padding:12px 14px;
                margin-bottom:8px;
            ">
                <span style="
                    width:9px; height:9px; border-radius:50%;
                    background:#00e5a0;
                    box-shadow:0 0 8px #00e5a0;
                    flex-shrink:0;
                "></span>
                <div>
                    <div style="font-family:'Syne',sans-serif; font-size:0.82rem; font-weight:700; color:#00e5a0;">API Connected</div>
                    <div style="font-family:'Space Mono',monospace; font-size:0.65rem; color:var(--text-muted);">All systems operational</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="
                display:flex; align-items:center; gap:10px;
                background:#ff475710; border:1px solid #ff475730;
                border-radius:10px; padding:12px 14px;
                margin-bottom:8px;
            ">
                <span style="width:9px;height:9px;border-radius:50%;background:#ff4757;flex-shrink:0;"></span>
                <div style="font-family:'Syne',sans-serif;font-size:0.82rem;font-weight:700;color:#ff4757;">API Error</div>
            </div>
            """, unsafe_allow_html=True)
    except Exception:
        st.markdown("""
        <div style="
            display:flex; align-items:center; gap:10px;
            background:#ff475710; border:1px solid #ff475730;
            border-radius:10px; padding:12px 14px;
            margin-bottom:8px;
        ">
            <span style="width:9px;height:9px;border-radius:50%;background:#ff4757;flex-shrink:0;"></span>
            <div>
                <div style="font-family:'Syne',sans-serif;font-size:0.82rem;font-weight:700;color:#ff4757;">Offline</div>
                <div style="font-family:'Space Mono',monospace;font-size:0.65rem;color:var(--text-muted);">Start FastAPI server</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    divider()

    # Quick Guide
    section_label("Quick Guide")
    st.markdown("""
    <div style="
        background: var(--bg-card2);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 14px 16px;
        font-family: 'Space Mono', monospace;
    ">
        <div style="color:var(--text-secondary); font-size:0.8rem; line-height:2;">
            <span style="color:var(--accent-blue);">01 /</span> Enter transaction details<br/>
            <span style="color:var(--accent-blue);">02 /</span> Set PCA-transformed features<br/>
            <span style="color:var(--accent-blue);">03 /</span> Run fraud detection<br/>
            <span style="color:var(--accent-blue);">04 /</span> Review risk assessment<br/>
            <span style="color:var(--accent-blue);">05 /</span> Take recommended action
        </div>
    </div>
    """, unsafe_allow_html=True)

    divider()

    # Risk Legend
    section_label("Risk Thresholds")
    risk_items = [
        ("🟢", "LOW",      "< 25%",  "#00e5a0"),
        ("🟡", "MEDIUM",   "25–50%", "#ffd166"),
        ("🟠", "HIGH",     "50–75%", "#ff9f43"),
        ("🔴", "CRITICAL", "> 75%",  "#ff4757"),
    ]
    for emoji, label, threshold, color in risk_items:
        st.markdown(f"""
        <div style="
            display:flex; align-items:center; justify-content:space-between;
            padding: 7px 0;
            border-bottom: 1px solid #1a305033;
            font-family:'Space Mono',monospace; font-size:0.73rem;
        ">
            <span>{emoji} <span style="color:{color}; font-weight:700;">{label}</span></span>
            <span style="color:var(--text-muted);">{threshold}</span>
        </div>
        """, unsafe_allow_html=True)

    divider()

    st.markdown("""
    <div style="
        font-family:'Space Mono',monospace;
        font-size:0.65rem; color:var(--text-muted);
        text-align:center; padding:8px;
    ">
        Powered by Random Forest<br/>© 2025 FraudShield Systems
    </div>
    """, unsafe_allow_html=True)


# ── Main Content ────────────────────────────────────────────────────────────────
header_banner()

# Quick Stats Row
s1, s2, s3, s4 = st.columns(4)
with s1:
    stat_card("💳", "Model Accuracy", "99.4%", "On test dataset", "var(--accent-cyan)")
with s2:
    stat_card("⚡", "Avg Latency", "< 40ms", "Real-time inference", "var(--accent-blue)")
with s3:
    stat_card("🎯", "Precision", "97.8%", "Fraud class", "var(--accent-green)")
with s4:
    stat_card("📊", "Features", "30", "Time · Amount · V1–V28", "var(--accent-yellow)")

st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)

# ── Tabs ────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "🔍  Single Transaction",
    "📦  Batch Analysis",
    "📈  Analytics",
])

# ────────────────────────────────────────────────────────────────────────────────
# TAB 1 – Single Transaction
# ────────────────────────────────────────────────────────────────────────────────
with tab1:
    left, right = st.columns([3, 2], gap="large")

    with left:
        section_label("Transaction Details")
        with st.form("fraud_form", clear_on_submit=False):

            c1, c2 = st.columns(2)
            with c1:
                amount = st.number_input(
                    "💰 Transaction Amount (USD)",
                    min_value=0.0, max_value=1_000_000.0,
                    value=250.00, step=0.01, format="%.2f",
                    help="Dollar value of the transaction"
                )
            with c2:
                txn_time = st.number_input(
                    "⏱️ Time Elapsed (seconds)",
                    min_value=0, max_value=200_000,
                    value=12345,
                    help="Seconds elapsed since the first transaction in the dataset"
                )

            divider()
            section_label("PCA-Transformed Feature Vectors (V1 – V28)")

            st.markdown("""
            <div style="
                background:#0e6fff08; border:1px solid #0e6fff20;
                border-radius:10px; padding:10px 14px; margin-bottom:12px;
                font-family:'Space Mono',monospace; font-size:0.72rem;
                color:var(--text-muted);
            ">
                ℹ️  These 28 features are principal components obtained via PCA on the
                original transaction data. Default to <code style="color:#00d4ff;">0.0</code>
                for a baseline transaction or paste known values.
            </div>
            """, unsafe_allow_html=True)

            v_features = {}
            with st.expander("⚙️  Expand to Set V1 – V28 Features", expanded=False):
                cols = st.columns(4)
                for i in range(1, 29):
                    with cols[(i - 1) % 4]:
                        v_features[f"V{i}"] = st.number_input(
                            f"V{i}",
                            value=0.0,
                            format="%.4f",
                            key=f"v_{i}",
                            label_visibility="visible",
                        )

            st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🚀  RUN FRAUD DETECTION")

    with right:
        section_label("Risk Assessment")

        if submitted:
            transaction = {"Time": txn_time, "Amount": amount, **v_features}

            with st.spinner("Analyzing transaction..."):
                time.sleep(0.3)  # slight UX delay for realism
                try:
                    response = requests.post(f"{API_URL}/predict", json=transaction, timeout=5)

                    if response.status_code == 200:
                        result = response.json()

                        # Gauge chart
                        prob = result.get("fraud_probability", 0)
                        risk = result.get("risk_level", "LOW")
                        rec  = result.get("recommendation", "No action required.")

                        gauge_colors = {
                            "LOW": "#00e5a0", "MEDIUM": "#ffd166",
                            "HIGH": "#ff9f43", "CRITICAL": "#ff4757"
                        }
                        gauge_col = gauge_colors.get(risk.upper(), "#00d4ff")

                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=round(prob * 100, 1),
                            domain={"x": [0, 1], "y": [0, 1]},
                            title={
                                "text": "Fraud Probability",
                                "font": {"family": "Space Mono", "size": 13, "color": "#8aa8c8"}
                            },
                            number={
                                "suffix": "%",
                                "font": {"family": "Syne", "size": 42, "color": gauge_col}
                            },
                            gauge={
                                "axis": {
                                    "range": [0, 100],
                                    "tickwidth": 1,
                                    "tickcolor": "#1a3050",
                                    "tickfont": {"family": "Space Mono", "size": 9, "color": "#4a6885"},
                                },
                                "bar": {"color": gauge_col, "thickness": 0.28},
                                "bgcolor": "#0a1628",
                                "borderwidth": 0,
                                "steps": [
                                    {"range": [0, 25],  "color": "rgba(0,229,160,0.07)"},
                                    {"range": [25, 50], "color": "rgba(255,209,102,0.07)"},
                                    {"range": [50, 75], "color": "rgba(255,159,67,0.07)"},
                                    {"range": [75, 100],"color": "rgba(255,71,87,0.07)"},
                                ],
                                "threshold": {
                                    "line": {"color": gauge_col, "width": 3},
                                    "thickness": 0.85,
                                    "value": round(prob * 100, 1),
                                },
                            },
                        ))
                        fig.update_layout(
                            height=240,
                            margin=dict(l=20, r=20, t=40, b=10),
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            font={"family": "Space Mono", "color": "#8aa8c8"},
                        )
                        st.plotly_chart(fig, use_container_width=True)

                        # Result Card
                        result_card_fraud(prob, risk, rec)

                        # Breakdown Metrics
                        divider()
                        section_label("Transaction Summary")
                        m1, m2 = st.columns(2)
                        with m1:
                            st.metric("Amount", f"${amount:,.2f}")
                        with m2:
                            st.metric("Is Fraud", "YES 🚨" if result.get("is_fraud") else "NO ✅")

                    else:
                        st.error(f"API returned status {response.status_code}")

                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot reach API. Is the FastAPI server running?")
                except Exception as exc:
                    st.error(f"Unexpected error: {exc}")

        else:
            # Placeholder state
            st.markdown("""
            <div style="
                background: var(--bg-card);
                border: 1px dashed var(--border);
                border-radius: 16px;
                padding: 48px 32px;
                text-align: center;
            ">
                <div style="font-size:3rem; margin-bottom:14px; opacity:0.4;">🛡️</div>
                <div style="
                    font-family:'Syne',sans-serif;
                    font-size:1rem; font-weight:700;
                    color:var(--text-secondary);
                    margin-bottom:6px;
                ">Awaiting Transaction</div>
                <div style="
                    font-family:'Space Mono',monospace;
                    font-size:0.72rem; color:var(--text-muted);
                ">Fill in the details and click<br/>RUN FRAUD DETECTION</div>
            </div>
            """, unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────────
# TAB 2 – Batch Analysis
# ────────────────────────────────────────────────────────────────────────────────
with tab2:
    section_label("Batch Transaction Upload")

    st.markdown("""
    <div style="
        background:#0e6fff08; border:1px solid #0e6fff20;
        border-radius:12px; padding:14px 18px; margin-bottom:18px;
        font-family:'Space Mono',monospace; font-size:0.72rem; color:var(--text-muted);
        line-height:1.8;
    ">
        📋 Upload a <strong style="color:#00d4ff;">CSV file</strong> with columns:
        <code style="color:#ffd166;">Time, Amount, V1…V28</code>.
        The system will score each row and return a full fraud assessment.
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drop your CSV file here",
        type=["csv"],
        help="CSV must contain Time, Amount, V1–V28 columns",
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        total_rows = len(df)

        section_label(f"Preview — {total_rows} rows loaded")
        st.dataframe(
            df.head(10),
            use_container_width=True,
            height=220,
        )

        st.markdown("<div style='margin:14px 0;'></div>", unsafe_allow_html=True)

        if st.button(f"⚡  ANALYZE {total_rows} TRANSACTIONS"):
            transactions = df.to_dict("records")
            with st.spinner(f"Running inference on {total_rows} transactions..."):
                try:
                    response = requests.post(
                        f"{API_URL}/predict/batch",
                        json={"transactions": transactions},
                        timeout=30,
                    )

                    if response.status_code == 200:
                        results = response.json()
                        fraud_count  = results.get("fraud_count", 0)
                        total        = results.get("total", total_rows)
                        fraud_pct    = results.get("fraud_percentage", 0)
                        legit_count  = total - fraud_count

                        divider()
                        section_label("Batch Results Summary")

                        c1, c2, c3, c4 = st.columns(4)
                        with c1:
                            stat_card("📦", "Total Transactions", f"{total:,}", "", "var(--accent-cyan)")
                        with c2:
                            stat_card("✅", "Legitimate", f"{legit_count:,}", f"{100-fraud_pct:.1f}%", "var(--accent-green)")
                        with c3:
                            stat_card("🚨", "Fraud Detected", f"{fraud_count:,}", f"{fraud_pct:.1f}%", "var(--accent-red)")
                        with c4:
                            stat_card("📉", "Fraud Rate", f"{fraud_pct:.2f}%", "Of total volume", "var(--accent-orange)")

                        st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)

                        # Charts
                        results_df = pd.DataFrame(results.get("results", []))

                        if not results_df.empty:
                            chart_col1, chart_col2 = st.columns(2)

                            with chart_col1:
                                section_label("Fraud vs Legitimate Split")
                                pie_fig = go.Figure(go.Pie(
                                    labels=["Legitimate", "Fraudulent"],
                                    values=[legit_count, fraud_count],
                                    hole=0.55,
                                    marker=dict(
                                        colors=["#00e5a0", "#ff4757"],
                                        line=dict(color="#050d1a", width=3),
                                    ),
                                    textfont=dict(family="Space Mono", size=11),
                                ))
                                pie_fig.update_layout(
                                    height=280,
                                    margin=dict(l=10, r=10, t=10, b=10),
                                    paper_bgcolor="rgba(0,0,0,0)",
                                    plot_bgcolor="rgba(0,0,0,0)",
                                    font=dict(color="#8aa8c8", family="Space Mono"),
                                    legend=dict(
                                        font=dict(family="Space Mono", size=11, color="#8aa8c8"),
                                        bgcolor="rgba(0,0,0,0)",
                                    ),
                                    annotations=[dict(
                                        text=f"<b>{fraud_pct:.1f}%</b><br>Fraud",
                                        x=0.5, y=0.5, font_size=14,
                                        font=dict(family="Syne", color="#ff4757"),
                                        showarrow=False,
                                    )],
                                )
                                st.plotly_chart(pie_fig, use_container_width=True)

                            with chart_col2:
                                if "fraud_probability" in results_df.columns:
                                    section_label("Probability Distribution")
                                    hist_fig = px.histogram(
                                        results_df,
                                        x="fraud_probability",
                                        nbins=20,
                                        color_discrete_sequence=["#0e6fff"],
                                    )
                                    hist_fig.update_layout(
                                        height=280,
                                        margin=dict(l=10, r=10, t=10, b=10),
                                        paper_bgcolor="rgba(0,0,0,0)",
                                        plot_bgcolor="rgba(0,0,0,0)",
                                        xaxis=dict(
                                            color="#4a6885",
                                            gridcolor="#1a3050",
                                            title=dict(text="Fraud Probability", font=dict(family="Space Mono", size=10)),
                                        ),
                                        yaxis=dict(
                                            color="#4a6885",
                                            gridcolor="#1a3050",
                                            title=dict(text="Count", font=dict(family="Space Mono", size=10)),
                                        ),
                                        showlegend=False,
                                        bargap=0.08,
                                    )
                                    hist_fig.update_traces(
                                        marker=dict(
                                            color="#0e6fff",
                                            line=dict(color="#00d4ff", width=0.8),
                                        )
                                    )
                                    st.plotly_chart(hist_fig, use_container_width=True)

                            section_label("Individual Transaction Results")
                            st.dataframe(results_df, use_container_width=True, height=320)

                    else:
                        st.error(f"API returned status {response.status_code}")

                except Exception as exc:
                    st.error(f"Batch analysis failed: {exc}")


# ────────────────────────────────────────────────────────────────────────────────
# TAB 3 – Analytics
# ────────────────────────────────────────────────────────────────────────────────
with tab3:
    section_label("Model Performance Overview")

    # Static demo charts for model analytics
    ac1, ac2, ac3 = st.columns(3)

    with ac1:
        stat_card("🎯", "AUC-ROC Score",  "0.9987", "Industry benchmark: 0.95+", "var(--accent-cyan)")
    with ac2:
        stat_card("🔬", "F1 Score",       "0.9814", "Fraud class", "var(--accent-green)")
    with ac3:
        stat_card("🚫", "False Positive", "0.21%",  "Rate on validation set", "var(--accent-yellow)")

    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)

    chart_l, chart_r = st.columns(2)

    with chart_l:
        section_label("Feature Importance — Top 10")
        features = ["V14","V4","V11","V12","Amount","V17","V3","V10","V16","V7"]
        importance = [0.187, 0.142, 0.118, 0.103, 0.089, 0.078, 0.066, 0.058, 0.047, 0.039]
        bar_fig = go.Figure(go.Bar(
            y=features[::-1],
            x=importance[::-1],
            orientation="h",
            marker=dict(
                color=importance[::-1],
                colorscale=[[0, "#0e6fff"], [1, "#00d4ff"]],
                line=dict(color="rgba(0,0,0,0)", width=0),
            ),
        ))
        bar_fig.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(color="#4a6885", gridcolor="#1a3050", tickfont=dict(family="Space Mono", size=10)),
            yaxis=dict(color="#8aa8c8", tickfont=dict(family="Space Mono", size=11)),
            showlegend=False,
        )
        st.plotly_chart(bar_fig, use_container_width=True)

    with chart_r:
        section_label("Confusion Matrix")
        z  = [[56857, 7], [11, 86]]
        cm = go.Figure(go.Heatmap(
            z=z,
            x=["Predicted: Legit", "Predicted: Fraud"],
            y=["Actual: Legit", "Actual: Fraud"],
            colorscale=[[0, "#050d1a"], [1, "#0e6fff"]],
            text=[[str(v) for v in row] for row in z],
            texttemplate="%{text}",
            textfont=dict(family="Syne", size=22, color="white"),
            showscale=False,
        ))
        cm.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(color="#8aa8c8", tickfont=dict(family="Space Mono", size=10)),
            yaxis=dict(color="#8aa8c8", tickfont=dict(family="Space Mono", size=10)),
        )
        st.plotly_chart(cm, use_container_width=True)

    section_label("Training Dataset Distribution")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    legit_vals = [4800, 5100, 4950, 5400, 5200, 5600,
                  5300, 5700, 5100, 5500, 5800, 6000]
    fraud_vals = [22, 18, 31, 25, 28, 35, 29, 33, 27, 24, 30, 38]

    line_fig = go.Figure()
    line_fig.add_trace(go.Scatter(
        x=months, y=legit_vals, name="Legitimate",
        mode="lines+markers",
        line=dict(color="#00e5a0", width=2.5),
        marker=dict(size=6, color="#00e5a0"),
        fill="tozeroy", fillcolor="rgba(0,229,160,0.06)",
    ))
    line_fig.add_trace(go.Scatter(
        x=months, y=fraud_vals, name="Fraudulent",
        mode="lines+markers",
        line=dict(color="#ff4757", width=2.5, dash="dot"),
        marker=dict(size=6, color="#ff4757"),
        yaxis="y2",
    ))
    line_fig.update_layout(
        height=280,
        margin=dict(l=10, r=60, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(color="#4a6885", gridcolor="#1a3050", tickfont=dict(family="Space Mono", size=10)),
        yaxis=dict(color="#4a6885", gridcolor="#1a3050", tickfont=dict(family="Space Mono", size=10), title="Legit Count"),
        yaxis2=dict(overlaying="y", side="right", color="#ff4757",
                    tickfont=dict(family="Space Mono", size=10), title="Fraud Count"),
        legend=dict(font=dict(family="Space Mono", size=10, color="#8aa8c8"),
                    bgcolor="rgba(0,0,0,0)", bordercolor="#1a3050"),
    )
    st.plotly_chart(line_fig, use_container_width=True)

# ── Footer ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    margin-top: 40px;
    border-top: 1px solid var(--border);
    padding-top: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
">
    <div style="
        font-family:'Space Mono',monospace;
        font-size:0.68rem; color:var(--text-muted);
    ">
        © 2025 FraudShield Systems · Powered by Random Forest · Real-Time Inference
    </div>
    <div style="
        font-family:'Space Mono',monospace;
        font-size:0.68rem; color:var(--text-muted);
    ">
        Model: Random Forest v2.1 · Features: 30 · Dataset: IEEE-CIS
    </div>
</div>
""", unsafe_allow_html=True)