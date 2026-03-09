/**
 * Dagoretti Community Hub — Google Sheets Auto-Approve Script
 * ============================================================
 * VERSION: 2.0
 *
 * WHAT THIS DOES:
 *   1. Adds a status dropdown (pending / approved / rejected) to every
 *      submission tab automatically when new rows arrive.
 *   2. When you change any status cell to "approved", it writes the row
 *      to the correct CSV in the GitHub repo and commits — no manual
 *      copy-paste, no terminal.
 *   3. Streamlit Cloud auto-redeploys on every commit (~60 seconds).
 *
 * TAB → CSV ROUTING:
 *   alumni_submissions   → data/alumni.csv
 *   memory_submissions   → data/memories.csv
 *   event_proposals      → data/events.csv
 *   corrections          → (no CSV — marked done only)
 *   feedback             → (no CSV — marked done only)
 *
 * ONE-TIME SETUP (do this once, then forget it):
 *   1. Open Extensions → Apps Script
 *   2. Paste this entire file, replacing all existing code
 *   3. Click the gear ⚙️ → Script Properties → Add the following:
 *        GITHUB_TOKEN   = ghp_xxxxxxxxxxxxxxxxxxxx   (repo scope)
 *        GITHUB_OWNER   = gabrielmahia
 *        GITHUB_REPO    = dagoretti-community-hub
 *        GITHUB_BRANCH  = main
 *   4. Save (Ctrl+S)
 *   5. Run setupTriggerAndValidation() ONCE from the editor
 *      (Run menu → Run function → setupTriggerAndValidation)
 *      Grant permissions when prompted.
 *   6. Done. Never need to touch this script again.
 *
 * SECURITY:
 *   - GitHub token lives in Script Properties only — never in code
 *   - Token needs only "repo" scope (Contents: read/write)
 *   - Revoke/rotate at github.com/settings/tokens any time
 */


// ─── Configuration ────────────────────────────────────────────────────────────

var STATUS_COL_NAME   = "status";
var STATUS_OPTIONS    = ["pending", "approved", "rejected"];
var STATUS_COLORS     = { pending: "#fff9c4", approved: "#c8e6c9", rejected: "#ffcdd2" };

// Sheet tab → { csvPath, columnMap }
// columnMap: { csv_column: sheet_column_header }
// Columns not in map are excluded from the CSV write.
var ROUTING = {

  alumni_submissions: {
    csvPath: "data/alumni.csv",
    columnMap: {
      name:        "full_name",
      year:        "year_left",
      industry:    "industry",
      role:        "role",
      city:        "city",
      country:     "country",
      lat:         null,          // left blank — app geocodes automatically
      lon:         null,          // left blank — app geocodes automatically
      email_public: null,         // never public
      linkedin:    "linkedin_url",
      mentoring:   "mentoring",
      bio_short:   "bio",
    },
  },

  memory_submissions: {
    csvPath: "data/memories.csv",
    columnMap: {
      name:               "name",
      year_at_dagoretti:  "year_at_dagoretti",
      submission_type:    "submission_type",
      body:               "body",
      status:             null,   // filled with "approved"
    },
  },

  event_proposals: {
    csvPath: "data/events.csv",
    columnMap: {
      id:          null,          // auto-generated (timestamp-based)
      title:       "event_title",
      date:        "proposed_date",
      time:        null,          // not collected in form — leave blank
      type:        "event_type",
      location:    "location",
      is_virtual:  null,          // not collected — leave blank
      description: "description",
      organiser:   "proposer_name",
      link:        null,          // admin can add later
      featured:    null,          // admin decision
      status:      null,          // filled with "approved"
    },
  },

};


// ─── Entry point: onEdit trigger ──────────────────────────────────────────────

/**
 * Called automatically on every cell edit.
 * Only acts when: edited cell is in the status column AND value is "approved".
 */
