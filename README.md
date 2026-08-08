# SmartMail AI (GmailAISorter) ⚡

**SmartMail AI** is an intelligent, high-speed desktop application that categorizes and organizes your Gmail inbox into custom labels using **Google Gemini AI** or a smart keyword scoring engine.

---

## 💻 Download Windows Desktop Executable (`.exe`)
The compiled standalone executable is available directly in the root of this GitHub repository:

👉 **[Download GmailAISorter.exe (59.5 MB)](https://github.com/sumitajsr79-eng/gmail-ai-sorter/raw/master/GmailAISorter.exe)**

---

## 🔑 Authentication (Gmail App Password)

No Google Cloud Console setup or OAuth API configuration is required! You can connect your Gmail account securely using **Google App Passwords over IMAP SSL**:

1. Go to your [Google Account Security Settings](https://myaccount.google.com/security) (ensure 2-Step Verification is ON).
2. Visit [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
3. Generate a 16-character App Password (e.g. `abcd efgh ijkl mnop`).
4. Double-click `GmailAISorter.exe`, enter your Gmail address and 16-character App Password, and click **Connect via App Password**!

---

## ✨ Features

- 🖥️ **Windows Desktop Executable (`GmailAISorter.exe`)**: Runs directly as a native Windows desktop app window without redirecting to a browser.
- ⚡ **High-Speed Bulk Batching**: Processes 1,700+ inbox emails in seconds using bulk IMAP operations.
- 📊 **Real-Time Live Progress Bar**: Tracks scanning and classification progress live from 0% to 100%.
- 📂 **Gmail Labels Explorer**: View all your Gmail labels and folders in-app with live email message counts.
- 🔍 **In-App Label Inspector**: Click any label to view emails belonging to it directly inside the app.
- 🗑️ **Delete Controls**: Remove labels or send individual emails to Trash with 1 click.
- 📥 **1-Click Inbox Restore**: Easily restore all archived emails back to your main Gmail Inbox view anytime.

---

## 📂 Repository Contents

- `GmailAISorter.exe`: Compiled Windows Desktop standalone application.
- `desktop_app.py`: Desktop application wrapper powered by PyWebView & Edge Chromium engine.
- `app.py`: Backend server & REST API endpoints.
- `imap_service.py`: High-speed Gmail IMAP SSL batching service.
- `ai_classifier.py`: Google Gemini AI & domain keyword scoring engine.
- `templates/index.html` & `static/`: Glassmorphic desktop interface, styling, and JavaScript logic.
