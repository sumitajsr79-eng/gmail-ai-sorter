from concurrent.futures import ThreadPoolExecutor
import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

import config
from gmail_service import GmailService
from imap_service import IMAPGmailService
from ai_classifier import AIEmailClassifier

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

DEFAULT_CATEGORIES = [
    "Work Projects",
    "Finance Receipts",
    "Newsletters Media",
    "Promotions Deals",
    "Urgent Important"
]

@app.route('/')
def index():
    auth_type = session.get('auth_type')
    user_email = None

    if auth_type == 'oauth' and 'credentials' in session:
        try:
            gmail_svc = GmailService(json.loads(session['credentials']))
            user_email = gmail_svc.get_user_email()
        except Exception:
            session.pop('credentials', None)
            session.pop('auth_type', None)
    elif auth_type == 'imap' and 'imap_user' in session:
        user_email = session['imap_user'].get('email')

    gemini_key = session.get('gemini_api_key', os.environ.get('GEMINI_API_KEY', ''))
    categories = session.get('categories', DEFAULT_CATEGORIES)
    has_oauth_config = os.path.exists(config.CLIENT_SECRETS_FILE)

    return render_template('index.html',
                           auth_type=auth_type,
                           user_email=user_email,
                           gemini_key=gemini_key,
                           categories=categories,
                           has_oauth_config=has_oauth_config)

