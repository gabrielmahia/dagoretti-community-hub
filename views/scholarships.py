"""
Scholarships — 25 curated opportunities with search and diaspora filter.

DATA NOTE: Amounts and deadlines change annually. The CSV stores ballpark
notes only. Users are directed to the official provider link for current details.
Inline correction forms are available on every card.
"""

import streamlit as st
import pandas as pd
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import sheets


@st.cache_data
def _load():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "scholarships.csv")
    try:
        return pd.read_csv(path).fillna("")
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
    <div class="card-gold">
      <strong>⚠️ Always verify at the official source.</strong>
      Deadlines and award amounts change every cycle. Links go directly to the provider.
      If a link is broken or a deadline is wrong, use the correction form on the card.
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

    st.caption(f"Showing {len(fdf)} of {len(df)} scholarships")

    if fdf.empty:
        st.info("No scholarships match the current filters.")
        return

    # ── Scholarship cards ─────────────────────────────────────────────────────
    for idx, (_, row) in enumerate(fdf.iterrows()):
        diaspora_badge = (
            '<span class="badge-gold">✈️ Diaspora OK</span>'
            if row.get("diaspora_relevant") == "Yes"
            else '<span class="badge">🇰🇪 Kenya-based</span>'
        )
        amount_note   = str(row.get("amount_note", "Verify at provider"))
        deadline_note = str(row.get("deadline_note", "Verify at provider"))

        link_url = str(row.get("link", "")).strip()
        link_html = (
            f'<a href="{link_url}" target="_blank" '
            f'style="background:var(--green-dark); color:#fff; padding:0.25rem 0.8rem; '
            f'border-radius:4px; font-size:0.82rem; text-decoration:none;">'
            f'Official site &#8594;</a>'
        ) if link_url.startswith("http") else ""

        desc = str(row.get("description", "")).strip()
        desc_html = f'<p style="margin:0.4rem 0 0; font-size:0.88rem;">{desc}</p>' if desc and desc != "nan" else ""

        card = (
            '<div class="scholarship-card">'
            '<div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.4rem;">'
            f'<h4 style="margin:0;">{row["name"]}</h4>'
            f'<span style="font-size:0.82rem; font-weight:600; color:var(--green-dark);">{amount_note}</span>'
            '</div>'
            f'<p style="margin:0.2rem 0; color:var(--text-muted); font-size:0.9rem;">{row["provider"]} · {row["destination"]}</p>'
            '<div style="margin:0.4rem 0;">'
            f'<span class="badge">{row["level"]}</span> '
            f'<span class="badge-blue">{row["field"]}</span> '
            f'{diaspora_badge}'
            '</div>'
            f'{desc_html}'
            '<div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.6rem; flex-wrap:wrap; gap:0.3rem;">'
            f'<span style="font-size:0.82rem; color:var(--text-muted);">📅 {deadline_note}</span>'
            f'{link_html}'
            '</div>'
            '</div>'
        )
        st.markdown(card, unsafe_allow_html=True)

        sheets.suggest_correction_button(
            page="Scholarships",
            field=f"{row['name']} — deadline / link / amount",
            current_value=f"deadline: {deadline_note} | amount: {amount_note}",
            key=f"sch_{idx}",
        )

    st.markdown("---")

    # ── Application guide ─────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>📋 Application Guide</h2>
    </div>
    """, unsafe_allow_html=True)

    tips = [
        ("📝 Start early", "Most scholarships require transcripts, recommendation letters, and essays. Collecting these takes weeks. Start 3 months before the deadline."),
        ("🎯 Target ruthlessly", "Apply to 3–5 well-matched scholarships rather than 15 long shots. Tailored applications consistently outperform generic ones."),
        ("🤝 Network through alumni", "Dagoretti alumni who have held these scholarships are your best resource. Use the Mentorship page to connect."),
        ("📄 KCSE certificate matters", "Keep a certified copy of your KCSE certificate and transcript. Most applications require it at short notice."),
        ("🌍 Diaspora advantage", "If you are outside Kenya, diaspora-tagged scholarships have shorter applicant pools. Filter the list above."),
    ]
    for title, body in tips:
        st.markdown(f"""
        <div class="card" style='margin-bottom:0.6rem;'>
          <strong>{title}</strong>
          <p style='margin:0.2rem 0 0; font-size:0.88rem;'>{body}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-gold" style='text-align:center; margin-top:1rem;'>
      <strong>Know a scholarship not listed here?</strong>
      <p style='margin:0.3rem 0 0; font-size:0.88rem;'>
        Use <strong>Submit Data → Feedback</strong> (type: Scholarship suggestion) to propose an addition.
      </p>
    </div>
    """, unsafe_allow_html=True)
