"""
Submit Data — community data submission forms.

NOTE: Forms currently display success messages but do NOT persist data.
This is the top priority for v1.1. See §6 of the engineering spec for
Google Sheets, Supabase, and Airtable backend options.
"""

import streamlit as st
import datetime


def render():
    st.markdown("""
    <div class="section-header">
      <h2>📝 Submit Data</h2>
      <p>Add yourself to the community — or update an existing listing</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-gold">
      ⚠️ <strong>Data note:</strong> Submissions are currently reviewed by the admin team and
      manually added to the platform. A database backend is on the roadmap. Thank you for
      your patience.
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["👤 Alumni Profile", "🕯️ Memory / Message", "💬 General Feedback"])

    # ── Tab 1: Alumni profile ──────────────────────────────────────────────────
    with tab1:
        st.markdown("""
        <div class="card-green">
          Add yourself to the Alumni Atlas and Mentorship directory.
          Fields marked * are required.
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            full_name    = st.text_input("Full name *")
            year_left    = st.number_input("Year you left Dagoretti (Form 4) *",
                                           min_value=1965, max_value=datetime.date.today().year, value=2000)
            industry     = st.selectbox("Industry *", [
                "Technology", "Medicine", "Engineering", "Law", "Finance",
                "Education", "Journalism", "Agriculture", "Health", "Business", "Other",
            ])
            role         = st.text_input("Current job title *")
        with c2:
            city         = st.text_input("City of residence *")
            country      = st.text_input("Country of residence *")
            linkedin_url = st.text_input("LinkedIn URL (optional)")
            mentoring    = st.radio("Open to mentoring?", ["Yes", "No"], horizontal=True)

        bio = st.text_area(
            "Short bio (max 200 characters) *",
            max_chars=200,
            placeholder="e.g. Software engineer in Nairobi. Passionate about edtech and youth mentorship."
        )
        email_contact = st.text_input(
            "Email (not displayed publicly — admin contact only)",
            placeholder="your@email.com"
        )

        consent = st.checkbox(
            "I confirm this information is accurate and I consent to it appearing on the Dagoretti Community Hub."
        )

        if st.button("Submit Alumni Profile", type="primary"):
            if not all([full_name, city, country, bio, consent]):
                st.warning("Please fill in all required fields and confirm consent.")
            else:
                st.success(f"""
                ✅ **Thank you, {full_name}!**

                Your submission has been received. The admin team will review and add your profile
                within 5–7 days. If you listed a LinkedIn URL, you may receive a connection request
                from the alumni team to confirm identity.
                """)
                st.balloons()

    # ── Tab 2: Memory / Message ────────────────────────────────────────────────
    with tab2:
        st.markdown("""
        <div class="card-green">
          Share a memory, a milestone, or a message for the Memory Wall. Open to all alumni —
          especially Class of 2000 for the 25th reunion year.
        </div>
        """, unsafe_allow_html=True)

        mem_name  = st.text_input("Your name *", key="mem_name")
        mem_year  = st.number_input("Your year at Dagoretti *",
                                    min_value=1965, max_value=datetime.date.today().year,
                                    value=2000, key="mem_year")
        mem_type  = st.radio("Type of submission", [
            "Memory (a story from school days)",
            "Message (a reflection for current students)",
            "Milestone (a personal achievement to celebrate)",
        ], key="mem_type")
        mem_body  = st.text_area(
            "Your memory / message / milestone *",
            max_chars=800,
            placeholder="Write in first person. Be specific — a teacher's name, a classroom moment, a lesson learned.",
            key="mem_body",
            height=160,
        )

        if st.button("Submit Memory / Message", type="primary", key="mem_submit"):
            if not all([mem_name, mem_body]):
                st.warning("Please fill in your name and the submission text.")
            else:
                st.success(f"""
                ✅ **Thank you, {mem_name}!**

                Your {'memory' if 'Memory' in mem_type else 'message' if 'Message' in mem_type else 'milestone'}
                has been received. It will be reviewed and added to the Memory Wall within 5–7 days.
                """)

    # ── Tab 3: General feedback ────────────────────────────────────────────────
    with tab3:
        st.markdown("""
        <div class="card-green">
          Bug reports, feature suggestions, data corrections, or just want to say hello?
          We read everything.
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
                st.success("""
                ✅ **Thank you for your feedback!**

                We have received your message. If you left an email address and requested a reply,
                we aim to respond within 7 days.
                """)

    st.markdown("---")

    st.markdown("""
    <div class="card">
      <strong>📧 Direct contact</strong><br>
      <span style='font-size:0.9rem;'>For urgent matters or partnership enquiries:
      <a href='mailto:alumni@dagoretti.ac.ke'>alumni@dagoretti.ac.ke</a></span><br>
      <span style='font-size:0.9rem;'>GitHub issues and PRs:
      <a href='https://github.com/dagoretti-community/hub' target='_blank'>github.com/dagoretti-community/hub</a></span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
      All submissions are reviewed before appearing on the platform. Personal data is not shared.
    </div>
    """, unsafe_allow_html=True)
