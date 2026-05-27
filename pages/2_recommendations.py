"""
StyLens Enterprise — Page 2: Recommendation Performance
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.graph_objects as go
from data.synthetic import recommendation_data
from utils.charts import apply_theme, GOLD, ACCENT_BLUE, POSITIVE, MUTED

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Jost:wght@300;400;500&display=swap');
  html, body, [class*="css"] { background-color: #0D0D0D; color: #F5F0E8; font-family: 'Jost', sans-serif; }
  [data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #1E1E1E; }
  .section-header { font-family: 'Cormorant Garamond', serif; font-size: 1.4rem; font-weight: 300; color: #F5F0E8; margin: 32px 0 4px 0; border-bottom: 1px solid #1E1E1E; padding-bottom: 8px; }
  .section-sub { font-size: 0.75rem; color: #8A8A8A; letter-spacing: 0.08em; margin-bottom: 20px; }
  .wordmark { font-family: 'Cormorant Garamond', serif; font-size: 1.6rem; font-weight: 300; letter-spacing: 0.2em; color: #C9A84C; }
  .wordmark-sub { font-size: 0.6rem; letter-spacing: 0.25em; text-transform: uppercase; color: #8A8A8A; }
  .stat-pill { display:inline-block; background:#1A1A1A; border:1px solid #2A2A2A; border-radius:3px; padding:10px 20px; margin:4px; text-align:center; }
  .stat-pill-val { font-family:'Cormorant Garamond',serif; font-size:1.8rem; font-weight:300; color:#F5F0E8; }
  .stat-pill-label { font-size:0.65rem; letter-spacing:0.12em; text-transform:uppercase; color:#8A8A8A; }
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

df = recommendation_data(months)

st.markdown('<div class="section-header">Recommendation Performance</div>', unsafe_allow_html=True)
st.markdown(f'<div class="section-sub">{client} · Last {months} months · CTR, conversion, style match, and revenue attribution</div>', unsafe_allow_html=True)

# ── Period averages as pills ───────────────────────────────────────────────────
avg_ctr = df["ctr"].mean()
avg_conv = df["conversion_rate"].mean()
avg_match = df["style_match_score"].mean()
total_rev = df["revenue_influenced"].sum()

st.markdown(f"""
<div style="display:flex; gap:12px; flex-wrap:wrap; margin-bottom:24px;">
  <div class="stat-pill">
    <div class="stat-pill-val">{avg_ctr*100:.1f}%</div>
    <div class="stat-pill-label">Avg Click-Through Rate</div>
  </div>
  <div class="stat-pill">
    <div class="stat-pill-val">{avg_conv*100:.1f}%</div>
    <div class="stat-pill-label">Avg Conversion Rate</div>
  </div>
  <div class="stat-pill">
    <div class="stat-pill-val">{avg_match*100:.0f}</div>
    <div class="stat-pill-label">Avg Style Match Score</div>
  </div>
  <div class="stat-pill">
    <div class="stat-pill-val">${total_rev/1_000_000:.2f}M</div>
    <div class="stat-pill-label">Total Revenue Influenced</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── CTR + Conversion ───────────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["month"], y=(df["ctr"] * 100).round(2),
        mode="lines+markers",
        line=dict(color=GOLD, width=2.5),
        marker=dict(size=5, color=GOLD),
        hovertemplate="%{x|%b %Y}<br><b>%{y:.1f}% CTR</b><extra></extra>",
    ))
    apply_theme(fig, "Click-Through Rate (%)")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df["month"], y=(df["conversion_rate"] * 100).round(2),
        mode="lines+markers",
        line=dict(color=POSITIVE, width=2.5),
        marker=dict(size=5, color=POSITIVE),
        hovertemplate="%{x|%b %Y}<br><b>%{y:.1f}% conversion</b><extra></extra>",
    ))
    apply_theme(fig2, "Conversion Rate (%)")
    st.plotly_chart(fig2, use_container_width=True)

# ── Style match + Revenue ──────────────────────────────────────────────────────
st.markdown('<div class="section-header">Style Intelligence & Revenue Attribution</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Style match index trend and StyLens-attributed revenue by month</div>', unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=df["month"], y=(df["style_match_score"] * 100).round(1),
        fill="tozeroy",
        mode="lines",
        line=dict(color=ACCENT_BLUE, width=2),
        fillcolor="rgba(91,141,184,0.12)",
        hovertemplate="%{x|%b %Y}<br><b>%{y:.1f} style match</b><extra></extra>",
    ))
    apply_theme(fig3, "Style Match Score (0–100)")
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    fig4 = go.Figure(go.Bar(
        x=df["month"], y=df["revenue_influenced"],
        marker_color=GOLD,
        marker_line_width=0,
        hovertemplate="%{x|%b %Y}<br><b>$%{y:,.0f} influenced</b><extra></extra>",
    ))
    apply_theme(fig4, "Revenue Influenced by StyLens ($)")
    fig4.update_layout(bargap=0.3)
    st.plotly_chart(fig4, use_container_width=True)
