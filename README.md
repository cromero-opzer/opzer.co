# Drive → Airtable Notifier

Automatically checks Google Drive for new files added in the last 24 hours, logs them to Airtable, and sends a Gmail summary notification. Runs daily at 9 AM EST via GitHub Actions and can also be triggered manually.

---

## How It Works

1. The script authenticates to Google Drive using a **service account**.
2. It queries Drive for any files created in the last 24 hours.
3. Each file (name, type, date, link) is written as a new record to an **Airtable** table.
4. A summary email is sent via **Gmail SMTP** using an app password.

---

## Setup Instructions

### 1. Google Drive API — Service Account Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/) and create or select a project.
2. Enable the **Google Drive API** for the project.
3. Navigate to **IAM & Admin → Service Accounts** and click **Create Service Account**.
4. Give it a name (e.g. `drive-notifier`) and click **Done**.
5. Open the new service account, go to the **Keys** tab, click **Add Key → Create new key → JSON**.
6. Download the JSON file — this is your `GOOGLE_SERVICE_ACCOUNT_JSON` credential.
7. Share any Drive folders/files you want monitored with the service account's email address (shown in the JSON as `client_email`) — grant **Viewer** access.

> The script searches all files the service account has access to that were created in the last 24 hours.

---

### 2. Airtable API Key

1. Go to [Airtable account settings](https://airtable.com/account) → **Developer Hub → Personal access tokens**.
2. Create a new token with scopes: `data.records:write` and `data.records:read`.
3. Grant access to the base `appWqNuh7ntCBc0Tj`.
4. Copy the token — this is your `AIRTABLE_API_KEY`.

The script writes to:
- **Base ID:** `appWqNuh7ntCBc0Tj`
- **Table ID:** `tblMEHXkOoN5V7N7Z`

Ensure that table has the following fields (exact names):
| Field Name | Type |
|------------|------|
| File Name  | Single line text |
| File Type  | Single line text |
| Date Added | Date (or single line text) |
| Drive Link | URL (or single line text) |
| Notified   | Checkbox |

---

### 3. Gmail App Password

1. Go to your [Google Account](https://myaccount.google.com/) → **Security**.
2. Enable **2-Step Verification** if not already active.
3. Search for **App passwords** and create one for "Mail" on "Other (custom name)".
4. Copy the 16-character password — this is your `GMAIL_APP_PASSWORD`.

---

### 4. Add GitHub Secrets

In your GitHub repository, go to **Settings → Secrets and variables → Actions → New repository secret** and add each of the following:

| Secret Name                  | Value |
|------------------------------|-------|
| `GOOGLE_SERVICE_ACCOUNT_JSON` | The full contents of the service account JSON file |
| `AIRTABLE_API_KEY`           | Your Airtable personal access token |
| `GMAIL_USER`                 | Your Gmail address (e.g. `you@gmail.com`) |
| `GMAIL_APP_PASSWORD`         | The 16-character Gmail app password |
| `NOTIFICATION_EMAIL`         | Email address to receive notifications (can be the same as `GMAIL_USER`) |

---

### 5. Run Manually (Terminal)

```bash
# Clone the repo and install dependencies
git clone https://github.com/cromero-opzer/opzer.co.git
cd opzer.co
pip install -r requirements.txt

# Set environment variables
export GOOGLE_SERVICE_ACCOUNT_JSON='{ ... paste full JSON content here ... }'
export AIRTABLE_API_KEY='your_airtable_token'
export GMAIL_USER='you@gmail.com'
export GMAIL_APP_PASSWORD='your_app_password'
export NOTIFICATION_EMAIL='you@gmail.com'

# Run the script
python drive_to_airtable_notifier.py
```

---

### 6. Scheduled Automation (GitHub Actions)

The workflow in `.github/workflows/daily_drive_sync.yml` runs automatically:

- **Scheduled:** Every day at **9:00 AM EST** (14:00 UTC)
- **Manual trigger:** Go to your repo on GitHub → **Actions** tab → **Daily Google Drive Sync** → **Run workflow**

Each run:
1. Checks out the repo and installs Python dependencies.
2. Runs `drive_to_airtable_notifier.py` with credentials from GitHub Secrets.
3. Logs new files to Airtable and sends an email notification.

View run history and logs under the **Actions** tab in your repository.

---

## File Structure

```
opzer.co/
├── drive_to_airtable_notifier.py   # Main automation script
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── .github/
    └── workflows/
        └── daily_drive_sync.yml    # GitHub Actions workflow
```
