# Medicine Expiry Dashboard

A beginner-friendly Cloud Computing mini-project built with Python Flask, SQLite, HTML and CSS. It tracks medicine batches and automatically classifies their expiry status.

## Features

- Dashboard counts for total, safe, expiring soon and expired records
- Add medicine name, batch number, quantity and expiry date
- Search by medicine name or batch number
- Delete medicine records
- Automatic status calculation:
  - **Expired:** expiry date is before today
  - **Expiring Soon:** expiry date is today through the next 30 days
  - **Safe:** expiry date is more than 30 days away
- Responsive professional dashboard

## Project structure

```text
medicine-expiry-dashboard/
├── app.py
├── requirements.txt
├── render.yaml
├── README.md
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Run on Windows

1. Install Python 3.10 or newer from https://www.python.org/downloads/
2. Extract this ZIP file.
3. Open the extracted `medicine-expiry-dashboard` folder.
4. Click the File Explorer address bar, type `cmd`, and press Enter.
5. Run:

   ```bash
   python -m pip install -r requirements.txt
   python app.py
   ```

6. Open http://127.0.0.1:5000 in your browser.
7. To stop the server, return to Command Prompt and press `Ctrl+C`.

The SQLite database file `medicines.db` is created automatically in the project folder.

## Deploy to Render using GitHub

1. Sign in to https://github.com/ and create a repository named `medicine-expiry-dashboard`.
2. Upload the contents of this project folder to the repository. Make sure `app.py`, `requirements.txt`, `render.yaml`, `templates/` and `static/` are at the repository root.
3. Sign in to https://render.com/ using GitHub.
4. Choose **New +** → **Web Service** and connect the repository.
5. Use these settings:
   - Runtime: Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
6. Choose a plan available to your account and click **Deploy Web Service**.
7. When deployment succeeds, open the `onrender.com` URL shown in the Render dashboard.

Render can also read the included `render.yaml` configuration when creating the service.

## SQLite and Render persistence note

This project uses SQLite to keep the demo simple. Render web services have an ephemeral filesystem by default, so a local SQLite database can be lost when the service restarts, is redeployed, or the instance is replaced.

For persistent SQLite storage, attach a persistent disk to the Render service (where supported by your plan), mount it at `/var/data`, and set the environment variable:

`DATABASE_PATH=/var/data/medicines.db`

For a multi-user or production application, use a managed PostgreSQL database instead. Do not use this classroom demo as the sole system for real medicine safety or dispensing decisions.

## Viva / project explanation

**Objective:** Build a cloud-hosted web application that helps users maintain a medicine inventory and identify medicines that have expired or are approaching expiry.

**Cloud concepts demonstrated:** cloud web hosting, client-server architecture, HTTP requests, backend processing, database integration and deployment through a cloud platform.

**Technology:** Python Flask (backend), HTML/CSS (frontend), SQLite (database), Gunicorn (production WSGI server), Render (cloud hosting).

**Limitation:** This is an educational demonstration. It does not send notifications, verify manufacturer expiry information, or replace professional medicine inventory controls.
