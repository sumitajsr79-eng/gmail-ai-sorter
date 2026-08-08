import threading
import time
import webview
import sys
import os
import webbrowser

# Ensure current directory is in python path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

def start_flask_server():
    """Runs Flask backend server in background thread."""
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # Launch Flask backend on background thread
    server_thread = threading.Thread(target=start_flask_server, daemon=True)
    server_thread.start()

    time.sleep(1)

    try:
        # Force Edge Chromium (WebView2) engine to bypass pythonnet / winforms DLL issues
        webview.create_window(
            title='SmartMail AI (GmailAISorter)',
            url='http://127.0.0.1:5000',
            width=1280,
            height=850,
            resizable=True,
            min_size=(900, 600)
        )
        webview.start(gui='edgechromium')
    except Exception as e:
        print(f"WebView initialization notice: {e}")
        # Fallback launcher for any system without WebView2
        webbrowser.open('http://127.0.0.1:5000')
        # Keep background server alive
        server_thread.join()
