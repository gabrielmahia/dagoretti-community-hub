"""
Alumni Atlas — world map + filterable directory.
Pattern: data → filter → render. Runs on every interaction.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
import urllib.request
import urllib.parse
import json


@st.cache_data(ttl=3600)
def _geocode(city: str, country: str):
    """Geocode city+country using OSM Nominatim. Returns (lat, lon) or (None, None)."""
    query = f"{city}, {country}".strip(", ")
    if not query:
        return None, None
    try:
        url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
            "q": query, "format": "json", "limit": 1,
        })
        req = urllib.request.Request(url, headers={"User-Agent": "DagorettiCommunityHub/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            results = json.loads(resp.read())
        if results:
            return float(results[0]["lat"]), float(results[0]["lon"])
    except Exception:
        pass
    return None, None


@st.cache_data(ttl=300)
def _load():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "alumni.csv")
    try:
        df = pd.read_csv(path)
        df["year"] = pd.to_numeric(df["year"], errors="coerce").fillna(0).astype(int)
        df["lat"]  = pd.to_numeric(df["lat"], errors="coerce")
        df["lon"]  = pd.to_numeric(df["lon"], errors="coerce")

        # Auto-geocode any rows missing lat/lon
        needs_geocode = df["lat"].isna() | df["lon"].isna()
        if needs_geocode.any():
            for idx in df[needs_geocode].index:
                city    = str(df.at[idx, "city"]    or "").strip()
                country = str(df.at[idx, "country"] or "").strip()
                lat, lon = _geocode(city, country)
                if lat is not None:
                    df.at[idx, "lat"] = lat
                    df.at[idx, "lon"] = lon
                time.sleep(0.5)  # Nominatim rate limit: 1 req/sec

            # Persist geocoded values back to CSV so next load is instant
            try:
                df.to_csv(path, index=False)
            except Exception:
                pass

        return df.dropna(subset=["lat", "lon"])
    except FileNotFoundError:
        return pd.DataFrame()


COMMUNITY_SIZE = 78  # known WhatsApp group size — update as community grows

# School gate coordinates (Dagoretti High School, Kikuyu Road, Nairobi)
SCHOOL_LAT = -1.2497
SCHOOL_LON  = 36.6889


def _render_school_pin_only():
    """Render a map with just the school gate pin — shown when alumni list is empty."""
    import pandas as _pd
    school_df = _pd.DataFrame([{
        "name": "🦁 Dagoretti High School",
        "lat": SCHOOL_LAT, "lon": SCHOOL_LON,
        "role": "Where it all started — Class of '01",
        "industry": "Origin",
    }])
    fig = px.scatter_geo(
        school_df, lat="lat", lon="lon",
        hover_name="name",
        hover_data={"role": True, "lat": False, "lon": False, "industry": False},
        projection="natural earth", height=420,
    )
    fig.update_traces(marker=dict(size=14, color="#c9a94e", symbol="star",
                                  line=dict(width=1, color="#1a5c2e")))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#fdf8f0",
        geo=dict(showframe=False, showcoastlines=True, coastlinecolor="#c8e6c9",
                 showland=True, landcolor="#e8f5e9", showocean=True, oceancolor="#e3f2fd",
                 showlakes=True, lakecolor="#e3f2fd", showcountries=True,
                 countrycolor="#a5d6a7", bgcolor="#fdf8f0",
                 center=dict(lat=-1.25, lon=36.69), projection_scale=8),
    )
    st.plotly_chart(fig, width="stretch")


def render():
    st.markdown("""
    <div class="section-header">
      <h2>🌍 Alumni Atlas</h2>
      <p>Where are Dagoretti graduates today? Every pin is a story.</p>
    </div>
    """, unsafe_allow_html=True)

    df = _load()

    # ── Network stats bar (always visible, even when empty) ───────────────────
    n_reg        = len(df)
    n_countries  = df["country"].nunique() if not df.empty else 0
    n_industries = df["industry"].nunique() if not df.empty else 0
    n_mentors    = int((df["mentoring"] == "Yes").sum()) if not df.empty else 0
    pct          = int(n_reg / COMMUNITY_SIZE * 100)

    st.markdown(f"""
    <div class="card" style="background:linear-gradient(135deg,#1a5c2e 0%,#2e7d32 100%);
         color:#fff; padding:1rem 1.5rem; margin-bottom:1rem; border-radius:8px;">
      <div style="font-size:0.78rem; letter-spacing:1px; text-transform:uppercase;
           opacity:0.8; margin-bottom:0.5rem;">🦁 Dagoretti High · Class of 2001 Network</div>
      <div style="display:flex; gap:2rem; flex-wrap:wrap; align-items:center;">
        <div><span style="font-size:1.9rem; font-weight:700;">{n_reg}</span>
             <span style="font-size:0.82rem; opacity:0.8;"> / {COMMUNITY_SIZE} registered</span></div>
        <div><span style="font-size:1.4rem; font-weight:600;">{n_countries}</span>
             <span style="font-size:0.82rem; opacity:0.8;"> countries</span></div>
        <div><span style="font-size:1.4rem; font-weight:600;">{n_industries}</span>
             <span style="font-size:0.82rem; opacity:0.8;"> industries</span></div>
        <div><span style="font-size:1.4rem; font-weight:600;">{n_mentors}</span>
             <span style="font-size:0.82rem; opacity:0.8;"> mentors</span></div>
      </div>
      <div style="margin-top:0.6rem; background:rgba(255,255,255,0.2);
           border-radius:4px; height:6px; width:100%;">
        <div style="background:#a5d6a7; height:6px; border-radius:4px;
             width:{pct}%; transition:width 0.4s;"></div>
      </div>
      <div style="font-size:0.72rem; opacity:0.7; margin-top:0.3rem;">{pct}% of known alumni on the map</div>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.markdown("""
        <div class="card" style="text-align:center; padding:2.5rem 1.5rem;">
          <div style="font-size:3rem; margin-bottom:1rem;">🌍</div>
          <h3 style="color:var(--green-dark); margin:0 0 0.5rem;">No alumni on the map yet.</h3>
          <p style="color:var(--text-muted); font-size:0.95rem; margin:0 0 1.2rem;">
            The Atlas grows as alumni register themselves.<br>
            Every verified profile becomes a pin.
          </p>
        </div>
        """, unsafe_allow_html=True)
        st.info("👆 Use the **Submit Data → Alumni Profile** tab to add yourself.")
        _render_school_pin_only()
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
        if year_min < year_max:
            year_range = st.slider("Graduation year", year_min, year_max, (year_min, year_max))
        else:
            st.caption(f"Graduation year: {year_min}")
            year_range = (year_min, year_max)

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
        import pandas as _pd2
        # Add school gate as a fixed anchor pin
        school_pin = _pd2.DataFrame([{
            "name": "🦁 Dagoretti High School",
            "lat": SCHOOL_LAT, "lon": SCHOOL_LON,
            "role": "Where it all started — Class of '01",
            "city": "Kikuyu Road", "country": "Kenya",
            "year": 0, "industry": "📍 Origin",
        }])
        map_df = _pd2.concat([fdf.assign(industry=fdf["industry"]), school_pin], ignore_index=True)

        fig = px.scatter_geo(
            map_df,
            lat="lat", lon="lon",
            color="industry",
            hover_name="name",
            hover_data={"role": True, "city": True, "country": True, "year": True, "lat": False, "lon": False},
            projection="natural earth",
            title="",
            color_discrete_sequence=px.colors.qualitative.Safe,
            height=480,
        )
        # Style alumni pins
        fig.update_traces(marker=dict(size=9, opacity=0.85, line=dict(width=0.5, color="white")))
        # Style school pin differently (gold star, larger)
        for trace in fig.data:
            if trace.name == "📍 Origin":
                trace.marker.update(size=14, color="#c9a94e", symbol="star",
                                    line=dict(width=1.5, color="#1a5c2e"), opacity=1.0)
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="#fdf8f0",
            geo=dict(
                showframe=False, showcoastlines=True, coastlinecolor="#c8e6c9",
                showland=True, landcolor="#e8f5e9", showocean=True, oceancolor="#e3f2fd",
                showlakes=True, lakecolor="#e3f2fd", showcountries=True,
                countrycolor="#a5d6a7", bgcolor="#fdf8f0",
            ),
            legend=dict(orientation="h", y=-0.05, x=0, font=dict(size=11)),
        )
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("No alumni match the current filters.")
        _render_school_pin_only()

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
            mentor_badge = '<span class="badge-gold">🤝 Mentoring</span>' if row.get("mentoring") == "Yes" else ""
            li_url = str(row.get("linkedin", "") or "")
            linkedin_html = (
                f'<a href="{li_url}" target="_blank" style="color:var(--green-mid); font-size:0.8rem; display:inline-block; margin-top:0.3rem;">LinkedIn &#8594;</a>'
                if li_url.startswith("http") else ""
            )
            bio_val = str(row.get("bio_short", "") or "").strip()
            bio_html = f'<p style="margin:0.3rem 0 0; font-size:0.85rem; color:var(--text-muted);">{bio_val}</p>' if bio_val else ""
            card = (
                '<div class="alumni-card">'
                f'<h4>{row["name"]} <span style="font-weight:400; color:var(--text-muted); font-size:0.85rem;">· Class of {int(row["year"])}</span></h4>'
                f'<p>{row["role"]} · {row["city"]}, {row["country"]}</p>'
                f'<span class="badge">{row["industry"]}</span> {mentor_badge}'
                f'{linkedin_html}{bio_html}'
                '</div>'
            )
            st.markdown(card, unsafe_allow_html=True)
    else:
        st.info("No alumni match the current filters.")

    st.markdown("---")

    # ── Leaderboard ───────────────────────────────────────────────────────────
    if not df.empty:
        st.markdown("""
        <div class="section-header">
          <h2>📊 Network Leaderboard</h2>
          <p>Where the brotherhood has landed</p>
        </div>
        """, unsafe_allow_html=True)

        lb1, lb2 = st.columns(2)

        with lb1:
            city_counts = df["city"].value_counts().head(8)
            if not city_counts.empty:
                rows_html = "".join(
                    f'<tr><td style="font-size:0.85rem; padding:0.25rem 0.5rem;">'
                    f'<span style="color:#888; font-size:0.78rem; margin-right:0.4rem;">{i+1}.</span>'
                    f'{city}</td>'
                    f'<td style="font-weight:700; color:var(--green-dark); text-align:right; '
                    f'padding:0.25rem 0.5rem;">{count}</td></tr>'
                    for i, (city, count) in enumerate(city_counts.items())
                )
                st.markdown(f"""
                <div class="card">
                  <strong style="font-size:0.9rem; color:var(--green-dark);">🏙️ Top Cities</strong>
                  <table style="width:100%; border-collapse:collapse; margin-top:0.5rem;">
                    {rows_html}
                  </table>
                </div>
                """, unsafe_allow_html=True)

        with lb2:
            ind_counts = df["industry"].value_counts().head(8)
            if not ind_counts.empty:
                rows_html = "".join(
                    f'<tr><td style="font-size:0.85rem; padding:0.25rem 0.5rem;">'
                    f'<span style="color:#888; font-size:0.78rem; margin-right:0.4rem;">{i+1}.</span>'
                    f'{ind}</td>'
                    f'<td style="font-weight:700; color:var(--green-dark); text-align:right; '
                    f'padding:0.25rem 0.5rem;">{count}</td></tr>'
                    for i, (ind, count) in enumerate(ind_counts.items())
                )
                st.markdown(f"""
                <div class="card">
                  <strong style="font-size:0.9rem; color:var(--green-dark);">💼 Industries</strong>
                  <table style="width:100%; border-collapse:collapse; margin-top:0.5rem;">
                    {rows_html}
                  </table>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
      Alumni data is community-maintained. Add yourself via the Submit Data page.
    </div>
    """, unsafe_allow_html=True)
