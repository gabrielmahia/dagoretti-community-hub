# Contributing to Dagoretti Community Hub

Thank you for wanting to contribute. This project is volunteer-maintained by Dagoretti alumni.

## Who Can Contribute

- Dagoretti alumni with Python skills
- Community members wanting to update data (alumni profiles, scholarships, KCSE records)
- Anyone who spots a bug or has a feature idea

## Branching Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Production. Deployed by Streamlit Cloud. Never push directly. |
| `dev` | Integration. All PRs merge here first. |
| `feature/xxx` | New features. e.g. `feature/events-board` |
| `fix/xxx` | Bug fixes. e.g. `fix/atlas-filter-crash` |
| `data/xxx` | Data updates. e.g. `data/kcse-2024` |

## PR Checklist

- [ ] Does not break existing pages — test all 9 pages before submitting
- [ ] No hardcoded secrets or API keys — all config goes in `.streamlit/secrets.toml`
- [ ] New pages follow the `render()` pattern and register in `app.py`
- [ ] Data changes include source citation in PR description
- [ ] No unbounded loops over DataFrames — use vectorised pandas operations
- [ ] `@st.cache_data` on any function hitting a database or external API

## Code Style

```bash
pip install black
black pages/ app.py
```

## Not Accepting PRs For

- Changes to the licence
- Features that require users to create accounts (auth is deferred to v2)
- Replacing Plotly with other charting libraries

## Data Contributions

To add alumni profiles, scholarships, or KCSE data:

1. Open an Issue describing the addition
2. The admin team will coordinate data collection and consent
3. Submit via a `data/` branch PR with source citation

**Never add email addresses to CSV files.** Emails stay in the backend only.

## Questions

Open a GitHub Discussion or email [alumni@dagoretti.ac.ke](mailto:alumni@dagoretti.ac.ke).
