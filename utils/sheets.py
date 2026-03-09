"""
Google Sheets backend for Dagoretti Community Hub.
Uses Google Apps Script webhook — no service account or credentials file required.

HOW IT WORKS:
  The app POSTs JSON to a deployed Google Apps Script web app URL.
  The script appends each row to a named tab in your Google Sheet.
  You own the sheet — it lives in your Google Drive.

SETUP (one-time, ~8 minutes):
  1. Go to sheets.google.com → New spreadsheet → name it "Dagoretti Hub Submissions"
  2. Extensions → Apps Script → paste the script from docs/SHEETS_SETUP.md → Save
  3. Deploy → New deployment → Web app
       Execute as: Me | Who has access: Anyone
  4. Copy the Web App URL (looks like https://script.google.com/macros/s/.../exec)
  5. Streamlit Cloud → App settings → Secrets → add:
       [sheets]
       webhook_url = "https://script.google.com/macros/s/.../exec"

TABS WRITTEN (created automatically by the script):
  alumni_submissions | memory_submissions | event_proposals | corrections | feedback

FALLBACK:
  If webhook_url is not set, is_configured() returns False.
  All forms show a visible warning and email fallback — nothing is silently dropped.
"""

import datetime
import streamlit as st
import urllib.request
import urllib.parse
import json


def is_configured() -> bool:
    """True only if the Apps Script webhook URL is present in secrets."""
    try:
        url = st.secrets.get("sheets", {}).get("webhook_url", "")
        return bool(url and url.startswith("https://script.google.com"))
    except Exception:
        return False


def _webhook_url() -> str:
    return st.secrets["sheets"]["webhook_url"]


def append_row(tab_name: str, row_data: dict) -> bool:
    """
    POST row_data to the Apps Script webhook.
    tab_name becomes the sheet tab; timestamp and status are added automatically.
    Returns True on success, False on any failure.
    """
    if not is_configured():
        return False

    payload = {
        "tab": tab_name,
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "status": "pending",
        **{k: str(v) for k, v in row_data.items()},
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            _webhook_url(),
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            if body.get("status") != "ok":
                raise ValueError(f"Script returned: {body}")
        return True
    except Exception as e:
        st.error(
            f"Submission could not be saved ({e}). "
            "Please email [alumni@dagoretti.ac.ke](mailto:alumni@dagoretti.ac.ke) directly."
        )
        return False


def not_configured_banner():
    """Render a visible, honest warning when the backend is not wired up."""
    st.warning(
        "**Submissions are not yet live.** "
        "The Google Sheets backend has not been configured for this deployment. "
        "Your entry will **not** be saved. "
        "To contribute now, email "
        "[alumni@dagoretti.ac.ke](mailto:alumni@dagoretti.ac.ke) directly.",
        icon="⚠️",
    )


def success_banner(name: str = "", extra: str = "") -> None:
    msg = "✅ **Received"
    msg += f" — thank you, {name}!**" if name else "!**"
    if extra:
        msg += f" {extra}"
    else:
        msg += " Pending admin review — will appear on the platform once approved."
    st.success(msg)


def suggest_correction_button(page: str, field: str, current_value: str, key: str):
    """
    Render a compact inline 'Suggest correction' expander.
    Used on data-heavy pages next to any figure that may be stale.
    """
    with st.expander(f"✏️ Suggest a correction for this figure", expanded=False):
        correct = st.text_input("Correct value", key=f"corr_val_{key}")
        source  = st.text_input("Source URL (required)", key=f"corr_src_{key}",
                                placeholder="https://...")
        name    = st.text_input("Your name (optional)", key=f"corr_name_{key}")
        email   = st.text_input("Your email (optional)", key=f"corr_email_{key}")
        if st.button("Submit correction", key=f"corr_btn_{key}"):
            if not correct or not source:
                st.warning("Correct value and source URL are required.")
            else:
                ok = append_row("corrections", {
                    "page": page, "field": field,
                    "current_value": current_value, "correct_value": correct,
                    "source_url": source, "submitter_name": name,
                    "submitter_email": email,
                })
                if ok:
                    st.success("Correction submitted — reviewed within 48 hours.")
                elif not is_configured():
                    st.info(f"Email correction to alumni@dagoretti.ac.ke — Page: {page}, Field: {field}")
