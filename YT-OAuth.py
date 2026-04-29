from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
import json

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
credentials_file = Path("credentials.json")

if credentials_file.exists():
    with open(credentials_file, 'r') as f:
        client_credentials = json.load(f)

        client_id = input("\nPaste your client id").strip().lower()
        client_credentials['installed']['client_id'] = client_id

        client_secret = input("\nPaste your client secret").strip().lower()
        client_credentials['installed']['client_secret'] = client_secret

        project_id = input("\nPaste your project id").strip().lower()
        client_credentials['installed']['project_id'] = project_id

        refresh_token = input("\nPaste your refresh token").strip().lower()
        client_credentials['installed']['refresh_token'] = refresh_token

    with open(credentials_file, 'w') as e:
        json.dump(client_credentials, e, indent=4)

else:
    client_credentials = {}


flow = InstalledAppFlow.from_client_config(client_credentials, SCOPES)

credentials = flow.run_local_server(access_type='offline')

print("Access token:", credentials.token)
print("Refresh token:", credentials.refresh_token)
print("Token expiry:", credentials.expiry)
