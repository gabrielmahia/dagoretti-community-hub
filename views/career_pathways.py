"""
Career Pathways — enter KCSE subjects and grades, explore matching careers.

The CLUSTERS dict is the core data structure. Extend it to add new career paths.
Grade matching uses keyword-based subject matching — intentionally simple.
Extension: integrate actual KUCCPS cluster weights (kuccps.ac.ke).
"""

import streamlit as st
import urllib.request, json

@st.cache_data(ttl=86400)
def fetch_kenya_education_data():
    """World Bank Kenya education + labour indicators (free, no key)."""
    indicators = {
        "SE.SEC.ENRR":   "Secondary school enrolment rate (%)",
        "SE.TER.ENRR":   "Tertiary enrolment rate (%)",
        "SL.UEM.1524.ZS":"Youth unemployment rate (15-24, %)",
        "NY.GDP.PCAP.CD": "GDP per capita (USD)",
    }
    results = {}
    for code, label in indicators.items():
        try:
            url = (
                f"https://api.worldbank.org/v2/country/KE/indicator/{code}"
                f"?format=json&mrv=3&per_page=3"
            )
            with urllib.request.urlopen(url, timeout=8) as r:
                data = json.loads(r.read())
            entries = [e for e in (data[1] if len(data) > 1 else []) if e.get("value")]
            if entries:
                latest = entries[0]
                results[code] = {
                    "label": label,
                    "value": round(latest["value"], 1),
                    "year":  latest.get("date", "?"),
                    "live":  True,
                }
        except Exception:
            pass
    return results


import pandas as pd

# ── Grade hierarchy ───────────────────────────────────────────────────────────
GRADE_ORDER = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"]

