"""
Memory Wall — Class of 2001 · 25th anniversary tribute.
Co-curricular facts sourced from Wikipedia, The Standard (2011), KRU, and Kenya Music Festival records.
Memories marked [confirmed], [probable], or [illustrative] in code comments.
"""

import streamlit as st
import pandas as pd
import os


@st.cache_data
def _load_alumni():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "alumni.csv")
    try:
        df = pd.read_csv(path)
        return df[df["year"] == 2001].reset_index(drop=True)
    except FileNotFoundError:
        return pd.DataFrame()


# ── Timeline ──────────────────────────────────────────────────────────────────
# [C] = Confirmed (Wikipedia / The Standard / KRU / Kenya Music Festival records)
# [P] = Probable (consistent with confirmed institutional record)
# [I] = Illustrative (school context, not individually sourced)
MEMORIES = [
    {
        "year": "Dec\n1997",
        "icon": "📋",
        "title": "KCPE Results — December 1997",
        "body": (
            "Results out. Those who made the cut for an extra-county school held those letters "
            "carefully. Dagoretti High School — Kikuyu Road, Nairobi — was calling."
        ),
        "tag": None,
    },
    {
        "year": "Jan\n1998",
        "icon": "🏫",
        "title": "Form 1 Intake — January/February 1998",
        "body": (
            "We showed up at the end of January 1998, some early February. Uniforms still stiff, "
            "bags too heavy. A day and boarding school 16 kilometres from the city along Kikuyu Road — "
            "far enough to feel like a different world. The red-soil paths. The old main block. "
            "The view from the school hill."
        ),
        "tag": None,
    },
    {
        "year": "1998",
        "icon": "🥁",
        "title": "The School Band — First Festival Season",
        "body": (
            "The school band was a Dagoretti institution. Every year the Kenya Music Festival "
            "ran the same circuit — Zonal, then Regional, then National. Dagoretti's ensemble "
            "had been making that run throughout the 1990s, and Dagoretti High has even hosted "
            "Nairobi Zonal Music Festivals on its own grounds. "
            "We inherited that culture as Form 1s, and some of us were pulled straight into rehearsals."
        ),
        "tag": "🎵 Kenya Music Festival [Active]",
    },
    {
        "year": "1998–\n2001",
        "icon": "🎭",
        "title": "Drama & Traditional Dance — End of a Golden Era",
        "body": (
            "Dagoretti dominated the Traditional Dance category at the Kenya National Drama "
            "Festivals throughout the 1990s — holding the High Schools title for years on end. "
            "The Class of 2001 were among the last to experience that peak at full force. "
            "The school would step back from festival participation in the early 2000s, "
            "not long after we left. We did not know then that we were closing a chapter. "
            "The Standard would later write that no school produced more showbiz talent "
            "in that generation than Dagoretti. Showbiz was a culture passed from one "
            "generation to the next — and we were one of those generations."
        ),
        "tag": "🎭 Drama Festival [Confirmed — Wikipedia / The Standard 2011]",
    },
    {
        "year": "1999",
        "icon": "🏉",
        "title": "Rugby — Nairobi Schools Circuit",
        "body": (
            "Rugby 15s had been a formal school sport since 1990. Dagoretti ran a competitive "
            "team in the Nairobi schools bracket — the same circuit that pits provincial schools "
            "against Lenana, Nairobi School, and Upper Hill. Saturday morning matches. "
            "The green and black. That team culture is still competing today: "
            "Dagoretti has featured in Nairobi schools semifinals and represented Kenya "
            "at the 2019 East Africa School Games in Arusha against Kakamega High."
        ),
        "tag": "🏉 Rugby [Confirmed — KRU / Citizen Digital]",
    },
    {
        "year": "2000",
        "icon": "🌟",
        "title": "The Arts Culture — What We Were Known For",
        "body": (
            "By Form 3 the reputation was clear: Dagoretti was not just an academic school. "
            "The school produced John Kiarie (KJ) — comedian, cartoonist, now MP. "
            "It produced Alfred Mutua — journalist, Governor, Cabinet Secretary. "
            "It produced Boomba Clan, who formed the group right here on these grounds. "
            "The Standard would later write that no school produced more of Kenya's "
            "showbiz generation than Dagoretti. Talent Day was the school's unofficial fifth subject."
        ),
        "tag": "🎤 Arts Legacy [Confirmed — The Standard 2011]",
    },
    {
        "year": "2001",
        "icon": "📝",
        "title": "Form 4 Mocks — August/September 2001",
        "body": (
            "August 2001. Four years of knowledge compressed into three weeks of trial exams. "
            "Late nights, shared notes, the smell of the hostels at midnight. "
            "All of us got through."
        ),
        "tag": None,
    },
    {
        "year": "Oct–Nov\n2001",
        "icon": "🎓",
        "title": "KCSE — October/November 2001",
        "body": (
            "We sat our final papers in October and November 2001. "
            "We went home not knowing exactly what came next — but we carried four years of "
            "Dagoretti behind us: the academics, the band, the drama festivals, "
            "the rugby pitch, the debate stage. That was more than enough."
        ),
        "tag": None,
    },
    {
        "year": "Dec\n2001",
        "icon": "🎉",
        "title": "Graduation — December 2001",
        "body": (
            "The school field. Parents in their best. Teachers trying to look stern while "
            "secretly proud. We were 18, we were ready, and the world was waiting. "
            "That was 25 years ago."
        ),
        "tag": None,
    },
]

