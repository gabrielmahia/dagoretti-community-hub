"""
Mentorship — directory of alumni open to mentoring, with guidance on how to connect.
"""

import streamlit as st
import pandas as pd
import os


@st.cache_data(ttl=300)
def _load():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "alumni.csv")
    try:
        df = pd.read_csv(path).fillna("")
        return df[df["mentoring"] == "Yes"].reset_index(drop=True)
    except FileNotFoundError:
        return pd.DataFrame()


def render():
    st.markdown("""
    <div class="section-header">
      <h2>🤝 Mentorship</h2>
      <p>Connect with Dagoretti alumni who have offered to guide the next generation</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-gold">
      <strong>How mentorship works here:</strong> Every mentor listed below is a Dagoretti alumnus
      who has explicitly opted in to being contacted. Reach out via LinkedIn where a profile
      is listed. For others, send an introduction through the Submit Data page with the subject
      "Mentorship Request" and the alumni team will make the introduction.
    </div>
    """, unsafe_allow_html=True)

    df = _load()

    if df.empty:
        st.markdown("""
        <div class="card" style="text-align:center; padding:2.5rem 1.5rem;">
          <div style="font-size:3rem; margin-bottom:1rem;">🤝</div>
          <h3 style="color:var(--green-dark); margin:0 0 0.5rem;">No mentors listed yet.</h3>
          <p style="color:var(--text-muted); font-size:0.95rem; margin:0 0 1.2rem;">
            Mentors are alumni who have explicitly opted in to being contacted.<br>
            Register yourself on the Submit Data page and tick <strong>Open to mentoring</strong>.
          </p>
        </div>
        """, unsafe_allow_html=True)
        st.info("👆 Use the **Submit Data → Alumni Profile** tab to register as a mentor.")
        return

    # ── Filters ───────────────────────────────────────────────────────────────
    fc1, fc2 = st.columns(2)
    with fc1:
        industries = ["All Industries"] + sorted(df["industry"].dropna().unique().tolist())
        ind_filter = st.selectbox("Filter by industry", industries)
    with fc2:
        locations = ["All Locations"] + sorted(df["country"].dropna().unique().tolist())
        loc_filter = st.selectbox("Filter by country", locations)

    fdf = df.copy()
    if ind_filter != "All Industries":
        fdf = fdf[fdf["industry"] == ind_filter]
    if loc_filter != "All Locations":
        fdf = fdf[fdf["country"] == loc_filter]

    st.caption(f"{len(fdf)} mentor{'s' if len(fdf) != 1 else ''} available")

    if fdf.empty:
        st.info("No mentors match the current filters.")
        return

    st.markdown("---")

    # ── Mentor cards ──────────────────────────────────────────────────────────
    cols = st.columns(2)
    for i, (_, row) in enumerate(fdf.iterrows()):
        with cols[i % 2]:
            li_url = str(row.get("linkedin", "") or "")
            linkedin_html = (
                f'<a href="{li_url}" target="_blank" style="display:inline-block; background:var(--green-dark); color:#fff; padding:0.25rem 0.75rem; border-radius:4px; font-size:0.8rem; text-decoration:none; margin-top:0.5rem;">LinkedIn &#8594;</a>'
                if li_url.startswith("http") else ""
            )
            bio_val = str(row.get("bio_short", "") or "").strip()
            bio_html = f'<p style="font-size:0.85rem; color:var(--text-muted); margin:0.4rem 0 0;">{bio_val}</p>' if bio_val else ""

            card = (
                '<div class="alumni-card" style="min-height:160px;">'
                f'<h4>{row["name"]} <span style="font-weight:400; font-size:0.82rem; color:var(--text-muted);">· Class of {int(row["year"])}</span></h4>'
                f'<p style="margin:0.15rem 0;">{row["role"]}</p>'
                f'<p style="margin:0; font-size:0.85rem; color:var(--text-muted);">{row["city"]}, {row["country"]}</p>'
                f'<span class="badge">{row["industry"]}</span> <span class="badge-gold">&#129309; Mentor</span>'
                f'{bio_html}{linkedin_html}'
                '</div>'
            )
            st.markdown(card, unsafe_allow_html=True)

    st.markdown("---")

    # ── How to reach out ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>How to Reach Out</h2>
      <p>Tips for a successful first contact</p>
    </div>
    """, unsafe_allow_html=True)

    tips = [
        ("1. Be specific", "Don't say 'I want career advice.' Say: 'I'm a Form 4 student interested in medicine. I would like 20 minutes to understand your path from KCSE to becoming a doctor.'"),
        ("2. Be brief", "Your first message should be 3–5 sentences maximum. Introduce yourself, explain what you need, and ask for a specific thing (a 20-minute call, one question answered by email)."),
        ("3. Mention Dagoretti", "The shared school connection matters. Say your year, your stream if you remember it, a teacher's name. It opens doors."),
        ("4. Follow up once", "If you don't hear back in two weeks, one follow-up is fine. After that, move to a different mentor."),
        ("5. Say thank you", "After any interaction — a call, an email reply, a LinkedIn connection — send a brief thank you. It's rare enough to be memorable."),
    ]

    for title, body in tips:
        st.markdown(f"""
        <div class="card-green">
          <strong>{title}</strong><br>
          <span style='font-size:0.9rem;'>{body}</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Become a mentor ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="card-gold" style='margin-top:1.5rem; text-align:center;'>
      <strong>Are you an alumnus? Become a mentor.</strong><br>
      <p>Update your listing via the Submit Data page and set "Open to mentoring: Yes".</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
      Mentor directory is community-maintained. All mentors have opted in voluntarily.
    </div>
    """, unsafe_allow_html=True)
