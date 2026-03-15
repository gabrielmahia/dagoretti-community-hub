/**
 * Dagoretti Community Hub — Google Sheets Auto-Approve Script
 * ============================================================
 * VERSION: 2.2  (2026-03 — wrap all getUi() calls in try/catch for editor compat)
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
 *      Success message appears in View → Logs (not a popup — this is normal).
 *   6. IF your sheet has rows submitted before the dorm field existed, run
 *      repairDormAlignment() ONCE to fix any misaligned values in the sheet.
 *      Check View → Logs to confirm which rows were corrected.
 *   7. Done. Never need to touch this script again.
 *
 * SECURITY:
 *   - GitHub token lives in Script Properties only — never in code
 *   - Token needs only "repo" scope (Contents: read/write)
 *   - Revoke/rotate at github.com/settings/tokens any time
 */


// ─── Helpers ──────────────────────────────────────────────────────────────────

/**
 * Safe alert: shows a popup when triggered from the sheet UI,
 * falls back to Logger.log when run directly from the editor.
 * getUi() throws outside a UI context — this prevents that crash.
 */
function _alert(msg) {
  try {
    SpreadsheetApp.getUi().alert(msg);
  } catch (e) {
    Logger.log(msg);
  }
}


// ─── Configuration ────────────────────────────────────────────────────────────

var STATUS_COL_NAME = "status";
var STATUS_OPTIONS  = ["pending", "approved", "rejected"];
var STATUS_COLORS   = { pending: "#fff9c4", approved: "#c8e6c9", rejected: "#ffcdd2" };

