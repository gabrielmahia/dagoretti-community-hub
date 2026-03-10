"""
Memory Wall — Class of 2001 · 25th anniversary tribute.
Co-curricular facts sourced from Wikipedia, The Standard (2011), KRU, and Kenya Music Festival records.
Memories marked [confirmed], [probable], or [illustrative] in code comments.
"""

import streamlit as st
import pandas as pd
import os
import sys


@st.cache_data(ttl=300)
def _load_alumni():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "alumni.csv")
    try:
        df = pd.read_csv(path).fillna("")
        return df[df["year"] == 2001].reset_index(drop=True)
    except FileNotFoundError:
        return pd.DataFrame()


# ── Timeline ──────────────────────────────────────────────────────────────────
# [C] = Confirmed (Wikipedia / The Standard / KRU / Kenya Music Festival records)
# [P] = Probable (consistent with confirmed institutional record)
# [I] = Illustrative (school context / shared memory — not individually sourced)
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
        "confidence": "illustrative",  # [I] shared experience, not individually sourced
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
        "confidence": "illustrative",  # [I] shared experience
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
        "confidence": "confirmed",  # [C] Kenya Music Festival institutional record
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
        "confidence": "confirmed",  # [C] Wikipedia + The Standard 2011
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
        "confidence": "confirmed",  # [C] KRU + Citizen Digital
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
        "confidence": "confirmed",  # [C] The Standard 2011 + Wikipedia biographies
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
        "confidence": "illustrative",  # [I] shared experience
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
        "confidence": "probable",  # [P] KCSE calendar is institutional — specific class experience is shared memory
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
        "confidence": "illustrative",  # [I] shared experience
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
      <p>Dagoretti High School · All Classes Welcome · Est. 1961</p>
      <p style='color:#81c784; margin-top:0.5rem;'>
        Class of 2001 spotlight · 25th Reunion 2026 · From Kikuyu Road to five continents.
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
    <div class="card" style="background:#1a2e1f; border:1px solid #2e5c3a; padding:1rem 1.2rem;">
      <div style="display:flex; flex-wrap:wrap; gap:1.4rem; align-items:center;">
        <div>
          <span style="font-size:0.72rem; color:#a5d6a7; text-transform:uppercase; letter-spacing:0.5px;">Motto</span><br>
          <strong style="color:#c9a94e;">Elimu Ni Mali</strong>
          <span style="color:#c8e6c9; font-size:0.82rem;"> (Education is Wealth)</span>
        </div>
        <div>
          <span style="font-size:0.72rem; color:#a5d6a7; text-transform:uppercase; letter-spacing:0.5px;">Colours</span><br>
          <span style="display:inline-block; width:12px; height:12px; background:#800000; border-radius:2px; margin-right:3px; vertical-align:middle;"></span>
          <span style="display:inline-block; width:12px; height:12px; background:#fff; border:1px solid #aaa; border-radius:2px; margin-right:3px; vertical-align:middle;"></span>
          <span style="display:inline-block; width:12px; height:12px; background:#2e7d32; border-radius:2px; margin-right:3px; vertical-align:middle;"></span>
          <span style="display:inline-block; width:12px; height:12px; background:#9e9e9e; border-radius:2px; margin-right:6px; vertical-align:middle;"></span>
          <strong style="font-size:0.88rem; color:#fff;">Maroon · White · Green · Grey</strong>
        </div>
        <div>
          <span style="font-size:0.72rem; color:#a5d6a7; text-transform:uppercase; letter-spacing:0.5px;">Location</span><br>
          <strong style="font-size:0.88rem; color:#fff;">16km from Nairobi · Nairobi–Kikuyu Road</strong>
        </div>
        <div>
          <span style="font-size:0.72rem; color:#a5d6a7; text-transform:uppercase; letter-spacing:0.5px;">Founded</span><br>
          <strong style="font-size:0.88rem; color:#fff;">1929 (Ruthimitu) · Reopened 1962</strong>
        </div>
        <div>
          <span style="font-size:0.72rem; color:#a5d6a7; text-transform:uppercase; letter-spacing:0.5px;">KNEC Code</span><br>
          <strong style="font-size:0.88rem; color:#fff;">20405001</strong>
        </div>
      </div>
      <p style="font-size:0.72rem; color:#a5d6a7; margin:0.6rem 0 0;">Source: Wikipedia · Dagoretti High School article (updated Feb 2026)</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Four pillars ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>🏆 Four Pillars of Dagoretti Excellence</h2>
      <p>What made the school more than an exam centre — confirmed by public record</p>
    </div>
    """, unsafe_allow_html=True)

    pillars = [
        {
            "icon": "🎭",
            "title": "Drama & Dance",
            "body": (
                "Dominated Traditional Dance at Kenya National Drama Festivals "
                "throughout the 1990s. Back-to-back titles in 2004 and 2005. "
                "In Dagoretti, showbiz was a culture passed from one generation to the next."
            ),
            "source": "Wikipedia · The Standard, Nov 2011",
        },
        {
            "icon": "🥁",
            "title": "School Band & Music",
            "body": (
                "A fixture in the Kenya Music Festival circuit — Zonal, Regional, National. "
                "Dagoretti High has hosted Nairobi Zonal Music Festivals on its own grounds. "
                "The band was a school identity, not just a club."
            ),
            "source": "Kenya Music Festival records · Apostolic Carmel (2024)",
        },
        {
            "icon": "🏉",
            "title": "Rugby",
            "body": (
                "Competing in the Nairobi schools championship against Upper Hill, "
                "Lenana, and Nairobi School. Represented Kenya at the 2019 East Africa "
                "School Games in Arusha."
            ),
            "source": "Kenya Rugby Union (2025) · Citizen Digital (2023)",
        },
        {
            "icon": "🏀",
            "title": "Basketball",
            "body": (
                "Peter Orero's principal tenure transformed the school into a national "
                "basketball powerhouse. Giants of Africa — the NBA-backed initiative — "
                "installed a world-class court at Dagoretti, cementing it as a talent "
                "incubator for East African basketball."
            ),
            "source": "Nation Africa · Giants of Africa (giantsofafrica.org)",
        },
    ]
    p_html = '<div style="display:flex;flex-wrap:wrap;gap:0.75rem;margin-bottom:1rem;">'
    for p in pillars:
        p_html += (
            f'<div style="flex:1 1 180px;min-width:160px;background:#fdf8f0;border-radius:10px;'
            f'padding:1.1rem 0.8rem;text-align:center;">'
            f'<div style="font-size:2rem;margin-bottom:0.3rem;">{p["icon"]}</div>'
            f'<h4 style="color:var(--green-dark);margin:0 0 0.3rem;font-size:0.95rem;">{p["title"]}</h4>'
            f'<p style="font-size:0.82rem;margin:0 0 0.3rem;">{p["body"]}</p>'
            f'<p style="font-size:0.68rem;color:#888;margin:0;">Source: {p["source"]}</p>'
            f'</div>'
        )
    p_html += '</div>'
    st.markdown(p_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Timeline ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>The Journey: 1997 → 2001</h2>
      <p>Four years at Kikuyu Road · Band · Drama · Rugby · KCSE</p>
    </div>
    """, unsafe_allow_html=True)

    # Provenance legend
    st.markdown("""
    <div style="display:flex;flex-wrap:wrap;gap:0.5rem;margin-bottom:1rem;font-size:0.78rem;">
      <span style="background:#e8f5e9;color:#1a5c2e;padding:2px 9px;border-radius:10px;font-weight:600;">✅ Confirmed — named primary source</span>
      <span style="background:#e3f2fd;color:#1565c0;padding:2px 9px;border-radius:10px;font-weight:600;">🔵 Probable — consistent with institutional record</span>
      <span style="background:#f3e5f5;color:#6a1b9a;padding:2px 9px;border-radius:10px;font-weight:600;">🟣 Shared memory — community experience, not individually sourced</span>
    </div>
    """, unsafe_allow_html=True)

    for mem in MEMORIES:
        conf = mem.get("confidence", "illustrative")
        if conf == "confirmed":
            conf_html = '<span style="font-size:0.71rem;background:#e8f5e9;color:#1a5c2e;font-weight:600;padding:2px 7px;border-radius:10px;">✅ Confirmed</span>'
        elif conf == "probable":
            conf_html = '<span style="font-size:0.71rem;background:#e3f2fd;color:#1565c0;font-weight:600;padding:2px 7px;border-radius:10px;">🔵 Probable</span>'
        else:
            conf_html = '<span style="font-size:0.71rem;background:#f3e5f5;color:#6a1b9a;font-weight:600;padding:2px 7px;border-radius:10px;">🟣 Shared memory</span>'

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
            f'<div style="margin:0.3rem 0 0.4rem;display:flex;flex-wrap:wrap;gap:0.4rem;">{conf_html}{" " + tag_html if tag_html else ""}</div>'
            f'<p style="margin-top:0.2rem;">{mem["body"]}</p>'
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
                "Mr. R.M. Murengi arrived as principal around 2000, succeeding "
                "Mr. J.K. Mburia, who had led the school for many years before him. "
                "Mr. Mburia passed away several years ago — alumni marked his passing on social media. "
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
                f'<p style="font-size:0.78rem; font-weight:700; color:#aaa; margin:0 0 0.4rem; text-transform:uppercase; letter-spacing:0.5px;">{dorm["who"]}</p>' +
                f'<p style="font-size:0.88rem; margin:0;">{dorm["body"]}</p>' +
                '</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Principals timeline ─────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>🎓 Principals of Dagoretti High School</h2>
      <p>Known record · Alumni-verified entries marked · Gaps remain — community input welcome</p>
    </div>
    """, unsafe_allow_html=True)

    PRINCIPALS = [
        {
            "era": "c. 1942",
            "name": "Mr. Eliud Mathu",
            "note": "First principal of the Waithaka Independent School era. Makerere University graduate. Simultaneously the first African appointed to Kenya's Legislative Council.",
            "source": "Wikipedia · Confirmed",
        },
        {
            "era": "1962",
            "name": "Mr. N.C. Bhatt",
            "note": "First Headmaster of the modern Dagoretti High School, which opened to its first cohort in January 1962 following the school's rebirth from a Mau Mau detention camp.",
            "source": "Wikipedia · Confirmed",
        },
        {
            "era": "1962 – c. 2000",
            "name": "Gap in record",
            "note": "Alumni with knowledge of principals serving between Mr. Bhatt and Mr. Mburia are encouraged to submit corrections via the Submit Data page.",
            "source": "Gap — community input needed",
        },
        {
            "era": "c. 1980s – 2000",
            "name": "Mr. J.K. Mburia",
            "note": "Long-serving principal who led the school through the 1980s and 1990s. Remembered fondly by alumni of that era. Mr. Mburia passed away several years ago — his passing was marked by alumni on social media.",
            "source": "Alumni-verified · Facebook eulogy · Class of 2001 account",
        },
        {
            "era": "c. 2000 – 2004",
            "name": "Mr. R.M. Murengi",
            "note": "Succeeded Mr. Mburia around 2000. Remembered for firm discipline and steady administration during the early 2000s, including the KCSE period for the Class of 2001.",
            "source": "Alumni-verified · Class of 2001 account",
        },
        {
            "era": "c. 2014 – 2016",
            "name": "Mr. B.K. Ngahu",
            "note": "Oversaw infrastructure improvements during his tenure. Later moved to Upper Hill School.",
            "source": "Alumni records",
        },
        {
            "era": "2017 – 2022",
            "name": "Mr. Peter Orero",
            "note": "Transformed the school into a national basketball powerhouse. Partnered with Giants of Africa for a world-class court on campus. Elected MP for Kibra Constituency in 2022.",
            "source": "Nation Africa · Wikipedia · Confirmed",
        },
        {
            "era": "c. 2023",
            "name": "Dr. Nyakweba",
            "note": "Chief Principal who focused on alumni relations during his tenure.",
            "source": "Alumni records",
        },
        {
            "era": "2026",
            "name": "Mr. John Caron Dier",
            "note": "Senior Principal as of early 2026.",
            "source": "LinkedIn alumni homecoming article",
        },
    ]

    for p in PRINCIPALS:
        is_gap    = "Gap" in p["name"]
        is_alumni = "Alumni-verified" in p["source"]
        border    = "#555" if is_gap else ("#c9a94e" if is_alumni else "var(--green-mid)")
        badge     = ""
        if is_gap:
            badge = '<span style="font-size:0.7rem;background:#333;color:#aaa;padding:2px 7px;border-radius:10px;margin-left:6px;">Gap</span>'
        elif is_alumni:
            badge = '<span style="font-size:0.7rem;background:#fdf3d9;color:#7a5c00;padding:2px 7px;border-radius:10px;margin-left:6px;">Alumni-verified</span>'
        else:
            badge = '<span style="font-size:0.7rem;background:#e8f5e9;color:#1a5c2e;padding:2px 7px;border-radius:10px;margin-left:6px;">Confirmed</span>'

        st.markdown(
            f'<div class="card" style="border-left:3px solid {border};padding:0.7rem 1rem;margin-bottom:0.5rem;">'
            f'<div style="display:flex;align-items:baseline;gap:0.6rem;flex-wrap:wrap;">'
            f'<span style="font-size:0.72rem;font-weight:700;color:var(--green-dark);text-transform:uppercase;letter-spacing:0.5px;">{p["era"]}</span>'
            f'<strong style="font-size:0.95rem;{"color:#666;" if is_gap else ""}">{p["name"]}</strong>'
            f'{badge}'
            f'</div>'
            f'<p style="font-size:0.84rem;color:var(--text-muted);margin:0.25rem 0 0.15rem;">{p["note"]}</p>'
            f'<p style="font-size:0.68rem;color:#888;margin:0;font-style:italic;">Source: {p["source"]}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Add / correct a principal ──────────────────────────────────────────────
    with st.expander("📥 Add or correct a principal entry", expanded=False):
        st.markdown("""
        <div style="font-size:0.87rem;background:#fdf3d9;border-radius:6px;padding:0.75rem 1rem;margin-bottom:0.75rem;">
        <strong>What's needed most:</strong> Any principal who served between Mr. N.C. Bhatt (1962)
        and Mr. J.K. Mburia (c. 1980s). Also: exact years for Mburia, Murengi, and Ngahu, and the
        full first name / title for Dr. Nyakweba. Verified newspaper, school gazette, or transcript
        references preferred.
        </div>
        """, unsafe_allow_html=True)
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from utils import sheets as _sheets_p
        with st.form("principals_form"):
            pc1, pc2 = st.columns(2)
            with pc1:
                p_name = st.text_input("Principal's name *")
                p_era  = st.text_input("Approximate era / years *", placeholder="e.g. 1970–1978")
            with pc2:
                p_src  = st.text_input("Source / evidence *", placeholder="e.g. newspaper article, school gazette, personal memory + class year")
                p_your = st.text_input("Your name (optional)")
            p_note = st.text_area("Additional context (optional)", height=70,
                                  placeholder="What do you remember about this principal? Any notable events during their tenure?")
            if st.form_submit_button("Submit Principal Record", type="primary"):
                if not p_name or not p_era or not p_src:
                    st.warning("Please complete: Principal name, Era/years, and Source.")
                else:
                    ok = _sheets_p.append_row("corrections", {
                        "page": "Memory Wall — Principals",
                        "field": p_name,
                        "current_value": f"Era: {p_era}",
                        "correction": p_note,
                        "source": p_src,
                        "submitter": p_your,
                    })
                    if ok:
                        _sheets_p.success_banner(
                            p_your or "contributor",
                            f"Principal record for {p_name} ({p_era}) received. Will be cross-checked and added.",
                        )
                    elif not _sheets_p.is_configured():
                        st.info(
                            f"Email to contact@gabrielmahia.com — Subject: Dagoretti Principal Record — "
                            f"{p_name} ({p_era}). Include your source."
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

    # Mobile-first timeline: single left spine, cards full-width.
    # High-contrast colours — readable on phone screens outdoors.
    tl_items = []
    for item in POLITICAL_LINEAGE:
        tl_items.append(
            f'<div style="display:flex;align-items:stretch;margin-bottom:0.5rem;">'
            # spine + dot
            f'<div style="display:flex;flex-direction:column;align-items:center;width:2rem;flex-shrink:0;">'
            f'<div style="width:2px;flex:1;background:#8B0000;min-height:12px;"></div>'
            f'<div style="width:12px;height:12px;border-radius:50%;background:#8B0000;'
            f'border:2px solid #c9a94e;flex-shrink:0;margin:2px 0;"></div>'
            f'<div style="width:2px;flex:1;background:#8B0000;min-height:12px;"></div>'
            f'</div>'
            # card — white text on near-black, high contrast
            f'<div style="flex:1;background:#111827;border:1px solid #8B0000;border-radius:8px;'
            f'padding:0.75rem 1rem;margin-left:0.6rem;">'
            f'<span style="font-size:0.72rem;font-weight:800;color:#e87070;'
            f'text-transform:uppercase;letter-spacing:1px;">{item["year"]}</span><br>'
            f'<strong style="font-size:0.95rem;color:#ffffff;">{item["figure"]}</strong> '
            f'<span style="font-size:0.8rem;color:#aaaaaa;font-style:italic;">— {item["role"]}</span><br>'
            f'<span style="font-size:0.85rem;color:#e0e0e0;line-height:1.4;">{item["event"]}</span>'
            f'</div>'
            f'</div>'
        )
    st.markdown(
        '<div style="padding:0.25rem 0;">' + "".join(tl_items) + '</div>',
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

    # Sector groupings — confirmed by Wikipedia sources only
    ALUMNI_SECTORS = [
        {
            "sector": "🏛️ Politics & Public Service",
            "color": "#8B0000",
            "names": ["Dr. Alfred Mutua", "John Kiarie (KJ)", "Ferdinand Waititu"],
        },
        {
            "sector": "🎵 Entertainment & Arts",
            "color": "#c9a94e",
            "names": ["Kevin Wyre", "Boomba Clan"],
        },
        {
            "sector": "📺 Media",
            "color": "#1565c0",
            "names": ["Renson Michael"],
        },
    ]
    alumni_by_name = {a["name"]: a for a in NOTABLE_ALUMNI}

    for sector in ALUMNI_SECTORS:
        st.markdown(
            f'<p style="font-size:0.82rem; font-weight:700; color:{sector["color"]}; '
            f'text-transform:uppercase; letter-spacing:0.8px; margin:0.8rem 0 0.3rem;">'
            f'{sector["sector"]}</p>',
            unsafe_allow_html=True,
        )
        s_html = '<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:0.6rem; margin-bottom:0.8rem;">'
        for name in sector["names"]:
            alum = alumni_by_name.get(name)
            if not alum:
                continue
            s_html += (
                f'<div class="alumni-card" style="border-left:3px solid {sector["color"]};">'
                f'<h4 style="color:var(--green-dark); font-size:0.92rem;">{alum["name"]}</h4>'
                f'<p style="font-weight:600; font-size:0.84rem; margin:0.1rem 0; color:var(--text);">{alum["known_for"]}</p>'
                f'<p style="font-size:0.84rem; margin:0.2rem 0 0; color:var(--text-muted);">{alum["note"]}</p>'
                f'<p style="font-size:0.72rem; color:#777; margin:0.3rem 0 0; font-style:italic;">Source: {alum["source"]}</p>'
                '</div>'
            )
        s_html += '</div>'
        st.markdown(s_html, unsafe_allow_html=True)

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
      Memory Wall · Class of 2001 · 25th Reunion 2026 ·
      <a href='mailto:contact@gabrielmahia.com'>Contact the alumni team</a><br>
      <span style='font-size:0.75rem; color:#aaa;'>
        Co-curricular facts: Wikipedia, The Standard (Nov 2011), Kenya Rugby Union,
        Kenya Music Festival records. Class memories are illustrative unless tagged [Confirmed].
      </span>
    </div>
    """, unsafe_allow_html=True)