function onEditTrigger(e) {
  try {
    var sheet = e.range.getSheet();
    var tabName = sheet.getName();

    // Only act on known submission tabs
    if (!ROUTING[tabName] && tabName !== "corrections" && tabName !== "feedback") return;

    var editedRow = e.range.getRow();
    var editedCol = e.range.getColumn();
    var newValue  = e.value;

    // Find which column is "status"
    var headers    = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    var statusColIdx = headers.indexOf(STATUS_COL_NAME);
    if (statusColIdx === -1) return;

    // Only proceed if this edit is in the status column and value is "approved"
    if (editedCol !== statusColIdx + 1) return;
    if (newValue !== "approved") {
      _colorStatusCell(e.range, newValue);
      return;
    }

    _colorStatusCell(e.range, newValue);

    // corrections and feedback: just color and mark done — no CSV write
    if (!ROUTING[tabName]) {
      sheet.getRange(editedRow, editedCol).setNote("Reviewed " + new Date().toISOString());
      return;
    }

    // Get the full row data
    var rowData = sheet.getRange(editedRow, 1, 1, sheet.getLastColumn()).getValues()[0];
    var rowObj  = {};
    headers.forEach(function(h, i) { rowObj[h] = rowData[i]; });

    // Write to GitHub
    var result = _writeToGitHub(tabName, rowObj);
    if (result.success) {
      sheet.getRange(editedRow, editedCol).setNote(
        "Auto-committed to GitHub\n" + result.commitUrl + "\n" + new Date().toISOString()
      );
    } else {
      sheet.getRange(editedRow, editedCol).setNote(
        "⚠️ GitHub write failed: " + result.error + "\n" + new Date().toISOString()
      );
      SpreadsheetApp.getUi().alert(
        "GitHub write failed for row " + editedRow + ":\n" + result.error
      );
    }

  } catch (err) {
    Logger.log("onEditTrigger error: " + err.toString());
  }
}


// ─── GitHub write ─────────────────────────────────────────────────────────────

