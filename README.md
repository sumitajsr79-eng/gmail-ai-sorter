# AI Gmail Organizer & Categorizer ⚡

An AI-powered application that connects securely to Gmail via Google OAuth 2.0 and classifies incoming messages into custom user-defined categories using Google Gemini AI.

---

## 🔒 Security Notice

Google accounts **cannot and should not** be accessed by entering raw email/passwords directly into third-party apps. To protect user privacy and account security, this application uses **Google OAuth 2.0 (Gmail API)**. Users log in directly on Google's official consent page to grant label modification permissions.

---

## 🚀 Quick Start Guide

### 1. Configure Google OAuth Credentials (`credentials.json`)
1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and search for **Gmail API** -> Click **Enable**.
3. Go to **OAuth Consent Screen** -> Select **External** (or Internal) -> Fill in App Name & Email.
4. Go to **Credentials** -> Click **Create Credentials** -> **OAuth Client ID**.
5. Select Application Type: **Web Application**.
6. Under **Authorized redirect URIs**, add:
   `http://localhost:5000/oauth2callback`
7. Click **Create**, then click **Download JSON**.
8. Save this file as `credentials.json` directly inside `C:\Users\Baba\.gemini\antigravity\scratch\gmail_ai_sorter\credentials.json`.

---

### 2. Run the Application

Navigate to the project folder and start the Flask server:

```powershell
cd C:\Users\Baba\.gemini\antigravity\scratch\gmail_ai_sorter
python app.py
```

Open your browser and navigate to:
**http://localhost:5000**

---

### 3. Usage Instructions

1. **Connect Gmail**: Click **Connect Gmail** to log in securely via Google's official OAuth page.
2. **Add Categories**: Input your preferred labels (e.g. `Finance & Receipts`, `Work Projects`, `Newsletters & Media`, `Action Required`).
3. **Gemini API Key (Optional)**: Paste your Google Gemini API key to enable zero-shot AI classification. If left blank, the app will use rule-based keyword matching as a fallback.
4. **Dry-Run vs Live Mode**:
   - **Dry-Run**: Preview how emails will be categorized without changing anything in your actual Gmail inbox.
   - **Live Mode**: Automatically creates Gmail labels and applies them to your inbox messages.

---

## 📁 Project Directory Structure

- `app.py`: Flask web server and API endpoints.
- `gmail_service.py`: Google OAuth 2.0 authentication & Gmail API interaction module.
- `ai_classifier.py`: Gemini AI email classification engine.
- `templates/index.html`: Dashboard UI.
- `static/css/style.css`: Visual styling & animations.
- `static/js/main.js`: Interactive UI script.