# ── Career clusters ───────────────────────────────────────────────────────────
CLUSTERS = {
    "Medicine / Surgery": {
        "required": ["Biology", "Chemistry"],
        "helpful": ["Mathematics", "Physics"],
        "min_grade": "B+",
        "universities_ke": ["University of Nairobi", "Moi University", "Egerton University", "Kenyatta University"],
        "universities_abroad": ["University of Edinburgh", "Imperial College London", "University of Cape Town"],
        "salary_ke": "KSh 150,000–400,000/month",
        "salary_diaspora": "USD 8,000–20,000/month",
        "years": 6,
        "diaspora_path": "USMLE (USA), PLAB (UK), AMC (Australia) — all require additional exams after Kenyan degree.",
        "icon": "🏥",
        "description": "Diagnose and treat disease. One of the most respected and financially rewarding careers in Kenya and globally.",
    },
    "Engineering (Civil / Structural)": {
        "required": ["Mathematics", "Physics"],
        "helpful": ["Chemistry", "Geography"],
        "min_grade": "B",
        "universities_ke": ["University of Nairobi", "JKUAT", "Moi University", "Technical University of Kenya"],
        "universities_abroad": ["University of Leeds", "TU Delft", "University of Pretoria"],
        "salary_ke": "KSh 80,000–250,000/month",
        "salary_diaspora": "USD 5,000–12,000/month",
        "years": 4,
        "diaspora_path": "CEng (UK), PE (USA). Kenyan BSc recognised in most Commonwealth countries with top-up exams.",
        "icon": "🏗️",
        "description": "Design and build roads, bridges, buildings, and dams. High demand across East Africa and beyond.",
    },
    "Software Engineering / Computer Science": {
        "required": ["Mathematics"],
        "helpful": ["Physics", "Business Studies"],
        "min_grade": "B-",
        "universities_ke": ["University of Nairobi", "JKUAT", "Strathmore University", "KCA University"],
        "universities_abroad": ["MIT", "Carnegie Mellon", "University of Edinburgh", "University of Melbourne"],
        "salary_ke": "KSh 80,000–300,000/month",
        "salary_diaspora": "USD 8,000–25,000/month",
        "years": 4,
        "diaspora_path": "Tech skills transfer globally. US H1-B visa, UK Skilled Worker visa common paths. Strong remote work market.",
        "icon": "💻",
        "description": "Build the software that runs the world. Fastest-growing sector in Kenya. Strong diaspora demand.",
    },
    "Medicine (Clinical Officer)": {
        "required": ["Biology", "Chemistry"],
        "helpful": ["Mathematics"],
        "min_grade": "C+",
        "universities_ke": ["Kenya Medical Training College", "Amref Health Africa"],
        "universities_abroad": [],
        "salary_ke": "KSh 50,000–120,000/month",
        "salary_diaspora": "N/A (qualification is Kenya-specific)",
        "years": 3,
        "diaspora_path": "Clinical officer qualification is primarily Kenya-specific. Upgrade path to nursing (internationally recognised).",
        "icon": "🩺",
        "description": "Deliver frontline healthcare. Critical role in Kenya's public health system. Fast entry into health sector.",
    },
    "Law": {
        "required": ["English", "History"],
        "helpful": ["Government", "Kiswahili"],
        "min_grade": "B",
        "universities_ke": ["University of Nairobi", "Moi University", "KCA University", "Catholic University of East Africa"],
        "universities_abroad": ["University of London", "Durham University", "University of Edinburgh"],
        "salary_ke": "KSh 80,000–500,000/month",
        "salary_diaspora": "GBP 40,000–120,000/year (requires SQE in UK)",
        "years": 4,
        "diaspora_path": "UK: Solicitors Qualifying Exam (SQE). USA: LLM + Bar exam. Kenya law degree highly valued in East Africa.",
        "icon": "⚖️",
        "description": "Advocate for justice, business, and policy. Rewarding career in private practice, government, or NGOs.",
    },
    "Finance / Accounting": {
        "required": ["Mathematics", "Business Studies"],
        "helpful": ["Economics", "Accounting"],
        "min_grade": "B-",
        "universities_ke": ["University of Nairobi", "Strathmore University", "USIU-Africa", "KCA University"],
        "universities_abroad": ["London School of Economics", "University of Manchester", "University of Johannesburg"],
        "salary_ke": "KSh 60,000–250,000/month",
        "salary_diaspora": "USD 5,000–15,000/month",
        "years": 4,
        "diaspora_path": "CPA Kenya → CPA USA/ACCA (UK/Global) → internationally mobile. Strong demand in diaspora remittance and fintech.",
        "icon": "📈",
        "description": "Manage money, businesses, and economies. High demand across East Africa and in diaspora financial services.",
    },
    "Education / Teaching": {
        "required": ["English"],
        "helpful": ["Any two teaching subjects"],
        "min_grade": "C",
        "universities_ke": ["Kenyatta University", "Moi University", "Egerton University", "Maasai Mara University"],
        "universities_abroad": ["University of Bath", "University of Glasgow"],
        "salary_ke": "KSh 30,000–90,000/month",
        "salary_diaspora": "GBP 28,000–45,000/year (UK QTS required)",
        "years": 4,
        "diaspora_path": "UK: Qualified Teacher Status (QTS) route for international teachers. Strong demand in UK, Australia, Canada.",
        "icon": "📚",
        "description": "Shape the next generation. Nation-building career. Diaspora demand strong especially in UK secondary schools.",
    },
    "Agriculture / Agri-Business": {
        "required": ["Biology", "Chemistry"],
        "helpful": ["Agriculture", "Geography"],
        "min_grade": "C+",
        "universities_ke": ["Egerton University", "University of Nairobi", "Moi University", "Kenyatta University"],
        "universities_abroad": ["Wageningen University", "University of Reading", "Makerere University"],
        "salary_ke": "KSh 50,000–200,000/month",
        "salary_diaspora": "USD 4,000–10,000/month",
        "years": 4,
        "diaspora_path": "International agri-development roles with FAO, CGIAR, World Bank. MSc opens diaspora doors.",
        "icon": "🌾",
        "description": "Feed nations and build livelihoods. Critical in Kenya's economy. Exciting intersection with climate tech and fintech.",
    },
    "Journalism / Media": {
        "required": ["English", "Kiswahili"],
        "helpful": ["History", "Government"],
        "min_grade": "C+",
        "universities_ke": ["University of Nairobi", "Daystar University", "USIU-Africa"],
        "universities_abroad": ["City University London", "Cardiff University"],
        "salary_ke": "KSh 40,000–200,000/month",
        "salary_diaspora": "GBP 25,000–80,000/year",
        "years": 4,
        "diaspora_path": "Strong market for African correspondents and diaspora media. Digital skills essential.",
        "icon": "📰",
        "description": "Tell the stories that matter. From print to digital to broadcast — Kenya's media sector is growing.",
    },
    "Public Health / Nursing": {
        "required": ["Biology", "Chemistry"],
        "helpful": ["Mathematics", "Home Science"],
        "min_grade": "C+",
        "universities_ke": ["Kenya Medical Training College", "University of Nairobi", "Kenyatta University"],
        "universities_abroad": ["University of Edinburgh", "King's College London", "University of Melbourne"],
        "salary_ke": "KSh 40,000–120,000/month",
        "salary_diaspora": "GBP 28,000–50,000/year (UK OSCE exam required)",
        "years": 3,
        "diaspora_path": "Nursing highly portable. UK: OSCE exam. Australia: AHPRA registration. USA: NCLEX-RN. Strong diaspora demand.",
        "icon": "💉",
        "description": "Care for communities. One of the most globally portable healthcare qualifications.",
    },
}


