"""
Dagoretti High School Community Hub
Entry point: global CSS injection, sidebar navigation, page routing.
Keep this file thin — all page logic lives in pages/ modules.
"""

import streamlit as st

st.set_page_config(
    page_title="Dagoretti Community Hub",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Variables ── */
  :root {
    --green-dark:  #1a5c2e;
    --green-mid:   #2e7d46;
    --green-light: #e8f5e9;
    --gold:        #c9a94e;
    --gold-light:  #fdf3d9;
    --cream:       #fdf8f0;
    --text:        #0d1a0f;
    --text-muted:  #4a5e4d;
    --shadow:      0 2px 8px rgba(26,92,46,0.10);
    --radius:      8px;
  }

  /* ── Base ── */
  html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--cream);
    color: var(--text);
  }
  [data-testid="stSidebar"] { background-color: var(--green-dark) !important; }
  [data-testid="stSidebar"] * { color: #f0f7f2 !important; }
  [data-testid="stSidebar"] a { color: var(--gold) !important; }
  [data-testid="stSidebar"] .stSelectbox label { color: #c8e6c9 !important; }

  /* ── Hero Banner ── */
  .hero-banner {
    background: linear-gradient(135deg, var(--green-dark) 0%, #0d3d1e 100%);
    border-bottom: 3px solid var(--gold);
    color: #fff;
    padding: 2.5rem 2rem 2rem;
    border-radius: var(--radius);
    margin-bottom: 1.5rem;
  }
  .hero-banner h1 { color: #fff; margin: 0 0 0.4rem; font-size: 2.2rem; }
  .hero-banner p  { color: #c8e6c9; margin: 0; font-size: 1.05rem; }

  /* ── Section Header ── */
  .section-header {
    border-left: 4px solid var(--gold);
    padding: 0.5rem 0 0.5rem 1rem;
    margin: 1.5rem 0 1rem;
  }
  .section-header h2 { margin: 0; color: var(--green-dark); font-size: 1.5rem; }
  .section-header p  { margin: 0.2rem 0 0; color: var(--text-muted); font-size: 0.95rem; }

  /* ── Cards ── */
  .card {
    background: #fff;
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
  }
  .card-green {
    background: #fff;
    border-left: 4px solid var(--green-mid);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
  }
  .card-gold {
    background: var(--gold-light);
    border-left: 4px solid var(--gold);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
  }

  /* ── Alumni Card ── */
  .alumni-card {
    background: #fff;
    border-radius: var(--radius);
    padding: 1.1rem 1.3rem;
    box-shadow: var(--shadow);
    margin-bottom: 0.75rem;
    transition: box-shadow 0.2s ease, transform 0.15s ease;
    border: 1px solid #e8f0e9;
  }
  .alumni-card:hover {
    box-shadow: 0 4px 16px rgba(26,92,46,0.18);
    transform: translateY(-1px);
  }
  .alumni-card h4 { margin: 0 0 0.25rem; color: var(--green-dark); }
  .alumni-card p  { margin: 0; color: var(--text-muted); font-size: 0.88rem; }

  /* ── Badges ── */
  .badge {
    display: inline-block;
    background: var(--green-light);
    color: var(--green-dark);
    border: 1px solid #a5d6a7;
    border-radius: 20px;
    padding: 0.15rem 0.65rem;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 0.1rem 0.2rem 0.1rem 0;
  }
  .badge-gold {
    display: inline-block;
    background: var(--gold-light);
    color: #7a5c00;
    border: 1px solid var(--gold);
    border-radius: 20px;
    padding: 0.15rem 0.65rem;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 0.1rem 0.2rem 0.1rem 0;
  }
  .badge-blue {
    display: inline-block;
    background: #e3f2fd;
    color: #1565c0;
    border: 1px solid #90caf9;
    border-radius: 20px;
    padding: 0.15rem 0.65rem;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 0.1rem 0.2rem 0.1rem 0;
  }

  /* ── Stat Pill ── */
  .stat-pill {
    background: var(--green-dark);
    color: #fff;
    border-radius: var(--radius);
    padding: 1rem 1.5rem;
    text-align: center;
    min-width: 100px;
  }
  .stat-pill .stat-n  { font-size: 2.2rem; font-weight: 700; color: var(--gold); display: block; line-height: 1; }
  .stat-pill .stat-lbl{ font-size: 0.82rem; color: #c8e6c9; display: block; margin-top: 0.25rem; }

  /* ── Scholarship Card ── */
  .scholarship-card {
    background: #fff;
    border-top: 3px solid var(--gold);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
  }
  .scholarship-card h4 { margin: 0 0 0.3rem; color: var(--green-dark); }
  .scholarship-card p  { margin: 0; color: var(--text-muted); font-size: 0.9rem; }

  /* ── Timeline Item ── */
  .timeline-item {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 0.75rem 0;
    border-bottom: 1px dashed #d4e8d6;
  }
  .timeline-year {
    width: 52px; height: 52px;
    background: var(--green-dark);
    color: var(--gold);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.75rem;
    flex-shrink: 0;
    text-align: center;
    line-height: 1.1;
  }
  .timeline-content h4 { margin: 0 0 0.2rem; color: var(--text); font-size: 0.95rem; }
  .timeline-content p  { margin: 0; color: var(--text-muted); font-size: 0.85rem; }

  /* ── Footer ── */
  .footer {
    background: var(--green-dark);
    color: #c8e6c9;
    border-radius: var(--radius);
    padding: 1.2rem 1.5rem;
    margin-top: 2rem;
    font-size: 0.85rem;
    text-align: center;
  }
  .footer a { color: var(--gold); text-decoration: none; }

  /* ── Misc Streamlit overrides ── */
  div[data-testid="stMetricValue"] { color: var(--green-dark); }
  .stButton button {
    background-color: var(--green-dark);
    color: #fff;
    border: none;
    border-radius: 6px;
    font-weight: 600;
  }
  .stButton button:hover { background-color: var(--green-mid); }
  h1, h2, h3 { color: var(--green-dark); }
</style>
""", unsafe_allow_html=True)


# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 0.5rem 0 1.5rem;'>
      <div style='font-size:3rem;'>🦁</div>
      <div style='font-size:1.1rem; font-weight:700; color:#f0f7f2;'>Dagoretti High School</div>
      <div style='font-size:0.8rem; color:#a5d6a7; margin-top:0.2rem;'>Community Hub</div>
      <div style='font-size:0.7rem; color:#81c784; margin-top:0.15rem;'>Est. 1961 · Nairobi, Kenya 🇰🇪</div>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        "🏠 Home":              "home",
        "🌍 Alumni Atlas":      "alumni_atlas",
        "📊 KCSE Tracker":      "kcse_tracker",
        "🧭 Career Pathways":   "career_pathways",
        "🕯️ Memory Wall":       "memory_wall",
        "🇰🇪 Kenya: Then & Now": "then_now",
        "🤝 Mentorship":        "mentorship",
        "🎓 Scholarships":      "scholarships",
        "📝 Submit Data":       "submit",
    }

    page_key = st.selectbox(
        "Navigate",
        list(pages.keys()),
        label_visibility="collapsed",
    )

    st.markdown("""
    <div style='margin-top:2rem; padding-top:1rem; border-top:1px solid #2e7d46; font-size:0.75rem; color:#81c784; text-align:center;'>
      Built by alumni · For the community<br>
      <a href='https://github.com/dagoretti-community/hub' style='color:#c9a94e;'>GitHub</a> ·
      <a href='mailto:alumni@dagoretti.ac.ke' style='color:#c9a94e;'>Contact</a>
    </div>
    """, unsafe_allow_html=True)

page = pages[page_key]


# ── ROUTING ──────────────────────────────────────────────────────────────────
if page == "home":
    from pages import home as p; p.render()
elif page == "alumni_atlas":
    from pages import alumni_atlas as p; p.render()
elif page == "kcse_tracker":
    from pages import kcse_tracker as p; p.render()
elif page == "career_pathways":
    from pages import career_pathways as p; p.render()
elif page == "memory_wall":
    from pages import memory_wall as p; p.render()
elif page == "then_now":
    from pages import then_now as p; p.render()
elif page == "mentorship":
    from pages import mentorship as p; p.render()
elif page == "scholarships":
    from pages import scholarships as p; p.render()
elif page == "submit":
    from pages import submit as p; p.render()