function _writeToGitHub(tabName, rowObj) {
  var props  = PropertiesService.getScriptProperties();
  var token  = props.getProperty("GITHUB_TOKEN");
  var owner  = props.getProperty("GITHUB_OWNER");
  var repo   = props.getProperty("GITHUB_REPO");
  var branch = props.getProperty("GITHUB_BRANCH") || "main";

  if (!token || !owner || !repo) {
    return { success: false, error: "Script Properties not configured (GITHUB_TOKEN / GITHUB_OWNER / GITHUB_REPO)" };
  }

  var route   = ROUTING[tabName];
  var csvPath = route.csvPath;
  var colMap  = route.columnMap;

  // ── 1. GET current file from GitHub ───────────────────────────────────────
  var apiBase = "https://api.github.com/repos/" + owner + "/" + repo + "/contents/" + csvPath;
  var getResp = UrlFetchApp.fetch(
    apiBase + "?ref=" + branch,
    { headers: { Authorization: "token " + token, Accept: "application/vnd.github.v3+json" },
      muteHttpExceptions: true }
  );

  if (getResp.getResponseCode() !== 200) {
    return { success: false, error: "GitHub GET failed: " + getResp.getContentText().substring(0, 200) };
  }

  var fileData    = JSON.parse(getResp.getContentText());
  var sha         = fileData.sha;
  var currentCsv  = Utilities.newBlob(Utilities.base64Decode(fileData.content.replace(/\n/g, ""))).getDataAsString();

  // ── 2. Build new CSV row ───────────────────────────────────────────────────
  var csvLines  = currentCsv.trimEnd().split("\n");
  var csvHeader = csvLines[0].replace(/"/g, "").split(",");  // strip quotes from header

  // Build the new row using columnMap
  var newRow = csvHeader.map(function(col) {
    var sheetCol = colMap[col];

    // Explicit null in map → computed or blank
    if (sheetCol === null) {
      if (col === "id") {
        return '"event_' + new Date().getTime() + '"';
      }
      if (col === "status") {
        return '"approved"';
      }
      return '""';
    }

    // Look up value from row object
    var val = rowObj[sheetCol] !== undefined ? rowObj[sheetCol] : "";
    if (val === null || val === undefined) val = "";
    // Escape quotes and wrap in quotes
    return '"' + String(val).replace(/"/g, '""') + '"';
  });

  csvLines.push(newRow.join(","));
  var newCsv = csvLines.join("\n") + "\n";

  // ── 3. PUT updated file ────────────────────────────────────────────────────
  var commitMsg = "auto: approve " + tabName.replace("_submissions","").replace("_"," ") +
    " — " + (rowObj["full_name"] || rowObj["name"] || rowObj["event_title"] || "entry") +
    " [via Sheets]";

  var putPayload = JSON.stringify({
    message: commitMsg,
    content: Utilities.base64Encode(Utilities.newBlob(newCsv).getBytes()),
    sha:     sha,
    branch:  branch,
  });

  var putResp = UrlFetchApp.fetch(apiBase, {
    method:  "PUT",
    headers: { Authorization: "token " + token, Accept: "application/vnd.github.v3+json",
               "Content-Type": "application/json" },
    payload: putPayload,
    muteHttpExceptions: true,
  });

  if (putResp.getResponseCode() !== 200 && putResp.getResponseCode() !== 201) {
    return { success: false, error: "GitHub PUT failed (" + putResp.getResponseCode() + "): " +
             putResp.getContentText().substring(0, 200) };
  }

  var putData   = JSON.parse(putResp.getContentText());
  var commitUrl = putData.commit ? putData.commit.html_url : "committed";
  return { success: true, commitUrl: commitUrl };
}


// ─── Dropdown validation ──────────────────────────────────────────────────────

/**
 * Apply status dropdown to the status column of a given sheet.
 * Called once per tab on setup, and again whenever a new row is added.
 */
function _applyStatusValidation(sheet) {
  if (sheet.getLastColumn() === 0) return;  // empty sheet — no columns yet
  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var statusColIdx = headers.indexOf(STATUS_COL_NAME);
  if (statusColIdx === -1) return;

  var lastRow = Math.max(sheet.getLastRow(), 2);
  var range   = sheet.getRange(2, statusColIdx + 1, lastRow - 1, 1);

  var rule = SpreadsheetApp.newDataValidation()
    .requireValueInList(STATUS_OPTIONS, true)
    .setAllowInvalid(false)
    .build();

  range.setDataValidation(rule);

  // Color existing cells
  for (var r = 2; r <= lastRow; r++) {
    var cell = sheet.getRange(r, statusColIdx + 1);
    _colorStatusCell(cell, cell.getValue());
  }
}

function _colorStatusCell(cell, value) {
  var color = STATUS_COLORS[value] || "#ffffff";
  cell.setBackground(color);
}

/**
 * Re-apply dropdowns to all known tabs.
 * Run this manually if you add new rows and want dropdowns extended.
 */
function refreshAllValidation() {
  var ss   = SpreadsheetApp.getActiveSpreadsheet();
  var tabs = Object.keys(ROUTING).concat(["corrections", "feedback"]);
  tabs.forEach(function(name) {
    var sheet = ss.getSheetByName(name);
    if (sheet) _applyStatusValidation(sheet);
  });
  SpreadsheetApp.getUi().alert("Dropdowns refreshed on all tabs.");
}


// ─── One-time setup ───────────────────────────────────────────────────────────

/**
 * RUN THIS ONCE after pasting the script.
 * Sets up the onEdit installable trigger and applies dropdowns to all tabs.
 */
function setupTriggerAndValidation() {
  // Remove any existing onEdit triggers to avoid duplicates
  var triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(function(t) {
    if (t.getHandlerFunction() === "onEditTrigger") {
      ScriptApp.deleteTrigger(t);
    }
  });

  // Install fresh trigger
  ScriptApp.newTrigger("onEditTrigger")
    .forSpreadsheet(SpreadsheetApp.getActive())
    .onEdit()
    .create();

  // Apply dropdowns to all existing tabs
  refreshAllValidation();

  SpreadsheetApp.getUi().alert(
    "✅ Setup complete.\n\n" +
    "onEdit trigger installed.\n" +
    "Status dropdowns applied to all tabs.\n\n" +
    "Make sure you have added these Script Properties:\n" +
    "  GITHUB_TOKEN\n  GITHUB_OWNER\n  GITHUB_REPO\n  GITHUB_BRANCH"
  );
}


// ─── Existing doPost (unchanged — keeps form submissions working) ─────────────

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var ss   = SpreadsheetApp.getActiveSpreadsheet();

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

    // Apply dropdown to the new row
    _applyStatusValidation(sheet);

    return ContentService
      .createTextOutput(JSON.stringify({ status: "ok" }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: "error", message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}


// ─── Test helpers ─────────────────────────────────────────────────────────────

/**
 * Test GitHub connectivity without touching real data.
 * Run from the editor to verify your token and repo are configured correctly.
 */
function testGitHubConnection() {
  var props = PropertiesService.getScriptProperties();
  var token = props.getProperty("GITHUB_TOKEN");
  var owner = props.getProperty("GITHUB_OWNER");
  var repo  = props.getProperty("GITHUB_REPO");

  if (!token || !owner || !repo) {
    SpreadsheetApp.getUi().alert("❌ Script Properties missing. Add GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO.");
    return;
  }

  var resp = UrlFetchApp.fetch(
    "https://api.github.com/repos/" + owner + "/" + repo,
    { headers: { Authorization: "token " + token }, muteHttpExceptions: true }
  );

  if (resp.getResponseCode() === 200) {
    SpreadsheetApp.getUi().alert("✅ GitHub connection OK — repo accessible.");
  } else {
    SpreadsheetApp.getUi().alert("❌ GitHub connection failed (" + resp.getResponseCode() + "):\n" +
      resp.getContentText().substring(0, 300));
  }
}
