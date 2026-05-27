"""
StyLens Enterprise — Page 1: Engagement Analytics
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.graph_objects as go
from data.synthetic import engagement_data
from utils.charts import apply_theme, line_chart, GOLD, ACCENT_BLUE, MUTED, CREAM

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Jost:wght@300;400;500&display=swap');
  html, body, [class*="css"] { background-color: #0D0D0D; color: #F5F0E8; font-family: 'Jost', sans-serif; }
  [data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #1E1E1E; }
  .section-header { font-family: 'Cormorant Garamond', serif; font-size: 1.4rem; font-weight: 300; letter-spacing: 0.05em; color: #F5F0E8; margin: 32px 0 4px 0; border-bottom: 1px solid #1E1E1E; padding-bottom: 8px; }
  .section-sub { font-size: 0.75rem; color: #8A8A8A; letter-spacing: 0.08em; margin-bottom: 20px; }
  .wordmark { font-family: 'Cormorant Garamond', serif; font-size: 1.6rem; font-weight: 300; letter-spacing: 0.2em; color: #C9A84C; }
  .wordmark-sub { font-size: 0.6rem; letter-spacing: 0.25em; text-transform: uppercase; color: #8A8A8A; margin-top: -4px; }
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

df = engagement_data(months)

st.markdown('<div class="section-header">User Engagement</div>', unsafe_allow_html=True)
st.markdown(f'<div class="section-sub">{client} · Last {months} months · Session depth, return behavior, and time-on-platform</div>', unsafe_allow_html=True)

# ── Sessions + Return Rate ─────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["month"], y=df["sessions"],
        fill="tozeroy", mode="lines",
        line=dict(color=GOLD, width=2.5),
        fillcolor="rgba(201,168,76,0.10)",
        hovertemplate="%{x|%b %Y}<br><b>%{y:,} sessions</b><extra></extra>",
        name="Sessions"
    ))
    apply_theme(fig, "Monthly Sessions")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df["month"], y=(df["return_rate"] * 100).round(1),
        mode="lines+markers",
        line=dict(color=ACCENT_BLUE, width=2.5),
        marker=dict(size=5, color=ACCENT_BLUE),
        hovertemplate="%{x|%b %Y}<br><b>%{y:.1f}% return rate</b><extra></extra>",
        name="Return Rate %"
    ))
    apply_theme(fig2, "Return Rate (%)")
    st.plotly_chart(fig2, use_container_width=True)

# ── Session Depth + Duration ───────────────────────────────────────────────────
st.markdown('<div class="section-header">Session Quality</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Average pages per session and time-on-platform in minutes</div>', unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=df["month"], y=df["avg_depth"],
        marker_color=GOLD,
        marker_line_width=0,
        hovertemplate="%{x|%b %Y}<br><b>%{y:.1f} pages/session</b><extra></extra>",
    ))
    apply_theme(fig3, "Avg. Session Depth (pages)")
    fig3.update_layout(bargap=0.35)
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=df["month"], y=df["session_duration_min"],
        mode="lines+markers",
        line=dict(color="#A67CB5", width=2.5, dash="dot"),
        marker=dict(size=5, color="#A67CB5"),
        hovertemplate="%{x|%b %Y}<br><b>%{y:.1f} min avg session</b><extra></extra>",
    ))
    apply_theme(fig4, "Avg. Session Duration (min)")
    st.plotly_chart(fig4, use_container_width=True)

# ── Summary table ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Monthly Breakdown</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Full engagement data table</div>', unsafe_allow_html=True)

display_df = df.copy()
display_df["month"] = display_df["month"].dt.strftime("%B %Y")
display_df["return_rate"] = (display_df["return_rate"] * 100).round(1).astype(str) + "%"
display_df.columns = ["Month", "Sessions", "Avg Depth", "Return Rate", "Duration (min)"]
display_df["Sessions"] = display_df["Sessions"].apply(lambda x: f"{x:,}")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
)