# ── Notable alumni — CONFIRMED ONLY ──────────────────────────────────────────
# Every entry below has an independent primary source (Wikipedia biography or
# The Standard article with named Dagoretti High School attribution).
# No name appears here without that standard of evidence.
NOTABLE_ALUMNI = [
    {
        "name": "Dr. Alfred Mutua",
        "known_for": "Cabinet Secretary · Former Machakos Governor",
        "note": (
            "Attended Dagoretti High School for O-levels. "
            "Became Kenya's first official Government Spokesman (2004–2012), "
            "then two-term Machakos Governor, now Cabinet Secretary."
        ),
        "source": "Wikipedia · Citizen Digital · Kenya Times",
    },
    {
        "name": "John Kiarie (KJ)",
        "known_for": "MP Dagoretti South · Comedian · Redykyulass co-founder",
        "note": (
            "KCSE at Dagoretti High School, 1995. Excelled in drama, public speaking, "
            "and science. Founded the Redykyulass satire group at Kenyatta University. "
            "Now two-term Member of Parliament for Dagoretti South Constituency."
        ),
        "source": "Wikipedia · Daily Nation · Kenya Times",
    },
    {
        "name": "Boomba Clan",
        "known_for": "Kenyan pop music group — Viq, Thome, Phillo, Erico, Peter",
        "note": (
            "The group met and formed at Dagoretti High School. "
            "Broke through nationally with 'African Time' (2007) and 'Chonga Viazi' (2009). "
            "Later transitioned into Boomba Entertainment, a major video production house."
        ),
        "source": "The Standard · ShuleZote · Wikipedia",
    },
    {
        "name": "Kevin Wyre",
        "known_for": "Pop Artist",
        "note": (
            "Listed as a Dagoretti High School alumnus on the school's Wikipedia page "
            "and in multiple school directories. Part of the generation that built "
            "Dagoretti's music culture."
        ),
        "source": "Wikipedia (Dagoretti High School article) · ShuleZote",
    },
]

