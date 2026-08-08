# SmartMail AI (GmailAISorter) ⚡

**SmartMail AI** is an intelligent, high-speed desktop and web application that categorizes and organizes your Gmail inbox into custom labels using **Google Gemini AI** or a smart keyword scoring engine.

---

## 🔗 GitHub Repository
**[https://github.com/sumitajsr79-eng/gmail-ai-sorter](https://github.com/sumitajsr79-eng/gmail-ai-sorter)**

---

## 📦 Download Desktop Executable (.exe)
**[👉 Click Here to Download SmartMail AI v1.0.0 for Windows (.zip)](https://github.com/sumitajsr79-eng/gmail-ai-sorter/releases/tag/v1.0.0)**

---

## 🔑 Alternative Authentication Technique (Gmail App Password)

No Google Cloud Console setup or OAuth API configuration is required! You can connect your Gmail account securely using **Google App Passwords over IMAP SSL**:

1. Go to your [Google Account Security Settings](https://myaccount.google.com/security) (ensure 2-Step Verification is ON).
2. Visit [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
3. Generate a 16-character App Password (e.g. `abcd efgh ijkl mnop`).
4. Enter your Gmail address and 16-character App Password directly into the app interface!

---

## ✨ Features

- 🖥️ **Windows Desktop Executable (`.exe`)**: Runs directly as a native Windows desktop app window without redirecting to a browser.
- ⚡ **High-Speed Bulk Batching**: Processes 1,700+ inbox emails in seconds using bulk IMAP operations.
- 📊 **Real-Time Live Progress Bar**: Tracks scanning and classification progress live from 0% to 100%.
- 📂 **Gmail Labels Explorer**: View all your Gmail labels and folders in-app with live email message counts.
- 🔍 **In-App Label Inspector**: Click any label to view emails belonging to it directly inside the app.
- 🗑️ **Delete Controls**: Remove labels or send individual emails to Trash with 1 click.
- 📥 **1-Click Inbox Restore**: Easily restore all archived emails back to your main Gmail Inbox view anytime.

---

## 💻 How to Run

### Standalone Executable
Double-click:
```
dist/GmailAISorter/GmailAISorter.exe
```

### Python Script / Development
```powershell
python desktop_app.py
```
Or run the web app:
```powershell
python app.py
```
And navigate to `http://localhost:5000`.
