"""
Alumni Atlas — world map + filterable directory.
Pattern: data → filter → render. Runs on every interaction.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os


@st.cache_data
def _load():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "alumni.csv")
    try:
        df = pd.read_csv(path)
        df["year"] = pd.to_numeric(df["year"], errors="coerce").fillna(0).astype(int)
        df["lat"]  = pd.to_numeric(df["lat"], errors="coerce")
        df["lon"]  = pd.to_numeric(df["lon"], errors="coerce")
        return df.dropna(subset=["lat", "lon"])
    except FileNotFoundError:
        return pd.DataFrame()


def render():
    st.markdown("""
    <div class="section-header">
      <h2>🌍 Alumni Atlas</h2>
      <p>Where are Dagoretti graduates today? Every pin is a story.</p>
    </div>
    """, unsafe_allow_html=True)

    df = _load()
    if df.empty:
        st.error("Alumni data not found. Please check data/alumni.csv.")
        return

    # ── Filters ──────────────────────────────────────────────────────────────
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        industries = ["All Industries"] + sorted(df["industry"].dropna().unique().tolist())
        ind_filter = st.selectbox("Industry", industries)
    with fc2:
        countries = ["All Countries"] + sorted(df["country"].dropna().unique().tolist())
        cty_filter = st.selectbox("Country", countries)
    with fc3:
        year_min, year_max = int(df["year"].min()), int(df["year"].max())
        year_range = st.slider("Graduation year", year_min, year_max, (year_min, year_max))

    mentoring_only = st.checkbox("Show mentors only", value=False)

    # ── Apply filters ─────────────────────────────────────────────────────────
    fdf = df.copy()
    if ind_filter != "All Industries":
        fdf = fdf[fdf["industry"] == ind_filter]
    if cty_filter != "All Countries":
        fdf = fdf[fdf["country"] == cty_filter]
    fdf = fdf[(fdf["year"] >= year_range[0]) & (fdf["year"] <= year_range[1])]
    if mentoring_only:
        fdf = fdf[fdf["mentoring"] == "Yes"]

    st.caption(f"Showing {len(fdf)} of {len(df)} alumni")

    # ── Map ───────────────────────────────────────────────────────────────────
    if not fdf.empty:
        fig = px.scatter_geo(
            fdf,
            lat="lat",
            lon="lon",
            color="industry",
            hover_name="name",
            hover_data={"role": True, "city": True, "country": True, "year": True, "lat": False, "lon": False},
            projection="natural earth",
            title="",
            color_discrete_sequence=px.colors.qualitative.Safe,
            height=480,
        )
        fig.update_traces(marker=dict(size=9, opacity=0.85, line=dict(width=0.5, color="white")))
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="#fdf8f0",
            geo=dict(
                showframe=False,
                showcoastlines=True,
                coastlinecolor="#c8e6c9",
                showland=True,
                landcolor="#e8f5e9",
                showocean=True,
                oceancolor="#e3f2fd",
                showlakes=True,
                lakecolor="#e3f2fd",
                showcountries=True,
                countrycolor="#a5d6a7",
                bgcolor="#fdf8f0",
            ),
            legend=dict(orientation="h", y=-0.05, x=0, font=dict(size=11)),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No alumni match the current filters.")

    # ── Summary stats ─────────────────────────────────────────────────────────
    if not fdf.empty:
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Alumni shown", len(fdf))
        s2.metric("Countries", fdf["country"].nunique())
        s3.metric("Industries", fdf["industry"].nunique())
        s4.metric("Mentors available", (fdf["mentoring"] == "Yes").sum())

    st.markdown("---")

    # ── Directory ─────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>Directory</h2>
      <p>Filtered alumni list</p>
    </div>
    """, unsafe_allow_html=True)

    if not fdf.empty:
        for _, row in fdf.iterrows():
            mentor_badge  = '<span class="badge-gold">🤝 Mentoring</span>' if row.get("mentoring") == "Yes" else ""
            linkedin_link = (
                f'<a href="{row["linkedin"]}" target="_blank" style="color:var(--green-mid);">LinkedIn →</a>'
                if pd.notna(row.get("linkedin")) and str(row.get("linkedin", "")).startswith("http") else ""
            )
            bio = f'<p style="margin:0.3rem 0 0; font-size:0.85rem; color:var(--text-muted);">{row["bio_short"]}</p>' \
                  if pd.notna(row.get("bio_short")) and row["bio_short"] else ""
            st.markdown(f"""
            <div class="alumni-card">
              <h4>{row['name']}
                <span style='font-weight:400; color:var(--text-muted); font-size:0.85rem;'>
                  · Class of {int(row['year'])}
                </span>
              </h4>
              <p>{row['role']} · {row['city']}, {row['country']}</p>
              <div style='margin-top:0.35rem;'>
                <span class="badge">{row['industry']}</span>
                {mentor_badge}
                {linkedin_link}
              </div>
              {bio}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No alumni match the current filters.")

    st.markdown("""
    <div class="footer">
      Alumni data is community-maintained. Add yourself via the Submit Data page.
    </div>
    """, unsafe_allow_html=True)
