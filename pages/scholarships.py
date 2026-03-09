"""
Scholarships — 25 curated opportunities with search and diaspora filter.
"""

import streamlit as st
import pandas as pd
import os


@st.cache_data
def _load():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "scholarships.csv")
    try:
        df = pd.read_csv(path)
        df["amount_usd"] = pd.to_numeric(df["amount_usd"], errors="coerce").fillna(0)
        return df
    except FileNotFoundError:
        return pd.DataFrame()


def render():
    st.markdown("""
    <div class="section-header">
      <h2>🎓 Scholarships</h2>
      <p>25 curated opportunities — Kenya, regional, and international</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-green">
      This directory covers scholarships accessible to Kenyan secondary school leavers and university
      students. Diaspora-relevant scholarships (marked with ✈️) are open to applicants outside Kenya.
      Always verify deadlines and eligibility at the official source — this data is curated but may
      not reflect real-time changes.
    </div>
    """, unsafe_allow_html=True)

    df = _load()
    if df.empty:
        st.error("Scholarship data not found.")
        return

    # ── Filters ───────────────────────────────────────────────────────────────
    f1, f2, f3 = st.columns(3)
    with f1:
        levels = ["All Levels"] + sorted(df["level"].dropna().unique().tolist())
        level_f = st.selectbox("Level", levels)
    with f2:
        dests = ["All Destinations"] + sorted(df["destination"].dropna().unique().tolist())
        dest_f = st.selectbox("Destination", dests)
    with f3:
        diaspora_only = st.checkbox("Diaspora-accessible only ✈️", value=False)

    fdf = df.copy()
    if level_f != "All Levels":
        fdf = fdf[fdf["level"].str.contains(level_f.split("/")[0], na=False)]
    if dest_f != "All Destinations":
        fdf = fdf[fdf["destination"] == dest_f]
    if diaspora_only:
        fdf = fdf[fdf["diaspora_relevant"] == "Yes"]

    # Sort by amount descending
    fdf = fdf.sort_values("amount_usd", ascending=False)

    st.caption(f"Showing {len(fdf)} of {len(df)} scholarships")

    if fdf.empty:
        st.info("No scholarships match the current filters.")
        return

    # ── Scholarship cards ─────────────────────────────────────────────────────
    for _, row in fdf.iterrows():
        diaspora_badge = '<span class="badge-gold">✈️ Diaspora OK</span>' if row.get("diaspora_relevant") == "Yes" \
                         else '<span class="badge">🇰🇪 Kenya-based</span>'
        amount = f"USD {int(row['amount_usd']):,}/year" if row['amount_usd'] > 0 else "Variable"

        st.markdown(f"""
        <div class="scholarship-card">
          <div style='display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.4rem;'>
            <h4 style='margin:0;'>{row['name']}</h4>
            <span style='font-size:1.1rem; font-weight:700; color:var(--green-dark);'>{amount}</span>
          </div>
          <p style='margin:0.2rem 0; color:var(--text-muted); font-size:0.9rem;'>
            {row['provider']} · {row['destination']}
          </p>
          <div style='margin:0.4rem 0;'>
            <span class="badge">{row['level']}</span>
            <span class="badge-blue">{row['field']}</span>
            {diaspora_badge}
          </div>
          <p style='margin:0.4rem 0 0; font-size:0.88rem;'>{row['description']}</p>
          <div style='display:flex; justify-content:space-between; align-items:center; margin-top:0.6rem; flex-wrap:wrap; gap:0.3rem;'>
            <span style='font-size:0.82rem; color:var(--text-muted);'>📅 Deadline: <strong>{row['deadline']}</strong></span>
            <a href='{row['link']}' target='_blank'
               style='background:var(--green-dark); color:#fff; padding:0.25rem 0.8rem;
                      border-radius:4px; font-size:0.82rem; text-decoration:none;'>
              Apply →
            </a>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Application guide ─────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>Application Guide</h2>
      <p>What makes a strong scholarship application</p>
    </div>
    """, unsafe_allow_html=True)

    guide = [
        ("📝 Start early", "Most scholarships require transcripts, recommendation letters, and essays. Collecting these takes weeks. Start 3 months before the deadline."),
        ("✉️ Recommendation letters", "Ask teachers and principals who know your work — not just those with impressive titles. A specific, personal letter beats a generic endorsement every time."),
        ("📖 The personal statement", "Connect your background, your Dagoretti experience, your goals, and why this specific scholarship fits. Generic statements are spotted instantly."),
        ("🌍 Diaspora applicants", "If you are applying from outside Kenya, filter for 'Diaspora OK' scholarships. You will still need academic records from Kenyan institutions — keep certified copies."),
        ("🔄 Apply to multiple", "Apply to 5–10 scholarships simultaneously. The top scholarships have single-digit acceptance rates. Breadth is a strategy, not a consolation."),
        ("📞 Contact the provider", "If you have genuine questions, email the scholarship office. Engaging professionally before you apply signals seriousness."),
    ]

    for title, body in guide:
        st.markdown(f"""
        <div class="card">
          <strong>{title}</strong><br>
          <span style='font-size:0.9rem; color:var(--text-muted);'>{body}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
      Scholarship data is curated and may not reflect real-time changes.
      Always verify at the official source before applying.
    </div>
    """, unsafe_allow_html=True)
