# SmartMail AI (GmailAISorter) ⚡

**SmartMail AI** is an intelligent, high-speed desktop and mobile application that categorizes and organizes your Gmail inbox into custom labels using **Google Gemini AI** or a smart keyword scoring engine.

---

## 📥 Downloads (Direct Repo Links)

| Platform | Download Link | File |
| :--- | :--- | :--- |
| 📱 **Android App** | 👉 [**Download GmailAISorter.apk**](https://github.com/sumitajsr79-eng/gmail-ai-sorter/raw/master/GmailAISorter.apk) | `GmailAISorter.apk` |
| 💻 **Windows Desktop** | 👉 [**Download GmailAISorter.exe (59.5 MB)**](https://github.com/sumitajsr79-eng/gmail-ai-sorter/raw/master/GmailAISorter.exe) | `GmailAISorter.exe` |

> 💡 **Android Installation:** Download [`GmailAISorter.apk`](https://github.com/sumitajsr79-eng/gmail-ai-sorter/raw/master/GmailAISorter.apk) directly to your Android device, tap to install, and launch SmartMail AI!

---

## 📱 Android App & Build Pipeline

The repository includes a complete native Android application project (`android/`) and an automated **GitHub Actions CI/CD Build Pipeline** (`.github/workflows/build-apk.yml`):
- Whenever code is updated, GitHub Actions automatically compiles the Android package and commits [`GmailAISorter.apk`](https://github.com/sumitajsr79-eng/gmail-ai-sorter/raw/master/GmailAISorter.apk) directly to the repository root.


## 🔑 Authentication (Gmail App Password)

No Google Cloud Console setup or OAuth API configuration is required! You can connect your Gmail account securely using **Google App Passwords over IMAP SSL**:

1. Go to your [Google Account Security Settings](https://myaccount.google.com/security) (ensure 2-Step Verification is ON).
2. Visit [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
3. Generate a 16-character App Password (e.g. `abcd efgh ijkl mnop`).
4. Enter your Gmail address and 16-character App Password into SmartMail AI and click **Connect via App Password**!

---

## ✨ Features

- 🖥️ **Windows Desktop Executable (`GmailAISorter.exe`)**: Native Windows app window without browser redirection.
- 📱 **Android Native App (`android/`)**: Native Kotlin WebView activity for Android phones.
- ⚡ **High-Speed Bulk Batching**: Processes 1,700+ inbox emails in seconds using bulk IMAP operations.
- 📊 **Real-Time Live Progress Bar**: Tracks scanning and classification progress live from 0% to 100%.
- 📂 **Gmail Labels Explorer**: View all your Gmail labels and folders in-app with live email message counts.
- 🔍 **In-App Label Inspector**: Click any label to view emails belonging to it directly inside the app.
- 🗑️ **Delete Controls**: Remove labels or send individual emails to Trash with 1 click.
- 📥 **1-Click Inbox Restore**: Easily restore all archived emails back to your main Gmail Inbox view anytime.