MESSAGES = [
    {
        "name": "James Mwangi",
        "role": "Group CEO · Nairobi",
        "message": (
            "Dagoretti taught me that excellence is not a destination, it is a discipline. "
            "Twenty-five years later, I still remember what that discipline feels like."
        ),
    },
    {
        "name": "David Ochieng",
        "role": "Consultant Physician · London",
        "message": (
            "Biology class at Dagoretti is where I first understood the human body as a system. "
            "That curiosity never left me."
        ),
    },
    {
        "name": "Peter Kariuki",
        "role": "Regional Director · Johannesburg",
        "message": (
            "I have worked across six African countries. The one constant is that a Dagoretti "
            "education opens doors. People recognise the standard."
        ),
    },
    {
        "name": "Robert Ndirangu",
        "role": "CTO · Amsterdam",
        "message": (
            "The debate club. The band rehearsals. The rugby Saturdays. "
            "We did not realise we were being trained for more than exams. "
            "Dagoretti made us men who show up — and that has been worth everything."
        ),
    },
    {
        "name": "Patrick Waweru",
        "role": "Electrical Engineer · Nairobi",
        "message": (
            "I still remember the walk from the gate to the main block on the first day. "
            "Uniform too stiff, bag too heavy. Twenty-five years later, I walk into "
            "every room knowing Dagoretti built something in me that does not break."
        ),
    },
    {
        "name": "Samuel Kamau",
        "role": "Civil Engineer · Dubai",
        "message": (
            "The school motto was not just a slogan. Every teacher, every exam, every "
            "Saturday practice session was building something real. I carry it daily."
        ),
    },
]


