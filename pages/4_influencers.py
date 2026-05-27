"""
StyLens Enterprise — Page 4: Influencer Performance
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.graph_objects as go
from data.synthetic import influencer_data
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
    st.markdown("---")
    st.markdown("**NAVIGATION**")
    st.page_link("app.py", label="✦  Overview")
    st.page_link("pages/1_engagement.py", label="◈  Engagement")
    st.page_link("pages/2_recommendations.py", label="◉  Recommendations")
    st.page_link("pages/3_trends.py", label="◍  Trend Intelligence")
    st.page_link("pages/4_influencers.py", label="◆  Influencers")

df = influencer_data()

st.markdown('<div class="section-header">Influencer Performance</div>', unsafe_allow_html=True)
st.markdown(f'<div class="section-sub">{client} · Full scorecard — reach, engagement, conversions, revenue, and style alignment</div>', unsafe_allow_html=True)

# ── Bar chart — Revenue driven ─────────────────────────────────────────────────
fig = go.Figure(go.Bar(
    x=df["name"], y=df["revenue_driven"],
    marker_color=GOLD,
    marker_line_width=0,
    hovertemplate="<b>%{x}</b><br>$%{y:,.0f} revenue driven<extra></extra>",
))
apply_theme(fig, "Revenue Driven by Influencer ($)")
fig.update_layout(bargap=0.4)
st.plotly_chart(fig, use_container_width=True)

# ── Engagement + Conversion side by side ──────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    fig2 = go.Figure(go.Bar(
        x=df["name"], y=(df["engagement_rate"] * 100).round(1),
        marker_color=ACCENT_BLUE,
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>%{y:.1f}% engagement<extra></extra>",
    ))
    apply_theme(fig2, "Engagement Rate (%)")
    fig2.update_layout(bargap=0.4)
    st.plotly_chart(fig2, use_container_width=True)

with c2:
    fig3 = go.Figure(go.Bar(
        x=df["name"], y=(df["post_conversion"] * 100).round(1),
        marker_color=POSITIVE,
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>%{y:.1f}% post conversion<extra></extra>",
    ))
    apply_theme(fig3, "Post Conversion Rate (%)")
    fig3.update_layout(bargap=0.4)
    st.plotly_chart(fig3, use_container_width=True)

# ── Style match ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Style Alignment</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">How closely each influencer\'s aesthetic aligns with the brand\'s StyLens profile</div>', unsafe_allow_html=True)

for _, row in df.iterrows():
    bar_pct = int(row["style_match"] * 100)
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:16px; margin-bottom:10px; padding:12px 18px; background:#141414; border:1px solid #1E1E1E; border-radius:3px;">
      <div style="width:220px; font-size:0.82rem; color:#F5F0E8;">{row['name']}</div>
      <div style="flex:1; background:#1E1E1E; border-radius:2px; height:6px;">
        <div style="width:{bar_pct}%; height:100%; background:linear-gradient(90deg,#C9A84C,#E8D5A3); border-radius:2px;"></div>
      </div>
      <div style="width:48px; text-align:right; font-family:'Cormorant Garamond',serif; font-size:1.2rem; color:#C9A84C;">{bar_pct}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Full scorecard table ───────────────────────────────────────────────────────
st.markdown('<div class="section-header">Full Scorecard</div>', unsafe_allow_html=True)

display = df.copy()
display["reach"] = display["reach"].apply(lambda x: f"{x:,}")
display["engagement_rate"] = (display["engagement_rate"] * 100).round(1).astype(str) + "%"
display["post_conversion"] = (display["post_conversion"] * 100).round(1).astype(str) + "%"
display["revenue_driven"] = display["revenue_driven"].apply(lambda x: f"${x:,}")
display["style_match"] = (display["style_match"] * 100).round(0).astype(int).astype(str)
display.columns = ["Influencer", "Tier", "Reach", "Engagement Rate", "Post Conversion", "Revenue Driven", "Style Match"]

st.dataframe(display, use_container_width=True, hide_index=True)