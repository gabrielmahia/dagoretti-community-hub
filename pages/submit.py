"""
Submit Data — all community input flows.

Tabs:
  1. Alumni Profile   → alumni_submissions sheet
  2. Memory / Message → memory_submissions sheet
  3. Event Proposal   → event_proposals sheet
  4. Data Correction  → corrections sheet
  5. General Feedback → feedback sheet

Backend: Google Sheets via utils/sheets.py
Fallback: visible warning + email instructions when not configured
"""

import streamlit as st
import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import sheets


def render():
    st.markdown("""
    <div class="section-header">
      <h2>📝 Submit Data</h2>
      <p>Contribute to the community — every submission is reviewed before it goes live</p>
    </div>
    """, unsafe_allow_html=True)

    if not sheets.is_configured():
        sheets.not_configured_banner()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👤 Alumni Profile",
        "🕯️ Memory / Message",
        "📅 Propose an Event",
        "✏️ Correct Data",
        "💬 Feedback",
    ])

    # ── Tab 1: Alumni profile ──────────────────────────────────────────────────
    with tab1:
        st.markdown("""
        <div class="card-green">
          Add yourself to the Alumni Atlas and Mentorship directory.
          Only alumni of <strong>Dagoretti High School</strong> (the school, not the area) are listed.
          Fields marked * are required.
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            full_name = st.text_input("Full name *", key="al_name")
            year_left = st.number_input(
                "Year you sat Form 4 KCSE *",
                min_value=1962, max_value=datetime.date.today().year,
                value=2001, key="al_year",
            )
            industry = st.selectbox("Industry *", [
                "Technology", "Medicine", "Engineering", "Law", "Finance",
                "Education", "Journalism", "Agriculture", "Public Service",
                "Business / Entrepreneurship", "Arts / Media", "Other",
            ], key="al_industry")
            role = st.text_input("Current job title *", key="al_role")
        with c2:
            city = st.text_input("City of residence *", key="al_city")
            country = st.text_input("Country of residence *", key="al_country")
            linkedin_url = st.text_input("LinkedIn URL (optional)", key="al_li")
            mentoring = st.radio(
                "Open to mentoring current students?",
                ["Yes", "No"], horizontal=True, key="al_mentor",
            )

        bio = st.text_area(
            "Short bio (max 220 characters) *",
            max_chars=220, key="al_bio",
            placeholder="e.g. Software engineer in Nairobi. Passionate about edtech and youth mentorship.",
        )
        email_admin = st.text_input(
            "Email (not shown publicly — admin verification only) *",
            placeholder="your@email.com", key="al_email",
        )
        consent = st.checkbox(
            "I confirm I attended Dagoretti High School (the school), "
            "this information is accurate, and I consent to it appearing on the Dagoretti Community Hub.",
            key="al_consent",
        )

        if st.button("Submit Alumni Profile", type="primary", key="al_submit"):
            errors = []
            if not full_name:   errors.append("Full name")
            if not city:        errors.append("City")
            if not country:     errors.append("Country")
            if not bio:         errors.append("Bio")
            if not email_admin: errors.append("Email")
            if not consent:     errors.append("Consent checkbox")
            if errors:
                st.warning(f"Please complete: {', '.join(errors)}")
            else:
                ok = sheets.append_row("alumni_submissions", {
                    "full_name": full_name, "year_left": year_left,
                    "industry": industry, "role": role,
                    "city": city, "country": country,
                    "linkedin_url": linkedin_url, "mentoring": mentoring,
                    "bio": bio, "email_admin": email_admin,
                })
                if ok:
                    sheets.success_banner(
                        full_name,
                        "Your profile will be reviewed and added to the Alumni Atlas within 5-7 days.",
                    )
                    st.balloons()
                elif not sheets.is_configured():
                    st.info(f"Email your details to alumni@dagoretti.ac.ke — Subject: Alumni Profile — {full_name}")

    # ── Tab 2: Memory / Message ────────────────────────────────────────────────
    with tab2:
        st.markdown("""
        <div class="card-green">
          Share a memory, a reflection, or a milestone. Approved submissions appear on the Memory Wall.
          Open to all Dagoretti alumni — especially Class of 2001 for the 25th reunion.
        </div>
        """, unsafe_allow_html=True)

        mem_name = st.text_input("Your name *", key="mem_name")
        mem_year = st.number_input(
            "Year you sat Form 4 at Dagoretti *",
            min_value=1962, max_value=datetime.date.today().year,
            value=2001, key="mem_year",
        )
        mem_type = st.radio("Type of submission", [
            "Memory — a story from school days",
            "Reflection — a lesson the school taught you",
            "Milestone — a personal achievement to celebrate",
        ], key="mem_type")
        mem_body = st.text_area(
            "Your submission *",
            max_chars=800, key="mem_body", height=160,
            placeholder="Write in first person. Be specific — a teacher's name, a moment in class, a lesson that stayed with you.",
        )

        if st.button("Submit Memory / Message", type="primary", key="mem_submit"):
            if not mem_name or not mem_body:
                st.warning("Please fill in your name and the submission text.")
            else:
                ok = sheets.append_row("memory_submissions", {
                    "name": mem_name,
                    "year_at_dagoretti": mem_year,
                    "submission_type": mem_type.split(" —")[0],
                    "body": mem_body,
                })
                if ok:
                    sheets.success_banner(
                        mem_name,
                        "Your submission will be reviewed and added to the Memory Wall.",
                    )
                elif not sheets.is_configured():
                    st.info(f"Email your memory to alumni@dagoretti.ac.ke — Subject: Memory Wall — {mem_name}")

    # ── Tab 3: Event Proposal ──────────────────────────────────────────────────
    with tab3:
        st.markdown("""
        <div class="card-green">
          Propose a reunion, networking evening, fundraiser, or community event.
          Confirmed events are added to the Events board.
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            ev_title = st.text_input("Event name *", key="ev_title")
            ev_type = st.selectbox("Event type *", [
                "Reunion", "Networking", "Fundraising", "Career / Mentorship",
                "Sports", "Virtual / Online", "Other",
            ], key="ev_type")
            ev_date = st.date_input(
                "Proposed date *",
                min_value=datetime.date.today(), key="ev_date",
            )
        with c2:
            ev_location = st.text_input(
                "Location / Venue *", key="ev_loc",
                placeholder="e.g. Nairobi (venue TBC) or Zoom",
            )
            ev_proposer = st.text_input("Your name *", key="ev_proposer")
            ev_contact = st.text_input(
                "Contact email *", key="ev_email",
                placeholder="for follow-up by admin team",
            )

        ev_desc = st.text_area(
            "Description *",
            max_chars=600, key="ev_desc", height=120,
            placeholder="Who is it for? What will happen? Ticketing or RSVP details?",
        )

        if st.button("Propose Event", type="primary", key="ev_submit"):
            errors = []
            if not ev_title:    errors.append("Event name")
            if not ev_location: errors.append("Location")
            if not ev_proposer: errors.append("Your name")
            if not ev_contact:  errors.append("Contact email")
            if not ev_desc:     errors.append("Description")
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
                        f"Your proposal for '{ev_title}' is under review. The admin team will be in touch.",
                    )
                elif not sheets.is_configured():
                    st.info(f"Email your event proposal to alumni@dagoretti.ac.ke — Subject: Event Proposal — {ev_title}")

    # ── Tab 4: Data Correction ─────────────────────────────────────────────────
    with tab4:
        st.markdown("""
        <div class="card-green">
          Spotted incorrect data anywhere on the site? Submit a correction with a source link
          and it will be reviewed within 48 hours.
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            cr_page = st.selectbox("Which page has the error? *", [
                "KCSE Tracker", "Kenya: Then & Now", "Scholarships",
                "Memory Wall", "Notable Alumni", "Alumni Atlas", "Events", "Other",
            ], key="cr_page")
            cr_field = st.text_input(
                "Which field or figure is wrong? *", key="cr_field",
                placeholder="e.g. '2019 mean score' or 'Chevening deadline'",
            )
        with c2:
            cr_current = st.text_input(
                "What does it currently say? *", key="cr_current",
                placeholder="The value shown on the site",
            )
            cr_correct = st.text_input(
                "What should it say? *", key="cr_correct",
                placeholder="The correct value",
            )

        cr_source = st.text_input(
            "Source URL *",
            key="cr_source",
            placeholder="https://knec.ac.ke/... — a link confirming the correct value",
        )
        c1, c2 = st.columns(2)
        with c1:
            cr_name = st.text_input("Your name (optional)", key="cr_name")
        with c2:
            cr_email = st.text_input("Your email (optional — for follow-up)", key="cr_email")

        if st.button("Submit Correction", type="primary", key="cr_submit"):
            errors = []
            if not cr_field:   errors.append("Which field is wrong")
            if not cr_current: errors.append("Current value")
            if not cr_correct: errors.append("Correct value")
            if not cr_source:  errors.append("Source URL")
            if errors:
                st.warning(f"Please complete: {', '.join(errors)}")
            else:
                ok = sheets.append_row("corrections", {
                    "page": cr_page, "field": cr_field,
                    "current_value": cr_current, "correct_value": cr_correct,
                    "source_url": cr_source,
                    "submitter_name": cr_name, "submitter_email": cr_email,
                })
                if ok:
                    sheets.success_banner(
                        cr_name or "contributor",
                        "Your correction will be reviewed against the source within 48 hours.",
                    )
                elif not sheets.is_configured():
                    st.info("Email your correction to alumni@dagoretti.ac.ke — Subject: Data Correction")

    # ── Tab 5: General Feedback ────────────────────────────────────────────────
    with tab5:
        st.markdown("""
        <div class="card-green">
          Bug reports, feature ideas, or general comments. We read everything.
        </div>
        """, unsafe_allow_html=True)

        fb_name    = st.text_input("Name (optional)", key="fb_name")
        fb_type    = st.selectbox("Type of feedback", [
            "Bug report", "Feature request", "Data correction",
            "Scholarship suggestion", "General comment",
        ], key="fb_type")
        fb_message = st.text_area("Your message *", height=140, key="fb_message")
        fb_email   = st.text_input("Email (optional — if you want a reply)", key="fb_email")

        if st.button("Send Feedback", type="primary", key="fb_submit"):
            if not fb_message:
                st.warning("Please enter a message.")
            else:
                ok = sheets.append_row("feedback", {
                    "name": fb_name, "feedback_type": fb_type,
                    "message": fb_message, "reply_email": fb_email,
                })
                if ok:
                    sheets.success_banner(fb_name or "contributor")
                elif not sheets.is_configured():
                    st.info("Email your feedback to alumni@dagoretti.ac.ke")

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div class="card">
      <strong>Direct contact</strong><br>
      <span style='font-size:0.9rem;'>
        For urgent matters: <a href='mailto:alumni@dagoretti.ac.ke'>alumni@dagoretti.ac.ke</a>
      </span><br>
      <span style='font-size:0.9rem; color:#888; margin-top:0.3rem; display:block;'>
        All submissions are reviewed before appearing on the platform.
        Personal emails are never displayed publicly.
      </span>
    </div>
    """, unsafe_allow_html=True)
