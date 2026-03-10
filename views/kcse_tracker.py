"""
KCSE Tracker — confirmed results only.

Only years with a verified primary source are shown.
Every other year is an explicit gap waiting to be filled.

Confirmed: 2014, 2015 (school Facebook page); 2022–2025 (Rejnac Daily/KNEC Jan 2026)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import sheets


@st.cache_data(ttl=300)
def _load():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "kcse_results.csv")
    try:
        df = pd.read_csv(path).fillna("")
        df["year"]       = pd.to_numeric(df["year"], errors="coerce")
        df["mean_grade"] = pd.to_numeric(df["mean_grade"], errors="coerce")
        df["candidates"] = pd.to_numeric(df["candidates"], errors="coerce")
        return df.dropna(subset=["year","mean_grade"]).sort_values("year")
    except FileNotFoundError:
        return pd.DataFrame()


GRADE_LABELS = {12:"A",11:"A−",10:"B+",9:"B",8:"B−",7:"C+",6:"C",5:"C−",4:"D+",3:"D",2:"D−",1:"E"}
GRADE_COLS   = ["a_plain","a_minus","b_plus","b_plain","b_minus","c_plus","c_plain","c_minus","d_plus","d_plain","d_minus","e"]
GRADE_NAMES  = ["A","A−","B+","B","B−","C+","C","C−","D+","D","D−","E"]


def render():
    st.markdown("""
    <div class="section-header">
      <h2>📊 KCSE Tracker</h2>
      <p>Confirmed exam results only · Source-verified · No estimates</p>
    </div>
    """, unsafe_allow_html=True)

    df = _load()
    confirmed_years = sorted(df["year"].dropna().astype(int).tolist()) if not df.empty else []
    n_confirmed = len(confirmed_years)
    n_missing   = len([y for y in range(1995, 2026) if y not in confirmed_years])

    st.markdown(f"""
    <div class="card-gold">
      <strong>Data integrity:</strong> This tracker shows <strong>{n_confirmed} confirmed years</strong>
      with verified primary sources. <strong>{n_missing} years (1995–2021 except 2014–2015) have no
      verified data</strong> and are intentionally left blank.<br>
      <span style="font-size:0.85rem;">
      📌 <strong>2014 &amp; 2015</strong> — mean grade and candidate count confirmed via school Facebook.
      Per-grade breakdowns (A, A−, B+, …) were not in that source and previously contained
      placeholder numbers that did not add up. Those have been removed.
      </span><br>
      If you have KNEC records, school transcripts, or newspaper links for any missing year or grade breakdown,
      contribute below — every verified addition is permanent.<br>
      <span style="font-size:0.85rem;">
      📌 <strong>2025:</strong> 389 candidates — nearly double the ~200 average in prior confirmed years.
      This likely reflects real school growth and/or expanded cohort registration.
      The figure comes from Rejnac Daily/KNEC (Jan 2026) and is marked confirmed, but
      if you have the official KNEC abstract to cross-check, please contribute it below.
      </span>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.info("No confirmed KCSE data loaded.")
        _render_contribution_form([])
        return

    latest    = df[df["year"] == df["year"].max()].iloc[0]
    latest_yr = int(latest["year"])

    # ── KPI pills ──────────────────────────────────────────────────────────────
    pills_data = [
        (str(n_confirmed), "Confirmed years"),
        (f"{latest['mean_grade']:.2f}/12", f"Mean grade ({latest_yr})"),
        (f"{int(latest['candidates'])}", f"Candidates ({latest_yr})"),
        (str(n_missing), "Years still missing"),
    ]
    ph = '<div style="display:flex;flex-wrap:wrap;gap:0.6rem;margin-bottom:1rem;">'
    for val, lbl in pills_data:
        ph += (
            f'<div style="flex:1 1 130px;min-width:110px;background:#fdf8f0;'
            f'border-left:3px solid #1a5c2e;border-radius:6px;padding:0.7rem 0.9rem;">'
            f'<div style="font-size:1.35rem;font-weight:800;color:#1a5c2e;">{val}</div>'
            f'<div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.05em;color:#4a5e4d;">{lbl}</div>'
            f'</div>'
        )
    ph += '</div>'
    st.markdown(ph, unsafe_allow_html=True)

    st.markdown("---")

    # ── Mean grade chart ───────────────────────────────────────────────────────
    st.markdown("#### Mean Grade — Confirmed Years")
    st.caption("Grey bands = years with no verified data. No interpolation shown.")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["year"].astype(int), y=df["mean_grade"],
        mode="markers+text", name="Confirmed",
        marker=dict(size=16, color="#1a5c2e", line=dict(color="#c9a94e", width=2)),
        text=[f"{v:.2f}" for v in df["mean_grade"]],
        textposition="top center",
        textfont=dict(size=11, color="#1a5c2e"),
    ))

    # Gap bands
    in_gap, gap_start = False, None
    for y in range(1995, 2027):
        if y not in confirmed_years:
            if not in_gap: gap_start, in_gap = y, True
        else:
            if in_gap:
                fig.add_vrect(x0=gap_start-0.4, x1=y-0.6,
                    fillcolor="rgba(180,180,180,0.12)", line_width=0,
                    annotation_text="no data" if (y-gap_start)>=4 else "",
                    annotation_font_size=9, annotation_font_color="#bbb",
                    annotation_position="top left")
                in_gap = False
    if in_gap:
        fig.add_vrect(x0=gap_start-0.4, x1=2025.4,
            fillcolor="rgba(180,180,180,0.12)", line_width=0)

    fig.update_layout(
        paper_bgcolor="#fdf8f0", plot_bgcolor="#fdf8f0",
        margin=dict(l=0,r=0,t=10,b=0), height=340, showlegend=False,
        yaxis=dict(range=[4,10], title="Mean grade (1–12)",
                   gridcolor="#e8f5e9",
                   tickvals=[5,6,7,8,9], ticktext=["C−","C","C+","B−","B"]),
        xaxis=dict(title="Year", gridcolor="#e8f5e9",
                   tickmode="array",
                   tickvals=confirmed_years,
                   ticktext=[str(y) for y in confirmed_years]),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Grade distribution ─────────────────────────────────────────────────────
    st.markdown("#### Grade Distribution — Select Year")
    selected_year = st.selectbox("Year", sorted(df["year"].unique().astype(int), reverse=True), key="kcse_yr_sel")
    yr_row = df[df["year"] == selected_year].iloc[0]
    dist_vals = [pd.to_numeric(yr_row.get(c,0), errors="coerce") or 0 for c in GRADE_COLS]
    source_note = str(yr_row.get("source","Verified")).strip()

    if any(v > 0 for v in dist_vals):
        fig2 = px.bar(x=GRADE_NAMES, y=dist_vals,
            labels={"x":"Grade","y":"Students"},
            color=GRADE_NAMES,
            color_discrete_sequence=[
                "#1a5c2e","#2e7d46","#43a059","#66bb6a","#a5d6a7",
                "#c9a94e","#f0c040","#f9a825","#e57373","#ef5350","#d32f2f","#b71c1c"],
        )
        fig2.update_layout(
            paper_bgcolor="#fdf8f0", plot_bgcolor="#fdf8f0",
            margin=dict(l=0,r=0,t=10,b=0), height=270, showlegend=False,
            yaxis=dict(gridcolor="#e8f5e9"),
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.markdown(
            '<div class="card-gold" style="font-size:0.88rem;">'
            '⚠️ <strong>Grade distribution not displayed for this year.</strong><br>'
            'The mean grade and candidate count were confirmed from the school\'s official Facebook page. '
            'The per-grade breakdown (A, A−, B+, …) was not published in that source — so no distribution '
            'is shown here. Previously, placeholder numbers were loaded that did not add up to the '
            'confirmed candidate count. Those have been removed to preserve data integrity.<br>'
            'If you have the KNEC certificate slip or a newspaper clipping with the full grade breakdown '
            'for this year, please contribute it below.'
            '</div>',
            unsafe_allow_html=True,
        )

    a_count = int(pd.to_numeric(yr_row.get("a_plain",0), errors="coerce") or 0)
    st.markdown(
        f'<div class="card" style="font-size:0.87rem;">'
        f'<strong>{selected_year}</strong> · {int(yr_row["candidates"])} candidates · '
        f'Mean <strong>{float(yr_row["mean_grade"]):.2f}</strong> ({_grade_str(float(yr_row["mean_grade"]))}) · '
        f'A grades: {a_count}'
        f'<br><span style="color:#4a5e4d;font-size:0.79rem;">✅ Source: {source_note}</span>'
        f'</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Gap visualisation ──────────────────────────────────────────────────────
    st.markdown("#### Missing Years — Help Fill the Record")
    st.caption("Grey = no verified data · Green = confirmed · 1995–2025 shown")

    grid_html = '<div style="display:flex;flex-wrap:wrap;gap:0.3rem;margin-bottom:1rem;">'
    for y in range(1995, 2026):
        if y in confirmed_years:
            grid_html += (
                f'<div style="padding:4px 9px;border-radius:4px;font-size:0.77rem;'
                f'background:#e8f5e9;color:#1a5c2e;font-weight:700;">{y} ✓</div>'
            )
        else:
            grid_html += (
                f'<div style="padding:4px 9px;border-radius:4px;font-size:0.77rem;'
                f'background:#f5f5f5;color:#aaa;border:1px dashed #ddd;">{y}</div>'
            )
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

    # ── Full table ─────────────────────────────────────────────────────────────
    with st.expander("📋 Full results table (confirmed years only)"):
        show = df[["year","mean_grade","candidates","source"]].sort_values("year", ascending=False).copy()
        show.columns = ["Year","Mean Grade","Candidates","Source"]
        show["Year"] = show["Year"].astype(int)
        st.dataframe(show, use_container_width=True, hide_index=True)
        st.caption("Every row confirmed from primary source. No estimates, no interpolation.")

    st.markdown("---")
    _render_contribution_form(confirmed_years)


def _render_contribution_form(confirmed_years):
    st.markdown("""
    <div class="section-header">
      <h2>📥 Contribute KCSE Data</h2>
      <p>Add a verified year · Source URL required · Admin-reviewed before publishing</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-green">
      <strong>Valid sources:</strong> Official KNEC publications · School official social media ·
      Named newspaper reports (Daily Nation, The Standard, The Star) ·
      Your own certified KNEC transcript for a specific year.<br>
      <strong>Not accepted:</strong> WhatsApp screenshots · Undated social media posts · Memory alone.
    </div>
    """, unsafe_allow_html=True)

    missing = [str(y) for y in range(1995, 2026) if y not in confirmed_years]

    c1, c2 = st.columns(2)
    with c1:
        year_sel   = st.selectbox("Year *", ["— select"]+missing+["Earlier than 1995","2026 and later"], key="kcsec_yr")
        mean_score = st.text_input("Mean score *", placeholder="e.g. 7.83 or B plain", key="kcsec_mean")
        n_cands    = st.text_input("Number of candidates (if known)", placeholder="e.g. 164", key="kcsec_cands")
    with c2:
        source_url  = st.text_input("Source URL * (must be a verifiable link)", placeholder="https://...", key="kcsec_src")
        top_student = st.text_input("Top student name (optional — public record only)", key="kcsec_top")
        top_grade   = st.text_input("Top student grade (optional)", placeholder="e.g. A plain", key="kcsec_topg")

    grade_dist = st.text_area(
        "Grade distribution (optional — paste as: A=12, A-=8, B+=10, ...)",
        key="kcsec_dist", height=70,
        placeholder="A=12, A-=8, B+=10, B=14, B-=16, C+=22, C=31, C-=28, D+=15, D=9, D-=5, E=1",
    )
    c1b, c2b = st.columns(2)
    with c1b:
        sub_name  = st.text_input("Your name (optional)", key="kcsec_name")
    with c2b:
        sub_email = st.text_input("Email (optional — for source follow-up)", key="kcsec_email")

    if st.button("Submit KCSE Data", type="primary", key="kcsec_btn"):
        errs = []
        if not year_sel or year_sel == "— select": errs.append("Year")
        if not mean_score:   errs.append("Mean score")
        if not source_url or not source_url.startswith("http"): errs.append("Valid source URL (must start https://)")
        if errs:
            st.warning(f"Please complete: {', '.join(errs)}")
        else:
            ok = sheets.append_row("kcse_submissions", {
                "year": year_sel, "mean_score": mean_score,
                "candidates": n_cands, "grade_distribution": grade_dist,
                "top_student": top_student, "top_grade": top_grade,
                "source_url": source_url,
                "submitter_name": sub_name, "submitter_email": sub_email,
            })
            if ok:
                sheets.success_banner(
                    sub_name or "contributor",
                    f"Data for {year_sel} received. Cross-checked against source and added within 5–7 days if verified.",
                )
            elif not sheets.is_configured():
                st.info(
                    f"Email KCSE data to contact@gabrielmahia.com — "
                    f"Subject: KCSE Data {year_sel} — include your source URL."
                )


def _grade_str(mean: float) -> str:
    return GRADE_LABELS.get(round(mean), "C")
