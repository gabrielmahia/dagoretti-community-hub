"""
Home page — landing stats, alumni spotlight, welcome content.
"""

import streamlit as st
import pandas as pd
import os


@st.cache_data(ttl=60)
def _load_alumni():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "alumni.csv")
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        return pd.DataFrame()


def render():
    df = _load_alumni()
    # Compute KCSE year count dynamically
    try:
        import pandas as _pd_kcse
        _kcse_df = _pd_kcse.read_csv(os.path.join(os.path.dirname(__file__), "..", "data", "kcse_results.csv"))
        _kcse_years = int(_kcse_df["year"].count())
    except Exception:
        _kcse_years = 0

    # ── Hero ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-banner">
      <h1>🦁 Dagoretti High School Community Hub</h1>
      <p>Alumni · Students · Parents · Teachers — one platform, one pride.</p>
      <p style='margin-top:0.5rem; font-size:0.9rem; color:#81c784;'>
        Est. 1961 · Kikuyu Road, Nairobi · Open to all classes · Class of 2001: 25th Reunion 2026 🎉
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats row ────────────────────────────────────────────────────────────
    n_alumni    = len(df) if not df.empty else 0
    n_countries = df["country"].nunique() if not df.empty else 0
    n_mentors   = int((df["mentoring"] == "Yes").sum()) if not df.empty else 0
    n_classes   = df["year"].nunique() if not df.empty else 0
    try:
        import pandas as _pds
        _sch = _pds.read_csv(os.path.join(os.path.dirname(__file__), "..", "data", "scholarships.csv"))
        n_scholarships = len(_sch)
    except Exception:
        n_scholarships = 22  # known baseline

    stats = [
        (n_alumni,       "Alumni in directory"),
        (n_countries,    "Countries represented"),
        (n_mentors,      "Mentors available"),
        (n_classes,      "Classes registered"),
        (n_scholarships, "Scholarships listed"),
        (_kcse_years,    "Confirmed KCSE years"),
    ]
    pills = "".join(
        f'<div class="stat-pill" style="flex:1 1 140px; min-width:120px;">' +
        f'<span class="stat-n">{n}</span>' +
        f'<span class="stat-lbl">{lbl}</span>' +
        '</div>'
        for n, lbl in stats
    )
    st.markdown(
        f'<div style="display:flex; flex-wrap:wrap; gap:0.6rem; margin-bottom:1rem;">{pills}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Main columns ─────────────────────────────────────────────────────────
    left, right = st.columns([3, 2])

    with left:
        st.markdown("""
        <div class="section-header">
          <h2>Welcome to the Hub</h2>
          <p>Built by alumni, for the community</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card-green">
          <p>This platform is your connection point to the Dagoretti community — wherever
          you are in the world. Whether you graduated in 1995 or 2024, whether you are a
          student planning your next step, a parent exploring scholarships, or a teacher
          looking for resources, there is something here for you.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header">
          <h2>🎉 Class of 2001 — 25th Reunion</h2>
          <p>A special milestone worth celebrating</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card-gold">
          <p><strong>This year marks 25 years since the Class of 2001 left Dagoretti.</strong>
          From Nairobi to New York, London to Dubai — they are now doctors, engineers,
          advocates, entrepreneurs, and community builders. The Memory Wall page honours
          their stories. If you are Class of 2001, add your update via Submit Data.</p>
        </div>
        """, unsafe_allow_html=True)

        # Quick navigation
        st.markdown("""
        <div class="section-header">
          <h2>Explore the Hub</h2>
          <p>Use the sidebar to navigate, or start here</p>
        </div>
        """, unsafe_allow_html=True)

        features = [
            ("🌍", "Alumni Atlas", "See where Dagoretti graduates live and work — plotted on a world map."),
            ("📅", "Events", "Upcoming reunions, career days, networking events — and the Class of 2001 25th reunion."),
            ("📊", "KCSE Tracker", f"{_kcse_years} confirmed years of verified exam results. More years added as alumni contribute sources."),
            ("🧭", "Career Pathways", "Enter your KCSE subjects and grades. Explore matching careers and universities."),
            ("🎓", "Scholarships", "Curated scholarships — including diaspora-accessible international awards."),
            ("🤝", "Mentorship", "Connect with alumni open to guiding students and early-career graduates."),
            ("🇰🇪", "Kenya: Then & Now", "25 indicators comparing Kenya in 2001 and 2025. The transformation is striking."),
        ]

        for emoji, title, desc in features:
            st.markdown(f"""
            <div class="card">
              <strong>{emoji} {title}</strong><br>
              <span style='color:var(--text-muted); font-size:0.9rem;'>{desc}</span>
            </div>
            """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="section-header">
          <h2>Alumni Spotlight</h2>
          <p>A few faces from the directory</p>
        </div>
        """, unsafe_allow_html=True)

        # Spotlight only shows alumni who have self-registered via Submit Data.
        # No fabricated records are ever displayed here.
        if not df.empty:
            spotlight = df[df["year"] == 2001]
            if spotlight.empty:
                spotlight = df
            spotlight = spotlight.head(6)

            for _, row in spotlight.iterrows():
                mentor_badge = '<span class="badge-gold">Mentoring ✓</span>' if row.get("mentoring") == "Yes" else ""
                li_url = str(row.get("linkedin", "") or "")
                linkedin_html = (
                    f'<a href="{li_url}" target="_blank" style="color:var(--green-mid); font-size:0.8rem; display:inline-block; margin-top:0.3rem;">LinkedIn &#8594;</a>'
                    if li_url.startswith("http") else ""
                )
                bio_val = str(row.get("bio_short", "") or "").strip()
                bio_html = f'<p style="margin-top:0.4rem; font-size:0.82rem; color:var(--text-muted);">{bio_val}</p>' if bio_val else ""
                card = (
                    '<div class="alumni-card">'
                    f'<h4>{row["name"]} <span style="font-weight:400; font-size:0.85rem; color:var(--text-muted);">({int(row["year"])})</span></h4>'
                    f'<p>{row["role"]} · {row["city"]}, {row["country"]}</p>'
                    f'<span class="badge">{row["industry"]}</span> {mentor_badge}'
                    f'{linkedin_html}{bio_html}'
                    '</div>'
                )
                st.markdown(card, unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="alumni-card" style="text-align:center; padding:2rem 1rem;">'
                '<p style="font-size:1.1rem; font-weight:600; color:var(--green-dark);">Be the first to appear here.</p>'
                '<p style="font-size:0.9rem; color:var(--text-muted); margin-top:0.5rem;">'
                'The spotlight shows alumni who register themselves.<br>'
                'No names are placed here without your consent.'
                '</p></div>',
                unsafe_allow_html=True,
            )

        st.markdown("""
        <div class="card-gold" style='margin-top:1rem; text-align:center;'>
          <strong>Are you a Dagoretti alumnus?</strong><br>
          <span style='font-size:0.9rem;'>Add yourself to the directory via the Submit Data page.</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Footer ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="footer">
      🦁 Dagoretti High School Community Hub · Open source · Built by alumni for the community ·
      <a href='https://github.com/gabrielmahia/dagoretti-community-hub'>GitHub</a> ·
      <a href='mailto:contact@aikungfu.dev'>contact@aikungfu.dev</a>
    </div>
    """, unsafe_allow_html=True)
