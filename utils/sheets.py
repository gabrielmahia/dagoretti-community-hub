"""
Google Sheets backend for Dagoretti Community Hub.
Uses Google Apps Script webhook — no service account required.

SETUP: docs/SHEETS_SETUP.md
Streamlit Cloud secrets:
  [sheets]
  webhook_url = "https://script.google.com/macros/s/.../exec"
"""

import datetime
import json
import urllib.request
import streamlit as st


def is_configured() -> bool:
    try:
        url = st.secrets.get("sheets", {}).get("webhook_url", "")
        return bool(url and url.startswith("https://script.google.com"))
    except Exception:
        return False


def _endpoint() -> str:
    return st.secrets["sheets"]["webhook_url"]


def append_row(tab_name: str, row_data: dict) -> bool:
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
            _endpoint(), data=data,
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
    msg += f" {extra}" if extra else " Pending admin review — will appear on the platform once approved."
    st.success(msg)


def suggest_correction_button(page: str, field: str, current_value: str, key: str):
    with st.expander("✏️ Suggest a correction for this figure", expanded=False):
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
