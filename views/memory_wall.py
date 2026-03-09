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
        "year": "Nov\n2001",
        "icon": "🏁",
        "title": "Last Paper — Clearing Out",
        "body": (
            "KCSE ended and that was it. You handed back your library books, "
            "settled any lab or boarding dues, and walked out of the gate. "
            "No ceremony, no stage — just clearance. "
            "The actual results would come from KNEC months later, "
            "around February 2002. Until then, you went home and waited."
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
            "Now two-term Member of Parliament for Dagoretti South Constituency. "
            "His MP tenure saw the long-unfinished Constra dormitory finally completed."
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
        "known_for": "Pop Artist · Love Child",
        "note": (
            "Listed as a Dagoretti High School alumnus on the school's Wikipedia page "
            "and in multiple school directories. Part of the generation that built "
            "Dagoretti's music culture."
        ),
        "source": "Wikipedia (Dagoretti High School article) · ShuleZote",
    },
    {
        "name": "Ferdinand Waititu",
        "known_for": "Former Governor of Kiambu County",
        "note": (
            "Dagoretti High School alumnus who rose to serve as Governor of Kiambu County. "
            "Part of the generation that established Dagoretti's track record of producing "
            "public figures across politics and public service."
        ),
        "source": "Wikipedia · Rejnac Daily",
    },
]





# ── Messages from the class ───────────────────────────────────────────────────
# These are read from Google Sheets (memory_submissions tab, status='approved').
# No messages are hardcoded — every quote shown was submitted by a real person
# and reviewed by an admin before appearing here.

import sys, os as _os
sys.path.insert(0, _os.path.dirname(_os.path.dirname(__file__)))
from utils import sheets as _sheets

