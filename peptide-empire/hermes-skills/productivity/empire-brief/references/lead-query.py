"""Query the Nurse Rob lead tracker Google Sheet via service account.
Usage: python3 /path/to/lead-query.py
Output: JSON with total_rows, header, and recent_rows (last 20).
"""
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

SHEET_ID = "1dx3R7X_c9lwDvR_MQiESrEaanMogVfgsCaHRg7Uoxic"
SA_PATHS = [
    "/home/robert/.hermes/gsc-service-account.json",
    "/home/robert/NurseRob_PeptideEmpire/gsc-service-account.json",
    "/home/robert/gsc-service-account.json",
]


def find_sa_file():
    import os
    for p in SA_PATHS:
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"No service account file found in {SA_PATHS}")


def main():
    sa_file = find_sa_file()
    creds = service_account.Credentials.from_service_account_file(
        sa_file, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    service = build("sheets", "v4", credentials=creds)

    result = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range="Sheet1!A:Z"
    ).execute()
    values = result.get("values", [])

    total = len(values)
    header = values[0] if values else []
    rows = values[-20:] if len(values) > 20 else values

    output = {
        "total_rows": total,
        "header": header,
        "recent_rows": rows,
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
