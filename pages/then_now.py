"""
Kenya: Then & Now — 25 indicators comparing 2000 and 2025.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os


@st.cache_data
def _load():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "kenya_then_now.csv")
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        return pd.DataFrame()


CATEGORY_ICONS = {
    "Economy":        "💰",
    "Technology":     "📱",
    "Education":      "📚",
    "Health":         "🏥",
    "Infrastructure": "🏗️",
    "Demographics":   "👥",
    "Governance":     "🏛️",
}


def render():
    st.markdown("""
    <div class="hero-banner">
      <h1>🇰🇪 Kenya: Then &amp; Now</h1>
      <p>25 indicators. 25 years. The transformation is striking.</p>
      <p style='color:#81c784; margin-top:0.4rem; font-size:0.9rem;'>
        Class of 2000 graduated into a different Kenya. Class of 2025 graduates into a different world.
      </p>
    </div>
    """, unsafe_allow_html=True)

    df = _load()
    if df.empty:
        st.error("Data not found. Please check data/kenya_then_now.csv.")
        return

    categories = sorted(df["category"].unique().tolist())

    # ── Category filter ────────────────────────────────────────────────────────
    selected_cat = st.selectbox(
        "Filter by category",
        ["All Categories"] + categories,
    )

    fdf = df if selected_cat == "All Categories" else df[df["category"] == selected_cat]

    # ── Summary cards ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>At a Glance</h2>
      <p>How Kenya has changed since the Class of 2000 graduated</p>
    </div>
    """, unsafe_allow_html=True)

    highlight_rows = df[df["indicator"].isin([
        "Population", "GDP per capita", "Mobile money accounts",
        "Mobile phone subscribers", "Electricity access - households",
        "Secondary school net enrolment",
    ])]

    cols = st.columns(3)
    for i, (_, row) in enumerate(highlight_rows.iterrows()):
        with cols[i % 3]:
            icon = CATEGORY_ICONS.get(row["category"], "📊")
            st.markdown(f"""
            <div class="stat-pill" style='margin-bottom:0.75rem;'>
              <span class="stat-n">{row['value_2025']}</span>
              <span class="stat-lbl">{icon} {row['indicator']}</span>
              <span style='font-size:0.72rem; color:#a5d6a7; display:block; margin-top:0.2rem;'>
                Was: {row['value_2000']} {row['unit']}
              </span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Numeric comparison chart ───────────────────────────────────────────────
    numeric_rows = []
    for _, row in fdf.iterrows():
        try:
            v2000 = float(str(row["value_2000"]).replace(",", ""))
            v2025 = float(str(row["value_2025"]).replace(",", ""))
            numeric_rows.append({
                "indicator": row["indicator"],
                "2000": v2000,
                "2025": v2025,
                "unit": row["unit"],
                "category": row["category"],
                "change_pct": round(100 * (v2025 - v2000) / v2000, 1) if v2000 > 0 else 0,
            })
        except (ValueError, TypeError):
            pass

    if numeric_rows:
        chart_df = pd.DataFrame(numeric_rows)

        st.markdown("""
        <div class="section-header">
          <h2>Numeric Indicators</h2>
          <p>Percentage change from 2000 to 2025</p>
        </div>
        """, unsafe_allow_html=True)

        chart_df_sorted = chart_df.sort_values("change_pct", ascending=True)
        fig = px.bar(
            chart_df_sorted,
            x="change_pct",
            y="indicator",
            orientation="h",
            color="change_pct",
            color_continuous_scale=["#ef5350", "#ffeb3b", "#66bb6a", "#1a5c2e"],
            labels={"change_pct": "% change (2000→2025)", "indicator": ""},
            height=max(400, len(chart_df_sorted) * 30),
        )
        fig.update_layout(
            paper_bgcolor="#fdf8f0", plot_bgcolor="#fdf8f0",
            margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_showscale=False,
            yaxis=dict(tickfont=dict(size=11)),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Full comparison table ──────────────────────────────────────────────────
    for cat in (categories if selected_cat == "All Categories" else [selected_cat]):
        cat_df = df[df["category"] == cat]
        if cat_df.empty:
            continue

        icon = CATEGORY_ICONS.get(cat, "📊")
        st.markdown(f"""
        <div class="section-header">
          <h2>{icon} {cat}</h2>
        </div>
        """, unsafe_allow_html=True)

        for _, row in cat_df.iterrows():
            try:
                v2000 = float(str(row["value_2000"]).replace(",", ""))
                v2025 = float(str(row["value_2025"]).replace(",", ""))
                direction = "📈" if v2025 > v2000 else "📉"
                change = f"{direction} {abs(round(100*(v2025-v2000)/v2000, 0)):.0f}% change" if v2000 > 0 else ""
            except (ValueError, TypeError):
                change = "🔄 Changed"

            st.markdown(f"""
            <div class="card">
              <div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;'>
                <strong style='color:var(--green-dark);'>{row['indicator']}</strong>
                <span class="badge-blue">{change}</span>
              </div>
              <div style='display:flex; gap:2rem; margin-top:0.5rem; flex-wrap:wrap;'>
                <span><strong style='color:var(--text-muted);'>2000:</strong> {row['value_2000']} <em style='font-size:0.8rem; color:var(--text-muted);'>{row['unit']}</em></span>
                <span><strong style='color:var(--green-dark);'>2025:</strong> {row['value_2025']} <em style='font-size:0.8rem; color:var(--text-muted);'>{row['unit']}</em></span>
              </div>
              <p style='margin:0.3rem 0 0; font-size:0.8rem; color:var(--text-muted);'>Source: {row['source']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
      Data sources: World Bank, KNBS, WHO, Communications Authority of Kenya, various.
      2025 figures are latest available estimates.
    </div>
    """, unsafe_allow_html=True)
