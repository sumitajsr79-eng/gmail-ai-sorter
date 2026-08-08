import base64
import email
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GmailService:
    def __init__(self, credentials_dict):
        """Initialize Gmail API service with OAuth credentials dictionary."""
        self.credentials = Credentials.from_authorized_user_info(credentials_dict)
        self.service = build('gmail', 'v1', credentials=self.credentials)

    def get_user_email(self):
        """Fetch the authenticated user's email address."""
        try:
            profile = self.service.users().getProfile(userId='me').execute()
            return profile.get('emailAddress', 'Unknown User')
        except Exception as e:
            print(f"Error fetching profile: {e}")
            return "Authenticated User"

    def get_existing_labels(self):
        """Retrieve all existing labels in the user's Gmail account."""
        try:
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            return {label['name'].lower(): label['id'] for label in labels}
        except Exception as e:
            print(f"Error fetching labels: {e}")
            return {}

    def ensure_label_exists(self, label_name):
        """Get existing label ID or create a new label with label_name."""
        existing_labels = self.get_existing_labels()
        clean_name = label_name.strip()
        
        if clean_name.lower() in existing_labels:
            return existing_labels[clean_name.lower()]

        # Create new label in Gmail
        label_body = {
            'name': clean_name,
            'labelListVisibility': 'labelShow',
            'messageListVisibility': 'show'
        }
        try:
            created_label = self.service.users().labels().create(userId='me', body=label_body).execute()
            print(f"Created new Gmail label: {clean_name} (ID: {created_label['id']})")
            return created_label['id']
        except HttpError as error:
            print(f"Failed to create label {clean_name}: {error}")
            return None

    def fetch_messages(self, max_results=15, query='in:inbox'):
        """Fetch list of messages with details (Subject, Sender, Snippet, Date)."""
        try:
            messages_meta = []
            page_token = None
            
            while True:
                fetch_limit = 100 if (max_results == 0 or max_results > 100) else max_results
                response = self.service.users().messages().list(
                    userId='me',
                    maxResults=fetch_limit,
                    q=query,
                    pageToken=page_token
                ).execute()

                fetched = response.get('messages', [])
                messages_meta.extend(fetched)
                page_token = response.get('nextPageToken')

                if max_results > 0 and len(messages_meta) >= max_results:
                    messages_meta = messages_meta[:max_results]
                    break

                if not page_token or (max_results > 0 and len(messages_meta) >= max_results):
                    break

            email_list = []

            for msg_meta in messages_meta:
                msg_id = msg_meta['id']
                msg = self.service.users().messages().get(userId='me', id=msg_id, format='full').execute()
                
                payload = msg.get('payload', {})
                headers = payload.get('headers', [])

                subject = "No Subject"
                sender = "Unknown Sender"
                date_str = ""

                for h in headers:
                    h_name = h['name'].lower()
                    if h_name == 'subject':
                        subject = h['value']
                    elif h_name == 'from':
                        sender = h['value']
                    elif h_name == 'date':
                        date_str = h['value']

                snippet = msg.get('snippet', '')

                email_list.append({
                    'id': msg_id,
                    'threadId': msg.get('threadId'),
                    'subject': subject,
                    'sender': sender,
                    'date': date_str,
                    'snippet': snippet,
                    'labels': msg.get('labelIds', [])
                })

            return email_list

        except Exception as e:
            print(f"Error fetching messages: {e}")
            return []

    def apply_label_to_message(self, message_id, label_id, remove_inbox=False):
        """Apply specified label ID to a Gmail message."""
        try:
            body = {'addLabelIds': [label_id]}
            if remove_inbox:
                body['removeLabelIds'] = ['INBOX']
                
            updated_msg = self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body=body
            ).execute()
            return True
        except Exception as e:
            print(f"Error modifying message {message_id}: {e}")
            return False
