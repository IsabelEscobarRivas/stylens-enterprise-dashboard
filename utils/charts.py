"""
Shared Plotly chart theme and formatting utilities for StyLens Enterprise Dashboard.
"""

import plotly.graph_objects as go
import plotly.express as px

# ── Brand palette ──────────────────────────────────────────────────────────────
OBSIDIAN = "#0D0D0D"
CREAM = "#F5F0E8"
GOLD = "#C9A84C"
GOLD_LIGHT = "#E8D5A3"
MUTED = "#8A8A8A"
POSITIVE = "#4CAF7D"
NEGATIVE = "#E05C5C"
ACCENT_BLUE = "#5B8DB8"

TREND_COLORS = [GOLD, "#B87E4B", "#8FAF7A", ACCENT_BLUE, "#A67CB5"]

LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Georgia, serif", color=CREAM, size=13),
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(color=MUTED, size=11),
        linecolor="#2A2A2A",
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#1E1E1E",
        zeroline=False,
        tickfont=dict(color=MUTED, size=11),
        linecolor="#2A2A2A",
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color=CREAM, size=12),
    ),
    hoverlabel=dict(
        bgcolor="#1A1A1A",
        font_color=CREAM,
        bordercolor=GOLD,
        font_family="Georgia, serif",
    ),
)


def apply_theme(fig, title=""):
    layout = dict(LAYOUT_BASE)
    if title:
        layout["title"] = dict(
            text=title,
            font=dict(color=CREAM, size=15, family="Georgia, serif"),
            x=0.02,
        )
    fig.update_layout(**layout)
    return fig


def line_chart(df, x, y, title="", color=GOLD, label=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x], y=df[y],
        mode="lines+markers",
        line=dict(color=color, width=2.5),
        marker=dict(size=5, color=color),
        name=label or y,
        hovertemplate="%{x|%b %Y}<br><b>%{y}</b><extra></extra>",
    ))
    apply_theme(fig, title)
    return fig


def area_chart(df, x, y, title="", color=GOLD):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x], y=df[y],
        fill="tozeroy",
        mode="lines",
        line=dict(color=color, width=2),
        fillcolor=color.replace("#", "rgba(") + ",0.12)" if color.startswith("#") else color,
        hovertemplate="%{x|%b %Y}<br><b>%{y}</b><extra></extra>",
    ))
    apply_theme(fig, title)
    return fig


def multi_line_chart(df, x, y, color_col, title=""):
    categories = df[color_col].unique()
    fig = go.Figure()
    for i, cat in enumerate(categories):
        sub = df[df[color_col] == cat]
        fig.add_trace(go.Scatter(
            x=sub[x], y=sub[y],
            mode="lines+markers",
            name=cat,
            line=dict(color=TREND_COLORS[i % len(TREND_COLORS)], width=2),
            marker=dict(size=4),
            hovertemplate=f"<b>{cat}</b><br>%{{x|%b %Y}}<br>%{{y:.2f}}<extra></extra>",
        ))
    apply_theme(fig, title)
    return fig


def bar_chart(df, x, y, title="", color=GOLD):
    fig = go.Figure(go.Bar(
        x=df[x], y=df[y],
        marker_color=color,
        marker_line_width=0,
        hovertemplate="%{x|%b %Y}<br><b>$%{y:,.0f}</b><extra></extra>",
    ))
    apply_theme(fig, title)
    fig.update_layout(bargap=0.35)
    return fig


def format_pct(val):
    return f"{val * 100:.1f}%"


def format_delta(val):
    sign = "▲" if val >= 0 else "▼"
    color = POSITIVE if val >= 0 else NEGATIVE
    return sign, f"{abs(val):.1f}%", color
