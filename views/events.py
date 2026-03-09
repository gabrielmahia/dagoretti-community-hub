"""
Events Board — upcoming reunions, career fairs, fundraisers, meetups.
Seed data covers the Class of 2001 25th reunion and key community events.
Extension: replace seed data with Google Sheets / Supabase backend.
"""

import streamlit as st
import datetime

# ── Seed events ───────────────────────────────────────────────────────────────
# NOTE: These are proposed/planning dates for 2026. They are not confirmed by
# any organising committee. Treat as illustrative until officially announced.
EVENTS = [
    {
        "id": "e001",
        "title": "Class of 2001 — 25th Reunion Dinner",
        "date": datetime.date(2026, 11, 28),
        "time": "6:30 PM – 11:00 PM EAT",
        "type": "Reunion",
        "location": "Nairobi — Venue TBC",
        "is_virtual": False,
        "description": (
            "Twenty-five years since we sat KCSE in 2001. "
            "This event is in the planning stages — the organising committee is yet to confirm "
            "the venue, date and ticket details. Register your interest via email and you will "
            "be the first to hear when it is confirmed."
        ),
        "organiser": "Class of 2001 Organising Committee",
        "link": "mailto:alumni@dagoretti.ac.ke?subject=2001 Reunion Interest",
        "featured": True,
        "gcal_dates": "20261128T183000/20261128T230000",
    },
    {
        "id": "e002",
        "title": "Class of 2001 — Diaspora Virtual Reunion",
        "date": datetime.date(2026, 12, 5),
        "time": "3:00 PM – 5:00 PM EAT (8:00 AM EST / 1:00 PM GMT)",
        "type": "Reunion",
        "location": "Zoom — link sent to registered attendees",
        "is_virtual": True,
        "description": (
            "For classmates who cannot travel to Nairobi. Breakout rooms by country, "
            "a global roll-call, and live connection to Nairobi if a physical event is confirmed. "
            "Free to attend. Register your interest via the Submit Data page."
        ),
        "organiser": "Class of 2001 Organising Committee",
        "link": "mailto:alumni@dagoretti.ac.ke?subject=2001 Diaspora Reunion Register",
        "featured": True,
        "gcal_dates": "20261205T150000/20261205T170000",
    },
    {
        "id": "e003",
        "title": "Alumni Careers Day — Form 3 & 4 Students",
        "date": datetime.date(2026, 9, 19),
        "time": "9:00 AM – 3:00 PM EAT",
        "type": "Career",
        "location": "Dagoretti High School, Kikuyu Road, Nairobi",
        "is_virtual": False,
        "description": (
            "Alumni from medicine, tech, law, finance, and agriculture return to school "
            "to speak to current Form 3 and 4 students about career paths, university selection, "
            "and the road from KCSE to professional life. Proposed for Term 3 2026. "
            "If you are an alumnus who wants to speak, register your interest via email."
        ),
        "organiser": "Alumni Relations Committee",
        "link": "mailto:alumni@dagoretti.ac.ke?subject=Careers Day Speaker 2026",
        "featured": False,
        "gcal_dates": "20260919T090000/20260919T150000",
    },
    {
        "id": "e004",
        "title": "Dagoretti Bursary Fund Drive — 2026",
        "date": datetime.date(2026, 8, 1),
        "time": "All of August 2026",
        "type": "Fundraising",
        "location": "Online / M-Pesa",
        "is_virtual": True,
        "description": (
            "Annual campaign to fund bursaries for bright but financially constrained "
            "current students at Dagoretti. Target: KSh 500,000 to fund 10 bursaries. "
            "Every contribution counts — KSh 1,000 to KSh 100,000 all welcome. "
            "M-Pesa details to be published when the campaign opens."
        ),
        "organiser": "Dagoretti Alumni Foundation",
        "link": "mailto:alumni@dagoretti.ac.ke?subject=Bursary Fund 2026",
        "featured": False,
        "gcal_dates": "20260801T000000/20260831T235900",
    },
    {
        "id": "e005",
        "title": "Alumni vs Current Students Football Match",
        "date": datetime.date(2026, 10, 10),
        "time": "10:00 AM – 1:00 PM EAT",
        "type": "Sports",
        "location": "Dagoretti High School Grounds, Nairobi",
        "is_virtual": False,
        "description": (
            "The annual pride-on-the-line football match. Alumni team vs current Form 4 students. "
            "Class of 2001 alumni especially invited. "
            "Spectators welcome. Bring family. Date subject to school term calendar."
        ),
        "organiser": "Dagoretti Sports Committee",
        "link": "mailto:alumni@dagoretti.ac.ke?subject=Football Match 2026",
        "featured": False,
        "gcal_dates": "20261010T100000/20261010T130000",
    },
    {
        "id": "e006",
        "title": "Nairobi Alumni Networking Evening",
        "date": datetime.date(2026, 7, 16),
        "time": "6:00 PM – 9:00 PM EAT",
        "type": "Networking",
        "location": "Nairobi — Venue TBC",
        "is_virtual": False,
        "description": (
            "Informal evening drinks and networking for Nairobi-based alumni. "
            "No agenda, no speeches — just reconnecting. All years welcome. "
            "Venue confirmed closer to the date."
        ),
        "organiser": "Nairobi Alumni Chapter",
        "link": "mailto:alumni@dagoretti.ac.ke?subject=Nairobi Networking 2026",
        "featured": False,
        "gcal_dates": "20260716T180000/20260716T210000",
    },
    {
        "id": "e007",
        "title": "London Diaspora Gathering",
        "date": datetime.date(2026, 9, 5),
        "time": "4:00 PM – 8:00 PM GMT",
        "type": "Reunion",
        "location": "Venue TBC — Central London",
        "is_virtual": False,
        "description": (
            "Dagoretti alumni based in the UK. "
            "Come meet classmates and connect with the global community. "
            "Venue and ticket details to follow — register interest via email."
        ),
        "organiser": "UK Dagoretti Alumni Chapter",
        "link": "mailto:alumni@dagoretti.ac.ke?subject=London Diaspora Gathering 2026",
        "featured": False,
        "gcal_dates": "20260905T160000/20260905T200000",
    },
]