@app.route('/login')
def login():
    if not os.path.exists(config.CLIENT_SECRETS_FILE):
        return jsonify({'error': 'credentials.json not found on server.'}), 400

    flow = Flow.from_client_secrets_file(
        config.CLIENT_SECRETS_FILE,
        scopes=config.OAUTH_SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session.get('state')
    if not os.path.exists(config.CLIENT_SECRETS_FILE):
        return redirect(url_for('index'))

    flow = Flow.from_client_secrets_file(
        config.CLIENT_SECRETS_FILE,
        scopes=config.OAUTH_SCOPES,
        state=state,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

    session['credentials'] = credentials.to_json()
    session['auth_type'] = 'oauth'
    return redirect(url_for('index'))

@app.route('/login_imap', methods=['POST'])
def login_imap():
    data = request.json or {}
    email_addr = data.get('email', '').strip()
    app_password = data.get('app_password', '').strip()

    if not email_addr or not app_password:
        return jsonify({'error': 'Please enter both Email Address and App Password.'}), 400

    imap_svc = IMAPGmailService(email_addr, app_password)
    success, msg = imap_svc.verify_credentials()

    if success:
        session['auth_type'] = 'imap'
        session['imap_user'] = {
            'email': email_addr,
            'app_password': app_password
        }
        return jsonify({'status': 'success', 'email': email_addr, 'message': msg})
    else:
        return jsonify({'error': msg}), 401

@app.route('/logout')
def logout():
    session.pop('credentials', None)
    session.pop('imap_user', None)
    session.pop('auth_type', None)
    return redirect(url_for('index'))

@app.route('/api/save_settings', methods=['POST'])
def save_settings():
    data = request.json or {}
    if 'gemini_api_key' in data:
        session['gemini_api_key'] = data['gemini_api_key'].strip()
    if 'categories' in data and isinstance(data['categories'], list):
        cleaned = [c.strip() for c in data['categories'] if c.strip()]
        if cleaned:
            session['categories'] = cleaned

    return jsonify({'status': 'success', 'message': 'Settings saved successfully'})

@app.route('/api/run_sorting', methods=['POST'])
def run_sorting():
    auth_type = session.get('auth_type')
    if not auth_type:
        return jsonify({'error': 'Please connect your Gmail account using either App Password or Google OAuth first.'}), 401

    data = request.json or {}
    dry_run = data.get('dry_run', True)
    max_emails = int(data.get('max_emails', 10))
    remove_inbox = data.get('remove_inbox', False)

    categories = session.get('categories', DEFAULT_CATEGORIES)
    gemini_key = session.get('gemini_api_key', os.environ.get('GEMINI_API_KEY', ''))
    ai_sorter = AIEmailClassifier(api_key=gemini_key)

    results = []

    try:
        if auth_type == 'oauth':
            user_credentials = session.get('credentials')
            gmail_svc = GmailService(json.loads(user_credentials))
            emails = gmail_svc.fetch_messages(max_results=max_emails, query='in:inbox')

            # Turbo-Speed Engine: Use classify_bulk_ultra_fast for instant sorting
            categories_assigned = ai_sorter.classify_bulk_god_mode(emails, categories)
            results = []
            for email_item, cat in zip(emails, categories_assigned):
                action_taken = "Analyzed (Dry Run)" if dry_run else f"Labeled as '{cat}'"
                results.append({
                    'id': email_item['id'],
                    'subject': email_item['subject'],
                    'sender': email_item['sender'],
                    'snippet': email_item['snippet'],
                    'assigned_category': cat,
                    'action_taken': action_taken
                })

        elif auth_type == 'imap':
            imap_info = session.get('imap_user', {})
            imap_svc = IMAPGmailService(imap_info.get('email'), imap_info.get('app_password'))
            emails = imap_svc.fetch_messages(max_results=max_emails)

            label_assignments = {}

            categories_assigned = ai_sorter.classify_bulk_god_mode(emails, categories)
            results = []
            for email_item, cat in zip(emails, categories_assigned):
                action_taken = "Analyzed (Dry Run)" if dry_run else f"Queued for '{cat}'"
                results.append({
                    'id': email_item['id'],
                    'subject': email_item['subject'],
                    'sender': email_item['sender'],
                    'snippet': email_item['snippet'],
                    'assigned_category': cat,
                    'action_taken': action_taken
                })

            # Execute high-speed bulk labeling if not in dry-run mode
            if not dry_run:
                success = imap_svc.batch_apply_labels(label_assignments, remove_inbox=remove_inbox)
                for res in results:
                    if res['assigned_category'] != "Uncategorized":
                        res['action_taken'] = f"Labeled as '{res['assigned_category']}' (IMAP Bulk)" if success else "Failed to label"

        return jsonify({
            'status': 'success',
            'dry_run': dry_run,
            'total_analyzed': len(results),
            'results': results
        })

    except Exception as e:
        print(f"Sorting error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/restore_inbox', methods=['POST'])
def restore_inbox():
    auth_type = session.get('auth_type')
    if auth_type == 'imap':
        imap_info = session.get('imap_user', {})
        imap_svc = IMAPGmailService(imap_info.get('email'), imap_info.get('app_password'))
        success, msg = imap_svc.restore_all_to_inbox()
        if success:
            return jsonify({'status': 'success', 'message': msg})
        else:
            return jsonify({'error': msg}), 500
    else:
        return jsonify({'error': 'Restore is supported for IMAP accounts.'}), 400

@app.route('/api/list_labels', methods=['GET'])
def list_labels():
    auth_type = session.get('auth_type')
    if auth_type == 'imap':
        imap_info = session.get('imap_user', {})
        imap_svc = IMAPGmailService(imap_info.get('email'), imap_info.get('app_password'))
        labels = imap_svc.list_user_labels()
        return jsonify({'status': 'success', 'labels': labels})
    return jsonify({'labels': []})

@app.route('/api/get_label_emails', methods=['POST'])
def get_label_emails():
    auth_type = session.get('auth_type')
    data = request.json or {}
    label_name = data.get('label_name')

    if not label_name:
        return jsonify({'error': 'Label name required'}), 400

    if auth_type == 'imap':
        imap_info = session.get('imap_user', {})
        imap_svc = IMAPGmailService(imap_info.get('email'), imap_info.get('app_password'))
        emails = imap_svc.fetch_messages_in_label(label_name)
        return jsonify({'status': 'success', 'label': label_name, 'emails': emails})
    return jsonify({'emails': []})

@app.route('/api/delete_label', methods=['POST'])
def delete_label():
    auth_type = session.get('auth_type')
    data = request.json or {}
    label_name = data.get('label_name')

    if not label_name:
        return jsonify({'error': 'Label name required'}), 400

    if auth_type == 'imap':
        imap_info = session.get('imap_user', {})
        imap_svc = IMAPGmailService(imap_info.get('email'), imap_info.get('app_password'))
        success, msg = imap_svc.delete_label(label_name)
        if success:
            return jsonify({'status': 'success', 'message': msg})
        return jsonify({'error': msg}), 500
    return jsonify({'error': 'Not authorized'}), 401

@app.route('/api/delete_email', methods=['POST'])
def delete_email():
    auth_type = session.get('auth_type')
    data = request.json or {}
    message_id = data.get('message_id')
    folder_name = data.get('folder_name', 'INBOX')

    if not message_id:
        return jsonify({'error': 'Message ID required'}), 400

    if auth_type == 'imap':
        imap_info = session.get('imap_user', {})
        imap_svc = IMAPGmailService(imap_info.get('email'), imap_info.get('app_password'))
        success, msg = imap_svc.delete_email(message_id, folder_name)
        if success:
            return jsonify({'status': 'success', 'message': msg})
        return jsonify({'error': msg}), 500
    return jsonify({'error': 'Not authorized'}), 401

if __name__ == '__main__':
    print("Starting AI Gmail Organizer App on http://localhost:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)
