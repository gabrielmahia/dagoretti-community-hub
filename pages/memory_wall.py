"""
Memory Wall — Class of 2000 · 25th anniversary tribute.
A curated collection of memories, milestones, and messages.
"""

import streamlit as st
import pandas as pd
import os


@st.cache_data
def _load_alumni():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "alumni.csv")
    try:
        df = pd.read_csv(path)
        return df[df["year"] == 2000].reset_index(drop=True)
    except FileNotFoundError:
        return pd.DataFrame()


# ── Curated Class of 2000 memories ───────────────────────────────────────────
MEMORIES = [
    {
        "year": "1996",
        "title": "Form 1 Intake — September 1996",
        "body": "200 students walked through the Dagoretti gates for the first time. "
                "Uniforms too large, bags too heavy, the city visible from the school hill. "
                "We didn't know we were starting a journey that would take us to five continents.",
    },
    {
        "year": "1997",
        "title": "The Science Block",
        "body": "Chemistry practicals in Form 2. The smell of the lab. Mr. Kamau's chalk diagrams that "
                "somehow made organic chemistry make sense. Several of us are now medical professionals "
                "because of those afternoons.",
    },
    {
        "year": "1998",
        "title": "The Debate Team",
        "body": "Dagoretti debate team won the Nairobi Division championship in 1998. Four of the team "
                "members went on to careers in law, journalism, and public policy. Coincidence?",
    },
    {
        "year": "1999",
        "title": "Form 4 Mock Exams",
        "body": "October 1999. The pressure of mocks. Late nights in the hostels. Sharing notes under "
                "torchlight. Some of us barely slept for three weeks. All of us got through.",
    },
    {
        "year": "2000",
        "title": "KCSE November 2000",
        "body": "We sat our final papers in November 2000. The school's mean grade that year was 6.4 — "
                "the highest it had been. James Mwangi got the top grade. We all went home not knowing "
                "exactly what came next. But we had Dagoretti behind us.",
    },
    {
        "year": "2000",
        "title": "Graduation Day",
        "body": "December 2000. The school field. Parents in their best. Teachers trying to look stern "
                "while secretly proud. We were 18, we were ready, and the world was waiting. "
                "That was 25 years ago.",
    },
]

MESSAGES = [
    {
        "name": "James Mwangi",
        "role": "Group CEO · Nairobi",
        "message": "Dagoretti taught me that excellence is not a destination, it is a discipline. "
                   "Twenty-five years later, I still remember what that discipline feels like.",
    },
    {
        "name": "Grace Wanjiku",
        "role": "Software Engineer · Toronto",
        "message": "I left Kenya carrying a KCSE certificate and a belief that I could compete anywhere. "
                   "Dagoretti put that belief in me. I think about that often when I mentor young Kenyan engineers.",
    },
    {
        "name": "David Ochieng",
        "role": "Consultant Physician · London",
        "message": "Biology class at Dagoretti is where I first understood the human body as a system. "
                   "That curiosity has never left me. Thank you to every teacher who fed it.",
    },
    {
        "name": "Esther Akinyi",
        "role": "Senior Advocate · Nairobi",
        "message": "The debate club shaped how I think and how I argue. "
                   "Every courtroom appearance has a little bit of Dagoretti in it.",
    },
    {
        "name": "Peter Kariuki",
        "role": "Regional Director · Johannesburg",
        "message": "I have worked across six African countries. The one constant is that a Dagoretti "
                   "education opens doors. People recognise the standard.",
    },
    {
        "name": "Mary Waithera",
        "role": "Foreign Correspondent · Washington DC",
        "message": "I cover African stories for international audiences. "
                   "I became a journalist because Dagoretti teachers told me my writing mattered. "
                   "That vote of confidence changed everything.",
    },
]


def render():
    st.markdown("""
    <div class="hero-banner">
      <h1>🕯️ Memory Wall</h1>
      <p>Class of 2000 · 25th Reunion · 1996–2000</p>
      <p style='color:#81c784; margin-top:0.5rem;'>
        From the gates of Dagoretti to five continents — 25 years of remarkable journeys.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-gold">
      <strong>🎉 Class of 2000 — 25th Anniversary, 2025</strong><br>
      This page is a tribute to the men and women who walked out of Dagoretti High School in 2000
      and spent the next 25 years building lives, careers, and families across Kenya and the world.
      If you are Class of 2000, add your update via the Submit Data page.
    </div>
    """, unsafe_allow_html=True)

    # ── Timeline ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>The Journey: 1996–2000</h2>
      <p>Four years that shaped a generation</p>
    </div>
    """, unsafe_allow_html=True)

    for mem in MEMORIES:
        st.markdown(f"""
        <div class="timeline-item">
          <div class="timeline-year">{mem['year']}</div>
          <div class="timeline-content">
            <h4>{mem['title']}</h4>
            <p>{mem['body']}</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Class directory ────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>Class of 2000 — Where Are They Now?</h2>
      <p>Alumni from the directory</p>
    </div>
    """, unsafe_allow_html=True)

    df = _load_alumni()
    if not df.empty:
        cols = st.columns(2)
        for i, (_, row) in enumerate(df.iterrows()):
            with cols[i % 2]:
                mentor = '<span class="badge-gold">Mentoring ✓</span>' if row.get("mentoring") == "Yes" else ""
                st.markdown(f"""
                <div class="alumni-card">
                  <h4>{row['name']}</h4>
                  <p>{row['role']} · {row['city']}, {row['country']}</p>
                  <div style='margin:0.3rem 0;'>
                    <span class="badge">{row['industry']}</span>
                    {mentor}
                  </div>
                  <p style='font-size:0.83rem; color:var(--text-muted);'>{row.get("bio_short","")}</p>
                </div>
                """, unsafe_allow_html=True)

    # ── Messages from the class ────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>Messages from the Class</h2>
      <p>25 years on, looking back</p>
    </div>
    """, unsafe_allow_html=True)

    for msg in MESSAGES:
        st.markdown(f"""
        <div class="card-green">
          <p style='font-style:italic; font-size:1.02rem; color:var(--text);'>
            &#x201C;{msg['message']}&#x201D;
          </p>
          <p style='margin-top:0.6rem; font-weight:600; color:var(--green-dark);'>
            — {msg['name']}, {msg['role']}
          </p>
        </div>
        """, unsafe_allow_html=True)

    # ── Call to action ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class="card-gold" style='text-align:center; margin-top:1.5rem;'>
      <strong>Are you Class of 2000?</strong><br>
      <p>Add your story to the Memory Wall. Use the Submit Data page to share an update,
      a memory, or a message for current students.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
      Memory Wall · Class of 2000 · 25th Reunion 2025 ·
      <a href='mailto:alumni@dagoretti.ac.ke'>Contact the alumni team</a>
    </div>
    """, unsafe_allow_html=True)
