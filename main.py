import requests
from requests_oauthlib import OAuth2Session
import webbrowser
import os
import json

# Allow HTTP for local dev
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Set your credentials here or via env vars
client_id = os.getenv("ZOOM_CLIENT_ID") or "your_client_id"
client_secret = os.getenv("ZOOM_CLIENT_SECRET") or "your_client_secret"
redirect_uri = 'http://localhost'

auth_base_url = 'https://zoom.us/oauth/authorize'
token_url = 'https://zoom.us/oauth/token'
meeting_url = 'https://api.zoom.us/v2/users/me/meetings'

TOKEN_FILE = 'zoom_token.json'  # where token will be saved

# ---- Step 1: OAuth Flow ----
zoom = OAuth2Session(client_id, redirect_uri=redirect_uri)
authorization_url, state = zoom.authorization_url(auth_base_url)

print(f"Go to this URL to authorize:\n{authorization_url}")
webbrowser.open(authorization_url)

redirect_response = input('\nPaste the full redirect URL here after authorization:\n')

# ---- Step 2: Fetch Token ----
token = zoom.fetch_token(
    token_url,
    authorization_response=redirect_response,
    client_secret=client_secret
)

print("\n✅ Access token fetched successfully!")
print(json.dumps(token, indent=2))

# ---- Step 3: Save Token to File ----
with open(TOKEN_FILE, 'w') as f:
    json.dump(token, f, indent=2)
print(f"\n🔒 Token saved to {TOKEN_FILE}")

# ---- Step 4: Prepare API Call ----
headers = {
    'Authorization': f"Bearer {token['access_token']}",
    'Content-Type': 'application/json'
}

meeting_data = {
    "topic": "Test Meeting with Zoom API",
    "type": 2,
    "start_time": "2025-07-05T15:00:00",
    "duration": 30,
    "timezone": "Asia/Kolkata",
    "settings": {
        "join_before_host": True,
        "mute_upon_entry": True,
        "approval_type": 0
    }
}

# ---- Step 5: Create Meeting ----
response = requests.post(meeting_url, headers=headers, json=meeting_data)

if response.status_code == 201:
    meeting_info = response.json()
    print("\n✅ Zoom Meeting Created Successfully!")
    print(f"Topic: {meeting_info['topic']}")
    print(f"Start Time: {meeting_info['start_time']}")
    print(f"Join URL: {meeting_info['join_url']}")
else:
    print("\n❌ Failed to create meeting")
    print(response.status_code, response.text)

