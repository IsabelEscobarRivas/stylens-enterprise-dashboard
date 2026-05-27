"""
StyLens Enterprise — Page 3: Trend Intelligence
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from data.synthetic import trend_data
from utils.charts import apply_theme, multi_line_chart, TREND_COLORS, GOLD, NEGATIVE, POSITIVE, MUTED

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Jost:wght@300;400;500&display=swap');
  html, body, [class*="css"] { background-color: #0D0D0D; color: #F5F0E8; font-family: 'Jost', sans-serif; }
  [data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #1E1E1E; }
  .section-header { font-family: 'Cormorant Garamond', serif; font-size: 1.4rem; font-weight: 300; color: #F5F0E8; margin: 32px 0 4px 0; border-bottom: 1px solid #1E1E1E; padding-bottom: 8px; }
  .section-sub { font-size: 0.75rem; color: #8A8A8A; letter-spacing: 0.08em; margin-bottom: 20px; }
  .wordmark { font-family: 'Cormorant Garamond', serif; font-size: 1.6rem; font-weight: 300; letter-spacing: 0.2em; color: #C9A84C; }
  .wordmark-sub { font-size: 0.6rem; letter-spacing: 0.25em; text-transform: uppercase; color: #8A8A8A; }
  .gap-chip { display:inline-block; padding:4px 12px; border-radius:2px; font-size:0.72rem; letter-spacing:0.08em; margin:2px; font-family:'Jost',sans-serif; }
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="wordmark">STYLENS</div>', unsafe_allow_html=True)
    st.markdown('<div class="wordmark-sub">Enterprise Intelligence</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**CLIENT**")
    client = st.selectbox("", ["Maison Éclat", "Velour Studio", "Arroyo & Co.", "Custom Upload"], label_visibility="collapsed")
    st.markdown("**REPORTING PERIOD**")
    months = st.slider("", min_value=3, max_value=24, value=12, step=3, format="%d mo", label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**NAVIGATION**")
    st.page_link("app.py", label="✦  Overview")
    st.page_link("pages/1_engagement.py", label="◈  Engagement")
    st.page_link("pages/2_recommendations.py", label="◉  Recommendations")
    st.page_link("pages/3_trends.py", label="◍  Trend Intelligence")
    st.markdown("---")
    st.markdown("**FILTER TRENDS**")
    all_trends = ["Quiet Luxury", "Coastal Grandmother", "Y2K Revival", "Gorpcore", "Boho Chic"]
    selected = st.multiselect("", all_trends, default=all_trends, label_visibility="collapsed")

df = trend_data(months)
if selected:
    df = df[df["trend"].isin(selected)]

st.markdown('<div class="section-header">Trend Intelligence</div>', unsafe_allow_html=True)
st.markdown(f'<div class="section-sub">{client} · Last {months} months · Trend signal strength vs. inventory alignment</div>', unsafe_allow_html=True)

# ── Trend signal lines ─────────────────────────────────────────────────────────
fig = multi_line_chart(df, x="month", y="trend_signal", color_col="trend",
                        title="Trend Signal Strength (0–1)")
st.plotly_chart(fig, use_container_width=True)

# ── Inventory alignment lines ──────────────────────────────────────────────────
st.markdown('<div class="section-header">Inventory Alignment</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">How well your current inventory tracks emerging trend signals — gaps indicate potential opportunity or risk</div>', unsafe_allow_html=True)

fig2 = multi_line_chart(df, x="month", y="inventory_alignment", color_col="trend",
                         title="Inventory Alignment Score (0–1)")
st.plotly_chart(fig2, use_container_width=True)

# ── Gap analysis — latest month ────────────────────────────────────────────────
st.markdown('<div class="section-header">Gap Analysis · Latest Month</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Positive gap = trend signal outpacing inventory (opportunity). Negative = overstock risk.</div>', unsafe_allow_html=True)

latest = df[df["month"] == df["month"].max()].copy()
latest = latest.sort_values("gap", ascending=False)

for _, row in latest.iterrows():
    gap = row["gap"]
    color = POSITIVE if gap >= 0 else NEGATIVE
    label = "OPPORTUNITY" if gap >= 0 else "OVERSTOCK RISK"
    bar_width = min(abs(gap) / 0.5 * 100, 100)
    direction = "right" if gap >= 0 else "left"

    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:16px; margin-bottom:10px; padding:10px 16px; background:#141414; border:1px solid #1E1E1E; border-radius:3px;">
      <div style="width:180px; font-size:0.8rem; color:#F5F0E8;">{row['trend']}</div>
      <div style="flex:1; background:#1E1E1E; border-radius:2px; height:8px; position:relative;">
        <div style="position:absolute; {'left:50%' if gap>=0 else 'right:50%'}; width:{bar_width/2}%; height:100%; background:{color}; border-radius:2px;"></div>
        <div style="position:absolute; left:50%; top:-3px; width:1px; height:14px; background:#3A3A3A;"></div>
      </div>
      <div style="width:60px; text-align:right; font-family:'Cormorant Garamond',serif; font-size:1.1rem; color:{color};">{gap:+.2f}</div>
      <span class="gap-chip" style="background:{color}22; color:{color}; border:1px solid {color}44;">{label}</span>
    </div>
    """, unsafe_allow_html=True)
