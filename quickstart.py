import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
GOOGLE_BASE_URL = 'https://www.googleapis.com'
TOKEN_FILE_NAME = 'google__auth_token.json'
CREDENTIAL_FILE_NAME = 'google__client_secret.json'
BASE_SCOPES = ['/auth/drive.file', '/auth/drive.appdata', '/auth/drive.file', '/auth/docs', '/auth/drive']

SCOPES = [GOOGLE_BASE_URL+scope for scope in BASE_SCOPES]

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE_NAME):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE_NAME, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIAL_FILE_NAME, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE_NAME, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        result = service.files().list()
        print(result.__dict__)

    except HttpError as exc:
        print('An error occurred: %s' % exc)


if __name__ == '__main__':
    main()
