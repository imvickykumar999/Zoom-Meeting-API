import requests
import json
import os
import time
import base64

TOKEN_FILE = 'zoom_token.json'
client_id = os.getenv("ZOOM_CLIENT_ID") or "your_client_id"
client_secret = os.getenv("ZOOM_CLIENT_SECRET") or "your_client_secret"

# Load saved token from file
def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            token = json.load(f)

        # If expires_at is missing, calculate it now
        if 'expires_at' not in token:
            print("⚠️ 'expires_at' missing. Calculating from 'expires_in'...")
            token['expires_at'] = time.time() + token.get('expires_in', 3600)
            save_token(token)

        return token
    else:
        raise Exception("❌ Token file not found. Run initial OAuth flow to create it.")

# Save token to file
def save_token(token_data):
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f, indent=2)
    print("💾 Token saved to file.")

# Check if access token is expired or close to expiry
def is_token_expired(token):
    current_time = time.time()
    expires_at = token.get('expires_at')

    if not expires_at:
        raise Exception("❌ 'expires_at' missing in token. Unable to verify expiry.")

    return current_time > (expires_at - 120)  # Refresh if <2 min left

# Refresh token using refresh_token
def refresh_access_token(token):
    print("🔄 Refreshing access token...")
    refresh_token = token['refresh_token']
    url = "https://zoom.us/oauth/token"

    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(url, headers=headers, params=params)

    if response.status_code == 200:
        new_token = response.json()
        new_token['expires_at'] = time.time() + new_token['expires_in']
        print("✅ Token refreshed successfully.")
        return new_token
    else:
        raise Exception(f"❌ Failed to refresh token: {response.status_code} {response.text}")

# Create Zoom meeting
def create_zoom_meeting(access_token):
    url = 'https://api.zoom.us/v2/users/me/meetings'
    headers = {
        'Authorization': f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }
    payload = {
        "topic": "Auto-Refreshed Token Meeting",
        "type": 2,
        "start_time": "2025-07-06T11:00:00",
        "duration": 30,
        "timezone": "Asia/Kolkata",
        "settings": {
            "join_before_host": True
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        meeting = response.json()
        print("✅ Zoom Meeting Created!")
        print("📅 Topic:", meeting['topic'])
        print("🕒 Start:", meeting['start_time'])
        print("🔗 Join URL:", meeting['join_url'])
    else:
        print("❌ Failed to create meeting:", response.status_code, response.text)

# ---- Main Flow ----
try:
    token = load_token()

    if is_token_expired(token):
        token = refresh_access_token(token)
        save_token(token)
    else:
        print("✅ Access token is still valid.")

    create_zoom_meeting(token['access_token'])

except Exception as e:
    print("⚠️ Error:", str(e))
