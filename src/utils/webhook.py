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


def get_webhooks(CLIENT_ID: str, ACCESS_TOKEN: str):
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.get("https://api.twitch.tv/helix/webhooks/subscriptions", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve webhooks:", response.status_code, response.text)
        return None
    

if __name__ == "__main__":
    from sys import argv

    CLIENT_ID = argv[1]
    ACCESS_TOKEN = argv[2]

    print(get_webhooks(CLIENT_ID, ACCESS_TOKEN))
