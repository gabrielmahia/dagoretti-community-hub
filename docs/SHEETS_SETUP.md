# Google Sheets Backend Setup

Enables all form submissions (alumni profiles, memories, event proposals,
data corrections, general feedback) to persist in a Google Sheet you own.

**Time:** ~8 minutes | **Cost:** Free | **Data ownership:** Your Google Drive

---

## Step 1 — Create the spreadsheet

1. Go to [sheets.google.com](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it exactly: **Dagoretti Hub Submissions**

---

## Step 2 — Add the Apps Script

1. In the spreadsheet: **Extensions → Apps Script**
2. Delete all existing code, paste the following:

```javascript
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.getActiveSpreadsheet();

    var tabName = data.tab || "submissions";
    delete data.tab;

    var sheet = ss.getSheetByName(tabName);
    if (!sheet) {
      sheet = ss.insertSheet(tabName);
    }

    if (sheet.getLastRow() === 0) {
      sheet.appendRow(Object.keys(data));
    }
    sheet.appendRow(Object.values(data));

    return ContentService
      .createTextOutput(JSON.stringify({ status: "ok" }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: "error", message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Run this once manually to verify the script works
function testConnection() {
  var e = { postData: { contents: JSON.stringify({
    tab: "test", timestamp: new Date().toISOString(), message: "connection OK"
  })}};
  Logger.log(doPost(e).getContent());
}
```

3. Click **Save** (Ctrl+S)
4. Run `testConnection` once to verify — check the Logs panel

---

## Step 3 — Deploy as Web App

1. Click **Deploy → New Deployment**
2. Click the gear ⚙️ next to "Select type" → **Web app**
3. Set:
   - **Execute as:** Me
   - **Who has access:** Anyone
4. Click **Deploy** → **Authorise** (grant the permissions it asks for)
5. Copy the **Web App URL** — it looks like:
   `https://script.google.com/macros/s/AKfycb.../exec`

---

## Step 4 — Add to Streamlit Cloud secrets

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Find **dagoretti-community-hub** → **⋮ → Settings → Secrets**
3. Paste:

```toml
[sheets]
webhook_url = "https://script.google.com/macros/s/YOUR_SCRIPT_ID_HERE/exec"
```

4. Click **Save** — the app restarts automatically

---

## What gets created automatically

| Tab name | Contents |
|---|---|
| `alumni_submissions` | Alumni profile forms |
| `memory_submissions` | Memory Wall submissions |
| `event_proposals` | Event proposals |
| `corrections` | Data correction requests |
| `feedback` | General feedback |

Each row has: `timestamp`, `status` (pending/approved/rejected), and all form fields.

---

## Admin workflow

1. Open **Dagoretti Hub Submissions** in Google Sheets
2. Review each `pending` row
3. Change `status` to `approved` or `rejected`
4. For `alumni_submissions`: copy approved rows into `data/alumni.csv` in the repo
5. For `memory_submissions`: approved rows appear live on the Memory Wall automatically
   (the app re-reads the sheet every 5 minutes)

---

## Redeployment note

If you edit the Apps Script, you **must** create a **new deployment** — editing
an existing deployment does not update the live URL behaviour.
