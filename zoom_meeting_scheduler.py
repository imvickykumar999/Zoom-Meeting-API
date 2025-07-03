import requests
from requests_oauthlib import OAuth2Session
import webbrowser
import time
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
client_id = os.getenv("ZOOM_CLIENT_ID")
client_secret = os.getenv("ZOOM_CLIENT_SECRET")
redirect_uri = 'http://localhost'  # For manual testing in browser

auth_base_url = 'https://zoom.us/oauth/authorize'
token_url = 'https://zoom.us/oauth/token'
user_info_url = 'https://api.zoom.us/v2/users/me'
meeting_url = 'https://api.zoom.us/v2/users/me/meetings'

# ---- Step 2: Start OAuth Flow ----
zoom = OAuth2Session(client_id, redirect_uri=redirect_uri)
authorization_url, state = zoom.authorization_url(auth_base_url)

print(f"Go to this URL to authorize:\n{authorization_url}")
webbrowser.open(authorization_url)

# ---- Step 3: Get Authorization Response Manually ----
redirect_response = input('\nPaste the full redirect URL here after authorization:\n')

# ---- Step 4: Fetch Access Token ----
token = zoom.fetch_token(
    token_url,
    authorization_response=redirect_response,
    client_secret=client_secret
)

print("\nAccess token fetched successfully!")
print(token)

# ---- Step 5: Prepare Meeting Details ----
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

# ---- Step 6: Create Meeting ----
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
