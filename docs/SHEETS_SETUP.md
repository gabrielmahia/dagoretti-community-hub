# Google Sheets Backend Setup

Enables all form submissions to land in a Google Sheet you own,
and auto-commits approved rows to GitHub — no manual copy-paste.

**Time:** ~12 minutes | **Cost:** Free | **Data ownership:** Your Google Drive

---

## Step 1 — Create the spreadsheet

1. Go to [sheets.google.com](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it: **Dagoretti Hub Submissions**

---

## Step 2 — Add the Apps Script

1. In the spreadsheet: **Extensions → Apps Script**
2. Delete all existing code
3. Paste the entire contents of `docs/AppsScript_AutoApprove.js`
4. Save (Ctrl+S)

---

## Step 3 — Add Script Properties (your secrets)

1. In the Apps Script editor: **Project Settings** (gear ⚙️ in the left sidebar)
2. Scroll to **Script Properties → Add script property** — add all four:

| Property | Value |
|---|---|
| `GITHUB_TOKEN` | `ghp_xxxx...` (Personal Access Token, `repo` scope) |
| `GITHUB_OWNER` | `gabrielmahia` |
| `GITHUB_REPO` | `dagoretti-community-hub` |
| `GITHUB_BRANCH` | `main` |

**To create a GitHub token:**
- github.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Scopes: tick `repo` only
- Copy the token immediately — it won't show again

---

## Step 4 — Run setup once

1. In the Apps Script editor, select function: `setupTriggerAndValidation`
2. Click **Run**
3. Grant the permissions it asks for (Google Drive + Sheets + UrlFetch)
4. You should see: "✅ Setup complete."

Then run `testGitHubConnection` to confirm GitHub access works.

---

## Step 5 — Deploy as Web App (for form submissions)

1. **Deploy → New Deployment**
2. Gear ⚙️ → **Web app**
3. Set: Execute as **Me** · Who has access **Anyone**
4. Click **Deploy** → copy the URL

---

## Step 6 — Add to Streamlit Cloud secrets

1. [share.streamlit.io](https://share.streamlit.io) → your app → ⋮ → Settings → Secrets
2. Paste:

```toml
[sheets]
webhook_url = "https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec"
```

---

## Admin workflow (ongoing)

Submissions arrive in the Sheet with status `pending` (yellow).

To approve:
1. Open **Dagoretti Hub Submissions**
2. Go to the relevant tab
3. Click the status cell dropdown → select **approved** (green)
4. Done — the row is automatically committed to GitHub and Streamlit redeploys in ~60 seconds

To reject: select **rejected** (red) — row stays in Sheet, nothing written to GitHub.

### Tab → CSV routing

| Sheet tab | GitHub file | Notes |
|---|---|---|
| `alumni_submissions` | `data/alumni.csv` | lat/lon auto-geocoded by app |
| `memory_submissions` | `data/memories.csv` | Appears on Memory Wall |
| `event_proposals` | `data/events.csv` | Appears on Events board |
| `corrections` | — | Marked done, no CSV write |
| `feedback` | — | Marked done, no CSV write |

---

## If something goes wrong

- Status cell gets a **note** showing what happened (hover to read)
- If GitHub write fails, you get an alert in the Sheet
- Manual fallback: copy the row yourself into the CSV and push

## Refresh dropdowns

If dropdowns disappear on new rows, run `refreshAllValidation` from the editor.
