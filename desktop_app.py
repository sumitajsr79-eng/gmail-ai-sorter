import threading
import time
import webview
import sys
import os

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

    # Wait briefly for server startup
    time.sleep(1)

    # Launch native desktop application window
    webview.create_window(
        title='AI Gmail Sorter App',
        url='http://127.0.0.1:5000',
        width=1280,
        height=850,
        resizable=True,
        min_size=(900, 600)
    )
    webview.start()
