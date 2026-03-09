"""
KCSE Tracker — 30 years of exam results with trend analysis.

DATA ACCURACY WARNING: The data/kcse_results.csv contains estimated/illustrative
historical data for demonstration. Replace with verified KNEC data before public
launch. Grade distribution columns (1995–2009) are particularly approximate.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os


@st.cache_data
def _load():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "kcse_results.csv")
    try:
        df = pd.read_csv(path)
        df["year"]       = pd.to_numeric(df["year"], errors="coerce")
        df["mean_grade"] = pd.to_numeric(df["mean_grade"], errors="coerce")
        df["candidates"] = pd.to_numeric(df["candidates"], errors="coerce")
        return df.dropna(subset=["year", "mean_grade"])
    except FileNotFoundError:
        return pd.DataFrame()


GRADE_LABELS = {
    12: "A", 11: "A−", 10: "B+", 9: "B", 8: "B−",
    7: "C+", 6: "C", 5: "C−", 4: "D+", 3: "D", 2: "D−", 1: "E"
}


def render():
    st.markdown("""
    <div class="section-header">
      <h2>📊 KCSE Tracker</h2>
      <p>Dagoretti academic performance · 1995–2025</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-gold">
      <strong>Data sources:</strong>
      <strong>Confirmed ✅</strong> — 2014, 2015 (official school Facebook page);
      2022, 2023, 2024, 2025 (Rejnac Daily / KNEC grade distribution, updated Jan 2026).
      <strong>Illustrative ⚠️</strong> — all other years are estimated trend data, not verified KNEC records.
      Mean scores and grade distributions for 1995–2013 and 2016–2021 should be replaced with
      official KNEC data before using this tool for any formal purpose.
    </div>
    """, unsafe_allow_html=True)

    df = _load()
    if df.empty:
        st.error("KCSE data not found. Please check data/kcse_results.csv.")
        return

    # ── Summary metrics ───────────────────────────────────────────────────────
    latest = df[df["year"] == df["year"].max()].iloc[0]
    earliest = df[df["year"] == df["year"].min()].iloc[0]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Latest mean grade (2024)", f"{latest['mean_grade']:.1f}/12",
              delta=f"+{latest['mean_grade'] - earliest['mean_grade']:.1f} since 1995")
    m2.metric("Candidates (2024)", int(latest["candidates"]),
              delta=f"+{int(latest['candidates'] - earliest['candidates'])} since 1995")
    m3.metric("Grade equivalent", _grade_str(latest["mean_grade"]))
    m4.metric("A grades (2024)", int(latest.get("a_plain", 0)))

    st.markdown("---")

    # ── Trend chart ───────────────────────────────────────────────────────────
    st.markdown("#### Mean Grade Trend · 1995–2024")

    # Polynomial trend line
    x = df["year"].values
    y = df["mean_grade"].values
    z = np.polyfit(x, y, 1)
    trend = np.poly1d(z)(x)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines+markers",
        name="Mean grade",
        line=dict(color="#1a5c2e", width=2.5),
        marker=dict(size=6, color="#1a5c2e"),
        fill="tozeroy",
        fillcolor="rgba(26,92,46,0.08)",
    ))
    fig.add_trace(go.Scatter(
        x=x, y=trend, mode="lines",
        name="Trend",
        line=dict(color="#c9a94e", width=2, dash="dash"),
    ))
    fig.update_layout(
        paper_bgcolor="#fdf8f0", plot_bgcolor="#fdf8f0",
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis=dict(range=[4, 10], title="Mean grade (1–12 scale)", gridcolor="#e8f5e9"),
        xaxis=dict(title="Year", gridcolor="#e8f5e9"),
        legend=dict(orientation="h", y=1.05),
        height=360,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Grade distribution ────────────────────────────────────────────────────
    st.markdown("#### Grade Distribution — Select Year")

    grade_cols = ["a_plain", "a_minus", "b_plus", "b_plain", "b_minus",
                  "c_plus", "c_plain", "c_minus", "d_plus", "d_plain", "d_minus", "e"]
    grade_names = ["A", "A−", "B+", "B", "B−", "C+", "C", "C−", "D+", "D", "D−", "E"]

    selected_year = st.selectbox(
        "Year",
        sorted(df["year"].unique(), reverse=True),
        index=0,
    )

    yr_row = df[df["year"] == selected_year].iloc[0]
    dist_vals = [pd.to_numeric(yr_row.get(c, 0), errors="coerce") or 0 for c in grade_cols]

    fig2 = px.bar(
        x=grade_names,
        y=dist_vals,
        labels={"x": "Grade", "y": "Number of students"},
        color=grade_names,
        color_discrete_sequence=[
            "#1a5c2e","#2e7d46","#43a059","#66bb6a","#a5d6a7",
            "#c9a94e","#f0c040","#f9a825","#e57373","#ef5350","#d32f2f","#b71c1c"
        ],
    )
    fig2.update_layout(
        paper_bgcolor="#fdf8f0", plot_bgcolor="#fdf8f0",
        margin=dict(l=0, r=0, t=10, b=0), height=300, showlegend=False,
        yaxis=dict(gridcolor="#e8f5e9"),
    )
    st.plotly_chart(fig2, use_container_width=True)

    total = yr_row["candidates"]
    a_count = yr_row.get("a_plain", 0)
    st.caption(
        f"{selected_year}: {int(total)} candidates · "
        f"Top student: {yr_row.get('top_student','—')} ({yr_row.get('top_grade','—')}) · "
        f"A grades: {int(a_count)} ({100*int(a_count)/int(total):.1f}%)"
    )

    st.markdown("---")

    # ── Candidates growth ─────────────────────────────────────────────────────
    st.markdown("#### Candidate Growth · School Size Over Time")
    fig3 = px.area(
        df, x="year", y="candidates",
        labels={"candidates": "Candidates", "year": "Year"},
        color_discrete_sequence=["#1a5c2e"],
    )
    fig3.update_layout(
        paper_bgcolor="#fdf8f0", plot_bgcolor="#fdf8f0",
        margin=dict(l=0, r=0, t=10, b=0), height=250,
        yaxis=dict(gridcolor="#e8f5e9"),
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ── Full table ────────────────────────────────────────────────────────────
    with st.expander("📋 Full results table (all years)"):
        show_df = df[["year", "mean_grade", "candidates", "top_student", "top_grade"]].sort_values("year", ascending=False)
        show_df.columns = ["Year", "Mean Grade", "Candidates", "Top Student", "Top Grade"]
        st.dataframe(show_df, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="footer">
      Source: Estimated data (1995–2009). Verified KNEC data (2010–2024 indicative).
      Replace with official records before public launch.
    </div>
    """, unsafe_allow_html=True)


def _grade_str(mean: float) -> str:
    """Convert numeric mean grade to letter grade string."""
    rounded = round(mean)
    return GRADE_LABELS.get(rounded, "C")
