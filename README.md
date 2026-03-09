# 🦁 Dagoretti High School Community Hub

A free, open-source Streamlit web application for the Dagoretti High School community — alumni, students, parents, and teachers.

**Live demo:** https://[your-username]-dagoretti-hub.streamlit.app

---

## What This Is

- **Alumni Atlas** — World map and directory of Dagoretti graduates across 15+ countries
- **KCSE Tracker** — 30 years of exam results with trend analysis
- **Career Pathways** — Enter your KCSE subjects and grades; explore matching careers and universities
- **Memory Wall** — Class of 2001 · 25th anniversary tribute
- **Kenya: Then & Now** — 25 indicators comparing Kenya in 2001 and 2025
- **Mentorship** — Directory of alumni open to guiding students
- **Scholarships** — 25 curated opportunities including diaspora-accessible awards
- **Submit Data** — Community data submission forms

## Quick Start

```bash
# 1. Clone
git clone https://github.com/dagoretti-community/hub.git
cd hub

# 2. Virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install
pip install -r requirements.txt

# 4. Configure
mkdir -p .streamlit
cat > .streamlit/config.toml << 'EOF'
[server]
headless = true
port = 8501

[theme]
primaryColor = '#1a5c2e'
backgroundColor = '#fdf8f0'
secondaryBackgroundColor = '#e8f5e9'
textColor = '#0d1a0f'
font = 'sans serif'
EOF

# 5. Run
streamlit run app.py
```

Open http://localhost:8501.

## Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub (public or private)
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select repo → set main file path to `app.py`
4. Click **Deploy** — live in ~2 minutes

## Adding a New Page

```python
# 1. Create pages/my_feature.py with a render() function
def render():
    import streamlit as st
    st.markdown('<div class="section-header"><h2>My Feature</h2></div>', unsafe_allow_html=True)
    # ... your logic

# 2. In app.py, add to the pages dict:
pages["🔧 My Feature"] = "my_feature"

# 3. Add to routing:
elif page == "my_feature":
    from pages import my_feature as p; p.render()
```

That's it. The page inherits all global CSS automatically.

## Data Files

| File | Description |
|------|-------------|
| `data/alumni.csv` | 50 seed alumni across 15+ countries |
| `data/kcse_results.csv` | 30 years of KCSE data (1995–2024) — **see KCSE data note** |
| `data/scholarships.csv` | 25 scholarship opportunities |
| `data/kenya_then_now.csv` | 25 Kenya 2000 vs 2025 indicators |

**KCSE data note:** Historical data for 1995–2009 is illustrative. Replace with verified KNEC data from [knec.ac.ke](https://knec.ac.ke) before public launch.

## Making It Production-Ready

See the [Engineering Spec](docs/ENGINEERING_SPEC.md) for backend options:

- **Option A: Google Sheets** — Recommended for v1. Free, no server, non-technical admin friendly.
- **Option B: Supabase** — Recommended for v2+. Postgres with row-level security.
- **Option C: Airtable** — Best for volunteer-managed communities.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## IP & Collaboration

See [docs/IP_POLICY.md](docs/IP_POLICY.md).

## Licence

MIT Licence. Free to use, modify, and distribute with attribution.  
If you adapt this for another Kenyan school — Mang'u, Alliance, Starehe, Lenana — please open-source your version and share the link.

---

Built by alumni. For the community. Nairobi, Kenya 🇰🇪
