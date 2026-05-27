"""
StyLens Enterprise Analytics Dashboard
Main entry point — Brand Overview
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import pandas as pd

from data.synthetic import engagement_data, recommendation_data, trend_data, overview_kpis
from utils.charts import format_pct, format_delta, GOLD, CREAM, MUTED, POSITIVE, NEGATIVE, OBSIDIAN

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StyLens Enterprise",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Jost:wght@300;400;500&display=swap');

  html, body, [class*="css"] {
    background-color: #0D0D0D;
    color: #F5F0E8;
    font-family: 'Jost', sans-serif;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background-color: #111111;
    border-right: 1px solid #1E1E1E;
  }
  [data-testid="stSidebar"] .stMarkdown p {
    color: #8A8A8A;
    font-size: 0.78rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }

  /* KPI cards */
  .kpi-card {
    background: #141414;
    border: 1px solid #222;
    border-radius: 4px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
  }
  .kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #C9A84C, transparent);
  }
  .kpi-label {
    font-family: 'Jost', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #8A8A8A;
    margin-bottom: 8px;
  }
  .kpi-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem;
    font-weight: 300;
    color: #F5F0E8;
    line-height: 1;
    margin-bottom: 6px;
  }
  .kpi-delta {
    font-family: 'Jost', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
  }

  /* Section headers */
  .section-header {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem;
    font-weight: 300;
    letter-spacing: 0.05em;
    color: #F5F0E8;
    margin: 32px 0 4px 0;
    border-bottom: 1px solid #1E1E1E;
    padding-bottom: 8px;
  }
  .section-sub {
    font-size: 0.75rem;
    color: #8A8A8A;
    letter-spacing: 0.08em;
    margin-bottom: 20px;
  }

  /* Wordmark */
  .wordmark {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    font-weight: 300;
    letter-spacing: 0.2em;
    color: #C9A84C;
  }
  .wordmark-sub {
    font-size: 0.6rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #8A8A8A;
    margin-top: -4px;
  }

  /* Hide default Streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="wordmark">STYLENS</div>', unsafe_allow_html=True)
    st.markdown('<div class="wordmark-sub">Enterprise Intelligence</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("**CLIENT**")
    client = st.selectbox(
        "", ["Maison Éclat", "Velour Studio", "Arroyo & Co.", "Custom Upload"],
        label_visibility="collapsed"
    )

    st.markdown("**REPORTING PERIOD**")
    months = st.slider("", min_value=3, max_value=24, value=12, step=3,
                        format="%d mo", label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**NAVIGATION**")
    st.page_link("app.py", label="✦  Overview", icon=None)
    st.page_link("pages/1_engagement.py", label="◈  Engagement")
    st.page_link("pages/2_recommendations.py", label="◉  Recommendations")
    st.page_link("pages/3_trends.py", label="◍  Trend Intelligence")

    st.markdown("---")
    st.caption(f"Data refreshed · synthetic demo\nClient: {client}")

# ── Load data ──────────────────────────────────────────────────────────────────
eng_df = engagement_data(months)
rec_df = recommendation_data(months)
kpis = overview_kpis(eng_df, rec_df)

# ── Page header ────────────────────────────────────────────────────────────────
st.markdown(f'<div class="section-header">Brand Overview</div>', unsafe_allow_html=True)
st.markdown(f'<div class="section-sub">{client} · Last {months} months · All figures reflect StyLens-attributed activity</div>', unsafe_allow_html=True)

# ── KPI row ────────────────────────────────────────────────────────────────────
k = kpis
cols = st.columns(4)

metrics = [
    ("Monthly Sessions", f"{k['total_sessions']:,}", k["sessions_delta"]),
    ("Return Rate", format_pct(k["return_rate"]), k["return_rate_delta"]),
    ("Rec. Click-Through", format_pct(k["ctr"]), k["ctr_delta"]),
    ("Revenue Influenced", f"${k['revenue_influenced']:,.0f}", k["revenue_delta"]),
]

for col, (label, value, delta) in zip(cols, metrics):
    sign, pct, color = format_delta(delta)
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-delta" style="color:{color}">{sign} {pct} vs prev mo</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Sparkline summary row ──────────────────────────────────────────────────────
import plotly.graph_objects as go
from utils.charts import apply_theme, GOLD, ACCENT_BLUE

st.markdown('<div class="section-header">12-Month Pulse</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Session volume and recommendation revenue over the reporting window</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=eng_df["month"], y=eng_df["sessions"],
        fill="tozeroy",
        mode="lines",
        line=dict(color=GOLD, width=2),
        fillcolor="rgba(201,168,76,0.10)",
        hovertemplate="%{x|%b %Y}<br><b>%{y:,} sessions</b><extra></extra>",
    ))
    apply_theme(fig, "Monthly Sessions")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=rec_df["month"], y=rec_df["revenue_influenced"],
        marker_color=ACCENT_BLUE,
        marker_line_width=0,
        hovertemplate="%{x|%b %Y}<br><b>$%{y:,.0f}</b><extra></extra>",
    ))
    apply_theme(fig2, "Revenue Influenced by StyLens ($)")
    fig2.update_layout(bargap=0.3)
    st.plotly_chart(fig2, use_container_width=True)

# ── Style match score callout ──────────────────────────────────────────────────
score = kpis["style_match_score"]
bar_pct = int(score * 100)

st.markdown('<div class="section-header">Style Match Score</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Aggregate alignment between StyLens recommendations and confirmed purchase behavior</div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="background:#141414; border:1px solid #222; border-radius:4px; padding:24px 28px;">
  <div style="display:flex; align-items:baseline; gap:16px; margin-bottom:16px;">
    <span style="font-family:'Cormorant Garamond',serif; font-size:3.5rem; font-weight:300; color:#F5F0E8;">{bar_pct}</span>
    <span style="font-size:1.2rem; color:#C9A84C; font-family:'Jost',sans-serif;">/ 100</span>
    <span style="font-size:0.75rem; color:#8A8A8A; letter-spacing:0.1em; text-transform:uppercase; margin-left:8px;">Style Match Index</span>
  </div>
  <div style="background:#1E1E1E; border-radius:2px; height:6px; width:100%;">
    <div style="background:linear-gradient(90deg,#C9A84C,#E8D5A3); width:{bar_pct}%; height:100%; border-radius:2px;"></div>
  </div>
  <div style="display:flex; justify-content:space-between; margin-top:6px;">
    <span style="font-size:0.65rem; color:#555; letter-spacing:0.08em;">0</span>
    <span style="font-size:0.65rem; color:#555; letter-spacing:0.08em;">100</span>
  </div>
</div>
""", unsafe_allow_html=True)
