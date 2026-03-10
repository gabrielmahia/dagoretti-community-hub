"""
Events Board — community-proposed and confirmed events.

NO events are hardcoded or synthesized. Every event shown has been
proposed via the Submit Data form and confirmed by an admin.
Empty at launch — grows as the community submits real proposals.
"""

import streamlit as st
import datetime
import os
import pandas as pd


EVENTS_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "events.csv")
EVENTS_SCHEMA = ["id", "title", "date", "time", "type", "location",
                 "is_virtual", "description", "organiser", "link",
                 "featured", "status"]

TYPE_COLORS = {
    "Reunion":     ("#1a5c2e", "#e8f5e9"),
    "Career":      ("#1565c0", "#e3f2fd"),
    "Fundraising": ("#c9a94e", "#fdf3d9"),
    "Sports":      ("#e65100", "#fff3e0"),
    "Networking":  ("#6a1b9a", "#f3e5f5"),
    "Virtual":     ("#00695c", "#e0f2f1"),
    "Other":       ("#37474f", "#eceff1"),
}


def _load_events():
    """Load approved events from CSV. Returns empty DataFrame on any failure."""
    try:
        if not os.path.exists(EVENTS_CSV):
            return pd.DataFrame(columns=EVENTS_SCHEMA)
        df = pd.read_csv(EVENTS_CSV)
        if "status" in df.columns:
            df = df[df["status"].str.lower() == "approved"]
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        return df.dropna(subset=["date"]).sort_values("date")
    except Exception:
        return pd.DataFrame(columns=EVENTS_SCHEMA)


def render():
    st.markdown("""
    <div class="hero-banner">
      <h1>📅 Events</h1>
      <p>Reunions · Networking · Fundraising · Careers · Sports</p>
      <p style='color:#81c784; font-size:0.88rem; margin-top:0.3rem;'>
        All events are proposed by alumni and confirmed before appearing here.
      </p>
    </div>
    """, unsafe_allow_html=True)

    df = _load_events()
    today = datetime.date.today()

    upcoming = df[df["date"].dt.date >= today] if not df.empty else pd.DataFrame()
    past     = df[df["date"].dt.date <  today] if not df.empty else pd.DataFrame()

    # ── Upcoming events ────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>Upcoming Events</h2>
    </div>
    """, unsafe_allow_html=True)

    if upcoming.empty:
        st.markdown("""
        <div class="card" style="text-align:center; padding:2.5rem 1.5rem;">
          <div style="font-size:2.5rem; margin-bottom:0.75rem;">📭</div>
          <h3 style="color:var(--green-dark); margin:0 0 0.4rem;">No confirmed events yet.</h3>
          <p style="color:var(--text-muted); font-size:0.92rem; margin:0;">
            Have an idea for a reunion, networking evening, careers day, or fundraiser?
            Propose it below — the admin team will confirm and list it here.
          </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for _, ev in upcoming.iterrows():
            _render_event_card(ev)

    st.markdown("---")

    # ── Propose an event ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>📬 Propose an Event</h2>
      <p>Your proposal goes to the admin team for review — confirmed events are listed above</p>
    </div>
    """, unsafe_allow_html=True)

    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from utils import sheets

    if not sheets.is_configured():
        sheets.not_configured_banner()

    with st.form("event_proposal_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            ev_title    = st.text_input("Event name *")
            ev_type     = st.selectbox("Type *", [
                "Reunion", "Networking", "Fundraising",
                "Career / Mentorship", "Sports", "Virtual / Online", "Other",
            ])
            ev_date     = st.date_input("Proposed date *", min_value=today)
        with c2:
            ev_location = st.text_input("Location / Venue *",
                            placeholder="e.g. Nairobi (venue TBC) or Zoom")
            ev_proposer = st.text_input("Your name *")
            ev_contact  = st.text_input("Your email *",
                            placeholder="for follow-up by admin team")

        ev_desc = st.text_area("Description *", height=110, max_chars=600,
                    placeholder="Who is it for? What will happen? "
                                "Any ticketing or RSVP details you know so far?")

        submitted = st.form_submit_button("Submit Proposal", type="primary")

    if submitted:
        errors = [f for f, v in [
            ("Event name", ev_title), ("Location", ev_location),
            ("Your name", ev_proposer), ("Email", ev_contact),
            ("Description", ev_desc),
        ] if not v]
        if errors:
            st.warning(f"Please complete: {', '.join(errors)}")
        else:
            ok = sheets.append_row("event_proposals", {
                "proposer_name": ev_proposer, "event_title": ev_title,
                "proposed_date": str(ev_date), "event_type": ev_type,
                "location": ev_location, "description": ev_desc,
                "contact_email": ev_contact,
            })
            if ok:
                sheets.success_banner(
                    ev_proposer,
                    f"Proposal for '{ev_title}' received — the admin team will be in touch.",
                )
            elif not sheets.is_configured():
                st.info(f"Email your proposal to contact@gabrielmahia.com — Subject: Event Proposal — {ev_title}")

    # ── Past events ────────────────────────────────────────────────────────────
    if not past.empty:
        with st.expander(f"📁 Past events ({len(past)})", expanded=False):
            for _, ev in past.sort_values("date", ascending=False).iterrows():
                _render_event_card(ev, past=True)


def _render_event_card(ev, past: bool = False):
    ev_type  = str(ev.get("type", "Other"))
    colors   = TYPE_COLORS.get(ev_type, TYPE_COLORS["Other"])
    border   = colors[0]
    bg       = colors[1]
    virtual  = str(ev.get("is_virtual", "")).lower() in ("true", "1", "yes")
    v_badge  = '<span class="badge">🌐 Virtual</span>' if virtual else ""
    opacity  = "opacity:0.65;" if past else ""
    date_str = ev["date"].strftime("%A, %-d %B %Y") if hasattr(ev["date"], "strftime") else str(ev["date"])
    link_html = ""
    if ev.get("link") and str(ev.get("link", "")).startswith(("http", "mailto")):
        link_html = (
            f'<a href="{ev["link"]}" target="_blank" '
            f'style="background:var(--green-dark); color:#fff; padding:0.25rem 0.8rem; '
            f'border-radius:4px; font-size:0.82rem; text-decoration:none;">RSVP / Info &#8594;</a>'
        )

    card = (
        f'<div class="card" style="border-left:4px solid {border}; {opacity}">'
        f'<div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.4rem;">'
        f'<h4 style="margin:0; color:var(--green-dark);">{ev["title"]}</h4>'
        f'<span class="badge" style="background:{bg}; color:{border}; border-color:{border};">{ev_type}</span>'
        f'</div>'
        f'<p style="margin:0.3rem 0 0; font-size:0.88rem; color:var(--text-muted);">📅 {date_str}'
        + (f' &nbsp;·&nbsp; {ev["time"]}' if ev.get("time") else "") +
        f'</p>'
        f'<p style="margin:0.2rem 0 0; font-size:0.88rem; color:var(--text-muted);">📍 {ev["location"]}</p>'
        f'<p style="margin:0.5rem 0 0; font-size:0.9rem;">{ev["description"]}</p>'
        f'<div style="margin-top:0.6rem; display:flex; gap:0.5rem; align-items:center; flex-wrap:wrap;">'
        f'{v_badge} {link_html}'
        f'</div>'
        f'</div>'
    )
    st.markdown(card, unsafe_allow_html=True)
