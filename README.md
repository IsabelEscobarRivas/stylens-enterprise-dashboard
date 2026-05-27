# StyLens Enterprise Analytics Dashboard

A multi-page Streamlit analytics dashboard simulating an enterprise client portal for **StyLens** — an AI-powered fashion intelligence platform.

Built as a portfolio project demonstrating:
- Multi-page Streamlit app architecture
- Synthetic KPI data generation with realistic trend modeling
- Custom dark-theme Plotly visualizations with a shared design system
- Fashion retail domain expertise (engagement, recommendation performance, trend intelligence)

---

## Pages

| Page | Description |
|------|-------------|
| **✦ Overview** | Brand health KPIs at a glance — sessions, return rate, CTR, revenue influenced, style match score |
| **◈ Engagement** | Session volume, return rate, session depth, and time-on-platform trends |
| **◉ Recommendations** | CTR, conversion rate, style match score, and revenue attribution |
| **◍ Trend Intelligence** | Trend signal strength vs. inventory alignment with gap analysis |

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/IsabelEscobarRivas/stylens-enterprise-dashboard.git
cd stylens-enterprise-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Tech Stack

- **[Streamlit](https://streamlit.io/)** — multi-page app framework
- **[Plotly](https://plotly.com/python/)** — interactive charts with custom theming
- **[Pandas](https://pandas.pydata.org/)** / **[NumPy](https://numpy.org/)** — data generation and manipulation

---

## Project Structure

```
stylens-enterprise-dashboard/
├── app.py                  # Main entry point — Overview page
├── pages/
│   ├── 1_engagement.py     # User engagement analytics
│   ├── 2_recommendations.py# Recommendation performance
│   └── 3_trends.py         # Trend intelligence & gap analysis
├── data/
│   └── synthetic.py        # KPI data generator
├── utils/
│   └── charts.py           # Shared Plotly theme & chart helpers
├── requirements.txt
└── README.md
```

---

## About StyLens

StyLens is a four-agent AI fashion intelligence platform that helps retail brands understand style adoption, recommendation effectiveness, and trend-inventory alignment. This dashboard demonstrates the kind of enterprise analytics tooling StyLens provides to brand partners.

Learn more: [stylens.ai](https://stylens.ai) *(coming soon)*

---

*Built by [Isabel Escobar Rivas](https://linkedin.com/in/isabelescobarr) · [@IsabelEscobarRivas](https://github.com/IsabelEscobarRivas)*