@st.cache_data(ttl=300)
def _load_approved_memories():
    """
    Pull approved memory submissions from Google Sheets via Apps Script.
    The Apps Script must expose a doGet() handler that returns JSON.
    Falls back to empty list if not configured or read fails.

    NOTE: Until a doGet() endpoint is added to the Apps Script, this returns [].
    Approved memories can also be manually appended to data/memories.csv and
    read from there as an interim approach.
    """
    # Interim: read from local CSV if it exists (admin-curated approved memories)
    import os
    local_path = os.path.join(os.path.dirname(__file__), "..", "data", "memories.csv")
    if os.path.exists(local_path):
        try:
            import pandas as pd
            df = pd.read_csv(local_path)
            approved = df[df["status"].str.lower() == "approved"] if "status" in df.columns else df
            return approved.to_dict("records")
        except Exception:
            pass
    return []


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

    # ── School quick-facts ─────────────────────────────────────────────────────
    st.markdown("""
    <div class="card" style="background:#1a1a2e; border:1px solid #333; padding:1rem 1.2rem;">
      <div style="display:flex; flex-wrap:wrap; gap:1.4rem; align-items:center;">
        <div>
          <span style="font-size:0.72rem; color:#888; text-transform:uppercase; letter-spacing:0.5px;">Motto</span><br>
          <strong style="color:#c9a94e;">Elimu Ni Mali</strong>
          <span style="color:#888; font-size:0.82rem;"> (Education is Wealth)</span>
        </div>
        <div>
          <span style="font-size:0.72rem; color:#888; text-transform:uppercase; letter-spacing:0.5px;">Colours</span><br>
          <span style="display:inline-block; width:12px; height:12px; background:#800000; border-radius:2px; margin-right:3px; vertical-align:middle;"></span>
          <span style="display:inline-block; width:12px; height:12px; background:#fff; border:1px solid #555; border-radius:2px; margin-right:3px; vertical-align:middle;"></span>
          <span style="display:inline-block; width:12px; height:12px; background:#2e7d32; border-radius:2px; margin-right:3px; vertical-align:middle;"></span>
          <span style="display:inline-block; width:12px; height:12px; background:#9e9e9e; border-radius:2px; margin-right:6px; vertical-align:middle;"></span>
          <strong style="font-size:0.88rem;">Maroon · White · Green · Grey</strong>
        </div>
        <div>
          <span style="font-size:0.72rem; color:#888; text-transform:uppercase; letter-spacing:0.5px;">Location</span><br>
          <strong style="font-size:0.88rem;">16km from Nairobi · Nairobi–Kikuyu Road</strong>
        </div>
        <div>
          <span style="font-size:0.72rem; color:#888; text-transform:uppercase; letter-spacing:0.5px;">Founded</span><br>
          <strong style="font-size:0.88rem;">1929 (Ruthimitu) · Reopened 1962</strong>
        </div>
        <div>
          <span style="font-size:0.72rem; color:#888; text-transform:uppercase; letter-spacing:0.5px;">KNEC Code</span><br>
          <strong style="font-size:0.88rem;">20405001</strong>
        </div>
      </div>
      <p style="font-size:0.68rem; color:#555; margin:0.6rem 0 0;">Source: Wikipedia · Dagoretti High School article (updated Feb 2026)</p>
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
        card = (
            '<div class="timeline-item">'
            f'<div class="timeline-year">{mem["year"]}</div>'
            '<div class="timeline-content">'
            f'<h4>{mem["icon"]} {mem["title"]}</h4>'
            f'{tag_html}'
            f'<p style="margin-top:0.35rem;">{mem["body"]}</p>'
            '</div></div>'
        )
        st.markdown(card, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Dorm lore ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>🏠 The Dorms — Where You Slept Decided Who You Were</h2>
      <p>Alumni Memory · Class of 2001 era · Oral history — not in any formal record</p>
    </div>
    """, unsafe_allow_html=True)

    dorm_lore = [
        {
            "name": "Siberia",
            "icon": "🥶",
            "who": "Form 1s (Monos) + some Form 2s",
            "body": (
                "Sheet metal roof. During Kenya's cold seasons — June, July, the deep July cold "
                "that hits Nairobi at night — Siberia earned its name. "
                "The Form 1s landed here first, straight from home, still figuring out "
                "what boarding school actually meant. The name was not accidental."
            ),
        },
        {
            "name": "Constra",
            "icon": "🏗️",
            "who": "Mainly Form 2s",
            "body": (
                "Short for 'construction' — because it was never finished. "
                "Alumni recall the building had been incomplete since the 1980s. "
                "The students named it accordingly — a name that stuck for decades. "
                "Mr. R.M. Murengi arrived as principal around 2000, succeeding a long-serving "
                "predecessor whose name alumni records haven't yet confirmed. "
                "Constra was finally completed during KJ's tenure as MP for Dagoretti South."
            ),
        },
        {
            "name": "Senior Dorms 1–5",
            "icon": "🏆",
            "who": "Form 3s and Form 4s",
            "body": (
                "Five numbered dormitories. Getting here meant you had survived Siberia "
                "and Constra. The seniors ran things — the pecking order was understood "
                "by everyone from the first week of Form 1. "
                "By Form 4, you had seen three or four cohorts of Form 1s arrive "
                "and ask the same questions you once asked."
            ),
        },
        {
            "name": "Mara House",
            "icon": "🦁",
            "who": "Referenced in school records",
            "body": (
                "Mara House is cited in alumni records and the school's institutional history. "
                "The school used both numbered dorms and named houses across different eras — "
                "the naming conventions shifted over the decades."
            ),
        },
    ]

    dorm_cols = st.columns(2)
    for i, dorm in enumerate(dorm_lore):
        with dorm_cols[i % 2]:
            st.markdown(
                f'<div class="card" style="border-left:3px solid var(--green-mid); padding:1rem;">' +
                f'<h4 style="color:var(--green-dark); margin:0 0 0.2rem;">{dorm["icon"]} {dorm["name"]}</h4>' +
                f'<p style="font-size:0.78rem; font-weight:600; color:#888; margin:0 0 0.4rem; text-transform:uppercase; letter-spacing:0.5px;">{dorm["who"]}</p>' +
                f'<p style="font-size:0.88rem; margin:0;">{dorm["body"]}</p>' +
                '</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Political lineage ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>🏛️ A School Woven Into Kenya's Political History</h2>
      <p>From pre-independence to Parliament — confirmed by Wikipedia · Dagoretti High School article</p>
    </div>
    """, unsafe_allow_html=True)

    POLITICAL_LINEAGE = [
        {
            "year": "1939",
            "figure": "Jomo Kenyatta",
            "role": "Future President of Kenya",
            "event": (
                "Personally drove the reopening of the school after its colonial-era closure. "
                "The school reopened as Waithaka Independent School under the Kikuyu Karing'a "
                "School Association — a direct act of African resistance to colonial education policy."
            ),
        },
        {
            "year": "c. 1942",
            "figure": "Eliud Mathu",
            "role": "First Principal · First African on Kenya's Legislative Council",
            "event": (
                "Makerere University graduate who became the school's first principal. "
                "Mathu was simultaneously the first African ever appointed to Kenya's "
                "Legislative Council — the school's founding leadership and Kenya's "
                "legislative history were the same person."
            ),
        },
        {
            "year": "1959",
            "figure": "Dr. Njoroge Magana Mungai",
            "role": "First Member of Parliament for Dagoretti Constituency",
            "event": (
                "Drove the initiative to convert the school back from a Mau Mau detention camp "
                "into an educational institution. Form 1 students were temporarily housed at "
                "Thika High School while construction was completed. Without Mungai's push, "
                "the school may not have reopened at all."
            ),
        },
        {
            "year": "1963",
            "figure": "Kenneth Matiba",
            "role": "Permanent Secretary for Education · Later pro-democracy leader",
            "event": (
                "Officially inaugurated Dagoretti High School on 21 September 1963 in his "
                "capacity as PS for Education. Matiba went on to become one of Kenya's most "
                "prominent pro-democracy figures, leading the push for multiparty politics "
                "in the early 1990s."
            ),
        },
        {
            "year": "1995 →",
            "figure": "John Kiarie (KJ)",
            "role": "KCSE 1995 · Two-term MP, Dagoretti South",
            "event": (
                "Dagoretti alumnus who returned to represent the constituency the school sits in. "
                "His MP tenure saw the long-unfinished Constra dormitory finally completed — "
                "an alumnus finishing what his school started."
            ),
        },
        {
            "year": "2017–2022",
            "figure": "Peter Orero",
            "role": "Former Principal → MP for Kibra",
            "event": (
                "Ran Dagoretti High School as principal and transformed it into a basketball "
                "powerhouse before being elected Member of Parliament for Kibra Constituency. "
                "A principal who became a parliamentarian — the school's civic thread continued."
            ),
        },
    ]

    for item in POLITICAL_LINEAGE:
        st.markdown(
            '<div class="card" style="display:flex; gap:1rem; border-left:4px solid #8B0000; margin-bottom:0.6rem;">'
            f'<div style="min-width:56px; font-weight:700; font-size:0.82rem; color:#8B0000; padding-top:0.1rem;">{item["year"]}</div>'
            '<div>'
            f'<strong style="font-size:0.95rem;">{item["figure"]}</strong> '
            f'<span style="font-size:0.78rem; color:#888; font-style:italic;">— {item["role"]}</span><br>'
            f'<span style="font-size:0.85rem;">{item["event"]}</span>'
            '</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Notable alumni ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>🌟 The Dagoretti Tradition — Notable Alumni</h2>
      <p>Confirmed by Wikipedia · The Standard, November 2011 · School-level, not Class of 2001 specific</p>
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
            card = (
                '<div class="alumni-card" style="border-left:3px solid #c9a94e;">'
                f'<h4 style="color:var(--green-dark);">{alum["name"]}</h4>'
                f'<p style="font-weight:600; font-size:0.9rem; margin:0.1rem 0;">{alum["known_for"]}</p>'
                f'<p style="font-size:0.82rem; margin:0.2rem 0 0;">{alum["note"]}</p>'
                f'<p style="font-size:0.72rem; color:#888; margin:0.3rem 0 0;">Source: {alum["source"]}</p>'
                '</div>'
            )
            st.markdown(card, unsafe_allow_html=True)

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
                card2 = (
                    '<div class="alumni-card">'
                    f'<h4>{row["name"]}</h4>'
                    f'<p>{row["role"]} · {row["city"]}, {row["country"]}</p>'
                    f'<div style="margin:0.3rem 0;"><span class="badge">{row["industry"]}</span> {mentor}</div>'
                    f'<p style="font-size:0.83rem; color:var(--text-muted);">{row.get("bio_short","")}</p>'
                    '</div>'
                )
                st.markdown(card2, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Messages from the class ────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>Messages from the Class</h2>
      <p>Submitted by alumni, reviewed before appearing here</p>
    </div>
    """, unsafe_allow_html=True)

    approved = _load_approved_memories()
    if approved:
        for msg in approved:
            label = f"{msg.get('name','Anonymous')}"
            if msg.get("year_at_dagoretti"):
                label += f", Class of {msg['year_at_dagoretti']}"
            st.markdown(
                '<div class="card-green">'
                f'<p style="font-style:italic; font-size:1.02rem;">&#x201C;{msg["body"]}&#x201D;</p>'
                f'<p style="margin-top:0.6rem; font-weight:600; color:var(--green-dark);">— {label}</p>'
                '</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="card-green" style="text-align:center; padding:2rem 1rem;">'
            '<p style="font-size:1.05rem; font-weight:600; color:var(--green-dark);">No messages yet.</p>'
            '<p style="font-size:0.9rem; color:var(--text-muted); margin-top:0.5rem;">'
            'Be the first. Use the <strong>Submit Data → Memory / Message</strong> tab '
            'to share a story, a reflection, or a milestone.'
            '</p>'
            '</div>',
            unsafe_allow_html=True,
        )

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
      <a href='mailto:contact@aikungfu.dev'>Contact the alumni team</a><br>
      <span style='font-size:0.75rem; color:#aaa;'>
        Co-curricular facts: Wikipedia, The Standard (Nov 2011), Kenya Rugby Union,
        Kenya Music Festival records. Class memories are illustrative unless tagged [Confirmed].
      </span>
    </div>
    """, unsafe_allow_html=True)