// Sheet tab → { csvPath, columnMap }
// columnMap: { csv_column: sheet_column_header }
// Columns not in map are excluded from the CSV write.
var ROUTING = {

  alumni_submissions: {
    csvPath: "data/alumni.csv",
    columnMap: {
      name:         "full_name",
      year:         "year_left",
      industry:     "industry",
      role:         "role",
      city:         "city",
      country:      "country",
      lat:          null,          // left blank — app geocodes automatically
      lon:          null,          // left blank — app geocodes automatically
      email_public: null,          // never public
      linkedin:     "linkedin_url",
      mentoring:    "mentoring",
      dorm:         "dorm",
      bio_short:    "bio",
    },
  },

  memory_submissions: {
    csvPath: "data/memories.csv",
    columnMap: {
      name:              "name",
      year_at_dagoretti: "year_at_dagoretti",
      submission_type:   "submission_type",
      body:              "body",
      status:            null,     // filled with "approved"
    },
  },

  kcse_submissions: {
    csvPath: "data/kcse_results.csv",
    columnMap: {
      year:        "year",
      mean_grade:  "mean_score",
      a_plain:     null,
      a_minus:     null,
      b_plus:      null,
      b_plain:     null,
      b_minus:     null,
      c_plus:      null,
      c_plain:     null,
      c_minus:     null,
      d_plus:      null,
      d_plain:     null,
      d_minus:     null,
      e:           null,
      candidates:  "candidates",
      top_student: "top_student",
      top_grade:   "top_grade",
      verified:    null,           // always "confirmed" on approve
      source:      "source_url",
    },
  },

  event_proposals: {
    csvPath: "data/events.csv",
    columnMap: {
      id:          null,           // auto-generated (timestamp-based)
      title:       "event_title",
      date:        "proposed_date",
      time:        null,           // not collected in form — leave blank
      type:        "event_type",
      location:    "location",
      is_virtual:  null,           // not collected — leave blank
      description: "description",
      organiser:   "proposer_name",
      link:        null,           // admin can add later
      featured:    null,           // admin decision
      status:      null,           // filled with "approved"
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
    var sheet   = e.range.getSheet();
    var tabName = sheet.getName();

    // Only act on known submission tabs
    if (!ROUTING[tabName] && tabName !== "corrections" && tabName !== "feedback") return;

    var editedRow = e.range.getRow();
    var editedCol = e.range.getColumn();
    var newValue  = e.value;

    // Find which column is "status"
    var headers      = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    var statusColIdx = headers.indexOf(STATUS_COL_NAME);
    if (statusColIdx === -1) return;

    // Only proceed if this edit is in the status column
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

    // Get the full row data as a named object
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
      _alert("GitHub write failed for row " + editedRow + ":\n" + result.error);
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

  var fileData   = JSON.parse(getResp.getContentText());
  var sha        = fileData.sha;
  var currentCsv = Utilities.newBlob(
    Utilities.base64Decode(fileData.content.replace(/\n/g, ""))
  ).getDataAsString();

  // ── 2. Build new CSV row ───────────────────────────────────────────────────
  var csvLines  = currentCsv.trimEnd().split("\n");
  var csvHeader = csvLines[0].replace(/"/g, "").split(",");

  var newRow = csvHeader.map(function(col) {
    var sheetCol = colMap[col];

    if (sheetCol === null) {
      if (col === "id")     return '"event_' + new Date().getTime() + '"';
      if (col === "status") return '"approved"';
      return '""';
    }

    var val = rowObj[sheetCol] !== undefined ? rowObj[sheetCol] : "";
    if (val === null || val === undefined) val = "";
    return '"' + String(val).replace(/"/g, '""') + '"';
  });

  csvLines.push(newRow.join(","));
  var newCsv = csvLines.join("\n") + "\n";

  // ── 3. PUT updated file ────────────────────────────────────────────────────
  var commitMsg = "auto: approve " +
    tabName.replace("_submissions", "").replace("_", " ") +
    " — " +
    (rowObj["full_name"] || rowObj["name"] || rowObj["event_title"] || "entry") +
    " [via Sheets]";

  var putPayload = JSON.stringify({
    message: commitMsg,
    content: Utilities.base64Encode(Utilities.newBlob(newCsv).getBytes()),
    sha:     sha,
    branch:  branch,
  });

  var putResp = UrlFetchApp.fetch(apiBase, {
    method:  "PUT",
    headers: {
      Authorization:  "token " + token,
      Accept:         "application/vnd.github.v3+json",
      "Content-Type": "application/json",
    },
    payload:            putPayload,
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

function _applyStatusValidation(sheet) {
  if (sheet.getLastColumn() === 0) return;
  var headers      = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var statusColIdx = headers.indexOf(STATUS_COL_NAME);
  if (statusColIdx === -1) return;

  var lastRow = Math.max(sheet.getLastRow(), 2);
  var range   = sheet.getRange(2, statusColIdx + 1, lastRow - 1, 1);

  var rule = SpreadsheetApp.newDataValidation()
    .requireValueInList(STATUS_OPTIONS, true)
    .setAllowInvalid(false)
    .build();

  range.setDataValidation(rule);

  for (var r = 2; r <= lastRow; r++) {
    var cell = sheet.getRange(r, statusColIdx + 1);
    _colorStatusCell(cell, cell.getValue());
  }
}

function _colorStatusCell(cell, value) {
  cell.setBackground(STATUS_COLORS[value] || "#ffffff");
}

function refreshAllValidation() {
  var ss   = SpreadsheetApp.getActiveSpreadsheet();
  var tabs = Object.keys(ROUTING).concat(["corrections", "feedback"]);
  tabs.forEach(function(name) {
    var sheet = ss.getSheetByName(name);
    if (sheet) _applyStatusValidation(sheet);
  });
  _alert("Dropdowns refreshed on all tabs.");
}


// ─── One-time setup ───────────────────────────────────────────────────────────

/**
 * RUN THIS ONCE after pasting the script.
 * Sets up the onEdit installable trigger and applies dropdowns to all tabs.
 * Success message appears in View → Logs when run from the editor.
 */
function setupTriggerAndValidation() {
  // Remove any existing onEdit triggers to avoid duplicates
  ScriptApp.getProjectTriggers().forEach(function(t) {
    if (t.getHandlerFunction() === "onEditTrigger") ScriptApp.deleteTrigger(t);
  });

  // Install fresh trigger
  ScriptApp.newTrigger("onEditTrigger")
    .forSpreadsheet(SpreadsheetApp.getActive())
    .onEdit()
    .create();

  // Apply dropdowns to all existing tabs
  refreshAllValidation();

  _alert(
    "✅ Setup complete.\n\n" +
    "onEdit trigger installed.\n" +
    "Status dropdowns applied to all tabs.\n\n" +
    "Make sure Script Properties are set:\n" +
    "  GITHUB_TOKEN\n  GITHUB_OWNER\n  GITHUB_REPO\n  GITHUB_BRANCH"
  );
}


// ─── doPost — receives Streamlit form submissions ─────────────────────────────
//
// BUG FIXED (v2.1): old version used appendRow(Object.values(data)) which wrote
// values in payload key order. If the sheet existed before a new field (e.g. "dorm")
// was added to the form, values landed in wrong columns.
//
// Fix: read existing headers, auto-add missing columns, write each value by name.

function doPost(e) {
  try {
    var data    = JSON.parse(e.postData.contents);
    var ss      = SpreadsheetApp.getActiveSpreadsheet();
    var tabName = data.tab || "submissions";
    delete data.tab;

    var sheet = ss.getSheetByName(tabName);
    if (!sheet) sheet = ss.insertSheet(tabName);

    var keys    = Object.keys(data);
    var headers;

    if (sheet.getLastRow() === 0) {
      sheet.appendRow(keys);
      headers = keys;
    } else {
      headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];

      // Auto-add any payload keys missing from the header row
      keys.forEach(function(key) {
        if (headers.indexOf(key) === -1) {
          sheet.getRange(1, headers.length + 1).setValue(key);
          headers.push(key);
        }
      });
    }

    // Write values into their correct named columns
    var row = headers.map(function(h) {
      return data.hasOwnProperty(h) ? data[h] : "";
    });
    sheet.appendRow(row);

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
 * Verify GitHub token and repo access without touching any data.
 * Run from the editor — result appears in View → Logs.
 */
function testGitHubConnection() {
  var props = PropertiesService.getScriptProperties();
  var token = props.getProperty("GITHUB_TOKEN");
  var owner = props.getProperty("GITHUB_OWNER");
  var repo  = props.getProperty("GITHUB_REPO");

  if (!token || !owner || !repo) {
    _alert("❌ Script Properties missing. Add GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO.");
    return;
  }

  var resp = UrlFetchApp.fetch(
    "https://api.github.com/repos/" + owner + "/" + repo,
    { headers: { Authorization: "token " + token }, muteHttpExceptions: true }
  );

  if (resp.getResponseCode() === 200) {
    _alert("✅ GitHub connection OK — repo accessible.");
  } else {
    _alert("❌ GitHub connection failed (" + resp.getResponseCode() + "):\n" +
      resp.getContentText().substring(0, 300));
  }
}


/**
 * REPAIR UTILITY — run once to fix rows misaligned by the old doPost bug.
 *
 * Symptoms: dorm column contains bio text, bio column contains email,
 * email_admin column is blank. Caused by old positional appendRow() call
 * on sheets that existed before the dorm field was added to the form.
 *
 * HOW TO RUN:
 *   1. Select repairDormAlignment from the function dropdown
 *   2. Click Run
 *   3. View → Logs — lists every row touched
 *   4. Spot-check 2–3 rows in the sheet to confirm dorm and bio are correct
 *
 * SAFE TO RE-RUN: checks before shifting, won't double-shift.
 */
function repairDormAlignment() {
  var ss    = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("alumni_submissions");

  if (!sheet) {
    Logger.log("alumni_submissions tab not found — nothing to repair.");
    return;
  }

  var lastRow = sheet.getLastRow();
  var lastCol = sheet.getLastColumn();

  if (lastRow < 2) {
    Logger.log("No data rows found.");
    return;
  }

  var headers  = sheet.getRange(1, 1, 1, lastCol).getValues()[0];
  var dormIdx  = headers.indexOf("dorm");
  var bioIdx   = headers.indexOf("bio");
  var emailIdx = headers.indexOf("email_admin");

  if (dormIdx === -1 || bioIdx === -1) {
    Logger.log("Could not find dorm or bio column. Headers: " + headers.join(", "));
    return;
  }

  var repaired = 0;

  for (var r = 2; r <= lastRow; r++) {
    var row     = sheet.getRange(r, 1, 1, lastCol).getValues()[0];
    var dormVal = String(row[dormIdx] || "").trim();
    var bioVal  = String(row[bioIdx]  || "").trim();

    // Flag rows where the dorm cell looks like bio text (too long / not a known dorm name)
    var looksLikeBio =
      dormVal.length > 30 ||
      (dormVal.length > 0 &&
       dormVal.indexOf("Senior Dorm") === -1 &&
       dormVal.indexOf("Siberia")     === -1 &&
       dormVal.indexOf("Constra")     === -1 &&
       dormVal.indexOf("Mara")        === -1 &&
       dormVal.indexOf("Day")         === -1 &&
       dormVal.indexOf("Other")       === -1 &&
       bioVal === "");

    if (looksLikeBio) {
      var bioFromDorm  = row[dormIdx];
      var emailFromBio = row[bioIdx];

      row[dormIdx] = "";           // dorm was not submitted with this row
      row[bioIdx]  = bioFromDorm; // bio text belongs in bio column
      if (emailIdx !== -1) row[emailIdx] = emailFromBio;

      sheet.getRange(r, 1, 1, lastCol).setValues([row]);
      Logger.log("Repaired row " + r + ": moved '" + bioFromDorm.substring(0, 40) + "...' to bio column");
      repaired++;
    }
  }

  Logger.log("Done. " + repaired + " row(s) repaired out of " + (lastRow - 1) + " data rows.");
  _alert("Repair complete.\n" + repaired + " row(s) corrected.\nSee View → Logs for details.");
}
