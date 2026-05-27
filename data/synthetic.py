"""
Synthetic data generator for StyLens Enterprise Analytics Dashboard.
Produces realistic fashion retail KPIs for demo purposes.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def seed(n=42):
    np.random.seed(n)


def date_range(months=12):
    end = datetime.today().replace(day=1)
    return pd.date_range(end=end, periods=months, freq="MS")


def engagement_data(months=12):
    seed()
    dates = date_range(months)
    base_sessions = 18_000
    trend = np.linspace(1.0, 1.45, months)
    seasonal = 1 + 0.12 * np.sin(np.linspace(0, 2 * np.pi, months) + 1)
    noise = np.random.normal(1, 0.04, months)

    sessions = (base_sessions * trend * seasonal * noise).astype(int)
    avg_depth = np.clip(np.random.normal(4.2, 0.4, months), 2.5, 7.0).round(1)
    return_rate = np.clip(np.random.normal(0.61, 0.04, months), 0.48, 0.78).round(3)
    session_duration = np.clip(np.random.normal(7.4, 0.8, months), 4.0, 12.0).round(1)

    return pd.DataFrame({
        "month": dates,
        "sessions": sessions,
        "avg_depth": avg_depth,
        "return_rate": return_rate,
        "session_duration_min": session_duration,
    })


def recommendation_data(months=12):
    seed()
    dates = date_range(months)
    ctr = np.clip(np.random.normal(0.34, 0.03, months), 0.24, 0.46).round(3)
    conversion = np.clip(np.random.normal(0.082, 0.01, months), 0.055, 0.115).round(4)
    style_match = np.clip(np.random.normal(0.78, 0.03, months), 0.68, 0.91).round(3)
    revenue_influenced = np.clip(
        np.random.normal(210_000, 18_000, months) * np.linspace(1.0, 1.3, months),
        140_000, 340_000
    ).astype(int)

    return pd.DataFrame({
        "month": dates,
        "ctr": ctr,
        "conversion_rate": conversion,
        "style_match_score": style_match,
        "revenue_influenced": revenue_influenced,
    })


def trend_data(months=12):
    seed()
    dates = date_range(months)
    trends = ["Quiet Luxury", "Coastal Grandmother", "Y2K Revival", "Gorpcore", "Boho Chic"]
    rows = []
    for t in trends:
        base = np.random.uniform(0.4, 0.85)
        signal = np.clip(
            base + np.cumsum(np.random.normal(0.01, 0.04, months)),
            0.1, 1.0
        )
        inventory = np.clip(signal + np.random.normal(-0.08, 0.06, months), 0.05, 1.0)
        for i, d in enumerate(dates):
            rows.append({
                "month": d,
                "trend": t,
                "trend_signal": round(signal[i], 3),
                "inventory_alignment": round(inventory[i], 3),
                "gap": round(signal[i] - inventory[i], 3),
            })
    return pd.DataFrame(rows)


def overview_kpis(eng_df, rec_df):
    latest_eng = eng_df.iloc[-1]
    prev_eng = eng_df.iloc[-2]
    latest_rec = rec_df.iloc[-1]
    prev_rec = rec_df.iloc[-2]

    def delta(new, old):
        return round((new - old) / old * 100, 1)

    return {
        "total_sessions": int(latest_eng["sessions"]),
        "sessions_delta": delta(latest_eng["sessions"], prev_eng["sessions"]),
        "return_rate": float(latest_eng["return_rate"]),
        "return_rate_delta": delta(latest_eng["return_rate"], prev_eng["return_rate"]),
        "ctr": float(latest_rec["ctr"]),
        "ctr_delta": delta(latest_rec["ctr"], prev_rec["ctr"]),
        "revenue_influenced": int(latest_rec["revenue_influenced"]),
        "revenue_delta": delta(latest_rec["revenue_influenced"], prev_rec["revenue_influenced"]),
        "style_match_score": float(latest_rec["style_match_score"]),
    }

def influencer_data():
    seed()
    influencers = [
        {"id": "A", "tier": "Macro"},
        {"id": "B", "tier": "Mid"},
        {"id": "C", "tier": "Mid"},
        {"id": "D", "tier": "Micro"},
    ]
    rows = []
    for inf in influencers:
        rows.append({
            "name": f"{inf['tier']} · Influencer {inf['id']}",
            "tier": inf["tier"],
            "reach": int(np.random.uniform(10_000, 500_000)),
            "engagement_rate": round(np.random.uniform(0.02, 0.12), 3),
            "post_conversion": round(np.random.uniform(0.01, 0.08), 3),
            "revenue_driven": int(np.random.uniform(5_000, 120_000)),
            "style_match": round(np.random.uniform(0.60, 0.95), 2),
        })
    return pd.DataFrame(rows)