def grade_meets_minimum(student_grade: str, min_grade: str) -> bool:
    """Return True if student_grade >= min_grade in KCSE hierarchy."""
    if student_grade not in GRADE_ORDER or min_grade not in GRADE_ORDER:
        return True
    return GRADE_ORDER.index(student_grade) <= GRADE_ORDER.index(min_grade)


def match_career(student_subjects: dict, cluster: dict) -> dict:
    """
    Score a career against the student's subjects and grades.
    Returns dict with 'has_required', 'has_helpful', 'meets_grade', 'score'.
    """
    req_subjects   = cluster.get("required", [])
    help_subjects  = cluster.get("helpful", [])
    min_grade      = cluster.get("min_grade", "C")

    student_subject_names = list(student_subjects.keys())

    has_required = all(
        any(req.lower() in s.lower() for s in student_subject_names)
        for req in req_subjects
    )
    has_helpful = any(
        any(h.lower() in s.lower() for s in student_subject_names)
        for h in help_subjects
    )

    # Check best grade among required subjects
    best_grade = "E"
    for subj, grade in student_subjects.items():
        for req in req_subjects:
            if req.lower() in subj.lower():
                if GRADE_ORDER.index(grade) < GRADE_ORDER.index(best_grade):
                    best_grade = grade

    meets_grade = grade_meets_minimum(best_grade, min_grade)

    score = (3 if has_required else 0) + (1 if has_helpful else 0) + (2 if meets_grade else 0)
    return {
        "has_required": has_required,
        "has_helpful": has_helpful,
        "meets_grade": meets_grade,
        "score": score,
    }


