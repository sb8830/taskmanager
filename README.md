# TaskFlow Pro

Production-ready Streamlit task assignment and management portal with Moderator and Agent roles.

## Demo Credentials

Moderator:

```text
admin@taskflow.com / Admin@123
```

Agent:

```text
agent@taskflow.com / Agent@123
```

For Streamlit Cloud, set these in **App > Settings > Secrets** instead of committing passwords to GitHub.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## GitHub Deployment

```bash
git init
git add .
git commit -m "Initial TaskFlow Pro app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/taskflow-pro.git
git push -u origin main
```

## Streamlit Cloud Deployment

Use:

```text
Repository: YOUR_USERNAME/taskflow-pro
Branch: main
Main file path: app.py
```

Add these in Streamlit Cloud Secrets:

```toml
SECRET_KEY = "change-this-secret-key"
DATABASE_URL = "sqlite:///taskflow.db"
APP_ENV = "production"
SESSION_TIMEOUT_MINUTES = 30
MAX_UPLOAD_MB = 20

ADMIN_EMAIL = "admin@taskflow.com"
ADMIN_PASSWORD = "Admin@123"
AGENT_EMAIL = "agent@taskflow.com"
AGENT_PASSWORD = "Agent@123"
```

## Notes

SQLite works for demo and first deployment. For production, use PostgreSQL and set `DATABASE_URL` in Streamlit Secrets.