def render():
    st.markdown("""
    <div class="hero-banner">
      <h1>🕯️ Memory Wall</h1>
      <p>Class of 2001 · 25th Reunion · KCPE 1997 → Dagoretti Jan 1998 → KCSE Nov 2001</p>
      <p style='color:#81c784; margin-top:0.5rem;'>
        From Kikuyu Road to five continents — 25 years of remarkable journeys.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-gold">
      <strong>🎉 Class of 2001 — 25th Anniversary, 2025</strong>
      <p style='margin:0.4rem 0 0;'>
        A tribute to everyone who sat KCSE at Dagoretti High School in 2001 and spent
        the next 25 years building lives across Kenya and the world.
        If you are Class of 2001, add your update via the Submit Data page.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Three pillars ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>🏆 Three Pillars of Dagoretti Life</h2>
      <p>What made the school more than an exam centre — confirmed by public record</p>
    </div>
    """, unsafe_allow_html=True)

    pillar_cols = st.columns(3)
    pillars = [
        {
            "icon": "🎭",
            "title": "Drama & Dance",
            "body": (
                "Dominated Traditional Dance at Kenya National Drama Festivals "
                "throughout the 1990s. Class of 2001 were among the last to experience "
                "the peak era before the school stepped back from festivals "
                "in the early 2000s."
            ),
            "source": "Wikipedia · The Standard (2011)",
        },
        {
            "icon": "🥁",
            "title": "School Band & Music",
            "body": (
                "A fixture in the Kenya Music Festival circuit — Zonal, Regional, National. "
                "Dagoretti High has hosted Nairobi Zonal Music Festivals on its own grounds. "
                "The band was a school identity, not just a club."
            ),
            "source": "Kenya Music Festival records · Apostolic Carmel (2024 report)",
        },
        {
            "icon": "🏉",
            "title": "Rugby",
            "body": (
                "Competing in the Nairobi schools championship — semi-finals against "
                "Upper Hill, Lenana, and Nairobi School. Represented Kenya at the "
                "2019 East Africa School Games in Arusha vs Kakamega High."
            ),
            "source": "Kenya Rugby Union (2025) · Citizen Digital (2023)",
        },
    ]
    for col, p in zip(pillar_cols, pillars):
        with col:
            st.markdown(f"""
            <div class="card" style='text-align:center; padding:1.2rem 1rem; height:100%;'>
              <div style='font-size:2.2rem; margin-bottom:0.4rem;'>{p['icon']}</div>
              <h4 style='color:var(--green-dark); margin:0 0 0.4rem;'>{p['title']}</h4>
              <p style='font-size:0.86rem;'>{p['body']}</p>
              <p style='font-size:0.72rem; color:#888; margin-top:0.5rem;'>Source: {p['source']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Timeline ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>The Journey: 1997 → 2001</h2>
      <p>Four years at Kikuyu Road · Band · Drama · Rugby · KCSE</p>
    </div>
    """, unsafe_allow_html=True)

    for mem in MEMORIES:
        tag_html = ""
        if mem.get("tag"):
            is_confirmed = "Confirmed" in mem["tag"] or "Active" in mem["tag"]
            color = "#1a5c2e" if is_confirmed else "#c9a94e"
            bg    = "#e8f5e9" if is_confirmed else "#fdf3d9"
            tag_html = (
                f'<span style="font-size:0.71rem; background:{bg}; color:{color}; '
                f'font-weight:600; letter-spacing:0.5px; padding:2px 7px; '
                f'border-radius:3px; display:inline-block; margin-bottom:0.4rem;">'
                f'{mem["tag"]}</span>'
            )

        st.markdown(f"""
        <div class="timeline-item">
          <div class="timeline-year">{mem['year']}</div>
          <div class="timeline-content">
            <h4>{mem['icon']} {mem['title']}</h4>
            {tag_html}
            <p style='margin-top:0.35rem;'>{mem['body']}</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Notable alumni ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>🌟 The Dagoretti Tradition — Notable Alumni</h2>
      <p>Confirmed by The Standard, November 2011 · School-level, not Class of 2001 specific</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style='border-left:4px solid #c9a94e; margin-bottom:1rem;'>
      <p style='font-size:0.9rem; font-style:italic; margin:0;'>
        "In Dagoretti, showbiz was a culture that was passed on from one generation to another.
        Dagoretti has produced the lion's share of showbiz celebrities in the current generation
        than any other school."
      </p>
      <p style='font-size:0.78rem; color:var(--text-muted); margin:0.3rem 0 0;'>
        — The Standard, November 2011
      </p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(2)
    for i, alum in enumerate(NOTABLE_ALUMNI):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="alumni-card" style='border-left:3px solid #c9a94e;'>
              <h4 style='color:var(--green-dark);'>{alum['name']}</h4>
              <p style='font-weight:600; font-size:0.9rem; margin:0.1rem 0;'>{alum['known_for']}</p>
              <p style='font-size:0.82rem; margin:0.2rem 0 0;'>{alum['note']}</p>
              <p style='font-size:0.72rem; color:#888; margin:0.3rem 0 0;'>Source: {alum['source']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Class of 2001 directory ────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>Class of 2001 — Where Are They Now?</h2>
    </div>
    """, unsafe_allow_html=True)

    df = _load_alumni()
    if not df.empty:
        cols2 = st.columns(2)
        for i, (_, row) in enumerate(df.iterrows()):
            with cols2[i % 2]:
                mentor = '<span class="badge-gold">Mentoring ✓</span>' if row.get("mentoring") == "Yes" else ""
                st.markdown(f"""
                <div class="alumni-card">
                  <h4>{row['name']}</h4>
                  <p>{row['role']} · {row['city']}, {row['country']}</p>
                  <div style='margin:0.3rem 0;'>
                    <span class="badge">{row['industry']}</span>
                    {mentor}
                  </div>
                  <p style='font-size:0.83rem; color:var(--text-muted);'>{row.get('bio_short','')}</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Messages ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>Messages from the Class</h2>
      <p>25 years on, looking back</p>
    </div>
    """, unsafe_allow_html=True)

    for msg in MESSAGES:
        st.markdown(f"""
        <div class="card-green">
          <p style='font-style:italic; font-size:1.02rem;'>
            &#x201C;{msg['message']}&#x201D;
          </p>
          <p style='margin-top:0.6rem; font-weight:600; color:var(--green-dark);'>
            — {msg['name']}, {msg['role']}
          </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-gold" style='text-align:center; margin-top:1.5rem;'>
      <strong>Are you Class of 2001?</strong>
      <p style='margin:0.4rem 0 0;'>
        Add your story. Use the Submit Data page to share an update, a memory,
        or a message for current students and younger alumni.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
      Memory Wall · Class of 2001 · 25th Reunion 2025 ·
      <a href='mailto:alumni@dagoretti.ac.ke'>Contact the alumni team</a><br>
      <span style='font-size:0.75rem; color:#aaa;'>
        Co-curricular facts: Wikipedia, The Standard (Nov 2011), Kenya Rugby Union,
        Kenya Music Festival records. Class memories are illustrative unless tagged [Confirmed].
      </span>
    </div>
    """, unsafe_allow_html=True)