def render():
    st.markdown("""
    <div class="section-header">
      <h2>🧭 Career Pathways</h2>
      <p>Enter your subjects and grades. Explore where they lead.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-green">
      <strong>How it works:</strong> Enter up to 8 KCSE subjects and your grades (or expected grades).
      The tool matches you to careers based on required subjects and grade minimums.
      Use it for planning — for verified university cut-offs, check
      <a href="https://kuccps.ac.ke" target="_blank">KUCCPS</a>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-gold">
      <strong>⚠️ Salary ranges are indicative only.</strong>
      Figures are broad market estimates compiled from job boards and publicly reported ranges —
      they are <em>not</em> verified pay data. Actual salaries vary widely by employer, experience,
      location, and negotiation. Use them for rough career orientation only — not for financial planning.
    </div>
    """, unsafe_allow_html=True)

    # ── Subject input ─────────────────────────────────────────────────────────
    st.markdown("#### Your KCSE Subjects & Grades")

    common_subjects = [
        "Mathematics", "English", "Kiswahili", "Biology", "Chemistry",
        "Physics", "History", "Geography", "Agriculture", "Business Studies",
        "Economics", "Accounting", "Government", "Home Science",
        "Computer Studies", "Art", "Music", "Religious Education",
    ]

    student_subjects = {}
    num_subjects = st.number_input("Number of subjects to enter", min_value=1, max_value=8, value=6)

    cols = st.columns(2)
    for i in range(num_subjects):
        with cols[i % 2]:
            subj = st.selectbox(f"Subject {i+1}", common_subjects, key=f"subj_{i}",
                                index=i if i < len(common_subjects) else 0)
            grade = st.selectbox(f"Grade", GRADE_ORDER, key=f"grade_{i}", index=5)
            student_subjects[subj] = grade

    # ── Match and display ─────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### Matching Career Paths")

    results = []
    for career_name, cluster in CLUSTERS.items():
        match = match_career(student_subjects, cluster)
        results.append((career_name, cluster, match))

    results.sort(key=lambda x: x[2]["score"], reverse=True)

    filter_strong = st.checkbox("Show strong matches only (all required subjects covered)", value=False)

    for career_name, cluster, match in results:
        if filter_strong and not match["has_required"]:
            continue

        score = match["score"]
        if score >= 5:
            strength = "🟢 Strong match"
            card_class = "card-green"
        elif score >= 3:
            strength = "🟡 Possible match"
            card_class = "card"
        else:
            strength = "🔴 Stretch goal"
            card_class = "card"

        req_note = "✅ Required subjects covered" if match["has_required"] else "❌ Missing required subjects"
        grade_note = "✅ Grade threshold met" if match["meets_grade"] else f"⚠️ Grade minimum: {cluster['min_grade']}"

        universities_ke = ", ".join(cluster["universities_ke"][:3]) or "—"
        universities_ab = ", ".join(cluster["universities_abroad"][:2]) or "—"

        with st.expander(f"{cluster['icon']} {career_name}   {strength}"):
            st.markdown(f"""
            <div class="{card_class}">
              <p>{cluster['description']}</p>
              <p>{req_note} &nbsp;|&nbsp; {grade_note}</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="card">
                  <strong>📍 Kenya Universities</strong><br>
                  <span style='font-size:0.9rem;'>{universities_ke}</span><br><br>
                  <strong>🌍 International Options</strong><br>
                  <span style='font-size:0.9rem;'>{universities_ab if universities_ab != '—' else 'Kenyan degree + top-up'}</span>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="card">
                  <strong>💰 Salary Range (Kenya)</strong>
                  <span style='font-size:0.72rem;color:#888;'> — indicative estimate</span><br>
                  <span style='font-size:0.9rem;'>{cluster['salary_ke']}</span><br><br>
                  <strong>✈️ Diaspora Earning</strong>
                  <span style='font-size:0.72rem;color:#888;'> — indicative estimate</span><br>
                  <span style='font-size:0.9rem;'>{cluster['salary_diaspora']}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card-gold">
              <strong>✈️ Diaspora Pathway</strong><br>
              <span style='font-size:0.9rem;'>{cluster['diaspora_path']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
      Career matching is indicative only. For official KUCCPS cluster weights and cut-off points, use
      <a href='https://kuccps.ac.ke'>kuccps.ac.ke</a>.
      Salary ranges are broad estimates from public job boards and reported ranges — not verified pay data.
      They should not be used for financial planning or salary negotiation.
    </div>
    """, unsafe_allow_html=True)
