from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import re

# Define the SCOPES
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def clean_filename(subject):
    # Replace invalid characters with underscores
    return re.sub(r'[\/:*?"<>|]', '_', subject)

def save_email_original(subject, message_id, original_content):
    if not os.path.exists('original'):
        os.makedirs('original')
    
    # Ensure unique filename by including message_id if subject is not available
    if subject.strip() == "":
        subject = f"No_Subject_{message_id}"
    
    filename = f'original/{clean_filename(subject)}.eml'
    with open(filename, 'wb') as file:
        file.write(original_content)

def getEmails():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    page_token = None

    while True:
        result = service.users().messages().list(userId='me', pageToken=page_token).execute()

        messages = result.get('messages', [])
        if not messages:
            print("No messages found.")
            break

        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id'], format='raw').execute()  # Use 'raw' format to get the original message

            try:
                # Extract subject and ensure it is unique
                headers = txt.get('payload', {}).get('headers', [])
                subject = next((header['value'] for header in headers if header['name'] == 'Subject'), '')
                
                # Decode the raw message content
                raw_data = txt['raw']
                original_data = base64.urlsafe_b64decode(raw_data)
                
                # Save the original message with unique filename
                save_email_original(subject, msg['id'], original_data)

            except Exception as e:
                print(f"An error occurred while processing message id {msg['id']}: {e}")

        page_token = result.get('nextPageToken')
        if not page_token:
            break

if __name__ == '__main__':
    getEmails()