TYPE_COLORS = {
    "Reunion":     ("#1a5c2e", "#e8f5e9"),
    "Career":      ("#1565c0", "#e3f2fd"),
    "Fundraising": ("#c9a94e", "#fdf3d9"),
    "Sports":      ("#e65100", "#fff3e0"),
    "Networking":  ("#6a1b9a", "#f3e5f5"),
}


def _gcal_link(event: dict) -> str:
    title   = event["title"].replace(" ", "+")
    details = event["description"][:100].replace(" ", "+")
    loc     = event["location"].replace(" ", "+")
    dates   = event["gcal_dates"]
    return (
        f"https://calendar.google.com/calendar/render?action=TEMPLATE"
        f"&text={title}&dates={dates}&details={details}&location={loc}"
    )


def render():
    st.markdown("""
    <div class="section-header">
      <h2>📅 Events</h2>
      <p>Reunions · Career days · Networking · Fundraisers</p>
    </div>
    """, unsafe_allow_html=True)

    today = datetime.date.today()

    # ── Featured: 25th Reunion banner ─────────────────────────────────────────
    featured = [e for e in EVENTS if e.get("featured")]
    for ev in featured:
        days_to = (ev["date"] - today).days
        countdown = f"{days_to} days away" if days_to > 0 else ("Today!" if days_to == 0 else "Past")
        st.markdown(f"""
        <div class="hero-banner" style='margin-bottom:1rem;'>
          <div style='display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.5rem;'>
            <div>
              <div style='font-size:0.8rem; color:#c9a94e; letter-spacing:2px; text-transform:uppercase; margin-bottom:0.3rem;'>
                ⭐ Featured Event
              </div>
              <h2 style='color:#fff; margin:0 0 0.3rem;'>{ev['title']}</h2>
              <p style='margin:0; color:#c8e6c9;'>{ev['date'].strftime('%A, %d %B %Y')} · {ev['time']}</p>
              <p style='margin:0.2rem 0 0; color:#a5d6a7; font-size:0.9rem;'>
                {'🌐 Virtual' if ev['is_virtual'] else '📍'} {ev['location']}
              </p>
            </div>
            <div style='text-align:right;'>
              <div style='font-size:2rem; font-weight:700; color:#c9a94e;'>{countdown}</div>
              <a href='{ev['link']}' target='_blank'
                 style='display:inline-block; background:#c9a94e; color:#0d1a0f; padding:0.4rem 1rem;
                        border-radius:4px; font-size:0.85rem; font-weight:600; text-decoration:none; margin-top:0.4rem;'>
                RSVP →
              </a>
              <a href='{_gcal_link(ev)}' target='_blank'
                 style='display:inline-block; background:transparent; color:#c8e6c9; padding:0.4rem 0.8rem;
                        border-radius:4px; font-size:0.85rem; border:1px solid #4a8060; text-decoration:none;
                        margin-top:0.4rem; margin-left:0.4rem;'>
                + Calendar
              </a>
            </div>
          </div>
          <p style='margin:0.8rem 0 0; color:#e8f5e9; font-size:0.92rem;'>{ev['description']}</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Filter controls ────────────────────────────────────────────────────────
    f1, f2 = st.columns(2)
    with f1:
        all_types = ["All Types"] + sorted(set(e["type"] for e in EVENTS))
        type_filter = st.selectbox("Event type", all_types)
    with f2:
        time_filter = st.radio("Show", ["Upcoming", "All events"], horizontal=True)

    # ── Filtered list ──────────────────────────────────────────────────────────
    filtered = EVENTS.copy()
    if type_filter != "All Types":
        filtered = [e for e in filtered if e["type"] == type_filter]
    if time_filter == "Upcoming":
        filtered = [e for e in filtered if e["date"] >= today]

    filtered.sort(key=lambda e: e["date"])

    st.caption(f"Showing {len(filtered)} event{'s' if len(filtered) != 1 else ''}")

    if not filtered:
        st.info("No upcoming events match the filter. Switch to 'All events' to see past events.")
        return

    # ── Event cards ────────────────────────────────────────────────────────────
    for ev in filtered:
        is_past = ev["date"] < today
        border_color, bg_color = TYPE_COLORS.get(ev["type"], ("#1a5c2e", "#e8f5e9"))
        virtual_tag = '<span class="badge-blue">🌐 Virtual</span>' if ev["is_virtual"] \
                      else '<span class="badge">📍 In-person</span>'
        past_tag = '<span class="badge" style="background:#f5f5f5; color:#9e9e9e; border-color:#e0e0e0;">Past</span>' \
                   if is_past else ""

        days_left = (ev["date"] - today).days
        if not is_past:
            if days_left == 0:
                countdown_html = '<span style="font-weight:700; color:#e65100;">Today!</span>'
            elif days_left <= 7:
                countdown_html = f'<span style="font-weight:700; color:#e65100;">{days_left}d away</span>'
            elif days_left <= 30:
                countdown_html = f'<span style="font-weight:600; color:#c9a94e;">{days_left}d away</span>'
            else:
                countdown_html = f'<span style="color:var(--text-muted);">{days_left}d away</span>'
        else:
            countdown_html = ""

        st.markdown(f"""
        <div style='background:#fff; border-left:4px solid {border_color}; border-radius:8px;
                    padding:1.2rem 1.5rem; box-shadow:0 2px 8px rgba(26,92,46,0.10);
                    margin-bottom:1rem; opacity:{"0.7" if is_past else "1"};'>
          <div style='display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.4rem;'>
            <div>
              <div style='font-size:0.75rem; color:{border_color}; letter-spacing:2px;
                          text-transform:uppercase; margin-bottom:0.25rem;'>
                {ev['type']}
              </div>
              <strong style='color:var(--green-dark); font-size:1.05rem;'>{ev['title']}</strong>
            </div>
            {countdown_html}
          </div>
          <p style='margin:0.3rem 0; color:var(--text-muted); font-size:0.9rem;'>
            🗓 {ev['date'].strftime('%A, %d %B %Y')} · {ev['time']}
          </p>
          <p style='margin:0 0 0.4rem; font-size:0.88rem; color:var(--text-muted);'>
            {'🌐' if ev['is_virtual'] else '📍'} {ev['location']}
          </p>
          <div style='margin-bottom:0.5rem;'>
            {virtual_tag}
            <span class="badge">{ev['type']}</span>
            {past_tag}
          </div>
          <p style='margin:0.4rem 0; font-size:0.88rem;'>{ev['description']}</p>
          <div style='display:flex; gap:0.5rem; flex-wrap:wrap; margin-top:0.6rem;'>
            <a href='{ev['link']}' target='_blank'
               style='background:var(--green-dark); color:#fff; padding:0.25rem 0.9rem;
                      border-radius:4px; font-size:0.82rem; text-decoration:none; font-weight:600;'>
              {'View details' if is_past else 'RSVP / Register →'}
            </a>
            <a href='{_gcal_link(ev)}' target='_blank'
               style='background:transparent; color:var(--green-dark); padding:0.25rem 0.9rem;
                      border-radius:4px; font-size:0.82rem; border:1px solid var(--green-dark);
                      text-decoration:none;'>
              + Google Calendar
            </a>
          </div>
          <p style='margin:0.5rem 0 0; font-size:0.78rem; color:var(--text-muted);'>
            Organised by: {ev['organiser']}
          </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Propose an event ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
      <h2>Propose an Event</h2>
      <p>Organising a reunion, fundraiser, or networking event?</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📋 Submit an event proposal"):
        ev_title  = st.text_input("Event name")
        ev_date   = st.date_input("Date", min_value=today)
        ev_type   = st.selectbox("Type", ["Reunion", "Career", "Fundraising", "Sports", "Networking", "Other"])
        ev_loc    = st.text_input("Location (city or 'Virtual')")
        ev_virtual= st.checkbox("Virtual / online event")
        ev_desc   = st.text_area("Description (max 400 chars)", max_chars=400)
        ev_org    = st.text_input("Organiser name / contact")

        if st.button("Submit Event Proposal"):
            if not all([ev_title, ev_loc, ev_desc, ev_org]):
                st.warning("Please fill in all fields.")
            else:
                st.success(f"✅ Proposal for **{ev_title}** received. The admin team will review and add it within 3 days.")

    st.markdown("""
    <div class="footer">
      Events are community-organised. The hub lists but does not manage ticketing or payments.
      For the Class of 2001 reunion, contact <a href='mailto:alumni@dagoretti.ac.ke'>alumni@dagoretti.ac.ke</a>.
    </div>
    """, unsafe_allow_html=True)
