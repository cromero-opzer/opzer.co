import os
import json
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from google.oauth2 import service_account
from googleapiclient.discovery import build
from pyairtable import Api

# ── Configuration (loaded from environment variables) ────────────────────────
GOOGLE_SERVICE_ACCOUNT_JSON = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
AIRTABLE_API_KEY            = os.environ["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID            = os.getenv("AIRTABLE_BASE_ID", "appWqNuh7ntCBc0Tj")
AIRTABLE_TABLE_ID           = os.getenv("AIRTABLE_TABLE_ID", "tblMEHXkOoN5V7N7Z")
GMAIL_USER                  = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD          = os.environ["GMAIL_APP_PASSWORD"]
NOTIFICATION_EMAIL          = os.getenv("NOTIFICATION_EMAIL", os.environ["GMAIL_USER"])

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

MIME_LABELS = {
    "application/vnd.google-apps.document":     "Google Doc",
    "application/vnd.google-apps.spreadsheet":  "Google Sheet",
    "application/vnd.google-apps.presentation": "Google Slides",
    "application/vnd.google-apps.folder":       "Folder",
    "application/pdf":                          "PDF",
    "image/jpeg":                               "JPEG Image",
    "image/png":                                "PNG Image",
    "video/mp4":                                "MP4 Video",
    "text/plain":                               "Text File",
    "text/csv":                                 "CSV",
}


def get_drive_service():
    info = json.loads(GOOGLE_SERVICE_ACCOUNT_JSON)
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def fetch_new_files(service):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    cutoff_str = cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")
    query = f"createdTime > '{cutoff_str}' and trashed = false"
    response = service.files().list(
        q=query,
        fields="files(id, name, mimeType, createdTime, webViewLink)",
        orderBy="createdTime desc",
        pageSize=100,
    ).execute()
    return response.get("files", [])


def mime_to_label(mime_type):
    return MIME_LABELS.get(mime_type, mime_type)


def log_to_airtable(files):
    api = Api(AIRTABLE_API_KEY)
    table = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID)
    records = [
        {
            "File Name":  f["name"],
            "File Type":  mime_to_label(f.get("mimeType", "")),
            "Date Added": f.get("createdTime", "")[:10],
            "Drive Link": f.get("webViewLink", ""),
            "Notified":   True,
        }
        for f in files
    ]
    if records:
        table.batch_create(records)
    return len(records)


def send_email_notification(files):
    subject = f"Drive Sync: {len(files)} new file(s) added in the last 24 hours"
    lines = ["The following new files were detected in Google Drive:\n"]
    for f in files:
        lines.append(f"• {f['name']}  ({mime_to_label(f.get('mimeType', ''))})")
        lines.append(f"  Added: {f.get('createdTime', '')[:19].replace('T', ' ')} UTC")
        lines.append(f"  Link:  {f.get('webViewLink', 'N/A')}\n")
    body = "\n".join(lines)

    msg = MIMEMultipart()
    msg["From"]    = GMAIL_USER
    msg["To"]      = NOTIFICATION_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, NOTIFICATION_EMAIL, msg.as_string())
    print(f"Email notification sent to {NOTIFICATION_EMAIL}")


def main():
    print("Checking Google Drive for new files in the last 24 hours...")
    service = get_drive_service()
    files = fetch_new_files(service)

    if not files:
        print("No new files found. Nothing to log or notify.")
        return

    print(f"Found {len(files)} new file(s):")
    for f in files:
        print(f"  - {f['name']}  ({mime_to_label(f.get('mimeType', ''))})")

    logged = log_to_airtable(files)
    print(f"Logged {logged} record(s) to Airtable (base={AIRTABLE_BASE_ID}, table={AIRTABLE_TABLE_ID}).")

    send_email_notification(files)


if __name__ == "__main__":
    main()
