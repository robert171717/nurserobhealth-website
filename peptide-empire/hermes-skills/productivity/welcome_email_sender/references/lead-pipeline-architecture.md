# Lead Pipeline Architecture — Sheets + Discord Layer

## Overview
Built 2026-05-13. Runs alongside `welcome_email_sender` (which handles the HTML welcome email). This layer adds Google Sheets logging and Discord notifications for every new Formspree lead.

## Data Flow
```
Formspree submission → Fastmail inbox (nurse@nurserobhealth.com)
     ↓
Lead Pipeline cron (every 30 min, job 67d985ef957a)
     ↓
himalaya envelope list → filter "New submission from Wolverine Stack Calculator Leads"
     ↓
Extract email/name → dedup against lead_tracker.json
     ↓
Google Sheets API (service account) → append row
     ↓
Hermes native Discord → alert to #hermes-private
     ↓
himalaya flag add Seen → mark processed
```

## Key Files
| File | Purpose |
|------|---------|
| `~/NurseRob_PeptideEmpire/leads/lead_tracker.json` | Processed emails + last_run timestamp |
| `~/NurseRob_PeptideEmpire/leads/welcome_sent.json` | Welcome email sent log (separate, used by welcome_email_sender) |
| `~/.hermes/gsc-service-account.json` | Service account (reused from GSC setup, used for Sheets API) |

## Google Sheet
- ID: `1dx3R7X_c9lwDvR_MQiESrEaanMogVfgsCaHRg7Uoxic`
- Tab: `Sheet1`
- Headers: Date | Email | Name | Source | Stack | Welcome Sent | Notes | Discord Alert
- Shared with: `hermes-gsc@nurserob-gsc.iam.gserviceaccount.com` (Editor)

## Sheets API — Python Pattern
```python
import json, jwt, time, requests

with open('/home/robert/.hermes/gsc-service-account.json') as f:
    sa = json.load(f)

now = int(time.time())
payload = {
    'iss': sa['client_email'],
    'scope': 'https://www.googleapis.com/auth/spreadsheets',
    'aud': sa['token_uri'],
    'exp': now + 3600, 'iat': now
}
token = jwt.encode(payload, sa['private_key'], algorithm='RS256')
r = requests.post(sa['token_uri'], data={
    'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    'assertion': token
})
access_token = r.json()['access_token']

row = [['2026-05-13', 'lead@example.com', 'Name', 'Formspree', 'Wolverine', 'Yes', 'Notes', 'Yes']]
r2 = requests.post(
    "https://sheets.googleapis.com/v4/spreadsheets/1dx3R7X_c9lwDvR_MQiESrEaanMogVfgsCaHRg7Uoxic/values/'Sheet1'!A:H:append?valueInputOption=RAW&insertDataOption=INSERT_ROWS",
    headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'},
    json={'values': row}
)
```

## Pitfalls
- **Sheets API must be enabled** on the Google Cloud project (`nurserob-gsc`). Enable at: console.cloud.google.com/apis/api/sheets.googleapis.com
- **Sheet must be shared** with the service account email (Editor permission)
- **Sheet name MUST be single-quoted in the URL**: Use `values/'Sheet1'!A:H:append` not `values/Sheet1!A:H:append`. Without quotes, the Sheets API returns 404 even when the spreadsheet exists and the SA has access. The quotes are URL-safe (no encoding needed).
- **Zapier Sheets auth is restricted** — can't create or access sheets reliably. Use direct API + service account instead
- **Welcome email is separate** — handled by welcome_email_sender cron, not this pipeline
- **Max 5 leads per run**, skip emails older than 30 min
- **Never process** nurse@nurserobhealth.com or mundellrobert84@gmail.com
