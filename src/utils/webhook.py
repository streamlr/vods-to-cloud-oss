import requests

def register_webhook(CLIENT_ID: str, ACCESS_TOKEN: str, BROADCASTER_ID: str, WEBHOOK_PATH: str = "http://127.0.0.1:5000/webhook"):
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "type": "stream.offline",
        "version": "1",
        "condition": {
            "broadcaster_user_id": BROADCASTER_ID
        },
        "transport": {
            "method": "webhook",
            "callback": WEBHOOK_PATH
        }
    }

    response = requests.post(WEBHOOK_PATH, headers=headers, json=body)

    if response.status_code == 200:
        print("Webhook registered successfully.")
    else:
        print("Failed to register webhook:", response.status_code, response.text)
